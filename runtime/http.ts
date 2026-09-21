import {createHash,timingSafeEqual} from 'node:crypto';
import type { GenesisService } from './service.ts';
export function isOperator(request:Request,secret:string){const token=request.headers.get('authorization')?.replace(/^Bearer /,'')??'';return token.length<=500&&timingSafeEqual(createHash('sha256').update(token).digest(),createHash('sha256').update(secret).digest());}
const json=(value:unknown,status=200)=>Response.json(value,{status,headers:{'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});
export async function handleRequest(request:Request,service:GenesisService):Promise<Response>{
 const url=new URL(request.url),operator=isOperator(request,service.config.operatorToken);
 try{
  if(request.method==='GET'){
   if(url.pathname==='/healthz'){await service.extension.assertDormant();return json({ok:true,executionLock:'CLOSED',workers:'OFF'});}
   if(url.pathname==='/api/state')return json(await service.observe(operator));
   if(url.pathname==='/api/brain')return json(service.graph());
   if(url.pathname==='/api/history')return json(await service.history(url.searchParams.get('id')??undefined));
   if(url.pathname==='/api/replay'){
    const id=url.searchParams.get('id');if(!id||id.length>100)return json({error:'Invalid replay ID'},400);
    const replay=await service.replay(id);return json({replay},replay?200:404);
   }
   return json({error:'Not found'},404);
  }
  if(request.method!=='POST')return json({error:'Method not allowed'},405);
  if(!operator)return json({error:'Operator authorization required'},401);
  const origin=request.headers.get('origin');if(origin&&!service.config.allowedOrigins.includes(origin))return json({error:'Origin not allowed'},403);
  // No control endpoint can unlock or alter schedule; all callers share this gate.
  if(url.pathname==='/api/cycle'||url.pathname==='/api/control'){await service.extension.assertExecutionAllowed();}
  return json({error:'Not found'},404);
 }catch(e){if(e instanceof Error&&e.message.startsWith('GENESIS_EXECUTION'))return json({error:e.message},423);return json({error:'Read-only runtime unavailable; no state changed'},503);}
}

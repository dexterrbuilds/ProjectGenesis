import {developmentPreviewEnabled} from '@/lib/awakening';
export const dynamic='force-dynamic';
export async function GET(_request:Request,{params}:{params:Promise<{kind:string}>}){
 if(!developmentPreviewEnabled(process.env))return Response.json({error:'Not found'},{status:404});
 const {kind}=await params;
 if(kind==='graph'){const {default:data}=await import('@/data/connectome.json');return Response.json({id:'celegans-cook2019-rate-v1',nodes:data.neurons,edges:data.edges},{headers:{'Cache-Control':'no-store'}});}
 if(kind==='replay'){
  // Genuine saved activity from the existing sanitized fixture; no neural execution or inferred timestamp.
  const {default:fixture}=await import('@/tests/fixtures/genesis-dormant-sanitized.json');
  return Response.json({replay:{id:'fixture-saved-snapshot',at:null,modelId:fixture.brain.adapter,frames:[{tick:fixture.brain.payload.tick,activity:fixture.brain.payload.activity}],fixture:true}},{headers:{'Cache-Control':'no-store'}});
 }
 return Response.json({error:'Not found'},{status:404});
}

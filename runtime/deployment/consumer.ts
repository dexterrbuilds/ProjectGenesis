/** Explicit private consumer of EXISTING authority. Does not issue authority or events. */
import type pg from 'pg';
import {z} from 'zod';
import {OperatorAuthentication,type Principal} from '../../server/operator-auth.ts';
import {OperatorControl} from '../../server/operator-control.ts';
import {OneShotController} from '../../server/one-shot.ts';
import {ContinuousController} from '../../server/continuous.ts';
import {ContinuousWorker} from '../../server/continuous-worker.ts';
import {ProductFallback} from '../../core/v2/planner.ts';
import {digest} from '../../core/v2/identity.ts';
import {runtimeIdentity} from '../../server/one-shot-spec.ts';
import {requireRole} from './schema.ts';
import {inspectReadiness} from './readiness.ts';
import type {ReasoningOptions} from '../../server/reasoning/control.ts';
const id=z.string().min(1).max(100),hash=z.string().regex(/^[a-f0-9]{64}$/);
export const consumerRequest=z.object({version:z.literal(1),id,mode:z.enum(['one-shot','continuous-local']),organismId:id,bornAt:z.string().datetime(),runtimeHash:hash,targetId:id,authorityRowHash:hash,admissionId:id.nullable(),reviewReference:id,maximumSessionMs:z.number().int().min(1).max(240000)}).strict();
export async function consumeExisting(input:unknown,operatorPool:pg.Pool,workerPool:pg.Pool,auth:OperatorAuthentication,principal:Principal,signal:AbortSignal,fixtureOptions?:Pick<ReasoningOptions,'secretResolver'|'fixtureScenario'|'onFixtureSend'>){
 const q=consumerRequest.parse(input);auth.assert(principal);
 if(signal.aborted||q.runtimeHash!==runtimeIdentity().sha256||!(await inspectReadiness(operatorPool,q)).ready)throw Error('CONSUMER_PREFLIGHT_REFUSED');
 for(const [pool,role] of [[operatorPool,'operator'],[workerPool,'worker']] as const){const c=await pool.connect();try{await requireRole(c,role);}finally{c.release();}}
 const a=(await operatorPool.query('SELECT current_database() db,current_schema() schema,inet_server_addr() host,inet_server_port() port')).rows[0],b=(await workerPool.query('SELECT current_database() db,current_schema() schema,inet_server_addr() host,inet_server_port() port')).rows[0];if(digest(a)!==digest(b))throw Error('CONSUMER_DATABASE_MISMATCH');
 const op=new OperatorControl(operatorPool,auth),result=await op.execute(principal,{id:q.id,organismId:q.organismId,operation:q.mode==='one-shot'?'inspect_grant':'inspect_scopes',targetId:q.mode==='one-shot'?q.targetId:null,expectedHash:null,reasonReference:q.reviewReference,payload:null});
 // Durable inspection command ID is also the single-use launch receipt. Restart cannot reuse it.
 const r=result as unknown as {record:Record<string,unknown>;hash:string}|{record:Record<string,unknown>;hash:string}[];
 const authority=Array.isArray(r)?r.find(x=>x.record.id===q.targetId):r;
 if(!authority||authority.hash!==q.authorityRowHash||authority.record.status!=='AUTHORIZED'||signal.aborted)throw Error('AUTHORITY_CHANGED');
 if(q.mode==='one-shot'){
 const h=new OneShotController(workerPool);let fence:Awaited<ReturnType<OneShotController['claim']>>|undefined;
 try{
 fence=await h.claim(q.targetId);const g=await h.check(fence);
 const selected=g.permission.llm?(q.admissionId?await h.admittedReasoningPlanner(fence,{admissionId:q.admissionId,owner:q.id,...fixtureOptions}):(()=>{throw Error('ADMISSION_REQUIRED');})()):{identity:'product-deterministic-v1',planner:new ProductFallback()};
 if(!g.permission.llm&&(q.admissionId||g.planner.identity!=='product-deterministic-v1'))throw Error('LOCAL_PLANNER_IDENTITY_MISMATCH');
 const abort=()=>{if(fence)void h.cancel(fence).catch(()=>{});};signal.addEventListener('abort',abort,{once:true});const timer=setTimeout(abort,q.maximumSessionMs);
 try{if(signal.aborted)throw Error('CANCELLED');const p=await h.prepare(fence,selected);if(signal.aborted)throw Error('CANCELLED');await h.journal(fence,p.decision);const d=await h.commit(fence,p);return {status:'COMMITTED',cycle:d.cycle};}finally{clearTimeout(timer);signal.removeEventListener('abort',abort);}
 }catch{if(fence)await h.fail(fence);throw Error('CONSUMER_STOPPED_INSPECT_DURABLE_STATE');}
 }
 if(q.admissionId||fixtureOptions)throw Error('LOCAL_SCOPE_ONLY');
 const payload=authority.record.payload as {planner?:{identity?:string}};if(payload.planner?.identity!=='product-deterministic-v1')throw Error('LOCAL_PLANNER_IDENTITY_MISMATCH');
 const worker=new ContinuousWorker(new ContinuousController(workerPool),q.targetId,{identity:'product-deterministic-v1',planner:new ProductFallback()},true,1000);
 const abort=new AbortController(),stop=()=>abort.abort();signal.addEventListener('abort',stop,{once:true});const timer=setTimeout(stop,q.maximumSessionMs);let ticks=0;
 try{while(!abort.signal.aborted){auth.assert(principal);const actor=(await operatorPool.query('SELECT enabled,capabilities FROM genesis_operator_actors WHERE id=$1',[principal.actorId])).rows[0];if(!actor?.enabled||!actor.capabilities.includes('MANAGE_CONTINUOUS'))throw Error('OPERATOR_REVOKED');if(!(await inspectReadiness(operatorPool,q)).ready)throw Error('DEPLOYMENT_CHANGED');
 const row=(await workerPool.query('SELECT status FROM genesis_continuous_scopes WHERE id=$1',[q.targetId])).rows[0];if(row?.status!=='AUTHORIZED')break;
 await worker.tick(abort.signal);ticks++;if(!abort.signal.aborted)await new Promise<void>(resolve=>{const t=setTimeout(done,1000);function done(){clearTimeout(t);abort.signal.removeEventListener('abort',done);resolve();}abort.signal.addEventListener('abort',done,{once:true});});}
 return {status:'STOPPED',ticks};
 }finally{clearTimeout(timer);signal.removeEventListener('abort',stop);}
}

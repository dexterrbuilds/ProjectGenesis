/** Production reasoning path behind ProviderControl. No retries; no authority issuance. */
import type pg from 'pg';
import {randomUUID} from 'node:crypto';
import {digest} from '../../core/v2/identity.ts';
import {credentialLike} from '../../core/v2/memory.ts';
import {InterruptedCycle} from '../../core/v2/cycle.ts';
import {validateProposal} from '../../core/v2/planner.ts';
import type {WorkingContext,Proposal,PlannerV2} from '../../core/v2/contracts.ts';
import type {CycleFence} from '../commit-v2.ts';
import {checkProviderDisclosure} from '../provider-disclosure.ts';
import {buildRequest,cost,type ReasoningRequest} from './request.ts';
import {loadAdmission,fixtureTarget} from './store.ts';
import {resolveAdapter,type FixtureScenario} from './factory.ts';
import {environmentSecrets,noSecret,outputSchema,replySchema,ReasoningError,type SecretResolver,type Admission} from './contracts.ts';
export type ReasoningOptions={admissionId:string;owner:string;secretResolver?:SecretResolver;fixtureScenario?:FixtureScenario;onFixtureSend?:()=>void};
export class ReasoningControl{
 private pool:pg.Pool;private check:(f:CycleFence)=>Promise<void>;
 constructor(pool:pg.Pool,check:(f:CycleFence)=>Promise<void>){this.pool=pool;this.check=check;}
 async tx<T>(fn:(c:pg.PoolClient)=>Promise<T>){const c=await this.pool.connect();try{await c.query('BEGIN');await c.query("SELECT pg_advisory_xact_lock(hashtext('genesis-provider-budget-v1'))");const r=await fn(c);await c.query('COMMIT');return r;}catch(e){await c.query('ROLLBACK');throw e;}finally{c.release();}}
 async validate(f:CycleFence,c:WorkingContext,a:Admission){await this.check(f);await checkProviderDisclosure(this.pool,c);const now=await loadAdmission(this.pool,a.id,c.organismId);if(digest(now)!==digest(a)||c.hash!==digest(c.text)||!c.permission.llm||c.permission.maxAttempts!==1||c.manifest.stateRevision!==f.lifeRevision)throw new ReasoningError('ADMISSION_MISMATCH');}
 async replay(id:string,f:CycleFence,c:WorkingContext,a:Admission):Promise<Proposal>{
  await this.validate(f,c,a);const r=(await this.pool.query('SELECT record FROM genesis_provider_attempts WHERE id=$1',[id])).rows[0]?.record;
  const receipt=(await this.pool.query('SELECT * FROM genesis_provider_receipts WHERE attempt_id=$1',[id])).rows[0];
  if(!r||r.status!=='received'||r.context.hash!==c.hash||digest(r.fence)!==digest(f)||!receipt||receipt.request_hash!==r.request.hash||receipt.admission_hash!==digest(a)||receipt.record.validation!=='SCHEMA_VALID'||!receipt.record.proposal||receipt.record.proposalHash!==digest(receipt.record.proposal)||r.costMicros===null)throw new ReasoningError('ADMISSION_MISMATCH');
  const {hash:storedHash,...payload}=r.request;if(storedHash!==digest(payload)||r.request.wireHash!==digest(r.request.wire)||r.request.wire!==buildRequest(a,c,f,r.request.requestedAt).wire||digest(r.context.manifest)!==digest(c.manifest))throw new ReasoningError('ADMISSION_MISMATCH');
  const p=validateProposal(receipt.record.proposal,c);if(p.planner!=='provider:'+a.provider+':'+a.model)throw new ReasoningError('ADMISSION_MISMATCH');return p;
 }
 planner(f:CycleFence,o:ReasoningOptions):PlannerV2{return {propose:async c=>{try{return await this.propose(f,c,o);}catch{throw new InterruptedCycle('PROVIDER_REASONING_STOPPED_REVIEW_REQUIRED');}}};}
 async propose(f:CycleFence,c:WorkingContext,o:ReasoningOptions):Promise<Proposal>{
  const a=await loadAdmission(this.pool,o.admissionId,c.organismId);await this.validate(f,c,a);
  const id=f.cycleId+':reasoning';const existing=(await this.pool.query('SELECT record FROM genesis_provider_attempts WHERE id=$1',[id])).rows[0];
  if(existing)return this.replay(id,f,c,a); // ONLY durable receipt; every other state stops, never dispatches again.
  const fixture=await fixtureTarget(this.pool);if((o.fixtureScenario||o.onFixtureSend||o.secretResolver)&&!fixture)throw new ReasoningError('CONFIGURATION');
  const resolver=o.secretResolver??environmentSecrets;let secret:string;try{secret=await resolver.resolve(a.secretReference);if(typeof secret!=='string'||secret.length<16||secret.length>4096||/[\r\n]/.test(secret))throw Error();}catch{throw new ReasoningError('CONFIGURATION');}
  noSecret(c,secret);const request=buildRequest(a,c,f,new Date().toISOString());noSecret(request,secret);
  if(!o.owner||o.owner.length>150||credentialLike(o.owner)||o.owner===secret)throw new ReasoningError('CONFIGURATION');
  const adapter=resolveAdapter(a,fixture,o.fixtureScenario,o.onFixtureSend);const leaseUntil=new Date(Date.now()+a.timeoutMs+5000).toISOString();
  await this.tx(async db=>{
   const rows=(await db.query("SELECT record,cycle_id FROM genesis_provider_attempts WHERE (at AT TIME ZONE 'UTC')::date=(now() AT TIME ZONE 'UTC')::date OR record->>'status' IN ('reserved','dispatching','unknown')")).rows;
   if((await db.query('SELECT 1 FROM genesis_provider_attempts WHERE cycle_id=$1',[f.cycleId])).rowCount)throw new ReasoningError('CONFIGURATION');
   const liability=rows.reduce((s,r)=>{const n=r.record.costMicros??r.record.reservedMicros;if(!Number.isSafeInteger(n)||n<0)throw new ReasoningError('USAGE_UNKNOWN');return s+n;},0);
   if(liability+request.reservationMicros>a.dailyMicros)throw new ReasoningError('CONFIGURATION');
   await db.query('INSERT INTO genesis_provider_attempts(id,cycle_id,grant_id,record) VALUES($1,$2,$3,$4)',[id,f.cycleId,a.id,{protocolVersion:2,status:'reserved',owner:o.owner,leaseUntil,fence:f,context:c,contextHash:c.hash,request,admissionHash:digest(a),model:a.model,reservedMicros:request.reservationMicros,costMicros:null,usage:null,response:null}]);
  });
  let sent=false;const abort=new AbortController();let timer:ReturnType<typeof setTimeout>|undefined,poll:ReturnType<typeof setInterval>|undefined;
  try{
   await this.validate(f,c,a);
   const changed=await this.pool.query("UPDATE genesis_provider_attempts SET record=record || $2::jsonb WHERE id=$1 AND record->>'status'='reserved' AND record->>'owner'=$3 AND (record->>'leaseUntil')::timestamptz>now()",[id,JSON.stringify({status:'dispatching',dispatchAt:new Date().toISOString()}),o.owner]);if(changed.rowCount!==1)throw new ReasoningError('ADMISSION_MISMATCH');
   await this.validate(f,c,a);sent=true;
   timer=setTimeout(()=>abort.abort(),a.timeoutMs);poll=setInterval(()=>{void this.validate(f,c,a).catch(()=>abort.abort());},50);
   const cancelled=new Promise<never>((_,reject)=>abort.signal.addEventListener('abort',()=>reject(new ReasoningError('CANCEL_UNCONFIRMED')),{once:true}));
   const raw=await Promise.race([adapter.send(request.wire,secret,abort.signal),cancelled]);
   noSecret(raw,secret);const reply=replySchema.parse(raw);if(reply.model!==a.model||reply.admissionHash!==digest(a)||credentialLike(JSON.stringify([reply.responseId,reply.requestId,reply.usage])))throw new ReasoningError('ADMISSION_MISMATCH');
   let amount:number|null=null;try{if(reply.usage){if(reply.usage.input>request.accounting.inputBound||reply.usage.output>a.maximumOutputTokens)throw Error();amount=cost(a,reply.usage);}if(amount!==null&&amount>request.reservationMicros)amount=null;}catch{amount=null;}
   let proposal:Proposal|null=null;try{const structured=typeof reply.structured==='string'?JSON.parse(reply.structured):reply.structured;const p=outputSchema.parse(structured);if(credentialLike(JSON.stringify(p))||p.planner!=='provider:'+a.provider+':'+a.model)throw Error();proposal=validateProposal(p,c);}catch{/* Only hash and rejection metadata for malformed bodies; never store hidden content. */}
   const record={responseId:reply.responseId,providerRequestId:reply.requestId,requestHash:request.hash,admissionHash:digest(a),responseHash:digest(raw),proposal,proposalHash:proposal?digest(proposal):null,usage:reply.usage,costMicros:amount,validation:proposal?'SCHEMA_VALID':'REJECTED',receivedAt:new Date().toISOString()};
   await this.tx(async db=>{
    const current=(await db.query('SELECT record FROM genesis_provider_attempts WHERE id=$1 FOR UPDATE',[id])).rows[0]?.record;if(current?.status!=='dispatching'||current.owner!==o.owner||current.request.hash!==request.hash||Date.parse(current.leaseUntil)<=Date.now())throw new ReasoningError('ADMISSION_MISMATCH');
    await db.query('INSERT INTO genesis_provider_receipts(attempt_id,provider,response_id,request_hash,admission_hash,record) VALUES($1,$2,$3,$4,$5,$6)',[id,a.provider,reply.responseId,request.hash,digest(a),record]);
    await db.query('UPDATE genesis_provider_attempts SET record=record || $2::jsonb WHERE id=$1',[id,JSON.stringify({status:amount===null?'unknown':'received',costMicros:amount,usage:reply.usage,response:{id:reply.responseId,requestId:reply.requestId,proposalHash:record.proposalHash},receivedAt:record.receivedAt})]);
   });
   if(!proposal||amount===null)throw new ReasoningError(proposal?'USAGE_UNKNOWN':'SCHEMA_VIOLATION');
   return await this.replay(id,f,c,a);
  }catch(e){
   const cancellation=abort.signal.aborted?await adapter.cancel().catch(()=> 'SUPPORTED_UNCONFIRMED' as const):null;
   const code=e instanceof ReasoningError?e.category:'MALFORMED_RESPONSE';
   await this.pool.query("UPDATE genesis_provider_attempts SET record=record || $2::jsonb WHERE id=$1 AND record->>'status' IN ('reserved','dispatching') AND record->>'owner'=$3",[id,JSON.stringify({status:sent?'unknown':'not_sent',costMicros:sent?null:0,errorCode:code,cancellation}),o.owner]);
   throw new ReasoningError(code);
  }finally{if(timer)clearTimeout(timer);if(poll)clearInterval(poll);}
 }
}
export const processOwner=()=> 'worker:'+randomUUID();
export type {ReasoningRequest};

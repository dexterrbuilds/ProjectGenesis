import {ReasoningControl,type ReasoningOptions} from './reasoning/control.ts';
import {checkProviderDisclosure} from './provider-disclosure.ts';
import type pg from 'pg';
import {digest} from '../core/v2/identity.ts';
import {validateProposal} from '../core/v2/planner.ts';
import type {PlannerV2,WorkingContext,Proposal} from '../core/v2/contracts.ts';
import type {CycleFence} from './commit-v2.ts';
export type ModelGrant={id:string;enabled:boolean;model:string;pricingEvidence:string;inputMicrosPerToken:number;outputMicrosPerToken:number;maxInputTokens:number;maxOutputTokens:number;perCallMicros:number;perCycleMicros:number;dailyMicros:number;maxAttempts:number;timeoutMs:number;expiresAt:string};
export type ProviderRequest={attemptId:string;contextHash:string;revision:number;model:string;input:string;maxOutputTokens:number;signal:AbortSignal};
export type ProviderReply={id:string;model:string;proposal:unknown;usage:{inputTokens:number;outputTokens:number};requestId:string};
export type ProviderTransport=(request:ProviderRequest)=>Promise<ProviderReply>;
export type TokenCounter={provenance:string;model:string;count:(completeInput:string)=>number};
export class ProviderControl {
 constructor(pool:pg.Pool,check:(f:CycleFence)=>Promise<void>){this.pool=pool;this.check=check;}
 private pool:pg.Pool;private check:(f:CycleFence)=>Promise<void>;
 private async transaction<T>(fn:(c:pg.PoolClient)=>Promise<T>){const c=await this.pool.connect();try{await c.query('BEGIN');await c.query("SELECT pg_advisory_xact_lock(hashtext('genesis-provider-budget-v1'))");const result=await fn(c);await c.query('COMMIT');return result;}catch(e){await c.query('ROLLBACK');throw e;}finally{c.release();}}
 async grant(id:string):Promise<ModelGrant>{const g=(await this.pool.query('SELECT record FROM genesis_provider_grants WHERE id=$1',[id])).rows[0]?.record as ModelGrant|undefined;
  if(!g?.enabled||g.id!==id||!g.model||!g.pricingEvidence||!Number.isFinite(Date.parse(g.expiresAt))||Date.parse(g.expiresAt)<=Date.now())throw new Error('PROVIDER_DISABLED_OR_EXPIRED');
  for(const k of ['inputMicrosPerToken','outputMicrosPerToken','maxInputTokens','maxOutputTokens','perCallMicros','perCycleMicros','dailyMicros','maxAttempts','timeoutMs'] as const)if(!Number.isSafeInteger(g[k])||g[k]<1)throw new Error('Invalid reviewed provider limits');return g;
 }
 async reserve(id:string,grantId:string,f:CycleFence,context:WorkingContext,counter:TokenCounter){
  if(!context.permission.llm||!context.permission.execution||context.permission.maxAttempts<1||context.permission.maxCostMicros<1||context.hash!==digest(context.text)||context.manifest.stateRevision!==f.lifeRevision)throw new Error('Provider permission/context mismatch');
  await this.check(f);await checkProviderDisclosure(this.pool,context);
  return this.transaction(async c=>{
   const g=await this.grant(grantId);
   if(counter.model!==g.model||!counter.provenance)throw new Error('Reviewed model-compatible token counter required');
   const inputTokens=counter.count(context.text);if(!Number.isSafeInteger(inputTokens)||inputTokens<1||inputTokens>g.maxInputTokens)throw new Error('Input token ceiling');
   const reserve=inputTokens*g.inputMicrosPerToken+g.maxOutputTokens*g.outputMicrosPerToken;
   if(!Number.isSafeInteger(reserve)||reserve>g.perCallMicros||reserve>context.permission.maxCostMicros)throw new Error('Per-call budget exceeded');
   const rows=(await c.query('SELECT record,cycle_id FROM genesis_provider_attempts WHERE ((at AT TIME ZONE \'UTC\')::date=(now() AT TIME ZONE \'UTC\')::date OR record->>\'status\' IN (\'reserved\',\'dispatching\',\'unknown\'))',[])).rows;
   // Unknown/in-flight liabilities survive midnight; no timeout releases their reservation.
   const liability=(r:{record:{costMicros:number|null;reservedMicros:number}})=>r.record.costMicros??r.record.reservedMicros;
   const cycleRows=(await c.query('SELECT record FROM genesis_provider_attempts WHERE cycle_id=$1',[f.cycleId])).rows;
   if(cycleRows.some(r=>['unknown','dispatching','reserved'].includes(r.record.status)))throw new Error('Ambiguous/in-flight attempt cannot retry');
   if(cycleRows.length>=Math.min(g.maxAttempts,context.permission.maxAttempts)||cycleRows.reduce((s,r)=>s+liability(r),0)+reserve>Math.min(g.perCycleMicros,context.permission.maxCostMicros)||rows.reduce((s,r)=>s+liability(r),0)+reserve>g.dailyMicros)throw new Error('Provider cycle/daily/attempt budget exhausted');
   const record={status:'reserved',fence:f,contextHash:context.hash,revision:f.lifeRevision,model:g.model,grantHash:digest(g),inputTokenCeiling:inputTokens,maxOutputTokens:g.maxOutputTokens,reservedMicros:reserve,costMicros:null,usage:null,response:null,counterProvenance:counter.provenance};
   await c.query('INSERT INTO genesis_provider_attempts(id,cycle_id,grant_id,record) VALUES($1,$2,$3,$4)',[id,f.cycleId,grantId,record]);return g;
  });
 }
 async dispatch(id:string,grantId:string,f:CycleFence,context:WorkingContext,g:ModelGrant,transport:ProviderTransport):Promise<Proposal>{
  if(context.hash!==digest(context.text)||context.manifest.stateRevision!==f.lifeRevision)throw new Error('Dispatch context mismatch');
  const bound=(await this.pool.query('SELECT record,cycle_id,grant_id FROM genesis_provider_attempts WHERE id=$1',[id])).rows[0];
  if(!bound||bound.cycle_id!==f.cycleId||bound.grant_id!==grantId||digest(bound.record.fence)!==digest(f)||bound.record.contextHash!==context.hash||bound.record.grantHash!==digest(g))throw new Error('Dispatch attempt binding mismatch');
  const controller=new AbortController();let timer:ReturnType<typeof setTimeout>|undefined;let poll:ReturnType<typeof setInterval>|undefined;let sent=false;
  try{
   await this.check(f);if(digest(await this.grant(grantId))!==digest(g))throw new Error('Provider grant changed');
   const updated=await this.pool.query("UPDATE genesis_provider_attempts SET record=jsonb_set(record,'{status}','\"dispatching\"') WHERE id=$1 AND record->>'status'='reserved' AND record->>'contextHash'=$2 AND record->>'grantHash'=$3 RETURNING record",[id,context.hash,digest(g)]);
   if(updated.rowCount!==1)throw new Error('Attempt already dispatched or binding mismatch');
   await this.check(f);await checkProviderDisclosure(this.pool,context);sent=true;
   const abort=new Promise<never>((_,reject)=>controller.signal.addEventListener('abort',()=>reject(new Error('Provider cancelled/timeout; remote outcome unknown')),{once:true}));
   timer=setTimeout(()=>controller.abort(),g.timeoutMs);
   poll=setInterval(()=>{void Promise.all([this.check(f),this.grant(grantId).then(current=>{if(digest(current)!==digest(g))throw new Error('Revoked');})]).catch(()=>controller.abort());},20);
   const reply=await Promise.race([transport({attemptId:id,contextHash:context.hash,revision:f.lifeRevision,model:g.model,input:context.text,maxOutputTokens:g.maxOutputTokens,signal:controller.signal}),abort]);
   const row=(await this.pool.query('SELECT record FROM genesis_provider_attempts WHERE id=$1',[id])).rows[0].record;
   if(reply.model!==g.model||!reply.id||!reply.requestId||![reply.usage.inputTokens,reply.usage.outputTokens].every(x=>Number.isSafeInteger(x)&&x>=0)||reply.usage.inputTokens>row.inputTokenCeiling||reply.usage.outputTokens>g.maxOutputTokens)throw new Error('Unreconciled response identity/usage');
   const cost=reply.usage.inputTokens*g.inputMicrosPerToken+reply.usage.outputTokens*g.outputMicrosPerToken;
   // Record billing evidence even if authority was revoked while the request ran.
   const settled=await this.pool.query("UPDATE genesis_provider_attempts SET record=record || $2::jsonb WHERE id=$1 AND record->>'status'='dispatching'",[id,JSON.stringify({status:'received',costMicros:cost,usage:reply.usage,response:{id:reply.id,requestId:reply.requestId,model:reply.model,contextHash:context.hash,proposalHash:digest(reply.proposal)}})]);
   if(settled.rowCount!==1)throw new Error('Concurrent recovery/reconciliation; reply not admitted');
   await this.check(f);if(digest(await this.grant(grantId))!==digest(g))throw new Error('Provider revoked before acceptance');
   return validateProposal({...reply.proposal as object,planner:`provider:${g.model}:${id}`},context);
  }catch{
   // Raw errors may contain credentials or provider bodies. Retain only bounded status.
   await this.pool.query("UPDATE genesis_provider_attempts SET record=record || $2::jsonb WHERE id=$1 AND record->>'status' IN ('reserved','dispatching')",[id,JSON.stringify({status:sent?'unknown':'not_sent',costMicros:sent?null:0,errorCode:sent?'PROVIDER_OUTCOME_UNKNOWN':'REQUEST_NOT_SENT'})]);
   throw new Error(sent?'PROVIDER_ATTEMPT_FAILED_OR_UNKNOWN':'PROVIDER_REQUEST_NOT_SENT');
  }finally{if(timer)clearTimeout(timer);if(poll)clearInterval(poll);}
 }
 reasoningPlanner(f:CycleFence,o:ReasoningOptions){return new ReasoningControl(this.pool,this.check).planner(f,o);}
 async recover(){
  // A crashed request may have reached the provider. Never fabricate success or retry.
  await this.pool.query("UPDATE genesis_provider_attempts SET record=record || '{\"status\":\"unknown\",\"costMicros\":null}'::jsonb WHERE record->>'status' IN ('reserved','dispatching') AND (record->>'protocolVersion' IS DISTINCT FROM '2' OR (record->>'leaseUntil')::timestamptz<=now())");
 }
 async reconcile(id:string,evidence:{operator:string;reference:string;costMicros:number}){
  if(!evidence.operator||!evidence.reference||!Number.isSafeInteger(evidence.costMicros)||evidence.costMicros<0)throw new Error('Reviewed reconciliation evidence required');
  await this.transaction(async c=>{const row=(await c.query('SELECT record FROM genesis_provider_attempts WHERE id=$1 FOR UPDATE',[id])).rows[0];if(!row||row.record.status!=='unknown'||evidence.costMicros>row.record.reservedMicros)throw new Error('Manual investigation required');await c.query('UPDATE genesis_provider_attempts SET record=record || $2::jsonb WHERE id=$1',[id,JSON.stringify({status:'reconciled',costMicros:evidence.costMicros,reconciliation:evidence})]);});
 }
 planner(grantId:string,f:CycleFence,id:string,counter:TokenCounter,transport:ProviderTransport):PlannerV2{return {propose:async c=>{const g=await this.reserve(id,grantId,f,c,counter);return this.dispatch(id,grantId,f,c,g,transport);}};}
}

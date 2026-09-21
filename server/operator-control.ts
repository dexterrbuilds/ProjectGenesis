import {compatibleAdmission} from './reasoning/store.ts';
/** Private capability boundary. No execution operation, planner callback, SQL input or worker start. */
import type pg from 'pg';
import {readFileSync} from 'node:fs';
import {z} from 'zod';
import {digest} from '../core/v2/identity.ts';
import {credentialLike} from '../core/v2/memory.ts';
import {AUDIENCES} from '../core/v2/disclosure.ts';
import {OperatorAuthentication,type Principal,type Capability} from './operator-auth.ts';
import {OneShotController} from './one-shot.ts';
import {ContinuousController} from './continuous.ts';
import {validateGrant,runtimeIdentity} from './one-shot-spec.ts';
import {validateScope} from './continuous-spec.ts';
import {recordHumanResponse} from './assistance-intake.ts';
import {inspectOneShot} from './cycle-inspection.ts';
import {ProviderControl} from './provider-control.ts';
import {readMemoryArchive} from './memory-store.ts';
import {disclosureSources,loadDisclosure} from './disclosure-store.ts';
import {transactionBoundPool} from './operator-transaction.ts';
const rowHash=(v:unknown)=>digest(JSON.parse(JSON.stringify(v)));
const id=z.string().min(1).max(180).regex(/^[a-zA-Z0-9][a-zA-Z0-9:._/-]*$/),hash=z.string().regex(/^[a-f0-9]{64}$/);
const OPERATIONS={readiness:'VIEW_PRIVATE_STATE',inspect_state:'VIEW_PRIVATE_STATE',inspect_source:'VIEW_PRIVATE_STATE',inspect_grant:'MANAGE_ONE_SHOT',propose_grant:'MANAGE_ONE_SHOT',authorize_grant:'MANAGE_ONE_SHOT',revoke_grant:'MANAGE_ONE_SHOT',cancel_grant:'MANAGE_ONE_SHOT',inspect_attempt:'INSPECT_RECOVERY',inspect_recovery:'INSPECT_RECOVERY',mark_expired_claim:'RESOLVE_RECOVERY',inspect_scopes:'MANAGE_CONTINUOUS',inspect_queue:'MANAGE_CONTINUOUS',propose_scope:'MANAGE_CONTINUOUS',authorize_scope:'MANAGE_CONTINUOUS',revoke_scope:'MANAGE_CONTINUOUS',cancel_event:'MANAGE_CONTINUOUS',emergency_stop:'MANAGE_ONE_SHOT',human_response:'RECORD_HUMAN_RESPONSE',disclosure_sources:'REVIEW_DISCLOSURE',review_disclosure:'REVIEW_DISCLOSURE',inspect_disclosure:'REVIEW_DISCLOSURE',recovery_disposition:'RESOLVE_RECOVERY',provider_reconcile:'RESOLVE_RECOVERY',provider_readiness:'MANAGE_PROVIDER_ADMISSION',propose_provider:'MANAGE_PROVIDER_ADMISSION',admit_provider:'MANAGE_PROVIDER_ADMISSION',revoke_provider:'MANAGE_PROVIDER_ADMISSION',inspect_provider:'MANAGE_PROVIDER_ADMISSION',inspect_provider_attempt:'INSPECT_RECOVERY'} as const;
export const commandSchema=z.object({id,organismId:id,operation:z.enum(Object.keys(OPERATIONS) as [keyof typeof OPERATIONS,...(keyof typeof OPERATIONS)[]]),targetId:id.nullable(),expectedHash:hash.nullable(),reasonReference:id,payload:z.unknown()}).strict();
export type OperatorCommand=z.infer<typeof commandSchema>;
const reviewSchema=z.object({sourceType:id,sourceId:id,sourceHash:hash,audience:z.enum(AUDIENCES),decision:z.enum(['APPROVED','DENIED','REVOKED','EXPIRED']),expectedVersion:z.number().int().nonnegative(),expiresAt:z.string().datetime().nullable()}).strict();
const recoverySchema=z.object({targetType:z.enum(['one_shot','continuous']),disposition:z.enum(['CONFIRMED_NO_EXTERNAL_EFFECT','CONFIRMED_EXTERNAL_EFFECT_WITHOUT_LOCAL_COMMIT','CONFIRMED_LOCAL_COMMIT','UNRESOLVED_REMAIN_STOPPED']),evidenceHash:hash}).strict();
const reconciliationSchema=z.object({fact:z.enum(['PROVIDER_NOT_EXECUTED','PROVIDER_BILLED','PROVIDER_UNKNOWN']),costMicros:z.number().int().nonnegative().nullable(),usage:z.object({inputTokens:z.number().int().nonnegative(),outputTokens:z.number().int().nonnegative()}).strict().nullable(),responseId:id.nullable(),evidenceHash:hash}).strict();
export class OperatorControl{
 readonly pool:pg.Pool;readonly auth:OperatorAuthentication;
 constructor(pool:pg.Pool,auth:OperatorAuthentication){this.pool=pool;this.auth=auth;}
 async installFixtureSchema(){const r=(await this.pool.query('SELECT current_database() db,current_schema() schema')).rows[0];if(r.db!=='genesis_runtime_v1_test'||!r.schema.startsWith('awakening_test_'))throw Error('DISPOSABLE_OPERATOR_SCHEMA_REQUIRED');await this.pool.query(readFileSync(new URL('../runtime/operator-schema-v1.sql',import.meta.url),'utf8'));}
 /** Every operation, including private inspection and refusal, requires a durable audit.
  * No success is returned if either the administrative change or journal commit fails. */
 async execute(principal:Principal,raw:unknown){
  this.auth.assert(principal);const q=commandSchema.parse(raw),cap:Capability=OPERATIONS[q.operation];
  if(credentialLike(q.reasonReference)||credentialLike(q.id)||credentialLike(q.targetId??''))throw Error('OPERATOR_REFERENCE_REFUSED');
  const c=await this.pool.connect();let result:unknown=null,refused=false,previousHash:string|null=null;
  try{
   await c.query('BEGIN');
   if(principal.mode==='test'){const t=(await c.query('SELECT current_database() db,current_schema() schema')).rows[0];if(t.db!=='genesis_runtime_v1_test'||!t.schema.startsWith('awakening_test_'))throw Error('TEST_AUTH_TARGET_REFUSED');}
   const actor=(await c.query('SELECT enabled,capabilities FROM genesis_operator_actors WHERE id=$1',[principal.actorId])).rows[0];
   if(!actor?.enabled)throw Error('OPERATOR_AUTH_FAILED');
   const b=(await c.query("SELECT state FROM genesis_organisms WHERE id='genesis' FOR UPDATE")).rows[0];
   if(b?.state.id!==q.organismId)throw Error('OPERATOR_TARGET_REFUSED');
   await c.query("SELECT organism_id FROM genesis_control_state WHERE organism_id='genesis' FOR UPDATE");
   if((await c.query('SELECT id FROM genesis_operator_audit WHERE id=$1',[q.id])).rowCount)throw Error('OPERATOR_REQUEST_ALREADY_RECORDED');
   await c.query('SAVEPOINT control_operation');
   try{
    if(!actor.capabilities.includes(cap)||q.operation==='emergency_stop'&&!actor.capabilities.includes('MANAGE_CONTINUOUS'))throw Error('CAPABILITY_REQUIRED');
    this.auth.assert(principal);
    const p=transactionBoundPool(c),h=new OneShotController(p),continuous=new ContinuousController(p);
    const target=async(table:string)=>{const r=(await c.query(`SELECT * FROM ${table} WHERE id=$1 FOR UPDATE`,[q.targetId])).rows[0];if(!r)throw Error('TARGET_ABSENT');previousHash=rowHash(r);if(q.expectedHash!==previousHash)throw Error('STALE_OPERATOR_TARGET');return r;};
    switch(q.operation){
     case 'readiness':z.null().parse(q.payload);result={organismId:b.state.id,bornAt:b.state.bornAt,decisions:b.state.cycles,execution:(await c.query('SELECT record FROM genesis_life_state')).rows[0].record.executionLock,schedule:(await c.query('SELECT enabled FROM genesis_schedule')).rows[0].enabled,providerAdmission:'PENDING',executionAvailable:false};break;
     case 'inspect_state':z.null().parse(q.payload);result={identity:{id:b.state.id,name:b.state.name,bornAt:b.state.bornAt,cycles:b.state.cycles},life:(await c.query('SELECT record FROM genesis_life_state')).rows[0].record};break;
     case 'inspect_source':{const v=z.object({sourceType:id}).strict().parse(q.payload);const l=(await c.query('SELECT record,revision FROM genesis_life_state')).rows[0];const a=await readMemoryArchive(c,q.organismId,Number(l.revision));const source=disclosureSources(b.state,l.record,a).find(s=>s.type===v.sourceType&&s.id===q.targetId);if(!source||source.hash!==q.expectedHash||source.internalOnly)throw Error('SOURCE_PREVIEW_REFUSED');const memory=a.legacy.find((m):m is {id:string;text:string}=>!!m&&typeof m==='object'&&'id' in m&&m.id===source.id&&'text' in m&&typeof m.text==='string');result={source,untrusted:true,excerpt:source.type==='legacy_memory'&&memory?memory.text.slice(0,2000):null,excerptClipped:source.type==='legacy_memory'&&memory?memory.text.length>2000:false};break;}
     case 'inspect_grant':z.null().parse(q.payload);{const row=(await c.query('SELECT * FROM genesis_execution_grants WHERE id=$1',[q.targetId])).rows[0];result=row?{record:row,hash:rowHash(row)}:null;}break;
     case 'propose_grant':{const g=validateGrant(q.payload);if(g.organismId!==q.organismId||g.issuer!==principal.actorId||g.authorizationReference!==q.reasonReference||q.targetId!==g.id||q.expectedHash!==null)throw Error('GRANT_ATTRIBUTION_MISMATCH');await h.propose(g);result={id:g.id,status:'PROPOSED',payloadHash:digest(g)};break;}
     case 'authorize_grant':{z.null().parse(q.payload);const r=await target('genesis_execution_grants');await h.authorize(r.id,{payloadHash:r.payload_hash,issuer:r.payload.issuer,reference:r.payload.authorizationReference});result={id:r.id,status:'AUTHORIZED',executionStarted:false};break;}
     case 'revoke_grant':case 'cancel_grant':{z.null().parse(q.payload);const r=await target('genesis_execution_grants');await h.revoke(r.id,q.reasonReference);result={id:r.id,status:(await c.query('SELECT status FROM genesis_execution_grants WHERE id=$1',[r.id])).rows[0].status};break;}
     case 'mark_expired_claim':{z.null().parse(q.payload);const r=await target('genesis_execution_grants');await h.recoverExpired(r.id);result={status:'AMBIGUOUS',automaticRetry:false};break;}
     case 'inspect_attempt':z.null().parse(q.payload);result=await inspectOneShot(p,q.targetId!);break;
     case 'inspect_recovery':{z.null().parse(q.payload);const event=(await c.query('SELECT id,status,reason,cycle_id,payload_hash FROM genesis_runtime_events WHERE id=$1',[q.targetId])).rows[0]??null;
      const attempts=(await c.query('SELECT * FROM genesis_continuous_attempts WHERE event_id=$1 ORDER BY at DESC LIMIT 100',[q.targetId])).rows;
      const providers=event?(await c.query("SELECT id,record->>'status' AS status,record->'reservedMicros' AS reserved_micros,record->'costMicros' AS cost_micros FROM genesis_provider_attempts WHERE cycle_id=$1 ORDER BY id",[event.cycle_id])).rows:[];
      const decision=event?(await c.query('SELECT record FROM genesis_decisions WHERE id=$1',[event.cycle_id])).rows[0]?.record:null;
      const episode=event?(await c.query('SELECT record FROM genesis_life_events WHERE id=$1',[event.cycle_id+':episode'])).rows[0]?.record:null;
      const committed=!!(decision?.schemaVersion===2&&decision.organismId===q.organismId&&episode?.organismId===q.organismId&&episode?.source===event?.cycle_id&&decision.memory?.episode?.id===episode?.id);
      result={continuousEvent:event,continuousAttempts:attempts,associatedProviders:providers,canonicalCommit:{observed:committed,decisionRecordPresent:!!decision,episodeRecordPresent:!!episode},reviewRequired:event?.status==='AMBIGUOUS'||providers.some(p=>['reserved','dispatching','unknown'].includes(p.status)),dispositions:(await c.query('SELECT * FROM genesis_recovery_dispositions WHERE target_id=$1 ORDER BY at,id LIMIT 100',[q.targetId])).rows,provider:(await c.query('SELECT * FROM genesis_provider_attempts WHERE id=$1',[q.targetId])).rows.map(r=>({id:r.id,cycleId:r.cycle_id,hash:rowHash(r),status:r.record.status,costMicros:r.record.costMicros??null,reservedMicros:r.record.reservedMicros??null,responseIdentity:r.record.response?.id??null})),automaticRetry:false};break;}
     case 'inspect_scopes':z.null().parse(q.payload);result=(await c.query('SELECT * FROM genesis_continuous_scopes ORDER BY created_at DESC,id LIMIT 100')).rows.map(r=>({record:r,hash:rowHash(r)}));break;
     case 'inspect_queue':{z.null().parse(q.payload);const scopes=(await c.query('SELECT id,payload FROM genesis_continuous_scopes ORDER BY id LIMIT 100')).rows;const resources=await Promise.all(scopes.map(async s=>({scopeId:s.id,...await continuous.resources(c,validateScope(s.payload))})));result={resources,events:(await c.query('SELECT * FROM genesis_runtime_events ORDER BY available_at,id LIMIT 100')).rows.map(r=>({record:r,hash:rowHash(r)})),attempts:(await c.query('SELECT * FROM genesis_continuous_attempts ORDER BY at DESC LIMIT 100')).rows,scopes};break;}
     case 'propose_scope':{const s=validateScope(q.payload);if(s.organismId!==q.organismId||s.issuer!==principal.actorId||s.authorizationReference!==q.reasonReference||q.targetId!==s.id||q.expectedHash!==null)throw Error('SCOPE_ATTRIBUTION_MISMATCH');await continuous.proposeScope(s);result={id:s.id,status:'PROPOSED',payloadHash:digest(s)};break;}
     case 'authorize_scope':{z.null().parse(q.payload);const r=await target('genesis_continuous_scopes');await continuous.authorizeScope(r.id,{payloadHash:r.payload_hash,issuer:r.payload.issuer,reference:r.payload.authorizationReference});result={id:r.id,status:'AUTHORIZED',workerStarted:false};break;}
     case 'revoke_scope':{z.null().parse(q.payload);const r=await target('genesis_continuous_scopes');await continuous.revoke(r.id,q.reasonReference);result={id:r.id,status:'REVOKED_OR_REVIEW_REQUIRED'};break;}
     case 'cancel_event':{z.null().parse(q.payload);const r=await target('genesis_runtime_events');await continuous.cancelEvent(r.id,q.reasonReference);result={id:r.id,cancelled:true};break;}
     case 'emergency_stop':{
      z.null().parse(q.payload);const grants=(await c.query("SELECT id FROM genesis_execution_grants WHERE status IN ('PROPOSED','AUTHORIZED','CLAIMED') ORDER BY id")).rows;
      for(const r of grants)await h.revoke(r.id,q.reasonReference);
      const scopes=(await c.query("SELECT id FROM genesis_continuous_scopes WHERE status IN ('PROPOSED','AUTHORIZED') ORDER BY id")).rows;
      for(const r of scopes)await continuous.revoke(r.id,q.reasonReference);
      result={grantsRevoked:grants.map(x=>x.id),scopesRevoked:scopes.map(x=>x.id),pendingEventsPreserved:true,terminalAmbiguitiesPreserved:true,executionReopened:false,processSignal:'NOT_APPLICABLE_NO_MANAGED_WORKER'};break;
     }
     case 'human_response':{
      const v=z.object({response:z.unknown(),expectedRevision:z.number().int().nonnegative(),wake:z.boolean()}).strict().parse(q.payload);
      result=await recordHumanResponse(p,v.response,{organismId:q.organismId,expectedRevision:v.expectedRevision,operatorRef:principal.actorId,authorizationRef:q.reasonReference,scope:'RECORD_HUMAN_RESPONSE_ONLY',...(v.wake?{wake:'ENQUEUE_IF_INSTALLED'}:{})});break;
     }
     case 'disclosure_sources':case 'inspect_disclosure':{
      z.null().parse(q.payload);const l=(await c.query('SELECT record,revision FROM genesis_life_state')).rows[0];const archive=await readMemoryArchive(c,q.organismId,Number(l.revision));
      const set=await loadDisclosure(c,b.state,l.record,archive);result=q.operation==='disclosure_sources'?set.sources.map(({projection:_,...x})=>{void _;return x;}):{version:set.version,revision:set.revision,reviews:set.reviews};break;
     }
     case 'review_disclosure':{
      const v=reviewSchema.parse(q.payload),l=(await c.query('SELECT record,revision FROM genesis_life_state')).rows[0];const a=await readMemoryArchive(c,q.organismId,Number(l.revision));
      const s=disclosureSources(b.state,l.record,a).find(s=>s.type===v.sourceType&&s.id===v.sourceId);if(!s||s.hash!==v.sourceHash||s.internalOnly&&v.audience!=='INTERNAL_USE'&&v.decision==='APPROVED')throw Error('SOURCE_DISCLOSURE_REFUSED');
      const prior=(await c.query("SELECT * FROM genesis_disclosure_reviews WHERE organism_id='genesis' AND source_type=$1 AND source_id=$2 AND audience=$3 ORDER BY version DESC LIMIT 1",[v.sourceType,v.sourceId,v.audience])).rows[0];previousHash=prior?rowHash(prior):null;
      if((prior?.version??0)!==v.expectedVersion||q.expectedHash!==previousHash||q.targetId!==v.sourceId||v.expiresAt&&Date.parse(v.expiresAt)<=Date.now()||v.decision==='REVOKED'&&!prior)throw Error('STALE_DISCLOSURE_REVIEW');
      await c.query("INSERT INTO genesis_disclosure_reviews(id,organism_id,source_type,source_id,source_hash,audience,version,schema_version,decision,reviewer_id,reason_reference,expires_at,audit_id) VALUES($1,'genesis',$2,$3,$4,$5,$6,1,$7,$8,$9,$10,$11)",[q.id+':review',v.sourceType,v.sourceId,v.sourceHash,v.audience,v.expectedVersion+1,v.decision,principal.actorId,q.reasonReference,v.expiresAt,q.id]);
      result={reviewId:q.id+':review',version:v.expectedVersion+1,decision:v.decision,audience:v.audience};break;
     }
     case 'recovery_disposition':{
      const v=recoverySchema.parse(q.payload);const r=await target(v.targetType==='one_shot'?'genesis_execution_grants':'genesis_runtime_events');
      if(!['AMBIGUOUS','CONSUMED','FAILED','CANCELLED','REVOKED'].includes(r.status))throw Error('UNSETTLED_RECOVERY_TARGET');
      const cycle=r.cycle_id,decision=(await c.query('SELECT record FROM genesis_decisions WHERE id=$1',[cycle])).rows[0]?.record;
      const episode=(await c.query('SELECT record FROM genesis_life_events WHERE id=$1',[cycle+':episode'])).rows[0]?.record;
      const committed=decision?.schemaVersion===2&&decision.organismId===q.organismId&&episode?.organismId===q.organismId&&episode?.source===cycle&&decision.memory?.episode?.id===episode?.id;
      if((decision||episode)&&!committed)throw Error('INCONSISTENT_COMMIT_EVIDENCE');
      const providers=(await c.query('SELECT id,record FROM genesis_provider_attempts WHERE cycle_id=$1',[cycle])).rows;
      const facts=(await c.query("SELECT target_id,disposition FROM genesis_recovery_dispositions WHERE target_type='provider' AND target_id=ANY($1::text[])",[providers.map(p=>p.id)])).rows;
      if(v.disposition==='CONFIRMED_LOCAL_COMMIT'&&!decision||v.disposition!=='CONFIRMED_LOCAL_COMMIT'&&v.disposition!=='UNRESOLVED_REMAIN_STOPPED'&&decision)throw Error('RECOVERY_COMMIT_CONTRADICTION');
      if(v.disposition==='CONFIRMED_NO_EXTERNAL_EFFECT'&&providers.some(x=>x.record.costMicros!==0||!(x.record.status==='not_sent'||x.record.status==='reconciled'&&facts.some(f=>f.target_id===x.id&&f.disposition==='PROVIDER_NOT_EXECUTED'))))throw Error('UNRESOLVED_EXTERNAL_LIABILITY');
      if(v.disposition==='CONFIRMED_EXTERNAL_EFFECT_WITHOUT_LOCAL_COMMIT'&&!providers.some(x=>Number.isSafeInteger(x.record.costMicros)&&(x.record.status==='received'&&x.record.response||x.record.status==='reconciled'&&facts.some(f=>f.target_id===x.id&&f.disposition==='PROVIDER_BILLED'))))throw Error('EXTERNAL_FACT_NOT_ESTABLISHED');
      await c.query("INSERT INTO genesis_recovery_dispositions(id,organism_id,actor_id,target_type,target_id,previous_hash,disposition,reference,facts,audit_id) VALUES($1,'genesis',$2,$3,$4,$5,$6,$7,$8,$9)",[q.id+':recovery',principal.actorId,v.targetType,q.targetId,previousHash,v.disposition,q.reasonReference,{evidenceHash:v.evidenceHash,localCommitObserved:!!decision,automaticRetry:false,authorityStatusUnchanged:r.status},q.id]);
      result={disposition:v.disposition,remainsStopped:true,automaticRetry:false,authorityReopened:false};break;
     }
     case 'provider_reconcile':{
      const v=reconciliationSchema.parse(q.payload),r=await target('genesis_provider_attempts');
      if(r.record.status!=='unknown')throw Error('PROVIDER_NOT_UNRESOLVED');
      const owner=(await c.query("SELECT EXISTS(SELECT 1 FROM genesis_execution_grants WHERE cycle_id=$1 AND payload->>'organismId'=$2) OR EXISTS(SELECT 1 FROM genesis_continuous_attempts a JOIN genesis_continuous_scopes s ON s.id=a.scope_id WHERE a.cycle_id=$1 AND s.payload->>'organismId'=$2) AS owned",[r.cycle_id,q.organismId])).rows[0].owned;if(!owner)throw Error('PROVIDER_OWNER_UNRESOLVED');
      if(v.fact==='PROVIDER_UNKNOWN'&&(v.costMicros!==null||v.usage!==null)||v.fact==='PROVIDER_NOT_EXECUTED'&&(v.costMicros!==0||v.usage!==null||v.responseId!==null)||v.fact==='PROVIDER_BILLED'&&v.costMicros===null)throw Error('PROVIDER_FACT_INCONSISTENT');
      if(v.fact!=='PROVIDER_UNKNOWN'){const pc=new ProviderControl(p,async()=>{throw Error('NO_DISPATCH');});await pc.reconcile(r.id,{operator:principal.actorId,reference:q.reasonReference,costMicros:v.costMicros!});}
      await c.query("INSERT INTO genesis_recovery_dispositions(id,organism_id,actor_id,target_type,target_id,previous_hash,disposition,reference,facts,audit_id) VALUES($1,'genesis',$2,'provider',$3,$4,$5,$6,$7,$8)",[q.id+':recovery',principal.actorId,r.id,previousHash,v.fact,q.reasonReference,{...v,automaticRetry:false},q.id]);result={fact:v.fact,costMicros:v.costMicros,automaticRetry:false,authorityReopened:false};break;
     }
     case 'propose_provider':{const a=compatibleAdmission(q.payload);if(q.targetId!==a.id||q.expectedHash!==null||a.reviewReference!==q.reasonReference||credentialLike(JSON.stringify(Object.values(a).filter(v=>v!==a.secretReference))))throw Error('PROVIDER_ADMISSION_REFUSED');
      if(a.provider==='fixture'){const t=(await c.query('SELECT current_database() db,current_schema() schema')).rows[0];if(t.db!=='genesis_runtime_v1_test'||!t.schema.startsWith('awakening_test_'))throw Error('FIXTURE_ADMISSION_REFUSED');}
      await c.query("INSERT INTO genesis_provider_admissions(id,organism_id,payload,payload_hash,status,audit_id) VALUES($1,'genesis',$2,$3,'PROPOSED',$4)",[a.id,a,digest(a),q.id]);result={id:a.id,status:'PROPOSED',hash:digest(a),executionAuthorized:false};break;}
     case 'admit_provider':case 'revoke_provider':{z.null().parse(q.payload);const r=await target('genesis_provider_admissions');if(r.organism_id!=='genesis'||r.payload_hash!==digest(r.payload))throw Error('PROVIDER_IDENTITY_MISMATCH');const a=compatibleAdmission(r.payload);if(q.operation==='admit_provider'&&(r.status!=='PROPOSED'||Date.parse(a.effectiveAt)>Date.now()||Date.parse(a.expiresAt)<=Date.now()))throw Error('PROVIDER_ADMISSION_REFUSED');const status=q.operation==='admit_provider'?'ADMITTED':'REVOKED';await c.query('UPDATE genesis_provider_admissions SET status=$2,audit_id=$3 WHERE id=$1',[r.id,status,q.id]);result={id:r.id,status,executionAuthorized:false};break;}
     case 'inspect_provider':{z.null().parse(q.payload);const r=(await c.query("SELECT * FROM genesis_provider_admissions WHERE id=$1 AND organism_id='genesis'",[q.targetId])).rows[0];result=r?{record:r,hash:rowHash(r),secretValueIncluded:false}:null;break;}
     case 'inspect_provider_attempt':{z.null().parse(q.payload);const r=(await c.query('SELECT * FROM genesis_provider_attempts WHERE id=$1',[q.targetId])).rows[0];const receipt=(await c.query('SELECT record FROM genesis_provider_receipts WHERE attempt_id=$1',[q.targetId])).rows[0]?.record;
      result=r?{id:r.id,cycleId:r.cycle_id,hash:rowHash(r),status:r.record.status,owner:r.record.owner??null,leaseUntil:r.record.leaseUntil??null,requestHash:r.record.request?.hash??null,admissionHash:r.record.admissionHash??null,reservedMicros:r.record.reservedMicros,costMicros:r.record.costMicros,errorCode:r.record.errorCode??null,cancellation:r.record.cancellation??null,receipt:receipt?{responseId:receipt.responseId,providerRequestId:receipt.providerRequestId,validation:receipt.validation,proposalHash:receipt.proposalHash,usage:receipt.usage,receivedAt:receipt.receivedAt}:null,automaticRetry:false,proposalBodyIncluded:false,contextIncluded:false}:null;break;}
     case 'provider_readiness':z.null().parse(q.payload);result={admission:'PENDING',productionAdmissionAvailable:false,providerCalls:0};break;
    }
    if(Buffer.byteLength(JSON.stringify(result))>131072)throw Error('PRIVATE_INSPECTION_BOUND_EXCEEDED');
   }catch{await c.query('ROLLBACK TO SAVEPOINT control_operation');refused=true;result={code:'OPERATOR_OPERATION_REFUSED'};}
   await c.query("INSERT INTO genesis_operator_audit(id,actor_id,capability,operation,organism_id,target_id,previous_hash,requested_hash,reason_reference,result,result_hash,runtime_hash) VALUES($1,$2,$3,$4,'genesis',$5,$6,$7,$8,$9,$10,$11)",[q.id,principal.actorId,cap,q.operation,q.targetId,previousHash,digest(q),q.reasonReference,refused?'REFUSED':'SUCCEEDED',digest(result),runtimeIdentity().sha256]);
   await c.query('COMMIT');if(refused)throw Error('OPERATOR_OPERATION_REFUSED');return result;
  }catch(e){await c.query('ROLLBACK');throw e;}finally{c.release();}
 }
}

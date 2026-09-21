import {loadAdmission,fixtureTarget} from './reasoning/store.ts';
import {ReasoningControl,type ReasoningOptions} from './reasoning/control.ts';
import type {WorkingContext} from '../core/v2/contracts.ts';
import {readMemoryArchive} from './memory-store.ts';
import {loadDisclosure} from './disclosure-store.ts';
/** Explicit single-cycle controller. No boot/API/CLI entry point and no automatic authorization. */
import type pg from 'pg';
import {randomUUID} from 'node:crypto';
import {readFileSync} from 'node:fs';
import {digest} from '../core/v2/identity.ts';
import {journalIntent,closeUncommittedIntent} from './intent-journal.ts';
import {savedSnapshotReference} from './saved-provenance.ts';
import {prepareCycle,InterruptedCycle} from '../core/v2/cycle.ts';
import {SavedObservationAdapter} from '../core/v2/biology.ts';
import type {PlannerV2,DecisionV2,LifeStateV1} from '../core/v2/contracts.ts';
import {commitV2,type CycleFence} from './commit-v2.ts';
import {assertGrantState,assertOneShotClaim,type GrantRow} from './one-shot-authority.ts';
import {awakeningMode,validateGrant,type OneShotGrant} from './one-shot-spec.ts';
import {awakeningEventSchema} from './awakening-event.ts';
import {ProviderControl,type ProviderTransport,type TokenCounter} from './provider-control.ts';
import {validateProviderAdmission,type ProviderAdmission} from './provider-admission.ts';
export class OneShotController{
 private admittedPlanners=new WeakSet<PlannerV2>();
 private governedPlanners=new WeakSet<PlannerV2>();
 readonly pool:pg.Pool;
 constructor(pool:pg.Pool){this.pool=pool;}
 async tx<T>(fn:(c:pg.PoolClient)=>Promise<T>){const c=await this.pool.connect();try{await c.query('BEGIN');await c.query("SELECT set_config('genesis.writer_version','runtime-v1',true)");const result=await fn(c);await c.query('COMMIT');return result;}catch(e){await c.query('ROLLBACK');throw e;}finally{c.release();}}
 /** Explicit structural install, only for the dedicated fixture database in this release. */
 async installFixtureSchema(){const r=(await this.pool.query('SELECT current_database() AS db,current_schema() AS schema')).rows[0];if(r.db!=='genesis_runtime_v1_test'||!r.schema.startsWith('awakening_test_'))throw Error('Fixture schema only');await this.pool.query(readFileSync(new URL('../runtime/one-shot-schema.sql',import.meta.url),'utf8'));}
 async propose(payload:OneShotGrant){const g=validateGrant(payload);await this.pool.query("INSERT INTO genesis_execution_grants(id,payload,payload_hash,status) VALUES($1,$2,$3,'PROPOSED')",[g.id,g,digest(g)]);}
 /** Privileged internal operation. The future operator entry point must authenticate its caller. */
 async authorize(id:string,evidence:{payloadHash:string;issuer:string;reference:string}){return this.tx(async c=>{const r=(await c.query('SELECT * FROM genesis_execution_grants WHERE id=$1 FOR UPDATE',[id])).rows[0] as GrantRow;const g=r&&validateGrant(r.payload);if(!g||r.status!=='PROPOSED'||digest(g)!==evidence.payloadHash||evidence.issuer!==g.issuer||evidence.reference!==g.authorizationReference||Date.parse(g.expiresAt)<=Date.now())throw Error('Explicit matching authorization required');await c.query("UPDATE genesis_execution_grants SET status='AUTHORIZED',authorization_record=$2,updated_at=now() WHERE id=$1",[id,evidence]);});}
 private async mark(c:pg.PoolClient,f:CycleFence){await c.query("SELECT set_config('genesis.oneshot_grant',$1,true),set_config('genesis.oneshot_lease',$2,true)",[f.oneShotGrantId!,f.lease]);}
 private async base(c:pg.PoolClient){const base=(await c.query("SELECT state,revision,lease,lease_until>now() AS valid FROM genesis_organisms WHERE id='genesis' FOR UPDATE")).rows[0];const ext=(await c.query("SELECT record,revision FROM genesis_life_state WHERE organism_id='genesis' FOR UPDATE")).rows[0];if(!base||!ext)throw Error('Existing Genesis required');return {base,ext};}
 async claim(id:string):Promise<CycleFence>{const result=await this.tx(async c=>{
  const {base,ext}=await this.base(c);const row=(await c.query('SELECT * FROM genesis_execution_grants WHERE id=$1 FOR UPDATE',[id])).rows[0] as GrantRow;
  if(!row||row.status!=='AUTHORIZED')throw Error('Grant is not available');
  if(Date.parse(row.payload.expiresAt)<=Date.now()){await c.query("UPDATE genesis_execution_grants SET status='EXPIRED',updated_at=now() WHERE id=$1",[id]);return null;}
  const g=await assertGrantState(c,row,base,ext);
  if(base.valid||(await c.query("SELECT id FROM genesis_execution_grants WHERE status IN ('CLAIMED','AMBIGUOUS') AND payload->>'organismId'=$1",[g.organismId])).rowCount)throw Error('Outstanding claim/reconciliation');
  const f:CycleFence={cycleId:'oneshot:'+id,lease:randomUUID(),baseRevision:Number(base.revision),lifeRevision:Number(ext.revision),oneShotGrantId:id};
  await c.query("INSERT INTO genesis_cycle_attempts(id,lease,revision,status) VALUES($1,$2,$3,'preparing')",[f.cycleId,f.lease,f.baseRevision]);
  await c.query("UPDATE genesis_execution_grants SET status='CLAIMED',cycle_id=$2,lease=$3,updated_at=now() WHERE id=$1",[id,f.cycleId,f.lease]);
  await this.mark(c,f);
  await c.query("UPDATE genesis_organisms SET lease=$1,lease_until=now()+($2 * interval '1 millisecond'),phase='planning' WHERE id='genesis'",[f.lease,awakeningMode().leaseMs]);
return f;
 });if(!result)throw Error('Grant expired');return result;}
 async check(f:CycleFence){return this.tx(async c=>{const {base,ext}=await this.base(c);const a=(await c.query('SELECT * FROM genesis_cycle_attempts WHERE id=$1 FOR UPDATE',[f.cycleId])).rows[0];if(!base.valid||base.lease!==f.lease||!a||a.cancelled||a.status!=='preparing'||a.lease!==f.lease||Number(base.revision)!==f.baseRevision||Number(ext.revision)!==f.lifeRevision)throw Error('Stale or cancelled one-shot');return assertOneShotClaim(c,f,base,ext);});}
 async prepare(f:CycleFence,selected:{identity:string;planner:PlannerV2}){
  const g=await this.check(f);if(selected.identity!==g.planner.identity||(g.permission.llm&&!this.admittedPlanners.has(selected.planner)))throw Error('Unadmitted planner identity');
  const {o,life,archive,snapshot,disclosure,last}=await this.tx(async c=>{const {base,ext}=await this.base(c);await assertOneShotClaim(c,f,base,ext);const archive=await readMemoryArchive(c,base.state.id,Number(ext.revision));return {o:base.state,life:ext.record as LifeStateV1,archive,snapshot:await savedSnapshotReference(c,base.state.brain),disclosure:await loadDisclosure(c,base.state,ext.record,archive),last:(await c.query('SELECT at FROM genesis_decisions ORDER BY cycle DESC LIMIT 1')).rows[0].at};});
  const lastAt=new Date(last).toISOString(),at=new Date().toISOString();
  const event=awakeningEventSchema.parse({schemaVersion:1,id:f.cycleId+':event',kind:'operator_authorized_runtime_activation',activationAuthorizationRef:g.authorizationReference,observedAt:at,organismId:o.id,bornAt:o.bornAt,lastLifeEventAt:lastAt,elapsedSinceLastLifeEventMs:Math.max(0,Date.parse(at)-Date.parse(lastAt)),constitutionHash:g.constitution.hash,canonicalCyclesBefore:7,biologicalStatus:'not_applied',walletIdentityStatus:life.walletIdentity.status==='unresolved'?'UNRESOLVED':'OPERATOR_VERIFIED_BINDING',contextRefs:['identity','constitution','life','permissions','biology'],permissionManifestHash:g.permissionHash});
  const brain=new SavedObservationAdapter(o.id);if(snapshot)brain.restore(snapshot);
  let called=false;const planner:PlannerV2={propose:async ctx=>{if(called)throw Error('Second planner invocation forbidden');called=true;await this.check(f);if(this.governedPlanners.has(selected.planner)){try{const p=await selected.planner.propose(ctx);await this.check(f);return p;}catch{throw new InterruptedCycle('PROVIDER_REASONING_STOPPED_REVIEW_REQUIRED');}}let timer:ReturnType<typeof setTimeout>|undefined;let poll:ReturnType<typeof setInterval>|undefined;
   try{const stopped=new Promise<never>((_,reject)=>{timer=setTimeout(()=>reject(Error('Planner deadline exceeded')),awakeningMode().timeoutMs);poll=setInterval(()=>{void this.check(f).catch(()=>reject(Error('One-shot authority revoked')));},20);});
    const p=await Promise.race([selected.planner.propose(ctx),stopped]);await this.check(f);return {...p,planner:selected.identity};
   }finally{if(timer)clearTimeout(timer);if(poll)clearInterval(poll);}}};
  const prepared=await prepareCycle(o,life,brain,planner,{id:event.id,kind:'digital-event',source:'one-shot-authorized-factual-event',observedAt:at},g.permission,at,f.cycleId,{grantId:g.id,grantHash:digest(g),permissionHash:g.permissionHash,event},archive,undefined,disclosure);
  // Persist factual envelope privately; public projection never exports raw event/context.
  Object.assign(prepared.decision.memory.episode.record as object,{awakeningEvent:event,executionGrantHash:digest(g)});
  await this.check(f);return prepared;
 }
 async journal(f:CycleFence,d:DecisionV2){await this.tx(async c=>{const {base,ext}=await this.base(c);await assertOneShotClaim(c,f,base,ext);if(!base.valid||base.lease!==f.lease||d.id!==f.cycleId||d.organismId!==base.state.id)throw Error('Stale or mismatched intent');await journalIntent(c,d);});}
 async commit(f:CycleFence,p:{life:LifeStateV1;decision:DecisionV2}){return this.tx(c=>commitV2(c,f,p.life,p.decision));}
 async revoke(id:string,reference:string){if(!reference.trim())throw Error('Revocation reference required');return this.tx(async c=>{const {base}=await this.base(c);const r=(await c.query('SELECT * FROM genesis_execution_grants WHERE id=$1 FOR UPDATE',[id])).rows[0];if(!r||!['PROPOSED','AUTHORIZED','CLAIMED'].includes(r.status))throw Error('Terminal grant');const unknown=r.cycle_id&&Number((await c.query("SELECT count(*) n FROM genesis_provider_attempts WHERE cycle_id=$1 AND record->>'status' IN ('reserved','dispatching','unknown')",[r.cycle_id])).rows[0].n)>0;if(r.cycle_id){await closeUncommittedIntent(c,r.cycle_id,base.state.id,unknown?'unknown':'cancelled',new Date().toISOString());await c.query('UPDATE genesis_cycle_attempts SET cancelled=true WHERE id=$1',[r.cycle_id]);if(base.lease===r.lease&&Number(base.revision)===r.payload.stateRevision&&Date.parse(r.payload.expiresAt)>Date.now()){await this.mark(c,{oneShotGrantId:id,lease:r.lease,cycleId:r.cycle_id,baseRevision:0,lifeRevision:0});await c.query("UPDATE genesis_organisms SET lease=NULL,lease_until='-infinity',phase='idle' WHERE id='genesis'");}}await c.query("UPDATE genesis_execution_grants SET status=$3,result=$2,updated_at=now() WHERE id=$1",[id,reference,unknown?'AMBIGUOUS':'REVOKED']);});}
 async cancel(f:CycleFence){await this.revoke(f.oneShotGrantId!,'CANCELLED');}
 async recoverExpired(id:string){return this.tx(async c=>{const {base}=await this.base(c);const r=(await c.query('SELECT * FROM genesis_execution_grants WHERE id=$1 FOR UPDATE',[id])).rows[0];if(r?.status!=='CLAIMED'||base.valid)throw Error('Recovery requires an expired unresolved claim');await closeUncommittedIntent(c,r.cycle_id,base.state.id,'unknown',new Date().toISOString());await c.query("UPDATE genesis_execution_grants SET status='AMBIGUOUS',result='RECONCILIATION_REQUIRED',updated_at=now() WHERE id=$1",[id]);await c.query('UPDATE genesis_cycle_attempts SET cancelled=true WHERE id=$1',[r.cycle_id]);});}
 async fail(f:CycleFence){return this.tx(async c=>{const {base}=await this.base(c);const r=(await c.query('SELECT * FROM genesis_execution_grants WHERE id=$1 FOR UPDATE',[f.oneShotGrantId])).rows[0];if(r?.status!=='CLAIMED'||r.lease!==f.lease)return;
  const unknown=(await c.query("SELECT id FROM genesis_provider_attempts WHERE cycle_id=$1 AND record->>'status' IN ('unknown','reserved','dispatching')",[f.cycleId])).rowCount;
  await closeUncommittedIntent(c,f.cycleId,base.state.id,unknown?'unknown':'failed',new Date().toISOString());
  await c.query('UPDATE genesis_cycle_attempts SET cancelled=true WHERE id=$1',[f.cycleId]);if(base.lease===f.lease&&Number(base.revision)===r.payload.stateRevision&&Date.parse(r.payload.expiresAt)>Date.now()){await this.mark(c,f);await c.query("UPDATE genesis_organisms SET lease=NULL,lease_until='-infinity',phase='idle' WHERE id='genesis'");}await c.query("UPDATE genesis_execution_grants SET status=$2,result=$3,updated_at=now() WHERE id=$1",[r.id,unknown?'AMBIGUOUS':'FAILED',unknown?'RECONCILIATION_REQUIRED':'FAILED']);
 });}
 async run(id:string,select:(f:CycleFence)=>Promise<{identity:string;planner:PlannerV2}>){const f=await this.claim(id);try{const selected=await select(f);const prepared=await this.prepare(f,selected);await this.journal(f,prepared.decision);return await this.commit(f,prepared);}catch(e){await this.fail(f);throw e;}}
 async admittedReasoningPlanner(f:CycleFence,options:ReasoningOptions){
  const g=await this.check(f),a=await loadAdmission(this.pool,options.admissionId,g.organismId);
  if(!g.permission.llm||g.planner.admissionHash!==digest(a)||g.planner.provider!==a.provider||g.planner.model!==a.model||g.planner.identity!==`provider:${a.provider}:${a.model}`||a.maximumInputTokens>g.maximumInputTokens||a.maximumOutputTokens>g.maximumOutputTokens||a.perCycleMicros>g.maximumCostMicros||a.timeoutMs>awakeningMode().timeoutMs)throw Error('ADMISSION_GRANT_MISMATCH');
  const pc=new ProviderControl(this.pool,async fence=>{await this.check(fence);});const planner=pc.reasoningPlanner(f,options);this.admittedPlanners.add(planner);this.governedPlanners.add(planner);return {identity:g.planner.identity,planner};
 }
 /** Explicit recovery of an already received proposal under the SAME still-valid fence.
  * No claim, retry, dispatch, new authority, or automatic commit occurs here. */
 async resumeReceived(f:CycleFence){
  const g=await this.check(f),r=(await this.pool.query('SELECT record FROM genesis_provider_attempts WHERE id=$1',[f.cycleId+':reasoning'])).rows[0]?.record;
  if(r?.protocolVersion!==2||r.status!=='received'||digest(r.fence)!==digest(f))throw Error('DURABLE_RECEIPT_REQUIRED');
  const context=r.context as WorkingContext,parsed=JSON.parse(context.text),authority=parsed.critical.oneShotAuthority;
  if(context.hash!==digest(context.text)||authority?.grantHash!==digest(g))throw Error('RECOVERY_CONTEXT_MISMATCH');
  const a=await loadAdmission(this.pool,r.request.admissionId,g.organismId);if(g.planner.admissionHash!==digest(a))throw Error('RECOVERY_ADMISSION_MISMATCH');
  const control=new ReasoningControl(this.pool,async fence=>{await this.check(fence);});
  const proposal=await control.replay(f.cycleId+':reasoning',f,context,a);
  const prepared=await this.tx(async c=>{const {base,ext}=await this.base(c);await assertOneShotClaim(c,f,base,ext);const archive=await readMemoryArchive(c,base.state.id,Number(ext.revision)),disclosure=await loadDisclosure(c,base.state,ext.record,archive);
   const brain=new SavedObservationAdapter(base.state.id,()=>parsed.critical.biology.observedAt),snapshot=await savedSnapshotReference(c,base.state.brain);if(snapshot)brain.restore(snapshot);
   const p=await prepareCycle(base.state,ext.record,brain,{propose:async fresh=>{if(fresh.hash!==context.hash||digest(fresh.manifest)!==digest(context.manifest))throw Error('RECOVERY_CONTEXT_CHANGED');return proposal;}},parsed.currentEvent,g.permission,authority.event.observedAt,f.cycleId,authority,archive,undefined,disclosure);
   if(p.decision.lifeContext.contextHash!==context.hash||!p.decision.proposal)throw Error('RECOVERY_CONTEXT_CHANGED');Object.assign(p.decision.memory.episode.record as object,{awakeningEvent:authority.event,executionGrantHash:digest(g)});return p;
  });await this.check(f);return prepared;
 }
 /** Deprecated compatibility path: injected transport identities are accepted ONLY on disposable fixtures. */
 async providerPlanner(f:CycleFence,input:{admission:ProviderAdmission;counter:TokenCounter & {id:string};transport:{id:string;codeHash:string;send:ProviderTransport}}){
  if(!await fixtureTarget(this.pool))throw Error('LEGACY_PROVIDER_FIXTURE_ONLY');
  const g=await this.check(f),a=validateProviderAdmission(input.admission,g);
  if(input.counter.id!==a.tokenCounter.id||input.transport.id!==a.transport.id||input.transport.codeHash!==a.transport.codeHash||input.counter.provenance!==a.tokenCounter.evidence||input.counter.model!==a.model)throw Error('Provider implementation admission mismatch');
  const pc=new ProviderControl(this.pool,async fence=>{await this.check(fence);});const id=f.cycleId+':provider-grant';
  const record={id,enabled:true,model:a.model,pricingEvidence:a.rateCard.reference,inputMicrosPerToken:a.rateCard.inputMicrosPerToken,outputMicrosPerToken:a.rateCard.outputMicrosPerToken,maxInputTokens:a.maximumInputTokens,maxOutputTokens:a.maximumOutputTokens,perCallMicros:a.perAttemptMicros,perCycleMicros:a.perCycleMicros,dailyMicros:a.dailyMicros,maxAttempts:1,timeoutMs:a.timeoutMs,expiresAt:g.expiresAt,executionGrantHash:digest(g),admissionHash:digest(a),secretReference:a.secretReference};
  await this.pool.query('INSERT INTO genesis_provider_grants(id,record) VALUES($1,$2)',[id,record]);const planner=pc.planner(id,f,f.cycleId+':provider-attempt',input.counter,input.transport.send);this.admittedPlanners.add(planner);return {identity:g.planner.identity,planner};
 }
}

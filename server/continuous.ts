import {loadDisclosure} from './disclosure-store.ts';
/** Explicit local controller. No boot hook, environment unlock, endpoint, scheduler or live provider factory. */
import type pg from 'pg';
import {readFileSync} from 'node:fs';
import {randomUUID} from 'node:crypto';
import {digest} from '../core/v2/identity.ts';
import {eventSchema,LOCAL_PERMISSION,obsolete,followups} from '../core/v2/continuous.ts';
import {validateScope,type ContinuousScope} from './continuous-spec.ts';
import {continuousState,assertContinuousClaim,continuousInput,ContinuousFenceError} from './continuous-authority.ts';
import {prepareCycle,InterruptedCycle} from '../core/v2/cycle.ts';
import {SavedObservationAdapter} from '../core/v2/biology.ts';
import {savedSnapshotReference} from './saved-provenance.ts';
import {readMemoryArchive} from './memory-store.ts';
import {commitV2,type CycleFence} from './commit-v2.ts';
import type {PlannerV2,DecisionV2,LifeStateV1} from '../core/v2/contracts.ts';
export class SimulatedCrash extends InterruptedCycle {}
export type Prepared={life:LifeStateV1;decision:DecisionV2};
export type PhaseHook=(stage:string)=>Promise<void>;
export async function enqueueInTransaction(c:pg.PoolClient,raw:unknown){
 const e=eventSchema.parse(raw);if(Date.parse(e.availableAt)<Date.parse(e.createdAt)||e.expiresAt&&Date.parse(e.expiresAt)<=Date.parse(e.createdAt))throw Error('Invalid event times');
 const owner=(await c.query("SELECT state->>'id' id FROM genesis_organisms WHERE id='genesis'")).rows[0];if(owner?.id!==e.organismId)throw Error('Wrong event organism');
 const existing=(await c.query('SELECT * FROM genesis_runtime_events WHERE id=$1 OR dedup_key=$2 FOR UPDATE',[e.id,e.dedupKey])).rows;
 if(existing.length){if(existing.length!==1||existing[0].payload_hash!==digest(e)||existing[0].id!==e.id)throw Error('Dedup payload conflict');return false;}
 await c.query("INSERT INTO genesis_runtime_events(id,organism_id,payload,payload_hash,dedup_key,available_at,status) VALUES($1,'genesis',$2,$3,$4,$5,'PENDING')",[e.id,e,digest(e),e.dedupKey,e.availableAt]);
 await c.query("INSERT INTO genesis_continuous_journal(event_id,transition,reason) VALUES($1,'ENQUEUED',$2)",[e.id,e.source]);return true;
}

/** Pre-admission work. Organism lock excludes competing event intake. */
async function validateFollowup(c:pg.PoolClient,e:ReturnType<typeof eventSchema.parse>){
 eventSchema.parse(e);
 if(Date.parse(e.availableAt)<Date.parse(e.createdAt)||e.expiresAt&&Date.parse(e.expiresAt)<=Date.parse(e.createdAt))throw Error('Invalid event times');
 if((await c.query('SELECT id FROM genesis_runtime_events WHERE id=$1 OR dedup_key=$2',[e.id,e.dedupKey])).rowCount)throw Error('Duplicate followup');
}
/** Bounded, prevalidated local writes only; caller owns organism/authority locks. */
async function persistFollowup(c:pg.PoolClient,e:ReturnType<typeof eventSchema.parse>){
 await c.query("INSERT INTO genesis_runtime_events(id,organism_id,payload,payload_hash,dedup_key,available_at,status) VALUES($1,'genesis',$2,$3,$4,$5,'PENDING')",[e.id,e,digest(e),e.dedupKey,e.availableAt]);
 await c.query("INSERT INTO genesis_continuous_journal(event_id,transition,reason) VALUES($1,'ENQUEUED',$2)",[e.id,e.source]);
}

export class ContinuousController{
 readonly pool:pg.Pool;
 constructor(pool:pg.Pool){this.pool=pool;}
 async tx<T>(fn:(c:pg.PoolClient)=>Promise<T>){const c=await this.pool.connect();try{await c.query('BEGIN');await c.query("SELECT set_config('genesis.writer_version','runtime-v1',true)");const r=await fn(c);await c.query('COMMIT');return r;}catch(e){await c.query('ROLLBACK');throw e;}finally{c.release();}}
 private async base(c:pg.PoolClient){const base=(await c.query("SELECT state,revision,lease,lease_until>clock_timestamp() valid FROM genesis_organisms WHERE id='genesis' FOR UPDATE")).rows[0];const ext=(await c.query("SELECT record,revision FROM genesis_life_state WHERE organism_id='genesis' FOR UPDATE")).rows[0];if(!base||!ext)throw Error('Existing organism required');return {base,ext};}
 private async mark(c:pg.PoolClient,f:CycleFence){await c.query("SELECT set_config('genesis.continuous_cycle',$1,true),set_config('genesis.continuous_lease',$2,true)",[f.cycleId,f.lease]);}
 /** Structural preparation only on dedicated test DB. Production installation remains separately reviewed. */
 async installFixtureSchema(){const r=(await this.pool.query('SELECT current_database() db,current_schema() schema')).rows[0];if(r.db!=='genesis_runtime_v1_test'||!r.schema.startsWith('awakening_test_'))throw Error('Disposable schema required');await this.pool.query(readFileSync(new URL('../runtime/continuous-schema.sql',import.meta.url),'utf8'));}
 async proposeScope(raw:unknown){const s=validateScope(raw);await this.tx(async c=>{const {base}=await this.base(c);if(base.state.id!==s.organismId)throw Error('Scope owner');await c.query("INSERT INTO genesis_continuous_scopes(id,organism_id,payload,payload_hash,status) VALUES($1,'genesis',$2,$3,'PROPOSED')",[s.id,s,digest(s)]);});}
 /** Trusted operator library only; no public endpoint. Requires separately authenticated operator caller. */
 async authorizeScope(id:string,evidence:{payloadHash:string;issuer:string;reference:string}){await this.tx(async c=>{const {base}=await this.base(c);const r=(await c.query('SELECT * FROM genesis_continuous_scopes WHERE id=$1 FOR UPDATE',[id])).rows[0];const s=r&&validateScope(r.payload);if(!s||s.organismId!==base.state.id||r.status!=='PROPOSED'||evidence.payloadHash!==digest(s)||evidence.issuer!==s.issuer||evidence.reference!==s.authorizationReference||Date.parse(s.expiresAt)<=Date.now())throw Error('Explicit scope authorization_record required');await c.query("UPDATE genesis_continuous_scopes SET status='AUTHORIZED',authorization_record=$2 WHERE id=$1",[id,evidence]);await c.query("INSERT INTO genesis_continuous_journal(scope_id,transition) VALUES($1,'AUTHORIZED')",[id]);});}
 async enqueue(raw:unknown,operatorReference:string){if(!operatorReference.trim())throw Error('Operator evidence required');const e=eventSchema.parse(raw);if(e.source!=='operator'||e.sourceRef!==operatorReference||!['MANUAL_EVENT','TIME_WAKE','TASK_REVIEW_DUE','COMMITMENT_REVIEW_DUE','PROJECT_REVIEW','ASSISTANCE_REVIEW','QUESTION_REVIEW'].includes(e.payload.kind)||e.depth!==0||e.rootId!==e.id||e.parentCycleId||e.parentEventId)throw Error('Operator event provenance');return this.tx(async c=>{await this.base(c);return enqueueInTransaction(c,e);});}
 async resources(c:pg.PoolClient,s:ContinuousScope){
 const r=(await c.query("SELECT count(*) n,count(*) FILTER(WHERE at>now()-($2 * interval '1 millisecond')) w,count(*) FILTER(WHERE status='CLAIMED') active,count(*) FILTER(WHERE status='FAILED' OR status='COMMITTED' AND failure IS NOT NULL) failures,count(*) FILTER(WHERE status='AMBIGUOUS') ambiguous,coalesce(sum(reserved_micros) FILTER(WHERE status IN ('CLAIMED','AMBIGUOUS')),0) reserved,coalesce(sum(cost_micros) FILTER(WHERE at>now()-($2 * interval '1 millisecond')),0) cost FROM genesis_continuous_attempts WHERE scope_id=$1",[s.id,s.windowMs])).rows[0];
 // Existing provider ledger is authoritative for unresolved liabilities, including older days/scopes.
 const ledger=(await c.query("SELECT record,at FROM genesis_provider_attempts")).rows;let liabilities=0,costs=0,unresolved=0;
 for(const row of ledger){const p=row.record;if(['reserved','dispatching','unknown'].includes(p.status)){if(!Number.isSafeInteger(p.reservedMicros)||p.reservedMicros<0)throw Error('Unidentified provider liability requires review');liabilities+=p.reservedMicros;unresolved++;}else if(new Date(row.at).getTime()>Date.now()-s.windowMs&&p.costMicros!==null&&p.costMicros!==undefined){if(!Number.isSafeInteger(p.costMicros)||p.costMicros<0)throw Error('Invalid provider cost ledger');costs+=p.costMicros;}}
 return {scopeClaims:Number(r.n),windowClaims:Number(r.w),active:Number(r.active),failures:Number(r.failures),ambiguous:Number(r.ambiguous),reservedMicros:Math.max(Number(r.reserved),liabilities),committedMicros:Number(r.cost)+costs,unresolvedProviderAttempts:unresolved};
 }
 async claim(scopeId:string):Promise<CycleFence|null>{return this.tx(async c=>{
  const {base,ext}=await this.base(c),s=await continuousState(c,scopeId,base,ext);
  if(base.valid)return null;
  if((await c.query("SELECT id FROM genesis_execution_grants WHERE status IN ('CLAIMED','AMBIGUOUS')")).rowCount||(await c.query("SELECT cycle_id FROM genesis_continuous_attempts WHERE status IN ('CLAIMED','AMBIGUOUS')")).rowCount)return null;
  const budget=await this.resources(c,s);if(budget.scopeClaims>=s.maxCycles||budget.windowClaims>=s.maxCyclesPerWindow||budget.active>=s.maxConcurrent||budget.reservedMicros+budget.committedMicros>s.maxCostPerWindowMicros||budget.unresolvedProviderAttempts)return null;
  const rows=(await c.query("SELECT * FROM genesis_runtime_events WHERE status='PENDING' AND available_at<=now() AND payload->'payload'->>'kind'=ANY($1::text[]) ORDER BY available_at,id LIMIT 100 FOR UPDATE",[s.allowedEvents])).rows;
  for(const row of rows){const e=eventSchema.parse(row.payload);if(row.payload_hash!==digest(e)||e.organismId!==s.organismId)throw Error('Corrupted event identity');if(!s.allowedEvents.includes(e.payload.kind))continue;
   const reason=e.expiresAt&&Date.parse(e.expiresAt)<=Date.now()?'EXPIRED':obsolete(e,ext.record);
   if(reason){await c.query('UPDATE genesis_runtime_events SET status=$2,reason=$3 WHERE id=$1',[e.id,reason==='EXPIRED'?'EXPIRED':'CANCELLED',reason]);await c.query("INSERT INTO genesis_continuous_journal(event_id,scope_id,transition,reason) VALUES($1,$2,'DISCARDED',$3)",[e.id,s.id,reason]);continue;}
   const root=Number((await c.query("SELECT count(*) n FROM genesis_continuous_attempts a JOIN genesis_runtime_events e ON e.id=a.event_id WHERE e.payload->>'rootId'=$1 AND a.at>now()-($2 * interval '1 millisecond')",[e.rootId,s.backoffMs])).rows[0].n);
   if(root>=s.maxImmediatePerRoot){await c.query("UPDATE genesis_runtime_events SET status='FAILED',reason='ROOT_RATE_LIMIT' WHERE id=$1",[e.id]);await c.query("INSERT INTO genesis_continuous_journal(event_id,scope_id,transition,reason) VALUES($1,$2,'FAILED','ROOT_RATE_LIMIT')",[e.id,s.id]);continue;}
   if(e.depth>s.maxDepth||row.attempts>=s.maxAttemptsPerEvent){await c.query("UPDATE genesis_runtime_events SET status='FAILED',reason='CHAIN_OR_ATTEMPT_LIMIT' WHERE id=$1",[e.id]);await c.query("INSERT INTO genesis_continuous_journal(event_id,scope_id,transition,reason) VALUES($1,$2,'FAILED','CHAIN_OR_ATTEMPT_LIMIT')",[e.id,s.id]);continue;}
   const issued=(await c.query("WITH t AS MATERIALIZED (SELECT clock_timestamp() t) SELECT t::text issued_at,(t+($1 * interval '1 millisecond'))::text deadline,t>=$2::timestamptz AND t<$3::timestamptz AND ($4::timestamptz IS NULL OR t<$4::timestamptz) eligible FROM t",[s.leaseMs,s.issuedAt,s.expiresAt,e.expiresAt])).rows[0];
   if(!issued.eligible)throw Error('SCOPE_INVALID');
   const f:CycleFence={cycleId:e.id+':attempt:'+(row.attempts+1),lease:randomUUID(),baseRevision:Number(base.revision),lifeRevision:Number(ext.revision),continuousScopeId:s.id,eventId:e.id};
   await c.query("INSERT INTO genesis_cycle_attempts(id,lease,revision,status) VALUES($1,$2,$3,'preparing')",[f.cycleId,f.lease,f.baseRevision]);
   await c.query("INSERT INTO genesis_continuous_attempts(cycle_id,event_id,scope_id,lease,base_revision,life_revision,status,phase,resources,claim_issued_at,lease_until) VALUES($1,$2,$3,$4,$5,$6,'CLAIMED','claimed',$7,$8,$9)",[f.cycleId,e.id,s.id,f.lease,f.baseRevision,f.lifeRevision,{scopeClaims:budget.scopeClaims+1,windowClaims:budget.windowClaims+1,reservedMicros:budget.reservedMicros,committedMicros:budget.committedMicros},issued.issued_at,issued.deadline]);
   await c.query("UPDATE genesis_runtime_events SET status='CLAIMED',attempts=attempts+1,cycle_id=$2,lease=$3,lease_until=$4::timestamptz WHERE id=$1",[e.id,f.cycleId,f.lease,issued.deadline]);
   await this.mark(c,f);await c.query("UPDATE genesis_organisms SET lease=$1,lease_until=$2::timestamptz,phase='planning' WHERE id='genesis'",[f.lease,issued.deadline]);
   await c.query("INSERT INTO genesis_continuous_journal(event_id,scope_id,cycle_id,transition) VALUES($1,$2,$3,'CLAIMED')",[e.id,s.id,f.cycleId]);return f;
  }return null;
 });}
 async check(f:CycleFence){return this.tx(async c=>{const {base,ext}=await this.base(c);if(base.lease!==f.lease)throw new ContinuousFenceError('OWNERSHIP_MISMATCH',true);if(Number(base.revision)!==f.baseRevision||Number(ext.revision)!==f.lifeRevision)throw new ContinuousFenceError('REVISION_STALE',true);if(!base.valid)throw new ContinuousFenceError('LEASE_EXPIRED_BEFORE_ADMISSION',true);const r=await assertContinuousClaim(c,f,base,ext);const a=(await c.query('SELECT cancelled FROM genesis_cycle_attempts WHERE id=$1',[f.cycleId])).rows[0];if(a?.cancelled)throw Error('CANCELLED');return r;});}
 async phase(f:CycleFence,stage:string,hook?:PhaseHook){try{await this.check(f);await this.pool.query("UPDATE genesis_continuous_attempts SET phase=$2 WHERE cycle_id=$1 AND status='CLAIMED' AND lease=$3",[f.cycleId,stage,f.lease]);}catch(e){if(e instanceof ContinuousFenceError)throw e;throw new InterruptedCycle(e instanceof Error?e.message:'PHASE_PERSISTENCE_FAILED');}await hook?.(stage);}
 async prepare(f:CycleFence,selected:{identity:string;planner:PlannerV2},signal?:AbortSignal,hook?:PhaseHook):Promise<Prepared>{
  const {scope,authority}=await this.check(f);if(selected.identity!==scope.planner.identity)throw Error('UNADMITTED_LOCAL_PLANNER');
  const {o,life,archive,snapshot,disclosure}=await this.tx(async c=>{const {base,ext}=await this.base(c);await assertContinuousClaim(c,f,base,ext);const archive=await readMemoryArchive(c,base.state.id,Number(ext.revision));return {o:base.state,life:ext.record,archive,disclosure:await loadDisclosure(c,base.state,ext.record,archive),snapshot:await savedSnapshotReference(c,base.state.brain)};});
  const at=new Date().toISOString(),brain=new SavedObservationAdapter(o.id);if(snapshot)brain.restore(snapshot);let invoked=false;
  const planner:PlannerV2={propose:async ctx=>{if(invoked||signal?.aborted)throw new InterruptedCycle('CANCELLED');invoked=true;await this.check(f);
   let timer:ReturnType<typeof setTimeout>|undefined,poll:ReturnType<typeof setInterval>|undefined;let cancel:(()=>void)|undefined;
   try{const interrupted=new Promise<never>((_,reject)=>{timer=setTimeout(()=>reject(new Error('PLANNER_TIMEOUT')),scope.plannerTimeoutMs);poll=setInterval(()=>{void this.check(f).catch(e=>reject(e instanceof ContinuousFenceError?new ContinuousFenceError(e.message):new InterruptedCycle('CANCELLED_OR_STALE')));},50);cancel=()=>reject(new InterruptedCycle('CANCELLED'));signal?.addEventListener('abort',cancel,{once:true});});
    const p=await Promise.race([selected.planner.propose(ctx),interrupted]);await this.check(f);if(p.cost.maxMicros!==0)throw Error('LOCAL_PLANNER_NONZERO_COST');return {...p,planner:selected.identity};
   }finally{if(timer)clearTimeout(timer);if(poll)clearInterval(poll);if(cancel)signal?.removeEventListener('abort',cancel);}
  }};
  const p=await prepareCycle(o,life,brain,planner,continuousInput(authority,at),LOCAL_PERMISSION,at,f.cycleId,authority,archive,stage=>this.phase(f,stage,hook),disclosure);Object.assign(p.decision.memory.episode.record as object,{continuousAuthority:authority});await this.check(f);return p;
 }
 async commit(f:CycleFence,p:Prepared,hook?:PhaseHook){return this.tx(async c=>{
  const {base,ext}=await this.base(c),{scope,authority}=await assertContinuousClaim(c,f,base,ext);await hook?.('before_commit');
  const pending=(await c.query("SELECT id FROM genesis_provider_attempts WHERE cycle_id=$1 AND record->>'status' IN ('reserved','dispatching','unknown')",[f.cycleId])).rowCount;if(pending)throw Error('PROVIDER_AMBIGUITY');
  const wakes=p.decision.proposal&&['ALLOW','DEFER'].includes(p.decision.policy?.verdict??'')?followups(p.decision.proposal,p.life,authority.event,f.cycleId,p.decision.at,authority):[];
  for(const e of wakes)await validateFollowup(c,e);
  const d=await commitV2(c,f,p.life,p.decision);for(const e of wakes)await persistFollowup(c,e);
  await c.query("UPDATE genesis_runtime_events SET status='CONSUMED',reason=$2 WHERE id=$1",[f.eventId,d.outcome.status]);await c.query("UPDATE genesis_continuous_attempts SET status='COMMITTED',phase='committed',reserved_micros=0,failure=$2 WHERE cycle_id=$1",[f.cycleId,d.outcome.status==='failed'?'PLANNER_OR_VALIDATION_FAILURE':null]);
  await c.query("INSERT INTO genesis_continuous_journal(event_id,scope_id,cycle_id,transition,reason) VALUES($1,$2,$3,'COMMITTED',$4)",[f.eventId,scope.id,f.cycleId,d.outcome.status]);return d;
 });}
 private async close(c:pg.PoolClient,f:CycleFence,reason:string,retry:boolean){
  const {base}=await this.base(c);const a=(await c.query('SELECT * FROM genesis_continuous_attempts WHERE cycle_id=$1 FOR UPDATE',[f.cycleId])).rows[0];if(!a||a.status!=='CLAIMED'||a.lease!==f.lease)return;
  const e=(await c.query('SELECT * FROM genesis_runtime_events WHERE id=$1 FOR UPDATE',[f.eventId])).rows[0],row=(await c.query('SELECT * FROM genesis_continuous_scopes WHERE id=$1 FOR UPDATE',[a.scope_id])).rows[0];const s=row.payload as ContinuousScope;
  const unresolved=(await c.query("SELECT record FROM genesis_provider_attempts WHERE cycle_id=$1 AND record->>'status' IN ('reserved','dispatching','unknown')",[f.cycleId])).rows;const unknown=unresolved.length;let liability=0;for(const r of unresolved){if(!Number.isSafeInteger(r.record.reservedMicros)||r.record.reservedMicros<0)throw Error('Unidentified provider liability requires review');liability+=r.record.reservedMicros;}
  await this.mark(c,f);if(base.lease===f.lease)await c.query("UPDATE genesis_organisms SET lease=NULL,lease_until='-infinity',phase='idle' WHERE id='genesis'");
  const again=!unknown&&retry&&row.status==='AUTHORIZED'&&Date.parse(s.expiresAt)>Date.now()&&e.attempts<s.maxAttemptsPerEvent;
  const status=unknown?'AMBIGUOUS':again?'PENDING':reason.startsWith('CANCEL')||reason==='REVOKED'?'CANCELLED':'FAILED';
  await c.query("UPDATE genesis_runtime_events SET status=$2,reason=$3,available_at=CASE WHEN $2='PENDING' THEN now()+($4 * interval '1 millisecond') ELSE available_at END WHERE id=$1",[f.eventId,status,reason,s.backoffMs*e.attempts]);
  await c.query("UPDATE genesis_continuous_attempts SET status=$2,phase='closed',failure=$3,reserved_micros=CASE WHEN $2='AMBIGUOUS' THEN greatest(reserved_micros,$4) ELSE 0 END WHERE cycle_id=$1",[f.cycleId,unknown?'AMBIGUOUS':status==='CANCELLED'?'CANCELLED':'FAILED',reason,Math.max(liability,s.maxCostPerCycleMicros)]);
  await c.query('UPDATE genesis_cycle_attempts SET cancelled=true WHERE id=$1',[f.cycleId]);
  if(unknown&&row.status==='AUTHORIZED')await c.query("UPDATE genesis_continuous_scopes SET status='REVIEW_REQUIRED' WHERE id=$1",[s.id]);
  await c.query("INSERT INTO genesis_continuous_journal(event_id,scope_id,cycle_id,transition,reason) VALUES($1,$2,$3,$4,$5)",[f.eventId,s.id,f.cycleId,status,reason]);
 }
 async fail(f:CycleFence,reason:string,retry=false){return this.tx(c=>this.close(c,f,reason,retry));}
 async cancelEvent(id:string,reference:string){if(!reference.trim())throw Error('Cancellation reference required');return this.tx(async c=>{await this.base(c);const e=(await c.query('SELECT * FROM genesis_runtime_events WHERE id=$1 FOR UPDATE',[id])).rows[0];if(e?.status==='CLAIMED'){const a=(await c.query('SELECT * FROM genesis_continuous_attempts WHERE cycle_id=$1',[e.cycle_id])).rows[0];await this.close(c,{cycleId:a.cycle_id,lease:a.lease,eventId:id,continuousScopeId:a.scope_id,baseRevision:Number(a.base_revision),lifeRevision:Number(a.life_revision)},'CANCELLED:'+reference,false);}else if(e?.status==='PENDING'){await c.query("UPDATE genesis_runtime_events SET status='CANCELLED',reason=$2 WHERE id=$1",[id,reference]);await c.query("INSERT INTO genesis_continuous_journal(event_id,transition,reason) VALUES($1,'CANCELLED',$2)",[id,reference]);}else throw Error('Terminal/missing event');});}
 async revoke(id:string,reference:string){if(!reference.trim())throw Error('Revocation evidence required');return this.tx(async c=>{await this.base(c);const row=(await c.query('SELECT * FROM genesis_continuous_scopes WHERE id=$1 FOR UPDATE',[id])).rows[0];if(!row||!['AUTHORIZED','PROPOSED'].includes(row.status))throw Error('Scope terminal');const active=(await c.query("SELECT * FROM genesis_continuous_attempts WHERE scope_id=$1 AND status='CLAIMED'",[id])).rows;for(const a of active)await this.close(c,{cycleId:a.cycle_id,lease:a.lease,eventId:a.event_id,continuousScopeId:id,baseRevision:Number(a.base_revision),lifeRevision:Number(a.life_revision)},'REVOKED',false);const state=(await c.query('SELECT status FROM genesis_continuous_scopes WHERE id=$1',[id])).rows[0];if(state.status==='AUTHORIZED'||state.status==='PROPOSED')await c.query("UPDATE genesis_continuous_scopes SET status='REVOKED',revocation_reference=$2 WHERE id=$1",[id,reference]);await c.query("INSERT INTO genesis_continuous_journal(scope_id,transition,reason) VALUES($1,'REVOKED',$2)",[id,reference]);});}
 async recover(){return this.tx(async c=>{await this.base(c);const rows=(await c.query("SELECT a.* FROM genesis_continuous_attempts a JOIN genesis_runtime_events e ON e.id=a.event_id WHERE a.status='CLAIMED' AND e.lease_until<=clock_timestamp() ORDER BY a.cycle_id FOR UPDATE OF a")).rows;for(const a of rows)await this.close(c,{cycleId:a.cycle_id,lease:a.lease,eventId:a.event_id,continuousScopeId:a.scope_id,baseRevision:Number(a.base_revision),lifeRevision:Number(a.life_revision)},'EXPIRED_LOCAL_CLAIM',true);return rows.length;});}
}

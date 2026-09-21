import {loadAdmission} from './reasoning/store.ts';
import {loadDisclosure} from './disclosure-store.ts';
import {assertContinuousClaim,continuousInput,ContinuousFenceError} from './continuous-authority.ts';
import {LOCAL_PERMISSION} from '../core/v2/continuous.ts';
import {reduceLife} from '../core/v2/life-state.ts';
import {readMemoryArchive} from './memory-store.ts';
import type pg from 'pg';
import type {LifeStateV1,DecisionV2} from '../core/v2/contracts.ts';
import {assertOneShotClaim} from './one-shot-authority.ts';
import {compileContext} from '../core/v2/context.ts';
import {evaluatePolicy} from '../core/v2/policy.ts';
import {awakeningEventSchema} from './awakening-event.ts';
import {prepareIntentFinalization,persistIntentFinalization} from './intent-journal.ts';
import {digest} from '../core/v2/identity.ts';
export type CycleFence={cycleId:string;lease:string;baseRevision:number;lifeRevision:number;oneShotGrantId?:string;continuousScopeId?:string;eventId?:string};
/** Shared atomic commit, requiring caller-owned transaction and locked identity/extension rows.
 * No HTTP/CLI entry point; production service still refuses before reaching this function. */
export async function commitV2(c:pg.PoolClient,f:CycleFence,life:LifeStateV1,d:DecisionV2){
 if(f.oneShotGrantId&&f.continuousScopeId)throw Error('Mixed execution authorities');
 const base=(await c.query("SELECT state,revision,lease,lease_until>now() AS valid FROM genesis_organisms WHERE id='genesis' FOR UPDATE")).rows[0];
 const ext=(await c.query("SELECT record,revision FROM genesis_life_state WHERE organism_id='genesis' FOR UPDATE")).rows[0];
 const attempt=(await c.query('SELECT * FROM genesis_cycle_attempts WHERE id=$1 FOR UPDATE',[f.cycleId])).rows[0];
 if(f.continuousScopeId){
  if(!base||!ext||!attempt||attempt.status!=='preparing'||attempt.lease!==f.lease||base.lease!==f.lease)throw new ContinuousFenceError('OWNERSHIP_MISMATCH');
  if(attempt.cancelled)throw new ContinuousFenceError('CANCELLED');
  if(Number(base.revision)!==f.baseRevision||Number(ext.revision)!==f.lifeRevision)throw new ContinuousFenceError('REVISION_STALE');
  if(!base.valid)throw new ContinuousFenceError('LEASE_EXPIRED_BEFORE_ADMISSION');
  if(ext.record.executionLock!=='CLOSED')throw new ContinuousFenceError('SCOPE_INVALID');
 }
 if(!base||!ext||!attempt||attempt.cancelled||attempt.status!=='preparing'||attempt.lease!==f.lease||base.lease!==f.lease||!base.valid||(f.oneShotGrantId||f.continuousScopeId?ext.record.executionLock!=='CLOSED':ext.record.executionLock!=='OPEN')||Number(base.revision)!==f.baseRevision||Number(ext.revision)!==f.lifeRevision)throw new Error('CYCLE_FENCE_REJECTED');
 const grant=f.oneShotGrantId?await assertOneShotClaim(c,f,base,ext):null;
 const continuous=f.continuousScopeId?await assertContinuousClaim(c,f,base,ext):null;
 let authority;
 if(grant){
  const event=awakeningEventSchema.parse((d.memory.episode.record as {awakeningEvent?:unknown}).awakeningEvent);
  if(event.activationAuthorizationRef!==grant.authorizationReference||event.organismId!==base.state.id||event.permissionManifestHash!==grant.permissionHash||event.constitutionHash!==grant.constitution.hash||event.bornAt!==base.state.bornAt||event.id!==f.cycleId+':event')throw Error('Event/grant mismatch');
  authority={grantId:grant.id,grantHash:digest(grant),permissionHash:grant.permissionHash,event};
 }
 if(continuous){authority=continuous.authority;if(digest(d.event)!==digest(continuousInput(authority,d.at))||digest((d.memory.episode.record as {continuousAuthority?:unknown}).continuousAuthority)!==digest(authority))throw Error('Continuous event/context binding');}
 const permission=d.lifeContext.permission;
 if(!permission||grant&&digest(permission)!==digest(grant.permission)||continuous&&digest(permission)!==digest(LOCAL_PERMISSION))throw Error('Prepared permission mismatch');
 const archive=await readMemoryArchive(c,base.state.id,Number(ext.revision));
 const disclosure=await loadDisclosure(c,base.state,ext.record,archive);
 const context=compileContext(base.state,ext.record,d.biological,permission,12000,authority,archive,[],disclosure);
 if(context.hash!==d.lifeContext.contextHash||digest(context.manifest)!==digest(d.lifeContext.contextManifest))throw Error(continuous?'DISCLOSURE_INVALID':'One-shot context changed');
 if(d.proposal&&((grant&&d.reasoning.producer!==grant.planner.identity)||digest(evaluatePolicy(d.proposal,context,ext.record.executionLock==='CLOSED'&&!grant&&!continuous,Number(ext.revision),ext.record,base.state.businesses.map((p:{id:string})=>p.id)))!==digest(d.policy)))throw Error('Planner/policy changed');
 if(continuous&&d.proposal&&(d.reasoning.producer!==continuous.scope.planner.identity||d.policy?.verdict==='ALLOW'&&d.proposal.changes.length&&!continuous.scope.allowedEffects.includes('life_changes')||d.policy?.verdict==='ALLOW'&&d.proposal.tool&&!continuous.scope.allowedEffects.includes(d.proposal.tool as 'local_artifact'|'local_reflection')))throw Error('Continuous planner/effect outside scope');
 if((grant||continuous)&&(await c.query("SELECT id FROM genesis_provider_attempts WHERE cycle_id=$1 AND record->>'status' IN ('reserved','dispatching','unknown')",[f.cycleId])).rowCount)throw Error('Ambiguous provider outcome requires reconciliation');
 if(grant?.permission.llm){
  const r=(await c.query("SELECT record FROM genesis_provider_attempts WHERE cycle_id=$1 AND record->>'protocolVersion'='2' FOR UPDATE",[f.cycleId])).rows[0]?.record;
  if(r){const a=await loadAdmission(c,r.request.admissionId,base.state.id);const receipt=(await c.query('SELECT record FROM genesis_provider_receipts WHERE attempt_id=$1',[f.cycleId+':reasoning'])).rows[0]?.record;
   if(r.status!=='received'||digest(a)!==grant.planner.admissionHash||r.contextHash!==context.hash||!receipt||receipt.validation!=='SCHEMA_VALID'||receipt.proposalHash!==digest(d.proposal)||r.costMicros===null)throw Error('PROVIDER_RECEIPT_COMMIT_MISMATCH');
  }else {const t=(await c.query('SELECT current_database() db,current_schema() schema')).rows[0];if(t.db!=='genesis_runtime_v1_test'||!t.schema.startsWith('awakening_test_'))throw Error('DURABLE_PROVIDER_RECEIPT_REQUIRED');}
 }
 if(grant&&d.proposal?.tool&&d.action.status==='local_saved'&&!grant.allowedLocalEffects.includes(d.proposal.tool as 'local_artifact'|'local_reflection'))throw Error('Effect outside grant');
 if(d.id!==f.cycleId||d.organismId!==base.state.id||life.organismId!==base.state.id||life.revision!==f.lifeRevision+1||d.lifeContext.revision!==f.lifeRevision)throw new Error('Prepared identity/revision mismatch');
 if(life.constitutionHash!==ext.record.constitutionHash||life.executionLock!==ext.record.executionLock||digest(life.walletIdentity)!==digest(ext.record.walletIdentity)||life.biologicalContext.snapshotHash!==ext.record.biologicalContext.snapshotHash)throw new Error('Protected state mutation');
 if(d.biological.executedThisCycle||d.biological.status!=='not_applied'||d.biological.value!==null)throw new Error('Saved-only boundary');
 if(d.proposal&&(!d.policy||d.policy.payloadHash!==digest(d.proposal)))throw new Error('Policy/payload mismatch');
 if(d.action.status==='local_saved'&&(d.policy?.verdict!=='ALLOW'||!['local_reflection','local_artifact'].includes(d.proposal?.tool??'')))throw new Error('Unauthorized local effect');
 const expectedChanges=d.policy?.verdict==='ALLOW'?[...d.proposal?.changes??[]]:[];
 if(d.policy?.verdict==='REQUIRE_HUMAN_APPROVAL'&&d.proposal?.kind==='REQUEST_ASSISTANCE'&&permission.localArtifacts){
  expectedChanges.push({kind:'operational',expectedRevision:Number(ext.revision),sourceIds:[d.event.id],operation:{op:'assistance_create',id:d.id+':assistance',question:d.proposal.assistance!,projectId:d.proposal.projectId,taskId:d.proposal.taskId,relationshipId:null}});
 }
 if(digest(expectedChanges)!==digest(d.memory.changes)||digest((d.memory.episode.record as {lifeChanges?:unknown}).lifeChanges)!==digest(d.memory.changes))throw Error('Unauthorized Life State changes');
 const expectedLife=reduceLife(ext.record,d.memory.episode,d.memory.changes,d.lifeContext.contextManifest.selectedIds,base.state.businesses.map((p:{id:string})=>p.id));expectedLife.biologicalContext.observationIds.push(d.biological.id);
 if(digest(expectedLife)!==digest(life))throw Error('Life State differs from deterministic reducer');
 await c.query("SELECT set_config('genesis.writer_version','runtime-v1',true)");
 if(grant)await c.query("SELECT set_config('genesis.oneshot_grant',$1,true),set_config('genesis.oneshot_lease',$2,true)",[grant.id,f.lease]);
 if(continuous)await c.query("SELECT set_config('genesis.continuous_cycle',$1,true),set_config('genesis.continuous_lease',$2,true)",[f.cycleId,f.lease]);
 const intent=await prepareIntentFinalization(c,d);
 const episode=d.memory.episode.record as Record<string,unknown>;
 if(episode.outcomeStatus!==d.outcome.status||episode.actionStatus!==d.action.status||episode.policy!==(d.policy?.verdict??null))throw Error('Episode/decision status mismatch');
 const numbering=(await c.query('SELECT count(*) n,coalesce(max(cycle),0) m FROM genesis_decisions')).rows[0];
 if(Number(numbering.n)!==base.state.cycles||Number(numbering.m)!==base.state.cycles)throw Error('Persisted decision numbering mismatch');
 const cycle=Number(numbering.n)+1;
 await c.query('INSERT INTO genesis_decisions(id,cycle,at,record) VALUES($1,$2,$3,$4)',[d.id,cycle,d.at,{...d,cycle}]);
 await persistIntentFinalization(c,intent);
 await c.query('INSERT INTO genesis_life_events(id,organism_id,at,record) VALUES($1,$2,$3,$4)',[d.memory.episode.id,'genesis',d.at,d.memory.episode]);
 await c.query("UPDATE genesis_life_state SET revision=revision+1,record=$1 WHERE organism_id='genesis'",[{...life,baseRevision:f.baseRevision+1}]);
 await c.query("UPDATE genesis_organisms SET state=$1,revision=revision+1,lease=NULL,lease_until='-infinity',phase='idle' WHERE id='genesis'",[{...base.state,cycles:cycle,activity:'Computational life event recorded'}]);
 await c.query("UPDATE genesis_cycle_attempts SET status='committed' WHERE id=$1",[f.cycleId]);
 if(grant)await c.query("UPDATE genesis_execution_grants SET status='CONSUMED',result=$2,updated_at=now() WHERE id=$1",[grant.id,d.outcome.status==='failed'?'FAILED':d.policy?.verdict==='DENY'?'DENIED':d.outcome.status.toUpperCase()]);
 return {...d,cycle};
}

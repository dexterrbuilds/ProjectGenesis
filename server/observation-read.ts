import {operational} from '../core/v2/operations.ts';
import type pg from 'pg';
import type {Organism,Decision} from '../core/contracts.ts';
import type {DecisionV2,LifeStateV1} from '../core/v2/contracts.ts';
import type {PublicFacts} from '../core/v2/public.ts';
import {CONSTITUTION_HASH} from '../core/v2/identity.ts';
import {savedSnapshotReference} from './saved-provenance.ts';
import {readIntentRow} from './intent-journal.ts';
/** Consistent read-only projection snapshot. Optional preparation tables are never installed. */
export async function readObservation(pool:pg.Pool){
 const c=await pool.connect();
 try{
  await c.query('BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY');
  const base=(await c.query("SELECT state,phase,lease,lease_until>now() AS busy FROM genesis_organisms WHERE id='genesis'")).rows[0];
  const life:LifeStateV1=(await c.query("SELECT record FROM genesis_life_state WHERE organism_id='genesis'")).rows[0]?.record;
  if(!base||!life||base.state.id!==life.organismId||life.schemaVersion!==1||life.constitutionHash!==CONSTITUTION_HASH||life.biologicalContext.mode!=='SAVED-OBSERVATION-ONLY')throw Error('Observation identity missing or inconsistent');
  const organism:Organism=base.state;
  const records=(await c.query('SELECT record FROM genesis_decisions ORDER BY cycle DESC LIMIT 20')).rows;
  const history=records.map(r=>r.record as Decision|DecisionV2);
  const counts=(await c.query("SELECT (SELECT count(*) FROM genesis_memories) AS legacy, (SELECT count(*) FROM genesis_life_events WHERE organism_id='genesis' AND record->>'kind'='episode') AS episodes, (SELECT max(at) FROM genesis_decisions WHERE record->>'schemaVersion'='2') AS computational_at")).rows[0];
  const available=(await c.query("SELECT to_regclass('genesis_execution_grants') IS NOT NULL AS grants,to_regclass('genesis_provider_attempts') IS NOT NULL AS providers,to_regclass('genesis_continuous_attempts') IS NOT NULL AS continuous")).rows[0];
  let reviewRequired=false;let busy=Boolean(base.busy);let matched=false;
  if(available.grants){const rows=(await c.query("SELECT status,lease,(payload->>'expiresAt')::timestamptz>now() AS not_expired FROM genesis_execution_grants WHERE payload->>'organismId'=$1 AND status IN ('CLAIMED','AMBIGUOUS')",[organism.id])).rows;reviewRequired=rows.some(r=>r.status==='AMBIGUOUS'||!base.busy||r.lease!==base.lease||!r.not_expired);matched ||= rows.some(r=>r.status==='CLAIMED'&&r.lease===base.lease&&r.not_expired);}
  if(available.continuous){const rows=(await c.query("SELECT a.status,a.lease,s.status scope_status,(s.payload->>'expiresAt')::timestamptz>now() not_expired FROM genesis_continuous_attempts a JOIN genesis_continuous_scopes s ON s.id=a.scope_id WHERE a.status IN ('CLAIMED','AMBIGUOUS')")).rows;reviewRequired ||= rows.some(r=>r.status==='AMBIGUOUS'||!base.busy||r.lease!==base.lease||!r.not_expired||r.scope_status!=='AUTHORIZED');matched ||= rows.some(r=>r.status==='CLAIMED'&&r.lease===base.lease&&r.not_expired&&r.scope_status==='AUTHORIZED');}
  if(available.grants||available.continuous){busy=busy&&matched;if(base.busy&&!matched)reviewRequired=true;}
  if(available.providers){const rows=(await c.query("SELECT record FROM genesis_provider_attempts WHERE record->>'status' IN ('unknown','reserved','dispatching')")).rows;reviewRequired ||= rows.some(r=>r.record.status==='unknown'||!base.busy||r.record.fence?.lease!==base.lease);}
  const pending=(await c.query("SELECT * FROM genesis_action_intents WHERE organism_id='genesis' AND record->>'status'='awaiting_approval' ORDER BY id")).rows.map(row=>readIntentRow(row,organism.id));
  const op=operational(life);
  // New local requests have their own receipt/resolution lifecycle. Historical approval intents are not rewritten.
  const awaitingAssistance=op.assistance.some(q=>q.status==='pending')||pending.some(i=>i.proposal.kind==='REQUEST_ASSISTANCE'&&!op.assistance.some(q=>q.id===i.id.replace(/:intent$/,':assistance')));
  const awaitingApproval=pending.some(i=>i.proposal.kind!=='REQUEST_ASSISTANCE');
  const facts:PublicFacts={phase:base.phase,busy,reviewRequired,awaiting:awaitingAssistance?'assistance':awaitingApproval?'approval':null,legacyMemories:Number(counts.legacy),episodes:Number(counts.episodes),latestActivityAt:history[0]?.at??null,latestComputationalAt:counts.computational_at?new Date(counts.computational_at).toISOString():null};
  const snapshot=await savedSnapshotReference(c,organism.brain);
  const schedule=(await c.query("SELECT enabled FROM genesis_schedule WHERE id='genesis'")).rows[0];
  await c.query('COMMIT');return {organism,life,history,facts,snapshot,schedule};
 }catch(e){await c.query('ROLLBACK');throw e;}finally{c.release();}
}

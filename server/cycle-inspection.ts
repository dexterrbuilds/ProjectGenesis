/** Private, read-only durable inspection. No reconciliation, retry, grant transition or effect. */
import type pg from 'pg';
import {digest} from '../core/v2/identity.ts';
import {operatorTrace} from '../core/v2/public.ts';
import {readIntentRow} from './intent-journal.ts';
const micros=(v:unknown):number|null=>typeof v==='number'&&Number.isSafeInteger(v)&&v>=0?v:null;
export async function inspectOneShot(pool:pg.Pool,grantId:string){
 const c=await pool.connect();
 try{
  await c.query('BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY');
  const exists=(await c.query("SELECT to_regclass('genesis_execution_grants') IS NOT NULL AS present")).rows[0].present;
  if(!exists){await c.query('COMMIT');return null;}
  const g=(await c.query('SELECT *,now() AS inspected_at FROM genesis_execution_grants WHERE id=$1',[grantId])).rows[0];
  if(!g){await c.query('COMMIT');return null;}
  const organismId=g.payload.organismId;
  const base=(await c.query("SELECT state->>'id' AS id,lease,lease_until>now() AS valid FROM genesis_organisms WHERE id='genesis'")).rows[0];
  const available=(await c.query("SELECT to_regclass('genesis_cycle_attempts') IS NOT NULL AS attempts,to_regclass('genesis_provider_attempts') IS NOT NULL AS providers")).rows[0];
  const attempt=available.attempts?(await c.query('SELECT id,status,cancelled,revision FROM genesis_cycle_attempts WHERE id=$1',[g.cycle_id])).rows[0]:null;
  const decision=(await c.query('SELECT record FROM genesis_decisions WHERE id=$1',[g.cycle_id])).rows[0]?.record;
  const episode=(await c.query('SELECT record FROM genesis_life_events WHERE id=$1',[g.cycle_id+':episode'])).rows[0]?.record;
  const row=(await c.query('SELECT * FROM genesis_action_intents WHERE id=$1',[g.cycle_id+':intent'])).rows[0];
  const violations:string[]=[];
  if(base?.id!==organismId||digest(g.payload)!==g.payload_hash)violations.push('Grant identity or payload integrity mismatch');
  let intent=null;
  if(row){try{const i=readIntentRow(row,organismId);intent={id:i.id,status:i.status,revision:Number(row.revision),policy:i.policy.verdict,reservedMicros:i.reservedMicros,attempts:i.attempts,approvalRecorded:i.approval!==null,receiptRecorded:i.receipt!==null};}catch{violations.push('Malformed or incompatible intent; no repair performed');}}
  const providers=available.providers?(await c.query('SELECT id,at,record FROM genesis_provider_attempts WHERE cycle_id=$1 ORDER BY id',[g.cycle_id])).rows.map(r=>{
   const v=r.record,status=typeof v.status==='string'?v.status:'unknown';
   const unresolved=['reserved','dispatching','unknown'].includes(status);
   const recognized=['reserved','dispatching','unknown','received','not_sent','reconciled'].includes(status);
   return {id:r.id,status,reservationRecordedAt:new Date(r.at).toISOString(),dispatchRecordedAt:null,responseRecordedAt:null,dispatchMayHaveOccurred:status==='not_sent'||status==='reserved'?false:recognized?true:null,responseDurablyObserved:v.response!==null&&v.response!==undefined,reservedMicros:micros(v.reservedMicros),observedCostMicros:micros(v.costMicros),unresolvedLiabilityMicros:unresolved?micros(v.reservedMicros):recognized&&micros(v.costMicros)!==null?0:null};
  }):[];
  const committed=decision?.schemaVersion===2&&decision.organismId===organismId&&episode?.organismId===organismId&&episode?.source===g.cycle_id&&decision.memory?.episode?.id===episode.id;
  if((decision||episode)&&!committed)violations.push('Decision/episode commit evidence incomplete or inconsistent');
  if((g.status==='CONSUMED')!==!!committed)violations.push('Grant terminal state and commit evidence disagree');
  const unresolved=providers.some(p=>p.unresolvedLiabilityMicros===null||p.unresolvedLiabilityMicros>0);
  const review=g.status==='AMBIGUOUS'||g.status==='CLAIMED'&&(!base?.valid||base.lease!==g.lease||!Number.isFinite(Date.parse(g.payload.expiresAt))||Date.parse(g.payload.expiresAt)<=new Date(g.inspected_at).getTime()||attempt?.cancelled)||unresolved||violations.length>0;
  const liabilities=providers.map(p=>p.unresolvedLiabilityMicros);
  const result={schemaVersion:1,organismId,cycleId:g.cycle_id,grant:{id:g.id,status:g.status,result:g.result},attempt:attempt?{id:attempt.id,status:attempt.status,cancelled:attempt.cancelled,revision:Number(attempt.revision)}:null,
   lastDurableTransition:{state:g.status,recordedAt:new Date(g.updated_at).toISOString(),source:'execution-grant row',completeTransitionHistory:false},
   canonicalCommit:{observed:!!committed,decisionId:decision?.id??null,cycle:decision?.cycle??null,episodeId:episode?.id??null},intent,providers,
   unresolvedProviderLiabilityMicros:liabilities.some(v=>v===null)?null:liabilities.reduce<number>((sum,v)=>sum+v!,0),reviewRequired:review,integrityIssues:violations,
   automaticRetryAllowed:false,executionMayReopen:false,
   retryProhibition:'Single-use authorization never permits retry after claim. Unresolved dispatch may have reached the provider; absence of a response is not evidence of non-dispatch.',
   reconciliationEvidenceNeeded:review?['Compare committed decision and episode with the grant and attempt identities.','For each possible dispatch, obtain provider request/response and billing evidence; reservation time is not dispatch time.','Inspect intent integrity and local commit evidence. No external-effect executor exists in this scope.','A separate operator-reviewed reconciliation procedure is required; this inspection changes nothing.']:[],
   trace:committed?operatorTrace(decision):null};
  await c.query('COMMIT');return result;
 }catch(e){await c.query('ROLLBACK');throw e;}finally{c.release();}
}

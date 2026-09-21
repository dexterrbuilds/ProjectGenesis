import type pg from 'pg';
import type { LifeStateV1, DecisionV2, ActionIntent, IntentStatus, Approval } from '../core/v2/contracts.ts';
import { CONSTITUTION_HASH, digest } from '../core/v2/identity.ts';
import {commitV2,type CycleFence} from './commit-v2.ts';
import {validateIntent} from '../core/v2/intents.ts';
import {readIntentRow,type IntentRow} from './intent-journal.ts';
import { transitionIntent } from '../core/v2/policy.ts';
export class LifeExtensionStore {
 constructor(privatePool:pg.Pool){this.pool=privatePool;}
 private pool:pg.Pool;
 async read():Promise<LifeStateV1>{
  const row=(await this.pool.query("SELECT record FROM genesis_life_state WHERE organism_id='genesis'")).rows[0];
  if(!row||row.record.schemaVersion!==1||row.record.constitutionHash!==CONSTITUTION_HASH)throw new Error('Reviewed runtime migration required; never initialize a replacement');
  return row.record;
 }
 async assertExecutionAllowed():Promise<void>{
  const state=await this.read();
  if(state.executionLock==='CLOSED')throw new Error('GENESIS_EXECUTION_LOCK_CLOSED');
  // An unlock alone is insufficient: this reviewed build does not carry an activation grant.
  throw new Error('GENESIS_EXECUTION_NOT_AUTHORIZED_IN_THIS_RELEASE');
 }
 async assertDormant(){const state=await this.read();if(state.executionLock!=='CLOSED')throw new Error('Dormant release requires CLOSED lock');return state;}
 /** Atomic journal commit for a future explicitly authorized producer; default closed. */
 async commitPrepared(expectedRevision:number,life:LifeStateV1,d:DecisionV2,intent?:ActionIntent,fence?:CycleFence){
  await this.assertExecutionAllowed();
  if(!fence||fence.lifeRevision!==expectedRevision||intent)throw new Error('Reviewed lease and separately journaled intent required');
  const c=await this.pool.connect();try{await c.query('BEGIN');const result=await commitV2(c,fence,life,d);await c.query('COMMIT');return result;}catch(e){await c.query('ROLLBACK');throw e;}finally{c.release();}
 }
 async savePendingIntent(intent:ActionIntent){
  // Operator draft journal only, no implicit approval or effect. Not exposed publicly.
  const c=await this.pool.connect();try{
   await c.query('BEGIN');await c.query("SELECT id FROM genesis_organisms WHERE id='genesis' FOR UPDATE");
   const life=(await c.query("SELECT record FROM genesis_life_state WHERE organism_id='genesis' FOR UPDATE")).rows[0]?.record;
   intent=validateIntent(intent,life?.organismId);
   if(intent.payloadHash!==digest(intent.proposal)||intent.policy.payloadHash!==intent.payloadHash||life?.organismId!==intent.organismId||intent.status!=='proposed'||intent.attempts!==0||intent.reservedMicros!==0||intent.approval||intent.receipt)throw new Error('Only unexecuted draft intents allowed');
   await c.query('INSERT INTO genesis_action_intents(id,organism_id,payload_hash,record) VALUES($1,$2,$3,$4)',[intent.id,'genesis',intent.payloadHash,intent]);await c.query('COMMIT');
  }catch(e){await c.query('ROLLBACK');throw e;}finally{c.release();}
 }
 /** Private operator journal transition. No dispatcher or public approval API. */
 async recordIntentTransition(id:string,expectedRevision:number,status:IntentStatus,at:string,approval:Approval|null=null,receipt:string|null=null){
  const c=await this.pool.connect();try{
   await c.query('BEGIN');await c.query("SELECT id FROM genesis_organisms WHERE id='genesis' FOR UPDATE");
   const life=(await c.query("SELECT record FROM genesis_life_state WHERE organism_id='genesis' FOR UPDATE")).rows[0]?.record;
   if(!life)throw Error('Missing organism life state');
   const row=(await c.query('SELECT * FROM genesis_action_intents WHERE id=$1 FOR UPDATE',[id])).rows[0];
   if(!row||Number(row.revision)!==expectedRevision)throw new Error('Missing or stale intent');
   const current=readIntentRow(row as IntentRow,life.organismId);
   // Reservation/dispatch require a separately reviewed execution grant and cost
   // protocol. The dormant journal cannot create either, even with an approval.
   if(['reserved','dispatching','succeeded','local_completed','abstained'].includes(status))throw new Error('Execution/reservation disabled in dormant release');
   if(approval&&status!=='approved')throw new Error('Approval only accepted in approval transition');
   if(receipt&&status!=='reconciled')throw new Error('Receipt only accepted during reconciliation');
   if(status==='reconciled'&&!receipt)throw new Error('Reconciliation evidence required');
   const next=transitionIntent({...current,approval:approval??current.approval,receipt:receipt??current.receipt},status,at);
   await c.query('UPDATE genesis_action_intents SET record=$1,revision=revision+1 WHERE id=$2',[next,id]);
   await c.query('INSERT INTO genesis_life_events(id,organism_id,at,record) VALUES($1,$2,$3,$4)',[`${id}:transition:${expectedRevision+1}`,'genesis',at,{schemaVersion:1,kind:'administrative',source:'intent-journal',countsAsExperience:false,from:row.record.status,to:status,payloadHash:next.payloadHash}]);
   await c.query('COMMIT');return next;
  }catch(e){await c.query('ROLLBACK');throw e;}finally{c.release();}
 }
}

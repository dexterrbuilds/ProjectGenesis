import type pg from 'pg';
import type {DecisionV2,IntentStatus} from '../core/v2/contracts.ts';
import {createIntent,validateIntent,committedIntentStatus} from '../core/v2/intents.ts';
import {transitionIntent} from '../core/v2/policy.ts';
import {digest} from '../core/v2/identity.ts';
export type IntentRow={id:string;organism_id:string;payload_hash:string;revision:string|number;record:unknown};
export function readIntentRow(row:IntentRow,organismId:string){
 const intent=validateIntent(row.record,organismId);
 if(row.organism_id!=='genesis'||row.id!==intent.id||row.payload_hash!==intent.payloadHash)throw new Error('Intent journal envelope mismatch');
 return intent;
}
export async function journalIntent(c:pg.PoolClient,d:DecisionV2){
 const intent=createIntent(d);if(!intent)return;
 const owner=(await c.query("SELECT state->>'id' AS id FROM genesis_organisms WHERE id='genesis'")).rows[0]?.id;
 if(owner!==intent.organismId)throw new Error('Intent organism mismatch');
 await c.query("INSERT INTO genesis_action_intents(id,organism_id,payload_hash,record) VALUES($1,'genesis',$2,$3)",[intent.id,intent.payloadHash,intent]);
}
/** Called in the same fenced transaction as decision/episode commit. No effect dispatcher. */
export async function prepareIntentFinalization(c:pg.PoolClient,d:DecisionV2){
 committedIntentStatus(d);
 if(!d.proposal||!d.policy)return null;
 const row=(await c.query('SELECT * FROM genesis_action_intents WHERE id=$1 FOR UPDATE',[d.id+':intent'])).rows[0] as IntentRow|undefined;
 const intent=row?readIntentRow(row,d.organismId):createIntent(d)!;
 if(digest(intent.proposal)!==digest(d.proposal)||digest(intent.policy)!==digest(d.policy))throw new Error('Prepared intent changed');
 if(intent.status!=='proposed')throw new Error('Intent already processed or operator changed it');
 const next=transitionIntent(intent,committedIntentStatus(d),d.at);
 return {insert:!row,intent,next};
}
export async function persistIntentFinalization(c:pg.PoolClient,p:Awaited<ReturnType<typeof prepareIntentFinalization>>){
 if(!p)return;
 if(p.insert)await c.query("INSERT INTO genesis_action_intents(id,organism_id,payload_hash,record) VALUES($1,'genesis',$2,$3)",[p.intent.id,p.intent.payloadHash,p.intent]);
 await c.query('UPDATE genesis_action_intents SET record=$1,revision=revision+1 WHERE id=$2',[p.next,p.intent.id]);
}
export async function finalizeIntent(c:pg.PoolClient,d:DecisionV2){await persistIntentFinalization(c,await prepareIntentFinalization(c,d));}
/** Closure records only, never resolves unknown and never executes an effect. */
export async function closeUncommittedIntent(c:pg.PoolClient,cycleId:string,organismId:string,status:Extract<IntentStatus,'failed'|'cancelled'|'unknown'>,at:string){
 const row=(await c.query('SELECT * FROM genesis_action_intents WHERE id=$1 FOR UPDATE',[cycleId+':intent'])).rows[0] as IntentRow|undefined;
 if(!row)return;
 const intent=readIntentRow(row,organismId);
 if(intent.status!=='proposed')return; // committed/processed historical result must not be rewritten
 const next=transitionIntent(intent,status,at);
 await c.query('UPDATE genesis_action_intents SET record=$1,revision=revision+1 WHERE id=$2',[next,intent.id]);
}

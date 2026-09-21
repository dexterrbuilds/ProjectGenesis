import {enqueueInTransaction} from './continuous.ts';
/** Private trusted-operator library only. No HTTP/CLI client, dispatch or automatic cycle. Optional durable local event is explicitly requested. */
import type pg from 'pg';
import {z} from 'zod';
import {applyHumanResponse,humanResponseSchema,operational,operationalChangeSchema} from '../core/v2/operations.ts';
import {CONSTITUTION_HASH,digest} from '../core/v2/identity.ts';
const authorizationSchema=z.object({organismId:z.string().min(1),expectedRevision:z.number().int().nonnegative(),operatorRef:z.string().min(1).max(120),authorizationRef:z.string().min(1).max(120),wake:z.literal('ENQUEUE_IF_INSTALLED').optional(),scope:z.literal('RECORD_HUMAN_RESPONSE_ONLY')}).strict();
/** Caller must authenticate the operator. This function validates attribution, revision and scope; possession of strings is not authentication. */
export async function recordHumanResponse(pool:pg.Pool,input:unknown,authorization:unknown){
 const r=humanResponseSchema.parse(input),a=authorizationSchema.parse(authorization);
 if(a.organismId!==r.organismId)throw Error('Response authorization ownership mismatch');
 const c=await pool.connect();try{
  await c.query('BEGIN');
  const owner=(await c.query("SELECT state FROM genesis_organisms WHERE id='genesis' FOR UPDATE")).rows[0];
  const row=(await c.query("SELECT record,revision FROM genesis_life_state WHERE organism_id='genesis' FOR UPDATE")).rows[0];
  if(!owner||!row||owner.state.id!==r.organismId||row.record.organismId!==r.organismId||row.record.constitutionHash!==CONSTITUTION_HASH||Number(row.revision)!==a.expectedRevision||row.record.revision!==a.expectedRevision||Date.parse(r.receivedAt)>Date.now())throw Error('Response identity/time/revision mismatch');
  const state=operational(row.record),created=state.history.find(h=>h.operation==='assistance_create'&&h.targetId===r.requestId);
  const original=created?(await c.query("SELECT record FROM genesis_life_events WHERE id=$1 AND organism_id='genesis'",[created.sourceEvent])).rows[0]?.record:null;
  if(!original||original.organismId!==r.organismId||!(original.record?.lifeChanges??[]).some((raw:unknown)=>{const p=operationalChangeSchema.safeParse(raw);return p.success&&p.data.operation.op==='assistance_create'&&p.data.operation.id===r.requestId&&digest(p.data)===created!.changeHash;}))throw Error('Unresolved original assistance provenance');
  const eventId=r.id+':input';const op=applyHumanResponse(row.record,r,eventId);
  const event={schemaVersion:1,id:eventId,organismId:r.organismId,at:r.receivedAt,kind:'administrative',source:r.id,visibility:'private',record:{type:'human_response',countsAsExperience:false,response:r,operatorRef:a.operatorRef,authorizationRef:a.authorizationRef,responseHash:digest(r)}};
  await c.query("INSERT INTO genesis_life_events(id,organism_id,at,record) VALUES($1,'genesis',$2,$3)",[eventId,r.receivedAt,event]);
  await c.query("UPDATE genesis_life_state SET revision=revision+1,record=$1 WHERE organism_id='genesis'",[{...row.record,revision:a.expectedRevision+1,operational:op}]);
  if(a.wake==='ENQUEUE_IF_INSTALLED'){const installed=(await c.query("SELECT to_regclass('genesis_runtime_events') IS NOT NULL installed")).rows[0].installed;if(!installed)throw Error('Continuous event schema not installed');const key='response:'+digest({organismId:r.organismId,responseId:r.id});await enqueueInTransaction(c,{version:1,id:key,organismId:r.organismId,createdAt:r.receivedAt,availableAt:r.receivedAt,expiresAt:null,dedupKey:key,source:'human_input',sourceRef:eventId,visibility:'private',disclosure:{internal:true,provider:false,public:false},parentEventId:null,parentCycleId:null,rootId:key,depth:0,payload:{kind:'HUMAN_RESPONSE_RECEIVED',requestId:r.requestId,responseId:r.id,inputEventId:eventId}});}
  await c.query('COMMIT');return {eventId,requestId:r.requestId,revision:a.expectedRevision+1};
 }catch(e){await c.query('ROLLBACK');throw e;}finally{c.release();}
}

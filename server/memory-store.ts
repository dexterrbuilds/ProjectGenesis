/** Private read-only archive projection. No runtime bootstrap, network, migration or disclosure mutation. */
import type pg from 'pg';
import type {MemoryArchive} from '../core/v2/memory.ts';
export const ARCHIVE_SCAN_LIMIT=10000;
/** Existing tables only. Bounded discovery is explicit, never represented as complete if clipped. */
export async function readMemoryArchive(db:Pick<pg.PoolClient,'query'>,organismId:string,revision:number):Promise<MemoryArchive>{
 const owner=(await db.query("SELECT o.state->>'id' AS id,l.revision FROM genesis_organisms o JOIN genesis_life_state l ON l.organism_id=o.id WHERE o.id='genesis'")).rows[0];
 if(owner?.id!==organismId||Number(owner.revision)!==revision)throw Error('Memory archive ownership/revision mismatch');
 const legacy=(await db.query("SELECT id,at,decision_id,CASE WHEN octet_length(record::text)<=65536 THEN record ELSE jsonb_build_object('excluded','oversized source') END AS record FROM genesis_memories ORDER BY at DESC,id LIMIT $1",[ARCHIVE_SCAN_LIMIT+1])).rows;
 // Only the fields required for provenance and structured past outcomes. No rationale, prompts, provider diagnostics or activity arrays.
 const decisions=(await db.query(`SELECT id,at,cycle,jsonb_strip_nulls(jsonb_build_object(
 'id',record->'id','at',record->'at','cycle',record->'cycle','schemaVersion',record->'schemaVersion','organismId',record->'organismId',
 'event',CASE WHEN record ? 'schemaVersion' THEN jsonb_build_object('id',record->'event'->'id','observedAt',record->'event'->'observedAt','kind',record->'event'->'kind','source',record->'event'->'source','recall',record->'event'->'recall') END,
 'biological',CASE WHEN record ? 'schemaVersion' THEN jsonb_build_object('id',record->'biological'->'id','observedAt',record->'biological'->'observedAt','status',record->'biological'->'status','executedThisCycle',record->'biological'->'executedThisCycle') END,
 'outcome',CASE WHEN record ? 'schemaVersion' THEN jsonb_build_object('status',record->'outcome'->'status') END,
 'action',CASE WHEN record ? 'schemaVersion' THEN jsonb_build_object('status',record->'action'->'status','artifact',CASE WHEN octet_length(record->'action'->>'artifact')<=65536 THEN record->'action'->'artifact' END) END,
 'memory',CASE WHEN record ? 'schemaVersion' THEN jsonb_build_object('episode',jsonb_build_object('id',record->'memory'->'episode'->'id'),'changes','[]'::jsonb) END
 )) || CASE WHEN record ? 'schemaVersion' THEN jsonb_build_object('proposal',CASE WHEN record->'proposal'!='null'::jsonb THEN jsonb_build_object('projectId',record->'proposal'->'projectId','taskId',record->'proposal'->'taskId') ELSE 'null'::jsonb END) ELSE '{}'::jsonb END AS record
 FROM genesis_decisions ORDER BY at DESC,id LIMIT $1`,[ARCHIVE_SCAN_LIMIT+1])).rows;
 const episodes=(await db.query(`SELECT id,at,organism_id,jsonb_build_object('schemaVersion',record->'schemaVersion','id',record->'id','organismId',record->'organismId','at',record->'at','kind',record->'kind','source',record->'source','visibility',record->'visibility','record',
 jsonb_strip_nulls(jsonb_build_object('outcomeStatus',record->'record'->'outcomeStatus','actionStatus',record->'record'->'actionStatus','recall',record->'record'->'recall','lifeChanges',CASE WHEN octet_length((record->'record'->'lifeChanges')::text)<=131072 THEN record->'record'->'lifeChanges' END,'artifactOmitted',octet_length(record->'record'->>'localArtifact')>65536,'localArtifact',CASE WHEN octet_length(record->'record'->>'localArtifact')<=65536 THEN record->'record'->'localArtifact' END))) AS record
 FROM genesis_life_events WHERE organism_id='genesis' AND record->>'kind'='episode' ORDER BY at DESC,id LIMIT $1`,[ARCHIVE_SCAN_LIMIT+1])).rows;
 const inputs=(await db.query(`SELECT id,at,organism_id,jsonb_build_object('schemaVersion',record->'schemaVersion','id',record->'id','organismId',record->'organismId','at',record->'at','kind',record->'kind','source',record->'source','visibility',record->'visibility','record',jsonb_build_object('type',record->'record'->'type','response',CASE WHEN octet_length((record->'record'->'response')::text)<=16384 THEN record->'record'->'response' END,'responseHash',record->'record'->'responseHash')) AS record FROM genesis_life_events WHERE organism_id='genesis' AND record->'record'->>'type'='human_response' ORDER BY at DESC,id LIMIT $1`,[ARCHIVE_SCAN_LIMIT+1])).rows;
 const valid=(r:Record<string,unknown>,kind:'legacy'|'decision'|'episode')=>{
  const v=r.record as Record<string,unknown>|null;
  const timestamp=typeof v?.at==='string'?Date.parse(v.at):NaN;
  if(!v||v.id!==r.id||!Number.isFinite(timestamp)||timestamp!==new Date(r.at as string).getTime()||
   (kind==='legacy'&&v.sourceDecision!==r.decision_id)||(kind==='decision'&&v.cycle!==Number(r.cycle))||(kind==='episode'&&(r.organism_id!=='genesis'||v.organismId!==organismId)))return {invalidEnvelope:true};
  return v;
 };
 return {legacy:legacy.slice(0,ARCHIVE_SCAN_LIMIT).map(r=>valid(r,'legacy')),decisions:decisions.slice(0,ARCHIVE_SCAN_LIMIT).map(r=>valid(r,'decision')),episodes:episodes.slice(0,ARCHIVE_SCAN_LIMIT).map(r=>valid(r,'episode')),inputs:inputs.slice(0,ARCHIVE_SCAN_LIMIT).map(r=>valid(r,'episode')),complete:[legacy,decisions,episodes,inputs].every(a=>a.length<=ARCHIVE_SCAN_LIMIT)};
}
export async function loadMemoryArchive(pool:pg.Pool,organismId:string,revision:number){const c=await pool.connect();try{await c.query('BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY');const result=await readMemoryArchive(c,organismId,revision);await c.query('COMMIT');return result;}catch(e){await c.query('ROLLBACK');throw e;}finally{c.release();}}

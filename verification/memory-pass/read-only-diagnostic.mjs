import pg from 'pg';
import {writeFileSync} from 'node:fs';
import {readMemoryArchive} from '../../server/memory-store.ts';
import {retrieveMemory,EMPTY_QUERY} from '../../core/v2/memory.ts';
import {SavedObservationAdapter} from '../../core/v2/biology.ts';
let networkCalls=0;globalThis.fetch=async()=>{networkCalls++;throw Error('External transport prohibited');};
const pool=new pg.Pool({connectionString:process.env.DATABASE_URL}),c=await pool.connect();
try{
 await c.query('BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY');
 const o=(await c.query("SELECT state FROM genesis_organisms WHERE id='genesis'")).rows[0].state,life=(await c.query("SELECT record FROM genesis_life_state WHERE organism_id='genesis'")).rows[0].record;
 const archive=await readMemoryArchive(c,o.id,life.revision);
 const at='2026-09-20T23:59:59.000Z';
 const queries=[{name:'recent-history',query:EMPTY_QUERY},{name:'explicit-first-memory',query:{...EMPTY_QUERY,referenceIds:[archive.legacy[0]?.id??'no-id']}},{name:'existing-project',query:{...EMPTY_QUERY,projectIds:o.businesses.map(p=>p.id)}},{name:'lexical-review',query:{...EMPTY_QUERY,text:'previous experience reflection research'}}];
 const diagnostics=queries.map(({name,query})=>{
  const bio=new SavedObservationAdapter(o.id,()=>at).accept({id:'synthetic-diagnostic:'+name,kind:'digital-event',source:'read-only-memory-diagnostic-not-a-life-event',observedAt:at,recall:query});
  const s=retrieveMemory(o,life,bio,archive,query,'internal');return {syntheticEvent:name,discoveredLegacyRecords:archive.legacy.length,eligible:s.manifest.eligible,selectedIds:s.manifest.selectedIds,exclusions:s.manifest.excluded};
 });
 await c.query('COMMIT');
 writeFileSync('verification/memory-pass/seven-memory-diagnostic.json',JSON.stringify({mode:'READ-ONLY SYNTHETIC DIAGNOSTIC; NOT A CANONICAL EVENT',organismId:o.id,legacyRecords:archive.legacy.length,disclosureMetadataPresent:archive.legacy.filter(m=>m.disclosure).length,diagnostics,networkCalls,canonicalWrites:0},null,2)+'\n');
 console.log(JSON.stringify({legacy:archive.legacy.length,eligible:diagnostics.map(d=>d.eligible),selected:diagnostics.map(d=>d.selectedIds.length),networkCalls}));
}finally{c.release();await pool.end();}

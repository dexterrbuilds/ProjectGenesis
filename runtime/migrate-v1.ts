/** Explicit preparation command/library, never called on runtime startup. */
import type pg from 'pg';
import { readFile } from 'node:fs/promises';
import { initialLifeState } from '../core/v2/identity.ts';
import type { Organism } from '../core/contracts.ts';
import { createHash } from 'node:crypto';
export const ORIGINAL_TABLES=['genesis_decisions','genesis_external_observations','genesis_ledger','genesis_memories','genesis_migrations','genesis_milestones','genesis_organisms','genesis_projects','genesis_schedule'];
export async function originalRows(c:pg.PoolClient){
 const rows:Record<string,unknown[]>={};
 for(const n of ORIGINAL_TABLES)rows[n]=(await c.query(`SELECT row_to_json(t) AS row FROM "${n}" t ORDER BY row_to_json(t)::text`)).rows.map(r=>r.row);
 return rows;
}
export const rowDigest=(rows:unknown)=>createHash('sha256').update(JSON.stringify(rows)).digest('hex');
export async function migrateRuntimeV1(pool:pg.Pool, expected:{organismId:string;bornAt:string;cycles:number;baselineDigest?:string;requireExclusiveClient?:boolean}){
 const c=await pool.connect();
 try{
  await c.query('BEGIN');await c.query("SELECT pg_advisory_xact_lock(hashtext('project-genesis-schema'))");
  await c.query('SET LOCAL lock_timeout=\'5s\'');
  // Deterministic table order prevents any legacy writer racing the backup check.
  for(const table of ORIGINAL_TABLES)await c.query(`LOCK TABLE "${table}" IN SHARE ROW EXCLUSIVE MODE`);
  if(expected.requireExclusiveClient && (await c.query("SELECT 1 FROM pg_stat_activity WHERE datname=current_database() AND pid<>pg_backend_pid() AND backend_type='client backend'")).rowCount)throw new Error('Other database clients present; refusing migration');
  const before=await originalRows(c);
  if(expected.baselineDigest && rowDigest(before)!==expected.baselineDigest)throw new Error('Frozen baseline digest mismatch');
  const rs=await c.query("SELECT state,revision,lease,lease_until>NOW() AS busy FROM genesis_organisms WHERE id='genesis' FOR UPDATE");
  const o=rs.rows[0]?.state as Organism|undefined;
  if(!o||o.id!==expected.organismId||o.bornAt!==expected.bornAt||o.cycles!==expected.cycles||!o.brain||rs.rows[0].busy||rs.rows[0].lease)throw new Error('Existing identity/state/lease mismatch; refusing migration');
  const schedule=await c.query("SELECT * FROM genesis_schedule WHERE id='genesis' FOR UPDATE");
  if(schedule.rows.length!==1||schedule.rows[0].enabled)throw new Error('Disabled schedule required');
  if((await c.query("SELECT version FROM genesis_migrations WHERE version='003'")).rowCount){
   const existing=(await c.query("SELECT record FROM genesis_life_state WHERE organism_id='genesis'")).rows[0]?.record;
   if(existing?.organismId!==o.id||existing?.executionLock!=='CLOSED')throw new Error('Invalid migrated identity or execution lock');
   await c.query('COMMIT');return {applied:false};
  }
  await c.query(await readFile(new URL('./migrations/003_runtime_v1.sql',import.meta.url),'utf8'));
  const life=initialLifeState(o,Number(rs.rows[0].revision));
  await c.query('INSERT INTO genesis_life_state(organism_id,schema_version,record) VALUES($1,1,$2)',['genesis',life]);
  await c.query('INSERT INTO genesis_life_events(id,organism_id,at,record) VALUES($1,$2,NOW(),$3)',[o.id+':runtime-v1-migration','genesis',{schemaVersion:1,kind:'administrative',source:'reviewed-runtime-v1-migration',countsAsExperience:false,constitutionHash:life.constitutionHash}]);
  await c.query("INSERT INTO genesis_migrations(version) VALUES('003')");
  const after=await originalRows(c);after.genesis_migrations=after.genesis_migrations.filter(row=>(row as {version:string}).version!=='003');
  if(rowDigest(after)!==rowDigest(before))throw new Error('Original row preservation failed; rolling back');
  await c.query('COMMIT');return {applied:true};
 }catch(e){await c.query('ROLLBACK');throw e;}finally{c.release();}
}

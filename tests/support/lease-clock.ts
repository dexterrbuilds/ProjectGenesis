/** Disposable owner-only database clock seam. No production import, GUC or env override. */
import type pg from 'pg';
export async function leaseClock(pool:pg.Pool){
 const target=(await pool.query('SELECT current_database() db,current_schema() s')).rows[0];
 if(target.db!=='genesis_runtime_v1_test'||!/^awakening_test_[a-z0-9_]+$/.test(target.s))throw Error('DISPOSABLE_CLOCK_ONLY');
 const schema=target.s as string;
 await pool.query('CREATE TABLE lease_test_time(t timestamptz NOT NULL)');
 await pool.query('INSERT INTO lease_test_time VALUES(clock_timestamp())');
 await pool.query(`CREATE FUNCTION lease_test_clock() RETURNS timestamptz LANGUAGE sql VOLATILE AS 'SELECT t FROM ${schema}.lease_test_time'`);
 // Replace only the authoritative primitive in this disposable schema's trigger.
 const def=(await pool.query("SELECT pg_get_functiondef('genesis_admit_continuous_decision()'::regprocedure) d")).rows[0].d as string;
 await pool.query(def.replaceAll('clock_timestamp()',schema+'.lease_test_clock()'));
 const wrap=(c:Pick<pg.PoolClient,'query'>)=>({query:((sql:unknown,...args:unknown[])=>{
  if(typeof sql==='string')sql=sql.replaceAll('clock_timestamp()',schema+'.lease_test_clock()').replaceAll('now()',schema+'.lease_test_clock()');
  return (c.query as (...args:unknown[])=>unknown).call(c,sql,...args);
 }) as pg.PoolClient['query']});
 const wrapped={...wrap(pool),connect:async()=>{const c=await pool.connect();return {...wrap(c),release:()=>c.release()};}} as pg.Pool;
 return {pool:wrapped,async advance(ms:number){await pool.query("UPDATE lease_test_time SET t=t+($1 * interval '1 millisecond')",[ms]);},async deadline(offset=0){await pool.query("UPDATE lease_test_time SET t=(SELECT lease_until FROM genesis_runtime_events WHERE status='CLAIMED' LIMIT 1)+($1 * interval '1 millisecond')",[offset]);}};
}

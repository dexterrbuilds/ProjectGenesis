import {loadMemoryArchive} from './memory-store.ts';
/** Isolated activation harness. No factory accepting canonical DBs; no runtime boot import. */
import pg from 'pg';
import {randomUUID} from 'node:crypto';
import {readFileSync} from 'node:fs';
import {commitV2,type CycleFence} from './commit-v2.ts';
import {prepareCycle} from '../core/v2/cycle.ts';
import {SavedObservationAdapter} from '../core/v2/biology.ts';
import {journalIntent} from './intent-journal.ts';
import {savedSnapshotReference} from './saved-provenance.ts';
import type {Permissions,PlannerV2,DecisionV2,LifeStateV1} from '../core/v2/contracts.ts';
export class IsolatedCycle {
 readonly pool:pg.Pool;
 private constructor(pool:pg.Pool){this.pool=pool;}
 static async connect(pool:pg.Pool){
  const r=(await pool.query('SELECT current_database() AS db,current_schema() AS schema')).rows[0];
  const o=(await pool.query("SELECT state FROM genesis_organisms WHERE id='genesis'")).rows[0]?.state;
  if(r.db!=='genesis_runtime_v1_test'||!r.schema.startsWith('awakening_test_')||!o?.id.startsWith('fixture-'))throw new Error('Dedicated sanitized fixture required');
  return new IsolatedCycle(pool);
 }
 async installPreparationSchema(){await this.pool.query(readFileSync(new URL('../runtime/preparation-schema.sql',import.meta.url),'utf8'));}
 async tx<T>(fn:(c:pg.PoolClient)=>Promise<T>){const c=await this.pool.connect();try{await c.query('BEGIN');await c.query("SELECT set_config('genesis.writer_version','runtime-v1',true)");const result=await fn(c);await c.query('COMMIT');return result;}catch(e){await c.query('ROLLBACK');throw e;}finally{c.release();}}
 async claim(id:string):Promise<CycleFence>{return this.tx(async c=>{
  const base=(await c.query("SELECT state,revision,lease_until>now() AS busy FROM genesis_organisms WHERE id='genesis' FOR UPDATE")).rows[0];
  const ext=(await c.query("SELECT record,revision FROM genesis_life_state WHERE organism_id='genesis' FOR UPDATE")).rows[0];
  if(ext.record.executionLock!=='OPEN'||base.busy)throw new Error('LOCKED_OR_BUSY');
  const lease=randomUUID();const f={cycleId:id,lease,baseRevision:Number(base.revision),lifeRevision:Number(ext.revision)};
  await c.query('INSERT INTO genesis_cycle_attempts(id,lease,revision,status) VALUES($1,$2,$3,\'preparing\')',[id,lease,f.baseRevision]);
  await c.query("UPDATE genesis_organisms SET lease=$1,lease_until=now()+interval '30 seconds',phase='planning' WHERE id='genesis'",[lease]);return f;
 });}
 async check(f:CycleFence){
  const r=(await this.pool.query("SELECT o.lease,o.revision,o.lease_until>now() AS valid,l.record->>'executionLock' AS lock,l.revision AS life_revision,a.cancelled,a.lease AS attempt_lease,a.status FROM genesis_organisms o CROSS JOIN genesis_life_state l JOIN genesis_cycle_attempts a ON a.id=$1 WHERE o.id='genesis'",[f.cycleId])).rows[0];
  if(!r||r.lease!==f.lease||r.attempt_lease!==f.lease||!r.valid||r.cancelled||r.status!=='preparing'||r.lock!=='OPEN'||Number(r.revision)!==f.baseRevision||Number(r.life_revision)!==f.lifeRevision)throw new Error('CYCLE_FENCE_REJECTED');
 }
 async cancel(id:string){await this.pool.query('UPDATE genesis_cycle_attempts SET cancelled=true WHERE id=$1',[id]);}
 async prepare(f:CycleFence,planner:PlannerV2,permission:Permissions){
  await this.check(f);const o=(await this.pool.query("SELECT state FROM genesis_organisms WHERE id='genesis'")).rows[0].state;
  const life:LifeStateV1=(await this.pool.query("SELECT record FROM genesis_life_state WHERE organism_id='genesis'")).rows[0].record;
  const brain=new SavedObservationAdapter(o.id);const snapshot=await savedSnapshotReference(this.pool,o.brain);if(snapshot)brain.restore(snapshot);
  const at=new Date().toISOString();const result=await prepareCycle(o,life,brain,planner,{id:f.cycleId+':event',kind:'digital-event',source:'isolated-harness',observedAt:at},permission,at,f.cycleId,undefined,await loadMemoryArchive(this.pool,o.id,life.revision));
  await this.check(f);return result;
 }
 async journal(f:CycleFence,d:DecisionV2){await this.check(f);if(d.id!==f.cycleId)throw Error('Intent cycle mismatch');if(!d.proposal||!d.policy)return;
  await this.tx(async c=>{
   await c.query("SELECT id FROM genesis_organisms WHERE id='genesis' FOR UPDATE");
   // Journaling never executes; commit repeats the complete fence under row locks.
   await journalIntent(c,d);
  });
 }
 async commit(f:CycleFence,result:{life:LifeStateV1;decision:DecisionV2}){return this.tx(c=>commitV2(c,f,result.life,result.decision));}
}

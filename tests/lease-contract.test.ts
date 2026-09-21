import test from 'node:test';
import assert from 'node:assert/strict';
import type pg from 'pg';
import {readFileSync} from 'node:fs';
import {continuousFixture,manual} from './support/continuous-fixture.ts';
import {leaseClock} from './support/lease-clock.ts';
import {ContinuousController,SimulatedCrash} from '../server/continuous.ts';
import {ProductFallback} from '../core/v2/planner.ts';
const limits={leaseMs:250,plannerTimeoutMs:100};
async function counts(pool:pg.Pool){return (await pool.query("SELECT (SELECT count(*)::int FROM genesis_decisions) decisions,(SELECT count(*)::int FROM genesis_life_events WHERE record->>'kind'='episode') episodes,(SELECT count(*)::int FROM genesis_continuous_admissions) admissions,(SELECT count(*)::int FROM genesis_runtime_events WHERE status='CONSUMED') consumed")).rows[0];}
async function setup(h:ContinuousController,s:Parameters<typeof manual>[0]){const clock=await leaseClock(h.pool),c=new ContinuousController(clock.pool);await c.enqueue(manual(s),'fixture-operator');const f=(await c.claim(s.id))!;const p=await c.prepare(f,{identity:s.planner.identity,planner:new ProductFallback()});return {clock,c,f,p};}

test('lease contract A/B: pristine before-claim crash and fresh atomic publication',()=>continuousFixture(async(h,s,w)=>{
 await h.enqueue(manual(s),'fixture-operator');await assert.rejects(w.tick(undefined,async stage=>{if(stage==='before_claim')throw new SimulatedCrash();}));
 assert.deepEqual((await h.pool.query('SELECT status,attempts,cycle_id,lease,lease_until FROM genesis_runtime_events')).rows[0],{status:'PENDING',attempts:0,cycle_id:null,lease:null,lease_until:null});
 for(const t of ['genesis_continuous_attempts','genesis_cycle_attempts','genesis_continuous_admissions'])assert.equal((await h.pool.query(`SELECT count(*)::int n FROM ${t}`)).rows[0].n,0);
 assert.equal((await counts(h.pool)).decisions,7);assert.equal(await h.recover(),0);
 const f=await h.claim(s.id);assert.ok(f);const r=(await h.pool.query('SELECT a.lease=a2.lease AND a.lease=e.lease AND e.lease=o.lease exact,a.lease_until=e.lease_until AND e.lease_until=o.lease_until same,extract(epoch FROM(a.lease_until-a.claim_issued_at))*1000 duration FROM genesis_continuous_attempts a JOIN genesis_cycle_attempts a2 ON a2.id=a.cycle_id JOIN genesis_runtime_events e ON e.id=a.event_id CROSS JOIN genesis_organisms o')).rows[0];
 assert.deepEqual(r,{exact:true,same:true,duration:'250.000000'});
},limits));

test('lease contract C: frozen authoritative DB clock commits once, not a process clock mock',()=>continuousFixture(async(h,s)=>{
 const {c,f,p}=await setup(h,s);await c.commit(f,p);assert.equal((await counts(h.pool)).decisions,8);assert.equal((await counts(h.pool)).admissions,1);assert.equal((await counts(h.pool)).episodes,1);assert.equal((await counts(h.pool)).consumed,1);await assert.rejects(c.commit(f,p));
},limits));
for(const offset of [0,1])test('lease contract D: final DB equality/expiry refuses at '+offset+'ms',()=>continuousFixture(async(h,s)=>{
 const {clock,c,f,p}=await setup(h,s);await clock.deadline(offset);
 // Call shared commit directly so the SQL gate, not an early controller check, is exercised.
 const db=await h.pool.connect();try{await db.query('BEGIN');await db.query("SELECT set_config('genesis.writer_version','runtime-v1',true),set_config('genesis.continuous_cycle',$1,true),set_config('genesis.continuous_lease',$2,true)",[f.cycleId,f.lease]);
 await assert.rejects(db.query('INSERT INTO genesis_decisions(id,cycle,at,record) VALUES($1,8,$2,$3)',[p.decision.id,p.decision.at,{...p.decision,cycle:8}]),/LEASE_EXPIRED_BEFORE_ADMISSION/);await db.query('ROLLBACK');
 }finally{db.release();}assert.equal((await counts(h.pool)).decisions,7);assert.equal((await counts(h.pool)).admissions,0);await assert.rejects(c.commit(f,p),/LEASE_EXPIRED/);
},limits));

test('lease contract: BEGIN before expiry does not authorize final SQL insertion after expiry',()=>continuousFixture(async(h,s)=>{
 const {clock,f,p}=await setup(h,s);const db=await h.pool.connect();try{await db.query('BEGIN');await clock.deadline(1);await db.query("SELECT set_config('genesis.writer_version','runtime-v1',true),set_config('genesis.continuous_cycle',$1,true),set_config('genesis.continuous_lease',$2,true)",[f.cycleId,f.lease]);await assert.rejects(db.query('INSERT INTO genesis_decisions(id,cycle,at,record) VALUES($1,8,$2,$3)',[p.decision.id,p.decision.at,p.decision]),/LEASE_EXPIRED_BEFORE_ADMISSION/);await db.query('ROLLBACK');}finally{db.release();}
 assert.equal((await counts(h.pool)).decisions,7);
},limits));

// Intercept the actual driver solely in tests, at completion of the admitted INSERT.
function pausedCommit(h:ContinuousController,onAdmitted:()=>Promise<void>){
 const connect=h.pool.connect.bind(h.pool);const pool={query:h.pool.query.bind(h.pool),connect:async()=>{const c=await connect();return {release:()=>c.release(),query:async(sql:string,args?:unknown[])=>{const r=await c.query(sql,args);if(sql.startsWith('INSERT INTO genesis_decisions'))await onAdmitted();return r;}};}} as unknown as pg.Pool;
 return new ContinuousController(pool);
}
function trackedController(c:ContinuousController){
 let identify!:(n:number)=>void;const pid=new Promise<number>(r=>identify=r);
 const pool={query:c.pool.query.bind(c.pool),connect:async()=>{const db=await c.pool.connect();identify((await db.query('SELECT pg_backend_pid() pid')).rows[0].pid);return db;}} as pg.Pool;
 return {controller:new ContinuousController(pool),pid};
}
for(const rollback of [false,true])test('lease contract: admitted tail crosses expiry; '+(rollback?'rollback then bounded recovery':'commit excludes recovery'),()=>continuousFixture(async(h,s)=>{
 const {clock,c,f,p}=await setup(h,s);let competitor:Promise<number>|undefined;
 const paused=pausedCommit(c,async()=>{await clock.deadline(1);const tracked=trackedController(c);competitor=tracked.controller.recover();await blocked(h.pool,await tracked.pid);if(rollback)throw Error('TEST_ROLLBACK');});
 if(rollback){await assert.rejects(paused.commit(f,p),/TEST_ROLLBACK/);assert.equal(await competitor,1);assert.equal((await counts(h.pool)).decisions,7);assert.equal((await counts(h.pool)).admissions,0);}
 else{await paused.commit(f,p);assert.equal(await competitor,0);assert.equal((await counts(h.pool)).decisions,8);assert.equal((await counts(h.pool)).consumed,1);}
},limits));

test('lease contract: admission wins before revoke; revoke serializes afterward',()=>continuousFixture(async(h,s)=>{
 const {c,f,p}=await setup(h,s);let revoke:Promise<void>|undefined;await pausedCommit(c,async()=>{const tracked=trackedController(c);revoke=tracked.controller.revoke(s.id,'fixture-stop');await blocked(h.pool,await tracked.pid);}).commit(f,p);await revoke;assert.equal((await counts(h.pool)).decisions,8);assert.equal((await h.pool.query('SELECT status FROM genesis_continuous_scopes')).rows[0].status,'REVOKED');
},limits));
test('lease contract: revoke before admission refuses effects',()=>continuousFixture(async(h,s)=>{const {c,f,p}=await setup(h,s);await c.revoke(s.id,'fixture-stop');await assert.rejects(c.commit(f,p));assert.equal((await counts(h.pool)).decisions,7);},limits));

test('lease contract E: recovery creates a new token; old generation cannot commit',()=>continuousFixture(async(h,s)=>{
 const {clock,c,f,p}=await setup(h,s);await clock.deadline(1);assert.equal(await c.recover(),1);await clock.advance(1000);
 const next=(await c.claim(s.id))!;assert.ok(next);assert.notEqual(next.lease,f.lease);assert.notEqual(next.cycleId,f.cycleId);await assert.rejects(c.commit(f,p),/OWNERSHIP_MISMATCH/);assert.equal((await counts(h.pool)).decisions,7);
},limits));

test('lease contract F: two claims have one owner; acknowledgement never renews',()=>continuousFixture(async(h,s)=>{
 const clock=await leaseClock(h.pool),c=new ContinuousController(clock.pool);await c.enqueue(manual(s),'fixture-operator');const claims=await Promise.all([c.claim(s.id),c.claim(s.id)]);assert.equal(claims.filter(Boolean).length,1);
 const before=(await h.pool.query('SELECT lease_until FROM genesis_runtime_events')).rows[0];await c.check(claims.find(Boolean)!);assert.deepEqual((await h.pool.query('SELECT lease_until FROM genesis_runtime_events')).rows[0],before);
},limits));

test('lease contract: no planner/provider/archive/context/discovery/callback after admission',()=>continuousFixture(async(h,s)=>{
 const {c,f,p}=await setup(h,s);let tail=false;const sqls:string[]=[];const connect=c.pool.connect.bind(c.pool);
 const proxy={query:c.pool.query.bind(c.pool),connect:async()=>{const db=await connect();return {release:()=>db.release(),query:async(sql:string,args?:unknown[])=>{if(tail){sqls.push(sql);assert.ok(!/genesis_memories|genesis_disclosure_reviews|genesis_control_state|pg_sleep/.test(sql));}const r=await db.query(sql,args);if(sql.startsWith('INSERT INTO genesis_decisions'))tail=true;return r;}};}} as unknown as pg.Pool;
 await new ContinuousController(proxy).commit(f,p,async()=>{assert.equal(tail,false);});assert.ok(tail);assert.ok(sqls.some(s=>s==='COMMIT'));
 const commit=readFileSync('server/commit-v2.ts','utf8').split("await c.query('INSERT INTO genesis_decisions")[1];assert.ok(!/compileContext\(|readMemoryArchive\(|loadDisclosure\(|\.propose\(|fetch\(|hook\?/.test(commit));
},limits));

async function blocked(pool:pg.Pool,pid:number){
 for(let n=0;n<200;n++)if((await pool.query('SELECT cardinality(pg_blocking_pids($1))>0 blocked',[pid])).rows[0].blocked)return;
 throw Error('Expected database lock wait not observed');
}
test('lease contract: claim lock wait precedes issuance and cannot spend the new 250ms interval',()=>continuousFixture(async(h,s)=>{
 const clock=await leaseClock(h.pool);await h.enqueue(manual(s),'fixture-operator');const holder=await h.pool.connect();await holder.query('BEGIN');await holder.query('SELECT id FROM genesis_organisms FOR UPDATE');
 let identify!:(pid:number)=>void;const pid=new Promise<number>(r=>identify=r);const wrapped={query:clock.pool.query.bind(clock.pool),connect:async()=>{const c=await clock.pool.connect();identify((await c.query('SELECT pg_backend_pid() pid')).rows[0].pid);return c;}} as pg.Pool;
 const c=new ContinuousController(wrapped),claim=c.claim(s.id);
 try{await blocked(h.pool,await pid);await clock.advance(1000);}finally{await holder.query('ROLLBACK');holder.release();}
 assert.ok(await claim);const row=(await h.pool.query('SELECT a.claim_issued_at=t.t same,extract(epoch FROM(a.lease_until-a.claim_issued_at))*1000 ms FROM genesis_continuous_attempts a CROSS JOIN lease_test_time t')).rows[0];assert.equal(row.same,true);assert.equal(Number(row.ms),250);
},limits));

test('lease contract: final INSERT waiting on ownership lock cannot use pre-wait transaction time',()=>continuousFixture(async(h,s)=>{
 const {clock,f,p}=await setup(h,s);const holder=await h.pool.connect(),db=await h.pool.connect();await holder.query('BEGIN');await holder.query('SELECT id FROM genesis_organisms FOR UPDATE');await db.query('BEGIN');const pid=(await db.query('SELECT pg_backend_pid() pid')).rows[0].pid;
 await db.query("SELECT set_config('genesis.writer_version','runtime-v1',true),set_config('genesis.continuous_cycle',$1,true),set_config('genesis.continuous_lease',$2,true)",[f.cycleId,f.lease]);
 const insert=db.query('INSERT INTO genesis_decisions(id,cycle,at,record) VALUES($1,8,$2,$3)',[p.decision.id,p.decision.at,p.decision]);const rejection=assert.rejects(insert,/LEASE_EXPIRED_BEFORE_ADMISSION/);
 try{await blocked(h.pool,pid);await clock.deadline(1);}finally{await holder.query('ROLLBACK');holder.release();}
 try{await rejection;await db.query('ROLLBACK');}finally{db.release();}assert.equal((await counts(h.pool)).decisions,7);
},limits));

test('lease contract: claim publication rollback leaves pristine ownership',()=>continuousFixture(async(h,s)=>{
 await h.enqueue(manual(s),'fixture-operator');const connect=h.pool.connect.bind(h.pool);
 const proxy={query:h.pool.query.bind(h.pool),connect:async()=>{const c=await connect();return {release:()=>c.release(),query:async(sql:string,args?:unknown[])=>{const r=await c.query(sql,args);if(sql.includes("'CLAIMED')")&&sql.includes('genesis_continuous_journal'))throw Error('CRASH_BEFORE_PUBLICATION');return r;}};}} as unknown as pg.Pool;
 await assert.rejects(new ContinuousController(proxy).claim(s.id),/CRASH_BEFORE_PUBLICATION/);assert.equal((await h.pool.query('SELECT status FROM genesis_runtime_events')).rows[0].status,'PENDING');assert.equal((await h.pool.query('SELECT count(*)::int n FROM genesis_continuous_attempts')).rows[0].n,0);assert.equal((await h.pool.query('SELECT lease FROM genesis_organisms')).rows[0].lease,null);
},limits));

test('lease contract: lost claim acknowledgement cannot duplicate or extend published ownership',()=>continuousFixture(async(h,s)=>{
 const clock=await leaseClock(h.pool);await h.enqueue(manual(s),'fixture-operator');const proxy={query:clock.pool.query.bind(clock.pool),connect:async()=>{const c=await clock.pool.connect();return {release:()=>c.release(),query:async(sql:string,args?:unknown[])=>{const r=await c.query(sql,args);if(sql==='COMMIT')throw Error('CLAIM_ACK_LOST');return r;}};}} as unknown as pg.Pool;
 await assert.rejects(new ContinuousController(proxy).claim(s.id),/CLAIM_ACK_LOST/);const row=(await h.pool.query('SELECT cycle_id,lease,lease_until FROM genesis_runtime_events')).rows[0];assert.ok(row.lease);assert.equal(await new ContinuousController(clock.pool).claim(s.id),null);assert.deepEqual((await h.pool.query('SELECT cycle_id,lease,lease_until FROM genesis_runtime_events')).rows[0],row);
},limits));

test('lease contract: disclosure epoch invalidation before final SQL admission refuses',()=>continuousFixture(async(h,s)=>{
 await h.pool.query(readFileSync('runtime/operator-schema-v1.sql','utf8'));const {f,p}=await setup(h,s);await h.pool.query('UPDATE genesis_control_state SET review_revision=review_revision+1');
 const db=await h.pool.connect();try{await db.query('BEGIN');await db.query("SELECT set_config('genesis.writer_version','runtime-v1',true),set_config('genesis.continuous_cycle',$1,true),set_config('genesis.continuous_lease',$2,true)",[f.cycleId,f.lease]);await assert.rejects(db.query('INSERT INTO genesis_decisions(id,cycle,at,record) VALUES($1,8,$2,$3)',[p.decision.id,p.decision.at,p.decision]),/DISCLOSURE_INVALID/);await db.query('ROLLBACK');}finally{db.release();}assert.equal((await counts(h.pool)).decisions,7);
},limits));

test('lease contract: no caller admission GUC bypasses protected writes before decision fence',()=>continuousFixture(async(h,s)=>{
 const {f}=await setup(h,s);const db=await h.pool.connect();try{await db.query('BEGIN');await db.query("SELECT set_config('genesis.continuous_cycle',$1,true),set_config('genesis.continuous_lease',$2,true),set_config('genesis.admitted','true',true)",[f.cycleId,f.lease]);await assert.rejects(db.query('UPDATE genesis_life_state SET revision=revision+1'),/CONTINUOUS_ADMISSION_REQUIRED/);await db.query('ROLLBACK');}finally{db.release();}
},limits));

test('lease contract: final expiry is terminal, while abandoned claimed expiry retains bounded recovery',()=>continuousFixture(async(h,s)=>{
 const {clock,c,f,p}=await setup(h,s);await clock.deadline(1);await assert.rejects(c.commit(f,p),/LEASE_EXPIRED_BEFORE_ADMISSION/);await c.fail(f,'LEASE_EXPIRED_BEFORE_ADMISSION',false);assert.equal((await h.pool.query('SELECT status FROM genesis_runtime_events')).rows[0].status,'FAILED');assert.equal(await c.recover(),0);
},limits));

test('lease contract: admitted local artifact, episode and intent commit coherently',()=>continuousFixture(async(h,s)=>{
 const clock=await leaseClock(h.pool),c=new ContinuousController(clock.pool);await c.enqueue(manual(s),'fixture-operator');const f=(await c.claim(s.id))!;
 const p=await c.prepare(f,{identity:s.planner.identity,planner:{propose:async ctx=>({...await new ProductFallback().propose(ctx),kind:'PROPOSAL',tool:'local_artifact',arguments:{text:'Bounded private fixture note'}})}});
 const d=await c.commit(f,p);assert.equal(d.action.status,'local_saved');assert.equal((await counts(h.pool)).episodes,1);assert.equal((await h.pool.query('SELECT record FROM genesis_action_intents')).rows[0].record.status,'local_completed');
},limits));

test('lease contract: planner timer starts at invocation, clears, and never extends lease',()=>continuousFixture(async(h,s)=>{
 const clock=await leaseClock(h.pool),c=new ContinuousController(clock.pool);await c.enqueue(manual(s),'fixture-operator');const f=(await c.claim(s.id))!,before=(await h.pool.query('SELECT lease_until FROM genesis_runtime_events')).rows[0];
 const originalSet=globalThis.setTimeout,originalClear=globalThis.clearTimeout;const active=new Set<Parameters<typeof clearTimeout>[0]>();let started=0;
 globalThis.setTimeout=((fn:()=>void,ms?:number,...args:unknown[])=>{const t=originalSet(fn,ms,...args);if(ms===100){active.add(t);started++;}return t;}) as typeof setTimeout;
 globalThis.clearTimeout=((t:Parameters<typeof clearTimeout>[0])=>{active.delete(t);return originalClear(t);}) as typeof clearTimeout;
 try{const p=await c.prepare(f,{identity:s.planner.identity,planner:{propose:async ctx=>{assert.equal(active.size,1);return new ProductFallback().propose(ctx);}}});assert.equal(started,1);assert.equal(active.size,0);await c.commit(f,p);}finally{globalThis.setTimeout=originalSet;globalThis.clearTimeout=originalClear;}
 assert.deepEqual((await h.pool.query('SELECT lease_until FROM genesis_runtime_events')).rows[0],before);
},limits));

test('lease contract: 100ms planner timeout is separate from 250ms admission and cannot resurrect expiry',()=>continuousFixture(async(h,s)=>{
 const {clock,c,f}=await setup(h,s);await assert.rejects(c.prepare(f,{identity:s.planner.identity,planner:{propose:async()=>{await clock.deadline(1);return new Promise<never>(()=>{});}}}));assert.equal((await counts(h.pool)).decisions,7);await assert.rejects(c.check(f),/LEASE_EXPIRED/);
},limits));

test('lease contract: lost commit acknowledgement preserves one committed outcome for inspection',()=>continuousFixture(async(h,s)=>{
 const {c,f,p}=await setup(h,s);const proxy={query:c.pool.query.bind(c.pool),connect:async()=>{const db=await c.pool.connect();return {release:()=>db.release(),query:async(sql:string,args?:unknown[])=>{const r=await db.query(sql,args);if(sql==='COMMIT')throw Error('COMMIT_ACK_LOST');return r;}};}} as unknown as pg.Pool;
 await assert.rejects(new ContinuousController(proxy).commit(f,p),/COMMIT_ACK_LOST/);assert.equal((await counts(h.pool)).decisions,8);assert.equal((await counts(h.pool)).episodes,1);assert.equal(await c.claim(s.id),null);await assert.rejects(c.commit(f,p));
},limits));

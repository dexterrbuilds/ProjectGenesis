import test from 'node:test';
import assert from 'node:assert/strict';
import type pg from 'pg';
import {continuousFixture,manual} from './support/continuous-fixture.ts';
import {SimulatedCrash} from '../server/continuous.ts';
import {assertContinuousClaim} from '../server/continuous-authority.ts';
const limits={leaseMs:250,plannerTimeoutMs:100};
const skip=!process.env.TEST_DATABASE_URL;

test('Short lease: before_claim crash creates no durable attempt or lease',{skip},()=>continuousFixture(async(h,s,w)=>{
 await h.enqueue(manual(s),'fixture-operator');
 await assert.rejects(w.tick(undefined,async phase=>{if(phase==='before_claim')throw new SimulatedCrash(phase);}),SimulatedCrash);
 const e=(await h.pool.query('SELECT status,attempts,cycle_id,lease,lease_until FROM genesis_runtime_events')).rows[0];
 assert.deepEqual(e,{status:'PENDING',attempts:0,cycle_id:null,lease:null,lease_until:null});
 assert.equal((await h.pool.query('SELECT count(*) n FROM genesis_continuous_attempts')).rows[0].n,'0');
 assert.equal((await h.pool.query('SELECT count(*) n FROM genesis_cycle_attempts')).rows[0].n,'0');
 assert.equal(await h.recover(),0);
 const fresh=await h.claim(s.id);assert.ok(fresh);assert.equal(fresh.cycleId,'manual:attempt:1');
 assert.equal((await h.pool.query('SELECT count(*) n FROM genesis_decisions')).rows[0].n,'7');
},limits));

test('Short lease: after_claim crash remains claimed until expiry; recovery issues distinct fresh lease',{skip},()=>continuousFixture(async(h,s,w)=>{
 await h.enqueue(manual(s),'fixture-operator');
 await assert.rejects(w.tick(undefined,async phase=>{if(phase==='after_claim')throw new SimulatedCrash(phase);}),SimulatedCrash);
 const old=(await h.pool.query('SELECT * FROM genesis_continuous_attempts')).rows[0];
 assert.equal(old.status,'CLAIMED');assert.equal(old.phase,'claimed');
 await h.pool.query('SELECT pg_sleep(0.27)');assert.equal(await h.recover(),1);
 await h.pool.query('SELECT pg_sleep(0.02)');const fresh=await h.claim(s.id);assert.ok(fresh);
 assert.notEqual(fresh.lease,old.lease);assert.equal(fresh.cycleId,'manual:attempt:2');
 const interval=(await h.pool.query('SELECT extract(epoch FROM(e.lease_until-a.claim_issued_at))*1000 ms FROM genesis_runtime_events e JOIN genesis_continuous_attempts a ON a.cycle_id=e.cycle_id')).rows[0];
 assert.equal(Number(interval.ms),250);
 await assert.rejects(h.check({...fresh,cycleId:old.cycle_id,lease:old.lease}),/OWNERSHIP_MISMATCH|LEASE_EXPIRED_BEFORE_ADMISSION/);
 assert.equal((await h.pool.query('SELECT count(*) n FROM genesis_decisions')).rows[0].n,'7');
},limits));

test('Short lease: expiry before preparation refuses stale worker, no decision',{skip},()=>continuousFixture(async(h,s)=>{
 await h.enqueue(manual(s),'fixture-operator');const f=await h.claim(s.id);assert.ok(f);
 await h.pool.query('SELECT pg_sleep(0.27)');await assert.rejects(h.check(f),/OWNERSHIP_MISMATCH|LEASE_EXPIRED_BEFORE_ADMISSION/);
 assert.equal((await h.pool.query('SELECT count(*) n FROM genesis_decisions')).rows[0].n,'7');
},limits));

test('Short lease: concurrent claims give exactly one owner',{skip},()=>continuousFixture(async(h,s)=>{
 await h.enqueue(manual(s),'fixture-operator');const claims=await Promise.all([h.claim(s.id),h.claim(s.id)]);
 assert.equal(claims.filter(Boolean).length,1);assert.equal((await h.pool.query('SELECT count(*) n FROM genesis_continuous_attempts')).rows[0].n,'1');
},limits));

for(const margin of [1,0,-1])test('Short lease: application honors database lease result with '+margin+'ms remaining',{skip},()=>continuousFixture(async(h,s)=>{
 await h.enqueue(manual(s),'fixture-operator');const f=await h.claim(s.id);assert.ok(f);
 // Capture actual compatible rows, then isolate the existing process-clock predicate.
 // This fake reader is NOT a database integration or permission test.
 const base=(await h.pool.query('SELECT state,revision,lease FROM genesis_organisms')).rows[0];
 const ext=(await h.pool.query('SELECT record,revision FROM genesis_life_state')).rows[0];
 const scope=(await h.pool.query('SELECT * FROM genesis_continuous_scopes')).rows[0];
 const attempt=(await h.pool.query('SELECT * FROM genesis_continuous_attempts')).rows[0];
 const event=(await h.pool.query('SELECT * FROM genesis_runtime_events')).rows[0];
 const at=Date.now();event.lease_until=new Date(at+margin);event.lease_current=margin>0;
 const reader={query:async(sql:string)=>({rows:sql.includes('FROM genesis_continuous_scopes')?[scope]:sql.includes('FROM genesis_schedule')?[{enabled:false}]:sql.includes('FROM genesis_decisions')?[{n:'7',m:'7'}]:sql.includes('FROM genesis_continuous_attempts')?[attempt]:sql.includes('FROM genesis_runtime_events')?[event]:[]})} as unknown as pg.PoolClient;
 const original=Date.now;Date.now=()=>at;
 try{if(margin>0)assert.equal((await assertContinuousClaim(reader,f,base,ext)).scope.id,s.id);else await assert.rejects(assertContinuousClaim(reader,f,base,ext),/LEASE_EXPIRED_BEFORE_ADMISSION/);}finally{Date.now=original;}
},limits));

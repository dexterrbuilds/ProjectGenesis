/** Fresh-process, disposable real-time evidence. No clock seam, retries or canonical credentials. */
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {existsSync,writeFileSync} from 'node:fs';
import assert from 'node:assert/strict';
import type pg from 'pg';
import {continuousFixture,manual} from '../tests/support/continuous-fixture.ts';
import {ContinuousController,SimulatedCrash} from '../server/continuous.ts';
import {ContinuousWorker} from '../server/continuous-worker.ts';
import {ProductFallback} from '../core/v2/planner.ts';
if(process.env.DATABASE_URL||!process.env.TEST_DATABASE_URL||new URL(process.env.TEST_DATABASE_URL).pathname!=='/genesis_runtime_v1_test')throw Error('DISPOSABLE_ONLY');
if(process.argv[2]==='--trial'){
 await continuousFixture(async(h,s)=>{
  const observations:{phase:string;elapsedMs:number;durationMs?:number;databaseTime?:string;deadline?:string;detail?:unknown}[]=[];let origin=performance.now();
  const query=(c:Pick<pg.PoolClient,'query'>)=>(async(sql:string,args?:unknown[])=>{const start=performance.now();try{const r=await c.query(sql,args);if(sql.startsWith('WITH t AS MATERIALIZED'))observations.push({phase:'claim_sample',elapsedMs:performance.now()-origin,databaseTime:r.rows[0].issued_at,deadline:r.rows[0].deadline});if(sql.startsWith('INSERT INTO genesis_decisions')||sql==='COMMIT')observations.push({phase:sql==='COMMIT'?'transaction_ack_observed':'admission_insert_returned',elapsedMs:performance.now()-origin,durationMs:performance.now()-start});return r;}catch(e){const error=e as {message?:string;detail?:string};if(error.message==='LEASE_EXPIRED_BEFORE_ADMISSION')observations.push({phase:'admission_refused',elapsedMs:performance.now()-origin,detail:error.detail?JSON.parse(error.detail):null});throw e;}}) as pg.PoolClient['query'];
  const proxy={query:query(h.pool),connect:async()=>{const c=await h.pool.connect();return {query:query(c),release:()=>c.release()};}} as pg.Pool;
  const controller=new ContinuousController(proxy),worker=new ContinuousWorker(controller,s.id,{identity:s.planner.identity,planner:new ProductFallback()},true);
  await h.enqueue(manual(s),'fixture-operator');await assert.rejects(worker.tick(undefined,async phase=>{if(phase==='before_claim')throw new SimulatedCrash('before_claim');}));
  origin=performance.now();const result=await worker.tick();const durationMs=performance.now()-origin;
  const rows=(await h.pool.query("SELECT (SELECT count(*)::int FROM genesis_decisions) decisions,(SELECT count(*)::int FROM genesis_life_events WHERE record->>'kind'='episode') episodes,(SELECT count(*)::int FROM genesis_continuous_attempts) attempts")).rows[0];
  const admission=(await h.pool.query('SELECT admitted_at::text,lease_until::text,extract(epoch FROM(lease_until-admitted_at))*1000 AS margin_ms FROM genesis_continuous_admissions')).rows[0]??null;
  const event=(await h.pool.query('SELECT status FROM genesis_runtime_events')).rows[0].status;
  assert.equal(rows.attempts,1);
  if(result.status==='COMMITTED'){assert.equal(rows.decisions,8);assert.equal(rows.episodes,1);assert.equal(event,'CONSUMED');assert.ok(admission);}
  else{assert.equal(result.status,'CLOSED_WITH_ERROR');assert.equal(result.reason,'LEASE_EXPIRED_BEFORE_ADMISSION');assert.equal(rows.decisions,7);assert.equal(rows.episodes,0);assert.equal(admission,null);}
  console.log(JSON.stringify({status:result.status,reason:result.status==='CLOSED_WITH_ERROR'?result.reason:null,durationMs,rows,event,admission,observations}));
 },{leaseMs:250,plannerTimeoutMs:100});
}else{
 const path=process.argv[2];if(!path||existsSync(path))throw Error('UNIQUE_OUTPUT_REQUIRED');const runs=[];
 for(let n=0;n<50;n++){const {stdout}=await promisify(execFile)(process.execPath,['scripts/lease-contract-latency.ts','--trial'],{env:{PATH:process.env.PATH,TEST_DATABASE_URL:process.env.TEST_DATABASE_URL,NODE_ENV:'test'},maxBuffer:1024*1024});const run=JSON.parse(stdout);runs.push({run:n+1,...run});writeFileSync(path,JSON.stringify({fixtureOnly:true,canonical:false,freshProcesses:true,leaseMs:250,plannerTimeoutMs:100,retries:0,runs},null,2)+'\n');console.log(n+1,run.status,run.reason??'');}
}

import test from 'node:test';
import assert from 'node:assert/strict';
import pg from 'pg';
import { WalletObserver } from '../runtime/wallet-observer.ts';
import { once } from 'node:events';
import { migrate } from '../runtime/migrate.ts';
import { LifeStore } from '../server/store.ts';
import { GenesisService } from '../runtime/service.ts';
import { LifeScheduler } from '../runtime/scheduler.ts';
import { readConfig } from '../runtime/config.ts';
import { CElegansBrain } from '../core/brain/celegans.ts';
import { LocalPlanner } from '../core/planner.ts';
import { liveCycle } from '../core/life.ts';
import { handleRequest } from '../runtime/http.ts';
const databaseUrl=process.env.TEST_DATABASE_URL;
test('real Postgres: atomic state, restart, leases, authenticated API and browser-independent schedule', {skip:!databaseUrl}, async () => {
  const admin=new pg.Pool({connectionString:databaseUrl}); const schema='genesis_test_'+crypto.randomUUID().replaceAll('-','');
  await admin.query(`CREATE SCHEMA ${schema}`);
  const pool=new pg.Pool({connectionString:databaseUrl,options:`-c search_path=${schema}`,max:5});
  let scheduler:LifeScheduler|undefined;
  try {
    await migrate(pool); const store=new LifeStore(pool); await store.initialize(10000); const initial=await store.read();
    assert.equal((await store.schedule()).enabled,false,'a fresh life waits for the operator to start its schedule');
    let reads=0, failed=false;
    const reader={async readAccount(){reads++;if(failed)throw new Error('test RPC failure');return {address:'test-wallet',observedAt:new Date().toISOString(),balances:[]};}};
    const observer=new WalletObserver(pool,reader,'test-wallet');
    await Promise.all([observer.refresh(),observer.refresh()]);assert.equal(reads,1);
    const observation=await observer.get();assert(observation?.account);
    const restartedObserver=new WalletObserver(pool,reader,'test-wallet');
    assert.deepEqual(await restartedObserver.get(),observation);await restartedObserver.refresh();assert.equal(reads,1);
    await pool.query("UPDATE genesis_external_observations SET record=jsonb_set(record,'{checkedAt}',to_jsonb((NOW()-INTERVAL '2 minutes')::text))");
    failed=true;await restartedObserver.refresh();const stale=await restartedObserver.get();
    assert.deepEqual(stale?.account,observation.account);assert(stale?.error);assert.deepEqual((await store.read()).organism.wallet,initial.organism.wallet);

    const claims=await Promise.all([store.claim('one'),store.claim('two')]); assert.equal(claims.filter(Boolean).length,1);
    const index=claims.findIndex(Boolean), token=index===0?'one':'two', claim=claims[index]!;
    const result=await liveCycle(claim.organism,new CElegansBrain(),new LocalPlanner(),{internet:false,id:'cycle-00000001'});
    await store.pause(true); await store.commit(token,claim.revision,result.organism,result.decision);
    assert.equal((await store.read()).organism.paused,true,'pause during a cycle must survive commit');
    const reopened=new LifeStore(pool); assert.equal((await reopened.read()).organism.id,initial.organism.id); assert.deepEqual((await reopened.read()).organism.brain,result.organism.brain);
    assert.equal((await store.history()).length,1); assert.equal((await pool.query('SELECT count(*) FROM genesis_memories')).rows[0].count,'1');
    await store.pause(false); const next=await store.claim('next'); assert(next);
    const second=await liveCycle(next.organism,new CElegansBrain(),new LocalPlanner(),{internet:false,id:'cycle-00000002'});
    await assert.rejects(store.commit('wrong',next.revision,second.organism,second.decision),/lease/);
    assert.equal((await store.history()).length,1); await store.release('next');
    const config=readConfig({DATABASE_URL:databaseUrl!,GENESIS_OPERATOR_TOKEN:'integration-test-secret-123456',GENESIS_AUTONOMY_ENABLED:'true',GENESIS_INTERVAL_MS:'1000'});
    const service=new GenesisService(store,config,()=>new CElegansBrain(),new LocalPlanner());
    assert.equal((await handleRequest(new Request('http://runtime/api/cycle',{method:'POST',body:'{}'}),service)).status,401);
    const post=(path:string,body:unknown,origin?:string)=>handleRequest(new Request('http://runtime'+path,{method:'POST',headers:{authorization:'Bearer '+config.operatorToken,...(origin?{origin}:{})},body:JSON.stringify(body)}),service);
    assert.equal((await post('/api/control',{enabled:true},'https://evil.example')).status,403);
    assert.equal((await post('/api/control',{enabled:true,remainingCycles:101})).status,400);
    assert.equal((await post('/api/cycle',{requestId:'cycle-00000001'})).status,200); assert.equal((await store.read()).organism.cycles,1);
    await store.control({enabled:true,remainingCycles:2}); scheduler=new LifeScheduler(service,20); scheduler.start();
    for(let i=0;i<80&&(await store.read()).organism.cycles<3;i++) await new Promise(r=>setTimeout(r,50));
    await scheduler.stop(); assert.equal((await store.read()).organism.cycles,3); assert.equal((await store.schedule()).enabled,false);
    // A new worker instance resumes the persisted schedule without any frontend.
    await store.control({enabled:true,remainingCycles:1}); scheduler=new LifeScheduler(new GenesisService(new LifeStore(pool),config,()=>new CElegansBrain(),new LocalPlanner()),20); scheduler.start();
    for(let i=0;i<60&&(await store.read()).organism.cycles<4;i++) await new Promise(r=>setTimeout(r,50));
    await scheduler.stop(); assert.equal((await store.read()).organism.cycles,4); assert.equal((await store.schedule()).remaining_cycles,0);
    assert.equal((await store.history(3)).length,2);
    assert.equal(await store.claim('budget',false,1),null,'daily cap is enforced before planner calls');
  } finally { await scheduler?.stop(); await pool.end(); await admin.query(`DROP SCHEMA ${schema} CASCADE`); await admin.end(); }
});

test('standalone runtime process restart preserves paused life and resumes a browser-free bounded run', {skip:!databaseUrl,timeout:30000}, async () => {
  const {spawn}=await import('node:child_process');
  const {createServer}=await import('node:net');
  const admin=new pg.Pool({connectionString:databaseUrl});
  const schema='genesis_process_'+crypto.randomUUID().replaceAll('-','');
  await admin.query(`CREATE SCHEMA ${schema}`);
  const socket=createServer(); socket.listen(0,'127.0.0.1'); await once(socket,'listening');
  const port=(socket.address() as import('node:net').AddressInfo).port; await new Promise<void>(r=>socket.close(()=>r()));
  const origin=`http://127.0.0.1:${port}`, token='process-test-operator-123456789';
  let child: ReturnType<typeof spawn> | undefined;
  const start=async()=>{
    child=spawn(process.execPath,['runtime/main.ts'],{env:{...process.env,DATABASE_URL:databaseUrl!,PGOPTIONS:`-c search_path=${schema}`,PORT:String(port),HOST:'127.0.0.1',GENESIS_OPERATOR_TOKEN:token,GENESIS_PLANNER_MODE:'local',GENESIS_INTERNET:'false',GENESIS_AUTONOMY_ENABLED:'true',GENESIS_INTERVAL_MS:'1000'},stdio:['ignore','pipe','pipe']});
    let logs=''; child.stdout!.on('data',x=>logs+=x); child.stderr!.on('data',x=>logs+=x);
    for(let i=0;i<100;i++) {
      if(child.exitCode!==null) throw new Error('Runtime exited: '+logs);
      try {if((await fetch(origin+'/healthz')).ok) return;} catch {}
      await new Promise(r=>setTimeout(r,50));
    }
    throw new Error('Runtime did not start: '+logs);
  };
  const stop=async()=>{if(child&&child.exitCode===null){const exited=once(child,'exit');child.kill('SIGTERM');await exited;} child=undefined;};
  const state=async()=>{const r=await fetch(origin+'/api/state');assert.equal(r.status,200);return r.json();};
  const control=async(body:unknown)=>{const r=await fetch(origin+'/api/control',{method:'POST',headers:{authorization:'Bearer '+token,'content-type':'application/json'},body:JSON.stringify(body)});assert.equal(r.status,200);};
  try {
    await start(); const original=await state();
    await control({enabled:true,remainingCycles:2,paused:true});
    await stop(); await start(); const paused=await state();
    assert.equal(paused.organism.id,original.organism.id); assert.equal(paused.organism.bornAt,original.organism.bornAt);
    assert.equal(paused.organism.paused,true); assert.equal(paused.organism.cycles,0); assert.equal(paused.schedule.remaining_cycles,2);
    await control({paused:false});
    let completed=await state();
    for(let i=0;i<100&&completed.organism.cycles<2;i++){await new Promise(r=>setTimeout(r,100));completed=await state();}
    assert.equal(completed.organism.cycles,2);assert.equal(completed.schedule.enabled,false);
    await stop(); await start(); const restored=await state();
    assert.equal(restored.organism.paused,false);assert.deepEqual(restored.organism.brain,completed.organism.brain);
    assert.deepEqual(restored.organism.wallet,completed.organism.wallet);assert.equal(restored.organism.cycles,2);
    assert.equal(restored.schedule.remaining_cycles,0);
  } finally {await stop();await admin.query(`DROP SCHEMA ${schema} CASCADE`);await admin.end();}
});

import test from 'node:test';
import assert from 'node:assert/strict';
import pg from 'pg';
import {readFileSync,existsSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import {createServer} from 'node:net';
import {migrate} from '../runtime/migrate.ts';
import {migrateRuntimeV1,ORIGINAL_TABLES} from '../runtime/migrate-v1.ts';
import {LifeStore} from '../server/store.ts';
import {LifeExtensionStore} from '../server/life-store-v1.ts';
import {GenesisService} from '../runtime/service.ts';
import {LifeScheduler} from '../runtime/scheduler.ts';
import {readConfig} from '../runtime/config.ts';
import {handleRequest} from '../runtime/http.ts';
import {createOrganism} from '../core/life.ts';
import {CElegansBrain} from '../core/brain/celegans.ts';
import {ProductFallback} from '../core/v2/planner.ts';
import {SavedObservationAdapter} from '../core/v2/biology.ts';
import {compileContext} from '../core/v2/context.ts';
import {CLOSED_PERMISSIONS,digest} from '../core/v2/identity.ts';
import {evaluatePolicy} from '../core/v2/policy.ts';
const url=process.env.TEST_DATABASE_URL;
if(url){assert.equal(new URL(url).pathname,'/genesis_runtime_v1_test','Only explicitly dedicated test DB accepted');if(process.env.DATABASE_URL)assert.notEqual(new URL(url).pathname,new URL(process.env.DATABASE_URL).pathname);}
const skip=!url;
async function audit(pool:pg.Pool){const names=(await pool.query("SELECT tablename FROM pg_tables WHERE schemaname=current_schema() AND tablename LIKE 'genesis_%' ORDER BY tablename")).rows.map(r=>r.tablename);const rows:Record<string,unknown[]>={};for(const n of names)rows[n]=(await pool.query(`SELECT row_to_json(t) AS row FROM "${n}" t ORDER BY row_to_json(t)::text`)).rows.map(r=>r.row);return rows;}
const hash=(x:unknown)=>createHash('sha256').update(JSON.stringify(x)).digest('hex');
async function fixture(run:(pool:pg.Pool,schema:string,before:Record<string,unknown[]>)=>Promise<void>,empty=false){
 const admin=new pg.Pool({connectionString:url});const schema='runtime_v1_test_'+crypto.randomUUID().replaceAll('-','');await admin.query(`CREATE SCHEMA ${schema}`);
 const pool=new pg.Pool({connectionString:url,options:`-c search_path=${schema}`,max:5});
 try{
  await migrate(pool);
  if(!empty){
   const file='outputs/runtime-v1/PRIVATE_BASELINE_BACKUP.json';
   if(existsSync(file)){
    const backup=JSON.parse(readFileSync(file,'utf8'));assert.equal(hash(backup.rows),backup.sha256);assert.equal(backup.sha256,'3377c9dddbe2abf89ed9a820a6aabbc1da951cac7bfc1823471c5aac043ea312');
    await pool.query('TRUNCATE genesis_migrations');
    for(const table of ['genesis_organisms','genesis_decisions','genesis_memories','genesis_ledger','genesis_projects','genesis_milestones','genesis_schedule','genesis_external_observations','genesis_migrations'])for(const row of backup.rows[table]){
     const keys=Object.keys(row);assert(keys.every(x=>/^[a-z_]+$/.test(x)));await pool.query(`INSERT INTO ${table} (${keys.join(',')}) VALUES (${keys.map((_,i)=>'$'+(i+1)).join(',')})`,keys.map(k=>row[k]));
    }
    assert.equal(hash(await audit(pool)),backup.sha256,'Private backup restoration reproduces original row digest');
   }else{
    // CI-only synthetic fixture: no canonical state, neural advancement or provider call.
    const o=createOrganism('2026-09-14T00:00:00Z','fixture-genesis');o.brain=new CElegansBrain().snapshot();
    await pool.query('INSERT INTO genesis_organisms(id,state) VALUES($1,$2)',['genesis',o]);await pool.query("INSERT INTO genesis_schedule(id,enabled) VALUES('genesis',false)");
   }
  }
  await run(pool,schema,await audit(pool));
 }finally{await pool.end();await admin.query(`DROP SCHEMA ${schema} CASCADE`);await admin.end();}
}
async function upgrade(pool:pg.Pool){const {organism:o}=await new LifeStore(pool).read();return migrateRuntimeV1(pool,{organismId:o.id,bornAt:o.bornAt,cycles:o.cycles,baselineDigest:hash(Object.fromEntries(Object.entries(await audit(pool)).filter(([k])=>ORIGINAL_TABLES.includes(k))))});}
test('V1 Postgres: restored backup, additive migration, all original rows preserved and idempotent',{skip},async()=>fixture(async(pool,_schema,before)=>{
 await upgrade(pool);const after=await audit(pool);
 for(const [table,rows] of Object.entries(before))assert.deepEqual(table==='genesis_migrations'?after[table].filter(x=>(x as {version:string}).version!=='003'):after[table],rows,table);
 assert.equal(after.genesis_life_state.length,1);assert.equal(after.genesis_life_events.length,1);assert.equal(after.genesis_action_intents.length,0);
 assert.equal((await new LifeExtensionStore(pool).read()).executionLock,'CLOSED');assert.deepEqual(await upgrade(pool),{applied:false});assert.deepEqual(await audit(pool),after);
 if(existsSync('outputs/runtime-v1/PRIVATE_BASELINE_BACKUP.json'))writeFileSync('outputs/runtime-v1/MIGRATION_DRY_RUN.json',JSON.stringify({passed:true,migrationSqlSha256:createHash('sha256').update(readFileSync('runtime/migrations/003_runtime_v1.sql')).digest('hex'),migrationCodeSha256:createHash('sha256').update(readFileSync('runtime/migrate-v1.ts')).digest('hex'),backupRestorationVerified:true,beforeDigest:hash(before),afterDigest:hash(after),originalRowsPreserved:true,newRows:{lifeState:1,administrativeEvent:1,migration:1,actionIntents:0}},null,2)+'\n');
}));
test('V1 Postgres: empty/wrong identity and active schedule refuse migration',{skip},async()=>{
 await fixture(async pool=>{await assert.rejects(migrateRuntimeV1(pool,{organismId:'missing',bornAt:'unknown',cycles:7}));},true);
 await fixture(async(pool,_s,before)=>{await assert.rejects(migrateRuntimeV1(pool,{organismId:'wrong',bornAt:'unknown',cycles:7}));assert.deepEqual(await audit(pool),before);await pool.query("UPDATE genesis_schedule SET enabled=true WHERE id='genesis'");await assert.rejects(upgrade(pool),/Disabled/);});
});
test('V1 Postgres: old writers and marked writers fenced while closed',{skip},async()=>fixture(async pool=>{
 await upgrade(pool);const before=await audit(pool);
 await assert.rejects(pool.query("UPDATE genesis_organisms SET state=state WHERE id='genesis'"),/locked|incompatible/);
 await assert.rejects(new LifeStore(pool).initialize(10000),/locked|incompatible/);
 const c=await pool.connect();try{await c.query('BEGIN');await c.query("SELECT set_config('genesis.writer_version','runtime-v1',true)");await assert.rejects(c.query("UPDATE genesis_schedule SET enabled=true WHERE id='genesis'"),/locked/);await c.query('ROLLBACK');}finally{c.release();}
 assert.deepEqual(await audit(pool),before);
}));
test('V1 Postgres: manual, scheduled, direct service and worker ticks preserve dormant database',{skip},async()=>fixture(async pool=>{
 await upgrade(pool);const config=readConfig({DATABASE_URL:url!,GENESIS_OPERATOR_TOKEN:'isolated-secret-at-least-24-chars',GENESIS_AUTONOMY_ENABLED:'true'});const service=new GenesisService(new LifeStore(pool),config);const before=await audit(pool);
 for(const automatic of [false,true])await assert.rejects(service.advance('no-cycle',undefined,automatic),/EXECUTION_LOCK_CLOSED/);
 const scheduler=new LifeScheduler(service);await scheduler.tick();
 for(const route of ['/api/cycle','/api/control']){const r=await handleRequest(new Request('http://runtime'+route,{method:'POST',headers:{authorization:'Bearer '+config.operatorToken},body:JSON.stringify({enabled:true})}),service);assert.equal(r.status,423);}
 assert.equal((await handleRequest(new Request('http://runtime/api/cycle',{method:'POST'}),service)).status,401);
 assert.deepEqual(await audit(pool),before);
}));
test('V1 Postgres: direct runtime public responses are redacted, reads do not write',{skip},async()=>fixture(async pool=>{
 await upgrade(pool);const service=new GenesisService(new LifeStore(pool),readConfig({DATABASE_URL:url!,GENESIS_OPERATOR_TOKEN:'isolated-secret-at-least-24-chars'}));const before=await audit(pool);
 const r=await handleRequest(new Request('http://runtime/api/state'),service);assert.equal(r.status,200);const state=await r.json();assert.equal(state.executionLock,'CLOSED');assert(!('organism'in state));assert(!('memory'in state));assert(!('approvals'in state));assert(!('businesses'in state));assert.equal(state.onchain.balance,null);
 const h=await handleRequest(new Request('http://runtime/api/history'),service);const history=await h.json();for(const d of history.decisions){assert(!('plan'in d));assert(!('outcome'in d));assert(!('event'in d));assert.equal(d.schemaVersion,1);}
 assert.deepEqual(await audit(pool),before);
}));
test('V1 Postgres: durable intent idempotency collision and transactional concurrency',{skip},async()=>fixture(async pool=>{
 await upgrade(pool);const store=new LifeExtensionStore(pool);const life=await store.read();const o=(await new LifeStore(pool).read()).organism;const brain=new SavedObservationAdapter(o.id);const context=compileContext(o,life,brain.accept({id:'test',kind:'digital-event',source:'test',observedAt:new Date().toISOString()}),CLOSED_PERMISSIONS);const proposal=await new ProductFallback().propose(context);const intent={id:'draft',organismId:o.id,payloadHash:digest(proposal),proposal,policy:evaluatePolicy(proposal,context,true,life.revision),status:'proposed' as const,attempts:0,reservedMicros:0,receipt:null,approval:null};
 const results=await Promise.allSettled([store.savePendingIntent(intent),store.savePendingIntent(intent)]);assert.equal(results.filter(x=>x.status==='fulfilled').length,1);assert.equal((await pool.query('SELECT count(*) FROM genesis_action_intents')).rows[0].count,'1');
 await assert.rejects(store.savePendingIntent({...intent,id:'bad',payloadHash:'0'.repeat(64)}));await assert.rejects(pool.query('DELETE FROM genesis_life_events'),/Append-only/);
 const moved=await store.recordIntentTransition('draft',0,'denied',new Date().toISOString());assert.equal(moved.status,'denied');
 await assert.rejects(store.recordIntentTransition('draft',0,'denied',new Date().toISOString()),/stale/);
 await assert.rejects(store.recordIntentTransition('draft',1,'proposed',new Date().toISOString()),/Invalid/);
 assert.deepEqual(await new LifeExtensionStore(pool).read(),life);
}));
test('V1 standalone process boots/restarts read-only; environment cannot awaken it',{skip,timeout:30000},async()=>{
 const {deploymentFixture}=await import('./support/deployment-fixture.ts');const {planInstall,applyInstall}=await import('../runtime/deployment/install.ts');
 await deploymentFixture(async(pool,fixtureUrl,schema,roles)=>{
 const o=(await pool.query('SELECT state FROM genesis_organisms')).rows[0].state;const plan=await planInstall(pool,fixtureUrl,o.id,o.bornAt,roles);await applyInstall(pool,fixtureUrl,plan,'INSTALL_REVIEWED_PLAN:'+plan.hash);
 const before=await audit(pool);const sock=createServer();sock.listen(0,'127.0.0.1');await once(sock,'listening');const port=(sock.address() as {port:number}).port;await new Promise<void>(r=>sock.close(()=>r()));
 for(let i=0;i<2;i++){
 const child=spawn(process.execPath,['runtime/main.ts'],{env:{NODE_ENV:'test',PATH:process.env.PATH,DATABASE_URL:fixtureUrl,GENESIS_DB_SCHEMA:schema,GENESIS_DB_ROLE:roles.reader,GENESIS_RUNTIME_MODE:'dormant',GENESIS_EXPECTED_ORGANISM_ID:o.id,GENESIS_EXPECTED_BIRTH:o.bornAt,PORT:String(port),HOST:'127.0.0.1'},stdio:['ignore','pipe','pipe']});let logs='';child.stdout?.on('data',x=>logs+=x);child.stderr?.on('data',x=>logs+=x);
 try{let ready=false;for(let n=0;n<100;n++){if(child.exitCode!==null)throw Error(logs);try{const r=await fetch(`http://127.0.0.1:${port}/readiness`);if(r.ok){ready=true;break;}}catch{}await new Promise(r=>setTimeout(r,50));}assert(ready,logs);const r=await fetch(`http://127.0.0.1:${port}/api/state`);assert.equal((await r.json()).executionLock,'CLOSED');assert.equal((await fetch(`http://127.0.0.1:${port}/api/cycle`,{method:'POST'})).status,405);}
 finally{if(child.exitCode===null){const exited=once(child,'exit');child.kill('SIGTERM');await exited;}}
 }
 assert.deepEqual(await audit(pool),before);
 });
});

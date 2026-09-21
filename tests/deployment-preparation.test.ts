import test from 'node:test';
import assert from 'node:assert/strict';
import pg from 'pg';
import {readFileSync} from 'node:fs';
import {deploymentFixture} from './support/deployment-fixture.ts';
import {planInstall,applyInstall} from '../runtime/deployment/install.ts';
import {rows,hashObject} from '../runtime/deployment/schema.ts';
import {inspectReadiness} from '../runtime/deployment/readiness.ts';
import {poolConfig,dormantMode} from '../runtime/deployment/config.ts';
import {logRecord} from '../runtime/deployment/log.ts';
import {GenesisService} from '../runtime/service.ts';
import {LifeStore} from '../server/store.ts';
import {observationServer,stopObservation} from '../runtime/deployment/http-server.ts';
import type {RuntimeConfig} from '../runtime/config.ts';
const o=JSON.parse(readFileSync('tests/fixtures/genesis-dormant-sanitized.json','utf8'));
const expected={organismId:o.id,bornAt:o.bornAt};
const config:RuntimeConfig={databaseUrl:'fixture',operatorToken:'private-canary',port:3001,host:'127.0.0.1',intervalMs:30000,maxDailyCycles:1,autonomous:false,internet:false,startingCents:0,plannerMode:'local',allowedOrigins:[]};
async function installed<T>(fn:(pool:pg.Pool,url:string,schema:string,roles:Parameters<Parameters<typeof deploymentFixture>[0]>[3])=>Promise<T>){return deploymentFixture(async(pool,url,schema,roles)=>{const p=await planInstall(pool,url,o.id,o.bornAt,roles);await applyInstall(pool,url,p,'INSTALL_REVIEWED_PLAN:'+p.hash);return fn(pool,url,schema,roles);});}
async function snapshot(pool:pg.Pool){const c=await pool.connect();try{return await rows(c);}finally{c.release();}}
test('deployment: explicit dormant mode; absence, unknown and unsafe flags refused',()=>{
 const env={GENESIS_RUNTIME_MODE:'dormant',GENESIS_EXPECTED_ORGANISM_ID:o.id,GENESIS_EXPECTED_BIRTH:o.bornAt};assert.deepEqual(dormantMode(env),expected);
 for(const x of [{...env,GENESIS_RUNTIME_MODE:undefined},{...env,GENESIS_RUNTIME_MODE:'live'},{...env,GENESIS_WORKER_ENABLED:'true'},{...env,OPENAI_API_KEY:'secret'}])assert.throws(()=>dormantMode(x));
});
test('deployment: TLS certificate verification, pool bounds and no SSL URL override',()=>{
 const prod={NODE_ENV:'production',GENESIS_DB_TLS:'verify-full'};const c=poolConfig('postgresql://user:canary@db.invalid/genesis','runtime',prod);assert.equal((c.ssl as {rejectUnauthorized:boolean}).rejectUnauthorized,true);assert.equal(c.max,4);
 assert.throws(()=>poolConfig('postgresql://db.invalid/genesis?sslmode=no-verify','runtime',prod));assert.throws(()=>poolConfig('postgresql://db.invalid/genesis','runtime',{NODE_ENV:'production'}));assert.throws(()=>poolConfig('postgresql://db.invalid/genesis','runtime',{...prod,GENESIS_DB_POOL_MAX:'10000'}));assert.throws(()=>poolConfig('postgresql://127.0.0.1/canonical','runtime',{}));
});
test('deployment: safe structured logs have no free-form error/context channel',()=>{const x=JSON.parse(logRecord('runtime','REFUSED','credential-canary'));assert.deepEqual(Object.keys(x).sort(),['at','service','status']);assert.ok(!JSON.stringify(x).includes('credential'));});
test('deployment: plan is read-only and exact additive install preserves original rows',async()=>deploymentFixture(async(pool,url,schema,roles)=>{
 const before=await snapshot(pool),p=await planInstall(pool,url,o.id,o.bornAt,roles);assert.deepEqual(await snapshot(pool),before);await applyInstall(pool,url,p,'INSTALL_REVIEWED_PLAN:'+p.hash);
 const after=await snapshot(pool);for(const [k,v] of Object.entries(before))assert.deepEqual(after[k],v);assert.equal(after.genesis_execution_grants.length,0);assert.equal(after.genesis_continuous_scopes.length,0);assert.equal(after.genesis_provider_attempts.length,0);assert.equal(after.genesis_provider_admissions.length,0);assert.equal(after.genesis_operator_actors.length,0);assert.equal((await inspectReadiness(pool,expected)).ready,true);
 await assert.rejects(applyInstall(pool,url,p,'INSTALL_REVIEWED_PLAN:'+p.hash));
}));
test('deployment: changed acknowledgement, target, SQL hash and row plan refuse without install',async()=>deploymentFixture(async(pool,url,schema,roles)=>{
 const p=await planInstall(pool,url,o.id,o.bornAt,roles),before=await snapshot(pool);
 await assert.rejects(applyInstall(pool,url,p,'yes'));await assert.rejects(applyInstall(pool,url.replace('127.0.0.1','localhost'),p,'INSTALL_REVIEWED_PLAN:'+p.hash));
 for(const delta of [{rowHash:'a'.repeat(64)},{sqlHashes:{}},{runtimeHash:'old-runtime'}]){const {hash:discard,...u}=p;void discard;const n={...u,...delta};await assert.rejects(applyInstall(pool,url,{...n,hash:hashObject(n)},'INSTALL_REVIEWED_PLAN:'+hashObject(n)));}
 assert.deepEqual(await snapshot(pool),before);
}));
test('deployment: unknown schema refuses plan and weak role refuses apply',async()=>deploymentFixture(async(pool,url,schema,roles)=>{
 await pool.query('CREATE TABLE unexpected(x text)');await assert.rejects(planInstall(pool,url,o.id,o.bornAt,roles));await pool.query('DROP TABLE unexpected');const p=await planInstall(pool,url,o.id,o.bornAt,roles);await pool.query(`GRANT CREATE ON SCHEMA ${schema} TO ${roles.worker}`);await assert.rejects(applyInstall(pool,url,p,'INSTALL_REVIEWED_PLAN:'+p.hash));assert.equal((await pool.query("SELECT to_regclass('genesis_execution_grants') r")).rows[0].r,null);
}));
test('deployment: readiness rejects code mismatch, missing schema, wrong identity, open execution',async()=>installed(async(pool)=>{
 assert.equal((await inspectReadiness(pool,{...expected,organismId:'wrong'})).ready,false);
 await pool.query('ALTER TABLE genesis_deployment_release DISABLE TRIGGER deployment_release_immutable');await pool.query("UPDATE genesis_deployment_release SET runtime_hash=repeat('a',64)");await pool.query('ALTER TABLE genesis_deployment_release ENABLE TRIGGER deployment_release_immutable');assert.equal((await inspectReadiness(pool,expected)).ready,false);
}));
test('deployment: role profile denies authority/schema/history operations independently of model',async()=>installed(async(pool,url,schema,roles)=>{
 for(const role of Object.values(roles)){
 const p=new pg.Pool({connectionString:url,options:`-c search_path=${schema} -c role=${role}`});try{
 await assert.rejects(p.query('CREATE TABLE injection(x text)'));
 await assert.rejects(p.query("UPDATE genesis_decisions SET record='{}'"));await assert.rejects(p.query('ALTER TABLE genesis_decisions DISABLE TRIGGER ALL'));
 if(role===roles.observer){await p.query('SELECT * FROM genesis_public_identity');await assert.rejects(p.query('SELECT * FROM genesis_memories'));}
 if(role===roles.reader){await p.query('SELECT * FROM genesis_memories');await assert.rejects(p.query("UPDATE genesis_organisms SET phase='idle'"));assert.equal((await inspectReadiness(p,expected)).ready,true);}
 if(role===roles.worker){for(const sql of ["INSERT INTO genesis_operator_actors(id,enabled,capabilities) VALUES('bad',true,'{}')","UPDATE genesis_schedule SET enabled=true","INSERT INTO genesis_disclosure_reviews(id) VALUES('bad')","INSERT INTO genesis_execution_grants(id) VALUES('bad')","UPDATE genesis_life_state SET record=jsonb_set(record,'{executionLock}','\"OPEN\"')","UPDATE genesis_life_state SET record=record-'executionLock'"])await assert.rejects(p.query(sql));}
 }finally{await p.end();}
 }
}));
test('deployment: dormant HTTP observer restart is read-only; no provider, claims or health mutation',async()=>installed(async(pool,url,schema,roles)=>{
 const before=await snapshot(pool);
 for(let n=0;n<2;n++){
 const reader=new pg.Pool({connectionString:url,options:`-c search_path=${schema} -c role=${roles.reader}`});const server=observationServer(new GenesisService(new LifeStore(reader),config),reader,expected);
 await new Promise<void>(r=>server.listen(0,'127.0.0.1',r));const addr=server.address() as {port:number};const base='http://127.0.0.1:'+addr.port;
 try{assert.equal((await fetch(base+'/health')).status,200);assert.equal((await fetch(base+'/readiness')).status,200);const r=await fetch(base+'/api/state',{headers:{authorization:'Bearer private-canary'}});assert.equal(r.status,200);const text=await r.text();for(const secret of ['private-canary','credential','operatorEvidence','workingContext'])assert.ok(!text.includes(secret));assert.equal((await fetch(base+'/api/cycle',{method:'POST'})).status,405);}finally{await stopObservation(server,reader);}
 }
 assert.deepEqual(await snapshot(pool),before);
}));
test('deployment: actual pg_dump restore preserves all rows/schema and creates no authority',async()=>installed(async(pool,url,schema)=>{
 const {restoreFixture}=await import('./support/deployment-restore.ts');const before=await snapshot(pool),r=await restoreFixture(pool,url,schema);assert.equal(r.decisions,7);assert.equal(r.attempts,0);assert.equal(r.receipts,0);assert.deepEqual(await snapshot(pool),before);
}));
test('deployment: old/uninstalled schema cannot serve public state; liveness survives DB failure',async()=>deploymentFixture(async(pool)=>{
 assert.equal((await inspectReadiness(pool,expected)).ready,false);
 const server=observationServer(new GenesisService(new LifeStore(pool),config),pool,expected);await new Promise<void>(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+(server.address() as {port:number}).port;
 try{assert.equal((await fetch(base+'/health')).status,200);assert.equal((await fetch(base+'/readiness')).status,503);assert.equal((await fetch(base+'/api/state')).status,503);}finally{await new Promise<void>(r=>server.close(()=>r()));}
}));
test('deployment: DB unavailable leaves health alive and readiness sanitized',async()=>{
 const pool=new pg.Pool({connectionString:'postgresql://fixture:credential-canary@127.0.0.1:1/genesis_runtime_v1_test',connectionTimeoutMillis:100});const server=observationServer(new GenesisService(new LifeStore(pool),config),pool,expected);await new Promise<void>(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+(server.address() as {port:number}).port;
 try{assert.equal((await fetch(base+'/health')).status,200);const r=await fetch(base+'/readiness');assert.equal(r.status,503);assert.deepEqual(await r.json(),{ready:false});}finally{await stopObservation(server,pool);}
});
test('deployment: runtime process refuses missing/unknown mode before opening a DB pool',async()=>{
 const {spawnSync}=await import('node:child_process');for(const mode of [undefined,'awake']){const r=spawnSync(process.execPath,['runtime/main.ts'],{env:{NODE_ENV:'test',PATH:process.env.PATH,GENESIS_RUNTIME_MODE:mode},encoding:'utf8'});assert.equal(r.status,1);const e=JSON.parse(r.stderr);assert.equal(e.status,'REFUSED');assert.ok(!r.stderr.includes('DATABASE_URL'));}
});
test('deployment: consumer entrypoint cannot execute from worker flag alone',async()=>{
 const {spawnSync}=await import('node:child_process');const r=spawnSync(process.execPath,['runtime/deployment/consumer-cli.ts'],{env:{NODE_ENV:'test',PATH:process.env.PATH,GENESIS_WORKER_ENABLED:'true'},encoding:'utf8'});assert.equal(r.status,1);assert.equal(JSON.parse(r.stderr).status,'REFUSED');
});
test('deployment: normal-service role check refuses migration-owner credentials',async()=>installed(async pool=>{
 const {requireRole}=await import('../runtime/deployment/schema.ts');const c=await pool.connect();try{for(const role of ['reader','worker','operator'] as const)await assert.rejects(requireRole(c,role));}finally{c.release();}
}));
test('deployment: read-only service rejects column-level write grants too',async()=>installed(async(pool,url,schema,roles)=>{
 await pool.query(`GRANT UPDATE(record) ON genesis_life_state TO ${roles.reader}`);const reader=new pg.Pool({connectionString:url,options:`-c search_path=${schema} -c role=${roles.reader}`});try{assert.equal((await inspectReadiness(reader,expected,'reader')).ready,false);}finally{await reader.end();}
}));

test('deployment: continuous admission proof cannot be forged by worker or observer',async()=>installed(async(pool,_url,_schema,roles)=>{
 for(const role of [roles.worker,roles.observer]){
  const c=await pool.connect();try{await c.query(`SET ROLE ${role}`);
   await assert.rejects(c.query("INSERT INTO genesis_continuous_admissions(cycle_id,transaction_id,lease,event_id,admitted_at,lease_until) VALUES('forged',pg_current_xact_id(),'forged','forged',clock_timestamp(),clock_timestamp()+interval '1 second')"),/permission denied/);
   await assert.rejects(c.query('SELECT genesis_admit_continuous_decision()'),/permission denied/);
   await assert.rejects(c.query('CREATE TABLE clock_timestamp(x int)'),/permission denied/);
  }finally{await c.query('RESET ROLE');c.release();}
 }
}));

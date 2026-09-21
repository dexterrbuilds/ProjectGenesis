/** Local-only, real built Next observer + fresh runtime processes + disposable Postgres. */
import {spawn,type ChildProcess} from 'node:child_process';import {once} from 'node:events';import {createServer} from 'node:net';import {writeFileSync,readFileSync,existsSync} from 'node:fs';
import {deploymentFixture} from '../tests/support/deployment-fixture.ts';import {planInstall,applyInstall} from '../runtime/deployment/install.ts';import {rows,hashObject} from '../runtime/deployment/schema.ts';
async function port(){const s=createServer();s.listen(0,'127.0.0.1');await once(s,'listening');const p=(s.address() as {port:number}).port;await new Promise<void>(r=>s.close(()=>r()));return p;}
async function stop(child:ChildProcess){if(child.exitCode===null){const p=once(child,'exit');child.kill('SIGTERM');await p;}}
async function ready(child:ChildProcess,url:string){for(let n=0;n<200;n++){if(child.exitCode!==null)throw Error('CHILD_EXITED');try{if((await fetch(url)).ok)return;}catch{}await new Promise(r=>setTimeout(r,100));}throw Error('START_TIMEOUT');}
const output=process.argv[2]??'verification/deployment-preparation-pass/OBSERVER_E2E.json';if(existsSync(output))throw Error('UNIQUE_EVIDENCE_PATH_REQUIRED');
await deploymentFixture(async(pool,url,schema,roles)=>{
 const o=(await pool.query('SELECT state FROM genesis_organisms')).rows[0].state,p=await planInstall(pool,url,o.id,o.bornAt,roles);await applyInstall(pool,url,p,'INSTALL_REVIEWED_PLAN:'+p.hash);
 const c=await pool.connect();const before=hashObject(await rows(c));c.release();const runtimePort=await port(),webPort=await port();const runs=[];
 for(let i=0;i<2;i++){
 const runtime=spawn(process.execPath,['runtime/main.ts'],{env:{NODE_ENV:'test',PATH:process.env.PATH,DATABASE_URL:url,GENESIS_DB_SCHEMA:schema,GENESIS_DB_ROLE:roles.reader,GENESIS_RUNTIME_MODE:'dormant',GENESIS_EXPECTED_ORGANISM_ID:o.id,GENESIS_EXPECTED_BIRTH:o.bornAt,HOST:'127.0.0.1',PORT:String(runtimePort)},stdio:'ignore'});
 let web:ChildProcess|undefined;
 try{
 await ready(runtime,`http://127.0.0.1:${runtimePort}/readiness`);
 const clean:NodeJS.ProcessEnv={NODE_ENV:'production',PATH:process.env.PATH};for(const file of ['.env','.env.local','.env.production','.env.production.local'])if(existsSync(file))for(const m of readFileSync(file,'utf8').matchAll(/^([A-Z][A-Z0-9_]*)=/gm))clean[m[1]]='';
 web=spawn(process.execPath,['node_modules/next/dist/bin/next','start','--hostname','127.0.0.1','--port',String(webPort)],{env:{...clean,NODE_ENV:'production',PATH:process.env.PATH,NEXT_TELEMETRY_DISABLED:'1',GENESIS_PUBLIC_MODE:i===0?'dormant':'live',GENESIS_API_URL:`http://127.0.0.1:${runtimePort}`},stdio:'ignore'});
 await ready(web,`http://127.0.0.1:${webPort}/`);const page=await fetch(`http://127.0.0.1:${webPort}/`),html=await page.text();if(!html.includes('GENESIS')&&!html.includes('Genesis'))throw Error('OBSERVER_CONTENT_MISSING');
 const projection=await fetch(`http://127.0.0.1:${webPort}/api/state`);if(i===0&&projection.status!==404)throw Error('DORMANT_PROXY_GATE');if(i===1){if(projection.status!==200)throw Error('PROXY_FAILURE');const s=await projection.json();if(s.executionLock!=='CLOSED'||s.status!=='DORMANT')throw Error('FALSE_ACTIVITY');}
 await new Promise(r=>setTimeout(r,1200));const check=await pool.connect();try{if(before!==hashObject(await rows(check)))throw Error('BOOT_MUTATION');}finally{check.release();}
 runs.push({freshProcess:i+1,presentation:i===0?'dormant landing':'live observer of dormant fixture',health:(await fetch(`http://127.0.0.1:${runtimePort}/health`)).status,readiness:200,pageStatus:page.status,proxyStatus:projection.status,rowsUnchanged:true});
 }finally{if(web)await stop(web);await stop(runtime);}
 }
 writeFileSync(output,JSON.stringify({fixtureOnly:true,canonical:false,realNextProductionBuild:true,realRuntimeMain:true,leastPrivilegeReader:true,runs,noAuthority:true,noProvider:true,noWorker:true},null,2)+'\n',{flag:'wx'});
});

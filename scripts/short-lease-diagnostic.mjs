/** Isolated sanitized diagnostic. No canonical credentials, provider, or safety changes. */
import '../tests/support/short-lease-instrumentation.mjs';
import pg from 'pg';
import {writeFileSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
const {continuousFixture,manual}=await import('../tests/support/continuous-fixture.ts');
const {SimulatedCrash}=await import('../server/continuous.ts');
const scenario=process.argv[3]??'fallback';if(!['fallback','planner-timeout'].includes(scenario))throw Error('Unknown diagnostic scenario');
const out=process.argv[2];if(!out||existsSync(out))throw Error('Unique diagnostic output required');
let active=false,origin=0,stage='setup';const timeline=[];
const stamp=(name,detail={})=>{if(active)timeline.push({name,stage,elapsedMs:performance.now()-origin,...detail});};
globalThis.__genesisLeaseProbe=(name,detail)=>stamp(name,detail);
const original=pg.Client.prototype.query;
const connect=pg.Pool.prototype.connect;
pg.Pool.prototype.connect=function(...args){
 if(!active)return connect.apply(this,args);const started=performance.now();
 const done=()=>stamp('db_connection_acquired',{durationMs:performance.now()-started});
 if(typeof args.at(-1)==='function'){const cb=args.at(-1);args[args.length-1]=(...values)=>{done();cb(...values);};return connect.apply(this,args);}
 return connect.apply(this,args).then(c=>{done();return c;});
};
pg.Client.prototype.query=function(...args){
 if(!active)return original.apply(this,args);
 let sql=typeof args[0]==='string'?args[0]:args[0]?.text;const started=performance.now();
 const tag=sql?.replace(/\s+/g,' ').slice(0,200)??'unknown';
 // Return clock metadata with existing reads/writes, without an extra round-trip.
 if(typeof args[0]==='string'){
  if(/^SELECT state,revision,lease,/.test(sql))args[0]=sql.replace('SELECT ',"SELECT clock_timestamp() diagnostic_db_clock,now() diagnostic_transaction_clock,lease_until diagnostic_lease_until, ");
  else if(/^SELECT \* FROM genesis_(runtime_events|continuous_attempts|continuous_scopes) WHERE/.test(sql))args[0]=sql.replace('SELECT *', 'SELECT *,clock_timestamp() diagnostic_db_clock,now() diagnostic_transaction_clock');
  else if(sql.startsWith('UPDATE genesis_runtime_events SET status=\'CLAIMED\''))args[0]=sql+' RETURNING clock_timestamp() diagnostic_db_clock,now() diagnostic_transaction_clock,lease_until diagnostic_lease_until';
 }
 const finish=(error,result)=>{
  const clocks=[];for(const row of result?.rows??[]){const x={};for(const key of ['diagnostic_db_clock','diagnostic_transaction_clock','diagnostic_lease_until'])if(row[key]!==undefined)x[key]=row[key];if(Object.keys(x).length)clocks.push(x);}
  stamp('db_query',{tag,sqlHash:createHash('sha256').update(sql??'').digest('hex'),durationMs:performance.now()-started,processWallMs:Date.now(),rows:result?.rowCount??null,clocks,errorCode:error?.code??null});
 };
 if(typeof args.at(-1)==='function'){const cb=args.at(-1);args[args.length-1]=(error,result)=>{finish(error,result);cb(error,result);};return original.apply(this,args);}
 try{const r=original.apply(this,args);return r?.then?r.then(v=>{finish(null,v);return v;},e=>{finish(e);throw e;}):r;}catch(e){finish(e);throw e;}
};
let report;
await continuousFixture(async(h,s,w)=>{
 await h.enqueue(manual(s),'fixture-operator');
 if(scenario==='planner-timeout')w.planner.planner={propose:()=>new Promise(()=>{})};
 // Every diagnostic query below happens outside the claimed execution window.
 const inspect=async()=>({events:(await h.pool.query('SELECT status,attempts,cycle_id,lease IS NOT NULL has_lease,lease_until,reason FROM genesis_runtime_events')).rows,attempts:(await h.pool.query('SELECT status,phase,failure FROM genesis_continuous_attempts')).rows,scopes:(await h.pool.query('SELECT status FROM genesis_continuous_scopes')).rows,cycleAttempts:(await h.pool.query('SELECT status,cancelled FROM genesis_cycle_attempts')).rows,organism:(await h.pool.query('SELECT lease IS NOT NULL has_lease,phase FROM genesis_organisms')).rows,dbClock:(await h.pool.query('SELECT clock_timestamp() t')).rows[0].t});
 const initial=await inspect();origin=performance.now();active=true;
 for(const name of ['recover','claim','check','prepare','phase','commit','fail']){const fn=h[name].bind(h);h[name]=async(...args)=>{const parent=stage;stage=name;stamp(name+'_start');try{const r=await fn(...args);stamp(name+'_end');return r;}catch(e){stamp(name+'_error',{failureCategory:e.message,failedCheck:e.stack?.split('\n').slice(1,4).map(x=>x.trim())});throw e;}finally{stage=parent;}};}
 stamp('tick_start');try{await w.tick(undefined,async p=>{stamp('hook_'+p);if(p==='before_claim')throw new SimulatedCrash(p);});}catch(e){if(!(e instanceof SimulatedCrash))throw e;stamp('simulated_crash');}
 active=false;const afterCrash=await inspect();active=true;stamp('second_tick_start');const result=await w.tick(undefined,async p=>stamp('hook_'+p));stamp('closure',{status:result.status,reason:result.reason??null});
 // Observe beyond the planner deadline without consuming any claimed execution time.
 await new Promise(resolve=>setTimeout(resolve,120));active=false;
 report={scenario,fixtureOnly:true,leaseMs:250,plannerTimeoutMs:100,initial,afterCrash,result:{status:result.status,reason:result.reason??null},final:await inspect(),timeline,instrumentation:'Test-only in-memory reducer/policy probes and returned DB clocks; statement total latency includes locks/network/server work, not a pure lock-wait measurement'};
},{leaseMs:250,plannerTimeoutMs:100});
writeFileSync(out,JSON.stringify(report,null,2)+'\n',{mode:0o600});console.log(JSON.stringify(report.result));

/** Disposable deterministic local-life exercise, not a neural simulation or production benchmark. */
import assert from 'node:assert/strict';
import {continuousFixture,manual} from './continuous-fixture.ts';
import {ContinuousWorker} from '../../server/continuous-worker.ts';
import {ProductFallback} from '../../core/v2/planner.ts';
import type {LifeChange,PlannerV2} from '../../core/v2/contracts.ts';
import type {Operation} from '../../core/v2/operations.ts';
export async function longRun(){return continuousFixture(async(h,s)=>{
 const started=performance.now(),sizes:number[]=[],selection:number[]=[];let idle=0,oldArtifactRecalled=false;
 const p:PlannerV2={propose:async c=>{const v=JSON.parse(c.text),n=v.critical.identity.cycles-6;
  sizes.push(Buffer.byteLength(c.text));selection.push(c.manifest.memory?.manifest.selectedIds.length??0);
  const ops:Operation[]=[];
  if(n===1)ops.push({op:'project_create',id:'p',title:'Local note archive',summary:'Neutral fixture project'},{op:'task_create',id:'t',projectId:'p',description:'Maintain local notes',dueAt:null},{op:'artifact_create',id:'a',projectId:'p',taskId:'t',content:'ORIGINAL_LOCAL_NOTE'});
  if(n%10===0){if(n===100)oldArtifactRecalled=c.text.includes('ORIGINAL_LOCAL_NOTE');ops.push({op:'artifact_revise',id:'a',expectedVersion:n/10,content:'ORIGINAL_LOCAL_NOTE revision '+(n/10+1),reason:'Deterministic fixture revision'});}
  if(n===100)ops.push({op:'task_status',id:'t',expectedVersion:1,status:'completed',reviewAt:null,evidenceIds:[v.currentEvent.id],reason:'Fixture task complete'});
  const changes:LifeChange[]=ops.map(operation=>({kind:'operational',expectedRevision:c.manifest.stateRevision,sourceIds:[v.currentEvent.id],operation}));
  return {...await new ProductFallback().propose(c),kind:ops.length||n%10!==0?'PROPOSAL':'ABSTAIN',changes,projectId:n>1?'p':null,taskId:n>1?'t':null,...(n%10!==0?{followUp:{kind:'CONTINUATION',availableAt:new Date().toISOString(),reason:'Next local fixture part'}}:{})};
 }};
 const w=new ContinuousWorker(h,s.id,{identity:s.planner.identity,planner:p},true);
 for(let group=0;group<10;group++){
  assert.equal((await w.tick()).status,'IDLE_OR_BUDGET_BLOCKED');idle++;
  const e=manual(s,'root'+group,{kind:'MANUAL_EVENT',text:'Local fixture review',references:group?['p','t','a']:[]});await h.enqueue(e,'fixture-operator');assert.equal(await h.enqueue(e,'fixture-operator'),false);
  for(let i=0;i<10;i++){const r=await w.tick();assert.equal(r.status,'COMMITTED');if(r.status==='COMMITTED'){assert.equal(r.decision.cycle,8+group*10+i);assert.equal(r.decision.policy?.verdict,'ALLOW',JSON.stringify(r.decision.policy));assert.notEqual(r.decision.outcome.status,'failed');assert.equal(r.decision.biological.executedThisCycle,false);}}
 }
 await h.enqueue(manual(s,'over-budget'),'fixture-operator');assert.equal((await w.tick()).status,'IDLE_OR_BUDGET_BLOCKED');
 const counts=(await h.pool.query(`SELECT (SELECT count(*) FROM genesis_decisions) decisions,(SELECT count(*) FROM genesis_life_events WHERE record->>'kind'='episode') episodes,(SELECT count(*) FROM genesis_runtime_events) events,(SELECT count(*) FROM genesis_runtime_events WHERE status='CONSUMED') consumed,(SELECT count(*) FROM genesis_continuous_attempts WHERE status='COMMITTED') committed,(SELECT max((payload->>'depth')::integer) FROM genesis_runtime_events) max_depth,(SELECT count(*)-count(DISTINCT cycle) FROM genesis_decisions) duplicate_decisions,(SELECT count(*)-count(DISTINCT dedup_key) FROM genesis_runtime_events) duplicate_events,(SELECT octet_length(record::text) FROM genesis_life_state) life_bytes,(SELECT coalesce(sum(octet_length(record::text)),0) FROM genesis_life_events) archive_json_bytes,(SELECT coalesce(sum(pg_column_size(e)),0) FROM genesis_runtime_events e) event_row_bytes,(SELECT coalesce(sum(pg_column_size(d)),0) FROM genesis_decisions d) decision_row_bytes`)).rows[0];
 const state=(await h.pool.query('SELECT record FROM genesis_life_state')).rows[0].record;assert.equal(state.operational.artifacts[0].versions.length,11);assert.equal(state.operational.tasks[0].status,'completed');assert(oldArtifactRecalled);assert(Math.max(...sizes)<=12000);assert.equal(state.executionLock,'CLOSED');const resources=await h.tx(c=>h.resources(c,s));assert.equal(resources.failures,0);
 return {classification:'DISPOSABLE LOCAL FIXTURE; NOT CANONICAL; NOT A PRODUCTION THROUGHPUT BENCHMARK',cycles:100,counts,averageContextBytes:sizes.reduce((a,b)=>a+b,0)/sizes.length,maxContextBytes:Math.max(...sizes),maxSelectedMemoryItems:Math.max(...selection),artifactVersions:11,oldArtifactRecalled,idleTicks:idle,resources,wallMilliseconds:Math.round(performance.now()-started),providerCalls:0,walletActions:0,externalCommunications:0,biologicalAdvancement:false,duplicateEnqueuesRefused:10,budgetBlockedPendingEvents:1};
 },{maxCycles:100,maxCyclesPerWindow:100,maxDepth:9,maxImmediatePerRoot:10,backoffMs:10000});}

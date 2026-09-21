import test from 'node:test';
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import {activeFixture} from './support/active-fixture.ts';
import {ProductFallback} from '../core/v2/planner.ts';
import {CLOSED_PERMISSIONS,digest} from '../core/v2/identity.ts';
import {ProviderControl,type ModelGrant,type ProviderTransport} from '../server/provider-control.ts';
import {IsolatedCycle} from '../server/isolated-cycle.ts';
import {approvalMatches} from '../core/v2/policy.ts';
import type {PlannerV2,Proposal} from '../core/v2/contracts.ts';
const skip=!process.env.TEST_DATABASE_URL;
const permission={...CLOSED_PERMISSIONS,execution:true,localArtifacts:true,llm:true,maxCostMicros:50000,maxAttempts:1};
const counter={model:'fixture-model',provenance:'test-only exact mock counter; NOT a biological or live-provider calibration',count:()=>100};
const grant:ModelGrant={id:'fixture-grant',enabled:true,model:'fixture-model',pricingEvidence:'TEST ONLY — invented accounting tariff, not provider pricing',inputMicrosPerToken:1,outputMicrosPerToken:2,maxInputTokens:1000,maxOutputTokens:1200,perCallMicros:5000,perCycleMicros:5000,dailyMicros:10000,maxAttempts:1,timeoutMs:200,expiresAt:'2030-01-01T00:00:00Z'};
const fallback=new ProductFallback();
function planner(kind:Proposal['kind'],tool:Proposal['tool']=null):PlannerV2{return {propose:async c=>({...await fallback.propose(c),kind,tool,intent:'Fixture',arguments:{text:'Local test artifact'},assistance:kind==='REQUEST_ASSISTANCE'?'Please review a local question.':null,deferUntil:kind==='DEFER'?'2030-01-01T00:00:00Z':null})};}
for(const [name,p,verdict,action] of [
 ['normal reasoning/local reflection',planner('PROPOSAL','local_reflection'),'ALLOW','local_saved'],
 ['abstention',planner('ABSTAIN'),'ALLOW','not_executed'],['defer',planner('DEFER'),'DEFER','not_executed'],
 ['assistance',planner('REQUEST_ASSISTANCE'),'REQUIRE_HUMAN_APPROVAL','not_executed'],
 ['artifact',planner('PROPOSAL','local_artifact'),'ALLOW','local_saved'],
 ['pending approval',planner('PROPOSAL','external_message'),'REQUIRE_HUMAN_APPROVAL','not_executed']
] as const)test('Active fixture: '+name,{skip},()=>activeFixture(async h=>{
 const f=await h.claim('cycle');const result=await h.prepare(f,p,permission);assert.equal(result.decision.policy?.verdict,verdict);assert.equal(result.decision.action.status,action);await h.journal(f,result.decision);const d=await h.commit(f,result);assert.equal(d.cycle,8);await assert.rejects(h.commit(f,result));assert.equal((await h.pool.query('SELECT count(*) FROM genesis_decisions')).rows[0].count,'8');assert.equal((await h.pool.query("SELECT record->>'executionLock' AS lock FROM genesis_life_state")).rows[0].lock,'OPEN');
 if(verdict==='REQUIRE_HUMAN_APPROVAL')assert.equal((await h.pool.query('SELECT record FROM genesis_action_intents')).rows[0].record.status,'awaiting_approval');
}));
test('Active fixture: policy denial cannot stage local artifact',{skip},()=>activeFixture(async h=>{const f=await h.claim('denied');const r=await h.prepare(f,planner('PROPOSAL','local_artifact'),{...permission,localArtifacts:false});assert.equal(r.decision.policy?.verdict,'DENY');assert.equal(r.decision.action.status,'not_executed');await h.commit(f,r);}));
test('Active fixture: provider failure commits failure with no fallback',{skip},()=>activeFixture(async h=>{const f=await h.claim('failed');const r=await h.prepare(f,{propose:async()=>{throw Error('test failure');}},permission);assert.equal(r.decision.outcome.status,'failed');assert.equal(r.decision.proposal,null);await h.commit(f,r);}));
for(const phase of ['before planning','during planning','before commit','lock closing','stale revision','stale lease'])test('Active fixture: '+phase,{skip},()=>activeFixture(async h=>{
 const f=await h.claim('cancel');
 if(phase==='before planning'){await h.cancel(f.cycleId);await assert.rejects(h.prepare(f,fallback,permission));return;}
 if(phase==='during planning'){await assert.rejects(h.prepare(f,{propose:async c=>{await h.cancel(f.cycleId);return fallback.propose(c);}},permission));return;}
 const r=await h.prepare(f,planner('PROPOSAL','local_artifact'),permission);
 if(phase==='before commit')await h.cancel(f.cycleId);
 if(phase==='lock closing')await h.pool.query("UPDATE genesis_life_state SET record=jsonb_set(record,'{executionLock}','\"CLOSED\"')");
 if(phase==='stale revision')await h.pool.query('UPDATE genesis_life_state SET revision=revision+1');
 if(phase==='stale lease')await h.tx(c=>c.query("UPDATE genesis_organisms SET lease_until=now()-interval '1 second'"));
 await assert.rejects(h.commit(f,r));await assert.rejects(h.check(f));assert.equal((await h.pool.query('SELECT count(*) FROM genesis_decisions')).rows[0].count,'7');
}));
test('Active fixture: two workers race for exactly one lease',{skip},()=>activeFixture(async h=>{const other=await IsolatedCycle.connect(h.pool);const r=await Promise.allSettled([h.claim('a'),other.claim('b')]);assert.equal(r.filter(x=>x.status==='fulfilled').length,1);}));
async function installed(h:IsolatedCycle,g=grant){await h.pool.query('INSERT INTO genesis_provider_grants(id,record) VALUES($1,$2)',[g.id,g]);return new ProviderControl(h.pool,f=>h.check(f));}
const good:ProviderTransport=async r=>({id:'response-1',requestId:'request-1',model:r.model,usage:{inputTokens:80,outputTokens:30},proposal:{schemaVersion:2,id:'p',contextHash:r.contextHash,kind:'ABSTAIN',intent:'No local work required',taskId:null,projectId:null,tool:null,arguments:{text:''},citations:[],rationale:'Remain inactive in this fixture.',cost:{namespace:'OPERATIONAL',maxMicros:0},uncertainty:'Test fixture',deferUntil:null,assistance:null,changes:[],planner:'ignored'}});
test('Provider: durable reservation before request, provenance/usage recorded',{skip},()=>activeFixture(async h=>{
 const pc=await installed(h);const f=await h.claim('provider');let calls=0;const r=await h.prepare(f,pc.planner(grant.id,f,'attempt',counter,async req=>{calls++;const row=(await h.pool.query('SELECT record FROM genesis_provider_attempts')).rows[0].record;assert.equal(row.status,'dispatching');assert.equal(row.reservedMicros,2500);assert.equal(req.model,'fixture-model');return good(req);}),permission);assert.equal(calls,1);assert.equal(r.decision.proposal?.kind,'ABSTAIN');await h.commit(f,r);const record=(await h.pool.query('SELECT record FROM genesis_provider_attempts')).rows[0].record;assert.equal(record.costMicros,140);assert.equal(record.status,'received');assert.equal(record.response.contextHash,r.decision.lifeContext.contextHash);
}));
for(const mode of ['disabled','model bypass','token ceiling','per call','daily','timeout','ambiguous','revoked','cancelled','usage mismatch'])test('Provider: '+mode,{skip},()=>activeFixture(async h=>{
 const g={...grant,enabled:mode!=='disabled',perCallMicros:mode==='per call'?1:5000,dailyMicros:mode==='daily'?1:10000,timeoutMs:40};const pc=await installed(h,g);const f=await h.claim('provider-'+mode);let calls=0;
 const transport:ProviderTransport=async req=>{calls++;if(mode==='ambiguous')throw Error('SECRET_KEY_SHOULD_NOT_BE_SAVED');if(mode==='timeout')return new Promise(()=>{});if(mode==='cancelled'){await h.cancel(f.cycleId);return new Promise(()=>{});}if(mode==='revoked'){await h.pool.query("UPDATE genesis_provider_grants SET record=jsonb_set(record,'{enabled}','false')");return new Promise(()=>{});}const r=await good(req);if(mode==='usage mismatch')r.usage.outputTokens=9999;return r;};
 const r=await h.prepare(f,pc.planner(g.id,f,'attempt',mode==='model bypass'?{...counter,model:'environment-chosen-model'}:mode==='token ceiling'?{...counter,count:()=>9000}:counter,transport),permission).catch(()=>null);
 if(['disabled','model bypass','token ceiling','per call','daily'].includes(mode)){assert.equal(calls,0);assert.equal(r?.decision.outcome.status,'failed');}
 else {assert.equal(calls,1);const record=(await h.pool.query('SELECT record FROM genesis_provider_attempts')).rows[0].record;assert.equal(record.status,'unknown');assert.equal(record.costMicros,null);assert(!JSON.stringify(record).includes('SECRET_KEY'));await assert.rejects(pc.planner(g.id,f,'retry',counter,good).propose({} as never));}
}));
test('Provider: restart conserves unknown liability; reconciliation needs provenance',{skip},()=>activeFixture(async h=>{
 const pc=await installed(h);const f=await h.claim('recovery');let context:Parameters<PlannerV2['propose']>[0]|undefined;await h.prepare(f,{propose:async c=>{context=c;await pc.reserve('a',grant.id,f,c,counter);return fallback.propose(c);}},permission);
 const restarted=new ProviderControl(h.pool,x=>h.check(x));await restarted.recover();assert.equal((await h.pool.query('SELECT record FROM genesis_provider_attempts')).rows[0].record.status,'unknown');await assert.rejects(restarted.reserve('b',grant.id,f,context!,counter),/Ambiguous/);await assert.rejects(restarted.reconcile('a',{operator:'',reference:'',costMicros:0}));await restarted.reconcile('a',{operator:'fixture-reviewer',reference:'fixture-zero-charge-receipt',costMicros:0});await assert.rejects(restarted.reserve('c',grant.id,f,context!,counter),/budget/);
}));
test('Approval: changed payload cannot become approved',{skip},()=>activeFixture(async h=>{const f=await h.claim('approval');const r=await h.prepare(f,planner('PROPOSAL','external_message'),permission);const p=r.decision.proposal!;assert(!approvalMatches({id:'a',payloadHash:digest(p),operation:'external_message',recipient:null,network:null,asset:null,maximumMicros:0,expiresAt:'2030-01-01T00:00:00Z',approver:'operator',policyVersion:'policy-v1'},{...p,arguments:{text:'altered'}},new Date().toISOString()));}));
for(const phase of ['before_commit','after_intent'])test('Fresh process crash: '+phase,{skip,timeout:15000},()=>activeFixture(async(h,schema,url)=>{
 const child=spawn(process.execPath,['tests/support/crash-worker.ts',phase],{env:{NODE_ENV:'test',PATH:process.env.PATH,TEST_DATABASE_URL:url,FIXTURE_SCHEMA:schema},stdio:['ignore','pipe','pipe']});let error='';child.stderr.on('data',x=>error+=x);const [code]=await once(child,'exit');assert.equal(code,77,error);
 const restarted=await IsolatedCycle.connect(h.pool);assert.equal((await h.pool.query('SELECT count(*) FROM genesis_decisions')).rows[0].count,'7');assert.equal((await h.pool.query('SELECT count(*) FROM genesis_action_intents')).rows[0].count,phase==='after_intent'?'1':'0');await assert.rejects(restarted.claim('crash'));
 await h.tx(c=>c.query("UPDATE genesis_organisms SET lease_until=now()-interval '1 second'"));await assert.rejects(restarted.claim('crash'));const next=await restarted.claim('new-explicit-attempt');assert(next.lease);assert.equal((await h.pool.query("SELECT count(*) FROM genesis_life_events WHERE record->>'kind'='episode'")).rows[0].count,'0');
}));
test('Provider: stale/cancelled worker cannot dispatch a reserved request',{skip},()=>activeFixture(async h=>{const pc=await installed(h);const f=await h.claim('stale-dispatch');let ctx:Parameters<PlannerV2['propose']>[0]|undefined;await h.prepare(f,{propose:async c=>{ctx=c;await pc.reserve('a',grant.id,f,c,counter);return fallback.propose(c);}},permission);await h.cancel(f.cycleId);let calls=0;await assert.rejects(pc.dispatch('a',grant.id,f,ctx!,grant,async r=>{calls++;return good(r);}));assert.equal(calls,0);assert.equal((await h.pool.query('SELECT record FROM genesis_provider_attempts')).rows[0].record.status,'not_sent');}));
test('Provider: atomic budget reservation rejects racing attempts',{skip},()=>activeFixture(async h=>{const pc=await installed(h);const f=await h.claim('budget-race');await h.prepare(f,{propose:async c=>{const attempts=await Promise.allSettled([pc.reserve('a',grant.id,f,c,counter),pc.reserve('b',grant.id,f,c,counter)]);assert.equal(attempts.filter(r=>r.status==='fulfilled').length,1);return fallback.propose(c);}},permission);assert.equal((await h.pool.query('SELECT count(*) FROM genesis_provider_attempts')).rows[0].count,'1');}));
test('Provider: cross-cycle daily liabilities cannot be reset by another model grant',{skip},()=>activeFixture(async h=>{const pc=await installed(h,{...grant,dailyMicros:2500});const f=await h.claim('cycle-one');const r=await h.prepare(f,pc.planner(grant.id,f,'a',counter,async()=>{throw Error('ambiguous');}),permission);await h.commit(f,r);await h.pool.query('INSERT INTO genesis_provider_grants(id,record) VALUES($1,$2)',['second-grant',{...grant,id:'second-grant',dailyMicros:2500}]);const f2=await h.claim('cycle-two');let calls=0;const r2=await h.prepare(f2,pc.planner('second-grant',f2,'b',counter,async req=>{calls++;return good(req);}),permission);assert.equal(calls,0);assert.equal(r2.decision.outcome.status,'failed');}));

for(const mode of ['invalid expiration','wrong cycle binding','altered context'])test('Provider binding: '+mode,{skip},()=>activeFixture(async h=>{
 const g={...grant,expiresAt:mode==='invalid expiration'?'not-a-date':grant.expiresAt};const pc=await installed(h,g);const f=await h.claim('binding');let calls=0;
 await h.prepare(f,{propose:async c=>{
  if(mode==='invalid expiration'){await assert.rejects(pc.reserve('a',g.id,f,c,counter));return fallback.propose(c);}
  await pc.reserve('a',g.id,f,c,counter);
  await assert.rejects(pc.dispatch('a',g.id,mode==='wrong cycle binding'?{...f,cycleId:'other-cycle'}:f,mode==='altered context'?{...c,text:c.text+'changed'}:c,g,async req=>{calls++;return good(req);}));
  assert.equal((await h.pool.query('SELECT record FROM genesis_provider_attempts')).rows[0].record.status,'reserved');return fallback.propose(c);
 }},permission);assert.equal(calls,0);
}));

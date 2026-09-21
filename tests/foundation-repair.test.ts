import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {oneShotFixture,authorize} from './support/one-shot-fixture.ts';
import {OneShotController} from '../server/one-shot.ts';
import {LifeExtensionStore} from '../server/life-store-v1.ts';
import {LifeStore} from '../server/store.ts';
import {GenesisService} from '../runtime/service.ts';
import {readConfig} from '../runtime/config.ts';
import {ProductFallback} from '../core/v2/planner.ts';
import {createIntent,validateIntent} from '../core/v2/intents.ts';
import {digest} from '../core/v2/identity.ts';
import {inspectOneShot} from '../server/cycle-inspection.ts';
import {savedSnapshotReference} from '../server/saved-provenance.ts';
import {operatorTrace} from '../core/v2/public.ts';
import {currentCopy,momentCopy,readObservation} from '../lib/observer-presentation.ts';
import {SavedObservationAdapter} from '../core/v2/biology.ts';
import {CElegansBrain} from '../core/brain/celegans.ts';
import type {Approval,PlannerV2,Proposal} from '../core/v2/contracts.ts';
const skip=!process.env.TEST_DATABASE_URL;
const fallback=new ProductFallback();
const planner=(kind:Proposal['kind'],tool:Proposal['tool']=null):PlannerV2=>({propose:async c=>({...await fallback.propose(c),kind,tool,arguments:{text:'PRIVATE_CANARY local artifact'},rationale:'PRIVATE_CANARY bounded stored rationale',assistance:kind==='REQUEST_ASSISTANCE'?'PRIVATE_CANARY help':null,deferUntil:kind==='DEFER'?'2030-01-01T00:00:00Z':null})});
const selected=(p:PlannerV2=fallback)=>({identity:'product-deterministic-v1',planner:p});
const service=(h:OneShotController,url:string)=>new GenesisService(new LifeStore(h.pool),readConfig({DATABASE_URL:url,GENESIS_OPERATOR_TOKEN:'test-operator-not-a-real-secret'}));
async function rows(h:OneShotController){const names=['genesis_organisms','genesis_life_state','genesis_decisions','genesis_life_events','genesis_action_intents','genesis_execution_grants','genesis_cycle_attempts','genesis_provider_attempts','genesis_schedule'];const out:Record<string,unknown>={};for(const name of names)out[name]=(await h.pool.query(`SELECT row_to_json(t) AS row FROM ${name} t ORDER BY row_to_json(t)::text`)).rows;return out;}

for(const [kind,tool,outcome,status] of [
 ['ABSTAIN',null,'abstained','abstained'],['DEFER',null,'deferred','deferred'],
 ['REQUEST_ASSISTANCE',null,'pending','awaiting_approval'],['PROPOSAL','external_message','pending','awaiting_approval'],
 ['PROPOSAL','local_reflection','local','local_completed'],['PROPOSAL','local_artifact','local','local_completed'],
 ['PROPOSAL',null,'recorded','local_completed'],
] as const)test(`Foundation intent/episode commit: ${kind}/${tool}`,{skip},()=>oneShotFixture(async(h,g,_schema,url)=>{
 await authorize(h,g);const f=await h.claim(g.id);const p=await h.prepare(f,selected(planner(kind,tool)));
 await h.journal(f,p.decision);const before=(await h.pool.query('SELECT record FROM genesis_action_intents')).rows[0].record;
 assert.equal(validateIntent(before,g.organismId).status,'proposed');assert.equal(before.policy.payloadHash,before.payloadHash);assert.equal(before.reservedMicros,0);assert.equal(before.approval,null);
 const d=await h.commit(f,p);const row=(await h.pool.query('SELECT record FROM genesis_action_intents')).rows[0].record;
 assert.equal(validateIntent(row,g.organismId).status,status);assert.equal(d.outcome.status,outcome);
 const ep=(await h.pool.query("SELECT record FROM genesis_life_events WHERE record->>'kind'='episode'")).rows[0].record;
 assert.equal(ep.record.outcomeStatus,outcome);assert.equal(ep.record.actionStatus,d.action.status);
 const trace=operatorTrace(d);assert.equal(trace.action.performed,outcome==='local');assert.equal(trace.event.id,d.event.id);assert.equal(trace.memory.committed,true);assert.equal(trace.humanReviewRequiredAtDecision,status==='awaiting_approval');
 const observed=await service(h,url).observe(false);assert.equal(observed.identity.cycles,8);assert.equal(observed.memoryAccounting.v2Episodes,1);assert.equal(observed.memoryAccounting.semanticAssertions,0);assert.equal(observed.memoryAccounting.legacyRecords,0); // fixture has no legacy memory TABLE rows
 assert.equal(observed.status,status==='awaiting_approval'?kind==='REQUEST_ASSISTANCE'?'AWAITING_ASSISTANCE':'AWAITING_APPROVAL':'IDLE');
 assert(!JSON.stringify(observed).includes('PRIVATE_CANARY'));
 if(['local_completed','abstained','deferred'].includes(status))await assert.rejects(new LifeExtensionStore(h.pool).recordIntentTransition(row.id,1,'denied',new Date().toISOString()),/transition/);
 await assert.rejects(h.commit(f,p));assert.equal(Number((await h.pool.query('SELECT count(*) AS n FROM genesis_decisions')).rows[0].n),8);
}));

test('A11 actual one-shot journal -> operator denial and duplicate refusal',{skip},()=>oneShotFixture(async(h,g)=>{
 await authorize(h,g);const f=await h.claim(g.id),p=await h.prepare(f,selected(planner('PROPOSAL','local_reflection')));await h.journal(f,p.decision);
 const store=new LifeExtensionStore(h.pool),id=f.cycleId+':intent';const denied=await store.recordIntentTransition(id,0,'denied',new Date().toISOString());assert.equal(denied.status,'denied');assert.equal(denied.organismId,g.organismId);assert.equal(denied.policy.payloadHash,digest(p.decision.proposal));
 await assert.rejects(store.recordIntentTransition(id,0,'denied',new Date().toISOString()),/stale/);await assert.rejects(h.commit(f,p),/already processed/);assert.equal(Number((await h.pool.query('SELECT count(*) AS n FROM genesis_decisions')).rows[0].n),7);
}));

test('Approval evidence survives one-shot journal -> operator transition; approval enables no effect',{skip},()=>oneShotFixture(async(h,g)=>{
 await authorize(h,g);const d=await h.run(g.id,async()=>selected(planner('PROPOSAL','external_message')));const store=new LifeExtensionStore(h.pool);
 const a:Approval={id:'test-approval',payloadHash:digest(d.proposal),operation:'external_message',recipient:null,network:null,asset:null,maximumMicros:0,expiresAt:'2030-01-01T00:00:00Z',approver:'fixture-operator',policyVersion:'policy-v1'};
 const next=await store.recordIntentTransition(d.id+':intent',1,'approved',new Date().toISOString(),a);assert.equal(next.approval?.id,a.id);assert.equal(next.status,'approved');assert.equal(next.reservedMicros,0);
 await assert.rejects(store.recordIntentTransition(d.id+':intent',2,'reserved',new Date().toISOString()),/disabled/);
 assert.equal((await inspectOneShot(h.pool,g.id))!.trace!.action.performed,false);
}));

for(const defect of ['missing policy','wrong payload','wrong organism','missing approval','missing reservation','extra field'])test('Intent persistence rejects '+defect,{skip},()=>oneShotFixture(async(h,g)=>{
 await authorize(h,g);const f=await h.claim(g.id),p=await h.prepare(f,selected());const i=createIntent(p.decision)!;const raw:Record<string,unknown>={...i};
 if(defect==='missing policy')delete raw.policy;if(defect==='wrong payload')raw.payloadHash='0'.repeat(64);if(defect==='wrong organism')raw.organismId='someone-else';if(defect==='missing approval')delete raw.approval;if(defect==='missing reservation')delete raw.reservedMicros;if(defect==='extra field')raw.permissive=true;
 await h.pool.query("INSERT INTO genesis_action_intents(id,organism_id,payload_hash,record) VALUES($1,'genesis',$2,$3)",[i.id,i.payloadHash,raw]);
 await assert.rejects(new LifeExtensionStore(h.pool).recordIntentTransition(i.id,0,'denied',new Date().toISOString()),/intent|Intent/);assert.equal((await h.pool.query('SELECT revision FROM genesis_action_intents')).rows[0].revision,'0');
}));

test('Policy denial differs from abstention across decision/episode/intent',{skip},()=>oneShotFixture(async(h,g)=>{
 g.permission.localArtifacts=false;g.permissionHash=digest(g.permission);await authorize(h,g);const d=await h.run(g.id,async()=>selected(planner('PROPOSAL','local_reflection')));
 assert.equal(d.outcome.status,'denied');assert.equal(d.action.status,'not_executed');assert.equal((await h.pool.query('SELECT record FROM genesis_action_intents')).rows[0].record.status,'denied');assert.equal((await inspectOneShot(h.pool,g.id))!.grant.result,'DENIED');
}));
test('Planner failure never creates an abstention intent',{skip},()=>oneShotFixture(async(h,g)=>{
 await authorize(h,g);const d=await h.run(g.id,async()=>selected({propose:async()=>{throw Error('PRIVATE_PROVIDER_FAILURE');}}));assert.equal(d.outcome.status,'failed');assert.equal(d.proposal,null);assert.equal((await h.pool.query('SELECT count(*) AS n FROM genesis_action_intents')).rows[0].n,'0');assert.equal((d.memory.episode.record as {outcomeStatus:string}).outcomeStatus,'failed');
}));
for(const close of ['cancel','failed','ambiguous'] as const)test('Uncommitted intent closure '+close,{skip},()=>oneShotFixture(async(h,g)=>{
 await authorize(h,g);const f=await h.claim(g.id),p=await h.prepare(f,selected(planner('PROPOSAL','local_artifact')));await h.journal(f,p.decision);
 if(close==='cancel')await h.cancel(f);else if(close==='failed')await h.fail(f);else{await h.tx(async c=>{await c.query("SELECT set_config('genesis.oneshot_grant',$1,true),set_config('genesis.oneshot_lease',$2,true)",[g.id,f.lease]);await c.query("UPDATE genesis_organisms SET lease_until=now()-interval '1 second'");});await h.recoverExpired(g.id);}
 const row=(await h.pool.query('SELECT record FROM genesis_action_intents')).rows[0].record;assert.equal(row.status,close==='cancel'?'cancelled':close==='failed'?'failed':'unknown');await assert.rejects(h.commit(f,p));assert.equal((await h.pool.query('SELECT count(*) AS n FROM genesis_decisions')).rows[0].n,'7');
 const before=await rows(h);const a=await inspectOneShot(h.pool,g.id),b=await inspectOneShot(new OneShotController(h.pool).pool,g.id);assert.deepEqual(a,b);assert.deepEqual(await rows(h),before);assert.equal(a!.canonicalCommit.observed,false);assert.equal(a!.automaticRetryAllowed,false);assert.equal(a!.executionMayReopen,false);assert.equal(a!.reviewRequired,close==='ambiguous');
}));

test('A07 computational-only commit preserves biological recording and replay provenance',{skip},async t=>oneShotFixture(async(h,g,_schema,url)=>{
 for(const method of ['step','stimulate','decodeBehavior'] as const)t.mock.method(CElegansBrain.prototype,method,()=>{throw Error('Forbidden neural advance');});
 const s=service(h,url),before=await s.observe(false);assert.equal(before.status,'DORMANT');assert.equal(before.biological.sourceDecisionId,'fixture-history-7');assert(before.biological.sourceRecordedAt);
 await authorize(h,g);const f=await h.claim(g.id);assert.equal((await s.observe(false)).status,'REASONING');const p=await h.prepare(f,selected());assert.equal(p.decision.biological.status,'not_applied');assert.equal(p.decision.biological.value,null);assert.equal(p.decision.biological.executedThisCycle,false);
 const d=await h.commit(f,p),after=await s.observe(false);assert.equal(after.biological.sourceRecordedAt,before.biological.sourceRecordedAt);assert.equal(after.biological.sourceDecisionId,before.biological.sourceDecisionId);assert.equal(after.activity.latestAt,d.at);assert.equal(after.activity.latestComputationalAt,d.at);assert.notEqual(after.activity.latestAt,after.biological.sourceRecordedAt);assert.equal(after.status,'IDLE');
 const replay=await s.replay('fixture-history-7');assert.equal(replay!.at,before.biological.sourceRecordedAt);assert.equal(await s.replay(d.id),null);
 const restarted=service(new OneShotController(h.pool),url);assert.equal((await restarted.observe(false)).biological.sourceRecordedAt,before.biological.sourceRecordedAt);assert.equal((await restarted.observe(false)).memoryAccounting.v2Episodes,1);
 assert.equal((await h.pool.query('SELECT enabled FROM genesis_schedule')).rows[0].enabled,false);assert.equal((await h.pool.query('SELECT record FROM genesis_life_state')).rows[0].record.executionLock,'CLOSED');
}));

test('Missing or nonmatching biological provenance is null, never latest activity',{skip},()=>oneShotFixture(async(h)=>{
 const o=(await h.pool.query('SELECT state FROM genesis_organisms')).rows[0].state;assert.equal(await savedSnapshotReference(h.pool,null),null);assert.equal(await savedSnapshotReference(h.pool,{...o.brain,version:999}),null);
 const fakeDb={query:async()=>({rows:[{id:'bad',at:'2026-01-01T00:00:00Z',recorded_at:'2027-01-01T00:00:00Z'}]})} as unknown as Parameters<typeof savedSnapshotReference>[0];assert.equal(await savedSnapshotReference(fakeDb,o.brain),null);
 const brain=new SavedObservationAdapter(o.id);assert.equal(brain.observe().sourceRecordedAt,null);assert.equal(brain.observe().value,null);assert.equal(brain.observe().status,'unavailable');
}));

test('Ambiguous provider inspection retains unknown liability, no body/secrets and no writes',{skip},()=>oneShotFixture(async(h,g,_schema,url)=>{
 await authorize(h,g);const f=await h.claim(g.id);
 await h.pool.query('INSERT INTO genesis_provider_attempts(id,cycle_id,grant_id,record) VALUES($1,$2,$3,$4)',['provider-attempt',f.cycleId,'fixture-provider-grant',{status:'unknown',reservedMicros:3000,costMicros:null,response:null,secretReference:'SECRET_CANARY',fence:f}]);
 await h.fail(f);const before=await rows(h),i=await inspectOneShot(h.pool,g.id);assert.equal(i!.grant.status,'AMBIGUOUS');assert.equal(i!.unresolvedProviderLiabilityMicros,3000);assert.equal(i!.providers[0].dispatchMayHaveOccurred,true);assert.equal(i!.providers[0].responseDurablyObserved,false);assert.equal(i!.providers[0].dispatchRecordedAt,null);assert.equal(i!.canonicalCommit.observed,false);assert.equal(i!.lastDurableTransition.state,'AMBIGUOUS');assert(i!.reconciliationEvidenceNeeded.length);assert(!JSON.stringify(i).includes('SECRET_CANARY'));assert.deepEqual(await rows(h),before);
 const publicState=await service(h,url).observe(false);assert.equal(publicState.status,'REVIEW_REQUIRED');assert(!JSON.stringify(publicState).includes('provider-attempt'));assert(!JSON.stringify(publicState).includes('SECRET_CANARY'));assert.match(currentCopy(readObservation(publicState)).title,/review/);await assert.rejects(h.claim(g.id));
 // Artificial response metadata is a fixture, not a provider call. Inspection must not export bodies.
 await h.pool.query("UPDATE genesis_provider_attempts SET record=record || $1::jsonb",[JSON.stringify({status:'received',costMicros:100,response:{id:'r',body:'PRIVATE_RESPONSE_CANARY'}})]);
 const received=await inspectOneShot(h.pool,g.id);assert.equal(received!.providers[0].responseDurablyObserved,true);assert.equal(received!.providers[0].observedCostMicros,100);assert.equal(received!.unresolvedProviderLiabilityMicros,0);assert.equal(received!.reviewRequired,true);assert(!JSON.stringify(received).includes('PRIVATE_RESPONSE_CANARY'));
}));

test('Read-only inspection tolerates malformed historical intent without inventing its fields',{skip},()=>oneShotFixture(async(h,g)=>{
 await authorize(h,g);const f=await h.claim(g.id);await h.pool.query("INSERT INTO genesis_action_intents(id,organism_id,payload_hash,record) VALUES($1,'genesis',$2,$3)",[f.cycleId+':intent','0'.repeat(64),{status:'proposed'}]);const i=await inspectOneShot(h.pool,g.id);assert.equal(i!.intent,null);assert.equal(i!.reviewRequired,true);assert(i!.integrityIssues.some(x=>x.includes('Malformed')));
}));

test('Public activity/count namespaces and private traces are not raw planner narration',{skip},()=>oneShotFixture(async(h,g,_schema,url)=>{
 const s=service(h,url);const before=await s.observe(false);assert.equal(before.memoryAccounting.v2Episodes,0);assert.equal(before.memoryAccounting.semanticAssertions,0); // administrative birth/migration event not an episode
 await authorize(h,g);const p:PlannerV2={propose:async c=>({...await planner('PROPOSAL','local_reflection').propose(c),changes:[{kind:'assertion',assertion:{id:'assertion',text:'PRIVATE_MEMORY_CANARY',sources:[c.sources[0]],confidence:null,author:'planner',verified:false,supersedes:null,contradictions:[]}}]})};
 const d=await h.run(g.id,async()=>selected(p)),state=await s.observe(false);assert.equal(state.memoryAccounting.v2Episodes,1);assert.equal(state.memoryAccounting.semanticAssertions,1);assert.equal(state.counts.memories,state.memoryAccounting.legacyRecords);assert(!JSON.stringify(state).includes('PRIVATE_MEMORY_CANARY'));assert(!JSON.stringify(state).includes('contextManifest'));assert(!JSON.stringify(state).includes('payloadHash'));
 const view=readObservation(state);assert.equal(view.memoryAccounting!.v2Episodes,1);assert.equal(momentCopy(view.history[0]).title,'Genesis saved something locally.');assert.equal(operatorTrace(d).memory.changes.length,1);assert(!('text' in operatorTrace(d).contextManifest));
}));

test('Foundation pass adds no activation entry or external effect',()=>{
 for(const file of ['runtime/main.ts','runtime/http.ts','runtime/scheduler.ts','scripts/run-life.mjs','scripts/demo.ts'])assert(!readFileSync(file,'utf8').includes('OneShotController'),file);
 const read=readFileSync('server/cycle-inspection.ts','utf8');assert(!/fetch\(|UPDATE |INSERT |DELETE |\.step\(/.test(read));
 const config=JSON.parse(readFileSync('config/first-awakening-v1.json','utf8'));assert.equal(config.maximumCycles,1);assert.equal(config.expectedDecisions,7);assert.equal(config.scheduleEnabled,false);assert.equal(config.authorization,'NOT_AUTHORIZED');
});

test('Wrong journal owner fails before any record is inserted',{skip},()=>oneShotFixture(async(h,g)=>{
 await authorize(h,g);const f=await h.claim(g.id),p=await h.prepare(f,selected());p.decision.organismId='wrong';await assert.rejects(h.journal(f,p.decision),/mismatched/);assert.equal((await h.pool.query('SELECT count(*) AS n FROM genesis_action_intents')).rows[0].n,'0');
}));
test('Mismatched episode status rolls back intent completion and canonical fixture commit',{skip},()=>oneShotFixture(async(h,g)=>{
 await authorize(h,g);const f=await h.claim(g.id),p=await h.prepare(f,selected(planner('PROPOSAL','local_artifact')));await h.journal(f,p.decision);(p.decision.memory.episode.record as Record<string,unknown>).outcomeStatus='abstained';await assert.rejects(h.commit(f,p),/Episode\/decision/);assert.equal((await h.pool.query('SELECT record FROM genesis_action_intents')).rows[0].record.status,'proposed');assert.equal((await h.pool.query('SELECT count(*) AS n FROM genesis_decisions')).rows[0].n,'7');
}));
test('Aborted or nonmatching claims never look like current reasoning',{skip},()=>oneShotFixture(async(h,g,_schema,url)=>{
 await authorize(h,g);const f=await h.claim(g.id);await h.cancel(f);const s=await service(h,url).observe(false);assert.notEqual(s.status,'REASONING');assert.equal(s.status,'DORMANT');assert.equal((await inspectOneShot(h.pool,g.id))!.grant.status,'REVOKED');
}));
test('Terminal intents cannot be reserved again',{skip},()=>oneShotFixture(async(h,g)=>{
 const {reserveAttempt}=await import('../core/v2/policy.ts');await authorize(h,g);const d=await h.run(g.id,async()=>selected());const intent=(await h.pool.query('SELECT record FROM genesis_action_intents')).rows[0].record;assert.equal(intent.status,'abstained');assert.throws(()=>reserveAttempt(intent,5,50000));assert.equal(d.cycle,8);
}));

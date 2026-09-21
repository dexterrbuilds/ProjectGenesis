import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {observerFixtures} from '../lib/observer-fixtures.ts';
import {readObservation,momentCopy,currentCopy,resourceCopy,reasoningCopy,readView,OBSERVER_VIEWS,decisionSchema} from '../lib/observer-presentation.ts';
import {developmentPreviewEnabled} from '../lib/awakening.ts';
const fixture=observerFixtures();
const state=fixture.observations[0].state;
const moment=(id:string)=>fixture.observations.find(x=>x.id===id)!.state.history[0];

test('observer allowlist strips private context, memory, approval and transport fields at every level',()=>{
 const canary='PRIVATE_CANARY_DO_NOT_DISCLOSE';
 const parsed=readObservation({...state,rawContext:canary,memories:[{text:canary}],projects:[{name:canary}],providerKey:canary,operator:canary,revision:canary,identity:{...state.identity,privateIdentity:canary},history:state.history.map(d=>({...d,rationale:canary,proposal:{arguments:canary},approval:canary,lifeContext:canary,biological:{status:'not_applied',executedThisCycle:false,sourceRecordedAt:null,modelId:'saved',privateState:canary}}))});
 assert.equal(JSON.stringify(parsed).includes(canary),false);
 assert.equal(JSON.stringify(parsed.history.map(momentCopy)).includes(canary),false);
});
test('UI takes only public observations; production components do not read store or planner content',()=>{
 const source=readFileSync('components/live-observation.tsx','utf8');
 assert.ok(source.includes('readObservation(await r.json())'));
 for(const forbidden of ['server/store','server/runtime','core/v2/context','.rationale','.arguments','.lifeContext','.approval','.memories.map'])assert.equal(source.includes(forbidden),false,forbidden);
 assert.ok(source.includes('No memory excerpts have been approved for public sharing.'));
});
test('no arbitrary planner text or legacy semantic label can become current narration',()=>{
 const raw={...moment('reflection'),rationale:'The neurons crave profit',reasoning:{rationale:'secret'}};
 const parsed=decisionSchema.parse(raw);
 assert.equal(JSON.stringify(momentCopy(parsed)).includes('crave'),false);
 const legacy=decisionSchema.parse({schemaVersion:1,id:'legacy',at:'2026-09-15T00:00:00Z',cycle:7,legacyLabel:'APPROACH'});
 assert.equal(momentCopy(legacy).title,'An earlier experience, preserved.');
 assert.equal(JSON.stringify(momentCopy(legacy)).includes('APPROACH'),false);
 const source=readFileSync('components/live-observation.tsx','utf8');
 assert.ok(source.includes('not a validated biological action and has no authority now'));
});
test('not-applied biology and planning sources have separate plain-language explanations',()=>{
 assert.equal(momentCopy(moment('reflection')).biology,'The biological system wasn’t involved in this decision.');
 assert.match(reasoningCopy(moment('reflection')),/rule-based planner, separate/);
 const d=moment('reflection');assert.equal(d.schemaVersion,2);if(d.schemaVersion===2)assert.match(reasoningCopy({...d,reasoningSource:'LLM REASONING'}),/Language-model planning, separate/);
});
test('denial, assistance, abstention and deferral translate without implied external effects',()=>{
 assert.equal(momentCopy(moment('denied')).title,'Genesis wasn’t allowed to do this.');
 assert.equal(momentCopy(moment('assistance')).title,'Genesis asked for help.');
 assert.match(momentCopy(moment('assistance')).outcome,/No message was sent/);
 assert.match(momentCopy(moment('abstention')).title,/not to act/);
 assert.match(momentCopy(moment('defer')).title,/another time/);
 assert.match(momentCopy(moment('failure')).title,/couldn’t complete/);
});
test('local text save does not invent reflection, project, publication or motive',()=>{
 assert.deepEqual(momentCopy(moment('reflection')),momentCopy(moment('artifact')));
 assert.equal(momentCopy(moment('artifact')).title,'Genesis saved something locally.');
});
test('canonical dormant status overrides all activity examples',()=>{
 assert.equal(currentCopy(state).label,'Dormant');
 assert.match(currentCopy(state).description,/No new activity/);
 assert.equal(currentCopy(state,true).label,'Example of a recorded moment');
 assert.equal(currentCopy(null).label,'Observation unavailable');
});
test('resources retain namespaces and unknown wallet/revenue never turn into zero',()=>{
 const copy=resourceCopy(state);
 assert.equal(copy.label,'Simulated resources');assert.equal(copy.amount,'$100.75');
 assert.equal(state.onchain.balance,null);assert.equal(state.attributedRevenue.value,null);
 assert.match(copy.wallet,/not been verified/);assert.equal(copy.wallet.includes('$0'),false);
 assert.match(copy.revenue,/No verified earnings/);
 assert.throws(()=>readObservation({...state,onchain:{...state.onchain,balance:0}}));
 assert.throws(()=>readObservation({...state,economy:{...state.economy,namespace:'ONCHAIN ECONOMY'}}));
});
test('fixture lives are uncommitted, descending in time, and clearly distinguished',()=>{
 for(const scenario of fixture.observations){assert.equal(scenario.state.identity.cycles,7);assert.ok(scenario.state.identity.id.startsWith('fixture-'));assert.ok(scenario.state.history.every(d=>d.cycle===null));assert.deepEqual(scenario.state.history.map(d=>d.at),scenario.state.history.map(d=>d.at).sort().reverse());}
 const source=readFileSync('components/live-observation.tsx','utf8');
 assert.ok(source.includes('NOT CANONICAL · NOT AWAKENED · DEVELOPMENT FIXTURE'));
 assert.ok(source.includes('Example public memory · development fixture'));
 assert.ok(source.includes('Illustrative projects & interests · development fixture'));
});
test('preview page and read-only fixture endpoints are unavailable in production',()=>{
 for(const flag of ['true','false',undefined])assert.equal(developmentPreviewEnabled({NODE_ENV:'production',GENESIS_DEV_PREVIEW:flag}),false);
 for(const path of ['app/preview/page.tsx','app/api/preview/[kind]/route.ts'])assert.ok(readFileSync(path,'utf8').includes('developmentPreviewEnabled(process.env)'));
 const api=readFileSync('app/api/preview/[kind]/route.ts','utf8');assert.equal(/export async function POST|server\/store|stimulate|\.step\(/.test(api),false);
});
test('network is static by default; only historical measured values can illuminate it',()=>{
 const source=readFileSync('components/observer/network.tsx','utf8');
 assert.ok(source.includes("kind:'historical'"));assert.ok(source.includes('recording.frame.activity'));
 for(const forbidden of ['Math.random','requestAnimationFrame','setInterval','stimulate'])assert.equal(source.includes(forbidden),false);
 assert.ok(source.includes('Static structure only; no new neural activity.'));
 assert.ok(source.includes('Historical saved activity, not live.'));
 assert.ok(source.includes('ResizeObserver'));assert.ok(source.includes('memo(function ObserverNetwork'));
 assert.ok(readFileSync('components/live-observation.tsx','utf8').includes('const recording=useMemo'));
});
test('navigation, responsive layout and accessible reduced-motion fallback are present',()=>{
 assert.deepEqual(OBSERVER_VIEWS,['live','brain','life','money','memory','about']);assert.equal(readView('secrets'),'live');
 const ui=readFileSync('components/live-observation.tsx','utf8'),css=readFileSync('components/observer/observer.css','utf8');
 for(const text of ['aria-current','aria-controls="observer-nav"','Skip to Genesis','Saved response frame'])assert.ok(ui.includes(text));
 for(const text of ['prefers-reduced-motion:reduce','max-width:760px',':focus-visible','canvas-fallback'])assert.ok(css.includes(text));
});

/** Local UI-review fixture; never a production route or canonical runtime. */
import {createServer} from 'node:http';
import {readFileSync,writeFileSync} from 'node:fs';
import data from '../../data/connectome.json' with {type:'json'};
import {publicState,publicDecision} from '../../core/v2/public.ts';
import {prepareCycle} from '../../core/v2/cycle.ts';
import {SavedObservationAdapter} from '../../core/v2/biology.ts';
import {ProductFallback} from '../../core/v2/planner.ts';
import {CLOSED_PERMISSIONS,serializedDigest,digest} from '../../core/v2/identity.ts';
import type {Organism,Decision} from '../../core/contracts.ts';
const rows=JSON.parse(readFileSync('outputs/final-pre-awakening-PRIVATE_BEFORE.json','utf8')).rows;
const o:Organism=structuredClone(rows.genesis_organisms[0].state);o.id='fixture-genesis-review';
const life=structuredClone(rows.genesis_life_state[0].record);life.organismId=o.id;
const decisions:Decision[]=rows.genesis_decisions.map((r:{record:Decision})=>r.record).sort((a:Decision,b:Decision)=>b.cycle-a.cycle);
const brain=new SavedObservationAdapter(o.id);brain.restore({bytes:JSON.stringify(o.brain),sha256:serializedDigest(o.brain),recordedAt:decisions[0].at,parent:null});
const permission={...CLOSED_PERMISSIONS,execution:true,localArtifacts:true};
const authority={grantId:'NOT-CANONICAL-FIXTURE',grantHash:'0'.repeat(64),permissionHash:digest(permission),event:{notice:'NOT CANONICAL / NOT AWAKENED / DEVELOPMENT FIXTURE'}};
const prepared=await prepareCycle(o,life,brain,new ProductFallback(),{id:'fixture-event',kind:'digital-event',source:'local-review-fixture',observedAt:'2026-09-20T12:00:00Z'},permission,'2026-09-20T12:00:00Z','fixture-v2',authority);
prepared.decision.cycle=null;
prepared.decision.reasoning.rationale='PRIVATE_CONTEXT_CANARY';
prepared.decision.memory.episode.record={private:'PRIVATE_MEMORY_CANARY',approval:'PRIVATE_APPROVAL_CANARY'};
const state={...publicState(o,life),history:[publicDecision(prepared.decision),...decisions.map(publicDecision)],schedule:{enabled:false},biological:{mode:'SAVED-OBSERVATION-ONLY',status:'saved-model-output',sourceRecordedAt:decisions[0].at,modelClock:o.brain?.payload,limitations:['Saved historical model output'],availableCapabilities:[]}};
// The model clock is a scalar, never the raw private snapshot.
state.biological.modelClock=brain.observe().modelClock;
const routes:Record<string,unknown>={'/api/state':state,'/api/history':{decisions:state.history},'/api/brain':{id:'celegans-cook2019-rate-v1',nodes:data.neurons,edges:data.edges}};
for(const [path,value] of Object.entries(routes)){if(JSON.stringify(value).includes('CANARY'))throw new Error('Public leakage');if(path!=='/api/brain')writeFileSync('outputs/final-pre-awakening/UI_'+path.split('/').pop()+'.json',JSON.stringify(value,null,2));}
createServer((req,res)=>{const u=new URL(req.url??'/','http://fixture');res.setHeader('Content-Type','application/json');if(req.method!=='GET'){res.writeHead(423);res.end('{}');return;}if(u.pathname==='/api/replay'){const d=decisions.find(x=>x.id===u.searchParams.get('id'));res.end(JSON.stringify({replay:d?{id:d.id,at:d.at,modelId:d.brainAfter.adapter,frames:d.frames,status:'SAVED HISTORICAL REPLAY — FIXTURE COPY',interpretation:'Genuine saved frames; no new computation.'}:null}));return;}res.end(JSON.stringify(routes[u.pathname]??{}));}).listen(3701,'127.0.0.1',()=>console.log('Observer fixture 3701; no DB, provider or worker'));

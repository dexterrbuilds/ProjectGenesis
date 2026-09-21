/** Isolated deterministic fixture measurement; no database/model/provider execution. */
import {readFileSync,writeFileSync} from 'node:fs';
import type {Organism} from '../../core/contracts.ts';
import {initialLifeState,CLOSED_PERMISSIONS} from '../../core/v2/identity.ts';
import {SavedObservationAdapter} from '../../core/v2/biology.ts';
import {retrieveMemory,RECALL_POLICY,EMPTY_QUERY,type MemoryArchive} from '../../core/v2/memory.ts';
import {compileContext} from '../../core/v2/context.ts';
const o=JSON.parse(readFileSync('tests/fixtures/genesis-dormant-sanitized.json','utf8')) as Organism,life=initialLifeState(o,0);
const now='2026-09-20T12:00:00.000Z',at='2026-09-19T12:00:00.000Z';
const bio=new SavedObservationAdapter(o.id,()=>now).accept({id:'synthetic-growth',kind:'digital-event',source:'fixture-only',observedAt:now,recall:{...EMPTY_QUERY,referenceIds:['d1:event']}});
const results=[];
for(const n of [10,100,1000]){
 const archive:MemoryArchive={legacy:[],episodes:[],decisions:[],complete:true};
 for(let i=1;i<=n;i++){
  const id='d'+i,text='A bounded local note '+i;
  archive.episodes.push({schemaVersion:1,id:id+':episode',organismId:o.id,at,kind:'episode',source:id,visibility:'private',record:{recall:RECALL_POLICY,outcomeStatus:'local',actionStatus:'local_saved',localArtifact:text}});
  archive.decisions.push({schemaVersion:2,id,organismId:o.id,at,cycle:7+i,event:{id:id+':event',kind:'digital-event',source:'fixture',observedAt:at},biological:{id:id+':bio',observedAt:at,status:'not_applied',executedThisCycle:false},proposal:{projectId:null,taskId:null},outcome:{status:'local'},action:{status:'local_saved',artifact:text},memory:{episode:{id:id+':episode'},changes:[]}});
 }
 const start=performance.now(),s=retrieveMemory(o,life,bio,archive,bio.input!.recall),ms=performance.now()-start;
 const c=compileContext(o,life,bio,CLOSED_PERMISSIONS,12000,undefined,archive);
 const repeated=retrieveMemory(o,life,bio,archive,bio.input!.recall);
 results.push({episodes:n,selected:s.items.length,memoryBytes:s.manifest.bytes,contextBytes:Buffer.byteLength(c.text),retrievalMs:ms,deterministic:JSON.stringify(s)===JSON.stringify(repeated),firstSelected:s.items[0]?.id,processRssBytes:process.memoryUsage().rss});
}
writeFileSync('verification/memory-pass/growth.json',JSON.stringify({fixtureOnly:true,modelAdvanced:false,liveProviderCalls:0,results},null,2)+'\n');
console.log(JSON.stringify(results));

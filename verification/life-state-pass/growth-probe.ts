/** Pure disposable fixture diagnostic. No database, provider or biological computation. */
import {readFileSync,writeFileSync} from 'node:fs';
import {initialLifeState,CLOSED_PERMISSIONS,digest} from '../../core/v2/identity.ts';
import {reduceLife} from '../../core/v2/life-state.ts';
import {selectOperationalContext} from '../../core/v2/operational-context.ts';
import {compileContext} from '../../core/v2/context.ts';
import {SavedObservationAdapter} from '../../core/v2/biology.ts';
import type {Operation} from '../../core/v2/operations.ts';
const o=JSON.parse(readFileSync('tests/fixtures/genesis-dormant-sanitized.json','utf8'));
const results=[];
for(const tasks of [20,100,300]){
 let life=initialLifeState(o,0);const at='2026-09-20T00:00:00.000Z';const start=performance.now();
 const apply=(operation:Operation)=>{const n=life.revision;life=reduceLife(life,{schemaVersion:1,id:'fixture-episode-'+n,organismId:o.id,at,kind:'episode',source:'fixture-cycle-'+n,visibility:'private',record:{}},[{kind:'operational',expectedRevision:n,sourceIds:['fixture-source'],operation}],['fixture-source'],[]);};
 for(let i=0;i<5;i++)apply({op:'project_create',id:'p'+i,title:'Neutral fixture',summary:'Local notes'});
 for(let i=0;i<tasks;i++)apply({op:'task_create',id:'t'+i,description:'Review a local note',projectId:'p'+(i%5),dueAt:null});
 apply({op:'artifact_create',id:'a',projectId:'p0',taskId:'t0',content:'Original local note'});
 for(let i=1;i<20;i++)apply({op:'artifact_revise',id:'a',expectedVersion:i,content:'Revision '+(i+1),reason:'Fixture revision'});
 for(let i=0;i<20;i++){
  apply({op:'question_create',id:'q'+i,question:'Which revision?',projectId:'p0',taskId:'t0'});
  if(i%2===0)apply({op:'question_status',id:'q'+i,expectedVersion:1,status:'closed',evidenceIds:[],reason:'Closed without answer'});
  apply({op:'commitment_create',id:'c'+i,purpose:'review_task',statement:'Review local note',projectId:'p0',taskId:'t0',relationshipId:null,reviewAt:null});
  if(i%2===0)apply({op:'commitment_status',id:'c'+i,expectedVersion:1,status:'fulfilled',reviewAt:null,evidenceIds:['fixture-source'],reason:'Recorded local review'});
  else apply({op:'commitment_status',id:'c'+i,expectedVersion:1,status:'cancelled',reviewAt:null,evidenceIds:[],reason:'No longer current'});
 }
 for(let i=0;i<5;i++){
  apply({op:'relationship_create',id:'r'+i,label:'Fixture respondent '+i,context:'provided_input',consent:'unknown'});
  apply({op:'assistance_create',id:'h'+i,question:'Which local record?',projectId:'p0',taskId:'t0',relationshipId:'r'+i});
 }
 apply({op:'focus_set',mode:'task',targetId:'t0',reason:'Current fixture task'});
 const constructionMs=performance.now()-start,viewStart=performance.now();
 const bio=new SavedObservationAdapter(o.id,()=>at).accept({id:'fixture-current',kind:'digital-event',source:'fixture',observedAt:at,recall:{referenceIds:['t0'],projectIds:['p0'],taskIds:['t0'],subjects:[],text:''}});
 const context=compileContext(o,life,bio,CLOSED_PERMISSIONS),selection=selectOperationalContext(life,['t0','p0'],false);
 results.push({tasks,projects:5,artifactVersions:20,questions:20,commitments:20,relationships:5,pendingAssistance:5,historyEntries:life.operational!.history.length,stateBytes:Buffer.byteLength(JSON.stringify(life)),constructionMs,contextMs:performance.now()-viewStart,contextBytes:Buffer.byteLength(context.text),operationalBytes:selection.manifest.bytes,selected:selection.manifest.selectedIds.length,omitted:selection.manifest.omitted.length,deterministic:context.hash===compileContext(o,life,bio,CLOSED_PERMISSIONS).hash,restartSame:digest(JSON.parse(JSON.stringify(life)))===digest(life)});
}
writeFileSync('verification/life-state-pass/growth.json',JSON.stringify({scope:'Synthetic local fixture, not a production benchmark',results},null,2)+'\n');console.log(JSON.stringify(results));

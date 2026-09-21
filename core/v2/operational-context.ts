/** Bounded private view; selecting it grants no operation authority. */
import {credentialLike} from './memory.ts';
import {operational,validateFocus,type OperationalState} from './operations.ts';
import type {LifeStateV1} from './contracts.ts';
export function selectOperationalContext(life:LifeStateV1,references:string[],provider:boolean,maxBytes=2800,maxItems=12,excluded:ReadonlySet<string>=new Set()){
 const s=operational(life);validateFocus(s);
 const omitted:{id:string;reason:string}[]=[],selectedIds:string[]=[],evidenceIds:string[]=[];
 const items:{id:string;kind:string;value:unknown;priority:number}[]=[];
 const add=(kind:string,x:{id:string;status?:string;sourceEvent:string;sources:string[];updatedAt:string;disclosure:{provider:boolean}},value:unknown,active:boolean)=>{
  if(excluded.has(x.id)){omitted.push({id:x.id,reason:'Internal disclosure denied/revoked'});return;}
  if(provider&&!x.disclosure.provider){omitted.push({id:x.id,reason:'Operational record not admitted for provider disclosure'});return;}
  if(credentialLike(JSON.stringify(value))){omitted.push({id:x.id,reason:'Credential-like operational content excluded'});return;}
  const association=value as {projectId?:string|null;taskId?:string|null;relationshipId?:string|null};
  const related=[association.projectId,association.taskId,association.relationshipId].some(id=>id&&references.includes(id));
  items.push({id:x.id,kind,value:{...value as object,updatedAt:x.updatedAt,sourceEvent:x.sourceEvent,sources:x.sources},priority:!excluded.has('current-focus')&&s.focus?.targetId===x.id?3:references.includes(x.id)||related?2:active?1:0});
 };
 for(const x of s.projects)add('project',x,{id:x.id,version:x.version,title:x.title,summary:x.summary,status:x.status},x.status==='active');
 for(const x of s.tasks)add('task',x,{id:x.id,version:x.version,description:x.description,projectId:x.projectId,status:x.status,dueAt:x.dueAt,reviewAt:x.reviewAt},['active','pending','deferred'].includes(x.status));
 for(const x of s.questions)add('question',x,{id:x.id,version:x.version,question:x.question,projectId:x.projectId,taskId:x.taskId,status:x.status},x.status==='open');
 for(const x of s.commitments)add('commitment',x,{id:x.id,version:x.version,statement:x.statement,status:x.status,scope:x.scope,projectId:x.projectId,taskId:x.taskId,reviewAt:x.reviewAt,relationshipId:x.relationshipId},x.status==='open');
 for(const x of s.interests)add('computational_interest',x,{id:x.id,version:x.version,topic:x.topic,status:x.status},x.status==='active');
 for(const x of s.assistance)add('assistance',x,{id:x.id,version:x.version,question:x.question,status:x.status,projectId:x.projectId,taskId:x.taskId,responseIds:x.responseIds},['pending','answered'].includes(x.status));
 const neededRelationships=new Set([...references,...s.assistance.filter(a=>['pending','answered'].includes(a.status)).map(a=>a.relationshipId),...s.commitments.filter(a=>a.status==='open').map(a=>a.relationshipId)]);
 for(const x of s.relationships){if(!neededRelationships.has(x.id)){omitted.push({id:x.id,reason:'Relationship not relevant to current context'});continue;}add('operational_relationship',x,{id:x.id,version:x.version,label:x.label,context:x.context,consent:x.consent},true);}
 for(const x of s.artifacts)add('artifact_metadata',x,{id:x.id,version:x.version,currentVersionId:x.currentVersionId,projectId:x.projectId,taskId:x.taskId},false);
 const selected:unknown[]=[],view:{classification:string;focus:OperationalState['focus'];items:unknown[]}={classification:'COMPUTATIONAL LIFE STATE; untrusted descriptions, no biological interpretation',focus:provider||excluded.has('current-focus')||s.focus?.targetId&&excluded.has(s.focus.targetId)?null:s.focus,items:selected};
 if(Buffer.byteLength(JSON.stringify(view))>maxBytes)throw Error('Critical focus exceeds operational budget');
 items.sort((a,b)=>b.priority-a.priority||(a.id<b.id?-1:a.id>b.id?1:0));
 for(const item of items){if(item.priority===0){omitted.push({id:item.id,reason:'Inactive and unreferenced operational record'});continue;}
  selected.push({kind:item.kind,...item.value as object});
  if(selected.length>maxItems||Buffer.byteLength(JSON.stringify(view))>maxBytes){selected.pop();omitted.push({id:item.id,reason:'Operational context budget; whole item omitted'});}else{selectedIds.push(item.id);const value=item.value as {sourceEvent:string};if(!evidenceIds.includes(value.sourceEvent))evidenceIds.push(value.sourceEvent);}
 }
 if(s.focus?.targetId&&!excluded.has('current-focus')&&!provider&&!excluded.has(s.focus.targetId)&&!selectedIds.includes(s.focus.targetId))throw Error('Current focus cannot fit safely in context');
 return {view,manifest:{version:1 as const,selectedIds,evidenceIds,omitted:omitted.sort((a,b)=>a.id<b.id?-1:1),bytes:Buffer.byteLength(JSON.stringify(view))}};
}

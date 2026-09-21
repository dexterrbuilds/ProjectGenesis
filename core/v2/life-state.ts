import {operationalChangeSchema,applyOperational,operational,operationalIds,type OperationalChange} from './operations.ts';
import type { LifeStateV1, LifeChange, LifeEvent } from './contracts.ts';
import { z } from 'zod';
const assertion=z.object({id:z.string().min(1),text:z.string().min(1).max(2000),sources:z.array(z.string()).min(1),confidence:z.number().min(0).max(1).nullable(),author:z.enum(['planner','operator']),verified:z.literal(false),supersedes:z.string().nullable(),contradictions:z.array(z.string())}).strict();
export const changeSchema=z.discriminatedUnion('kind',[
 operationalChangeSchema,
 z.object({kind:z.literal('assertion'),assertion}).strict(),
 z.object({kind:z.literal('project_status'),id:z.string(),status:z.enum(['active','paused','completed','abandoned']),reason:z.string().min(1).max(1000)}).strict(),
 z.object({kind:z.literal('defer_task'),id:z.string(),reviewAt:z.string().datetime({offset:true})}).strict(),
]);
export function reduceLife(state:LifeStateV1,event:LifeEvent,changes:LifeChange[],knownSources:string[],projectIds:string[]):LifeStateV1 {
 if(event.organismId!==state.organismId||event.kind!=='episode')throw new Error('Wrong life/event identity');
 if(state.episodicRefs.includes(event.id))throw new Error('Duplicate episode');
 const next=structuredClone(state);
 for(const raw of changes){
  const c=changeSchema.parse(raw);
  if(c.kind==='operational')continue;
  if(c.kind==='assertion'){
   const a=c.assertion;
   const mutableIds=state.operational?[...state.operational.projects,...state.operational.tasks,...state.operational.artifacts,...state.operational.interests,...state.operational.questions,...state.operational.commitments,...state.operational.relationships,...state.operational.assistance].map(x=>x.id):[];
   if(a.sources.some(s=>mutableIds.includes(s)))throw Error('Semantic provenance requires immutable episode, input or artifact-version source');
   if(a.author!=='planner' || a.sources.some(s=>!knownSources.includes(s)) || next.semanticMemory.some(x=>x.id===a.id)||operationalIds(operational(next)).includes(a.id)) throw new Error('Unverified assertion provenance or identity');
   if([a.supersedes,...a.contradictions].filter(Boolean).some(id=>!next.semanticMemory.some(x=>x.id===id)))throw new Error('Unknown assertion history');
   next.semanticMemory.push(a);
  } else if(c.kind==='project_status'){
   if(!projectIds.includes(c.id))throw new Error('Unknown project');
   next.projectLife=next.projectLife.filter(p=>p.id!==c.id);next.projectLife.push({id:c.id,status:c.status,reason:c.reason,source:event.id});
  } else {
   const task=next.tasks.find(t=>t.id===c.id);if(!task)throw new Error('Unknown task');task.status='deferred';task.reviewAt=c.reviewAt;
  }
 }
 const ops=changes.filter((c):c is OperationalChange=>c.kind==='operational');
 if(ops.length)next.operational=applyOperational(next,event,ops,knownSources,projectIds);
 next.episodicRefs.push(event.id);next.revision++;return next;
}

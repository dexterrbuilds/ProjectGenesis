/** Local computational events only. No biological stimulus, effect dispatcher or implicit authority. */
import {z} from 'zod';
import {digest} from './identity.ts';
import {operational} from './operations.ts';
import type {LifeStateV1,Proposal,Permissions,ObservationInput} from './contracts.ts';
const id=z.string().min(1).max(180).regex(/^[a-zA-Z0-9][a-zA-Z0-9:._-]*$/);
const time=z.string().datetime({offset:true});
const target={targetId:id,targetVersion:z.number().int().positive()};
export const eventPayloadSchema=z.discriminatedUnion('kind',[
 z.object({kind:z.literal('MANUAL_EVENT'),text:z.string().min(1).max(1000),references:z.array(id).max(10)}).strict(),
 z.object({kind:z.literal('TIME_WAKE'),reason:z.literal('recorded_deferral'),projectId:id.nullable(),taskId:id.nullable()}).strict(),
 z.object({kind:z.literal('CONTINUATION'),reason:z.string().min(1).max(300),projectId:id.nullable(),taskId:id.nullable()}).strict(),
 ...(['TASK_REVIEW_DUE','COMMITMENT_REVIEW_DUE','PROJECT_REVIEW','ASSISTANCE_REVIEW','QUESTION_REVIEW'] as const).map(kind=>z.object({kind:z.literal(kind),...target}).strict()),
 z.object({kind:z.literal('HUMAN_RESPONSE_RECEIVED'),requestId:id,responseId:id,inputEventId:id}).strict(),
 z.object({kind:z.literal('SYSTEM_RECOVERY'),reference:id}).strict(),
]);
export type EventPayload=z.infer<typeof eventPayloadSchema>;
export const EVENT_KINDS=['MANUAL_EVENT','TIME_WAKE','CONTINUATION','TASK_REVIEW_DUE','COMMITMENT_REVIEW_DUE','PROJECT_REVIEW','ASSISTANCE_REVIEW','QUESTION_REVIEW','HUMAN_RESPONSE_RECEIVED','SYSTEM_RECOVERY'] as const;
export const eventSchema=z.object({version:z.literal(1),id,organismId:id,createdAt:time,availableAt:time,expiresAt:time.nullable(),dedupKey:id,source:z.enum(['operator','cycle','human_input','recovery']),sourceRef:id,visibility:z.literal('private'),disclosure:z.object({internal:z.literal(true),provider:z.literal(false),public:z.literal(false)}).strict(),parentEventId:id.nullable(),parentCycleId:id.nullable(),rootId:id,depth:z.number().int().min(0).max(100),payload:eventPayloadSchema}).strict();
export type RuntimeEvent=z.infer<typeof eventSchema>;
export const followUpSchema=z.discriminatedUnion('kind',[
 z.object({kind:z.literal('CONTINUATION'),availableAt:time,reason:z.string().min(1).max(300)}).strict(),
 ...(['TASK_REVIEW_DUE','COMMITMENT_REVIEW_DUE','PROJECT_REVIEW','ASSISTANCE_REVIEW','QUESTION_REVIEW'] as const).map(kind=>z.object({kind:z.literal(kind),targetId:id,availableAt:time}).strict()),
]);
export type FollowUp=z.infer<typeof followUpSchema>;
export type ContinuousContext={kind:'CONTINUOUS_LOCAL_V1';scopeId:string;scopeHash:string;permissionHash:string;event:RuntimeEvent;limits:{maxDepth:number;maxFollowups:number;minimumDelayMs:number;allowedEvents:readonly string[];allowedEffects:readonly string[];scheduling:boolean};resources:{scopeClaims:number;windowClaims:number;reservedMicros:number;committedMicros:number}};
export const LOCAL_PERMISSION:Permissions={execution:true,localArtifacts:true,llm:false,internet:false,communication:false,financial:false,maxCostMicros:0,maxAttempts:0};
export function eventObservation(e:RuntimeEvent,at:string):ObservationInput{
 const p=e.payload,refs='references'in p?p.references:'targetId'in p?[p.targetId]:p.kind==='HUMAN_RESPONSE_RECEIVED'?[p.requestId,p.responseId,p.inputEventId]:[];
 return {id:e.id,kind:'digital-event',source:'durable-local-event:'+p.kind,observedAt:at,recall:{referenceIds:refs,projectIds:'projectId'in p&&p.projectId?[p.projectId]:p.kind==='PROJECT_REVIEW'?[p.targetId]:[],taskIds:'taskId'in p&&p.taskId?[p.taskId]:p.kind==='TASK_REVIEW_DUE'?[p.targetId]:[],subjects:[],text:p.kind==='MANUAL_EVENT'?p.text:''}};
}
export function obsolete(e:RuntimeEvent,l:LifeStateV1):string|null{
 const s=operational(l),p=e.payload;
 if('targetId'in p){const list=p.kind==='TASK_REVIEW_DUE'?s.tasks:p.kind==='COMMITMENT_REVIEW_DUE'?s.commitments:p.kind==='PROJECT_REVIEW'?s.projects:p.kind==='QUESTION_REVIEW'?s.questions:s.assistance;const x=list.find(x=>x.id===p.targetId);
  if(!x||x.version!==p.targetVersion)return 'Target missing or changed version';
  if(['completed','cancelled','fulfilled','resolved','closed','abandoned','paused'].includes(x.status))return 'Target no longer eligible';
  if('projectId'in x&&x.projectId&&s.projects.some(y=>y.id===x.projectId&&y.status!=='active'))return 'Parent project no longer active';
 }
 if('taskId'in p&&p.taskId&&(!s.tasks.some(t=>t.id===p.taskId&&!['completed','cancelled'].includes(t.status))))return 'Task no longer eligible';
 if('projectId'in p&&p.projectId&&!s.projects.some(x=>x.id===p.projectId&&x.status==='active'))return 'Project missing or no longer active';
 if(p.kind==='HUMAN_RESPONSE_RECEIVED'){const q=s.assistance.find(x=>x.id===p.requestId);if(!q||['cancelled','resolved'].includes(q.status)||!q.responseIds.includes(p.responseId)||!s.responses.some(r=>r.id===p.responseId&&r.id+':input'===p.inputEventId))return 'Response/request no longer eligible';}
 return null;
}
export function followups(p:Proposal,life:LifeStateV1,parent:RuntimeEvent,cycleId:string,at:string,a:ContinuousContext):RuntimeEvent[]{
 const s=operational(life),specs:{payload:EventPayload;availableAt:string;key:string}[]=[];
 const target=(kind:FollowUp['kind'],key:string):EventPayload=>{
  if(kind==='CONTINUATION')throw Error('Missing continuation descriptor');
  const list=kind==='TASK_REVIEW_DUE'?s.tasks:kind==='COMMITMENT_REVIEW_DUE'?s.commitments:kind==='PROJECT_REVIEW'?s.projects:kind==='QUESTION_REVIEW'?s.questions:s.assistance;
  const x=list.find(x=>x.id===key);if(!x)throw Error('Unknown follow-up target');return {kind,targetId:key,targetVersion:x.version};
 };
 if(p.kind==='DEFER')specs.push({payload:{kind:'TIME_WAKE',reason:'recorded_deferral',projectId:p.projectId,taskId:p.taskId},availableAt:p.deferUntil!,key:'defer'});
 if(p.followUp){const f=followUpSchema.parse(p.followUp);specs.push({payload:f.kind==='CONTINUATION'?{kind:'CONTINUATION',reason:f.reason,projectId:p.projectId,taskId:p.taskId}:target(f.kind,f.targetId),availableAt:f.availableAt,key:'explicit'});}
 for(const c of p.changes){if(c.kind!=='operational')continue;const o=c.operation;
  if(o.op==='task_status'&&o.status==='deferred'||o.op==='task_create'&&o.dueAt){const x=s.tasks.find(x=>x.id===o.id)!;specs.push({payload:{kind:'TASK_REVIEW_DUE',targetId:x.id,targetVersion:x.version},availableAt:o.op==='task_create'?o.dueAt!:o.reviewAt!,key:'task:'+x.id+':v'+x.version});}
  if((o.op==='commitment_create'||o.op==='commitment_status'&&o.status==='open')&&o.reviewAt){const x=s.commitments.find(x=>x.id===o.id)!;specs.push({payload:{kind:'COMMITMENT_REVIEW_DUE',targetId:x.id,targetVersion:x.version},availableAt:o.reviewAt,key:'commitment:'+x.id+':v'+x.version});}
 }
 const unique=[...new Map(specs.map(x=>[digest({payload:x.payload,at:x.availableAt}),x])).values()];
 if(unique.length&&!a.limits.scheduling||unique.length>a.limits.maxFollowups||unique.length&&parent.depth>=a.limits.maxDepth)throw Error('Follow-up authority/chain limit');
 return unique.map(x=>{if(!a.limits.allowedEvents.includes(x.payload.kind)||Date.parse(x.availableAt)<Date.parse(at)+a.limits.minimumDelayMs)throw Error('Follow-up kind/delay outside scope');const key='wake:'+digest({cycleId,key:x.key,payload:x.payload,at:x.availableAt});const e=eventSchema.parse({...parent,id:key,dedupKey:key,createdAt:at,availableAt:x.availableAt,expiresAt:null,source:'cycle',sourceRef:cycleId,parentEventId:parent.id,parentCycleId:cycleId,rootId:parent.rootId,depth:parent.depth+1,payload:x.payload});if(obsolete(e,life))throw Error('Obsolete follow-up refused');return e;});
}

/** Computational life only. No neural semantics, timers, external effects or arbitrary patches. */
import {z} from 'zod';
import {digest} from './identity.ts';
import type {LifeStateV1,LifeEvent} from './contracts.ts';
const id=z.string().min(1).max(300).regex(/^[a-zA-Z0-9][a-zA-Z0-9:._-]*$/).refine(s=>!['constructor','prototype','__proto__'].includes(s));
const text=z.string().trim().min(1).max(1000);
const time=z.string().datetime({offset:true}).refine(s=>Number.isFinite(Date.parse(s)));
const date=time.nullable();
const ref=id.nullable();
const assoc={projectId:ref,taskId:ref};
const update={id,expectedVersion:z.number().int().positive()};
export const operationSchema=z.discriminatedUnion('op',[
 z.object({op:z.literal('project_create'),id,title:z.string().trim().min(1).max(120),summary:text}).strict(),
 z.object({op:z.literal('project_update'),...update,summary:text}).strict(),
 z.object({op:z.literal('project_status'),...update,status:z.enum(['active','paused','completed','abandoned']),reason:text}).strict(),
 z.object({op:z.literal('task_create'),id,description:text,projectId:ref,dueAt:date}).strict(),
 z.object({op:z.literal('task_status'),...update,status:z.enum(['active','deferred','completed','cancelled','pending']),reviewAt:date,evidenceIds:z.array(id).max(20),reason:text}).strict(),
 z.object({op:z.literal('artifact_create'),id,...assoc,content:z.string().min(1).max(6000)}).strict(),
 z.object({op:z.literal('artifact_revise'),...update,content:z.string().min(1).max(6000),reason:text}).strict(),
 z.object({op:z.literal('interest_add'),id,topic:z.string().trim().min(1).max(200)}).strict(),
 z.object({op:z.literal('interest_update'),...update,topic:z.string().trim().min(1).max(200)}).strict(),
 z.object({op:z.literal('interest_retire'),...update,reason:text}).strict(),
 z.object({op:z.literal('question_create'),id,...assoc,question:text}).strict(),
 z.object({op:z.literal('question_status'),...update,status:z.enum(['open','resolved','closed']),evidenceIds:z.array(id).max(20),reason:text}).strict(),
 z.object({op:z.literal('commitment_create'),id,...assoc,relationshipId:ref,purpose:z.enum(['finish_local_artifact','review_task','review_human_input','maintain_local_constraint']),statement:text,reviewAt:date}).strict(),
 z.object({op:z.literal('commitment_status'),...update,status:z.enum(['open','fulfilled','cancelled']),reviewAt:date,evidenceIds:z.array(id).max(20),reason:text}).strict(),
 z.object({op:z.literal('relationship_create'),id,label:z.string().trim().min(1).max(80),context:z.enum(['provided_input','assistance_contact','project_contact']),consent:z.literal('unknown')}).strict(),
 z.object({op:z.literal('relationship_update'),...update,context:z.enum(['provided_input','assistance_contact','project_contact'])}).strict(),
 z.object({op:z.literal('assistance_create'),id,...assoc,relationshipId:ref,question:text}).strict(),
 z.object({op:z.literal('assistance_resolve'),...update,responseId:id,reason:text}).strict(),
 z.object({op:z.literal('assistance_cancel'),...update,reason:text}).strict(),
 z.object({op:z.literal('focus_set'),mode:z.enum(['none','idle','project','task','assistance']),targetId:ref,reason:text}).strict(),
]);
export const operationalChangeSchema=z.object({kind:z.literal('operational'),expectedRevision:z.number().int().nonnegative(),sourceIds:z.array(id).min(1).max(20),operation:operationSchema}).strict();
export type OperationalChange=z.infer<typeof operationalChangeSchema>;
export type Operation=z.infer<typeof operationSchema>;
const privacy=z.object({visibility:z.literal('private'),internal:z.literal(true),provider:z.literal(false),public:z.literal(false)}).strict();
export const PRIVATE_LIFE={visibility:'private',internal:true,provider:false,public:false} as const;
const stamp={id,version:z.number().int().positive(),createdAt:time,updatedAt:time,sourceEvent:id,sources:z.array(id).min(1).max(20),disclosure:privacy};
const project=z.object({...stamp,title:z.string().max(120),summary:text,status:z.enum(['active','paused','completed','abandoned'])}).strict();
const task=z.object({...stamp,description:text,projectId:ref,status:z.enum(['pending','active','deferred','completed','cancelled']),dueAt:date,reviewAt:date,evidenceIds:z.array(id).max(20)}).strict();
const artifactVersion=z.object({id,revision:z.number().int().positive(),content:z.string().min(1).max(6000),at:time,sourceEvent:id,sources:z.array(id).min(1).max(20),supersedes:ref,disclosure:privacy}).strict();
const artifact=z.object({...stamp,...assoc,currentVersionId:id,versions:z.array(artifactVersion).min(1)}).strict();
const interest=z.object({...stamp,topic:z.string().max(200),status:z.enum(['active','retired'])}).strict();
const question=z.object({...stamp,...assoc,question:text,status:z.enum(['open','resolved','closed']),evidenceIds:z.array(id).max(20)}).strict();
const commitment=z.object({...stamp,...assoc,relationshipId:ref,purpose:z.enum(['finish_local_artifact','review_task','review_human_input','maintain_local_constraint']),statement:text,scope:z.literal('INTERNAL_COMPUTATIONAL'),status:z.enum(['open','fulfilled','cancelled']),reviewAt:date,evidenceIds:z.array(id).max(20)}).strict();
const relationship=z.object({...stamp,label:z.string().max(80),context:z.enum(['provided_input','assistance_contact','project_contact']),consent:z.literal('unknown')}).strict();
export const humanResponseSchema=z.object({id,organismId:id,requestId:id,receivedAt:time,respondentRef:id,attributionReference:id,content:z.string().trim().min(1).max(2000),relationshipId:ref,trust:z.literal('untrusted'),disclosure:privacy}).strict();
export type HumanResponse=z.infer<typeof humanResponseSchema>;
const assistance=z.object({...stamp,...assoc,relationshipId:ref,question:text,status:z.enum(['pending','answered','resolved','cancelled']),responseIds:z.array(id),resolutionResponseId:ref}).strict();
const focus=z.object({mode:z.enum(['none','idle','project','task','assistance']),targetId:ref,at:time,sourceEvent:id}).strict().nullable();
export const operationalStateSchema=z.object({version:z.literal(1),projects:z.array(project),tasks:z.array(task),artifacts:z.array(artifact),interests:z.array(interest),questions:z.array(question),commitments:z.array(commitment),relationships:z.array(relationship),assistance:z.array(assistance),responses:z.array(humanResponseSchema),focus,history:z.array(z.object({id,at:time,sourceEvent:id,sourceIds:z.array(id),operation:z.string().max(100),targetId:ref,fromVersion:z.number().int().nonnegative(),toVersion:z.number().int().nonnegative(),changeHash:z.string().length(64)}).strict())}).strict();
export type OperationalState=z.infer<typeof operationalStateSchema>;
export function emptyOperational():OperationalState{return {version:1,projects:[],tasks:[],artifacts:[],interests:[],questions:[],commitments:[],relationships:[],assistance:[],responses:[],focus:null,history:[]};}
export function operational(state:LifeStateV1):OperationalState{return state.operational===undefined?emptyOperational():operationalStateSchema.parse(state.operational);}
export const PROJECT_TRANSITIONS={active:['paused','completed','abandoned'],paused:['active','completed','abandoned'],abandoned:['active'],completed:[]} as const;
export const TASK_TRANSITIONS={pending:['active','deferred','completed','cancelled'],active:['deferred','completed','cancelled'],deferred:['pending','active','completed','cancelled'],completed:['pending'],cancelled:['pending']} as const;
export const QUESTION_TRANSITIONS={open:['resolved','closed'],resolved:['open'],closed:['open']} as const;
export const COMMITMENT_TRANSITIONS={open:['open','fulfilled','cancelled'],fulfilled:[],cancelled:[]} as const;
const traits=/\b(friendship|affection|trustworthy|untrustworthy|race|ethnicity|religion|sexual|diagnos|political|personality)\b/i;
const financial=/\b(pay|payment|purchase|buy|sell|loan|lend|debt|contract|legally|hire|salary|transfer|trade|invest|guarantee)\b|[$€£]/i;
const neural=/\b(?:worm|brain|neurons?)\s+(?:wants?|decid(?:ed|es)|chose)|neural curiosity|biological (?:interest|preference|desire|hunger)/i;
function transition(current:string,next:string,graph:Record<string,readonly string[]>){if(!graph[current]?.includes(next))throw Error('Invalid operational transition');}
function existing<T extends {id:string;version:number}>(list:T[],op:{id:string;expectedVersion:number}){const x=list.find(x=>x.id===op.id);if(!x||x.version!==op.expectedVersion)throw Error('Unknown target or stale entity version');return x;}
export function operationalIds(s:OperationalState){return [...s.projects,...s.tasks,...s.artifacts,...s.interests,...s.questions,...s.commitments,...s.relationships,...s.assistance,...s.responses,...s.artifacts.flatMap(a=>a.versions)].map(x=>x.id);}
function association(s:OperationalState,projectId:string|null,taskId:string|null,legacy:string[],active=true){
 if(projectId){const p=s.projects.find(x=>x.id===projectId);if(!p&&!legacy.includes(projectId)||active&&p&&p.status!=='active')throw Error('Unknown or inactive project');}
 if(taskId){const t=s.tasks.find(x=>x.id===taskId);if(!t||t.projectId!==projectId||active&&['completed','cancelled'].includes(t.status))throw Error('Invalid task/project ownership');}
}
export function validateFocus(s:OperationalState){const f=s.focus;if(!f)return;if(['none','idle'].includes(f.mode)){if(f.targetId!==null)throw Error('Idle focus has target');return;}
 if(f.mode==='project'&&!s.projects.some(x=>x.id===f.targetId&&x.status==='active')||f.mode==='task'&&!s.tasks.some(x=>x.id===f.targetId&&['pending','active','deferred'].includes(x.status))||f.mode==='assistance'&&!s.assistance.some(x=>x.id===f.targetId&&x.status==='pending'))throw Error('Inactive or unknown focus target');
 const t=f.mode==='task'?s.tasks.find(x=>x.id===f.targetId):null;if(t?.projectId&&s.projects.some(p=>p.id===t.projectId&&p.status!=='active'))throw Error('Focus project inactive');
}
/** All changes in a batch bind the input Life State revision. Target versions increment individually. */
export function applyOperational(state:LifeStateV1,event:LifeEvent,changes:OperationalChange[],knownSources:string[],legacyProjectIds:string[]):OperationalState{
 const s=operational(state);if(event.organismId!==state.organismId||!time.safeParse(event.at).success||!id.safeParse(event.id).success)throw Error('Operational event identity/time');
 if(s.history.some(h=>h.sourceEvent===event.id))throw Error('Duplicate operational source event');
 const allIds=new Set([...operationalIds(s),event.id,...knownSources,...state.episodicRefs,...legacyProjectIds,...state.tasks.map(x=>x.id),...state.semanticMemory.map(x=>x.id)]);
 if(new Set(operationalIds(s)).size!==operationalIds(s).length)throw Error('Duplicate stored operational identity');
 for(const [index,raw] of changes.entries()){
  const c=operationalChangeSchema.parse(raw),op=c.operation;
  if(c.expectedRevision!==state.revision||c.sourceIds.some(x=>!knownSources.includes(x)))throw Error('Operational revision/provenance mismatch');
  if(neural.test(JSON.stringify(op)))throw Error('Unsupported biological Life State claim');
  const fresh=(key:string)=>{if(allIds.has(key))throw Error('Duplicate operational ID');allIds.add(key);return {id:key,version:1,createdAt:event.at,updatedAt:event.at,sourceEvent:event.id,sources:[...c.sourceIds],disclosure:{...PRIVATE_LIFE}};};
  const touch=(x:{version:number;updatedAt:string;sourceEvent:string;sources:string[]})=>{if(Date.parse(event.at)<Date.parse(x.updatedAt))throw Error('Operational time moved backwards');x.version++;x.updatedAt=event.at;x.sourceEvent=event.id;x.sources=[...c.sourceIds];};
  const evidence=(ids:string[],required=true)=>{if(required&&!ids.length||ids.some(x=>!knownSources.includes(x)))throw Error('Missing or unresolved completion evidence');};
  const relation=(key:string|null)=>{if(key&&!s.relationships.some(x=>x.id===key))throw Error('Unknown relationship');};
  switch(op.op){
   case 'project_create':s.projects.push({...fresh(op.id),title:op.title,summary:op.summary,status:'active'});break;
   case 'project_update':{const x=existing(s.projects,op);if(x.status!=='active')throw Error('Project is inactive');touch(x);x.summary=op.summary;break;}
   case 'project_status':{const x=existing(s.projects,op);transition(x.status,op.status,PROJECT_TRANSITIONS);if(op.status==='completed'&&s.tasks.some(t=>t.projectId===x.id&&!['completed','cancelled'].includes(t.status)))throw Error('Unfinished project tasks');touch(x);x.status=op.status;break;}
   case 'task_create':association(s,op.projectId,null,legacyProjectIds);s.tasks.push({...fresh(op.id),description:op.description,projectId:op.projectId,status:'pending',dueAt:op.dueAt,reviewAt:null,evidenceIds:[]});break;
   case 'task_status':{const x=existing(s.tasks,op);transition(x.status,op.status,TASK_TRANSITIONS);if(op.status!=='cancelled')association(s,x.projectId,null,legacyProjectIds);if(op.status==='deferred'&&!op.reviewAt)throw Error('Deferral review time required');if(op.status!=='deferred'&&op.reviewAt!==null)throw Error('Review time only for deferred task');evidence(op.evidenceIds,['completed','cancelled'].includes(op.status));touch(x);x.status=op.status;x.reviewAt=op.reviewAt;x.evidenceIds=[...op.evidenceIds];break;}
   case 'artifact_create':{association(s,op.projectId,op.taskId,legacyProjectIds);const root=fresh(op.id),vid=op.id+':v1';if(allIds.has(vid))throw Error('Duplicate artifact version');allIds.add(vid);s.artifacts.push({...root,...{projectId:op.projectId,taskId:op.taskId},currentVersionId:vid,versions:[{id:vid,revision:1,content:op.content,at:event.at,sourceEvent:event.id,sources:[...c.sourceIds],supersedes:null,disclosure:{...PRIVATE_LIFE}}]});break;}
   case 'artifact_revise':{const x=existing(s.artifacts,op);association(s,x.projectId,x.taskId,legacyProjectIds);const prior=x.currentVersionId;touch(x);const vid=x.id+':v'+x.version;if(allIds.has(vid)||x.versions.some(v=>v.id===vid))throw Error('Duplicate artifact revision');allIds.add(vid);x.currentVersionId=vid;x.versions.push({id:vid,revision:x.version,content:op.content,at:event.at,sourceEvent:event.id,sources:[...c.sourceIds],supersedes:prior,disclosure:{...PRIVATE_LIFE}});break;}
   case 'interest_add':s.interests.push({...fresh(op.id),topic:op.topic,status:'active'});break;
   case 'interest_update':{const x=existing(s.interests,op);if(x.status!=='active')throw Error('Interest retired');touch(x);x.topic=op.topic;break;}
   case 'interest_retire':{const x=existing(s.interests,op);if(x.status!=='active')throw Error('Interest already retired');touch(x);x.status='retired';break;}
   case 'question_create':association(s,op.projectId,op.taskId,legacyProjectIds);s.questions.push({...fresh(op.id),projectId:op.projectId,taskId:op.taskId,question:op.question,status:'open',evidenceIds:[]});break;
   case 'question_status':{const x=existing(s.questions,op);transition(x.status,op.status,QUESTION_TRANSITIONS);evidence(op.evidenceIds,op.status==='resolved');touch(x);x.status=op.status;x.evidenceIds=[...op.evidenceIds];break;}
   case 'commitment_create':{association(s,op.projectId,op.taskId,legacyProjectIds);relation(op.relationshipId);if(financial.test(op.statement)||/\bon behalf of\b/i.test(op.statement))throw Error('External legal/financial obligation prohibited');s.commitments.push({...fresh(op.id),projectId:op.projectId,taskId:op.taskId,relationshipId:op.relationshipId,purpose:op.purpose,statement:op.statement,scope:'INTERNAL_COMPUTATIONAL',status:'open',reviewAt:op.reviewAt,evidenceIds:[]});break;}
   case 'commitment_status':{const x=existing(s.commitments,op);transition(x.status,op.status,COMMITMENT_TRANSITIONS);if(op.status==='open'&&op.reviewAt===x.reviewAt)throw Error('No commitment change');evidence(op.evidenceIds,op.status==='fulfilled');touch(x);x.status=op.status;x.reviewAt=op.reviewAt;x.evidenceIds=[...op.evidenceIds];break;}
   case 'relationship_create':if(traits.test(op.label))throw Error('Inferred personal traits prohibited');s.relationships.push({...fresh(op.id),label:op.label,context:op.context,consent:op.consent});break;
   case 'relationship_update':{const x=existing(s.relationships,op);touch(x);x.context=op.context;break;}
   case 'assistance_create':association(s,op.projectId,op.taskId,legacyProjectIds);relation(op.relationshipId);s.assistance.push({...fresh(op.id),projectId:op.projectId,taskId:op.taskId,relationshipId:op.relationshipId,question:op.question,status:'pending',responseIds:[],resolutionResponseId:null});break;
   case 'assistance_resolve':{const x=existing(s.assistance,op);if(x.status!=='answered'||!x.responseIds.includes(op.responseId)||!knownSources.includes(op.responseId))throw Error('Assistance resolution requires received response evidence');touch(x);x.status='resolved';x.resolutionResponseId=op.responseId;break;}
   case 'assistance_cancel':{const x=existing(s.assistance,op);if(!['pending','answered'].includes(x.status))throw Error('Assistance terminal');touch(x);x.status='cancelled';break;}
   case 'focus_set':s.focus={mode:op.mode,targetId:op.targetId,at:event.at,sourceEvent:event.id};break;
  }
  const target='id'in op?op.id:op.targetId;const version='expectedVersion'in op?op.expectedVersion:0;
  s.history.push({id:event.id+':op:'+index,at:event.at,sourceEvent:event.id,sourceIds:[...c.sourceIds],operation:op.op,targetId:target,fromVersion:version,toVersion:op.op==='focus_set'?0:version+1,changeHash:digest(c)});
 }
 validateFocus(s);return operationalStateSchema.parse(s);
}
/** Attributed input only: request becomes answered; no proposal/effect or arbitrary state patch. */
export function applyHumanResponse(state:LifeStateV1,raw:unknown,eventId:string):OperationalState{
 const r=humanResponseSchema.parse(raw),s=operational(state);if(r.organismId!==state.organismId||operationalIds(s).includes(r.id))throw Error('Response ownership or duplicate identity');
 const q=s.assistance.find(x=>x.id===r.requestId);if(!q||!['pending','answered'].includes(q.status)||q.relationshipId!==r.relationshipId||Date.parse(r.receivedAt)<Date.parse(q.updatedAt))throw Error('Wrong/terminal request or invalid response time');
 s.responses.push(r);q.responseIds.push(r.id);q.status='answered';q.version++;q.updatedAt=r.receivedAt;q.sourceEvent=eventId;q.sources=[r.id];
 s.history.push({id:eventId+':response',at:r.receivedAt,sourceEvent:eventId,sourceIds:[r.id],operation:'human_response_received',targetId:q.id,fromVersion:q.version-1,toVersion:q.version,changeHash:digest(r)});
 if(s.focus?.mode==='assistance'&&s.focus.targetId===q.id){s.focus={mode:'none',targetId:null,at:r.receivedAt,sourceEvent:eventId};s.history.push({id:eventId+':focus',at:r.receivedAt,sourceEvent:eventId,sourceIds:[r.id],operation:'answered_wait_focus_cleared',targetId:q.id,fromVersion:0,toVersion:0,changeHash:digest(r)});}
 validateFocus(s);return operationalStateSchema.parse(s);
}

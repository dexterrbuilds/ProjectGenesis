/** Derived private recall. Original records remain authoritative; no biological interpretation. */
import {operational,humanResponseSchema,operationalChangeSchema} from './operations.ts';
import {z} from 'zod';
import {digest} from './identity.ts';
import {changeSchema} from './life-state.ts';
import type {Organism} from '../contracts.ts';
import type {LifeStateV1,BiologicalObservation} from './contracts.ts';
export const RECALL_POLICY={version:'memory-disclosure-v1',internal:true,provider:false,public:false} as const;
export type MemoryArchive={legacy:unknown[];decisions:unknown[];episodes:unknown[];inputs?:unknown[];complete:boolean};
export const EMPTY_ARCHIVE:MemoryArchive={legacy:[],decisions:[],episodes:[],complete:true};
export type MemoryQuery={referenceIds:string[];projectIds:string[];taskIds:string[];subjects:string[];text:string};
export const EMPTY_QUERY:MemoryQuery={referenceIds:[],projectIds:[],taskIds:[],subjects:[],text:''};
export type MemoryReview={id:string;sourceHash:string;organismId:string;reference:string;internal:boolean;provider:boolean;public:boolean;operatorOnly:boolean};
export type MemoryLimits={episodes:number;assertions:number;artifacts:number;totalBytes:number;excerptBytes:number};
export const MEMORY_LIMITS:MemoryLimits={episodes:3,assertions:3,artifacts:1,totalBytes:4500,excerptBytes:600};
type Source={id:string;kind:string;at:string|null;hash:string;hashScope:'retrieval-source-projection';recordId:string;internal:boolean;provider:boolean;public:boolean};
export type MemoryCandidate={id:string;kind:'legacy_episode'|'episode'|'assertion'|'artifact';occurredAt:string|null;sourceIds:string[];visibility:'private'|'public';disclosure:{internal:boolean;provider:boolean;public:boolean;operatorOnly:boolean;basis:string};projectIds:string[];taskIds:string[];subjects:string[];excerpt:string;provenance:Source[];interpretation:'recorded_past_experience'|'unverified_assertion'|'past_artifact';confidence:number|null;author:string|null;supersedes:string|null;contradictions:string[];pendingAtRecording:boolean;trust:'untrusted';limitations:string[]};
export type MemorySelection={version:'memory-retrieval-v1';organismId:string;revision:number;eventId:string;audience:'internal'|'provider';queryHash:string;limits:MemoryLimits;items:MemoryCandidate[];manifest:{discovered:number;eligible:number;selectedIds:string[];excluded:{id:string;reason:string}[];reasons:Record<string,string>;bytes:number;discoveryComplete:boolean;selectionHash:string}};
const date=z.string().datetime({offset:true}).refine(s=>{const d=new Date(s);return Number.isFinite(d.getTime())&&d.toISOString().slice(0,10)===s.slice(0,10);});
const id=z.string().min(1).max(300).refine(s=>!['__proto__','constructor','prototype'].includes(s));
const refs=z.array(id).max(50);
const querySchema=z.object({referenceIds:refs,projectIds:refs,taskIds:refs,subjects:refs,text:z.string().max(2000)}).strict();
const reviewSchema=z.object({id,sourceHash:z.string().regex(/^[a-f0-9]{64}$/),organismId:id,reference:id,internal:z.boolean(),provider:z.boolean(),public:z.boolean(),operatorOnly:z.boolean()}).strict();
const legacySchema=z.object({id,at:date,text:z.string().min(1),sourceDecision:id,salience:z.number()});
const episodeSchema=z.object({schemaVersion:z.literal(1),id,organismId:id,at:date,kind:z.literal('episode'),source:id,visibility:z.enum(['private','public']),record:z.object({outcomeStatus:z.enum(['abstained','deferred','pending','failed','local','denied','recorded']),actionStatus:z.enum(['local_saved','not_executed']),lifeChanges:z.array(z.unknown()).max(20).optional(),localArtifact:z.string().optional(),artifactOmitted:z.boolean().optional(),recall:z.unknown().optional()}).passthrough()});
const decisionSchema=z.object({id,at:date,cycle:z.number().int().positive(),schemaVersion:z.literal(2).optional(),organismId:id.optional(),event:z.object({id,observedAt:date,kind:z.literal('digital-event'),source:z.string(),recall:querySchema.optional()}).optional(),biological:z.object({id,observedAt:date,status:z.string(),executedThisCycle:z.literal(false)}).optional(),outcome:z.object({status:z.string()}).optional(),action:z.object({status:z.string(),artifact:z.string().optional()}).optional(),proposal:z.object({projectId:id.nullable(),taskId:id.nullable()}).nullable().optional(),memory:z.object({episode:z.object({id}),changes:z.array(z.unknown())}).optional()});
export const credentialLike=(s:string)=>/\b(api[_-]?key|password|secret|bearer|private[_-]?key|authorization\s*:)|sk-[a-z0-9_-]{12,}|-----BEGIN .*PRIVATE KEY|\b(?:postgres(?:ql)?|https?):\/\/[^\s/]+:[^\s/@]+@/i.test(s);
const cmp=(a:string,b:string)=>a<b?-1:a>b?1:0;
export function utf8Excerpt(text:string,max:number){let out='',n=0;for(const c of text){const size=Buffer.byteLength(c);if(n+size>max)break;out+=c;n+=size;}return out;}
const safeTime=(at:string,now:string,birth:string)=>Date.parse(at)<=Date.parse(now)&&Date.parse(at)>=Date.parse(birth);
/** Reviews are trusted operator/config inputs, never taken from planner arguments or retrieved text. */
export function retrieveMemory(o:Organism,life:LifeStateV1,bio:BiologicalObservation,archive:MemoryArchive=EMPTY_ARCHIVE,query:MemoryQuery=EMPTY_QUERY,audience:'internal'|'provider'='internal',limits:MemoryLimits=MEMORY_LIMITS,reviews:MemoryReview[]=[]):MemorySelection{
 if(o.id!==life.organismId||bio.organismId!==o.id||!bio.input||!date.safeParse(bio.input.observedAt).success||!date.safeParse(o.bornAt).success)throw Error('Mandatory memory identity/event provenance invalid');
 query=querySchema.parse(query);
 if(credentialLike(JSON.stringify(query)))throw Error('Credential-like recall query refused');
 for(const [k,v] of Object.entries(limits))if(!Number.isSafeInteger(v)||v<0||v>(k==='totalBytes'?12000:k==='excerptBytes'?2000:10))throw Error('Invalid memory budget');
 if(Object.keys(limits).sort().join(',')!=='artifacts,assertions,episodes,excerptBytes,totalBytes')throw Error('Incomplete memory limits');
 const now=bio.input.observedAt,excluded:{id:string;reason:string}[]=[],reasons:Record<string,string>=Object.create(null);
 const sources=new Map<string,Source>(),candidates:MemoryCandidate[]=[],invalidSources=new Set<string>();
 const exclude=(key:string,reason:string)=>excluded.push({id:key,reason});
 const addSource=(s:Source)=>{if(sources.has(s.id)){sources.delete(s.id);invalidSources.add(s.id);}else if(!invalidSources.has(s.id))sources.set(s.id,s);};
 const reviewed=new Map<string,MemoryReview>();for(const raw of reviews){const r=reviewSchema.parse(raw);if(r.organismId!==o.id||reviewed.has(r.id))throw Error('Disclosure review identity/duplicate');reviewed.set(r.id,r);}
 const disclosure=(key:string,raw:unknown,builtin:boolean,_visibility:'public'|'private')=>{void _visibility;
  const r=reviewed.get(key);if(r&&r.sourceHash!==digest(raw))throw Error('Stale disclosure review');
  return r?{internal:r.internal,provider:r.provider,public:r.public,operatorOnly:r.operatorOnly,basis:'source-bound-operator-review:'+r.reference}:{internal:builtin,provider:false,public:false,operatorOnly:false,basis:builtin?'memory-disclosure-v1':'missing-disclosure'};
 };
 const source=(key:string,kind:string,at:string|null,recordId:string,raw:unknown,d:{internal:boolean;provider:boolean;public:boolean}):Source=>({id:key,kind,at,recordId,hash:digest(raw),hashScope:'retrieval-source-projection',internal:d.internal,provider:d.provider,public:d.public});
 const current={internal:true,provider:true,public:false};
 addSource(source(bio.input.id,'current_event',bio.input.observedAt,bio.input.id,bio.input,current));
 addSource(source(bio.id,'biological_provenance_only',bio.observedAt,bio.id,{id:bio.id,status:bio.status,sourceRecordedAt:bio.sourceRecordedAt,snapshot:bio.snapshotBefore},current));
 for(const e of life.environment){if(!id.safeParse(e.id).success||!date.safeParse(e.at).success||!safeTime(e.at,now,o.bornAt)||e.visibility!=='public'||credentialLike(JSON.stringify(e)))continue;addSource(source(e.id,'environment',e.at,e.id,e,current));}
 const decisions=new Map<string,z.infer<typeof decisionSchema>>();
 for(const raw of archive.decisions){const p=decisionSchema.safeParse(raw);if(!p.success){continue;}const d=p.data;if(!safeTime(d.at,now,o.bornAt)||decisions.has(d.id)){invalidSources.add(d.id);decisions.delete(d.id);continue;}if(!invalidSources.has(d.id))decisions.set(d.id,d);}
 const base=(key:string,kind:MemoryCandidate['kind'],at:string|null,text:string,d:MemoryCandidate['disclosure']):MemoryCandidate=>({id:key,kind,occurredAt:at,sourceIds:[],visibility:'private',disclosure:d,projectIds:[],taskIds:[],subjects:[],excerpt:utf8Excerpt(text,limits.excerptBytes),provenance:[],interpretation:kind==='assertion'?'unverified_assertion':kind==='artifact'?'past_artifact':'recorded_past_experience',confidence:null,author:null,supersedes:null,contradictions:[],pendingAtRecording:false,trust:'untrusted',limitations:kind==='legacy_episode'?['Historical computational record; legacy decoder labels are not biological action authority.']:['Past record or unverified assertion, not a current observation.']});
 const legacy=archive===EMPTY_ARCHIVE?o.memory:archive.legacy;
 for(const [i,raw] of legacy.entries()){
  const p=legacySchema.safeParse(raw),key=p.success?p.data.id:'legacy-invalid-'+i;
  if(!p.success){exclude(key,'malformed legacy memory');continue;}const m=p.data,d=decisions.get(m.sourceDecision);
  if(!d||d.schemaVersion!==undefined||d.at!==m.at||!safeTime(m.at,now,o.bornAt)){exclude(key,'missing or inconsistent legacy decision provenance');continue;}
  if(credentialLike(JSON.stringify(m))){exclude(key,'credential-like content');continue;}
  let dis;try{dis=disclosure(key,raw,false,'private');}catch{exclude(key,'stale disclosure review');continue;}
  const s=source(key,'legacy_memory',m.at,m.id,raw,dis),parent=source(d.id,'legacy_decision',d.at,d.id,d,dis);addSource(s);addSource(parent);
  const c=base(key,'legacy_episode',m.at,m.text,dis);c.sourceIds=[m.id,d.id];c.provenance=[s,parent];candidates.push(c);
 }
 for(const [i,raw] of archive.episodes.entries()){
  const p=episodeSchema.safeParse(raw),key=p.success?p.data.id:'episode-invalid-'+i;
  if(!p.success){exclude(key,'malformed episode');continue;}const e=p.data,d=decisions.get(e.source);
  if(e.organismId!==o.id||!safeTime(e.at,now,o.bornAt)||!d||d.schemaVersion!==2||d.organismId!==o.id||d.at!==e.at||d.memory?.episode.id!==e.id||d.outcome?.status!==e.record.outcomeStatus||d.action?.status!==e.record.actionStatus||!d.event||!d.biological||!safeTime(d.event.observedAt,now,o.bornAt)||!safeTime(d.biological.observedAt,now,o.bornAt)){exclude(key,'broken episode/decision provenance');continue;}
  const built=digest(e.record.recall??null)===digest(RECALL_POLICY);
  let dis;try{dis=disclosure(key,raw,built,e.visibility);}catch{exclude(key,'stale disclosure review');continue;}
  const refs=[source(e.id,'episode',e.at,e.id,raw,dis),source(d.id,'decision',d.at,d.id,d,dis),source(d.event.id,'past_event',d.event.observedAt,d.id,d.event,dis),source(d.biological.id,'biological_provenance_only',d.biological.observedAt,d.id,d.biological,dis)];
  if(credentialLike(JSON.stringify(refs))){exclude(key,'credential-like provenance');continue;}
  refs.forEach(addSource);
  const c=base(e.id,'episode',e.at,JSON.stringify({outcome:e.record.outcomeStatus,action:e.record.actionStatus}),dis);c.visibility=e.visibility;c.sourceIds=refs.map(s=>s.id);c.provenance=refs;c.projectIds=d.proposal?.projectId?[d.proposal.projectId]:[];c.taskIds=d.proposal?.taskId?[d.proposal.taskId]:[];c.subjects=d.event.recall?.subjects??[];c.pendingAtRecording=e.record.outcomeStatus==='pending'||e.record.outcomeStatus==='deferred';candidates.push(c);
  if(e.record.artifactOmitted)exclude(e.id+':artifact','artifact source exceeds discovery byte bound');
  if(e.record.localArtifact!==undefined){const key=e.id+':artifact';
   if(e.record.actionStatus!=='local_saved'||d.action?.artifact!==e.record.localArtifact){exclude(key,'corrupted artifact reference');continue;}
   if(credentialLike(e.record.localArtifact)){exclude(key,'credential-like artifact');continue;}
   const a={...base(key,'artifact',e.at,e.record.localArtifact,dis),sourceIds:[e.id,d.id],provenance:refs.slice(0,2),projectIds:c.projectIds,taskIds:c.taskIds,visibility:e.visibility};candidates.push(a);addSource(source(key,'artifact',e.at,e.id,{text:e.record.localArtifact},dis));
  }
 }
 // Operational references are supported by the stored, validated episode changes; never inferred from prose.
 const opState=operational(life);
 const validEpisodes=new Map(archive.episodes.map(raw=>episodeSchema.safeParse(raw)).filter(p=>p.success).map(p=>[p.data!.id,p.data!]));
 for(const c of candidates.filter(c=>c.kind==='episode')){
  const e=validEpisodes.get(c.id)!;
  for(const raw of e.record.lifeChanges??[]){const p=operationalChangeSchema.safeParse(raw);if(!p.success){continue;}const op=p.data.operation;
   const target='id'in op?op.id:op.targetId;
   if(target)c.sourceIds.push(target);
   if('id'in op){
    if(op.op.startsWith('project_'))c.projectIds.push(op.id);
    if(op.op.startsWith('task_'))c.taskIds.push(op.id);
    const owner=[...opState.tasks,...opState.artifacts,...opState.questions,...opState.commitments,...opState.assistance].find(x=>x.id===op.id);
    if(owner?.projectId)c.projectIds.push(owner.projectId);
    if(owner&&'taskId'in owner&&owner.taskId)c.taskIds.push(owner.taskId);
   }
   if('projectId'in op&&op.projectId)c.projectIds.push(op.projectId);
   if('taskId'in op&&op.taskId)c.taskIds.push(op.taskId);
   for(const key of ['relationshipId','responseId'] as const)if(key in op&&typeof op[key as keyof typeof op]==='string')c.sourceIds.push(op[key as keyof typeof op] as string);
  }
 }
 for(const raw of archive.inputs??[]){
  const p=z.object({schemaVersion:z.literal(1),id,organismId:id,at:date,kind:z.literal('administrative'),source:id,visibility:z.literal('private'),record:z.object({type:z.literal('human_response'),response:humanResponseSchema,responseHash:z.string()})}).safeParse(raw);
  if(!p.success){exclude('human-input','malformed attributed input');continue;}const e=p.data,r=e.record.response,q=opState.assistance.find(q=>q.id===r.requestId);
  if(e.organismId!==o.id||r.organismId!==o.id||e.id!==r.id+':input'||e.source!==r.id||e.at!==r.receivedAt||!safeTime(e.at,now,o.bornAt)||e.record.responseHash!==digest(r)||!q?.responseIds.includes(r.id)||!opState.responses.some(x=>digest(x)===digest(r))||credentialLike(JSON.stringify(r))){exclude(e.id,'broken or unsafe human-input provenance');continue;}
  const dis={internal:true,provider:false,public:false,operatorOnly:false,basis:'explicit internal-only attributed input'};
  const refs=[source(e.id,'attributed_human_input',e.at,e.id,e,dis),source(r.id,'untrusted_human_response',r.receivedAt,e.id,r,dis)];refs.forEach(addSource);
  const c=base(r.id,'episode',r.receivedAt,r.content,dis);c.sourceIds=[r.id,e.id,q.id];c.provenance=refs;c.projectIds=q.projectId?[q.projectId]:[];c.taskIds=q.taskId?[q.taskId]:[];c.author=r.respondentRef;c.limitations.push('Human-supplied untrusted input; receipt is not truth, approval or an instruction to execute.');candidates.push(c);
 }
 // Mutable entity IDs are relevance keys, not immutable evidence for semantic assertions.
 for(const a of opState.artifacts){
  if(a.versions.length!==a.version||a.currentVersionId!==a.versions.at(-1)?.id){exclude(a.id,'corrupted artifact revision chain');continue;}
  for(const [index,v] of a.versions.entries()){
   if(v.id!==a.id+':v'+(index+1)||v.revision!==index+1||v.supersedes!==(index?a.versions[index-1].id:null)){exclude(a.id,'corrupted artifact revision chain');break;}
   const e=validEpisodes.get(v.sourceEvent),parent=sources.get(v.sourceEvent);
   const valid=(e?.record.lifeChanges??[]).some(raw=>{const p=operationalChangeSchema.safeParse(raw);return p.success&&['artifact_create','artifact_revise'].includes(p.data.operation.op)&&'id'in p.data.operation&&p.data.operation.id===a.id&&'content'in p.data.operation&&p.data.operation.content===v.content&&digest(p.data.sourceIds)===digest(v.sources);});
   if(!valid||!parent||!parent.internal||!safeTime(v.at,now,o.bornAt)||v.at!==e?.at||credentialLike(v.content)){exclude(v.id,'broken artifact version provenance');continue;}
   const dis={internal:true,provider:false,public:false,operatorOnly:false,basis:'private versioned local artifact'};
   const src=source(v.id,'artifact_version',v.at,v.sourceEvent,v,dis);addSource(src);
   if(v.id!==a.currentVersionId&&!query.referenceIds.includes(v.id)){exclude(v.id,'superseded artifact version; explicit reference required');continue;}
   const c=base(v.id,'artifact',v.at,v.content,dis);c.sourceIds=[a.id,v.id,v.sourceEvent];c.provenance=[src,parent];c.projectIds=a.projectId?[a.projectId]:[];c.taskIds=a.taskId?[a.taskId]:[];c.supersedes=v.supersedes;candidates.push(c);
  }
 }
 const assertions=new Map<string,z.infer<typeof changeSchema> & {kind:'assertion'}>();
 for(const [i,a] of life.semanticMemory.entries()){const p=changeSchema.safeParse({kind:'assertion',assertion:a});if(!p.success||p.data.kind!=='assertion'||!id.safeParse(a.id).success||a.sources.length>50||a.contradictions.length>50||a.sources.some(s=>!id.safeParse(s).success)){exclude('assertion-invalid-'+i,'malformed assertion');continue;}if(assertions.has(a.id)){invalidSources.add(a.id);assertions.delete(a.id);exclude(a.id,'duplicate assertion');}else if(!invalidSources.has(a.id))assertions.set(a.id,p.data);}
 const resolving=new Set<string>(),resolved=new Map<string,MemoryCandidate>();
 const resolve=(key:string,depth=0):MemoryCandidate|null=>{
  if(resolved.has(key))return resolved.get(key)!;const a=assertions.get(key)?.assertion;if(!a)return null;
  if(depth>32||resolving.has(key)){exclude(key,'cyclic or excessive provenance');return null;}resolving.add(key);
  const done=(c:MemoryCandidate|null)=>{resolving.delete(key);return c;};
  if(credentialLike(JSON.stringify(a))){exclude(key,'credential-like assertion');return done(null);}
  if([a.supersedes,...a.contradictions].filter(Boolean).some(x=>x===key||!assertions.has(x!))){exclude(key,'invalid supersession/contradiction');return done(null);}
  // Supersession must be an acyclic chain, independently of source dependencies.
  const chain=new Set([key]);let parent=a.supersedes;while(parent){if(chain.has(parent)){exclude(key,'cyclic supersession');return done(null);}chain.add(parent);parent=assertions.get(parent)?.assertion.supersedes??null;}
  const refs:Source[]=[];
  for(const s of a.sources){if(assertions.has(s))resolve(s,depth+1);const r=sources.get(s);if(!r||invalidSources.has(s)){exclude(key,'unresolved assertion source');return done(null);}refs.push(r);}
  const dis={internal:refs.every(s=>s.internal),provider:false,public:false,operatorOnly:false,basis:'source-resolution; assertion remains unverified'};
  let override;try{override=disclosure(key,a,false,'private');}catch{exclude(key,'stale disclosure review');return done(null);}
  // An assertion cannot expand disclosure of its underlying sources.
  if(reviewed.has(key)){dis.internal&&=override.internal;dis.provider=override.provider&&refs.every(s=>s.provider);dis.operatorOnly=override.operatorOnly;}
  const c=base(key,'assertion',null,a.text,dis);c.sourceIds=[...a.sources];c.provenance=refs;c.confidence=a.confidence;c.author=a.author;c.supersedes=a.supersedes;c.contradictions=[...a.contradictions];
  // Assertion creation time is not in legacy schema; do not substitute source time.
  resolved.set(key,c);addSource(source(key,'unverified_assertion',null,key,a,dis));return done(c);
 };
 for(const key of [...assertions.keys()].sort(cmp)){const c=resolve(key);if(c)candidates.push(c);}
 for(const c of candidates.filter(c=>c.kind==='assertion')){c.contradictions=[...new Set([...c.contradictions,...candidates.filter(x=>x.kind==='assertion'&&x.contradictions.includes(c.id)).map(x=>x.id)])].sort(cmp);}
 const superseded=new Set(candidates.filter(c=>c.kind==='assertion'&&c.disclosure[audience]&&!c.disclosure.operatorOnly).map(c=>c.supersedes).filter(Boolean));
 const duplicates=new Set<string>();const counts=new Map<string,number>();for(const c of candidates)counts.set(c.id,(counts.get(c.id)??0)+1);for(const [key,n]of counts)if(n>1)duplicates.add(key);
 const words=(s:string)=>new Set(s.toLowerCase().match(/[\p{L}\p{N}_-]{3,}/gu)??[]),terms=words(query.text);
 const eligible: {c:MemoryCandidate;rank:number[]}[]=[];
 for(const c of candidates){
  if(credentialLike(JSON.stringify(c))){exclude(c.id,'credential-like candidate');continue;}
  if(duplicates.has(c.id)||invalidSources.has(c.id)){exclude(c.id,'duplicate source identity');continue;}
  if(c.disclosure.operatorOnly||!c.disclosure[audience]){exclude(c.id,c.disclosure.operatorOnly?'operator-only':`not admitted for ${audience}: ${c.disclosure.basis}`);continue;}
  if(c.provenance.some(s=>invalidSources.has(s.id)||!s[audience])){exclude(c.id,'source disclosure or identity unresolved');continue;}
  if(superseded.has(c.id)){exclude(c.id,'superseded assertion');continue;}
  const direct=query.referenceIds.some(r=>r===c.id||c.sourceIds.includes(r));const project=c.projectIds.some(r=>query.projectIds.includes(r)),task=c.taskIds.some(r=>query.taskIds.includes(r)),subject=c.subjects.some(r=>query.subjects.includes(r));
  const lexical=[...words(c.excerpt)].filter(w=>terms.has(w)).length;
  const recent=c.occurredAt!==null&&Date.parse(now)-Date.parse(c.occurredAt)<=30*86400000;
  if(!direct&&!project&&!task&&!subject&&!lexical&&!c.pendingAtRecording&&c.kind!=='assertion'&&!recent){exclude(c.id,'no structured/lexical/recency relevance');continue;}
  eligible.push({c,rank:[+direct,+task,+project,+subject,Math.min(lexical,10),+c.pendingAtRecording,+(c.kind==='assertion'),c.occurredAt?Date.parse(c.occurredAt):0]});
  reasons[c.id]=direct?'direct reference':task?'same task':project?'same project':subject?'same subject':lexical?'lexical token overlap':c.pendingAtRecording?'pending recorded outcome':c.kind==='assertion'?'current unverified assertion':'recent recorded experience';
 }
 eligible.sort((a,b)=>{for(let i=0;i<a.rank.length;i++)if(a.rank[i]!==b.rank[i])return b.rank[i]-a.rank[i];return cmp(a.c.id,b.c.id);});
 const items:MemoryCandidate[]=[],used={episodes:0,assertions:0,artifacts:0};const fingerprints=new Set<string>();
 for(const {c} of eligible){const group=c.kind==='artifact'?'artifacts':c.kind==='assertion'?'assertions':'episodes';const fp=digest({kind:c.kind,excerpt:c.excerpt,sources:c.sourceIds,supersedes:c.supersedes,contradictions:c.contradictions,confidence:c.confidence,author:c.author});
  if(fingerprints.has(fp)){exclude(c.id,'duplicate derived content/provenance');continue;}
  if(used[group]>=limits[group]||Buffer.byteLength(JSON.stringify([...items,c]))>limits.totalBytes){exclude(c.id,'selection budget: whole optional item dropped');continue;}
  items.push(c);used[group]++;fingerprints.add(fp);
 }
 excluded.sort((a,b)=>cmp(a.id,b.id)||cmp(a.reason,b.reason));
 return {version:'memory-retrieval-v1',organismId:o.id,revision:life.revision,eventId:bio.input.id,audience,queryHash:digest(query),limits:{...limits},items,manifest:{discovered:legacy.length+archive.episodes.length+(archive.inputs?.length??0)+life.semanticMemory.length+candidates.filter(c=>c.kind==='artifact').length,eligible:eligible.length,selectedIds:items.map(i=>i.id),excluded,reasons,bytes:Buffer.byteLength(JSON.stringify(items)),discoveryComplete:archive.complete,selectionHash:digest(items)}};
}

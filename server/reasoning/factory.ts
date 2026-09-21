import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {digest} from '../../core/v2/identity.ts';
import {admissionSchema,SCHEMA_HASH,PLANNER_HASH,ReasoningError,replySchema,type Admission,type Reply,type Cancellation} from './contracts.ts';
const fileHash=(p:string)=>createHash('sha256').update(readFileSync(new URL(p,import.meta.url))).digest('hex');
export function implementationHashes(){return {adapter:digest({factory:fileHash('./factory.ts'),contract:fileHash('./contracts.ts')}),counter:fileHash('./request.ts')};}
export function validateAdmission(raw:unknown):Admission{
 const a=admissionSchema.parse(raw),h=implementationHashes();if(a.schemaHash!==SCHEMA_HASH||a.plannerHash!==PLANNER_HASH||a.adapter.hash!==h.adapter||a.counting.hash!==h.counter||a.adapter.id!==(a.provider==='fixture'?'fixture-v1':'json-gateway-v1'))throw new ReasoningError('ADMISSION_MISMATCH');
 if(a.rateCard.hash!==digest({currency:a.rateCard.currency,categories:a.rateCard.categories})||new Set(a.rateCard.categories.map(c=>c.id)).size!==a.rateCard.categories.length||!a.rateCard.categories.some(c=>c.id==='input')||!a.rateCard.categories.some(c=>c.id==='output'))throw new ReasoningError('ADMISSION_MISMATCH');
 if(a.provider==='json-gateway'){if(!a.secretReference.startsWith('env:'))throw new ReasoningError('CONFIGURATION');const u=new URL(a.endpoint??'invalid:');if(u.protocol!=='https:'||u.username||u.password||u.search||u.hash||u.hostname==='localhost'||/^[\d:[\]]/.test(u.hostname)||/\.(local|internal)$/.test(u.hostname))throw new ReasoningError('CONFIGURATION');}else if(a.endpoint!==null||!a.secretReference.startsWith('fixture:'))throw new ReasoningError('CONFIGURATION');
 if(a.perAttemptMicros>a.perCycleMicros||a.perCycleMicros>a.dailyMicros||a.timeoutMs>25000||a.counting.maxWireBytes>262144||Date.parse(a.expiresAt)<=Date.parse(a.effectiveAt))throw new ReasoningError('CONFIGURATION');return a;
}
export type Adapter={send:(wire:string,secret:string,signal:AbortSignal)=>Promise<Reply>;cancel:()=>Promise<Cancellation>};
export type FixtureScenario='valid'|'abstain'|'defer'|'assistance'|'malformed'|'schema'|'before_timeout'|'timeout'|'network'|'5xx'|'rate_limit'|'unknown_usage'|'wrong_admission'|'secret_echo'|'cancel_confirmed'|'cancel_uncertain'|'excess_usage'|'extra_usage'|'duplicate_response'|'unknown_error';
/** Registry-selected implementations only. No API accepts caller-supplied code hashes/callbacks. */
export function resolveAdapter(a:Admission,fixture:boolean,scenario:FixtureScenario='abstain',onFixtureSend?:()=>void):Adapter{
 validateAdmission(a);if(a.provider==='fixture'){
  if(!fixture)throw new ReasoningError('ADMISSION_MISMATCH');return {cancel:async()=>scenario==='cancel_confirmed'?'SUPPORTED_CONFIRMED':'SUPPORTED_UNCONFIRMED',send:async(wire,secret,signal)=>{
   onFixtureSend?.();const w=JSON.parse(wire),context=JSON.parse(w.context),base={schemaVersion:2,id:'fixture-proposal',contextHash:w.contextHash,kind:'ABSTAIN',intent:'No local action',taskId:null,projectId:null,tool:null,arguments:{text:''},citations:[],rationale:'Fixture bounded explanation',cost:{namespace:'OPERATIONAL',maxMicros:0},uncertainty:'Fixture',deferUntil:null,assistance:null,changes:[],planner:'provider:'+a.provider+':'+a.model};
   if(scenario==='before_timeout')throw new ReasoningError('TIMEOUT_BEFORE_DISPATCH');
   if(['timeout','cancel_confirmed','cancel_uncertain'].includes(scenario))return new Promise((_,reject)=>{if(signal.aborted)reject(new ReasoningError('TIMEOUT_AFTER_DISPATCH'));else signal.addEventListener('abort',()=>reject(new ReasoningError('TIMEOUT_AFTER_DISPATCH')),{once:true});});
   if(scenario==='unknown_error')throw Error(secret);
   if(scenario==='network')throw new ReasoningError('NETWORK_AFTER_DISPATCH');if(scenario==='5xx')throw new ReasoningError('PROVIDER_5XX');if(scenario==='rate_limit')throw new ReasoningError('RATE_LIMIT');
   if(scenario==='valid'){base.kind='PROPOSAL';Object.assign(base,{tool:'local_reflection',arguments:{text:'Fixture local note'}});}if(scenario==='defer'){base.kind='DEFER';Object.assign(base,{deferUntil:new Date(Date.parse(context.currentEvent.observedAt)+60000).toISOString()});}if(scenario==='assistance'){base.kind='REQUEST_ASSISTANCE';Object.assign(base,{assistance:'Fixture request for human input'});}
   const usage=Object.fromEntries(a.rateCard.categories.map(c=>[c.id,Math.min(c.maximumUnits,c.id==='input'?10:c.id==='output'?5:0)]));
   if(scenario==='excess_usage')usage.input=12001;if(scenario==='extra_usage')usage.unreviewed=1;
   return {responseId:scenario==='duplicate_response'?'fixture-shared-response':'fixture-response:'+w.contextHash,requestId:'fixture-request:'+w.contextHash,admissionHash:scenario==='wrong_admission'?'0'.repeat(64):digest(a),model:a.model,structured:scenario==='malformed'?'{invalid':scenario==='schema'?{...base,unknown:true}:scenario==='secret_echo'?{...base,rationale:secret}:base,usage:scenario==='unknown_usage'?null:usage};
  }};
 }
 return {cancel:async()=> 'SUPPORTED_UNCONFIRMED',send:async(wire,secret,signal)=>{
  try{const response=await fetch(a.endpoint!,{method:'POST',redirect:'error',signal,headers:{'content-type':'application/json',authorization:'Bearer '+secret},body:wire});if(!response.ok)throw new ReasoningError(response.status===401||response.status===403?'AUTHENTICATION':response.status===429?'RATE_LIMIT':'PROVIDER_5XX');
   const reader=response.body?.getReader();if(!reader)throw new ReasoningError('MALFORMED_RESPONSE');let bytes=0;const chunks:Uint8Array[]=[];while(true){const r=await reader.read();if(r.done)break;bytes+=r.value.length;if(bytes>65536){await reader.cancel();throw new ReasoningError('MALFORMED_RESPONSE');}chunks.push(r.value);}try{return replySchema.parse(JSON.parse(Buffer.concat(chunks).toString('utf8')));}catch{throw new ReasoningError('MALFORMED_RESPONSE');}
  }catch(e){throw e instanceof ReasoningError?e:new ReasoningError(signal.aborted?'CANCEL_UNCONFIRMED':'NETWORK_AFTER_DISPATCH');}
 }};
}

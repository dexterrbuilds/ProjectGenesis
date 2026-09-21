import {digest} from '../../core/v2/identity.ts';
import type {WorkingContext} from '../../core/v2/contracts.ts';
import type {CycleFence} from '../commit-v2.ts';
import {INSTRUCTIONS,OUTPUT_SCHEMA,SCHEMA_HASH,PLANNER_HASH,ReasoningError,type Admission} from './contracts.ts';
/** The exact string counted is the exact UTF-8 HTTP body sent. Auth header is never part of context/accounting persistence. */
export function completeWire(a:Admission,c:WorkingContext){return JSON.stringify({format:a.format,model:a.model,plannerIdentity:`provider:${a.provider}:${a.model}`,admissionHash:digest(a),instructions:INSTRUCTIONS,context:c.text,contextHash:c.hash,outputSchema:OUTPUT_SCHEMA,reasoning:a.reasoning,maxOutputTokens:a.maximumOutputTokens,billableUnitCeilings:Object.fromEntries(a.rateCard.categories.map(k=>[k.id,k.maximumUnits])),maximumCostMicros:a.perAttemptMicros,automaticRetries:0,tools:[],store:false});}
export function cost(a:Admission,usage:Record<string,number>){
 const keys=Object.keys(usage);if(keys.length!==a.rateCard.categories.length||keys.some(k=>!a.rateCard.categories.some(c=>c.id===k)))throw new ReasoningError('USAGE_UNKNOWN');let sum=0n;
 for(const c of a.rateCard.categories){const n=usage[c.id];if(!Number.isSafeInteger(n)||n<0||n>c.maximumUnits)throw new ReasoningError('USAGE_UNKNOWN');sum+=(BigInt(n)*BigInt(c.microsNumerator)+BigInt(c.denominator)-1n)/BigInt(c.denominator);}if(sum>BigInt(Number.MAX_SAFE_INTEGER))throw new ReasoningError('USAGE_UNKNOWN');return Number(sum);
}
export function accountWire(a:Admission,wire:string,ceiling:number){
 const bytes=Buffer.byteLength(wire);if(bytes>a.counting.maxWireBytes||a.counting.strategy==='PROVIDER_REPORTED_ONLY')throw new ReasoningError('CONFIGURATION');
 const input=a.counting.strategy==='CONSERVATIVE_ESTIMATOR'?bytes:a.counting.inputBound;
 const category=a.rateCard.categories.find(k=>k.id==='input')!,output=a.rateCard.categories.find(k=>k.id==='output')!;
 if(input>a.maximumInputTokens||category.maximumUnits<input||output.maximumUnits<a.maximumOutputTokens)throw new ReasoningError('CONFIGURATION');
 const maxima=Object.fromEntries(a.rateCard.categories.map(c=>[c.id,c.maximumUnits])),reservation=cost(a,maxima);
 if(reservation>a.perAttemptMicros||reservation>a.perCycleMicros||reservation>ceiling)throw new ReasoningError('CONFIGURATION');return {bytes,input,reservation,maxima};
}
export function buildRequest(a:Admission,c:WorkingContext,f:CycleFence,at:string){
 if(c.hash!==digest(c.text)||c.manifest.disclosure?.audience!=='PROVIDER'||!c.manifest.disclosure.binding.installed)throw new ReasoningError('ADMISSION_MISMATCH');
 const wire=completeWire(a,c),{bytes,input,reservation,maxima}=accountWire(a,wire,c.permission.maxCostMicros);
 const request={version:1,organismId:c.organismId,cycleId:f.cycleId,eventId:JSON.parse(c.text).currentEvent.id,contextHash:c.hash,disclosureHash:digest(c.manifest.disclosure),runtimeHash:a.runtimeHash,constitutionHash:a.constitutionHash,policyHash:a.policyHash,permissionHash:digest(c.permission),executionAuthorityHash:digest(JSON.parse(c.text).critical?.oneShotAuthority??JSON.parse(c.text).critical?.continuousAuthority??null),admissionId:a.id,admissionHash:digest(a),plannerHash:PLANNER_HASH,schemaHash:SCHEMA_HASH,requestedAt:at,timeoutMs:a.timeoutMs,maximumAttempts:1,reservationMicros:reservation,wire,wireHash:digest(wire),accounting:{strategy:a.counting.strategy,bytes,inputBound:input,maximumUnits:maxima,evidence:a.counting.evidence}};
 return {...request,hash:digest(request)};
}
export type ReasoningRequest=ReturnType<typeof buildRequest>;

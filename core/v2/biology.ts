import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import data from '../../data/connectome.json' with {type:'json'};
import { CElegansBrain } from '../brain/celegans.ts';
import type { BiologicalObservation, BiologicalObservationAdapterV2, ObservationInput, SnapshotRef } from './contracts.ts';
export const REGISTRY_HASH='23efaa1a65cc7fe7ed49c3e17e90f1c9f1bc55ae11cbce77519cfe20eba44f88';
export const LIMITATIONS = ['Saved dimensionless model output, not calibrated physiology.', 'No supported biological input for this event; model state not advanced.', 'No semantic action authority. No fly learning capability is installed in this adapter.'];
const bytesHash=(s:string)=>createHash('sha256').update(s).digest('hex');
export function verifyEvidence(root = new URL('../../research/genesis-brain-spec-v0.2/',import.meta.url)) {
 const manifest=JSON.parse(readFileSync(new URL('PACKAGE_MANIFEST.json',root),'utf8'));
 // Owning release hashes compact sorted JSON of the manifest excluding its
 // self-address; this is NOT the hash of raw PACKAGE_MANIFEST.json bytes.
 const canonical=(x:unknown):unknown=>Array.isArray(x)?x.map(canonical):x!==null&&typeof x==='object'?Object.fromEntries(Object.entries(x).sort(([a],[b])=>a<b?-1:a>b?1:0).map(([k,v])=>[k,canonical(v)])):x;
 const content={...manifest};delete content.content_sha256;
 if(manifest.content_sha256!=='9322ea0f3c501b6bd29add73464c94b775fb616648801e7f945346776b9bdd0b'||bytesHash(JSON.stringify(canonical(content)))!==manifest.content_sha256)throw new Error('Evidence package identity mismatch');
 for(const [path,hash] of Object.entries(manifest.files)){
  if(path.includes('..')||path.startsWith('/')||bytesHash(readFileSync(new URL(path,root),'utf8'))!==hash)throw new Error('Evidence package member mismatch');
 }
 const raw=readFileSync(new URL('RELEASE.json',root),'utf8');
 if(bytesHash(raw)!=='90aaea995132903cbfca72327f289323f91253678ea087eb7fd30244f94f7788') throw new Error('Evidence release mismatch');
 const release=JSON.parse(raw);
 const registry=readFileSync(new URL(`objects/${REGISTRY_HASH}.json`,root),'utf8');
 if(bytesHash(registry)!==REGISTRY_HASH || release.registry.sha256!==REGISTRY_HASH) throw new Error('Evidence registry mismatch');
 const capabilities=readFileSync(new URL('CAPABILITY_REGISTRY.json',root),'utf8');
 if(bytesHash(capabilities)!==release.components['CAPABILITY_REGISTRY.json'].sha256) throw new Error('Capability evidence mismatch');
 return Object.freeze({registryHash:REGISTRY_HASH,capabilities:JSON.parse(capabilities)});
}
export function assertEvidenceScope(capability:string, modelId:string):never {
 throw new Error(`No runtime capability admission for ${capability} in ${modelId}; Stage-1 scope is frozen research only`);
}
export class SavedObservationAdapter implements BiologicalObservationAdapterV2 {
 private saved:SnapshotRef|null=null;
 private state:ReturnType<CElegansBrain['getState']>|null=null;
 private organismId:string;private at:()=>string;
 constructor(organismId:string, at:()=>string=()=>new Date().toISOString()) {verifyEvidence();this.organismId=organismId;this.at=at;}
 describe(){return {mode:'SAVED-OBSERVATION-ONLY' as const,modelId:'celegans-cook2019-rate-v1',availableCapabilities:[] as [],limitations:[...LIMITATIONS]};}
 restore(ref:SnapshotRef){
  if(bytesHash(ref.bytes)!==ref.sha256 || !Number.isFinite(Date.parse(ref.recordedAt))) throw new Error('Invalid saved snapshot provenance');
  const snapshot=JSON.parse(ref.bytes);
  const brain=new CElegansBrain();brain.initialize(snapshot);
  this.state=brain.getState();this.saved=structuredClone(ref);
 }
 advance(operation:unknown):never {void operation;throw new Error('Biological advancement unavailable in saved-observation-only mode');}
 snapshot(){return structuredClone(this.saved);}
 private envelope(input:ObservationInput|null):BiologicalObservation {
  return {schemaVersion:2,id:`saved:${this.saved?.sha256??'unavailable'}:${input?.id??'view'}`,organismId:this.organismId,producer:'saved-observation-facade',producerVersion:1,modelId:this.describe().modelId,datasetId:data.provenance.commit,anatomyRef:'data/connectome.json',representation:'legacy-scalar-model',snapshotBefore:this.saved?.sha256??null,snapshotAfter:this.saved?.sha256??null,modelClock:this.state?.tick??null,sourceRecordedAt:this.saved?.recordedAt??null,sourceDecisionId:this.saved?.sourceDecisionId??null,observedAt:this.at(),executedThisCycle:false,status:input?'not_applied':this.saved?'saved-model-output':'unavailable',quantityKind:input||!this.state?null:'saved_activity',value:input?null:structuredClone(this.state),units:input||!this.state?null:'dimensionless_model_activity',identityScope:'named C. elegans neurons',aggregation:'none',classification:'ENGINEERING ASSUMPTION',evidence:{registryVersion:'0.2.0',registryHash:REGISTRY_HASH,sourceScope:'C. elegans saved model only; Stage-1 fly learning remains research-only'},uncertainty:{value:null,reason:'No independently identified physiological calibration'},input:structuredClone(input),applicability:{applicable:false,reason:LIMITATIONS[1]},limitations:[...LIMITATIONS],availableCapabilities:[],researchOnlyCapabilities:['capability.associative_appetitive_learning (frozen Stage-1 preparation only)']};
 }
 accept(input:ObservationInput){if(input.kind!=='digital-event'||!input.id||!Number.isFinite(Date.parse(input.observedAt)))throw new Error('Unsupported input schema');return this.envelope(input);}
 observe(){return this.envelope(null);}
}

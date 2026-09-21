import type { Decision, Organism } from '../contracts.ts';
import type { DecisionV2, LifeStateV1 } from './contracts.ts';
export const LEGACY_LABEL='LEGACY COMPUTATIONAL DECODER LABEL — NOT VALIDATED BIOLOGICAL ACTION';
export function publicDecision(d:Decision|DecisionV2){
 if('schemaVersion' in d){
  if(d.schemaVersion!==2)throw new Error('Unknown decision version');
  return {schemaVersion:2 as const,id:d.id,at:d.at,cycle:d.cycle,biological:{status:d.biological.status,executedThisCycle:false,sourceRecordedAt:d.biological.sourceRecordedAt,modelId:d.biological.modelId},reasoningSource:d.reasoning.producer.startsWith('llm:')||d.reasoning.producer.startsWith('provider:')?'LLM REASONING':d.reasoning.producer==='product-deterministic-v1'?'DETERMINISTIC PRODUCT PLANNER':'FAILED OR OTHER PLANNER',layers:['EVENT','BIOLOGICAL OBSERVATION','COMPUTATIONAL LIFE STATE','REASONING','PROPOSAL','POLICY','ACTION OR NON-EXECUTION','OUTCOME','MEMORY / CHANGE'],proposalKind:d.proposal?.kind??null,policy:d.policy?.verdict??null,action:d.action.status,outcome:d.outcome.status,privateContentWithheld:true};
 }
 const label=['APPROACH','AVOID','RETREAT','EXPLORE','WAIT'].includes(d.neural.behavior)?d.neural.behavior:'UNKNOWN';
 return {schemaVersion:1 as const,id:d.id,at:d.at,cycle:d.cycle,legacyLabel:label,interpretation:LEGACY_LABEL,modelId:d.brainAfter?.adapter??null,privateContentWithheld:true};
}
export type PublicFacts={phase:string;busy:boolean;reviewRequired:boolean;awaiting:'assistance'|'approval'|null;legacyMemories:number;episodes:number;latestActivityAt:string|null;latestComputationalAt:string|null};
export function activityStatus(life:LifeStateV1|null,facts?:PublicFacts){
 if(facts?.reviewRequired)return 'REVIEW_REQUIRED';
 if(facts?.busy)return facts.phase==='planning'?'REASONING':'ACTIVE';
 if(facts?.awaiting==='assistance')return 'AWAITING_ASSISTANCE';
 if(facts?.awaiting==='approval')return 'AWAITING_APPROVAL';
 if(life?.executionLock==='CLOSED'&&!facts?.latestComputationalAt)return 'DORMANT';
 return life?'IDLE':'UNAVAILABLE';
}
export function publicState(o:Organism,life:LifeStateV1|null,facts?:PublicFacts){
 const legacy=facts?.legacyMemories??o.memory.length;
 const episodes=facts?.episodes??life?.episodicRefs.length??0;
 return {schemaVersion:2,identity:{id:o.id,name:'Genesis',bornAt:o.bornAt,cycles:o.cycles},status:activityStatus(life,facts),executionLock:life?.executionLock??null,biologicalMode:'SAVED-OBSERVATION-ONLY',savedBrain:{adapter:o.brain?.adapter??null,version:o.brain?.version??null},activity:{latestAt:facts?.latestActivityAt??null,latestComputationalAt:facts?.latestComputationalAt??null},
 // Compatibility alias: memories continues to mean legacy records ONLY, never an aggregate.
 counts:{memories:legacy,projects:o.businesses.length},memoryAccounting:{legacyRecords:legacy,v2Episodes:episodes,semanticAssertions:life?.semanticMemory.length??0},
 economy:{namespace:'SIMULATED ECONOMY',startingCents:o.wallet.startingCents,cashCents:o.wallet.startingCents+o.wallet.entries.reduce((s,e)=>s+e.cents,0)},onchain:{namespace:'ONCHAIN ECONOMY',identityStatus:life?.walletIdentity.status??'unresolved',balance:null},attributedRevenue:{namespace:'ATTRIBUTED REVENUE',value:null,reason:'No verified attribution source enabled'},privateContentWithheld:true};
}
export type PublicDecision=ReturnType<typeof publicDecision>;
export type PublicState=ReturnType<typeof publicState> & {history:PublicDecision[];schedule:{enabled:boolean};biological:unknown};

/** Private operator projection; caller must authenticate separately. Never includes hidden provider reasoning or raw context. */
export function operatorTrace(d:DecisionV2){return {id:d.id,organismId:d.organismId,at:d.at,committed:d.cycle!==null,event:{id:d.event.id,kind:d.event.kind,source:d.event.source,observedAt:d.event.observedAt},biological:d.biological,contextManifest:d.lifeContext.contextManifest,contextHash:d.lifeContext.contextHash,reasoning:{producer:d.reasoning.producer,rationale:d.reasoning.rationale.slice(0,2000)},proposal:d.proposal,policy:d.policy,action:{...d.action,performed:d.cycle!==null&&d.action.status==='local_saved'},outcome:d.outcome,memory:{episodeId:d.memory.episode.id,committed:d.cycle!==null,changes:d.memory.changes},memoryChanges:d.memory.changes,humanReviewRequiredAtDecision:d.policy?.verdict==='REQUIRE_HUMAN_APPROVAL',limitations:['Stored bounded rationale only; no hidden reasoning or working context.','Current grant/intent/provider review state requires a separate durable inspection.']};}

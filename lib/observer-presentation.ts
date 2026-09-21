import {z} from 'zod';
const timestamp=z.string().refine(x=>Number.isFinite(Date.parse(x)));
const base={id:z.string(),at:timestamp,cycle:z.number().int().positive().nullable()};
export const decisionSchema=z.discriminatedUnion('schemaVersion',[
 z.object({...base,schemaVersion:z.literal(1),legacyLabel:z.enum(['APPROACH','AVOID','RETREAT','EXPLORE','WAIT','UNKNOWN'])}),
 z.object({...base,schemaVersion:z.literal(2),biological:z.object({status:z.enum(['not_applied','saved-model-output','unavailable']),executedThisCycle:z.literal(false),sourceRecordedAt:timestamp.nullable(),modelId:z.string()}),reasoningSource:z.enum(['LLM REASONING','DETERMINISTIC PRODUCT PLANNER','FAILED OR OTHER PLANNER']),proposalKind:z.enum(['PROPOSAL','ABSTAIN','DEFER','REQUEST_ASSISTANCE']).nullable(),policy:z.enum(['ALLOW','DENY','REQUIRE_HUMAN_APPROVAL','DEFER']).nullable(),action:z.enum(['local_saved','not_executed']),outcome:z.enum(['failed','local','deferred','pending','abstained','denied','recorded'])})
]);
export const observerSchema=z.object({schemaVersion:z.literal(2),identity:z.object({id:z.string(),name:z.string(),bornAt:timestamp,cycles:z.number().int().nonnegative()}),status:z.enum(['DORMANT','IDLE','REASONING','ACTIVE','AWAITING_ASSISTANCE','AWAITING_APPROVAL','REVIEW_REQUIRED','UNAVAILABLE']),activity:z.object({latestAt:timestamp.nullable(),latestComputationalAt:timestamp.nullable()}).optional(),memoryAccounting:z.object({legacyRecords:z.number().int().nonnegative(),v2Episodes:z.number().int().nonnegative(),semanticAssertions:z.number().int().nonnegative()}).optional(),counts:z.object({memories:z.number().int().nonnegative(),projects:z.number().int().nonnegative()}),economy:z.object({namespace:z.literal('SIMULATED ECONOMY'),startingCents:z.number().int(),cashCents:z.number().int()}),onchain:z.object({namespace:z.literal('ONCHAIN ECONOMY'),identityStatus:z.enum(['unresolved','bound']),balance:z.null()}),attributedRevenue:z.object({namespace:z.literal('ATTRIBUTED REVENUE'),value:z.null()}),history:z.array(decisionSchema)});
export type Observation=z.infer<typeof observerSchema>;
export type PublicMoment=z.infer<typeof decisionSchema>;
/** Presentation allowlist: extra fields are discarded, never spread into JSX or copy. */
export function readObservation(value:unknown):Observation{return observerSchema.parse(value);}
export function momentCopy(d:PublicMoment){
 if(d.schemaVersion===1)return {title:'An earlier experience, preserved.',why:'This record belongs to an earlier version of the experiment.',outcome:'Its original record remains unchanged.',biology:'A saved neural response is available to inspect.',change:'Kept in Genesis’s history.'};
 const biology=d.biological.status==='not_applied'?"The biological system wasn’t involved in this decision.":d.biological.status==='saved-model-output'?'Only a historical biological observation was available.':'No biological observation was available.';
 const common={biology,change:d.cycle===null?'This is an uncommitted example, not a new Genesis memory.':'A computational experience was recorded. Its private contents are not shared.'};
 if(d.outcome==='failed')return {...common,title:'Genesis couldn’t complete its reasoning this time.',why:'No completed proposal was available.',outcome:'No external action was taken.'};
 if(d.policy==='DENY')return {...common,title:'Genesis wasn’t allowed to do this.',why:'The proposal was outside its permissions.',outcome:'The proposed action was not carried out.'};
 if(d.proposalKind==='REQUEST_ASSISTANCE')return {...common,title:'Genesis asked for help.',why:'A request for human review was recorded locally.',outcome:'No message was sent. The request was recorded for human review.'};
 if(d.policy==='REQUIRE_HUMAN_APPROVAL')return {...common,title:'Genesis is waiting for permission.',why:'This proposal needs human approval.',outcome:'The proposed action has not been carried out.'};
 if(d.proposalKind==='DEFER')return {...common,title:'Genesis left this for another time.',why:'The recorded proposal was to postpone.',outcome:'No external action was taken.'};
 if(d.action==='local_saved')return {...common,title:'Genesis saved something locally.',why:'A local text artifact was permitted and saved.',outcome:'It stayed local. Its contents are private.'};
 if(d.outcome==='recorded')return {...common,title:'Genesis recorded a computational update.',why:'A permitted update was recorded locally.',outcome:'No external action was taken.'};
 if(d.proposalKind==='ABSTAIN')return {...common,title:'Genesis decided not to act this time.',why:'The recorded proposal was to abstain.',outcome:'No external action was taken.'};
 return {...common,title:'Genesis considered a next step.',why:null,outcome:'No external action was taken.'};
}
export function currentCopy(s:Observation|null,fixture=false){
 if(!s)return {title:'A life, coming into view.',description:'Waiting for a saved observation. Nothing is inferred from missing information.',label:'Observation unavailable'};
 if(!fixture&&s.status==='DORMANT')return {title:'A life, held in waiting.',description:'Genesis is dormant. Its identity and experiences are preserved. No new activity is taking place.',label:'Dormant'};
 if(!fixture){
  if(s.status==='REVIEW_REQUIRED')return {title:'Genesis is waiting for a review.',description:'A recorded cycle needs human inspection. No retry has been authorized.',label:'Review required'};
  if(s.status==='REASONING'||s.status==='ACTIVE')return {title:s.status==='REASONING'?'Genesis is considering a next step.':'A computational cycle is in progress.',description:'No completed outcome is inferred from work in progress.',label:'In progress'};
  if(s.status==='AWAITING_ASSISTANCE'||s.status==='AWAITING_APPROVAL')return {title:s.status==='AWAITING_ASSISTANCE'?'Genesis has asked for help.':'Genesis is waiting for permission.',description:'A locally recorded request is awaiting human review. No external action has been taken.',label:'Waiting for review'};
 }
 const latest=s.history[0];return latest?{title:momentCopy(latest).title,description:momentCopy(latest).outcome,label:fixture?'Example of a recorded moment':'Last recorded activity'}:{title:'There is no new activity to share.',description:'Nothing is inferred from missing information.',label:'Between recorded moments'};
}
export function ageText(birth:string,now:number){const days=Math.floor((now-Date.parse(birth))/86400000);return days<0?null:days===0?'Less than a day':`${days} ${days===1?'day':'days'}`;}
export function resourceCopy(s:Observation){return {amount:new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'}).format(s.economy.cashCents/100),label:'Simulated resources',revenue:'No verified earnings to report.',wallet:s.onchain.identityStatus==='unresolved'?'A public wallet has not been verified.':'No verified wallet balance is available.'};}
export const OBSERVER_VIEWS=['live','brain','life','money','memory','about'] as const;
export type ObserverView=typeof OBSERVER_VIEWS[number];
export function readView(x:string|null):ObserverView{return OBSERVER_VIEWS.includes(x as ObserverView)?x as ObserverView:'live';}
export type ObserverExamples={label:string;publicMemories:{id:string;text:string}[];projects:{id:string;name:string;detail:string}[];interests:string[];question:string};
export type ObserverFixtures={observations:{id:string;label:string;state:Observation}[];examples:ObserverExamples};

export function reasoningCopy(d:PublicMoment){return d.schemaVersion===1?'Historical planning record; private details withheld.':d.reasoningSource==='LLM REASONING'?'Language-model planning, separate from the biological model.':d.reasoningSource==='DETERMINISTIC PRODUCT PLANNER'?'A rule-based planner, separate from the biological model.':'The planning source is unavailable or did not complete.';}

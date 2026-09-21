import {NO_DISCLOSURE,type DisclosureSet} from './disclosure.ts';
import {RECALL_POLICY,EMPTY_ARCHIVE,type MemoryArchive} from './memory.ts';
import type { Organism } from '../contracts.ts';
import type { BiologicalObservationAdapterV2, DecisionV2, LifeStateV1, ObservationInput, Permissions, PlannerV2, Proposal, PolicyVerdict, ScopedCycleAuthority } from './contracts.ts';
import { compileContext } from './context.ts';
import { evaluatePolicy } from './policy.ts';
import { validateProposal } from './planner.ts';
import {outcomeStatus} from './intents.ts';
import { reduceLife } from './life-state.ts';
export class InterruptedCycle extends Error {}
/** Pure isolated preparation; no DB/network/tool dispatcher. Runtime lock is checked before this entry. */
export async function prepareCycle(o:Organism,life:LifeStateV1,brain:BiologicalObservationAdapterV2,planner:PlannerV2,event:ObservationInput,permission:Permissions,at:string,id:string,authority?:ScopedCycleAuthority,archive:MemoryArchive=EMPTY_ARCHIVE,phase?:(stage:string)=>Promise<void>,disclosure:DisclosureSet=NO_DISCLOSURE):Promise<{life:LifeStateV1;decision:DecisionV2}> {
 const biological=brain.accept(event);const context=compileContext(o,life,biological,permission,12000,authority,archive,[],disclosure);
 let proposal:Proposal|null=null,policy:PolicyVerdict|null=null,error:string|null=null;
 try{await phase?.('before_planner');proposal=validateProposal(await planner.propose(context),context);await phase?.('after_planner');await phase?.('before_policy');policy=evaluatePolicy(proposal,context,life.executionLock==='CLOSED'&&!authority,life.revision,life,o.businesses.map(p=>p.id));await phase?.('after_policy');}catch(e){if(e instanceof InterruptedCycle)throw e;error=e instanceof Error?e.message:'Provider/validation failure';}
 const changes=policy?.verdict==='ALLOW'?[...proposal?.changes??[]]:[];
 if(policy?.verdict==='REQUIRE_HUMAN_APPROVAL'&&proposal?.kind==='REQUEST_ASSISTANCE'&&permission.localArtifacts)changes.push({kind:'operational',expectedRevision:life.revision,sourceIds:[event.id],operation:{op:'assistance_create',id:id+':assistance',question:proposal.assistance!,projectId:proposal.projectId,taskId:proposal.taskId,relationshipId:null}});
 const episode={schemaVersion:1 as const,id:id+':episode',organismId:o.id,at,kind:'episode' as const,source:id,visibility:'private' as const,record:{recall:RECALL_POLICY,proposalId:proposal?.id??null,policy:policy?.verdict??null,providerError:error}};
 const artifact=policy?.verdict==='ALLOW' && ['local_reflection','local_artifact'].includes(proposal?.tool??'') ? proposal!.arguments.text : null;
 if(artifact!==null)Object.assign(episode.record,{localArtifact:artifact});
 const status=outcomeStatus(proposal,policy,error!==null);
 Object.assign(episode.record,{outcomeStatus:status,actionStatus:artifact!==null?'local_saved':'not_executed',lifeChanges:changes});
 const next=reduceLife(life,episode,changes,context.sources,o.businesses.map(p=>p.id));
 next.biologicalContext.observationIds.push(biological.id);
 return {life:next,decision:{schemaVersion:2,id,organismId:o.id,at,cycle:null,event,biological,lifeContext:{permission:structuredClone(permission),revision:life.revision,contextManifest:context.manifest,contextHash:context.hash},reasoning:{producer:proposal?.planner??'failed-provider-attempt',rationale:proposal?.rationale??'Provider or validation failed; no fallback substituted.'},proposal,policy,action:artifact!==null?{status:'local_saved',reason:'Local artifact staged in episode; no external dispatch.',artifact}:{status:'not_executed',reason:error??'No external dispatcher enabled.'},outcome:{status,detail:error?'Provider or validation failed; private diagnostic retained.':'No external action executed.',namespace:'COMPUTATIONAL'},memory:{episode,changes}}};
}

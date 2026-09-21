import {followups,LOCAL_PERMISSION} from './continuous.ts';
import {reduceLife} from './life-state.ts';
import type {LifeStateV1} from './contracts.ts';
import type { ActionIntent, Approval, IntentStatus, PolicyVerdict, Proposal, WorkingContext } from './contracts.ts';
import { digest } from './identity.ts';
import {validateIntent} from './intents.ts';
import { validateProposal } from './planner.ts';
export function evaluatePolicy(proposal:Proposal,c:WorkingContext,locked:boolean,currentRevision:number,life?:LifeStateV1,projectIds:string[]=[]):PolicyVerdict {
 const p=validateProposal(proposal,c);const base={version:'policy-v1' as const,payloadHash:digest(p),executionEnabled:false as const};
 if(locked||!c.permission.execution)return {...base,verdict:'DENY',rules:['execution-lock-closed']};
 if(currentRevision!==c.manifest.stateRevision)return {...base,verdict:'DENY',rules:['stale-context']};
 if(p.cost.maxMicros>c.permission.maxCostMicros)return {...base,verdict:'DENY',rules:['cost-cap']};
 if(p.changes.some(x=>x.kind==='operational')){
  if(!c.permission.localArtifacts||!life)return {...base,verdict:'DENY',rules:['operational-life-permission-or-state-missing']};
  try{const event=JSON.parse(c.text).currentEvent;reduceLife(life,{schemaVersion:1,id:event.id+':policy-check',organismId:c.organismId,at:event.observedAt,kind:'episode',source:event.id,visibility:'private',record:{}},p.changes,c.sources,projectIds);}catch{return {...base,verdict:'DENY',rules:['invalid-operational-life-change']};}
 }
 if(p.kind==='REQUEST_ASSISTANCE'&&c.permission.localArtifacts){
  if(!life)return {...base,verdict:'DENY',rules:['assistance-state-missing']};
  try{const event=JSON.parse(c.text).currentEvent;reduceLife(life,{schemaVersion:1,id:event.id+':assistance-check',organismId:c.organismId,at:event.observedAt,kind:'episode',source:event.id,visibility:'private',record:{}},[{kind:'operational',expectedRevision:currentRevision,sourceIds:[event.id],operation:{op:'assistance_create',id:event.id+':request-check',question:p.assistance!,projectId:p.projectId,taskId:p.taskId,relationshipId:null}}],c.sources,projectIds);}catch{return {...base,verdict:'DENY',rules:['invalid-assistance-request']};}
 }
 const continuous=JSON.parse(c.text).critical.continuousAuthority;
 if(continuous){
  if(p.tool&&!continuous.limits.allowedEffects.includes(p.tool)||(p.changes.length||p.kind==='REQUEST_ASSISTANCE')&&!continuous.limits.allowedEffects.includes('life_changes'))return {...base,verdict:'DENY',rules:['continuous-effect-not-authorized']};
  if(!life||c.permission.llm||digest(c.permission)!==digest(LOCAL_PERMISSION))return {...base,verdict:'DENY',rules:['continuous-local-only']};
  try{const event=JSON.parse(c.text).currentEvent;const next=reduceLife(life,{schemaVersion:1,id:event.id+':wake-check',organismId:c.organismId,at:event.observedAt,kind:'episode',source:event.id,visibility:'private',record:{}},p.kind==='PROPOSAL'?p.changes:[],c.sources,projectIds);followups(p,next,continuous.event,'policy-check',event.observedAt,continuous);}catch{return {...base,verdict:'DENY',rules:['continuous-wake-or-reducer-limit']};}
 }
 if(p.kind==='DEFER')return {...base,verdict:'DEFER',rules:['product-postponement']};
 if(p.kind==='REQUEST_ASSISTANCE'||p.tool==='external_message'||p.tool==='financial_transfer')return {...base,verdict:'REQUIRE_HUMAN_APPROVAL',rules:['external-executor-not-installed']};
 if(p.tool&&!c.permission.localArtifacts)return {...base,verdict:'DENY',rules:['local-artifact-permission']};
 return {...base,verdict:'ALLOW',rules:['local-or-abstention-only']};
}
export function approvalMatches(a:Approval,p:Proposal,at:string):boolean {
 return !!a.approver&&!!a.id&&Number.isFinite(Date.parse(at))&&Date.parse(a.expiresAt)>Date.parse(at)&&a.payloadHash===digest(p)&&a.policyVersion==='policy-v1'&&a.operation===p.tool&&a.maximumMicros>=p.cost.maxMicros&&a.recipient===null&&a.network===null&&a.asset===null;
}
const transitions:Record<IntentStatus,IntentStatus[]>={proposed:['denied','awaiting_approval','deferred','reserved','local_completed','abstained','failed','cancelled','unknown'],denied:[],awaiting_approval:['approved','denied','cancelled'],approved:['reserved','denied','cancelled'],deferred:[],reserved:['failed'],dispatching:['succeeded','failed','unknown'],succeeded:[],failed:[],unknown:['reconciled'],reconciled:[],local_completed:[],abstained:[],cancelled:[]};
export function transitionIntent(intent:ActionIntent,status:IntentStatus,at:string):ActionIntent {
 intent=validateIntent(intent);
 if(!transitions[intent.status].includes(status))throw new Error('Invalid intent transition; dispatcher unavailable');
 if(status==='awaiting_approval'&&intent.policy.verdict!=='REQUIRE_HUMAN_APPROVAL')throw new Error('Approval not requested by policy');
 if(status==='reserved'&&intent.policy.verdict!=='ALLOW'&&!(intent.status==='approved'&&intent.approval&&approvalMatches(intent.approval,intent.proposal,at)))throw new Error('Policy does not permit reservation');
 if(status==='approved'&&(!intent.approval||!approvalMatches(intent.approval,intent.proposal,at)))throw new Error('Approval missing, changed or expired');
 if(status==='reserved'&&(intent.proposal.tool==='external_message'||intent.proposal.tool==='financial_transfer'))throw new Error('External execution disabled');
 return validateIntent({...structuredClone(intent),status});
}
export function reserveAttempt(intent:ActionIntent,maxAttempts:number,cap:number):ActionIntent {
 intent=validateIntent(intent);
 if(!['proposed','approved','reserved'].includes(intent.status)||intent.attempts>=maxAttempts||intent.reservedMicros+intent.proposal.cost.maxMicros>cap)throw new Error('Retry/cost limit or ambiguous outcome');
 return {...structuredClone(intent),attempts:intent.attempts+1,reservedMicros:intent.reservedMicros+intent.proposal.cost.maxMicros};
}

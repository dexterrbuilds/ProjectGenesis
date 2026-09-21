/** Canonical current-scope intent contract. No defaulting of authority or ownership. */
import {z} from 'zod';
import {proposalSchema} from './planner.ts';
import {digest} from './identity.ts';
import type {ActionIntent,DecisionV2,IntentStatus} from './contracts.ts';
const hash=z.string().regex(/^[a-f0-9]{64}$/);
export const intentSchema=z.object({
 id:z.string().min(1),organismId:z.string().min(1),payloadHash:hash,proposal:proposalSchema,
 policy:z.object({verdict:z.enum(['ALLOW','DENY','REQUIRE_HUMAN_APPROVAL','DEFER']),rules:z.array(z.string()),version:z.literal('policy-v1'),payloadHash:hash,executionEnabled:z.literal(false)}).strict(),
 status:z.enum(['proposed','denied','awaiting_approval','approved','deferred','reserved','dispatching','succeeded','failed','unknown','reconciled','local_completed','abstained','cancelled']),
 attempts:z.number().int().nonnegative().safe(),reservedMicros:z.number().int().nonnegative().safe(),receipt:z.string().nullable(),
 approval:z.object({id:z.string().min(1),payloadHash:hash,operation:z.enum(['local_reflection','local_artifact','external_message','financial_transfer']),recipient:z.string().nullable(),network:z.string().nullable(),asset:z.string().nullable(),maximumMicros:z.number().int().nonnegative().safe(),expiresAt:z.string().datetime({offset:true}),approver:z.string().min(1),policyVersion:z.literal('policy-v1')}).strict().nullable(),
}).strict();
export function validateIntent(value:unknown,organismId?:string):ActionIntent {
 const parsed=intentSchema.safeParse(value);
 if(!parsed.success)throw new Error('Malformed action intent: '+parsed.error.issues.map(i=>i.path.join('.')).join(', '));
 const i=parsed.data;
 if(organismId!==undefined&&i.organismId!==organismId)throw new Error('Intent organism mismatch');
 if(i.payloadHash!==digest(i.proposal)||i.policy.payloadHash!==i.payloadHash)throw new Error('Intent payload/policy mismatch');
 if(i.approval&&(i.approval.payloadHash!==i.payloadHash||i.approval.operation!==i.proposal.tool))throw new Error('Intent approval binding mismatch');
 if(i.status==='approved'&&!i.approval)throw new Error('Approved intent requires approval evidence');
 if(['awaiting_approval','approved'].includes(i.status)&&i.policy.verdict!=='REQUIRE_HUMAN_APPROVAL')throw new Error('Intent approval not requested');
 if(i.status==='deferred'&&i.policy.verdict!=='DEFER')throw new Error('Intent deferral not requested');
 if(i.status==='local_completed'&&(i.policy.verdict!=='ALLOW'||i.proposal.kind!=='PROPOSAL'||!['local_reflection','local_artifact',null].includes(i.proposal.tool)))throw new Error('Invalid local completion');
 if(i.status==='abstained'&&(i.policy.verdict!=='ALLOW'||i.proposal.kind!=='ABSTAIN'))throw new Error('Invalid abstention');
 return i;
}
/** At creation there has been no effect, reservation or approval. These are explicit facts. */
export function createIntent(d:DecisionV2):ActionIntent|null {
 if(!d.proposal||!d.policy)return null;
 return validateIntent({id:d.id+':intent',organismId:d.organismId,payloadHash:d.policy.payloadHash,proposal:d.proposal,policy:d.policy,status:'proposed',attempts:0,reservedMicros:0,receipt:null,approval:null},d.organismId);
}
export function outcomeStatus(proposal:DecisionV2['proposal'],policy:DecisionV2['policy'],failed:boolean):DecisionV2['outcome']['status'] {
 if(failed||!proposal||!policy)return 'failed';
 if(policy.verdict==='DENY')return 'denied';
 if(policy.verdict==='REQUIRE_HUMAN_APPROVAL')return 'pending';
 if(policy.verdict==='DEFER')return 'deferred';
 if(proposal.kind==='ABSTAIN')return 'abstained';
 return ['local_reflection','local_artifact'].includes(proposal.tool??'')?'local':'recorded';
}
export function committedIntentStatus(d:DecisionV2):IntentStatus {
 const expected=outcomeStatus(d.proposal,d.policy,d.outcome.status==='failed');
 if(expected!==d.outcome.status)throw new Error('Decision outcome contradicts proposal/policy');
 if((expected==='local')!==(d.action.status==='local_saved'))throw new Error('Decision action contradicts outcome');
 const states:Record<DecisionV2['outcome']['status'],IntentStatus>={failed:'failed',denied:'denied',pending:'awaiting_approval',deferred:'deferred',abstained:'abstained',local:'local_completed',recorded:'local_completed'};
 return states[expected];
}

import type {disclosureBinding} from './disclosure.ts';
import type {FollowUp,ContinuousContext} from './continuous.ts';
import type {OperationalState,OperationalChange} from './operations.ts';
import type {MemorySelection,MemoryQuery} from './memory.ts';
import type { BrainState, Organism } from '../contracts.ts';
export type EvidenceClass = 'BIOLOGICAL FACT' | 'EXPERIMENTALLY SUPPORTED COMPUTATIONAL APPROXIMATION' | 'HYPOTHESIS' | 'ENGINEERING ASSUMPTION' | 'GENESIS PRODUCT MAPPING';
export type SnapshotRef = { bytes: string; sha256: string; recordedAt: string; sourceDecisionId?:string; parent: string | null };
export type ObservationInput = { id: string; kind: 'digital-event'; source: string; observedAt: string; recall?:MemoryQuery };
export type BiologicalObservation = {
  schemaVersion: 2; id: string; organismId: string; producer: string; producerVersion: 1;
  modelId: string; datasetId: string; anatomyRef: string; representation: 'legacy-scalar-model';
  snapshotBefore: string | null; snapshotAfter: string | null; modelClock: number | null;
  sourceRecordedAt: string | null; sourceDecisionId:string|null; observedAt: string; executedThisCycle: false;
  status: 'saved-model-output' | 'not_applied' | 'unavailable'; quantityKind: 'saved_activity' | null;
  value: BrainState | null; units: 'dimensionless_model_activity' | null;
  identityScope: 'named C. elegans neurons'; aggregation: 'none'; classification: EvidenceClass;
  evidence: { registryVersion: '0.2.0'; registryHash: string; sourceScope: string };
  uncertainty: { value: null; reason: string }; input: ObservationInput | null;
  applicability: { applicable: false; reason: string }; limitations: string[];
  availableCapabilities: []; researchOnlyCapabilities: string[];
};
export interface BiologicalObservationAdapterV2 {
  describe(): { mode: 'SAVED-OBSERVATION-ONLY'; modelId: string; availableCapabilities: []; limitations: string[] };
  restore(ref: SnapshotRef): void;
  accept(input: ObservationInput): BiologicalObservation;
  advance(operation: unknown): never;
  observe(): BiologicalObservation;
  snapshot(): SnapshotRef | null;
}
export type MemoryAssertion = { id: string; text: string; sources: string[]; confidence: number | null; author: 'planner' | 'operator'; verified: false; supersedes: string | null; contradictions: string[] };
export type LifeStateV1 = {
 operational?:OperationalState;
 schemaVersion: 1; organismId: string; revision: number; baseRevision: number; constitutionHash: string;
 executionLock: 'CLOSED' | 'OPEN'; walletIdentity: { status: 'unresolved' | 'bound'; address: string | null; network: string | null; provenance: string | null };
 commitments: {id:string;source:string;status:'open'|'fulfilled'|'cancelled';dueAt:string|null}[];
 projectLife: {id:string;status:'active'|'paused'|'completed'|'abandoned';reason:string;source:string}[];
 interests: MemoryAssertion[]; openQuestions: MemoryAssertion[]; relationships: {id:string;source:string;consent:'unknown'|'recorded'}[];
 tasks: {id:string;status:'pending'|'deferred'|'completed';reviewAt:string|null;source:string}[];
 pendingDecisions: string[]; episodicRefs: string[]; semanticMemory: MemoryAssertion[];
 environment: {id:string;text:string;source:string;visibility:'private'|'public';at:string}[];
 rhythm: {legacy: Organism['rhythm'] | null; reviewAt:string|null; mode:'dormant'|'resting'|'scheduled'};
 biologicalContext: {snapshotHash:string|null;observationIds:string[];mode:'SAVED-OBSERVATION-ONLY'};
 provenance: {reducer:'life-v1';administrative:true;source:'existing-organism'};
};
export type LifeEvent = {schemaVersion:1;id:string;organismId:string;at:string;kind:'episode'|'administrative';source:string;visibility:'private'|'public';record:unknown};
export type Permissions = { execution: boolean; localArtifacts:boolean; llm:boolean; internet:false; communication:false; financial:false; maxCostMicros:number; maxAttempts:number };
export type WorkingContext = { text:string; hash:string; manifest:{version:'context-v1';stateRevision:number;constitutionHash:string;tokenBudget:number;estimatedTokens:number;selectedIds:string[];droppedIds:string[];reasons:Record<string,string>;truncations:string[];memory?:Omit<MemorySelection,'items'>;disclosure?:{version:1;audience:'PROVIDER'|'INTERNAL';binding:ReturnType<typeof disclosureBinding>;contextBytes:number;includedCategories:string[];includedSources:{id:string;hash:string}[];includedReviewIds:string[];omitted:{id:string;reason:string}[];omissionsClipped:boolean;excludedCategories:string[]};operational?:{version:1;selectedIds:string[];omitted:{id:string;reason:string}[];bytes:number}}; permission:Permissions; organismId:string; sources:string[] };
export type ToolName = 'local_reflection' | 'local_artifact' | 'external_message' | 'financial_transfer';
export type Proposal = {followUp?:FollowUp;schemaVersion:2;id:string;contextHash:string;kind:'PROPOSAL'|'DEFER'|'ABSTAIN'|'REQUEST_ASSISTANCE';intent:string;taskId:string|null;projectId:string|null;tool:ToolName|null;arguments:{text:string};citations:string[];rationale:string;cost:{namespace:'OPERATIONAL';maxMicros:number};uncertainty:string;deferUntil:string|null;assistance:string|null;changes:LifeChange[];planner:string};
export type LifeChange = OperationalChange | {kind:'assertion';assertion:MemoryAssertion} | {kind:'project_status';id:string;status:'active'|'paused'|'completed'|'abandoned';reason:string} | {kind:'defer_task';id:string;reviewAt:string};
export interface PlannerV2 { propose(context:WorkingContext):Promise<Proposal> }
export type PolicyVerdict = {verdict:'ALLOW'|'DENY'|'REQUIRE_HUMAN_APPROVAL'|'DEFER';rules:string[];version:'policy-v1';payloadHash:string;executionEnabled:false};
export type IntentStatus = 'proposed'|'denied'|'awaiting_approval'|'approved'|'deferred'|'reserved'|'dispatching'|'succeeded'|'failed'|'unknown'|'reconciled'|'local_completed'|'abstained'|'cancelled';
export type ActionIntent = {id:string;organismId:string;payloadHash:string;proposal:Proposal;policy:PolicyVerdict;status:IntentStatus;attempts:number;reservedMicros:number;receipt:string|null;approval:Approval|null};
export type Approval = {id:string;payloadHash:string;operation:ToolName;recipient:string|null;network:string|null;asset:string|null;maximumMicros:number;expiresAt:string;approver:string;policyVersion:'policy-v1'};
export type DecisionV2 = {schemaVersion:2;id:string;organismId:string;at:string;cycle:number|null;event:ObservationInput;biological:BiologicalObservation;lifeContext:{permission?:Permissions;revision:number;contextManifest:WorkingContext['manifest'];contextHash:string};reasoning:{producer:string;rationale:string};proposal:Proposal|null;policy:PolicyVerdict|null;action:{status:'not_executed'|'local_saved';reason:string;artifact?:string};outcome:{status:'abstained'|'deferred'|'pending'|'failed'|'local'|'denied'|'recorded';detail:string;namespace:'COMPUTATIONAL'};memory:{episode:LifeEvent;changes:LifeChange[]}};

/** Computational single-cycle authority; never a neural state or global unlock. */
export type ScopedCycleAuthority=ContinuousContext | {grantId:string;grantHash:string;permissionHash:string;event:Record<string,unknown>};

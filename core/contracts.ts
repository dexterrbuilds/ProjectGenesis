import type { WalletAccount } from './economy/adapters.ts';
export const CHANNELS = ['rewardOpportunity', 'danger', 'novelty', 'scarcity', 'acquisition', 'uncertainty', 'social'] as const;
export type Channel = typeof CHANNELS[number];
export type Stimulus = Record<Channel, number>;
export type Behavior = 'APPROACH' | 'AVOID' | 'EXPLORE' | 'RETREAT' | 'WAIT';
export type Node = { id: string; role: string };
export type Edge = { source: string; target: string; weight: number; kind: string };
export type BrainState = { tick: number; activity: number[]; stimulated: string[] };
export type BrainSnapshot = { adapter: string; version: number; payload: unknown };
export type BehavioralOutput = { behavior: Behavior; scores: Record<string, number>; evidence: { id: string; activity: number; pool: string }[]; policy: string };
export interface BrainAdapter {
  readonly id: string;
  readonly nodes: Node[];
  readonly edges: Edge[];
  initialize(snapshot?: BrainSnapshot): void;
  stimulate(input: Stimulus): { neuron: string; current: number; channels: Channel[] }[];
  step(count?: number): BrainState;
  decodeBehavior(): BehavioralOutput;
  getState(): BrainState;
  snapshot(): BrainSnapshot;
}
export type WorldEvent = { id: string; title: string; source: string; features: Partial<Stimulus>; detail?: string; parentDecision?: string };
export const ACTIONS = ['idle', 'manage_resources', 'research', 'read', 'learn', 'draft_service', 'work', 'reflect', 'rest', 'review_risk', 'withdraw', 'draft_message', 'request_payment', 'request_investment', 'request_hire', 'request_publish', 'request_physical'] as const;
export type Action = typeof ACTIONS[number];
export type Plan = { behavior: Behavior; action: Action; reasoning: string; content: string; planner: string };
export interface PlannerAdapter { plan(context: PlanningContext): Promise<Plan> }
export type PlanningContext = { behavior: BehavioralOutput; event: WorldEvent; allowedActions: readonly Action[]; organism: Organism; externalWallet?: WalletAccount };
export type LedgerEntry = { id: string; kind: 'business_income' | 'trading_fee_income' | 'expense' | 'investment_pnl'; cents: number; note: string; at: string };
export type WalletState = { mode: 'simulated'; startingCents: number; entries: LedgerEntry[] };
export interface WalletAdapter { getState(): WalletState; balance(): number; post(entry: LedgerEntry): void }
export type Business = { id: string; name: string; artifact: string; status: 'draft' | 'working'; workCycles: number; earnedCents: number };
export type Memory = { id: string; at: string; text: string; sourceDecision: string; salience: number };
export type Approval = { id: string; action: Action; content: string; status: 'pending'; decision: string };
export type Milestone = { id: string; kind: 'birth' | 'first_experience' | 'first_project' | 'first_income' | 'brain_change'; at: string; title: string; detail: string; decisionId?: string };
export type LifeRhythm = { energy: number; resting: boolean };
export type Organism = {
  id: string; name: string; bornAt: string; cycles: number; activity: string; paused: boolean;
  drives: string[]; wallet: WalletState; memory: Memory[]; businesses: Business[]; approvals: Approval[];
  brain: BrainSnapshot | null; brainLineage: { adapter: string; at: string }[]; nextEvent: WorldEvent;
  milestones?: Milestone[]; rhythm?: LifeRhythm;
};
export type Outcome = { ok: boolean; title: string; detail: string; simulated: boolean; artifact?: string; sourceUrl?: string; features: Partial<Stimulus>; approvalRequired?: boolean };
export type Decision = { externalWallet?: WalletAccount; id: string; at: string; cycle: number; event: WorldEvent; stimulus: Stimulus; encoding: ReturnType<BrainAdapter['stimulate']>; brainBefore: BrainSnapshot; frames: BrainState[]; neural: BehavioralOutput; plan: Plan | null; outcome: Outcome; nextEvent: WorldEvent; brainAfter: BrainSnapshot };

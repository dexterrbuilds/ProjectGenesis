import type { BrainAdapter, PlannerAdapter, WorldEvent } from '../core/contracts.ts';
import { liveCycle } from '../core/life.ts';
import { economics } from '../core/wallet.ts';
import { LifeStore } from '../server/store.ts';
import type { RuntimeConfig } from './config.ts';
export class GenesisService {
  readonly store: LifeStore; readonly config: RuntimeConfig;
  private brainFactory: () => BrainAdapter; private planner: PlannerAdapter;
  constructor(store: LifeStore, config: RuntimeConfig, brainFactory: () => BrainAdapter, planner: PlannerAdapter) { this.store = store; this.config = config; this.brainFactory = brainFactory; this.planner = planner; }
  async advance(id: string, event?: WorldEvent, automatic = false) {
    const previous = await this.store.decision(id); if (previous) return { decision: previous, replayed: true };
    const lease = crypto.randomUUID(), claim = await this.store.claim(lease, automatic, this.config.maxDailyCycles);
    if (!claim) return null;
    try {
      const raced = await this.store.decision(id); if (raced) return { decision: raced, replayed: true };
      const result = await liveCycle(claim.organism, this.brainFactory(), this.planner, { internet: this.config.internet, id, event, onPhase: phase => this.store.phase(lease, phase) });
      const resting = ['idle','rest','reflect'].includes(result.decision.plan?.action ?? '');
      await this.store.commit(lease, claim.revision, result.organism, result.decision, automatic, this.config.intervalMs * (resting ? 2 : 1));
      return { decision: result.decision, replayed: false };
    } finally { await this.store.release(lease); }
  }
  async observe(canOperate: boolean) {
    const [state, history, schedule] = await Promise.all([this.store.read(), this.store.history(Number.MAX_SAFE_INTEGER, 20, true), this.store.schedule()]);
    return { ...state, history, economy: economics(state.organism.wallet, state.organism.businesses.length), canOperate, serverTime: new Date().toISOString(), schedule, config: { project: 'Project Genesis', planner: this.config.plannerMode !== 'local' && this.config.apiKey ? `openai:${this.config.model}` : 'local-deterministic-v1', internet: this.config.internet, intervalMs: this.config.intervalMs, maxDailyCycles: this.config.maxDailyCycles, schedulerAvailable: this.config.autonomous, brain: { id: this.brainFactory().id, version: 1 } } };
  }
  graph() { const brain = this.brainFactory(); return { id: brain.id, nodes: brain.nodes, edges: brain.edges }; }
}

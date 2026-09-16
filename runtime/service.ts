import type { BrainAdapter, PlannerAdapter, WorldEvent } from '../core/contracts.ts';
import { liveCycle } from '../core/life.ts';
import { economics } from '../core/wallet.ts';
import { LifeStore } from '../server/store.ts';
import type { WalletObserver } from './wallet-observer.ts';
import type { RuntimeConfig } from './config.ts';
export class GenesisService {
  readonly store: LifeStore; readonly config: RuntimeConfig;
  readonly walletObserver?: WalletObserver;
  private brainLabel: string;
  private brainFactory: () => BrainAdapter; private planner: PlannerAdapter;
  constructor(store: LifeStore, config: RuntimeConfig, brainFactory: () => BrainAdapter, planner: PlannerAdapter, walletObserver?: WalletObserver, brainLabel = 'Brain') { this.brainLabel=brainLabel; this.walletObserver=walletObserver; this.store = store; this.config = config; this.brainFactory = brainFactory; this.planner = planner; }
  async advance(id: string, event?: WorldEvent, automatic = false) {
    const previous = await this.store.decision(id); if (previous) return { decision: previous, replayed: true };
    const lease = crypto.randomUUID(), claim = await this.store.claim(lease, automatic, this.config.maxDailyCycles);
    if (!claim) return null;
    try {
      const raced = await this.store.decision(id); if (raced) return { decision: raced, replayed: true };
      const result = await liveCycle(claim.organism, this.brainFactory(), this.planner, { internet: this.config.internet, id, event, externalWallet: (await this.walletObserver?.get())?.account ?? undefined, onPhase: phase => this.store.phase(lease, phase) });
      const resting = ['idle','rest','reflect'].includes(result.decision.plan?.action ?? '');
      await this.store.commit(lease, claim.revision, result.organism, result.decision, automatic, this.config.intervalMs * (resting ? 2 : 1));
      return { decision: result.decision, replayed: false };
    } finally { await this.store.release(lease); }
  }
  async observe(canOperate: boolean) {
    const [state, history, schedule] = await Promise.all([this.store.read(), this.store.history(Number.MAX_SAFE_INTEGER, 20, true), this.store.schedule()]);
    return { ...state, history, externalWallet: await this.walletObserver?.get() ?? null, economy: economics(state.organism.wallet, state.organism.businesses.length), canOperate, serverTime: new Date().toISOString(), schedule, config: { project: 'Project Genesis', planner: this.config.plannerMode !== 'local' && this.config.apiKey ? `openai:${this.config.model}` : 'local-deterministic-v1', internet: this.config.internet, intervalMs: this.config.intervalMs, maxDailyCycles: this.config.maxDailyCycles, schedulerAvailable: this.config.autonomous, walletConnected: !!this.walletObserver, brain: { id: this.brainFactory().id, version: 1 } } };
  }
  graph() { const brain = this.brainFactory(); return { id: brain.id, label: this.brainLabel, nodes: brain.nodes, edges: brain.edges }; }
}

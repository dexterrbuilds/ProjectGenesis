import type { GenesisService } from './service.ts';
/** A container-owned worker. The due time, budget, pause and remaining run live in Postgres. */
export class LifeScheduler {
  private service: GenesisService; private timer?: ReturnType<typeof setTimeout>; private stopping = false;
  private inFlight?: Promise<void>; private pollMs: number;
  constructor(service: GenesisService, pollMs = 1000) { this.service = service; this.pollMs = pollMs; }
  start() { if (this.timer || this.inFlight) return; this.stopping = false; this.queue(); }
  private queue() { if (this.stopping) return; this.timer = setTimeout(() => { this.timer = undefined; this.inFlight = this.tick().finally(() => { this.inFlight = undefined; this.queue(); }); }, this.pollMs); }
  async tick() {
    try {
      await this.service.store.heartbeat();
      if (!this.service.config.autonomous) return;
      const schedule = await this.service.store.schedule();
      if (schedule.enabled && new Date(schedule.next_at).getTime() <= Date.now()) await this.service.advance(crypto.randomUUID(), undefined, true);
    } catch (e) {
      console.error('Genesis autonomous cycle failed:', e instanceof Error ? e.message : 'Unknown error');
      try { await this.service.store.heartbeat('Runtime error; check service logs'); } catch { /* Database may be unavailable. No local state is advanced. */ }
    }
  }
  async stop() { this.stopping = true; if (this.timer) clearTimeout(this.timer); this.timer = undefined; await this.inFlight; }
}

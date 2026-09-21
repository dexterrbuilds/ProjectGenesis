import type { GenesisService } from './service.ts';
/** A container-owned worker. The due time, budget, pause and remaining run live in Postgres. */
export class LifeScheduler {
  private service: GenesisService; private timer?: ReturnType<typeof setTimeout>; private stopping = false;
  private inFlight?: Promise<void>; private pollMs: number;
  constructor(service: GenesisService, pollMs = 1000) { this.service = service; this.pollMs = pollMs; }
  start() { if (this.timer || this.inFlight) return; this.stopping = false; this.queue(); }
  private queue() { if (this.stopping) return; this.timer = setTimeout(() => { this.timer = undefined; this.inFlight = this.tick().finally(() => { this.inFlight = undefined; this.queue(); }); }, this.pollMs); }
  async tick() {
    // All worker classes are off in the reviewed dormant preparation release.
    // No heartbeat write, wallet RPC, life claim, or catch-up cycle.
    await this.service.extension.assertDormant();
  }
  async stop() { this.stopping = true; if (this.timer) clearTimeout(this.timer); this.timer = undefined; await this.inFlight; }
}

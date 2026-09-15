import type pg from 'pg';
import type { Decision, Organism } from '../core/contracts.ts';
import { createOrganism } from '../core/life.ts';
import { ensureIdentity } from '../core/identity.ts';
export type Schedule = { enabled: boolean; remaining_cycles: number | null; next_at: Date; last_heartbeat: Date | null; last_error: string | null };
export type Claim = { organism: Organism; revision: number };
export class LifeStore {
  private db: pg.Pool;
  constructor(db: pg.Pool) { this.db = db; }
  async initialize(startingCents: number) {
    const c = await this.db.connect();
    try {
      await c.query('BEGIN');
      const initial = createOrganism(undefined, undefined, startingCents);
      await c.query('INSERT INTO genesis_organisms(id,state) VALUES($1,$2) ON CONFLICT(id) DO NOTHING', ['genesis', initial]);
      await c.query('INSERT INTO genesis_schedule(id,enabled) VALUES($1,false) ON CONFLICT(id) DO NOTHING', ['genesis']);
      const row = (await c.query('SELECT state FROM genesis_organisms WHERE id=$1 FOR UPDATE', ['genesis'])).rows[0];
      const upgraded = ensureIdentity(row.state);
      await c.query('UPDATE genesis_organisms SET state=$1 WHERE id=$2', [upgraded, 'genesis']);
      for (const m of upgraded.milestones!) await c.query('INSERT INTO genesis_milestones(id,at,record) VALUES($1,$2,$3) ON CONFLICT(id) DO NOTHING', [m.id, m.at, m]);
      await c.query('COMMIT');
    } catch (e) { await c.query('ROLLBACK'); throw e; } finally { c.release(); }
  }
  async read() {
    const r = (await this.db.query('SELECT state,revision,phase,(lease_until>NOW()) AS busy FROM genesis_organisms WHERE id=$1', ['genesis'])).rows[0];
    if (!r) throw new Error('Organism not initialized');
    return { organism: r.state as Organism, revision: Number(r.revision), busy: r.busy as boolean, phase: r.busy ? r.phase as string : 'idle' };
  }
  async history(before = Number.MAX_SAFE_INTEGER, limit = 25, summary = false) {
    const result = await this.db.query(`SELECT ${summary ? "record - 'frames' - 'brainBefore' - 'brainAfter'" : 'record'} AS record FROM genesis_decisions WHERE cycle<$1 ORDER BY cycle DESC LIMIT $2`, [before, Math.min(50, limit)]);
    return result.rows.map(row => row.record as Decision);
  }
  async decision(id: string) { return (await this.db.query('SELECT record FROM genesis_decisions WHERE id=$1', [id])).rows[0]?.record as Decision | undefined ?? null; }
  async schedule(): Promise<Schedule> { return (await this.db.query('SELECT * FROM genesis_schedule WHERE id=$1', ['genesis'])).rows[0]; }
  async claim(token: string, automatic = false, maxDailyCycles = 200): Promise<Claim | null> {
    // Database time and a locked row serialize every process/replica and survive restarts.
    const c = await this.db.connect();
    try {
      await c.query('BEGIN');
      const r = (await c.query('SELECT state,revision,lease_until<=NOW() AS free FROM genesis_organisms WHERE id=$1 FOR UPDATE', ['genesis'])).rows[0];
      const s = (await c.query('SELECT enabled,remaining_cycles,next_at<=NOW() AS due FROM genesis_schedule WHERE id=$1 FOR UPDATE', ['genesis'])).rows[0];
      if (!r || !r.free || r.state.paused || (automatic && (!s.enabled || !s.due || s.remaining_cycles === 0))) { await c.query('ROLLBACK'); return null; }
      const used = Number((await c.query("SELECT count(*) FROM genesis_decisions WHERE at >= date_trunc('day', NOW() AT TIME ZONE 'UTC') AT TIME ZONE 'UTC'")).rows[0].count);
      if (used >= maxDailyCycles) { await c.query("UPDATE genesis_schedule SET last_error='Daily cycle budget reached',next_at=date_trunc('day',NOW() AT TIME ZONE 'UTC') AT TIME ZONE 'UTC'+INTERVAL '1 day' WHERE id=$1", ['genesis']); await c.query('COMMIT'); return null; }
      await c.query("UPDATE genesis_organisms SET lease=$1,lease_until=NOW()+INTERVAL '60 seconds',phase='sensing' WHERE id=$2", [token, 'genesis']);
      await c.query('COMMIT'); return { organism: r.state, revision: Number(r.revision) };
    } catch (e) { await c.query('ROLLBACK'); throw e; } finally { c.release(); }
  }
  async phase(token: string, phase: string) { await this.db.query('UPDATE genesis_organisms SET phase=$1 WHERE id=$2 AND lease=$3', [phase, 'genesis', token]); }
  async release(token: string) { await this.db.query("UPDATE genesis_organisms SET lease=NULL,lease_until='-infinity',phase='idle' WHERE id=$1 AND lease=$2", ['genesis', token]); }
  async commit(token: string, revision: number, organism: Organism, decision: Decision, automatic = false, intervalMs = 30000) {
    const c = await this.db.connect();
    try {
      await c.query('BEGIN');
      const row = (await c.query("SELECT revision,lease,lease_until>NOW() AS valid,state->'paused' AS paused FROM genesis_organisms WHERE id=$1 FOR UPDATE", ['genesis'])).rows[0];
      if (!row || row.lease !== token || !row.valid || Number(row.revision) !== revision) throw new Error('Cycle lease expired; no result committed');
      organism.paused = row.paused;
      await c.query('INSERT INTO genesis_decisions(id,cycle,at,record) VALUES($1,$2,$3,$4)', [decision.id, decision.cycle, decision.at, decision]);
      await this.persistDetails(c, organism, decision.id);
      await c.query("UPDATE genesis_organisms SET state=$1,revision=revision+1,lease=NULL,lease_until='-infinity',phase='idle' WHERE id=$2", [organism, 'genesis']);
      await c.query(`UPDATE genesis_schedule SET next_at=NOW()+$1*INTERVAL '1 millisecond', remaining_cycles=CASE WHEN $2 AND remaining_cycles IS NOT NULL THEN GREATEST(0,remaining_cycles-1) ELSE remaining_cycles END, enabled=CASE WHEN NOT $3 OR ($2 AND remaining_cycles=1) THEN false ELSE enabled END, last_error=$4,updated_at=NOW() WHERE id=$5`, [intervalMs, automatic, decision.outcome.ok, decision.outcome.ok ? null : decision.outcome.title, 'genesis']);
      await c.query('COMMIT');
    } catch (e) { await c.query('ROLLBACK'); throw e; } finally { c.release(); }
  }
  private async persistDetails(c: pg.PoolClient, o: Organism, decisionId?: string) {
    for (const m of o.memory.filter(m => !decisionId || m.sourceDecision === decisionId)) await c.query('INSERT INTO genesis_memories(id,decision_id,at,record) VALUES($1,$2,$3,$4) ON CONFLICT(id) DO NOTHING', [m.id, m.sourceDecision, m.at, m]);
    for (const e of o.wallet.entries) await c.query('INSERT INTO genesis_ledger(id,at,record) VALUES($1,$2,$3) ON CONFLICT(id) DO NOTHING', [e.id, e.at, e]);
    for (const p of o.businesses) await c.query('INSERT INTO genesis_projects(id,record) VALUES($1,$2) ON CONFLICT(id) DO UPDATE SET record=EXCLUDED.record', [p.id, p]);
    for (const m of o.milestones ?? []) await c.query('INSERT INTO genesis_milestones(id,at,record) VALUES($1,$2,$3) ON CONFLICT(id) DO NOTHING', [m.id, m.at, m]);
  }
  async control(patch: { paused?: boolean; enabled?: boolean; remainingCycles?: number | null }) {
    const c = await this.db.connect();
    try {
      await c.query('BEGIN');
      // Same locking order as claim/commit. A current cycle may complete; no next one starts.
      await c.query('SELECT id FROM genesis_organisms WHERE id=$1 FOR UPDATE', ['genesis']);
      if (patch.paused !== undefined) {
        await c.query("UPDATE genesis_organisms SET state=jsonb_set(state,'{paused}',$1::jsonb) WHERE id=$2", [JSON.stringify(patch.paused), 'genesis']);
        // Do not invalidate an in-flight cycle; commit preserves a newly requested pause.
      }
      if (patch.enabled !== undefined) await c.query('UPDATE genesis_schedule SET enabled=$1,remaining_cycles=$2,next_at=NOW(),last_error=NULL,updated_at=NOW() WHERE id=$3', [patch.enabled, patch.remainingCycles ?? null, 'genesis']);
      await c.query('COMMIT');
    } catch (e) { await c.query('ROLLBACK'); throw e; } finally { c.release(); }
  }
  async pause(paused: boolean) { return this.control({ paused }); }
  async heartbeat(error: string | null = null) { await this.db.query('UPDATE genesis_schedule SET last_heartbeat=NOW(),last_error=COALESCE($1,last_error) WHERE id=$2', [error, 'genesis']); }
  async importLife(organism: Organism, decisions: Decision[]) {
    const c = await this.db.connect();
    try {
      await c.query('BEGIN'); await c.query("SELECT pg_advisory_xact_lock(hashtext('project-genesis-import'))");
      if ((await c.query('SELECT id FROM genesis_organisms')).rowCount) throw new Error('Import only into an empty Genesis database; existing life will not be overwritten');
      const o = ensureIdentity(organism);
      await c.query('INSERT INTO genesis_organisms(id,state) VALUES($1,$2)', ['genesis', o]);
      for (const d of decisions) await c.query('INSERT INTO genesis_decisions(id,cycle,at,record) VALUES($1,$2,$3,$4)', [d.id, d.cycle, d.at, d]);
      await this.persistDetails(c, o);
      await c.query('INSERT INTO genesis_schedule(id,enabled) VALUES($1,false)', ['genesis']); await c.query('COMMIT');
    } catch (e) { await c.query('ROLLBACK'); throw e; } finally { c.release(); }
  }
}

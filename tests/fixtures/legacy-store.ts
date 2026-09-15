export interface LegacyStatement { bind(...args: unknown[]): LegacyStatement; first<T>(): Promise<T | null>; all<T>(): Promise<{ results: T[] }>; run(): Promise<{ meta: { changes: number } }> }
export interface D1Database { prepare(sql: string): LegacyStatement; batch(queries: LegacyStatement[]): Promise<{meta:{changes:number}}[]> }
import type { Decision, Organism } from '../../core/contracts.ts';
import { createOrganism } from '../../core/life.ts';
type Row = { state: string; revision: number; lease: string | null; lease_until: number };
export class LifeStore {
  private db: D1Database;
  constructor(db: D1Database) { this.db = db; }
  async initialize(startingCents: number) {
    const initial = createOrganism(undefined, undefined, startingCents);
    await this.db.prepare('INSERT OR IGNORE INTO organisms(id,state,revision,lease_until) VALUES(?,?,0,0)').bind('genesis', JSON.stringify(initial)).run();
  }
  async read() {
    const row = await this.db.prepare('SELECT state, revision, lease, lease_until FROM organisms WHERE id=?').bind('genesis').first<Row>();
    if (!row) throw new Error('Organism not initialized');
    return { organism: JSON.parse(row.state) as Organism, revision: row.revision, busy: row.lease_until > Date.now() };
  }
  async history(before = Number.MAX_SAFE_INTEGER, limit = 25) {
    const result = await this.db.prepare('SELECT record FROM decisions WHERE cycle < ? ORDER BY cycle DESC LIMIT ?').bind(before, limit).all<{ record: string }>();
    return result.results.map(row => JSON.parse(row.record) as Decision);
  }
  async decision(id: string) {
    const row = await this.db.prepare('SELECT record FROM decisions WHERE id=?').bind(id).first<{ record: string }>();
    return row ? JSON.parse(row.record) as Decision : null;
  }
  async claim(token: string) {
    const r = await this.db.prepare('UPDATE organisms SET lease=?,lease_until=? WHERE id=? AND lease_until < ? RETURNING state,revision').bind(token, Date.now() + 60000, 'genesis', Date.now()).first<{ state: string; revision: number }>();
    return r ? { organism: JSON.parse(r.state) as Organism, revision: r.revision } : null;
  }
  async release(token: string) { await this.db.prepare('UPDATE organisms SET lease=NULL,lease_until=0 WHERE id=? AND lease=?').bind('genesis', token).run(); }
  async commit(token: string, revision: number, organism: Organism, decision: Decision) {
    // D1 batches are transactional. Insert only while the exact lease/version is held;
    // then update the same row. Unique decision/cycle keys reject duplicate commits.
    const results = await this.db.batch([
      this.db.prepare('INSERT INTO decisions(id,cycle,at,record) SELECT ?,?,?,? FROM organisms WHERE id=? AND lease=? AND revision=? AND lease_until>=?').bind(decision.id, decision.cycle, decision.at, JSON.stringify(decision), 'genesis', token, revision, Date.now()),
      this.db.prepare('UPDATE organisms SET state=?,revision=revision+1,lease=NULL,lease_until=0 WHERE id=? AND lease=? AND revision=? AND EXISTS(SELECT 1 FROM decisions WHERE id=?)').bind(JSON.stringify(organism), 'genesis', token, revision, decision.id),
    ]);
    if (results.some(r => r.meta.changes !== 1)) throw new Error('Cycle lease expired; result was not committed');
  }
  async pause(paused: boolean) {
    const result = await this.db.prepare("UPDATE organisms SET state=json_set(state,'$.paused',json(?)),revision=revision+1 WHERE id=? AND lease_until<?").bind(JSON.stringify(paused), 'genesis', Date.now()).run();
    if (result.meta.changes !== 1) throw new Error('A cycle is running; pause after it completes');
  }
}

import test from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import { readFileSync, mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { LifeStore, type D1Database } from './fixtures/legacy-store.ts';
import { CElegansBrain } from '../core/brain/celegans.ts';
import { liveCycle } from '../core/life.ts';
import { LocalPlanner } from '../core/planner.ts';

// Exercise the real SQL and file persistence; this wrapper only matches D1's API.
function d1(sqlite: DatabaseSync): D1Database {
  const wrap = (query: string, args: unknown[] = []) => ({
    bind: (...values: unknown[]) => wrap(query, values),
    first: async () => sqlite.prepare(query).get(...args as never[]) ?? null,
    all: async () => ({ results: sqlite.prepare(query).all(...args as never[]) }),
    run: async () => ({ meta: { changes: Number(sqlite.prepare(query).run(...args as never[]).changes) } }),
  });
  return { prepare: wrap, batch: async (queries: { run(): Promise<unknown> }[]) => {
    sqlite.exec('BEGIN'); try { const r = []; for (const q of queries) r.push(await q.run()); sqlite.exec('COMMIT'); return r; } catch (e) { sqlite.exec('ROLLBACK'); throw e; }
  } } as unknown as D1Database;
}
test('SQLite persists identity and neural state; lease serializes cycles; trace commits atomically', async () => {
  const dir = mkdtempSync(join(tmpdir(), 'genesis-test-')), path = join(dir, 'life.sqlite');
  let db = new DatabaseSync(path);
  try {
    db.exec(readFileSync(new URL('./fixtures/legacy-schema.sql', import.meta.url), 'utf8'));
    let store = new LifeStore(d1(db)); await store.initialize(10000);
    const original = await store.read(); const a = await store.claim('a'); assert(a); assert.equal(await store.claim('b'), null);
    const result = await liveCycle(a.organism, new CElegansBrain(), new LocalPlanner(), { internet: false, id: 'cycle-00001' });
    await store.commit('a', a.revision, result.organism, result.decision);
    assert.equal((await store.history()).length, 1); assert.equal((await store.read()).organism.cycles, 1);
    db.close(); db = new DatabaseSync(path); store = new LifeStore(d1(db)); await store.initialize(20000);
    const restored = await store.read(); assert.equal(restored.organism.id, original.organism.id); assert.equal(restored.organism.wallet.startingCents, 10000);
    assert.deepEqual(restored.organism.brain, result.organism.brain);
    const b = await store.claim('b'); assert(b);
    await assert.rejects(store.commit('wrong-token', b.revision, result.organism, { ...result.decision, id: 'bad-lease' }));
    assert.equal((await store.history()).length, 1);
    await store.release('b'); await store.pause(true); assert.equal((await store.read()).organism.paused, true);
    assert.equal((await store.decision('cycle-00001'))?.id, 'cycle-00001'); assert.equal((await store.history(1)).length, 0);
  } finally { db.close(); rmSync(dir, { recursive: true, force: true }); }
});

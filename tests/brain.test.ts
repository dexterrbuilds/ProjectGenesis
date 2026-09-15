import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import data from '../data/connectome.json' with { type: 'json' };
import { CElegansBrain } from '../core/brain/celegans.ts';
import { DEMO_EVENTS, encodeEvent } from '../core/sensory.ts';
const stimulus = (key: string) => encodeEvent({ id: key, ...DEMO_EVENTS[key] });

test('pinned data integrity, 302 unique biological names, real edges and unique electrical pairs', () => {
  assert.equal(data.neurons.length, 302); assert.equal(new Set(data.neurons.map(n => n.id)).size, 302);
  assert.equal(data.edges.filter(e => e.kind === 'chemical').length, 3709);
  assert.equal(data.edges.filter(e => e.kind === 'gap').length, 1091);
  assert(data.edges.some(e => e.source === 'ASHL' && e.target === 'AVAL'));
  for (const [file, hash] of Object.entries(data.provenance.sourceSha256)) assert.equal(createHash('sha256').update(readFileSync(new URL('../data/source/' + file, import.meta.url))).digest('hex'), hash);
  const seen = new Set(); for (const e of data.edges) { const k = e.kind + ':' + e.source + ':' + e.target; assert(!seen.has(k)); seen.add(k); }
});
test('silent brain is silent; input reaches downstream cells only through real connectivity', () => {
  const b = new CElegansBrain(); assert.equal(b.step(80).activity.reduce((a, x) => a + x, 0), 0);
  b.stimulate(stimulus('danger')); b.step(80);
  const disconnected = new CElegansBrain([]); disconnected.stimulate(stimulus('danger')); disconnected.step(80);
  assert.equal(disconnected.decodeBehavior().behavior, 'WAIT');
  assert.notEqual(b.decodeBehavior().behavior, 'WAIT');
  assert(b.decodeBehavior().scores.reverse > 0);
  assert.equal(disconnected.decodeBehavior().scores.reverse, 0);
});
test('deterministic replay and persistent snapshot continuation', () => {
  const a = new CElegansBrain(), b = new CElegansBrain();
  a.stimulate(stimulus('novelty')); b.stimulate(stimulus('novelty'));
  assert.deepEqual(a.step(40), b.step(40));
  const c = new CElegansBrain(); c.initialize(JSON.parse(JSON.stringify(a.snapshot())));
  assert.deepEqual(a.step(40), c.step(40)); assert.deepEqual(a.decodeBehavior(), c.decodeBehavior());
});
test('bounded dynamics over repeated mixed stimulation and invalid inputs fail closed', () => {
  const b = new CElegansBrain();
  for (let i = 0; i < 100; i++) { b.stimulate(stimulus(i % 2 ? 'danger' : 'opportunity')); assert(b.step(80).activity.every(v => Number.isFinite(v) && v >= 0 && v <= 1)); }
  assert.throws(() => b.stimulate({ ...stimulus('quiet'), danger: NaN }));
  assert.throws(() => b.initialize({ adapter: 'other-species', version: 1, payload: {} }));
});
test('different inputs produce distinct downstream responses, not merely sensory lights', () => {
  const values = ['opportunity', 'danger', 'novelty'].map(key => { const b = new CElegansBrain(); b.stimulate(stimulus(key)); b.step(80); return b.decodeBehavior(); });
  assert.equal(new Set(values.map(x => x.behavior)).size, 3);
});

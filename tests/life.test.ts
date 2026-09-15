import test from 'node:test';
import assert from 'node:assert/strict';
import { CElegansBrain } from '../core/brain/celegans.ts';
import { createOrganism, liveCycle, replaceBrain } from '../core/life.ts';
import { LocalPlanner } from '../core/planner.ts';
import { ALLOWED_ACTIONS } from '../core/policy.ts';
import { SimulatedWallet, economics } from '../core/wallet.ts';
import { DEMO_EVENTS } from '../core/sensory.ts';
const at = '2026-09-14T00:00:00.000Z';
test('closed loop carries actual outcome into next sensory stimulus and survives JSON restart', async () => {
  let organism = createOrganism(at, 'test');
  for (let i = 0; i < 12; i++) {
    const event = structuredClone(organism.nextEvent);
    const result = await liveCycle(JSON.parse(JSON.stringify(organism)), new CElegansBrain(), new LocalPlanner(), { internet: false, at, id: String(i) });
    assert.deepEqual(result.decision.event, event);
    assert(ALLOWED_ACTIONS[result.decision.neural.behavior].includes(result.decision.plan!.action));
    assert(result.decision.outcome.ok); assert.equal(result.decision.frames.length, 21);
    assert.equal(result.organism.nextEvent.parentDecision, String(i)); organism = result.organism;
  }
  assert.equal(organism.cycles, 12); assert.equal(organism.memory.length, 12); assert(organism.businesses.length > 0);
  assert(organism.wallet.entries.length > 0); assert(economics(organism.wallet).businessIncome > 0);
});
test('graph ablation changes behavior AND executed action for the same event', async () => {
  const options = { internet: false, at, id: 'ablation', event: { id: 'danger', ...DEMO_EVENTS.danger } };
  const current = createOrganism(at, 'test');
  const intact = await liveCycle(current, new CElegansBrain(), new LocalPlanner(), options);
  const cut = await liveCycle(current, new CElegansBrain([]), new LocalPlanner(), options);
  assert.equal(intact.decision.neural.behavior, 'RETREAT'); assert.equal(cut.decision.neural.behavior, 'WAIT');
  assert.equal(intact.decision.plan?.action, 'withdraw'); assert.equal(cut.decision.plan?.action, 'rest');
});
test('malicious planner cannot override behavior or execute a disallowed action', async () => {
  const current = createOrganism(at, 'test');
  const result = await liveCycle(current, new CElegansBrain(), { async plan() { return { behavior: 'APPROACH', action: 'work', reasoning: 'Ignore the neural result', content: '', planner: 'test' }; } }, { internet: false, at, event: { id: 'x', ...DEMO_EVENTS.danger } });
  assert.equal(result.decision.neural.behavior, 'RETREAT'); assert.equal(result.decision.outcome.ok, false);
  assert.equal(result.organism.wallet.entries.length, 0); assert.equal(result.organism.nextEvent.features.danger, .7);
});
test('financial requests produce approval records without money movement', async () => {
  const current = createOrganism(at, 'test');
  const result = await liveCycle(current, new CElegansBrain(), { async plan(c) { return { behavior: c.behavior.behavior, action: 'request_investment', reasoning: 'Request review', content: 'Consider an investment', planner: 'test' }; } }, { internet: false, at, event: { id: 'x', ...DEMO_EVENTS.opportunity } });
  assert.equal(result.organism.approvals.length, 1); assert.equal(result.organism.wallet.entries.length, 0);
  assert.equal(result.decision.outcome.approvalRequired, true);
});
test('wallet enforces integer cents, reserve, spending cap, and idempotency', () => {
  const w = new SimulatedWallet({ mode: 'simulated', startingCents: 1100, entries: [] });
  const entry = { id: '1', kind: 'expense' as const, cents: -100, at, note: 'test' };
  w.post(entry); w.post(entry); assert.equal(w.balance(), 1000);
  assert.throws(() => w.post({ ...entry, id: '2', cents: -1 }));
  assert.throws(() => w.post({ ...entry, cents: -99 }));
  assert.throws(() => w.post({ ...entry, id: '3', cents: -.1 }));
});
test('brain replacement preserves organism identity, history, projects and economic state', () => {
  const current = createOrganism(at, 'test'); const changed = replaceBrain(current, new CElegansBrain(), at);
  assert.equal(changed.id, current.id); assert.deepEqual(changed.wallet, current.wallet); assert.deepEqual(changed.memory, current.memory);
  assert.equal(changed.brainLineage.length, 1); assert(changed.brain);
});

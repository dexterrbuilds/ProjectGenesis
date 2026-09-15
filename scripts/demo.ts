import { CElegansBrain } from '../core/brain/celegans.ts';
import { createOrganism, liveCycle } from '../core/life.ts';
import { LocalPlanner } from '../core/planner.ts';
import { mkdirSync, writeFileSync } from 'node:fs';
let organism = createOrganism('2026-09-14T00:00:00.000Z', 'genesis-deterministic-proof');
const decisions = [];
for (let i = 0; i < 12; i++) {
  const result = await liveCycle(organism, new CElegansBrain(), new LocalPlanner(), { internet: false, id: `proof-${i}`, at: `2026-09-14T00:${String(i).padStart(2, '0')}:00.000Z` });
  organism = result.organism; decisions.push(result.decision);
  console.log(`${i + 1}. ${result.decision.neural.behavior} → ${result.decision.plan?.action} → ${result.decision.outcome.title}`);
}
mkdirSync('outputs', { recursive: true }); writeFileSync('outputs/deterministic-proof.json', JSON.stringify({ organism, decisions }, null, 2));

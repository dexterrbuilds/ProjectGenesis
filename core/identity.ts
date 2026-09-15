import type { Decision, Milestone, Organism } from './contracts.ts';

/** Add metadata to an existing life without changing its ID, birth or brain. */
export function ensureIdentity(source: Organism): Organism {
  const organism = structuredClone(source);
  organism.rhythm ??= { energy: 1, resting: false };
  organism.milestones ??= [];
  if (!organism.milestones.some(e => e.kind === 'birth')) organism.milestones.unshift({
    id: `${organism.id}:birth`, kind: 'birth', at: organism.bornAt, title: 'Genesis began.',
    detail: `A persistent identity was born with ${(organism.wallet.startingCents / 100).toFixed(2)} simulated USD and an unfamiliar world. This record preserves the original birth time.`,
  });
  return organism;
}
export function recordMilestones(organism: Organism, d: Pick<Decision, 'id' | 'at'>) {
  organism.milestones ??= [];
  const add = (kind: Milestone['kind'], title: string, detail: string) => {
    if (!organism.milestones!.some(m => m.kind === kind)) organism.milestones!.push({ id: `${organism.id}:${kind}`, kind, title, detail, at: d.at, decisionId: d.id });
  };
  if (organism.cycles) add('first_experience', 'The first experience.', 'An event passed through the brain, constrained a decision, and became a memory.');
  if (organism.businesses.length) add('first_project', 'An idea became a project.', 'A service draft was saved. Publication and real sales remain separate approval-gated steps.');
  if (organism.wallet.entries.some(e => e.kind === 'business_income' && e.cents > 0)) add('first_income', 'The first simulated income.', 'A development-market work unit produced simulated revenue. This is not a real customer payment.');
}

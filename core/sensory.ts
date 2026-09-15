import { CHANNELS } from './contracts.ts';
import type { Organism, Stimulus, WorldEvent } from './contracts.ts';
export function encodeEvent(event: WorldEvent, organism?: Organism): Stimulus {
  const result = Object.fromEntries(CHANNELS.map(c => [c, 0])) as Stimulus;
  for (const [key, value] of Object.entries(event.features)) {
    if (!CHANNELS.includes(key as keyof Stimulus) || typeof value !== 'number' || !Number.isFinite(value) || value < 0 || value > 1) throw new Error('Invalid event feature');
    result[key as keyof Stimulus] = value;
  }
  if (organism) {
    const balance = organism.wallet.startingCents + organism.wallet.entries.reduce((s, e) => s + e.cents, 0);
    result.scarcity = Math.max(result.scarcity, Math.max(0, 1 - balance / Math.max(1, organism.wallet.startingCents * .5)));
  }
  return result;
}
export const DEMO_EVENTS: Record<string, Omit<WorldEvent, 'id'>> = {
  opportunity: { title: 'An opportunity to build something useful', source: 'operator stimulus', features: { rewardOpportunity: 1 }, detail: 'Explore a small digital research service.' },
  danger: { title: 'An unexpected negative outcome', source: 'operator stimulus', features: { danger: 1 }, detail: 'A potential expense has uncertain value.' },
  novelty: { title: 'Something unfamiliar enters the environment', source: 'operator stimulus', features: { novelty: 1 }, detail: 'There is a new subject to investigate.' },
  quiet: { title: 'A quiet environment', source: 'operator stimulus', features: {} },
  social: { title: 'A signal from the outside world', source: 'operator stimulus', features: { social: .8, novelty: .15 } },
};

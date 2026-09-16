import type { WalletAccount } from './economy/adapters.ts';
import type { BrainAdapter, Decision, Organism, Outcome, Plan, PlannerAdapter, WorldEvent } from './contracts.ts';
import { encodeEvent } from './sensory.ts';
import { ALLOWED_ACTIONS, LIMITS, validatePlan } from './policy.ts';
import { economics, SimulatedWallet } from './wallet.ts';
import { ensureIdentity, recordMilestones } from './identity.ts';

export const READINGS = [
  { title: 'OpenWorm: an open science project', url: 'https://openworm.org/', excerpt: 'OpenWorm builds computational models of C. elegans. Its code, data and models are distributed openly. A structural wiring diagram constrains a model but does not specify every physiological parameter.' },
  { title: 'A small service should have a testable deliverable', url: null, excerpt: 'Genesis working note: define one audience, one useful output, and one way to ask whether the output helped. Save drafts and evidence before spending capital. A draft is not an operating business or proof of demand.' },
  { title: 'Anatomy and behavior', url: 'https://openworm.org/ConnectomeToolbox/', excerpt: 'Connectome datasets describe connectivity at different developmental stages and from different reconstructions. Comparing datasets requires attention to neuron identity and the meaning of edge weights.' },
];
export type ToolOptions = { internet: boolean; fetcher?: typeof fetch };
export function createOrganism(at = new Date().toISOString(), id = crypto.randomUUID(), startingCents = 10000): Organism {
  const wallet = new SimulatedWallet({ mode: 'simulated', startingCents, entries: [] });
  return ensureIdentity({ id, name: 'Genesis', bornAt: at, cycles: 0, activity: 'Ready for its first experience', paused: false, drives: ['Preserve enough capital to continue', 'Learn from outcomes', 'Create useful work', 'Become economically self-sustaining'], wallet: wallet.getState(), memory: [], businesses: [], approvals: [], brain: null, brainLineage: [], nextEvent: { id: 'birth', title: 'An unfamiliar world, and room to explore', source: 'birth', features: { novelty: .8, rewardOpportunity: .2 } } });
}
export function replaceBrain(organism: Organism, brain: BrainAdapter, at: string): Organism {
  const next = ensureIdentity(organism); brain.initialize(); next.brain = brain.snapshot(); next.brainLineage.push({ adapter: brain.id, at }); next.milestones!.push({ id: `${next.id}:brain:${next.brainLineage.length}`, kind: 'brain_change', at, title: 'A new brain, the same life.', detail: `Brain adapter ${brain.id} initialized. Identity, money and memories retained.` }); return next;
}
async function readInternet(url: string, fetcher: typeof fetch): Promise<string> {
  // No model-supplied URLs, redirects, local network access, or arbitrary tools.
  const response = await fetcher(url, { redirect: 'error', signal: AbortSignal.timeout(8000), headers: { 'User-Agent': 'GenesisHackathon/0.1 (read-only research)' } });
  if (!response.ok || !response.body) throw new Error(`Reading returned HTTP ${response.status}`);
  const reader = response.body.getReader(); const decoder = new TextDecoder(); let text = ''; let bytes = 0;
  try { while (true) { const part = await reader.read(); if (part.done) break; bytes += part.value.length; if (bytes > 150000) break; text += decoder.decode(part.value, { stream: true }); } }
  finally { await reader.cancel(); }
  return text.replace(/<script[\s\S]*?<\/script>/gi, '').replace(/<style[\s\S]*?<\/style>/gi, '').replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 5000);
}
export async function executeTool(plan: Plan, organism: Organism, decisionId: string, at: string, options: ToolOptions): Promise<Outcome> {
  const action = plan.action;
  if (action === 'manage_resources') {
    const e = economics(organism.wallet, organism.businesses.length);
    return { ok: true, title: 'Made room for the next chapter', detail: `Reviewed ${organism.businesses.length} projects, ${(e.cash / 100).toFixed(2)} simulated USD in cash, and a ${(LIMITS.reserveCents / 100).toFixed(2)} reserve. No funds moved. ${plan.content}`, simulated: true, features: { novelty: .55, uncertainty: e.cash < LIMITS.reserveCents + 25 ? .35 : .1 } };
  }
  if (action === 'idle') return { ok: true, title: 'Letting the world pass for a moment', detail: 'Genesis retained its neural impulse and chose not to use a tool or spend resources this cycle.', simulated: false, features: {} };
  if (action.startsWith('request_')) {
    organism.approvals.push({ id: `${decisionId}:approval`, action, content: plan.content, status: 'pending', decision: decisionId });
    return { ok: true, title: 'Waiting for a human decision', detail: 'A request was saved. No external action has been executed.', simulated: false, approvalRequired: true, features: { uncertainty: .2 } };
  }
  if (action === 'draft_message') return { ok: true, title: 'A message drafted, awaiting human review', detail: plan.content, artifact: plan.content, simulated: false, features: { social: .25 } };
  if (action === 'research' || action === 'read' || action === 'learn') {
    const reading = READINGS[organism.cycles % READINGS.length];
    const live = options.internet && action === 'research' && reading.url;
    const content = live ? await readInternet(reading.url!, options.fetcher ?? fetch) : reading.excerpt;
    return { ok: true, title: `${action === 'learn' ? 'Learned' : 'Read'}: ${reading.title}`, detail: content, sourceUrl: reading.url ?? undefined, simulated: false, artifact: content, features: { rewardOpportunity: 1 } };
  }
  if (action === 'draft_service') {
    organism.businesses.push({ id: decisionId, name: `Signal Notes ${organism.businesses.length + 1}`, artifact: plan.content, status: 'draft', workCycles: 0, earnedCents: 0 });
    return { ok: true, title: 'Created a research-service draft', detail: 'The service exists as a saved artifact. It has not been published or sold.', artifact: plan.content, simulated: false, features: { rewardOpportunity: .9, novelty: .1 } };
  }
  if (action === 'work') {
    const business = organism.businesses[0]; if (!business) throw new Error('No project is available to work on');
    const wallet = new SimulatedWallet(organism.wallet);
    wallet.post({ id: decisionId + ':cost', at, kind: 'expense', cents: -25, note: 'Simulated production cost' });
    business.workCycles++; business.status = 'working'; business.artifact = plan.content;
    // Explicit deterministic development market, not real sales or fabricated external customers.
    const earned = business.workCycles % 3 === 0 ? 150 : 0;
    if (earned) wallet.post({ id: decisionId + ':revenue', at, kind: 'business_income', cents: earned, note: 'Simulated market: completed third work unit' });
    business.earnedCents += earned; organism.wallet = wallet.getState();
    return { ok: true, title: earned ? 'Completed a work unit; simulated income received' : 'Worked on a service draft', detail: `Saved a work artifact. Simulated cost $0.25; simulated revenue $${(earned / 100).toFixed(2)}.`, artifact: plan.content, simulated: true, features: earned ? { acquisition: .8, rewardOpportunity: .4 } : { rewardOpportunity: .75, uncertainty: .1 } };
  }
  if (action === 'withdraw' || action === 'review_risk') return { ok: true, title: action === 'withdraw' ? 'Stepped back from the opportunity' : 'Reviewed the risk before proceeding', detail: plan.content, simulated: false, features: { danger: .05, novelty: .65 } };
  return { ok: true, title: action === 'rest' ? 'Rested without spending capital' : 'Reflected on recent experiences', detail: plan.content, simulated: false, features: { novelty: .35 } };
}

export async function liveCycle(current: Organism, brain: BrainAdapter, planner: PlannerAdapter, options: ToolOptions & { externalWallet?: WalletAccount; event?: WorldEvent; at?: string; id?: string; onPhase?: (phase: string) => Promise<void> }): Promise<{ organism: Organism; decision: Decision }> {
  if (current.paused) throw new Error('Organism is paused');
  const organism = ensureIdentity(current), at = options.at ?? new Date().toISOString(), id = options.id ?? crypto.randomUUID();
  if (organism.brain) brain.initialize(organism.brain); else { brain.initialize(); organism.brainLineage.push({ adapter: brain.id, at }); }
  const event = options.event ?? organism.nextEvent;
  const stimulus = encodeEvent(event, organism), brainBefore = brain.snapshot();
  const encoding = brain.stimulate(stimulus), frames = [brain.getState()];
  await options.onPhase?.('neural integration');
  for (let i = 0; i < LIMITS.cycleSteps / 4; i++) frames.push(brain.step(4));
  const neural = brain.decodeBehavior(); let plan: Plan | null = null; let outcome: Outcome;
  try {
    await options.onPhase?.('reasoning');
    plan = await planner.plan({ behavior: neural, event, externalWallet: options.externalWallet, organism: structuredClone(organism), allowedActions: ALLOWED_ACTIONS[neural.behavior] });
    validatePlan(plan, neural.behavior);
    await options.onPhase?.('acting');
    // Tool mutations are staged. A failed tool cannot partially change economic state.
    const staged = structuredClone(organism);
    outcome = await executeTool(plan, staged, id, at, options);
    Object.assign(organism, staged);
  } catch (error) {
    outcome = { ok: false, title: 'Action blocked or failed', detail: error instanceof Error ? error.message : 'Unknown action failure', simulated: false, features: { danger: .7, uncertainty: .5 } };
  }
  organism.cycles++; organism.brain = brain.snapshot(); organism.activity = outcome.title;
  const resting = outcome.ok && ['idle', 'rest', 'reflect'].includes(plan?.action ?? '');
  organism.rhythm!.energy = Math.max(0, Math.min(1, organism.rhythm!.energy + (resting ? .2 : -.13)));
  if (organism.rhythm!.energy <= .2) organism.rhythm!.resting = true;
  if (organism.rhythm!.energy >= .8) organism.rhythm!.resting = false;
  const nextEvent: WorldEvent = { id: id + ':outcome', parentDecision: id, source: 'previous action outcome', title: outcome.title, detail: outcome.detail, features: outcome.features };
  organism.nextEvent = nextEvent;
  organism.memory.push({ id: id + ':memory', at, sourceDecision: id, salience: outcome.ok ? .5 : .9, text: `${neural.behavior} → ${plan?.action ?? 'no plan'}: ${outcome.title}. ${outcome.detail.slice(0, 1500)}` });
  organism.memory = organism.memory.slice(-80); // Full original experiences remain in append-only decisions.
  recordMilestones(organism, { id, at });
  return { organism, decision: { ...(options.externalWallet ? { externalWallet: structuredClone(options.externalWallet) } : {}), id, at, cycle: organism.cycles, event, stimulus, encoding, brainBefore, frames, neural, plan, outcome, nextEvent, brainAfter: organism.brain } };
}

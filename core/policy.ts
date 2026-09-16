import type { Action, Behavior, Plan } from './contracts.ts';
export const ALLOWED_ACTIONS: Record<Behavior, readonly Action[]> = {
  APPROACH: ['manage_resources', 'draft_service', 'work', 'learn', 'draft_message', 'request_payment', 'request_investment', 'request_hire', 'request_publish', 'request_physical', 'idle'],
  EXPLORE: ['research', 'read', 'learn', 'draft_message', 'idle'],
  AVOID: ['manage_resources', 'review_risk', 'reflect', 'idle'],
  RETREAT: ['withdraw', 'review_risk', 'rest', 'idle'],
  WAIT: ['rest', 'reflect', 'idle'],
};
export function validatePlan(plan: Plan, behavior: Behavior) {
  if (!plan || plan.behavior !== behavior || !ALLOWED_ACTIONS[behavior].includes(plan.action)) throw new Error('Planner violated the neural behavior constraint');
  if (typeof plan.reasoning !== 'string' || !plan.reasoning.trim() || plan.reasoning.length > 3000 || typeof plan.content !== 'string' || plan.content.length > 12000) throw new Error('Invalid structured plan');
}
export const LIMITS = { maxExpenseCents: 100, reserveCents: 1000, maxInvestmentCents: 500, maxCyclesPerRun: 100, cycleSteps: 80 };

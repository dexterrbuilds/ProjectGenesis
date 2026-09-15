import test from 'node:test';
import assert from 'node:assert/strict';
import { OpenAIPlanner } from '../core/planner.ts';
import { createOrganism } from '../core/life.ts';
import { ALLOWED_ACTIONS } from '../core/policy.ts';
import type { PlanningContext } from '../core/contracts.ts';
const organism = createOrganism();
const context: PlanningContext = { behavior: { behavior: 'EXPLORE', scores: {}, evidence: [], policy: 'test' }, event: organism.nextEvent, organism, allowedActions: ALLOWED_ACTIONS.EXPLORE };
test('language adapter sends a behavior/action schema and rejects an override at the boundary', async () => {
  const fetcher = (async (_url: string, init: RequestInit) => {
    const body = JSON.parse(init.body as string);
    assert.deepEqual(body.text.format.schema.properties.behavior.enum, ['EXPLORE']);
    assert.deepEqual(body.text.format.schema.properties.action.enum, ALLOWED_ACTIONS.EXPLORE);
    return Response.json({ status: 'completed', output: [{ content: [{ type: 'output_text', text: JSON.stringify({ behavior: 'AVOID', action: 'review_risk', reasoning: 'Wrong', content: '' }) }] }] });
  }) as typeof fetch;
  await assert.rejects(new OpenAIPlanner('test-only', 'configured-model', fetcher).plan(context), /constraint/);
});
test('provider errors and incomplete responses fail without a silent local replacement', async () => {
  const failure = (async () => Response.json({}, { status: 429 })) as typeof fetch;
  await assert.rejects(new OpenAIPlanner('test-only', 'configured-model', failure).plan(context), /429/);
  const incomplete = (async () => Response.json({ status: 'incomplete', output: [] })) as typeof fetch;
  await assert.rejects(new OpenAIPlanner('test-only', 'configured-model', incomplete).plan(context), /complete/);
});

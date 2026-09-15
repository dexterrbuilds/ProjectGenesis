import test from 'node:test';
import assert from 'node:assert/strict';
import { createOrganism, liveCycle, replaceBrain } from '../core/life.ts';
import { ensureIdentity } from '../core/identity.ts';
import { LocalPlanner } from '../core/planner.ts';
import { CElegansBrain } from '../core/brain/celegans.ts';
import { DEMO_EVENTS } from '../core/sensory.ts';
import { readConfig } from '../runtime/config.ts';
import { requestFinancialAction, ClawPumpFeeIncomeAdapter } from '../core/economy/adapters.ts';
import type { AssetAmount } from '../core/economy/adapters.ts';
test('birth is immutable and migration adds no invented neural decision', () => {
  const o = createOrganism('2026-09-14T00:00:00.000Z','genesis-original'); delete o.milestones;
  const upgraded = ensureIdentity(o), again = ensureIdentity(upgraded);
  assert.equal(again.milestones!.length,1); assert.equal(again.milestones![0].at,o.bornAt);
  assert.equal(again.cycles,0); assert.equal(again.brain,null); assert.equal(again.id,o.id);
});
test('rest can abstain without overriding the brain or spending money', async () => {
  const o = createOrganism(); o.rhythm = { energy:.1,resting:true };
  const r = await liveCycle(o,new CElegansBrain(),new LocalPlanner(),{internet:false,event:{id:'danger',...DEMO_EVENTS.danger}});
  assert.equal(r.decision.neural.behavior,'RETREAT'); assert.equal(r.decision.plan?.behavior,'RETREAT'); assert.equal(r.decision.plan?.action,'idle');
  assert.deepEqual(r.organism.wallet,o.wallet); assert(r.organism.rhythm!.energy > o.rhythm.energy); assert.equal(r.organism.milestones!.length,2);
});
test('brain upgrade keeps birth, milestones, identity, finances and memory', () => {
  const o=createOrganism(), original=structuredClone(o); const b=new CElegansBrain();
  const next=replaceBrain(o,b,'2026-09-15T00:00:00.000Z');
  assert.equal(next.id,o.id); assert.equal(next.bornAt,o.bornAt); assert.deepEqual(next.memory,o.memory); assert.deepEqual(next.wallet,o.wallet); assert.deepEqual(o,original);
  assert.equal(next.milestones!.at(-1)?.kind,'brain_change');
});
test('credentials select real planner; partial configuration fails instead of silently falling back', () => {
  const env={DATABASE_URL:'postgresql://localhost/genesis',GENESIS_OPERATOR_TOKEN:'test-token-at-least-24-chars'};
  assert.equal(readConfig(env).plannerMode,'auto');
  assert.equal(readConfig({...env,OPENAI_API_KEY:'test-key',OPENAI_MODEL:'configured-model'}).apiKey,'test-key');
  assert.throws(()=>readConfig({...env,OPENAI_API_KEY:'test-key'}));
  assert.throws(()=>readConfig({...env,GENESIS_PLANNER_MODE:'openai'}));
  assert.throws(()=>readConfig({...env,DATABASE_URL:''}));
});
test('external financial adapter keeps atomic assets separate and requires approval', async () => {
  const amount:AssetAmount={asset:{chain:'solana',network:'devnet',mint:'native',symbol:'SOL',decimals:9},atomicUnits:'1000000'};
  const intent={id:'intent',kind:'transfer' as const,recipient:'test-recipient',amount,rationale:'Human review required'};
  assert.equal(requestFinancialAction(intent,amount).status,'pending');
  assert.throws(()=>requestFinancialAction({...intent,amount:{...amount,atomicUnits:'1000001'}},amount));
  assert.throws(()=>requestFinancialAction({...intent,amount:{...amount,asset:{...amount.asset,network:'mainnet-beta'}}},amount));
  const fees=new ClawPumpFeeIncomeAdapter({async poll(){return {receipts:[{id:'fee',source:'clawpump_fee',transaction:'test-tx',recipient:'wrong',amount,finalized:true,at:new Date().toISOString()}]}}},'expected');
  await assert.rejects(fees.poll(),/mismatched/);
});

/** A real provider check using a fresh brain; never reads or mutates Genesis's database. */
import { CElegansBrain } from '../core/brain/celegans.ts';
import { createOrganism } from '../core/life.ts';
import { encodeEvent } from '../core/sensory.ts';
import { OpenAIPlanner } from '../core/planner.ts';
import { ALLOWED_ACTIONS, LIMITS, validatePlan } from '../core/policy.ts';
if (!process.env.OPENAI_API_KEY || !process.env.OPENAI_MODEL) {
  console.error('Live LLM check unavailable: configure OPENAI_API_KEY and OPENAI_MODEL on the runtime. No request was sent.');
  process.exitCode = 1;
} else {
  try {
    const organism = createOrganism(), brain = new CElegansBrain(); brain.initialize();
    brain.stimulate(encodeEvent(organism.nextEvent, organism)); brain.step(LIMITS.cycleSteps);
    const behavior = brain.decodeBehavior();
    const plan = await new OpenAIPlanner(process.env.OPENAI_API_KEY, process.env.OPENAI_MODEL).plan({organism,event:organism.nextEvent,behavior,allowedActions:ALLOWED_ACTIONS[behavior.behavior]});
    validatePlan(plan,behavior.behavior);
    console.log(JSON.stringify({ok:true,model:process.env.OPENAI_MODEL,brain:brain.id,neuralBehavior:behavior.behavior,plannedBehavior:plan.behavior,action:plan.action,toolsExecuted:false,lifeStateChanged:false},null,2));
  } catch(e) {console.error(e instanceof Error ? e.message : 'Language check failed');process.exitCode=1;}
}

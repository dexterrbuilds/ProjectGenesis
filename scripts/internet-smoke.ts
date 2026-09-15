import { createOrganism, executeTool } from '../core/life.ts';
const outcome = await executeTool({ behavior:'EXPLORE',action:'research',reasoning:'Verify selected internet access',content:'Read the OpenWorm source',planner:'smoke' },createOrganism(),'internet-smoke',new Date().toISOString(),{internet:true});
if (!outcome.ok || !outcome.sourceUrl || outcome.detail.length < 100) throw new Error('Live reading failed');
console.log(JSON.stringify({ok:outcome.ok,source:outcome.sourceUrl,characters:outcome.detail.length,simulated:outcome.simulated}));

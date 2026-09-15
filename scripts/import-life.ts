import { readFile } from 'node:fs/promises';
import pg from 'pg';
import { migrate } from '../runtime/migrate.ts';
import { LifeStore } from '../server/store.ts';
import { CElegansBrain } from '../core/brain/celegans.ts';
import { ensureIdentity } from '../core/identity.ts';
import type { Decision, Organism, Milestone } from '../core/contracts.ts';
if (!process.env.DATABASE_URL || !process.argv[2]) throw new Error('Usage: node --env-file=.env scripts/import-life.ts <export.json>');
const data = JSON.parse(await readFile(process.argv[2], 'utf8')) as { organism: Organism; decisions: Decision[] };
if (!data.organism?.id || data.organism.cycles !== data.decisions.length || !Number.isFinite(Date.parse(data.organism.bornAt))) throw new Error('Invalid life export');
const o = ensureIdentity(data.organism);
if (o.brain) new CElegansBrain().initialize(o.brain);
for (let i=0;i<data.decisions.length;i++) if(data.decisions[i].cycle!==i+1) throw new Error('Non-contiguous life history');
const milestone = (kind: Milestone['kind'], d: Decision | undefined, title: string, detail: string) => { if(d && !o.milestones!.some(m=>m.kind===kind)) o.milestones!.push({id:`${o.id}:${kind}`,kind,at:d.at,decisionId:d.id,title,detail}); };
milestone('first_experience',data.decisions[0],'The first experience.','Recovered from the original saved decision.');
milestone('first_project',data.decisions.find(d=>d.plan?.action==='draft_service'&&d.outcome.ok),'An idea became a project.','Original service draft, preserved across the storage migration.');
milestone('first_income',data.decisions.find(d=>o.wallet.entries.some(e=>e.kind==='business_income'&&e.cents>0&&e.id.startsWith(d.id+':'))),'The first simulated income.','Original development-market income, not a real customer payment.');
const pool = new pg.Pool({connectionString:process.env.DATABASE_URL});
try { await migrate(pool); await new LifeStore(pool).importLife(o,data.decisions); console.log(JSON.stringify({imported:true,id:o.id,bornAt:o.bornAt,cycles:o.cycles})); } finally { await pool.end(); }

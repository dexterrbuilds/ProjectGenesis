/** Sanitized fixture only, no planner, grant creation, event persistence, or neural advancement. */
import type pg from 'pg';
import {readMemoryArchive} from './memory-store.ts';
import {loadDisclosure} from './disclosure-store.ts';
import {compileContext} from '../core/v2/context.ts';
import {SavedObservationAdapter} from '../core/v2/biology.ts';
import {CLOSED_PERMISSIONS} from '../core/v2/identity.ts';
export async function inspectFixtureFirstContext(pool:pg.Pool){
 const c=await pool.connect();try{await c.query('BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY');
 const target=(await c.query('SELECT current_database() db,current_schema() schema')).rows[0];
 const o=(await c.query('SELECT state FROM genesis_organisms')).rows[0].state;
 if(target.db!=='genesis_runtime_v1_test'||!target.schema.startsWith('awakening_test_')||!o.id.startsWith('fixture-'))throw Error('FIXTURE_ONLY');
 const l=(await c.query('SELECT record,revision FROM genesis_life_state')).rows[0];const archive=await readMemoryArchive(c,o.id,Number(l.revision));const disclosure=await loadDisclosure(c,o,l.record,archive);
 const at=new Date().toISOString();const bio=new SavedObservationAdapter(o.id,()=>at).accept({id:'fixture-context-inspection',kind:'digital-event',source:'sanitized-hypothetical-first-context; not activation',observedAt:at});
 const context=compileContext(o,l.record,bio,{...CLOSED_PERMISSIONS,execution:true,localArtifacts:true,llm:true,maxAttempts:1,maxCostMicros:50000},12000,undefined,archive,[],disclosure);
 const structural=JSON.parse(context.text);await c.query('COMMIT');
 return {fixtureOnly:true,plannerInvoked:false,eventPersisted:false,decisionCreated:false,contextHash:context.hash,identityFields:Object.keys(structural.critical.identity),priorDecisionCount:structural.critical.identity.cycles,constitutionPresent:!!structural.critical.rules.constitution,projectMetadataCount:structural.reviewedLegacyProjects.length,selectedPastExperiences:structural.relevantPastExperiences.length,economyNamespace:'SIMULATED',walletStatus:l.record.walletIdentity.status,biologicalStatus:bio.status,localOperationContract:structural.localOperationContract,manifest:context.manifest.disclosure};
 }catch(e){await c.query('ROLLBACK');throw e;}finally{c.release();}
}

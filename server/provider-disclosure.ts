/** Revalidate disclosure immediately before reservation/dispatch; no transport or retry. */
import type pg from 'pg';
import type {WorkingContext} from '../core/v2/contracts.ts';
import {digest} from '../core/v2/identity.ts';
import {disclosureBinding} from '../core/v2/disclosure.ts';
import {readMemoryArchive} from './memory-store.ts';
import {loadDisclosure} from './disclosure-store.ts';
export async function checkProviderDisclosure(pool:pg.Pool,context:WorkingContext){
 const c=await pool.connect();try{
  await c.query('BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY');
  const present=(await c.query("SELECT to_regclass('genesis_control_state') IS NOT NULL present")).rows[0].present;
  if(!present){if(context.manifest.disclosure?.binding.installed)throw Error('DISCLOSURE_REMOVED');await c.query('COMMIT');return;}
  const base=(await c.query("SELECT state FROM genesis_organisms WHERE id='genesis'")).rows[0];
  const life=(await c.query("SELECT record,revision FROM genesis_life_state WHERE organism_id='genesis'")).rows[0];
  if(!base||base.state.id!==context.organismId||Number(life?.revision)!==context.manifest.stateRevision)throw Error('DISCLOSURE_CONTEXT_STALE');
  const archive=await readMemoryArchive(c,context.organismId,Number(life.revision));
  const current=await loadDisclosure(c,base.state,life.record,archive);
  if(context.manifest.disclosure?.audience!=='PROVIDER'||digest(context.manifest.disclosure.binding)!==digest(disclosureBinding(current))||JSON.parse(context.text).disclosureAuthority!==digest(disclosureBinding(current)))throw Error('DISCLOSURE_CONTEXT_STALE');
  await c.query('COMMIT');
 }catch(e){await c.query('ROLLBACK');throw e;}finally{c.release();}
}

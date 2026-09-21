import {InterruptedCycle} from '../core/v2/cycle.ts';
export class ContinuousFenceError extends InterruptedCycle {
 readonly recoverableLocal:boolean;
 constructor(category:string,recoverableLocal=false){super(category);this.recoverableLocal=recoverableLocal;}
}
import type pg from 'pg';
import {digest} from '../core/v2/identity.ts';
import {LOCAL_PERMISSION,eventSchema,eventObservation,type ContinuousContext} from '../core/v2/continuous.ts';
import {validateScope,type ContinuousScope} from './continuous-spec.ts';
import type {CycleFence} from './commit-v2.ts';
import type {BaseRow,ExtensionRow} from './one-shot-authority.ts';
export async function continuousState(c:pg.PoolClient,id:string,base:BaseRow,ext:ExtensionRow){
 const row=(await c.query('SELECT * FROM genesis_continuous_scopes WHERE id=$1 FOR UPDATE',[id])).rows[0];
 if(!row)throw Error('Continuous scope absent');const s=validateScope(row.payload);
 if(row.status!=='AUTHORIZED'||row.payload_hash!==digest(s)||row.authorization_record?.payloadHash!==digest(s)||row.authorization_record?.issuer!==s.issuer||row.authorization_record?.reference!==s.authorizationReference||Date.parse(s.issuedAt)>Date.now()||Date.parse(s.expiresAt)<=Date.now()||base.state.id!==s.organismId||ext.record.organismId!==s.organismId||ext.record.constitutionHash!==s.constitutionHash||ext.record.executionLock!=='CLOSED'||ext.record.biologicalContext.mode!=='SAVED-OBSERVATION-ONLY')throw new ContinuousFenceError('SCOPE_INVALID');
 const schedule=(await c.query("SELECT enabled FROM genesis_schedule WHERE id='genesis' FOR UPDATE")).rows[0];const count=(await c.query('SELECT count(*) n,coalesce(max(cycle),0) m FROM genesis_decisions')).rows[0];
 if(schedule?.enabled!==false||Number(count.n)!==base.state.cycles||Number(count.m)!==base.state.cycles||base.state.cycles<s.minimumPriorDecisions)throw Error('Continuous numbering/schedule mismatch');return s;
}
export async function assertContinuousClaim(c:pg.PoolClient,f:CycleFence,base:BaseRow,ext:ExtensionRow):Promise<{scope:ContinuousScope;authority:ContinuousContext}>{
 if(f.oneShotGrantId||!f.continuousScopeId||!f.eventId)throw Error('Distinct continuous fence required');
 const s=await continuousState(c,f.continuousScopeId,base,ext);
 const a=(await c.query('SELECT * FROM genesis_continuous_attempts WHERE cycle_id=$1 FOR UPDATE',[f.cycleId])).rows[0];const e=(await c.query('SELECT *,lease_until>clock_timestamp() AS lease_current FROM genesis_runtime_events WHERE id=$1 FOR UPDATE',[f.eventId])).rows[0];
 if(!a||a.status!=='CLAIMED'||a.lease!==f.lease||a.scope_id!==s.id||a.event_id!==f.eventId||!e||e.status!=='CLAIMED'||e.cycle_id!==f.cycleId||e.lease!==f.lease||Number(a.base_revision)!==f.baseRevision||Number(a.life_revision)!==f.lifeRevision)throw new ContinuousFenceError('OWNERSHIP_MISMATCH');
 if(!e.lease_current)throw new ContinuousFenceError('LEASE_EXPIRED_BEFORE_ADMISSION');
 const event=eventSchema.parse(e.payload);if(e.payload_hash!==digest(event)||event.organismId!==s.organismId||!s.allowedEvents.includes(event.payload.kind)||event.expiresAt&&Date.parse(event.expiresAt)<=Date.now())throw Error('Continuous event binding');
 const authority:ContinuousContext={kind:'CONTINUOUS_LOCAL_V1',scopeId:s.id,scopeHash:digest(s),permissionHash:digest(LOCAL_PERMISSION),event,limits:{maxDepth:s.maxDepth,maxFollowups:s.maxFollowups,minimumDelayMs:s.minimumDelayMs,allowedEvents:s.allowedEvents,allowedEffects:s.allowedEffects,scheduling:s.scheduling},resources:a.resources};
 return {scope:s,authority};
}
export function continuousInput(authority:ContinuousContext,at:string){return eventObservation(authority.event,at);}

import type pg from 'pg';
import type {Organism} from '../core/contracts.ts';
import type {LifeStateV1} from '../core/v2/contracts.ts';
import {digest} from '../core/v2/identity.ts';
import {validateGrant,type OneShotGrant} from './one-shot-spec.ts';
import type {CycleFence} from './commit-v2.ts';
export type GrantRow={id:string;payload:OneShotGrant;payload_hash:string;status:string;authorization_record:{payloadHash:string;issuer:string;reference:string}|null;cycle_id:string|null;lease:string|null};
export type BaseRow={state:Organism;revision:number;lease:string;valid:boolean};
export type ExtensionRow={record:LifeStateV1;revision:number};
export async function assertGrantState(c:pg.PoolClient,row:GrantRow,base:BaseRow,ext:ExtensionRow){
 const g=validateGrant(row.payload);
 if(row.payload_hash!==digest(g)||row.authorization_record?.payloadHash!==row.payload_hash||row.authorization_record.issuer!==g.issuer||row.authorization_record.reference!==g.authorizationReference)throw Error('Grant authorization binding rejected');
 const schedule=(await c.query("SELECT enabled FROM genesis_schedule WHERE id='genesis' FOR UPDATE")).rows[0];
 const count=Number((await c.query('SELECT count(*) AS n FROM genesis_decisions')).rows[0].n);
 if(!schedule||schedule.enabled||ext.record.executionLock!=='CLOSED'||base.state.id!==g.organismId||ext.record.organismId!==g.organismId||base.state.cycles!==7||count!==7||Number(base.revision)!==g.stateRevision||Number(ext.revision)!==g.lifeRevision||ext.record.constitutionHash!==g.constitution.hash||Date.parse(g.expiresAt)<=Date.now())throw Error('Grant state/expiry/schedule rejected');
 return g;
}
export async function assertOneShotClaim(c:pg.PoolClient,f:CycleFence,base:BaseRow,ext:ExtensionRow){
 const row=(await c.query('SELECT * FROM genesis_execution_grants WHERE id=$1 FOR UPDATE',[f.oneShotGrantId])).rows[0] as GrantRow|undefined;
 if(!row||row.status!=='CLAIMED'||row.cycle_id!==f.cycleId||row.lease!==f.lease)throw Error('Single-use claim rejected');
 return assertGrantState(c,row,base,ext);
}

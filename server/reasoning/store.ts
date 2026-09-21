import type pg from 'pg';
import {readFileSync} from 'node:fs';
import {digest} from '../../core/v2/identity.ts';
import {identities} from '../one-shot-spec.ts';
import {validateAdmission} from './factory.ts';
import {ReasoningError,type Admission} from './contracts.ts';
export async function fixtureTarget(pool:Pick<pg.Pool,'query'>){const t=(await pool.query('SELECT current_database() db,current_schema() schema')).rows[0];return t.db==='genesis_runtime_v1_test'&&t.schema.startsWith('awakening_test_');}
export async function installProviderFixture(pool:pg.Pool){if(!await fixtureTarget(pool))throw Error('FIXTURE_ONLY');await pool.query(readFileSync(new URL('../../runtime/provider-integration-schema.sql',import.meta.url),'utf8'));}
export function compatibleAdmission(raw:unknown){const a=validateAdmission(raw),i=identities();if(a.runtimeHash!==i.runtime.sha256||a.constitutionHash!==i.constitution.hash||a.policyHash!==i.policy.hash)throw new ReasoningError('ADMISSION_MISMATCH');return a;}
export async function loadAdmission(pool:Pick<pg.Pool,'query'>,id:string,organismId:string):Promise<Admission>{
 const r=(await pool.query("SELECT * FROM genesis_provider_admissions WHERE id=$1 AND organism_id='genesis'",[id])).rows[0];const o=(await pool.query("SELECT state->>'id' id FROM genesis_organisms WHERE id='genesis'")).rows[0];
 if(!r||r.status!=='ADMITTED'||r.payload_hash!==digest(r.payload)||o?.id!==organismId)throw new ReasoningError('ADMISSION_MISMATCH');const a=compatibleAdmission(r.payload);if(Date.parse(a.effectiveAt)>Date.now()||Date.parse(a.expiresAt)<=Date.now()||a.provider==='fixture'&&!await fixtureTarget(pool))throw new ReasoningError('ADMISSION_MISMATCH');return a;
}

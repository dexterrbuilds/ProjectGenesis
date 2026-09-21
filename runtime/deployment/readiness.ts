import type pg from 'pg';
import {runtimeIdentity} from '../../server/one-shot-spec.ts';
import {requireCatalog,requireRole,hashObject,sqlHashes} from './schema.ts';
export async function inspectReadiness(pool:pg.Pool,expected:{organismId:string;bornAt:string},role?:'reader'){
 const c=await pool.connect();try{
 await c.query('BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY');if(role)await requireRole(c,role);await requireCatalog(c,'installed');
 const release=(await c.query('SELECT runtime_hash,sql_hashes FROM genesis_deployment_release')).rows;
 if(release.length!==1||release[0].runtime_hash!==runtimeIdentity().sha256||hashObject(release[0].sql_hashes)!==hashObject(sqlHashes()))throw Error('DEPLOYMENT_IDENTITY_MISMATCH');
 const os=(await c.query('SELECT state FROM genesis_organisms')).rows,ls=(await c.query('SELECT record FROM genesis_life_state')).rows,sc=(await c.query('SELECT enabled FROM genesis_schedule')).rows;
 if(os.length!==1||os[0].state.id!==expected.organismId||os[0].state.bornAt!==expected.bornAt||ls.length!==1||ls[0].record.executionLock!=='CLOSED'||sc.length!==1||sc[0].enabled)throw Error('RUNTIME_STATE_MISMATCH');
 await c.query('COMMIT');return {ready:true,mode:'dormant',biology:'SAVED-OBSERVATION-ONLY'} as const;
 }catch{await c.query('ROLLBACK');return {ready:false,mode:'dormant'} as const;}finally{c.release();}
}

/** Explicit, reviewed additive installer. Never imported by observation boot. */
import type pg from 'pg';
import {z} from 'zod';
import {runtimeIdentity} from '../../server/one-shot-spec.ts';
import {source,sqlHashes,rows,hashObject,requireCatalog} from './schema.ts';
import {databaseTarget} from './config.ts';
const identifier=z.string().regex(/^[a-z][a-z0-9_]{0,62}$/);
export const rolesSchema=z.object({observer:identifier,reader:identifier,worker:identifier,operator:identifier}).strict();
const planSchema=z.object({version:z.literal(1),target:z.object({host:z.string(),port:z.string(),database:z.string(),schema:identifier}).strict(),organismId:z.string().min(1),bornAt:z.string().datetime(),decisions:z.literal(7),rowHash:z.string().regex(/^[a-f0-9]{64}$/),runtimeHash:z.string(),sqlHashes:z.record(z.string()),roles:rolesSchema,hash:z.string()}).strict();
export type InstallPlan=z.infer<typeof planSchema>;
export async function baseline(c:pg.PoolClient,id:string,birth:string){
 await requireCatalog(c,'baseline');
 const os=(await c.query('SELECT state,lease FROM genesis_organisms')).rows;
 const life=(await c.query('SELECT record FROM genesis_life_state')).rows;
 const schedules=(await c.query('SELECT enabled FROM genesis_schedule')).rows;
 if(os.length!==1||os[0].state.id!==id||os[0].state.bornAt!==birth||os[0].state.cycles!==7||os[0].lease||life.length!==1||life[0].record.executionLock!=='CLOSED'||schedules.length!==1||schedules[0].enabled||(await c.query('SELECT count(*) n FROM genesis_decisions')).rows[0].n!=='7')throw Error('INSTALL_BASELINE_MISMATCH');
 if((await c.query("SELECT count(*) n FROM genesis_life_events WHERE record->>'kind' IS DISTINCT FROM 'administrative'")).rows[0].n!=='0')throw Error('INSTALL_BASELINE_MISMATCH');
 if((await c.query('SELECT version FROM genesis_migrations ORDER BY version')).rows.map(r=>r.version).join(',')!=='001,002,003')throw Error('MIGRATION_VERSION_MISMATCH');
}
export async function planInstall(pool:pg.Pool,url:string,id:string,birth:string,roles:unknown){
 const c=await pool.connect();try{await c.query('BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY');await baseline(c,id,birth);
 const schema=(await c.query('SELECT current_schema() s')).rows[0].s;
 const plan={version:1 as const,target:databaseTarget(url,schema),organismId:id,bornAt:birth,decisions:7 as const,rowHash:hashObject(await rows(c)),runtimeHash:runtimeIdentity().sha256,sqlHashes:sqlHashes(),roles:rolesSchema.parse(roles)};
 if(new Set(Object.values(plan.roles)).size!==4)throw Error('DISTINCT_ROLES_REQUIRED');await c.query('COMMIT');return {...plan,hash:hashObject(plan)};
 }catch(e){await c.query('ROLLBACK');throw e;}finally{c.release();}
}
export function grantSQL(path:string,schema:string,roles:z.infer<typeof rolesSchema>){
 const vars={schema:identifier.parse(schema),...rolesSchema.parse(roles)};
 return source(path).replace(/:"(schema|observer|worker|operator|reader)"/g,(_,k:keyof typeof vars)=>'"'+vars[k]+'"');
}
export async function applyInstall(pool:pg.Pool,url:string,input:unknown,ack:string){
 const p=planSchema.parse(input),{hash,...unsigned}=p;
 if(hash!==hashObject(unsigned)||ack!=='INSTALL_REVIEWED_PLAN:'+hash||p.runtimeHash!==runtimeIdentity().sha256||hashObject(p.sqlHashes)!==hashObject(sqlHashes()))throw Error('INSTALL_PLAN_IDENTITY_MISMATCH');
 const c=await pool.connect();try{
 await c.query('BEGIN');await c.query("SET LOCAL lock_timeout='5s'");await c.query("SELECT pg_advisory_xact_lock(hashtext('project-genesis-schema'))");
 const schema=(await c.query('SELECT current_schema() s')).rows[0].s;
 if(hashObject(databaseTarget(url,schema))!==hashObject(p.target))throw Error('INSTALL_TARGET_MISMATCH');
 const before=await rows(c);for(const n of Object.keys(before))await c.query(`LOCK TABLE "${n}" IN SHARE ROW EXCLUSIVE MODE`);
 await baseline(c,p.organismId,p.bornAt);if(hashObject(await rows(c))!==p.rowHash)throw Error('INSTALL_ROWS_CHANGED');
 const owner=(await c.query("SELECT nspowner::regrole::text AS owner FROM pg_namespace WHERE nspname=current_schema()")).rows[0].owner;
 for(const role of Object.values(p.roles)){
 const r=(await c.query('SELECT rolname,rolsuper,rolcreaterole,rolcreatedb,rolbypassrls,rolcanlogin FROM pg_roles WHERE rolname=$1',[role])).rows[0];
 if(!r||r.rolsuper||r.rolcreaterole||r.rolcreatedb||r.rolbypassrls||r.rolcanlogin||role===owner)throw Error('ROLE_PROFILE_INVALID');
 if((await c.query('SELECT 1 FROM pg_auth_members WHERE member=(SELECT oid FROM pg_roles WHERE rolname=$1)',[role])).rowCount)throw Error('ROLE_INHERITANCE_INVALID');
 if((await c.query('SELECT has_schema_privilege($1,current_schema(),\'CREATE\') allowed',[role])).rows[0].allowed)throw Error('ROLE_SCHEMA_PRIVILEGE_INVALID');
 }
 for(const path of ['runtime/preparation-schema.sql','runtime/one-shot-schema.sql','runtime/continuous-schema.sql','runtime/operator-schema-v1.sql','runtime/provider-integration-schema.sql','runtime/deployment/release.sql'])await c.query(source(path));
 for(const path of ['runtime/operator-role-grants.sql','runtime/provider-role-grants.sql','runtime/deployment/roles.sql'])await c.query(grantSQL(path,schema,p.roles));
 await c.query("INSERT INTO genesis_deployment_release(id,runtime_hash,sql_hashes) VALUES('deployment-v1',$1,$2)",[p.runtimeHash,p.sqlHashes]);
 await requireCatalog(c,'installed');if(hashObject(await rows(c,Object.keys(before)))!==p.rowHash)throw Error('PRESERVATION_FAILED');
 await c.query('COMMIT');return {installed:true,planHash:hash,runtimeHash:p.runtimeHash};
 }catch(e){await c.query('ROLLBACK');throw e;}finally{c.release();}
}

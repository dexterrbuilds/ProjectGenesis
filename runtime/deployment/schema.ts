import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import type pg from 'pg';
export const sqlPaths=['runtime/migrations/001_genesis.sql','runtime/migrations/002_observations.sql','runtime/migrations/003_runtime_v1.sql','runtime/preparation-schema.sql','runtime/one-shot-schema.sql','runtime/continuous-schema.sql','runtime/operator-schema-v1.sql','runtime/provider-integration-schema.sql','runtime/deployment/release.sql','runtime/operator-role-grants.sql','runtime/provider-role-grants.sql','runtime/deployment/roles.sql'] as const;
export const sha=(x:string|Buffer)=>createHash('sha256').update(x).digest('hex');
function ordered(x:unknown):unknown{if(Array.isArray(x))return x.map(ordered);if(x&&typeof x==='object')return Object.fromEntries(Object.entries(x).sort(([a],[b])=>a.localeCompare(b,'en')).map(([k,v])=>[k,ordered(v)]));return x;}
export const hashObject=(x:unknown)=>sha(JSON.stringify(ordered(x)));
export const source=(path:string)=>readFileSync(new URL('../../'+path,import.meta.url),'utf8');
export const sqlHashes=()=>Object.fromEntries(sqlPaths.map(p=>[p,sha(source(p))]));
export async function catalog(c:pg.PoolClient){
 const schema=(await c.query('SELECT current_schema() s')).rows[0].s as string;
 const q=async(sql:string)=>(await c.query(sql,[schema])).rows;
 const result={
 relations:await q(`SELECT t.relname,t.relkind,t.relpersistence,t.relrowsecurity,t.relforcerowsecurity,t.reloptions FROM pg_class t JOIN pg_namespace n ON n.oid=t.relnamespace WHERE n.nspname=$1 AND t.relkind IN ('r','p','v','m','S') ORDER BY t.relname`),
 policies:await q(`SELECT tablename,policyname,permissive,roles,cmd,qual,with_check FROM pg_policies WHERE schemaname=$1 ORDER BY tablename,policyname`),
 columns:await q(`SELECT table_name,column_name,ordinal_position,data_type,udt_name,is_nullable,column_default FROM information_schema.columns WHERE table_schema=$1 ORDER BY table_name,ordinal_position`),
 constraints:await q(`SELECT t.relname AS table_name,k.conname,k.contype,pg_get_constraintdef(k.oid,true) AS definition FROM pg_constraint k JOIN pg_class t ON t.oid=k.conrelid JOIN pg_namespace n ON n.oid=t.relnamespace WHERE n.nspname=$1 ORDER BY t.relname,k.conname`),
 indexes:await q(`SELECT tablename,indexname,indexdef FROM pg_indexes WHERE schemaname=$1 ORDER BY tablename,indexname`),
 functions:await q(`SELECT p.proname,pg_get_function_identity_arguments(p.oid) args,pg_get_functiondef(p.oid) definition FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname=$1 ORDER BY p.proname,args`),
 triggers:await q(`SELECT t.relname AS table_name,g.tgname,g.tgenabled,pg_get_triggerdef(g.oid,true) definition FROM pg_trigger g JOIN pg_class t ON t.oid=g.tgrelid JOIN pg_namespace n ON n.oid=t.relnamespace WHERE n.nspname=$1 AND NOT g.tgisinternal ORDER BY t.relname,g.tgname`),
 views:await q(`SELECT viewname,definition FROM pg_views WHERE schemaname=$1 ORDER BY viewname`),
 sequences:await q(`SELECT sequencename,data_type,start_value,min_value,max_value,increment_by,cycle FROM pg_sequences WHERE schemaname=$1 ORDER BY sequencename`)
 };
 // Generated identifiers vary by fixture schema; SQL text/function bodies are otherwise exact.
 return JSON.parse(JSON.stringify(result).replaceAll('"'+schema+'".','__SCHEMA__.').replaceAll(schema+'.','__SCHEMA__.').replaceAll("'"+schema+"'","'__SCHEMA__'"));
}
export async function rows(c:pg.PoolClient,tables?:string[]){
 const names=tables??(await c.query("SELECT tablename FROM pg_tables WHERE schemaname=current_schema() ORDER BY tablename")).rows.map(r=>r.tablename as string);
 const out:Record<string,unknown[]>={};for(const n of names){if(!/^genesis_[a-z0-9_]+$/.test(n))throw Error('UNKNOWN_TABLE');out[n]=(await c.query(`SELECT row_to_json(t) r FROM "${n}" t ORDER BY row_to_json(t)::text`)).rows.map(r=>r.r);}return out;
}
export function expectedCatalog(kind:'baseline'|'installed'){return JSON.parse(source('runtime/deployment/catalog-'+kind+'.json'));}
export async function requireCatalog(c:pg.PoolClient,kind:'baseline'|'installed'){if(hashObject(await catalog(c))!==hashObject(expectedCatalog(kind)))throw Error('SCHEMA_MISMATCH');}
/** Reject owner/superuser or excessive credentials supplied to ordinary processes. */
export async function requireRole(c:pg.PoolClient,kind:'reader'|'worker'|'operator'){
 const r=(await c.query(`SELECT r.rolsuper,r.rolcreatedb,r.rolcreaterole,r.rolbypassrls,
 has_schema_privilege(current_user,current_schema(),'CREATE') AS creates,
 EXISTS(SELECT 1 FROM pg_class t JOIN pg_namespace n ON n.oid=t.relnamespace WHERE n.nspname=current_schema() AND pg_has_role(current_user,t.relowner,'MEMBER')) AS owns
 FROM pg_roles r WHERE rolname=current_user`)).rows[0];
 if(!r||r.rolsuper||r.rolcreatedb||r.rolcreaterole||r.rolbypassrls||r.creates||r.owns)throw Error('NORMAL_SERVICE_ROLE_REQUIRED');
 if(kind==='reader'){
 if((await c.query("SELECT 1 FROM pg_tables WHERE schemaname=current_schema() AND (has_table_privilege(current_user,quote_ident(schemaname)||'.'||quote_ident(tablename),'INSERT,UPDATE,DELETE,TRUNCATE,REFERENCES,TRIGGER') OR has_any_column_privilege(current_user,quote_ident(schemaname)||'.'||quote_ident(tablename),'INSERT,UPDATE,REFERENCES'))")).rowCount)throw Error('READ_ONLY_ROLE_REQUIRED');
 }else{
 const privileges=kind==='worker'?['genesis_operator_audit:INSERT','genesis_execution_grants:INSERT','genesis_disclosure_reviews:INSERT','genesis_operator_actors:UPDATE']:['genesis_operator_actors:UPDATE','genesis_decisions:UPDATE'];
 for(const spec of privileges){const [table,permission]=spec.split(':');if((await c.query('SELECT has_table_privilege(current_user,$1,$2) OR has_any_column_privilege(current_user,$1,$2) AS allowed',[table,permission])).rows[0].allowed)throw Error('ROLE_BOUNDARY_MISMATCH');}
 }
}

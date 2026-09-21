import pg from 'pg';
import {writeFileSync} from 'node:fs';
const pool=new pg.Pool({connectionString:process.env.DATABASE_URL});const c=await pool.connect();
try{
 await c.query('BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY');
 const queries={
 tables:"SELECT table_name,column_name,data_type,is_nullable,column_default FROM information_schema.columns WHERE table_schema='public' AND table_name LIKE 'genesis_%' ORDER BY table_name,ordinal_position",
 indexes:"SELECT tablename,indexname,indexdef FROM pg_indexes WHERE schemaname='public' AND tablename LIKE 'genesis_%' ORDER BY tablename,indexname",
 constraints:"SELECT t.relname AS table_name,c.conname,pg_get_constraintdef(c.oid) AS definition FROM pg_constraint c JOIN pg_class t ON t.oid=c.conrelid JOIN pg_namespace n ON n.oid=t.relnamespace WHERE n.nspname='public' AND t.relname LIKE 'genesis_%' ORDER BY t.relname,c.conname",
 triggers:"SELECT event_object_table,trigger_name,event_manipulation,action_statement FROM information_schema.triggers WHERE event_object_schema='public' AND event_object_table LIKE 'genesis_%' ORDER BY event_object_table,trigger_name,event_manipulation",
 functions:"SELECT p.proname,pg_get_functiondef(p.oid) AS definition FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='public' AND p.proname LIKE 'genesis_%' ORDER BY p.proname",
 role:"SELECT rolsuper,rolcreatedb,rolcreaterole,rolcanlogin,rolbypassrls FROM pg_roles WHERE rolname=current_user",
 rowSecurity:"SELECT relname,relrowsecurity,relforcerowsecurity FROM pg_class WHERE relnamespace='public'::regnamespace AND relname LIKE 'genesis_%' AND relkind='r' ORDER BY relname",
 migrations:"SELECT * FROM genesis_migrations ORDER BY version"
 };
 const out={};for(const [k,q]of Object.entries(queries))out[k]=(await c.query(q)).rows;
 await c.query('COMMIT');writeFileSync('verification/completion-audit/canonical-schema.json',JSON.stringify(out,null,2)+'\n');console.log(JSON.stringify({tables:[...new Set(out.tables.map(x=>x.table_name))],role:out.role,migrations:out.migrations,indexCount:out.indexes.length}));
}finally{c.release();await pool.end();}

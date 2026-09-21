/** Actual pg_dump/psql round trip into an empty disposable schema. No production URL accepted. */
import {existsSync} from 'node:fs';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {mkdtemp,writeFile,readFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import pg from 'pg';
import {catalog,hashObject,rows} from '../../runtime/deployment/schema.ts';
const exec=promisify(execFile);
export async function restoreFixture(pool:pg.Pool,url:string,schema:string){
 const u=new URL(url);if(u.pathname!=='/genesis_runtime_v1_test'||!schema.startsWith('awakening_test_')||process.env.DATABASE_URL)throw Error('FIXTURE_ONLY');
 const target='restore_'+crypto.randomUUID().replaceAll('-','');
 const dir=await mkdtemp(join(tmpdir(),'genesis-restore-')),dump=join(dir,'private.sql');
 const env:NodeJS.ProcessEnv={NODE_ENV:'test',PATH:process.env.PATH,PGHOST:u.hostname,PGPORT:u.port,PGUSER:decodeURIComponent(u.username),PGPASSWORD:decodeURIComponent(u.password),PGDATABASE:u.pathname.slice(1)};
 const bin=existsSync('/opt/homebrew/opt/postgresql@16/bin/pg_dump')?'/opt/homebrew/opt/postgresql@16/bin/':'';const c=await pool.connect();let before:Awaited<ReturnType<typeof rows>>,shape:unknown;let sequenceState:unknown;
 const sequences=async(db:pg.PoolClient)=>{const out:Record<string,unknown>={};for(const r of (await db.query("SELECT sequencename FROM pg_sequences WHERE schemaname=current_schema() ORDER BY sequencename")).rows)out[r.sequencename]=(await db.query(`SELECT last_value,is_called FROM "${r.sequencename}"`)).rows[0];return out;};
 try{before=await rows(c);shape=await catalog(c);sequenceState=await sequences(c);}finally{c.release();}
 let restored:pg.Pool|undefined;
 try{
 await exec(bin+'pg_dump',['--schema='+schema,'--no-owner','--no-privileges','--file='+dump],{env});
 const text=(await readFile(dump,'utf8')).replaceAll(schema+'.',target+'.').replaceAll('SCHEMA '+schema,'SCHEMA '+target).replaceAll('SCHEMA: '+schema,'SCHEMA: '+target).replaceAll("'"+schema+"'","'"+target+"'");
 await writeFile(dump,text,{mode:0o600});await exec(bin+'psql',['-X','-v','ON_ERROR_STOP=1','--single-transaction','--file='+dump],{env});
 restored=new pg.Pool({connectionString:url,options:'-c search_path='+target});const r=await restored.connect();try{const after=await rows(r);if(hashObject(before)!==hashObject(after)||hashObject(shape)!==hashObject(await catalog(r))||hashObject(sequenceState)!==hashObject(await sequences(r)))throw Error('RESTORE_MISMATCH');return {tables:Object.keys(after).length,decisions:after.genesis_decisions.length,attempts:after.genesis_provider_attempts.length,receipts:after.genesis_provider_receipts.length,rowHash:hashObject(after),schemaHash:hashObject(shape)};}finally{r.release();}
 }finally{if(restored)await restored.end();await pool.query(`DROP SCHEMA IF EXISTS ${target} CASCADE`);await rm(dir,{recursive:true,force:true});}
}

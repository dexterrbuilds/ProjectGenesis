/** Read-only canonical export/audit. No runtime or model imports. Private output mode 0600. */
import pg from 'pg';
import {writeFileSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
const out=process.argv[2];if(!out||existsSync(out))throw new Error('Unique private audit path required');
const pool=new pg.Pool({connectionString:process.env.DATABASE_URL});const c=await pool.connect();
try{
 await c.query('BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY');
 const names=(await c.query("SELECT tablename FROM pg_tables WHERE schemaname='public' AND tablename LIKE 'genesis_%' ORDER BY tablename")).rows.map(r=>r.tablename as string);
 const rows:Record<string,unknown[]>={};for(const n of names){if(!/^genesis_[a-z_]+$/.test(n))throw new Error('Invalid table');rows[n]=(await c.query(`SELECT row_to_json(t) AS row FROM "${n}" t ORDER BY row_to_json(t)::text`)).rows.map(r=>r.row);}
 const sessions=(await c.query("SELECT pid,application_name,state,backend_type FROM pg_stat_activity WHERE datname=current_database() AND pid<>pg_backend_pid() AND backend_type='client backend'")).rows;
 await c.query('COMMIT');
 const sha256=createHash('sha256').update(JSON.stringify(rows)).digest('hex');
 writeFileSync(out,JSON.stringify({sha256,rows,sessions},null,2)+'\n',{mode:0o600});
 console.log(JSON.stringify({sha256,tables:Object.fromEntries(Object.entries(rows).map(([k,v])=>[k,v.length])),otherClientSessions:sessions.length}));
}finally{c.release();await pool.end();}

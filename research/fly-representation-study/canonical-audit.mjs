// Read-only audit. Does not import Genesis runtime, migrations or scheduler.
import pg from 'pg';
import {createHash} from 'node:crypto';
import {writeFileSync,existsSync} from 'node:fs';
const dest=process.argv[2];
if(!dest || existsSync(dest)) throw new Error('Unique output path required');
const pool=new pg.Pool({connectionString:process.env.DATABASE_URL});
const c=await pool.connect();
try {
 await c.query('BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY');
 const tables=(await c.query("SELECT tablename FROM pg_tables WHERE schemaname='public' AND tablename LIKE 'genesis_%' ORDER BY tablename")).rows.map(r=>r.tablename);
 const data={};
 for(const table of tables){
  if(!/^genesis_[a-z_]+$/.test(table))throw new Error('Invalid table');
  data[table]=(await c.query(`SELECT row_to_json(t) AS row FROM "${table}" t ORDER BY row_to_json(t)::text`)).rows.map(r=>r.row);
 }
 await c.query('COMMIT');
 const counts=Object.fromEntries(tables.map(t=>[t,data[t].length]));
 if(counts.genesis_decisions!==7 || data.genesis_schedule.some(s=>s.enabled)) throw new Error('Preservation invariant violated');
 const result={sha256:createHash('sha256').update(JSON.stringify(data)).digest('hex'),tableRowCounts:counts,schedule:data.genesis_schedule,mode:'repeatable-read read-only; canonical cycles run: 0'};
 writeFileSync(dest,JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({sha256:result.sha256,cycles:counts.genesis_decisions,enabled:result.schedule[0].enabled}));
} finally {c.release();await pool.end();}

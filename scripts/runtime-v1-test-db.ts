/** Provision only a dedicated local test database; never modifies canonical tables. */
import pg from 'pg';
import {writeFileSync,readFileSync} from 'node:fs';
const canonical=new URL(process.env.DATABASE_URL!);
if(!['localhost','127.0.0.1','[::1]'].includes(canonical.hostname))throw new Error('Provision a dedicated TEST_DATABASE_URL explicitly for remote hosts');
const name='genesis_runtime_v1_test';if(canonical.pathname==='/'+name)throw new Error('Canonical/test database collision');
const admin=new URL(canonical);admin.pathname='/postgres';const pool=new pg.Pool({connectionString:admin.href});
try{if(!(await pool.query('SELECT 1 FROM pg_database WHERE datname=$1',[name])).rowCount)await pool.query('CREATE DATABASE genesis_runtime_v1_test');}finally{await pool.end();}
const test=new URL(canonical);test.pathname='/'+name;
writeFileSync('outputs/runtime-v1/test-db.env','TEST_DATABASE_URL='+test.href+'\n',{mode:0o600});
const b=JSON.parse(readFileSync('outputs/runtime-v1/PRIVATE_BASELINE_BACKUP.json','utf8'));if(b.sha256!=='3377c9dddbe2abf89ed9a820a6aabbc1da951cac7bfc1823471c5aac043ea312')throw new Error('Baseline mismatch');
console.log('Dedicated local test database prepared; credentials not printed.');

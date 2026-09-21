import pg from 'pg';
import {readFileSync} from 'node:fs';
import {randomUUID} from 'node:crypto';
import {migrate} from '../../runtime/migrate.ts';
import {migrateRuntimeV1} from '../../runtime/migrate-v1.ts';
export async function deploymentFixture<T>(run:(pool:pg.Pool,url:string,schema:string,roles:{observer:string;reader:string;worker:string;operator:string})=>Promise<T>){
 const url=process.env.TEST_DATABASE_URL;if(!url||new URL(url).pathname!=='/genesis_runtime_v1_test'||process.env.DATABASE_URL)throw Error('TEST_DATABASE_ONLY');
 const suffix=randomUUID().replaceAll('-',''),schema='awakening_test_deployment_'+suffix;
 const admin=new pg.Pool({connectionString:url}),roles={observer:'ob_'+suffix,reader:'rd_'+suffix,worker:'wk_'+suffix,operator:'op_'+suffix};
 await admin.query(`CREATE SCHEMA ${schema}`);for(const r of Object.values(roles))await admin.query(`CREATE ROLE ${r} NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS`);
 const pool=new pg.Pool({connectionString:url,options:`-c search_path=${schema}`,max:8});
 try{
 await migrate(pool);const o=JSON.parse(readFileSync('tests/fixtures/genesis-dormant-sanitized.json','utf8'));
 await pool.query("INSERT INTO genesis_organisms(id,state) VALUES('genesis',$1)",[o]);await pool.query("INSERT INTO genesis_schedule(id,enabled) VALUES('genesis',false)");
 for(let n=1;n<=7;n++)await pool.query('INSERT INTO genesis_decisions(id,cycle,at,record) VALUES($1,$2,$3,$4)',['fixture-history-'+n,n,o.bornAt,{id:'fixture-history-'+n,cycle:n,at:o.bornAt,fixture:true,neural:{behavior:'UNKNOWN'},brainAfter:n===7?o.brain:null,frames:n===7?[{tick:o.brain.payload.tick,activity:o.brain.payload.activity,stimulated:[]}]:[]}]);
 await migrateRuntimeV1(pool,{organismId:o.id,bornAt:o.bornAt,cycles:7});return await run(pool,url,schema,roles);
 }finally{await pool.end();await admin.query(`DROP SCHEMA ${schema} CASCADE`);for(const r of Object.values(roles)){await admin.query(`DROP OWNED BY ${r}`);await admin.query(`DROP ROLE ${r}`);}await admin.end();}
}

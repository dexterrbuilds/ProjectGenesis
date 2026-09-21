import pg from 'pg';
import {readFileSync} from 'node:fs';
import {migrate} from '../../runtime/migrate.ts';
import {migrateRuntimeV1} from '../../runtime/migrate-v1.ts';
import {IsolatedCycle} from '../../server/isolated-cycle.ts';
export async function activeFixture<T>(run:(h:IsolatedCycle,schema:string,url:string)=>Promise<T>){
 const url=process.env.TEST_DATABASE_URL;if(!url||new URL(url).pathname!=='/genesis_runtime_v1_test'||process.env.DATABASE_URL)throw new Error('Dedicated TEST_DATABASE_URL only; no canonical credentials');
 const admin=new pg.Pool({connectionString:url});const schema='awakening_test_'+crypto.randomUUID().replaceAll('-','');await admin.query(`CREATE SCHEMA ${schema}`);
 const pool=new pg.Pool({connectionString:url,options:`-c search_path=${schema}`,max:8});
 try{
  await migrate(pool);const o=JSON.parse(readFileSync('tests/fixtures/genesis-dormant-sanitized.json','utf8'));
  await pool.query("INSERT INTO genesis_organisms(id,state) VALUES('genesis',$1)",[o]);await pool.query("INSERT INTO genesis_schedule(id,enabled) VALUES('genesis',false)");
  // Historical fixture rows only; no model run, no invented V2 decisions.
  for(let n=1;n<=7;n++)await pool.query('INSERT INTO genesis_decisions(id,cycle,at,record) VALUES($1,$2,$3,$4)',['fixture-history-'+n,n,o.bornAt,{id:'fixture-history-'+n,cycle:n,at:o.bornAt,fixture:true,neural:{behavior:'UNKNOWN'},brainAfter:n===7?o.brain:null,frames:n===7?[{tick:o.brain.payload.tick,activity:o.brain.payload.activity,stimulated:[]}]:[]}]);
  await migrateRuntimeV1(pool,{organismId:o.id,bornAt:o.bornAt,cycles:7});
  await pool.query("UPDATE genesis_life_state SET record=jsonb_set(record,'{executionLock}','\"OPEN\"') WHERE organism_id='genesis'");
  const h=await IsolatedCycle.connect(pool);await h.installPreparationSchema();return await run(h,schema,url);
 }finally{await pool.end();await admin.query(`DROP SCHEMA ${schema} CASCADE`);await admin.end();}
}

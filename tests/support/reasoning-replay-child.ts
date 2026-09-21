// Spawned ONLY by disposable integration tests. It cannot dispatch or claim.
import pg from 'pg';
import {OneShotController} from '../../server/one-shot.ts';
const schema=process.env.PROVIDER_TEST_SCHEMA;
if(!process.env.TEST_DATABASE_URL||!schema||!/^awakening_test_[a-f0-9]+$/.test(schema)||process.env.DATABASE_URL)throw Error('FIXTURE_ONLY');
const pool=new pg.Pool({connectionString:process.env.TEST_DATABASE_URL,options:`-c search_path=${schema}`,max:3});
try{const db=(await pool.query('SELECT current_database() db')).rows[0].db;if(db!=='genesis_runtime_v1_test')throw Error('FIXTURE_ONLY');const h=new OneShotController(pool),f=JSON.parse(process.env.PROVIDER_TEST_FENCE!);const p=process.env.PROVIDER_TEST_PREPARE==='yes'?await h.prepare(f,await h.admittedReasoningPlanner(f,{admissionId:'admission-fixture',owner:'fresh-child',secretResolver:{resolve:async()=> 'fixture-only-provider-canary-abcdefghijklmnopqrstuvwxyz'}})):await h.resumeReceived(f);process.stdout.write(JSON.stringify(p));if(process.env.PROVIDER_TEST_PREPARE==='yes')process.exit(0);}finally{await pool.end();}

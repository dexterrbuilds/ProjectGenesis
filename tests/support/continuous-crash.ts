import {tailFaultPool} from './lease-tail-fault.ts';
import pg from 'pg';
import {ContinuousController} from '../../server/continuous.ts';
import {ContinuousWorker} from '../../server/continuous-worker.ts';
import {ProductFallback} from '../../core/v2/planner.ts';
if(process.env.DATABASE_URL||new URL(process.env.TEST_DATABASE_URL!).pathname!=='/genesis_runtime_v1_test'||!/^awakening_test_[a-f0-9]+$/.test(process.env.FIXTURE_SCHEMA??''))throw Error('Fixture only');
const pool=new pg.Pool({connectionString:process.env.TEST_DATABASE_URL,options:`-c search_path=${process.env.FIXTURE_SCHEMA}`});
const h=new ContinuousController(tailFaultPool(pool,async phase=>{if(phase===process.argv[2])process.exit(77);})),w=new ContinuousWorker(h,'continuous-fixture',{identity:'fixture-local',planner:{propose:async c=>({...await new ProductFallback().propose(c),kind:'PROPOSAL',followUp:{kind:'CONTINUATION',availableAt:new Date(Date.now()+60000).toISOString(),reason:'Later local review'}})}},true);
await w.tick(undefined,async phase=>{if(phase===process.argv[2])process.exit(77);});throw Error('Crash checkpoint not reached');

/** One-time reviewed baseline migration. Never used by boot, tests or scheduler. */
import pg from 'pg';
import {readFileSync,writeFileSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {migrateRuntimeV1,rowDigest} from '../runtime/migrate-v1.ts';
const BASELINE='3377c9dddbe2abf89ed9a820a6aabbc1da951cac7bfc1823471c5aac043ea312';
const fileHash=(p:string)=>createHash('sha256').update(readFileSync(p)).digest('hex');
if(process.argv[2]!=='--apply-reviewed-baseline'||!process.env.DATABASE_URL)throw new Error('Explicit reviewed migration invocation required');
const backup=JSON.parse(readFileSync('outputs/runtime-v1/PRIVATE_BASELINE_BACKUP.json','utf8'));
const dry=JSON.parse(readFileSync('outputs/runtime-v1/MIGRATION_DRY_RUN.json','utf8'));
const frozen=JSON.parse(readFileSync('outputs/runtime-v1/FROZEN_AFTER.json','utf8'));
if(backup.sha256!==BASELINE||rowDigest(backup.rows)!==BASELINE||!dry.passed||!dry.backupRestorationVerified||!dry.originalRowsPreserved||dry.beforeDigest!==BASELINE||!frozen.preserved)throw new Error('Backup/dry-run/preservation prerequisite failed');
if(dry.migrationSqlSha256!==fileHash('runtime/migrations/003_runtime_v1.sql')||dry.migrationCodeSha256!==fileHash('runtime/migrate-v1.ts'))throw new Error('Migration changed after dry-run');
const workers=execFileSync('/bin/ps',['-axo','pid=,comm=,args='],{encoding:'utf8'}).split('\n').filter(line=>/\b(node|tsx|npm)\b/.test(line)&&/(runtime\/main\.(ts|js)|scripts\/run-life\.mjs|npm run runtime|npm run life)/.test(line)&&!line.includes('runtime-v1-apply.ts'));
if(workers.length)throw new Error('Possible mutating runtime/CLI worker detected; refusing migration');
const resultPath='outputs/runtime-v1/CANONICAL_MIGRATION.json';if(existsSync(resultPath))throw new Error('Migration execution record already exists');
const o=backup.rows.genesis_organisms[0].state;
if(o.cycles!==7||backup.rows.genesis_decisions.length!==7||backup.rows.genesis_schedule[0].enabled||backup.rows.genesis_organisms[0].lease)throw new Error('Frozen identity/schedule/lease prerequisites failed');
const pool=new pg.Pool({connectionString:process.env.DATABASE_URL,max:1});
try{
 const applied=await migrateRuntimeV1(pool,{organismId:o.id,bornAt:o.bornAt,cycles:7,baselineDigest:BASELINE,requireExclusiveClient:true});
 writeFileSync(resultPath,JSON.stringify({at:new Date().toISOString(),...applied,beforeDigest:BASELINE,backupVerified:true,restorationDryRunVerified:true,possibleMutatingProcesses:workers.length,sqlHash:dry.migrationSqlSha256,codeHash:dry.migrationCodeSha256,originalRowsPreservedInsideTransaction:true,scheduleEnabled:false,executionLock:'CLOSED'},null,2)+'\n',{mode:0o600});
 console.log(JSON.stringify({applied:applied.applied,originalRowsPreserved:true,executionLock:'CLOSED',scheduleEnabled:false}));
}finally{await pool.end();}

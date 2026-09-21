import {readFileSync,writeFileSync} from 'node:fs';
import pg from 'pg';
import {poolConfig,databaseTarget} from './config.ts';
import {planInstall,applyInstall} from './install.ts';
async function main(){
 const env=process.env,url=env.GENESIS_MIGRATION_DATABASE_URL;
 if(!url||env.GENESIS_MIGRATION_MODE!=='explicit'||!env.GENESIS_INSTALL_PLAN_FILE)throw Error('EXPLICIT_INSTALLER_REQUIRED');
 const verb=process.argv[2];if(!['plan','apply'].includes(verb))throw Error('UNKNOWN_INSTALL_MODE');
 process.stdout.write(JSON.stringify({target:databaseTarget(url,env.GENESIS_DB_SCHEMA??'public'),operation:verb})+'\n');
 const pool=new pg.Pool(poolConfig(url,'migration'));pool.on('error',()=>process.stderr.write('MIGRATION_DATABASE_UNAVAILABLE\n'));
 try{
 if(verb==='plan'){
 if(!env.GENESIS_EXPECTED_ORGANISM_ID||!env.GENESIS_EXPECTED_BIRTH||!env.GENESIS_DB_ROLES_FILE)throw Error('EXPECTED_BASELINE_REQUIRED');
 const plan=await planInstall(pool,url,env.GENESIS_EXPECTED_ORGANISM_ID,env.GENESIS_EXPECTED_BIRTH,JSON.parse(readFileSync(env.GENESIS_DB_ROLES_FILE,'utf8')));
 writeFileSync(env.GENESIS_INSTALL_PLAN_FILE,JSON.stringify(plan,null,2)+'\n',{mode:0o600,flag:'wx'});process.stdout.write(JSON.stringify({dryRun:true,planHash:plan.hash})+'\n');
 }else process.stdout.write(JSON.stringify(await applyInstall(pool,url,JSON.parse(readFileSync(env.GENESIS_INSTALL_PLAN_FILE,'utf8')),env.GENESIS_INSTALL_ACK??''))+'\n');
 }finally{await pool.end();}
}
main().catch(()=>{process.stderr.write('INSTALLATION_REFUSED: inspect the reviewed target and plan; no success is asserted.\n');process.exitCode=1;});

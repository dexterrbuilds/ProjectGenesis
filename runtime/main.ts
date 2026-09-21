/** Observation only. Boot never installs schemas, initializes an organism or starts a worker. */
import pg from 'pg';
import {readConfig} from './config.ts';
import {verifyEvidence} from '../core/v2/biology.ts';
import {LifeStore} from '../server/store.ts';
import {GenesisService} from './service.ts';
import {dormantMode,poolConfig} from './deployment/config.ts';
import {observationServer,stopObservation} from './deployment/http-server.ts';
import {logRecord} from './deployment/log.ts';
import {runtimeIdentity} from '../server/one-shot-spec.ts';
async function main(){
 const expected=dormantMode();
 // No operator credential is needed by a public observation service.
 const config=readConfig({...process.env,GENESIS_OPERATOR_TOKEN:'observation-only-no-mutation-authority',GENESIS_PLANNER_MODE:'local'});
 const pool=new pg.Pool(poolConfig(config.databaseUrl,'observation'));
 pool.on('error',()=>console.error(logRecord('runtime','NOT_READY')));
 verifyEvidence();const service=new GenesisService(new LifeStore(pool),config);
 const server=observationServer(service,pool,expected);
 server.listen(config.port,config.host,()=>console.log(logRecord('runtime','STARTED',runtimeIdentity().sha256)));
 let stopping=false;const stop=async()=>{if(stopping)return;stopping=true;console.log(logRecord('runtime','STOPPING'));const hard=setTimeout(()=>process.exit(1),12000);hard.unref();await stopObservation(server,pool);clearTimeout(hard);console.log(logRecord('runtime','STOPPED'));};
 process.on('SIGTERM',()=>void stop());process.on('SIGINT',()=>void stop());
}
main().catch(()=>{console.error(logRecord('runtime','REFUSED'));process.exitCode=1;});

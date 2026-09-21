/** No default execution mode. Manual, authenticated, single-use launch request on stdin. */
import {readFileSync} from 'node:fs';
import pg from 'pg';
import {OperatorAuthentication} from '../../server/operator-auth.ts';
import {consumeExisting,consumerRequest} from './consumer.ts';
import {poolConfig} from './config.ts';
import {logRecord} from './log.ts';
async function main(){
 const e=process.env;if(e.GENESIS_CONSUMER_MODE!=='explicit'||!e.GENESIS_OPERATOR_AUTH_FILE||!e.GENESIS_OPERATOR_DATABASE_URL||!e.GENESIS_WORKER_DATABASE_URL)throw Error('CONSUMER_DISABLED');
 const conf=JSON.parse(readFileSync(e.GENESIS_OPERATOR_AUTH_FILE,'utf8'));if(conf.mode!=='production')throw Error('PRODUCTION_AUTH_REQUIRED');const auth=new OperatorAuthentication(conf),principal=auth.authenticate(e.GENESIS_OPERATOR_CREDENTIAL??'');
 let body='';for await(const chunk of process.stdin){body+=chunk;if(Buffer.byteLength(body)>8192)throw Error('REQUEST_TOO_LARGE');}const request=consumerRequest.parse(JSON.parse(body));
 const op=new pg.Pool(poolConfig(e.GENESIS_OPERATOR_DATABASE_URL,'private-consumer')),worker=new pg.Pool(poolConfig(e.GENESIS_WORKER_DATABASE_URL,'worker'));
 for(const pool of [op,worker])pool.on('error',()=>console.error(logRecord('consumer','NOT_READY')));
 const abort=new AbortController();let hard:ReturnType<typeof setTimeout>|undefined;const stop=()=>{abort.abort();hard??=setTimeout(()=>process.exit(1),12000);hard.unref();};process.on('SIGTERM',stop);process.on('SIGINT',stop);
 try{await consumeExisting(request,op,worker,auth,principal,abort.signal);console.log(logRecord('consumer','COMPLETED'));}finally{await Promise.all([op.end(),worker.end()]);if(hard)clearTimeout(hard);}
}
main().catch(()=>{console.error(logRecord('consumer','REFUSED'));process.exitCode=1;});

/** Separate private administration entrypoint. Never imported by runtime/main or Next.
 * Command JSON is stdin; the credential is an external secret environment reference,
 * never an argument, command payload, audit field or stdout diagnostic. No execution verb. */
import {readFileSync} from 'node:fs';
import pg from 'pg';
import {poolConfig} from './deployment/config.ts';
import {requireRole} from './deployment/schema.ts';
import {OperatorAuthentication} from '../server/operator-auth.ts';
import {OperatorControl} from '../server/operator-control.ts';
async function main(){
 if(process.env.GENESIS_PRIVATE_OPERATOR_MODE!=='enabled'||!process.env.GENESIS_OPERATOR_AUTH_FILE||!process.env.GENESIS_OPERATOR_DATABASE_URL)throw Error('PRIVATE_OPERATOR_DISABLED');
 const config=JSON.parse(readFileSync(process.env.GENESIS_OPERATOR_AUTH_FILE,'utf8'));
 if(config.mode!=='production')throw Error('PRODUCTION_AUTH_CONFIGURATION_REQUIRED');
 const auth=new OperatorAuthentication(config),principal=auth.authenticate(process.env.GENESIS_OPERATOR_CREDENTIAL??'');
 let body='';for await(const chunk of process.stdin){body+=chunk;if(Buffer.byteLength(body)>32768)throw Error('COMMAND_TOO_LARGE');}
 const pool=new pg.Pool({...poolConfig(process.env.GENESIS_OPERATOR_DATABASE_URL,'operator'),max:1});
 pool.on('error',()=>process.stderr.write('OPERATOR_DATABASE_UNAVAILABLE\n'));
 try{const c=await pool.connect();try{await requireRole(c,'operator');}finally{c.release();}const result=await new OperatorControl(pool,auth).execute(principal,JSON.parse(body));process.stdout.write(JSON.stringify({ok:true,result})+'\n');}finally{await pool.end();}
}
main().catch(()=>{process.stderr.write('Private operator command refused. No success is asserted; inspect durable audit state through an authorized operator.\n');process.exitCode=1;});

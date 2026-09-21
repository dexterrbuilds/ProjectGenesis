/** Production connection configuration; no credentials or connection strings in diagnostics. */
import {readFileSync} from 'node:fs';
import type {PoolConfig} from 'pg';
export function poolConfig(url:string,service:string,env:Record<string,string|undefined>=process.env):PoolConfig{
 let u:URL;try{u=new URL(url);}catch{throw Error('DATABASE_TARGET_INVALID');}
 if(!['postgres:','postgresql:'].includes(u.protocol)||!/^\/[a-zA-Z0-9_-]+$/.test(u.pathname)||u.search||u.hash)throw Error('DATABASE_TARGET_INVALID');
 const production=env.NODE_ENV==='production';
 if(!production&&!(u.pathname==='/genesis_runtime_v1_test'&&['localhost','127.0.0.1','[::1]'].includes(u.hostname)))throw Error('FIXTURE_DATABASE_REQUIRED');
 const number=(key:string,fallback:number,max:number)=>{const n=Number(env[key]??fallback);if(!Number.isSafeInteger(n)||n<1||n>max)throw Error('DATABASE_CONFIGURATION_INVALID');return n;};
 if(production&&env.GENESIS_DB_TLS!=='verify-full')throw Error('VERIFIED_DATABASE_TLS_REQUIRED');
 const role=env.GENESIS_DB_ROLE;if(production&&role)throw Error('DEDICATED_LOGIN_REQUIRED');if(role&&!/^[a-z][a-z0-9_]{0,62}$/.test(role))throw Error('DATABASE_ROLE_INVALID');
 const schema=env.GENESIS_DB_SCHEMA??'public';if(!/^[a-z][a-z0-9_]{0,62}$/.test(schema))throw Error('DATABASE_SCHEMA_INVALID');
 return {connectionString:url,ssl:production?{rejectUnauthorized:true,...(env.GENESIS_DB_CA_FILE?{ca:readFileSync(env.GENESIS_DB_CA_FILE,'utf8')}:{})}:false,max:number('GENESIS_DB_POOL_MAX',4,16),connectionTimeoutMillis:number('GENESIS_DB_CONNECT_TIMEOUT_MS',5000,30000),statement_timeout:number('GENESIS_DB_STATEMENT_TIMEOUT_MS',15000,60000),idle_in_transaction_session_timeout:20000,query_timeout:20000,idleTimeoutMillis:30000,maxLifetimeSeconds:300,application_name:'genesis-'+service,options:`-c search_path=${schema} -c lock_timeout=5000${role?' -c role='+role:''}`};
}
export function dormantMode(env:Record<string,string|undefined>=process.env){
 if(env.GENESIS_RUNTIME_MODE!=='dormant')throw Error('EXPLICIT_DORMANT_MODE_REQUIRED');
 for(const k of ['GENESIS_AUTONOMY_ENABLED','GENESIS_INTERNET','GENESIS_WORKER_ENABLED','GENESIS_SCHEDULER_ENABLED','GENESIS_PROVIDER_ENABLED'])if(env[k]&&env[k]!=='false')throw Error('DORMANT_CONFIGURATION_CONFLICT');
 for(const k of ['OPENAI_API_KEY','OPENAI_MODEL','SOLANA_RPC_URL','SOLANA_WALLET_ADDRESS','SOLANA_NETWORK'])if(env[k])throw Error('DORMANT_CREDENTIAL_SCOPE_CONFLICT');
 if(Object.keys(env).some(k=>k.startsWith('GENESIS_PROVIDER_')&&k!=='GENESIS_PROVIDER_ENABLED'&&env[k]))throw Error('DORMANT_CREDENTIAL_SCOPE_CONFLICT');
 if(!env.GENESIS_EXPECTED_ORGANISM_ID||!env.GENESIS_EXPECTED_BIRTH)throw Error('EXPECTED_IDENTITY_REQUIRED');
 return {organismId:env.GENESIS_EXPECTED_ORGANISM_ID,bornAt:env.GENESIS_EXPECTED_BIRTH};
}
export function databaseTarget(url:string,schema:string){const u=new URL(url);return {host:u.hostname,port:u.port||'5432',database:u.pathname.slice(1),schema};}

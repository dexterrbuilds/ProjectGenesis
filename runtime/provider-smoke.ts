/** PREPARED ONLY. Private manually authorized transport test; never imported at boot.
 * No Genesis context, decisions, grants, schema writes, cycle calls or retries.
 * Requires a separately reviewed, tiny-output admission and one-use private journal.
 */
import {readFileSync,openSync,writeSync,fsyncSync,closeSync,statSync} from 'node:fs';
import {resolve} from 'node:path';
import {z} from 'zod';
import pg from 'pg';
import {poolConfig} from './deployment/config.ts';
import {requireRole} from './deployment/schema.ts';
import {OperatorAuthentication} from '../server/operator-auth.ts';
import {compatibleAdmission} from '../server/reasoning/store.ts';
import {environmentSecrets,noSecret,replySchema,outputSchema} from '../server/reasoning/contracts.ts';
import {resolveAdapter} from '../server/reasoning/factory.ts';
import {completeWire,accountWire,cost} from '../server/reasoning/request.ts';
import {digest} from '../core/v2/identity.ts';
import type {WorkingContext} from '../core/v2/contracts.ts';
const authSchema=z.object({version:z.literal(1),purpose:z.literal('SANITIZED_PROVIDER_SMOKE_ONLY'),id:z.string().regex(/^[a-zA-Z0-9_-]{1,80}$/),actorId:z.string(),admissionId:z.string(),admissionHash:z.string().length(64),wireHash:z.string().length(64),maximumMicros:z.number().int().positive(),expiresAt:z.string().datetime(),authorizationReference:z.string().min(1).max(180)}).strict();
async function main(){
 if(process.env.GENESIS_PRIVATE_OPERATOR_MODE!=='enabled'||!process.env.GENESIS_OPERATOR_AUTH_FILE||!process.env.GENESIS_OPERATOR_DATABASE_URL||!process.env.GENESIS_SMOKE_AUTHORIZATION_FILE||!process.env.GENESIS_SMOKE_JOURNAL_DIRECTORY)throw Error();
 const config=JSON.parse(readFileSync(process.env.GENESIS_OPERATOR_AUTH_FILE,'utf8'));if(config.mode!=='production')throw Error();
 const auth=new OperatorAuthentication(config),principal=auth.authenticate(process.env.GENESIS_OPERATOR_CREDENTIAL??''),permit=authSchema.parse(JSON.parse(readFileSync(process.env.GENESIS_SMOKE_AUTHORIZATION_FILE,'utf8')));
 if(permit.actorId!==principal.actorId||Date.parse(permit.expiresAt)<=Date.now())throw Error();
 const dir=resolve(process.env.GENESIS_SMOKE_JOURNAL_DIRECTORY),st=statSync(dir);if(!st.isDirectory()||(st.mode&0o077)!==0||st.uid!==process.getuid?.())throw Error();
 const pool=new pg.Pool({...poolConfig(process.env.GENESIS_OPERATOR_DATABASE_URL,'provider-smoke'),max:1});let fd:number|undefined;let sent=false;pool.on('error',()=>process.stderr.write('SMOKE_DATABASE_UNAVAILABLE\n'));
 try{
  const c=await pool.connect();try{await requireRole(c,'operator');}finally{c.release();}
  const validate=async()=>{auth.assert(principal);if(Date.parse(permit.expiresAt)<=Date.now())throw Error();const actor=(await pool.query('SELECT enabled,capabilities FROM genesis_operator_actors WHERE id=$1',[principal.actorId])).rows[0];if(!actor?.enabled||!actor.capabilities.includes('MANAGE_PROVIDER_ADMISSION'))throw Error();const r=(await pool.query('SELECT payload,payload_hash,status FROM genesis_provider_admissions WHERE id=$1',[permit.admissionId])).rows[0];if(!r||r.status!=='ADMITTED'||r.payload_hash!==permit.admissionHash||digest(r.payload)!==permit.admissionHash)throw Error();const a=compatibleAdmission(r.payload);if(a.provider==='fixture'||Date.parse(a.effectiveAt)>Date.now()||Date.parse(a.expiresAt)<=Date.now()||a.maximumOutputTokens>128)throw Error();return a;};
  const a=await validate();const text=JSON.stringify({purpose:'Transport and schema verification only. Return ABSTAIN with no changes or tools.',identity:'sanitized-smoke-fixture-not-Genesis',currentEvent:{id:'smoke',observedAt:'2000-01-01T00:00:00.000Z'},facts:[],permissions:{externalEffects:false}});
  const context={text,hash:digest(text)} as WorkingContext,wire=completeWire(a,context),accounting=accountWire(a,wire,permit.maximumMicros);if(digest(wire)!==permit.wireHash)throw Error();
  const secret=await environmentSecrets.resolve(a.secretReference);noSecret(permit,secret);noSecret(wire,secret);
  fd=openSync(resolve(dir,permit.id+'.jsonl'),'wx',0o600);const record=(v:unknown)=>{writeSync(fd!,JSON.stringify(v)+'\n');fsyncSync(fd!);};
  record({status:'RESERVED',authorizationHash:digest(permit),actorId:principal.actorId,admissionHash:digest(a),wireHash:digest(wire),reservationMicros:accounting.reservation,at:new Date().toISOString(),genesisContext:false,genesisAuthority:false});
  const abort=new AbortController(),timer=setTimeout(()=>abort.abort(),a.timeoutMs);const poll=setInterval(()=>void validate().catch(()=>abort.abort()),100);
  try{await validate();record({status:'DISPATCHING_OUTCOME_UNKNOWN',at:new Date().toISOString(),automaticRetry:false});sent=true;
   const reply=await resolveAdapter(a,false).send(wire,secret,abort.signal);noSecret(reply,secret);replySchema.parse(reply);if(reply.admissionHash!==digest(a)||reply.model!==a.model)throw Error();const p=outputSchema.parse(typeof reply.structured==='string'?JSON.parse(reply.structured):reply.structured);if(p.kind!=='ABSTAIN'||p.contextHash!==context.hash||p.changes.length||p.tool!==null||!reply.usage)throw Error();const amount=cost(a,reply.usage);if(amount>accounting.reservation)throw Error();record({status:'RECEIVED',responseHash:digest(reply),responseId:reply.responseId,providerRequestId:reply.requestId,usage:reply.usage,costMicros:amount,structuredValidated:true,at:new Date().toISOString()});
  }finally{clearTimeout(timer);clearInterval(poll);}
 }catch{if(fd!==undefined){writeSync(fd,JSON.stringify({status:sent?'AMBIGUOUS_REVIEW_REQUIRED':'NOT_SENT',automaticRetry:false})+'\n');fsyncSync(fd);}throw Error('SMOKE_STOPPED_REVIEW_REQUIRED');}finally{if(fd!==undefined)closeSync(fd);await pool.end();}
}
main().catch(()=>{process.stderr.write('Provider smoke refused or stopped. Inspect the private one-use journal; no automatic retry.\n');process.exitCode=1;});

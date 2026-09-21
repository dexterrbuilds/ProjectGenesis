import {createHash,randomUUID} from 'node:crypto';
import {oneShotFixture} from './one-shot-fixture.ts';
import {ContinuousController} from '../../server/continuous.ts';
import {OperatorControl,type OperatorCommand} from '../../server/operator-control.ts';
import {OperatorAuthentication,CAPABILITIES} from '../../server/operator-auth.ts';
import {installProviderFixture} from '../../server/reasoning/store.ts';
import {implementationHashes} from '../../server/reasoning/factory.ts';
import {SCHEMA_HASH,PLANNER_HASH,type Admission} from '../../server/reasoning/contracts.ts';
import {identities} from '../../server/one-shot-spec.ts';
import {digest} from '../../core/v2/identity.ts';
export const TEST_SECRET='fixture-only-provider-canary-abcdefghijklmnopqrstuvwxyz';
export function fixtureAdmission():Admission{
 const i=identities(),h=implementationHashes();const categories=[{id:'input',unit:'fixture-token',microsNumerator:1,denominator:2,maximumUnits:12000},{id:'output',unit:'fixture-token',microsNumerator:2,denominator:1,maximumUnits:1200},{id:'reasoning',unit:'fixture-token',microsNumerator:1,denominator:1,maximumUnits:100},{id:'requests',unit:'request',microsNumerator:3,denominator:1,maximumUnits:1}];
 return {version:2,id:'admission-fixture',provider:'fixture',model:'fixture-model',adapter:{id:'fixture-v1',hash:h.adapter},format:'genesis-json-envelope-v1',schemaHash:SCHEMA_HASH,plannerHash:PLANNER_HASH,runtimeHash:i.runtime.sha256,constitutionHash:i.constitution.hash,policyHash:i.policy.hash,audience:'PROVIDER',reasoning:{hiddenContent:false,effort:'none'},endpoint:null,secretReference:'fixture:PROVIDER',counting:{id:'complete-request-bound-v1',hash:h.counter,strategy:'FIXED_WORST_CASE',maxWireBytes:128000,inputBound:12000,evidence:'fixture-only-bound-not-a-production-tokenizer'},rateCard:{id:'fixture-card',reference:'fixture-only-not-production-prices',currency:'USD',categories,hash:digest({currency:'USD',categories}),completeCategoriesAttested:true},maximumInputTokens:12000,maximumOutputTokens:1200,perAttemptMicros:50000,perCycleMicros:50000,dailyMicros:100000,timeoutMs:2000,maximumAttempts:1,automaticRetries:0,effectiveAt:new Date(Date.now()-1000).toISOString(),expiresAt:new Date(Date.now()+600000).toISOString(),reviewReference:'review:fixture-provider'};
}
export async function reasoningFixture<T>(run:(x:Awaited<ReturnType<typeof setup>>)=>Promise<T>){return oneShotFixture(async(h,g,schema,url)=>run(await setup(h,g,schema,url)));}
async function setup(h:Parameters<Parameters<typeof oneShotFixture>[0]>[0],original:Parameters<Parameters<typeof oneShotFixture>[0]>[1],schema:string,url:string){
 await new ContinuousController(h.pool).installFixtureSchema();const auth=new OperatorAuthentication({enabled:true,mode:'test',keys:[{id:'fixture-key',actorId:'operator-a',sha256:createHash('sha256').update(TEST_SECRET).digest('hex'),expiresAt:'2099-01-01T00:00:00.000Z'}]});const op=new OperatorControl(h.pool,auth);await op.installFixtureSchema();await installProviderFixture(h.pool);await h.pool.query('INSERT INTO genesis_operator_actors(id,enabled,capabilities) VALUES($1,true,$2)',['operator-a',CAPABILITIES]);const principal=auth.authenticate(TEST_SECRET);
 const call=(operation:OperatorCommand['operation'],v:Partial<OperatorCommand>={})=>op.execute(principal,{id:'cmd:'+randomUUID(),organismId:original.organismId,operation,targetId:null,expectedHash:null,reasonReference:'review:fixture-provider',payload:null,...v});
 const targetHash=async(table:string,id:string)=>digest(JSON.parse(JSON.stringify((await h.pool.query(`SELECT * FROM ${table} WHERE id=$1`,[id])).rows[0])));
 const a=fixtureAdmission(),permission={...original.permission,llm:true,maxAttempts:1,maxCostMicros:50000};
 const g={...original,issuer:'operator-a',authorizationReference:a.reviewReference,permission,permissionHash:digest(permission),planner:{identity:'provider:fixture:fixture-model',provider:'fixture',model:a.model,admissionHash:digest(a)}};
 const admit=async()=>{g.planner.admissionHash=digest(a);await call('propose_provider',{targetId:a.id,payload:a});await call('admit_provider',{targetId:a.id,expectedHash:await targetHash('genesis_provider_admissions',a.id)});};
 const authorize=async()=>{await call('propose_grant',{targetId:g.id,payload:g});await call('authorize_grant',{targetId:g.id,expectedHash:await targetHash('genesis_execution_grants',g.id)});};
 const options={admissionId:a.id,owner:'fixture-worker',secretResolver:{resolve:async()=>TEST_SECRET}};
 const count=async()=>Number((await h.pool.query('SELECT count(*) n FROM genesis_decisions')).rows[0].n);
 return {h,g,a,call,targetHash,admit,authorize,options,count,schema,url};
}

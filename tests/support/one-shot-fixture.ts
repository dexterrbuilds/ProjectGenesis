import {activeFixture} from './active-fixture.ts';
import {OneShotController} from '../../server/one-shot.ts';
import {makeGrant,type OneShotGrant} from '../../server/one-shot-spec.ts';
import {CLOSED_PERMISSIONS,digest} from '../../core/v2/identity.ts';
export async function oneShotFixture<T>(run:(h:OneShotController,g:OneShotGrant,schema:string,url:string)=>Promise<T>){return activeFixture(async(old,schema,url)=>{
 await old.pool.query("UPDATE genesis_life_state SET record=jsonb_set(record,'{executionLock}','\"CLOSED\"')");const h=new OneShotController(old.pool);await h.installFixtureSchema();
 const base=(await h.pool.query('SELECT state,revision FROM genesis_organisms')).rows[0],ext=(await h.pool.query('SELECT revision FROM genesis_life_state')).rows[0];
 const g=makeGrant({id:'fixture-grant',organismId:base.state.id,stateRevision:Number(base.revision),lifeRevision:Number(ext.revision),issuer:'fixture-operator',authorizationReference:'fixture-only-explicit-authorization',permission:{...CLOSED_PERMISSIONS,execution:true,localArtifacts:true},planner:{identity:'product-deterministic-v1',provider:null,model:null,admissionHash:null},at:new Date(Date.now()-1000).toISOString(),expiresAt:new Date(Date.now()+600000).toISOString()});
 return run(h,g,schema,url);
});}
export async function authorize(h:OneShotController,g:OneShotGrant){await h.propose(g);await h.authorize(g.id,{payloadHash:digest(g),issuer:g.issuer,reference:g.authorizationReference});}

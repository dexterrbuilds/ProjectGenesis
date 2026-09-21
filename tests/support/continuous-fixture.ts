import {oneShotFixture} from './one-shot-fixture.ts';
import {ContinuousController} from '../../server/continuous.ts';
import {ContinuousWorker} from '../../server/continuous-worker.ts';
import {continuousIdentity,FORBIDDEN,type ContinuousScope} from '../../server/continuous-spec.ts';
import {EVENT_KINDS,LOCAL_PERMISSION,type RuntimeEvent,type EventPayload} from '../../core/v2/continuous.ts';
import {digest} from '../../core/v2/identity.ts';
import {ProductFallback} from '../../core/v2/planner.ts';
export async function continuousFixture<T>(run:(h:ContinuousController,s:ContinuousScope,w:ContinuousWorker,schema:string,url:string)=>Promise<T>,overrides:Partial<ContinuousScope>={}){return oneShotFixture(async(old,g,schema,url)=>{
 const h=new ContinuousController(old.pool);await h.installFixtureSchema();
 const s:ContinuousScope={version:1,kind:'CONTINUOUS_LOCAL_V1',id:'continuous-fixture',organismId:g.organismId,...continuousIdentity(),biologicalMode:'SAVED-OBSERVATION-ONLY',planner:{kind:'LOCAL_DETERMINISTIC',identity:'fixture-local',provider:null,model:null},allowedEvents:[...EVENT_KINDS],allowedEffects:['local_reflection','local_artifact','life_changes'],forbidden:[...FORBIDDEN],scheduling:true,permissionHash:digest(LOCAL_PERMISSION),minimumPriorDecisions:7,maxCycles:1000,windowMs:86400000,maxCyclesPerWindow:1000,maxConcurrent:1,maxCostPerCycleMicros:0,maxCostPerWindowMicros:0,leaseMs:30000,plannerTimeoutMs:1000,maxAttemptsPerEvent:2,backoffMs:10,maxDepth:3,maxFollowups:5,maxImmediatePerRoot:10,minimumDelayMs:0,issuedAt:new Date(Date.now()-1000).toISOString(),expiresAt:new Date(Date.now()+600000).toISOString(),issuer:'fixture-operator',authorizationReference:'fixture-only-continuous-authorization',...overrides};
 await h.proposeScope(s);await h.authorizeScope(s.id,{payloadHash:digest(s),issuer:s.issuer,reference:s.authorizationReference});return run(h,s,new ContinuousWorker(h,s.id,{identity:s.planner.identity,planner:new ProductFallback()},true),schema,url);
 });}
export function manual(s:ContinuousScope,id='manual',payload:EventPayload={kind:'MANUAL_EVENT',text:'Neutral local fixture event',references:[]}):RuntimeEvent{const at=new Date(Date.now()-50).toISOString();return {version:1,id,organismId:s.organismId,createdAt:at,availableAt:at,expiresAt:null,dedupKey:id,source:'operator',sourceRef:'fixture-operator',visibility:'private',disclosure:{internal:true,provider:false,public:false},parentEventId:null,parentCycleId:null,rootId:id,depth:0,payload};}
export const sleep=(ms:number)=>new Promise<void>(resolve=>setTimeout(resolve,ms));

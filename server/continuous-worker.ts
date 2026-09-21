import {ContinuousFenceError} from './continuous-authority.ts';
/** Inert unless explicitly enabled by a trusted caller. Not imported by runtime/main or public APIs. */
import {ContinuousController,SimulatedCrash,type PhaseHook} from './continuous.ts';
import type {PlannerV2} from '../core/v2/contracts.ts';
export class ContinuousWorker{
 readonly controller:ContinuousController;readonly scopeId:string;readonly planner:{identity:string;planner:PlannerV2};readonly enabled:boolean;readonly pollMs:number;
 constructor(controller:ContinuousController,scopeId:string,planner:{identity:string;planner:PlannerV2},enabled=false,pollMs=1000){this.controller=controller;this.scopeId=scopeId;this.planner=planner;this.enabled=enabled;this.pollMs=pollMs;if(!Number.isSafeInteger(pollMs)||pollMs<25||pollMs>60000)throw Error('Invalid worker poll interval');}
 async tick(signal?:AbortSignal,hook?:PhaseHook){
  if(!this.enabled)return {status:'DISABLED'} as const;if(signal?.aborted)return {status:'STOPPED'} as const;
  await hook?.('before_claim');await this.controller.recover();const f=await this.controller.claim(this.scopeId);if(!f)return {status:'IDLE_OR_BUDGET_BLOCKED'} as const;
  try{await hook?.('after_claim');const p=await this.controller.prepare(f,this.planner,signal,hook);if(signal?.aborted){await this.controller.fail(f,'CANCELLED',false);return {status:'CANCELLED'} as const;}
   const d=await this.controller.commit(f,p,hook);await hook?.('after_commit');return {status:'COMMITTED',decision:d} as const;
  }catch(e){if(e instanceof SimulatedCrash)throw e;
   const reason=e instanceof Error?e.message:'LOCAL_RUNTIME_FAILURE';
   // No paid planner retry. DB uncertainty remains a durable claim if closure also fails.
   await this.controller.fail(f,reason,e instanceof ContinuousFenceError&&e.recoverableLocal);return {status:'CLOSED_WITH_ERROR',reason} as const;
  }
 }
 async run(signal:AbortSignal,onTick?:(result:Awaited<ReturnType<ContinuousWorker['tick']>>)=>void){
  if(!this.enabled)return;while(!signal.aborted){const r=await this.tick(signal);onTick?.(r);if(signal.aborted)break;await new Promise<void>(resolve=>{const done=()=>{clearTimeout(timer);signal.removeEventListener('abort',done);resolve();};const timer=setTimeout(done,this.pollMs);signal.addEventListener('abort',done,{once:true});});}
 }
}

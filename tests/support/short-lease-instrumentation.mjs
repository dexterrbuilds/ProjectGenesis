/** PRIVATE TEST DIAGNOSTICS ONLY. In-memory source probes, never runtime imports. */
import {registerHooks} from 'node:module';
registerHooks({load(url,ctx,next){const r=next(url,ctx);
 const rules=url.endsWith('/core/v2/cycle.ts')?[
 ['policy=evaluatePolicy(',"globalThis.__genesisLeaseProbe?.('policy_start');policy=evaluatePolicy("],
 ["await phase?.('after_policy');","globalThis.__genesisLeaseProbe?.('policy_end');await phase?.('after_policy');"],
 ['const next=reduceLife(',"globalThis.__genesisLeaseProbe?.('reducer_start');const next=reduceLife("],
 ['next.biologicalContext.observationIds.push',"globalThis.__genesisLeaseProbe?.('reducer_end');next.biologicalContext.observationIds.push"]
 ]:url.endsWith('/server/continuous.ts')?[
 ['const p=await Promise.race([selected.planner.propose(ctx),interrupted]);',"globalThis.__genesisLeaseProbe?.('planner_start');const p=await Promise.race([selected.planner.propose(ctx),interrupted]);globalThis.__genesisLeaseProbe?.('planner_end');"],
 ["}finally{if(timer)clearTimeout(timer);", "}finally{globalThis.__genesisLeaseProbe?.('planner_cleanup');if(timer)clearTimeout(timer);"],
 ['brain=new SavedObservationAdapter(o.id);',"brain=(globalThis.__genesisLeaseProbe?.('saved_adapter_start'),new SavedObservationAdapter(o.id));globalThis.__genesisLeaseProbe?.('saved_adapter_end');"],
 ["timer=setTimeout(()=>reject(new Error('PLANNER_TIMEOUT')),scope.plannerTimeoutMs);","timer=setTimeout(()=>{globalThis.__genesisLeaseProbe?.('planner_timeout');reject(new Error('PLANNER_TIMEOUT'));},scope.plannerTimeoutMs);"]
 ]:url.endsWith('/server/continuous-authority.ts')?[
 ["if(!a||a.status!=='CLAIMED'", "globalThis.__genesisLeaseProbe?.('continuous_fence',{processWallMs:Date.now(),eventLeaseMs:new Date(e?.lease_until).getTime(),remainingMs:new Date(e?.lease_until).getTime()-Date.now(),attemptValid:!!a&&a.status==='CLAIMED'&&a.lease===f.lease&&a.scope_id===s.id&&a.event_id===f.eventId&&Number(a.base_revision)===f.baseRevision&&Number(a.life_revision)===f.lifeRevision,eventValid:!!e&&e.status==='CLAIMED'&&e.cycle_id===f.cycleId&&e.lease===f.lease});if(!a||a.status!=='CLAIMED'"]
 ]:[];
 if(!rules.length)return r;
 let s=typeof r.source==='string'?r.source:Buffer.from(r.source).toString();
 for(const [before,after] of rules){if(!s.includes(before))throw Error('DIAGNOSTIC_SOURCE_MISMATCH');s=s.replace(before,after);}return {...r,source:s};}});

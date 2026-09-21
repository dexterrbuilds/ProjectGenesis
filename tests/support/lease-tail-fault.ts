/** Driver-side fault injection; never part of the runtime's admitted transaction tail. */
import type pg from 'pg';
export function tailFaultPool(pool:pg.Pool,fault:(phase:string)=>Promise<void>):pg.Pool{
 return {query:pool.query.bind(pool),connect:async()=>{
  const c=await pool.connect();let admitted=false,followed=false;
  return {release:()=>c.release(),query:async(sql:string,args?:unknown[])=>{
   const child=admitted&&sql.startsWith('INSERT INTO genesis_runtime_events');
   const close=admitted&&sql.startsWith("UPDATE genesis_runtime_events SET status='CONSUMED'");
   if(child||close&&!followed)await fault('before_followup');
   const r=await c.query(sql,args);
   if(sql.startsWith('INSERT INTO genesis_decisions'))admitted=true;
   if(child||close&&!followed){followed=true;await fault('after_followup');}
   return r;
  }};
 }} as unknown as pg.Pool;
}

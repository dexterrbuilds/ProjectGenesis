import type pg from 'pg';
/** Adapter for trusted existing controllers inside an operator-owned transaction/savepoint.
 * Controllers' nested BEGIN/COMMIT are scopes, not independent commits. Any exception escapes
 * to the outer savepoint rollback. Never exported through the control protocol. */
export function transactionBoundPool(c:pg.PoolClient):pg.Pool{
 const query:pg.PoolClient['query']=((sql:unknown,...args:unknown[])=>{
  if(typeof sql==='string'&&/^\s*(BEGIN(?:\s+ISOLATION LEVEL REPEATABLE READ READ ONLY)?|COMMIT|ROLLBACK)\s*$/i.test(sql))return Promise.resolve({rows:[],rowCount:0});
  return (c.query as (...a:unknown[])=>unknown)(sql,...args);
 }) as pg.PoolClient['query'];
 return {query,connect:async()=>({query,release:()=>{}})} as unknown as pg.Pool;
}

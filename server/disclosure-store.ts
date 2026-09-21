import type pg from 'pg';
import {digest} from '../core/v2/identity.ts';
import {credentialLike,type MemoryArchive} from '../core/v2/memory.ts';
import {operational} from '../core/v2/operations.ts';
import type {Organism} from '../core/contracts.ts';
import type {LifeStateV1} from '../core/v2/contracts.ts';
import {NO_DISCLOSURE,type DisclosureSet,type DisclosureSource,type Audience} from '../core/v2/disclosure.ts';
/** Existing Pass-3 operational disclosure is not elevated. Only reviewed historical memory / bounded legacy project metadata can leave internal use. */
export function disclosureSources(o:Organism,l:LifeStateV1,a:MemoryArchive):DisclosureSource[]{
 const out:DisclosureSource[]=[];const add=(type:string,raw:unknown,internalOnly=true)=>{if(!raw||typeof raw!=='object'||typeof(raw as {id?:unknown}).id!=='string')return;out.push({type,id:(raw as {id:string}).id,hash:digest(raw),internalOnly:internalOnly||credentialLike(JSON.stringify(raw))});};
 a.legacy.forEach(x=>add('legacy_memory',x,false));a.episodes.forEach(x=>add('v2_episode',x));l.semanticMemory.forEach(x=>add('semantic_assertion',x));
 for(const p of o.businesses){const projection={id:p.id,name:p.name.slice(0,200),status:p.status,workCycles:p.workCycles};out.push({type:'legacy_project_metadata',id:p.id,hash:digest(projection),internalOnly:credentialLike(JSON.stringify(projection)),projection});}
 const s=operational(l);for(const k of ['projects','tasks','artifacts','interests','questions','commitments','relationships','assistance','responses'] as const)for(const x of s[k]){add('operational_'+k,x);if(k==='artifacts')for(const v of s.artifacts.find(a=>a.id===x.id)!.versions)add('artifact_version',v);}
 if(s.focus)add('focus',{id:'current-focus',...s.focus});
 return out.sort((a,b)=>(a.type+':'+a.id).localeCompare(b.type+':'+b.id));
}
/** Caller holds organism row lock during prepare/commit. Review writers acquire the same lock. Expiry evaluated at actual check time, never at an old event timestamp. */
export async function loadDisclosure(c:Pick<pg.PoolClient,'query'>,o:Organism,l:LifeStateV1,a:MemoryArchive):Promise<DisclosureSet>{
 const present=(await c.query("SELECT to_regclass('genesis_control_state') IS NOT NULL present")).rows[0].present;if(!present)return structuredClone(NO_DISCLOSURE);
 const state=(await c.query("SELECT review_revision,schema_version FROM genesis_control_state WHERE organism_id='genesis'")).rows[0];if(!state||state.schema_version!==1)throw Error('DISCLOSURE_SCHEMA_UNAVAILABLE');
 const rows=(await c.query("SELECT DISTINCT ON(source_type,source_id,audience) * FROM genesis_disclosure_reviews WHERE organism_id='genesis' ORDER BY source_type,source_id,audience,version DESC LIMIT 257")).rows;if(rows.length>256)throw Error('DISCLOSURE_REVIEW_BOUND_EXCEEDED');
 const sources=disclosureSources(o,l,a),now=Date.now();return {version:1,installed:true,revision:Number(state.review_revision),sources,reviews:rows.map(r=>{const source=sources.find(s=>s.id===r.source_id&&s.type===r.source_type),expiresAt=r.expires_at?new Date(r.expires_at).toISOString():null;return {id:r.id,version:r.version,type:r.source_type,sourceId:r.source_id,sourceHash:r.source_hash,audience:r.audience as Audience,effective:!source||source.hash!==r.source_hash?'STALE_SOURCE':expiresAt&&Date.parse(expiresAt)<=now?'EXPIRED':r.decision,expiresAt,hash:digest(JSON.parse(JSON.stringify(r)))};})};
}

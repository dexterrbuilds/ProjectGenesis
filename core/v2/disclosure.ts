/** Explicit review metadata only. No authentication, raw evidence, model call or public projection. */
import {digest} from './identity.ts';
import type {MemoryReview} from './memory.ts';
export const AUDIENCES=['INTERNAL_USE','PROVIDER_DISCLOSURE','PUBLIC_DISCLOSURE'] as const;
export type Audience=typeof AUDIENCES[number];
export type DisclosureSource={type:string;id:string;hash:string;internalOnly:boolean;projection?:{id:string;name:string;status:string;workCycles:number}};
export type ReviewBinding={id:string;version:number;type:string;sourceId:string;sourceHash:string;audience:Audience;effective:string;expiresAt:string|null;hash:string};
export type DisclosureSet={version:1;installed:boolean;revision:number;reviews:ReviewBinding[];sources:DisclosureSource[]};
export const NO_DISCLOSURE:DisclosureSet={version:1,installed:false,revision:0,reviews:[],sources:[]};
export function disclosureBinding(s:DisclosureSet){return {version:1,installed:s.installed,revision:s.revision,reviews:s.reviews,sourceHashes:s.sources.filter(x=>s.reviews.some(r=>r.sourceId===x.id&&r.type===x.type)).map(x=>({id:x.id,type:x.type,hash:x.hash})),policy:'disclosure-control-v1'};}
export function reviewFor(s:DisclosureSet,type:string,id:string,audience:Audience){return s.reviews.find(r=>r.type===type&&r.sourceId===id&&r.audience===audience);}
export function approved(s:DisclosureSet,type:string,id:string,audience:Audience){return reviewFor(s,type,id,audience)?.effective==='APPROVED';}
export function memoryReviews(s:DisclosureSet,organismId:string):MemoryReview[]{
 return s.sources.filter(x=>['legacy_memory','v2_episode','semantic_assertion'].includes(x.type)&&s.reviews.some(r=>r.type===x.type&&r.sourceId===x.id)).map(x=>({id:x.id,sourceHash:x.hash,organismId,reference:'durable-disclosure:'+digest(s.reviews.filter(r=>r.type===x.type&&r.sourceId===x.id)),internal:reviewFor(s,x.type,x.id,'INTERNAL_USE')?approved(s,x.type,x.id,'INTERNAL_USE'):x.type!=='legacy_memory',provider:!x.internalOnly&&approved(s,x.type,x.id,'PROVIDER_DISCLOSURE'),public:!x.internalOnly&&approved(s,x.type,x.id,'PUBLIC_DISCLOSURE'),operatorOnly:false}));
}
export function internalExclusions(s:DisclosureSet){return new Set(s.reviews.filter(r=>r.audience==='INTERNAL_USE'&&r.effective!=='APPROVED').map(r=>r.sourceId));}

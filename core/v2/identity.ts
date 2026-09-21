import { createHash } from 'node:crypto';
import type { Organism } from '../contracts.ts';
import type { LifeStateV1 } from './contracts.ts';
export function serializedDigest(value: unknown): string { return createHash('sha256').update(JSON.stringify(value)).digest('hex'); }
/** Stable payload identity across JSONB object-key reordering; arrays remain ordered. */
export function digest(value:unknown):string {
 const canonical=(x:unknown):unknown=>Array.isArray(x)?x.map(canonical):x!==null&&typeof x==='object'?Object.fromEntries(Object.entries(x).sort(([a],[b])=>a<b?-1:a>b?1:0).map(([k,v])=>[k,canonical(v)])):x;
 return serializedDigest(canonical(value));
}
export const CONSTITUTION = Object.freeze({ version: '1.0.0', principles: Object.freeze([
 'Continuity: preserve this organism identity and authentic history across downtime and upgrades.',
 'Learning and honesty: learn from evidence; preserve sources, uncertainty and the distinction between biology and interpretation.',
 'Useful contribution: seek useful work and positive real-world impact through evidence and human feedback.',
 'Sustainable existence: manage permitted resources for continued operation, not wealth maximization.',
 'Human agency and safety: respect consent, privacy, permissions and commitments; ask for assistance without bypassing limits.',
 'Freedom to reconsider: doing nothing, postponing, revising or abandoning a project are valid computational outcomes.',
 ]) });
export const CONSTITUTION_HASH = digest(CONSTITUTION);
export const CLOSED_PERMISSIONS = Object.freeze({execution:false as const,localArtifacts:false,llm:false,internet:false as const,communication:false as const,financial:false as const,maxCostMicros:0,maxAttempts:0});
export function initialLifeState(o:Organism, revision:number):LifeStateV1 {
 if(!o.id || !o.bornAt || !Number.isFinite(Date.parse(o.bornAt)) || !o.brain) throw new Error('Existing identity and saved brain required; never provision a replacement');
 return {schemaVersion:1,organismId:o.id,revision:0,baseRevision:revision,constitutionHash:CONSTITUTION_HASH,executionLock:'CLOSED',walletIdentity:{status:'unresolved',address:null,network:null,provenance:null},commitments:[],projectLife:[],interests:[],openQuestions:[],relationships:[],tasks:[],pendingDecisions:[],episodicRefs:[],semanticMemory:[],environment:[],rhythm:{legacy:structuredClone(o.rhythm??null),reviewAt:null,mode:'dormant'},biologicalContext:{snapshotHash:serializedDigest(o.brain),observationIds:[],mode:'SAVED-OBSERVATION-ONLY'},provenance:{reducer:'life-v1',administrative:true,source:'existing-organism'}};
}
export function bindExistingWallet(state:LifeStateV1, address:string, network:string, provenance:string, operatorReviewed:boolean):LifeStateV1 {
 if(!operatorReviewed || !provenance.trim() || !/^[1-9A-HJ-NP-Za-km-z]{32,44}$/.test(address) || !['devnet','mainnet-beta'].includes(network)) throw new Error('Authoritative reviewed wallet provenance required');
 if(state.walletIdentity.status==='bound' && (state.walletIdentity.address!==address || state.walletIdentity.network!==network)) throw new Error('Wallet rotation requires separate authorization');
 return {...structuredClone(state),walletIdentity:{status:'bound',address,network,provenance}};
}

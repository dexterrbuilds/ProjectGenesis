import type { BrainAdapter, PlannerAdapter, WorldEvent } from '../core/contracts.ts';
import { LifeStore } from '../server/store.ts';
import { LifeExtensionStore } from '../server/life-store-v1.ts';
import { SavedObservationAdapter } from '../core/v2/biology.ts';
import { CLOSED_PERMISSIONS } from '../core/v2/identity.ts';
import {readObservation} from '../server/observation-read.ts';
import {savedSnapshotReference} from '../server/saved-provenance.ts';
import { publicDecision, publicState } from '../core/v2/public.ts';
import data from '../data/connectome.json' with {type:'json'};
import { prepareCycle } from '../core/v2/cycle.ts';
import { ProductFallback } from '../core/v2/planner.ts';
import type { WalletObserver } from './wallet-observer.ts';
import type { RuntimeConfig } from './config.ts';
export class GenesisService {
 readonly store:LifeStore;readonly config:RuntimeConfig;readonly walletObserver?:WalletObserver;readonly extension:LifeExtensionStore;
 // Legacy constructor arguments retained for compatibility, never invoked.
 constructor(store:LifeStore,config:RuntimeConfig,_brainFactory?:()=>BrainAdapter,_planner?:PlannerAdapter,walletObserver?:WalletObserver,_brainLabel?:string){this.store=store;this.config=config;this.walletObserver=walletObserver;void _brainLabel;this.extension=new LifeExtensionStore(store.connection());}
 async advance(id:string,event?:WorldEvent,automatic=false){
  await this.extension.assertExecutionAllowed(); // always refuses in this dormant release, before any other work
  void automatic;
  const {organism}=await this.store.read();const life=await this.extension.read();
  const brain=new SavedObservationAdapter(organism.id);const snapshot=await savedSnapshotReference(this.store.connection(),organism.brain);if(snapshot)brain.restore(snapshot);
  const at=new Date().toISOString();
  const result=await prepareCycle(organism,life,brain,new ProductFallback(),{id:event?.id??id+':event',kind:'digital-event',source:'runtime-world-observation',observedAt:at},CLOSED_PERMISSIONS,at,id);
  await this.extension.commitPrepared(life.revision,result.life,result.decision);
  return {decision:result.decision,replayed:false};
 }
 async observe(_canOperate:boolean){
  void _canOperate;
  const {organism,life,history,facts,snapshot,schedule}=await readObservation(this.store.connection());
  const adapter=new SavedObservationAdapter(organism.id);if(snapshot)adapter.restore(snapshot);
  const saved=adapter.observe();
  return {...publicState(organism,life,facts),history:history.map(publicDecision),schedule:{enabled:schedule.enabled},biological:{mode:adapter.describe().mode,status:saved.status,sourceRecordedAt:saved.sourceRecordedAt,sourceDecisionId:saved.sourceDecisionId,observedAt:saved.observedAt,modelClock:saved.modelClock,limitations:saved.limitations,availableCapabilities:[]}};
 }

 async history(id?:string){if(id){const d=await this.store.decision(id);return {decision:d?publicDecision(d):null};}return {decisions:(await this.store.history()).map(publicDecision)};}
 async replay(id:string){const d=await this.store.decision(id);if(!d || ('schemaVersion' in d && d.schemaVersion===2))return null;return {id:d.id,at:d.at,modelId:d.brainAfter.adapter,frames:d.frames.map(f=>({tick:f.tick,activity:[...f.activity],stimulated:[...f.stimulated]})),status:'SAVED HISTORICAL REPLAY',interpretation:'Dimensionless saved model activity; not a response to current events.'};}
 graph(){return {id:'celegans-cook2019-rate-v1',label:'C. elegans — saved model',nodes:data.neurons,edges:data.edges};}
}

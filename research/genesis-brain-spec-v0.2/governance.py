"""Governance validation only; intentionally no neural or Genesis runtime imports."""
from common import *
import sys
sys.path.insert(0,str(BASE))
from policy import check_revision
from validate import require,inspect_fields,validate_experiment

def registry():
 p=load(HERE/'REGISTRY_POINTER.json');require(sha(HERE/p['path'])==p['sha256'],'Registry bytes changed');return load(HERE/p['path'])
def check_registry(candidate,reviews):
 base=load(BASE/'objects'/f'{BASE_SHA}.json')
 check_revision(base,candidate,reviews)
 expected=load(HERE/'APPEND_ONLY_DIFF.json')['added_entries']
 added={e['id']:digest(e) for e in candidate['entries'] if e['id'] not in base['entry_hashes']}
 require(added==expected,'Unreviewed claim/category/classification change')
 require(candidate['version']=='0.2.0','Wrong successor version')
 return True
def check_capabilities(c):
 base=load(BASE/'objects'/f'{BASE_SHA}.json');old={e['id']:e for e in base['entries'] if e['kind']=='capability'}
 rows={e['id']:e for e in c['capabilities']};require(len(rows)==len(c['capabilities']),'Duplicate capability')
 require(set(rows)==set(old)|{'capability.avoidance','capability.escape','capability.visual_perception','capability.looming_detection_in_Genesis'},'Unreviewed capability')
 for cid,e in old.items():require(rows[cid]['status']==e['status'] and rows[cid]['inherited_entry_sha256']==digest(e),'Historical capability promotion')
 for cid in set(rows)-set(old):require(rows[cid]['status']=='unsupported','New semantic capability promotion')
 require({cid for cid,e in rows.items() if e['validated_biological_model_capability']}=={'capability.associative_appetitive_learning'},'Unsupported biological-model capability')
 require(c['action_selection']=='not_validated','Action selection promoted')
def check_identity(i):
 base=load(BASE/'objects'/f'{BASE_SHA}.json')
 require(i['ownership']=='reference_only' and i['new_rows_owned']==0,'Duplicate canonical anatomy ownership')
 require(i['identity']==base['identity'] and i['neurons_artifact']==base['neurons_artifact'],'Identity was rewritten')
 require(i['shared_counts']=={'KC_MBON07':4622,'KC_MBON11':1053},'Shared rows changed')
 require(i['physiology_composition']=='blocked_unresolved_rules','Conflicting shared rules combined')
def check_sensory(s):
 require(s['category']=='ENGINEERING ASSUMPTION' and not s['implemented'] and not s['runtime_authorized'],'Concept promoted to physiology/runtime')
 required=['observation_type','units','time','preparation','support_domain','provenance','uncertainty','identity_resolution','ood_status','representation_scope']
 require(s['required_fields']==required,'Missing observation-aware metadata')
 require(s['support_labels']==['DIRECTLY MEASURED','INTERPOLATION-SUPPORTED','WEAKLY SUPPORTED','OUT OF DISTRIBUTION / UNKNOWN'],'Support semantics changed')
 e=s['empirical_instance'];require(e['package_content_sha256']==PACKAGES['empirical'][1],'Wrong empirical dependency')
 require(e['units']=='mV' and e['observation_type']=='mean_baseline_subtracted_somatic_voltage' and e['time']=={'start_ms':0,'end_ms':500,'grid_ms':1,'original_resolution_preserved_in_provenance':True},'Unsupported observation conversion/horizon')
 require(set(e['conversions'])=={'calcium','spikes','release','synaptic_current','model_rate'},'Observation restrictions missing')
 for value in e['conversions'].values():require(value['state']=='unknown' and value['value'] is None and bool(value['reason']),'Unknown conversion silently known/zero')
 require(all(e['identity_resolution'][k] is None for k in ['fly','subtype','column','root']),'Unsupported identity transfer')
 require(e['Stage4_conditions_ood']==16 and not e['omitted_circuits_simulated'],'OOD/circuit reconstruction promotion')
 require(s['unknown_policy']=={'quantity':None,'physiology':None,'uncertainty':None,'never_substitute_zero':True,'UNKNOWN_status_overrides_support_annotation':True},'Unknown substituted or weakened')
def check_future_dependencies(m,r):
 """Check declarations only; never run the proposed experiment."""
 require(m['registry_sha256']==digest(r),'Wrong release dependency')
 require(bool(m['dependencies']),'Evidence dependencies required')
 entries={e['id']:e for e in r['entries']}
 for cid,h in m['dependencies'].items():require(cid in entries and digest(entries[cid])==h,'Missing/stale evidence dependency')
 require(not m.get('evidence_overrides') and not m.get('capability_promotions'),'Silent override/promotion')
 require(m.get('result_claims',[])==[],'Results need separate admission')
 owners={}
 for row in m.get('state_ownership',[]):
  key=(row['canonical_row_id'],row['model_instance'])
  require(key not in owners,'Duplicate canonical row physiology ownership');owners[key]=row['owner']
 for channel in m.get('input_channels',[]):
  require(channel['layer']=='biological' and channel['category']!='GENESIS PRODUCT MAPPING','Product-to-biology input leakage')
  require(channel['units'] not in ['USD','profit','business_value'],'Economic quantity in biology')
  require(all(entries[cid]['layer']=='biological' for cid in channel['evidence_refs']),'Product evidence supports biological input')
 return True

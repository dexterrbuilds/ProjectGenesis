"""Static protocol/governance validation ONLY.

Never imports prospective_analysis, opens Stage1 summary values, or evaluates a
transfer. Cryptographic streaming of immutable files is not outcome inspection.
"""
from pathlib import Path
import json,hashlib,ast,unittest,copy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def load(name):return json.loads((HERE/name).read_text())
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  while b:=f.read(4194304):h.update(b)
 return h.hexdigest()

def guard(prereg,families,assumptions,estimands,resolution,authorization,provenance,firewall):
 assert prereg['design_authorized'] is True and prereg['execution_authorized'] is False
 assert prereg['outcome_values'] is None and prereg['new_training'] is False and prereg['normalization']=='none'
 assert prereg['planned_run_count']==28
 assert set(prereg['family_ids'])=={'E','Z','P','R','WP','WR','H','U','N'}
 assert families['selected_family'] is None and families['physical_output_units'] is None
 assert families['biological_parameter_estimates']=={} and families['engineering_numerical_sweep'] is None
 fs={f['id']:f for f in families['families']};assert set(fs)==set(prereg['family_ids'])
 assert fs['N']['nuisance']=='unrestricted' and fs['H']['operator']=='heterogeneous'
 assert fs['P']['operator']=='increasing' and fs['R']['operator']=='decreasing' and fs['Z']['operator']=='zero'
 assert set(k for k in assumptions if k.isupper())=={'EVIDENCE-ADMISSIBLE FAMILY','RESTRICTED CONDITIONAL FAMILY','ENGINEERING SENSITIVITY RANGE'}
 assert assumptions['no_post_execution_pruning'] is True
 assert estimands['normalization'].startswith('none') and estimands['no_pooled_crosscue_rank'] is True
 assert resolution['root_assignment'] is None and resolution['driver_membership_assignment'] is None
 assert resolution['observation_conversions']==[] and resolution['biological_transfer_established'] is False
 assert authorization['authorization_granted'] is False and authorization['reviewer_decision'] is None
 assert provenance['engineering_grid'] is None and provenance['physiological_confidence_interval'] is None
 for p in provenance['parameters']:
  if p['name'] in ['gain','responder mass q','saturation/plateau','nuisance difference','latency/kernel','physical observation conversion']:assert p['value'] is None
 assert firewall['execution_authorized'] is False and firewall['neural_model_execution'] is False and firewall['biological_parameter_fit'] is False

class Design(unittest.TestCase):
 def args(self):return [load(p) for p in ['PREREGISTRATION.json','TRANSFER_FAMILIES.json','ASSUMPTION_PARTITIONS.json','ESTIMANDS.json','POPULATION_RESOLUTION.json','EXECUTION_AUTHORIZATION_CHECKLIST.json','PARAMETER_PROVENANCE.json','BLINDING_FIREWALL.json']]
 def test_01_preservation(self):
  p=load('PRESERVATION_MANIFEST.json');self.assertEqual(p['count'],9170)
  for path,h in p['files'].items():self.assertEqual(sha(ROOT/path),h,path)
 def test_02_dependencies(self):
  d=load('DEPENDENCIES.json');self.assertEqual(len(d['packages']),5);self.assertFalse(d['execution_authorized'])
  for name,p in d['packages'].items():
   folder=ROOT/'research'/name
   if 'release_sha256' in p:self.assertEqual(sha(folder/'RELEASE.json'),p['release_sha256'])
   if 'content_sha256' in p:
    r=json.loads((folder/'RELEASE.json').read_text());self.assertEqual(r['content_sha256'],p['content_sha256'])
    self.assertEqual(hashlib.sha256(json.dumps(r['files'],sort_keys=True,separators=(',',':')).encode()).hexdigest(),p['content_sha256'])
   if name=='genesis-brain-spec-v0.2':self.assertEqual(sha(folder/'objects'/f"{p['registry_sha256']}.json"),p['registry_sha256'])
   if name=='fly-stage1':self.assertEqual(sha(ROOT/p['evidence_manifest_path']),p['evidence_manifest_sha256'])
 def test_03_source_lock_without_value_reads(self):
  d=load('STAGE1_INPUT_LOCK.json');self.assertEqual(len(d['inputs']),28);self.assertFalse(d['neural_rerun_allowed'])
  self.assertEqual(len({r['run'] for r in d['inputs']}),28)
  count=0
  for r in d['inputs']:
   self.assertFalse(r['numeric_values_inspected_for_design']);self.assertEqual(r['cues'],['A','B'])
   for name,a in r['artifacts'].items():
    self.assertEqual(sha(ROOT/a['path']),a['sha256'])
    if name in ('initial.json.gz','trained.json.gz'):count+=1
  self.assertEqual(count,56)
 def test_04_canonical(self):
  a=load('CANONICAL_AFTER.json');b=load('CANONICAL_BEFORE.json');self.assertEqual(a,b)
  self.assertEqual(a['sha256'],'3377c9dddbe2abf89ed9a820a6aabbc1da951cac7bfc1823471c5aac043ea312')
  self.assertEqual(a['tableRowCounts']['genesis_decisions'],7);self.assertFalse(a['schedule'][0]['enabled'])
 def test_05_guard(self):guard(*self.args())
 def test_06_reject_branch_deletion(self):
  for name in ['Z','R','H','N']:
   a=self.args();a[1]['families']=[f for f in a[1]['families'] if f['id']!=name]
   with self.assertRaises(AssertionError):guard(*a)
 def test_07_reject_best_branch_selection(self):
  a=self.args();a[1]['selected_family']='R'
  with self.assertRaises(AssertionError):guard(*a)
 def test_08_reject_physical_or_root_mapping(self):
  for i,k,v in [(1,'physical_output_units','mV'),(4,'root_assignment','720575940608236978'),(4,'driver_membership_assignment','R64A11=SS67249'),(4,'observation_conversions',['rate_to_mV'])]:
   a=self.args();a[i][k]=v
   with self.assertRaises(AssertionError):guard(*a)
 def test_09_reject_parameter_promotion(self):
  for name,value in [('gain',1),('latency/kernel',.05),('responder mass q',4/17),('physical observation conversion',0)]:
   a=self.args();next(p for p in a[6]['parameters'] if p['name']==name)['value']=value
   with self.assertRaises(AssertionError):guard(*a)
 def test_10_reject_unblinding_execution(self):
  for i,k,v in [(0,'execution_authorized',True),(0,'outcome_values',{}),(5,'authorization_granted',True),(7,'neural_model_execution',True)]:
   a=self.args();a[i][k]=v
   with self.assertRaises(AssertionError):guard(*a)
 def test_11_reject_grid_as_bound(self):
  a=self.args();a[6]['physiological_confidence_interval']=[0,1]
  with self.assertRaises(AssertionError):guard(*a)
 def test_12_controls(self):
  c=load('CONTROL_MATRIX.json');ids={x['id'] for x in c['controls']}
  self.assertEqual(ids,{'intact','freeze','silence_dan','remove_da_contacts','single_dan','matched_dan','remove_pn_kc','remove_kc_mbon','no_apl','no_recurrence','shuffle_pn_weights','unpaired'})
  self.assertEqual(len(load('ESTIMANDS.json')['contrasts']),4)
 def test_13_compatibility_preserved(self):
  m=load('OBSERVATION_COMPATIBILITY.json');self.assertEqual(sha(ROOT/m['source']),m['source_sha256'])
  self.assertEqual(m['matrix'],json.loads((ROOT/m['source']).read_text()))
 def test_14_ast_only_no_analysis_import(self):
  source=(HERE/'prospective_analysis.py').read_text();tree=ast.parse(source)
  imports=[]
  for n in ast.walk(tree):
   if isinstance(n,ast.Import):imports.extend(x.name for x in n.names)
   if isinstance(n,ast.ImportFrom):imports.append(n.module)
  self.assertEqual(set(imports),{'pathlib','decimal','json','hashlib','argparse'})
  fn={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
  self.assertIn('require_authorization',fn);self.assertIn('execute_authorized',fn)
  first=fn['execute_authorized'].body[0]
  self.assertIsInstance(first,ast.Assign);self.assertEqual(first.value.func.id,'require_authorization')
  self.assertIn('research/fly-stage5-runs',source)
  for bad in ['exec','eval','__import__']:
   self.assertFalse(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id==bad for n in ast.walk(tree)))
 def test_15_result_semantics(self):
  r=load('RESULT_CLASSIFICATION.json');self.assertTrue(r['multi_label']);self.assertIsNone(r['execution_result'])
  self.assertEqual(set(r['labels']),{'ROBUST ACROSS DECLARED EVIDENCE-ADMISSIBLE FAMILY','ROBUST ONLY UNDER RESTRICTED CONDITIONAL FAMILY','TRANSFER-SENSITIVE / NON-ROBUST','NULL-COMPATIBLE','UNINTERPRETABLE'})
 def test_16_required_artifacts_and_no_results(self):
  required=['STAGE5_PROTOCOL.md','DEPENDENCIES.json','PREREGISTRATION.json','TRANSFER_FAMILIES.json','ASSUMPTION_PARTITIONS.json','ESTIMANDS.json','POPULATION_RESOLUTION.json','OBSERVATION_COMPATIBILITY.json','CONTROL_MATRIX.json','COUNTEREXAMPLE_REGISTRY.json','ROBUSTNESS_DEFINITIONS.json','PARAMETER_PROVENANCE.json','BLINDING_FIREWALL.json','RESULT_CLASSIFICATION.json','PRESERVATION_MANIFEST.json','EXECUTION_AUTHORIZATION_CHECKLIST.json','prospective_analysis.py']
  self.assertTrue(all((HERE/p).exists() for p in required))
  self.assertFalse((HERE/'RESULTS.json').exists());self.assertFalse((HERE/'__pycache__/prospective_analysis.cpython-39.pyc').exists())
 def test_17_release_if_sealed(self):
  if not (HERE/'RELEASE.json').exists():return
  r=load('RELEASE.json')
  for p,h in r['files'].items():self.assertEqual(sha(HERE/p),h,p)
  self.assertEqual(hashlib.sha256(json.dumps(r['files'],sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest(),r['content_sha256'])

if __name__=='__main__':unittest.main(verbosity=2)

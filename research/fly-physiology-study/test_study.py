"""Integrity, data separation and identifiability checks; no generated biology."""
import ast,hashlib,json,unittest
from pathlib import Path
import numpy as np
H=Path(__file__).resolve().parent;ROOT=H.parent.parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def read(n):return json.loads((H/n).read_text())

class StudyTests(unittest.TestCase):
 def test_all_previous_work_unchanged(self):
  for p,d in read('FROZEN_BEFORE.json').items():self.assertEqual(sha(ROOT/p),d,p)
  for p,d in read('RESUMED_HASHES.json').items():self.assertEqual(sha(H/p),d,p)
 def test_frozen_fit_and_transfer_sources(self):
  for f in ['CALIBRATION_FROZEN.json','IDENTIFICATION_FROZEN.json']:
   for p,d in read(f)['source_hashes'].items():self.assertEqual(sha(H/p),d,p)
  for p,d in read('TRANSFER_FROZEN.json')['frozen_inputs'].items():self.assertEqual(sha(H/p),d,p)
  self.assertFalse(read('TRANSFER_FROZEN.json')['calibrated_neural_kernel_exported'])
  self.assertEqual(read('TRANSFER_FROZEN.json')['stage_parameter_changes'],{})
 def test_train_validation_separation(self):
  a=read('data/apl-train.json');b=read('data/apl-validation.json')
  self.assertEqual(len(a),6);self.assertEqual(len(b),5)
  self.assertFalse({r['source_row'] for r in a}&{r['source_row'] for r in b})
  self.assertEqual({r['source_row'] for r in a+b},set(range(4,15)))
  src=ast.parse((H/'calibrate.py').read_text())
  train=next(x for x in src.body if isinstance(x,ast.FunctionDef) and x.name=='train')
  self.assertNotIn('validation.json',ast.unparse(train))
  for file in ['calibrate.py','identify.py']:
   tree=ast.parse((H/file).read_text());imports=[]
   for n in ast.walk(tree):
    if isinstance(n,ast.Import):imports.extend(a.name for a in n.names)
    elif isinstance(n,ast.ImportFrom):imports.append(n.module)
   self.assertFalse(set(imports)&{'model','experiment','evaluate','replay'})
 def test_held_out_metrics_are_from_saved_predictions(self):
  v=read('VALIDATION.json');y=np.asarray(v['observed'])
  self.assertEqual(v['calibration_sha256'],sha(H/'CALIBRATION_FROZEN.json'))
  for name,z in v['predictions'].items():self.assertAlmostEqual(float(np.mean((y-np.asarray(z))**2)),v['mse'][name],places=13)
  self.assertFalse(v['fit_updated']);self.assertFalse(v['neural_validation'])
 def test_identifiability_equivalence(self):
  v=read('IDENTIFICATION_FROZEN.json')
  for p in v['equivalence_profile']:
   self.assertAlmostEqual(np.exp(-p['eta']*p['unmeasured_exposure']),v['target_remaining'],places=14)
  self.assertEqual(v['joint_parameter_jacobian_rank'],1)
  self.assertIsNone(v['integrated_depression_approx_t95'][1])
  self.assertEqual(v['neural_parameters_identified'],[])
 def test_crosswalk_strings_and_parameter_coverage(self):
  c=read('CROSSWALK.json');self.assertEqual(len(c['rows']),37)
  for r in c['rows']:self.assertIs(type(r['root_id']),str)
  rows=read('PARAMETER_EVIDENCE.json');statuses={'experimentally constrained','weakly constrained','unconstrained','product-boundary assumption'}
  self.assertTrue(all(r['status'] in statuses for r in rows))
  for s,params in read('PARAMETER_INVENTORY.json').items():
   actual={r['name']:r['value'] for r in rows if r['stage']==int(s)}
   self.assertEqual(actual,params)
 def test_replay_comparison(self):
  c=read('REPLAY_COMPARISON.json');self.assertEqual(len(c['runs']),8)
  self.assertTrue(all(x['trained_state_exact'] and x['replay_exact'] and x['restoration_exact'] for x in c['runs']))
  self.assertFalse(c['calibrated_capability_inference_available'])
  for p in (H/'replays').glob('*/files.json'):
   for f,d in json.loads(p.read_text()).items():self.assertEqual(sha(p.parent/f),d)
 def test_canonical_read_only_audit(self):
  a=read('CANONICAL_BEFORE.json');b=read('CANONICAL_AFTER.json');self.assertEqual(a,b)
  self.assertEqual(b['tableRowCounts']['genesis_decisions'],7)
  self.assertFalse(b['schedule'][0]['enabled'])
if __name__=='__main__':unittest.main()

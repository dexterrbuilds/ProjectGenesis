"""Study validation and preservation only. No old neural experiments or life cycles."""
from common import *
import unittest,copy,csv,collections,subprocess
ROOT=HERE.parent.parent

def admissible_spec(x):
 if x['classification']!='PARTIAL VISUAL BOUNDARY CONSTRAINT':raise ValueError('No general boundary is supported by these completed results')
 for k in ['deployable_boundary','model_family_selected_for_general_T4T5','biological_parameters_frozen_for_transfer','anatomical_screen_transform','calcium_or_spike_observation_mapping']:
  if x[k] is not None:raise ValueError('Unsupported promotion of '+k)
 if x['stage4_evaluations'] or x['LPLC2_runs'] or x['product_mappings']:raise ValueError('Forbidden integration/evaluation')
class Checks(unittest.TestCase):
 def test_protocol_locks(self):
  for reg,file,key in [('REGISTRATION.json','PLAN.md','plan_sha256'),('CONDITIONAL_REGISTRATION.json','CONDITIONAL_PROTOCOL.md','protocol_sha256'),('TIMING_REGISTRATION.json','TIMING_AUDIT.md','sha256'),('POLARITY_REGISTRATION.json','POLARITY_PROTOCOL.md','sha256')]:
   d=json.loads((HERE/reg).read_text());self.assertEqual(sha(HERE/file),d[key])
 def test_spec_dependency(self):
  r=json.loads((ROOT/'research/genesis-brain-spec-v0.1/RELEASE.json').read_text());h='6b3a27ea3c41a87e701ca8a7eec7fd31d5e41469db7da27916b81cb040eb923e';self.assertEqual(r['registry']['sha256'],h);self.assertEqual(sha(ROOT/'research/genesis-brain-spec-v0.1'/r['registry']['path']),h)
 def test_completed_results_frozen(self):
  for p,h in json.loads((HERE/'PRIMARY_RESULT_LOCK.json').read_text()).items():self.assertEqual(sha(HERE/p),h,p)
 def test_provenance(self):
  a=json.loads((HERE/'metadata/compact-acquisition.json').read_text());tree={x['path']:x['sha'] for x in json.loads((HERE/'metadata/t5-model-tree.json').read_text())['tree']}
  for f in a['files']:
   self.assertEqual(sha(HERE/f['file']),f['sha256']);self.assertEqual(f['git_blob'],tree[Path(f['file']).name])
  for f in json.loads((HERE/'PARTITIONS.json').read_text())['entries']:self.assertEqual(sha(HERE/f['path']),f['sha256'])
 def test_access_log(self):
  for p in json.loads((HERE/'FIT_ACCESS.json').read_text()):
   self.assertTrue(p.endswith('_train.npz') or p in ['models.py','FITS.json','CONDITIONAL_PROTOCOL.md'],p)
  self.assertFalse(json.loads((HERE/'FIT_FREEZE.json').read_text())['test_outcomes_used'])
 def test_firewall_adversarial(self):
  targets=[ROOT/'outputs/fly-stage4/anything.json',ROOT/'core/planner.ts',HERE/'processed/cell_01_test.npz',HERE/'RESULTS.json',HERE/'T4_POLARITY_MEASUREMENTS.json']
  for target in targets:
   cmd='from common import firewall;firewall("fit");open('+repr(str(target))+')';r=subprocess.run([sys.executable,'-c',cmd],cwd=HERE,capture_output=True,text=True);self.assertIn('PermissionError',r.stderr)
 def test_no_unknown_gain_promotion(self):
  d=json.loads((HERE/'BASELINE_IDENTIFIABILITY.json').read_text());self.assertIsNone(d['biological_gain'])
  for f in json.loads((HERE/'FITS.json').read_text())['fits']:self.assertEqual(f['candidate_fits']['B0']['rank'],0)
 def test_identity_crosswalk(self):
  rr=list(csv.DictReader((HERE/'ROOT_COLUMN_CROSSWALK.csv').open()));self.assertEqual(len(rr),11822);self.assertEqual(len(set(r['root_id'] for r in rr)),len(rr));self.assertTrue(all(len(r['root_id'])==18 and r['root_id'].isdigit() for r in rr));self.assertEqual(sum(r['type_match']=='False' for r in rr),11);self.assertTrue(all(r['retinal_direction']=='' for r in rr))
 def test_not_general_validation(self):
  admissible_spec(json.loads((HERE/'VISUAL_BOUNDARY_SPEC.json').read_text()));self.assertFalse(json.loads((HERE/'PARTITIONS.json').read_text())['fly_held_out_possible'])
 def test_adversarial_promotions(self):
  spec=json.loads((HERE/'VISUAL_BOUNDARY_SPEC.json').read_text())
  for key,value in [('classification','VALIDATED T4/T5 BOUNDARY IDENTIFIED'),('biological_parameters_frozen_for_transfer',{}),('anatomical_screen_transform',0),('stage4_evaluations',1),('product_mappings',['avoid'])]:
   bad=copy.deepcopy(spec);bad[key]=value
   with self.assertRaises(ValueError):admissible_spec(bad)
 def test_fresh_reproduction(self):
  r=json.loads((HERE/'REPRODUCTION.json').read_text());self.assertTrue(r['fresh_process_fit_exact']);self.assertLessEqual(r['max_prediction_absolute_difference_mV'],r['tolerance_mV'])
 def test_canonical(self):
  before=json.loads((HERE/'CANONICAL_BEFORE.json').read_text());after=json.loads((HERE/'CANONICAL_AFTER.json').read_text());self.assertEqual(before,after);self.assertEqual(after['tableRowCounts']['genesis_decisions'],7);self.assertTrue(all(not s['enabled'] for s in after['schedule']))
 def test_preservation(self):
  protected=json.loads((HERE/'FROZEN_BEFORE.json').read_text());bad=[p for p,h in protected.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h];self.assertEqual(bad,[])
  write('PRESERVATION.json',{'files_checked':len(protected),'changed':bad,'canonical_sha256':json.loads((HERE/'CANONICAL_AFTER.json').read_text())['sha256'],'canonical_life_cycles':7,'new_life_cycles':0,'schedule_enabled':False,'stage4_reruns':0,'LPLC2_runs':0,'Brain_Spec_modified':False})
 def test_polarity_sources_and_missingness(self):
  counts={'T4':2260,'T5':2204}
  for typ,n in counts.items():
   d=json.loads((HERE/f'{typ}_POLARITY_MEASUREMENTS.json').read_text());self.assertEqual(len(d['rows']),n);self.assertEqual(d['source_member_sha256'],sha(HERE/f'data/wholecell/singleBarSt{typ}.mat'))
   self.assertTrue(all(r['fly_id'] is None for r in d['rows']))
   if typ=='T5':self.assertTrue(all(r['num_repeats_source'] is None for r in d['rows']))
  self.assertTrue(json.loads((HERE/'ACQUISITION_COMPLETE.json').read_text())['whole_archive_verified'])
  self.assertTrue(json.loads((HERE/'EXCLUSIONS.json').read_text())['T4_cell_5']['source_result_MATLAB_empty'])
 def test_package(self):
  p=HERE/'PACKAGE_MANIFEST.json'
  if not p.exists():return
  manifest=json.loads(p.read_text())
  for f,h in manifest['files'].items():self.assertEqual(sha(HERE/f),h,f)
  digest=hashlib.sha256(json.dumps({'files':manifest['files'],'large_sources':manifest['large_sources']},sort_keys=True,separators=(',',':')).encode()).hexdigest();self.assertEqual(digest,manifest['content_sha256'])
  for f,info in manifest['large_sources'].items():self.assertEqual((HERE/f).stat().st_size,info['bytes']);self.assertEqual(sha(HERE/f),info['sha256'])
if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Checks));write('VALIDATION.json',{'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'passed':result.wasSuccessful(),'scope':'scientific/identity/firewall/preservation checks, not a biological success criterion'});raise SystemExit(0 if result.wasSuccessful() else 1)

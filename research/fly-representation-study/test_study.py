"""Scientific provenance, numerical-result and identity regression checks."""
import gzip,hashlib,json,unittest
from pathlib import Path
import numpy as np
from identity import neuron_key,insert
H=Path(__file__).resolve().parent;P=H.parent/'fly-physiology-study'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class StudyTests(unittest.TestCase):
 def test_frozen_fit_sources(self):
  f=load(H/'FIT_FROZEN.json')
  for p,d in f['source_hashes'].items():self.assertEqual(sha(H/p),d,p)
  self.assertEqual(load(H/'VALIDATION.json')['fit_sha256'],sha(H/'FIT_FROZEN.json'))
 def test_interrupted_artifacts_preserved(self):
  for p,d in load(H/'RESUMED_HASHES.json').items():self.assertEqual(sha(H/p),d,p)
 def test_reused_validation_independent_arithmetic(self):
  a=np.array([r['values'] for r in load(P/'data/apl-validation.json')]);f=load(H/'FIT_FROZEN.json');v=load(H/'VALIDATION.json')
  for k,d in f['apl'].items():
   error=float(np.mean((a[:,[1,2]]-a[:,[0,3]]*d['q'])**2))
   self.assertAlmostEqual(error,v['reused_apl_validation'][k]['mse'],places=12)
 def test_no_positive_coupling_claim(self):
  f=load(H/'FIT_FROZEN.json')['apl'];v=load(H/'VALIDATION.json')['reused_apl_validation']
  self.assertEqual(f['R1_shared']['bootstrap_95pct'][0][0],0)
  self.assertLess(f['R1_zero']['train_aicc'],f['R1_shared']['train_aicc'])
  self.assertLess(1-v['R1_directional']['mse']/v['R1_zero']['mse'],.20)
 def test_MBON_source_flag_cannot_be_clean_validation(self):
  d=load(H/'data/challenges.json');r=load(H/'VALIDATION.json')['mbon14']
  mean=np.mean([x['tau_ms'] for x in d['mbon14']])
  self.assertAlmostEqual(mean,16.9825);self.assertGreater(abs(mean-d['mbon14_reported_mean']['tau_ms']),2.)
  self.assertFalse(r['independent_validation_qualified']);self.assertFalse(r['representation_discrimination'])
 def test_identity_strings_and_conflict(self):
  with self.assertRaises(ValueError):neuron_key(720575940605891040)
  e={'source':'720575940605891040','target':'720575940608186498','neuropil':'MB_VL_L','synapses':3};registry={}
  a=insert(registry,e,1);b=insert(registry,e,3);self.assertEqual(a,b);self.assertEqual(len(registry),1)
  with self.assertRaises(ValueError):insert(registry,{**e,'synapses':4},2)
 def test_real_shared_rows_unique_and_unassigned(self):
  audit=load(H/'IDENTITY_AUDIT.json');shared=load(H/'shared-row-ids.json');seen=set();found=set()
  wanted=set(shared['KC_MBON07']+shared['KC_MBON11'])
  with gzip.open(H/'identity-registry.jsonl.gz','rt') as f:
   for line in f:
    r=json.loads(line);self.assertNotIn(r['id'],seen);seen.add(r['id']);self.assertIsNone(r['physiology_rule'])
    if r['id'] in wanted:self.assertIn(1,r['preparations']);self.assertIn(3,r['preparations']);found.add(r['id'])
  self.assertEqual(len(seen),audit['unique_aggregate_rows']);self.assertEqual(found,wanted)
  self.assertEqual(len(shared['KC_MBON07']),4622);self.assertEqual(len(shared['KC_MBON11']),1053)
 def test_benchmark_preserves_contacts_and_all_updates(self):
  for context in ['s1','s2','s3','integrated','full']:
   rows=[load(H/'benchmarks'/f'{context}-{r}'/'result.json') for r in ['R0','R1','R2']]
   self.assertEqual(len({r['contacts'] for r in rows}),1);self.assertEqual(len({r['anatomical_rows'] for r in rows}),1)
   for r in rows:self.assertTrue(r['replay_exact']);self.assertTrue(r['all_finite']);self.assertEqual(r['updates'],100);self.assertFalse(r['biological_model'])
  self.assertEqual(rows[0]['roots'],139255);self.assertEqual(rows[0]['contacts'],54492922)
 def test_original_APL_remains_same(self):
  old=load(P/'CALIBRATION_FROZEN.json');new=load(H/'FIT_FROZEN.json')
  self.assertEqual(old['local_transfer'],new['apl']['R1_directional']['q'])
  self.assertEqual(load(P/'VALIDATION.json')['mse']['local'],load(H/'VALIDATION.json')['reused_apl_validation']['R1_directional']['mse'])
 def test_no_kernel_or_replay_from_unidentified_fit(self):
  a=load(H/'TEMPORAL_CONDITIONING.json');self.assertFalse(a['kernel_exported']);self.assertEqual(a['new_stage_replays'],0)
  self.assertEqual(load(H/'FIT_FROZEN.json')['calibrated_neural_parameters'],{})
if __name__=='__main__':unittest.main()

"""Read-only evidence/preservation tests; no models, fitting, or database imports."""
from common import *
import unittest,copy,zipfile,zlib,re

def guard(identity,transmission,mediation,readiness,crosswalk):
 for c in identity['four_responders']:
  assert c['mapping_classification']=='UNRESOLVED'
  assert all(c[k] is None for k in ['identified_cell_type','identified_FlyWire_root','recording_to_morphology_link'])
 for c in identity['recall_records']:
  assert all(c[k] is None for k in ['root','cell_type','morphology_link','fly_id','external_recording_id'])
 assert not identity['individuals_inferred_from_row_order']
 for c in transmission['target_specific']:
  assert all(c[k] is None for k in ['receptor','sign','paired_recording','localization','identified_target_perturbation'])
 assert not transmission['inhibitory_synaptic_current_measured']
 assert transmission['independent_replications_added']==0
 assert not mediation['numerical_composition']
 links={x['id']:x for x in mediation['links']}
 assert links['complete-mediated-chain']['classification']=='UNRESOLVED'
 assert links['chronic-blockade']['classification']=='PARTIAL'
 assert links['acute-blockade-upwind']['classification']=='CONTRADICTED'
 assert readiness['stage5_authorized'] is False and readiness['stage5_protocol'] is None
 assert readiness['neural_runs']==0 and readiness['canonical_writes']==0
 assert readiness['fitted_parameters']==[] and readiness['decoder'] is None and readiness['capability_promotions']==[]
 assert readiness['root_identity_is_not_universal_prerequisite'] is True
 assert readiness['complete_prior_mediation_proof_is_not_prerequisite'] is True
 assert readiness['classification']=='PARTIAL ROUTE SUPPORT — TARGETED EVIDENCE STILL REQUIRED'
 assert crosswalk['anatomy_ownership']==[] and crosswalk['roots_are_references_only']
 for m in crosswalk['mappings']:
  assert m['classification'] in ['IDENTIFIED','TYPE-COMPATIBLE','POSSIBLE','UNRESOLVED']
  assert m['evidence'] and m['scope']

class Audit(unittest.TestCase):
 def args(self):return [load(HERE/p) for p in ['SOURCE_IDENTITY_AUDIT.json','TRANSMISSION.json','MEDIATION.json','READINESS.json','IDENTITY_CROSSWALK.json']]
 def test_01_preservation(self):
  entries=load(HERE/'PRESERVATION_BEFORE.json');self.assertEqual(len(entries),9012)
  for p,h in entries.items():self.assertEqual(sha(ROOT/p),h,p)
 def test_02_spec_and_prior_release(self):
  d=load(HERE/'DEPENDENCIES.json');s=ROOT/'research/genesis-brain-spec-v0.2'
  h=d['brain_spec_v02_registry_sha256'];self.assertEqual(sha(s/'objects'/f'{h}.json'),h)
  self.assertEqual(sha(PRIOR/'RELEASE.json'),d['route_study_release_file_sha256'])
  r=load(PRIOR/'RELEASE.json');self.assertEqual(r['content_sha256'],d['route_study_content_sha256'])
  for p,h in r['files'].items():self.assertEqual(sha(PRIOR/p),h,p)
 def test_03_canonical(self):
  b=load(HERE/'CANONICAL_BEFORE.json');a=load(HERE/'CANONICAL_AFTER.json');self.assertEqual(a,b)
  self.assertEqual(a['sha256'],load(HERE/'DEPENDENCIES.json')['canonical_state_expected_sha256'])
  self.assertEqual(a['tableRowCounts']['genesis_decisions'],7);self.assertFalse(a['schedule'][0]['enabled'])
 def test_04_sources(self):
  s=load(HERE/'SOURCE_MANIFEST.json')
  for f in s['originals']+s['ancillary_files']:self.assertEqual(sha(HERE/f['path']),f['sha256'])
 def test_05_archive(self):
  a=load(HERE/'ARCHIVE_AUDIT.json');self.assertEqual(a['directory_members'],57)
  w=[r for r in a['extracted'] if r['name'].endswith('.xlsx')];self.assertEqual(len(w),36)
  for r in a['extracted']:self.assertEqual(sha(HERE/r['path']),r['sha256'])
  for r in w:
   self.assertTrue(r['identical_to_final']);self.assertEqual(sha(HERE/r['path']),sha(ROOT/r['final_counterpart']))
   with zipfile.ZipFile(HERE/r['path']) as z:self.assertIsNone(z.testzip())
 def test_06_observed_identities(self):
  x=load(HERE/'SOURCE_IDENTITY_AUDIT.json');self.assertEqual(len(x['four_responders']),4);self.assertEqual(len(x['recall_records']),11)
  self.assertEqual([c['source_column'] for c in x['four_responders']],list('PQRS'))
  self.assertEqual(len(x['archives']),9)
  for a in x['archives']:self.assertEqual(a['candidate_morphology_or_identity_parts'],[])
 def test_07_guard(self):guard(*self.args())
 def test_08_reject_response_identity_promotion(self):
  for k,v in [('identified_cell_type','SMP353'),('identified_FlyWire_root','720575940608236978'),('recording_to_morphology_link','MCFO cell#1')]:
   a=self.args();a[0]['four_responders'][0][k]=v
   with self.assertRaises(AssertionError):guard(*a)
 def test_09_reject_recall_identity_from_row(self):
  a=self.args();a[0]['recall_records'][0]['fly_id']='Fly1'
  with self.assertRaises(AssertionError):guard(*a)
 def test_10_reject_unknown_to_zero_or_sign(self):
  for k,v in [('sign','inhibitory'),('receptor','GluCl'),('receptor',0)]:
   a=self.args();a[1]['target_specific'][0][k]=v
   with self.assertRaises(AssertionError):guard(*a)
 def test_11_reject_double_counting(self):
  a=self.args();a[1]['independent_replications_added']=1
  with self.assertRaises(AssertionError):guard(*a)
 def test_12_reject_current_conversion(self):
  a=self.args();a[1]['inhibitory_synaptic_current_measured']=True
  with self.assertRaises(AssertionError):guard(*a)
 def test_13_reject_mediation_promotion(self):
  for key in ['complete-mediated-chain','chronic-blockade','acute-blockade-upwind']:
   a=self.args();next(x for x in a[2]['links'] if x['id']==key)['classification']='SUPPORTED'
   with self.assertRaises(AssertionError):guard(*a)
 def test_14_reject_composition(self):
  a=self.args();a[2]['numerical_composition']=True
  with self.assertRaises(AssertionError):guard(*a)
 def test_15_reject_stage5_or_execution(self):
  for k,v in [('stage5_authorized',True),('stage5_protocol',{}),('neural_runs',1),('canonical_writes',1),('fitted_parameters',['gain']),('decoder','weighted_sum'),('capability_promotions',['action'])]:
   a=self.args();a[3][k]=v
   with self.assertRaises(AssertionError):guard(*a)
 def test_16_reject_missing_scope_and_ownership(self):
  a=self.args();a[4]['mappings'][0]['evidence']=[]
  with self.assertRaises(AssertionError):guard(*a)
  a=self.args();a[4]['anatomy_ownership']=['synapse']
  with self.assertRaises(AssertionError):guard(*a)
 def test_17_resolutions(self):
  r=load(HERE/'READINESS.json');self.assertEqual(len(r['requirements']),10)
  self.assertEqual({r['resolution'] for r in r['resolutions']},{'individual-root','cell-type','driver-population'})
  for k in ['root_identity_is_not_universal_prerequisite','complete_prior_mediation_proof_is_not_prerequisite']:
   a=self.args();a[3][k]=False
   with self.assertRaises(AssertionError):guard(*a)
 def test_18_release_if_published(self):
  if not (HERE/'RELEASE.json').exists():return
  r=load(HERE/'RELEASE.json')
  for p,h in r['files'].items():self.assertEqual(sha(HERE/p),h,p)
  self.assertEqual(hashlib.sha256(json.dumps(r['files'],sort_keys=True,separators=(',',':')).encode()).hexdigest(),r['content_sha256'])

if __name__=='__main__':unittest.main(verbosity=2)

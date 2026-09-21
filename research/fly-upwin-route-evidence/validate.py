"""Read-only validation. No simulation, fitting, runtime import or database connection."""
from common import *
import unittest,copy,gzip,zipfile,re,numpy as np

def guard(evidence,readiness,crosswalk,dependencies):
 assert evidence['spec_registry_sha256']==SPEC_SHA
 assert evidence['spec_package_sha256']==PACKAGE_SHA
 assert evidence['admitted_to_spec'] is False and evidence['new_neural_operators']==[]
 assert readiness['stage5_authorized'] is False and readiness['stage5_protocol'] is None
 assert readiness['neural_runs']==0 and readiness['fitting'] is False and readiness['capability_promotions']==[]
 assert readiness['classification']=='PARTIAL ROUTE SUPPORT — TARGETED EVIDENCE STILL REQUIRED'
 assert dependencies['evidence_overrides']==[] and dependencies['state_ownership']==[]
 assert dependencies['capability_promotions']==[]
 assert crosswalk['root_ownership'].startswith('References only')
 for r in crosswalk['roots']:
  assert isinstance(r['root_id'],str) and re.fullmatch('[0-9]{18}',r['root_id'])
  assert r['target_specific_sign'] is None and r['receptor'] is None and r['recorded_cell_identity'] is None
 for c in evidence['claims']:
  assert c['category'] in ['BIOLOGICAL FACT','EXPERIMENTALLY SUPPORTED COMPUTATIONAL APPROXIMATION','HYPOTHESIS','ENGINEERING ASSUMPTION','GENESIS PRODUCT MAPPING']
  if c['category']=='BIOLOGICAL FACT':assert c.get('source') and c.get('scope')
  if c['category']=='GENESIS PRODUCT MAPPING':assert c['value'] is None
class Audit(unittest.TestCase):
 def test_01_dependencies(self):
  reg=load(SPEC/'objects'/f'{SPEC_SHA}.json');self.assertEqual(sha(SPEC/'objects'/f'{SPEC_SHA}.json'),SPEC_SHA)
  for k,v in load(HERE/'DEPENDENCIES.json')['dependencies'].items():
   self.assertEqual(v,reg['entry_hashes'][k]);entry=next(e for e in reg['entries'] if e['id']==k)
   self.assertEqual(hashlib.sha256(json.dumps(entry,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest(),v)
  self.assertTrue(load(HERE/'SPEC_VALIDATION.json')['valid'])
 def test_02_protected_files(self):
  for p,h in load(HERE/'FROZEN_BEFORE.json').items():self.assertEqual(sha(ROOT/p),h,p)
 def test_03_canonical(self):
  b=load(HERE/'CANONICAL_BEFORE.json');a=load(HERE/'CANONICAL_AFTER.json');self.assertEqual(a,b)
  self.assertEqual(a['tableRowCounts']['genesis_decisions'],7);self.assertFalse(a['schedule'][0]['enabled'])
 def test_04_original_sources(self):
  for w in load(HERE/'SOURCE_MANIFEST.json')['workbooks']:
   p=HERE/w['path'];self.assertEqual(sha(p),w['sha256'])
   with zipfile.ZipFile(p) as z:self.assertIsNone(z.testzip())
  for s in load(HERE/'AUXILIARY_SOURCES.json')['files']:self.assertEqual(sha(HERE/s['path']),s['sha256'])
 def test_05_processed_cells(self):
  ws=load(HERE/'WORKBOOK_INVENTORY.json');self.assertEqual(len(ws),36)
  for w in ws:
   self.assertEqual(sha(HERE/w['processed_path']),w['processed_sha256']);data=json.loads(gzip.decompress((HERE/w['processed_path']).read_bytes()))
   self.assertEqual(sum(len(s['cells']) for s in data),sum(s['actual_populated_cells'] for s in w['sheets']))
 def test_06_means_and_sem(self):
  for c in load(HERE/'MEASUREMENT_AUDIT.json')['conditioning']:
   for g in c['groups'].values():self.assertLess(abs(g['mean_error']),1e-12);self.assertLess(abs(g['sem_error']),1e-12)
  for c in load(HERE/'ALPHA1_CONDITIONING_AUDIT.json')['groups']:
   for g in c['groups']:self.assertLess(abs(g['mean_error']),1e-12);self.assertLess(abs(g['sem_error']),1e-12)
 def test_07_anatomy_independent_sum(self):
  d=ROOT/'research/fly-boundary-study/anatomy';ns=load(d/'nodes.json');ids={n['root_id']:i for i,n in enumerate(ns)}
  p=np.load(d/'pre.npy',mmap_mode='r');q=np.load(d/'post.npy',mmap_mode='r');c=np.load(d/'count.npy',mmap_mode='r')
  mask=(p==ids['720575940617302365'])&(q==ids['720575940608236978']);self.assertEqual(int(c[mask].sum()),11)
  a=load(HERE/'ANATOMY_AUDIT.json');s=a['boundary_sets']['annotation_candidate_context'];self.assertEqual((s['neurons'],s['directed_pairs'],s['contacts']),(14,47,751))
  for r in s['roots']:
   self.assertEqual(r['full_input_contacts'],r['retained_input_contacts']+r['omitted_input_contacts'])
   self.assertEqual(r['full_output_contacts'],r['retained_output_contacts']+r['omitted_output_contacts'])
 def test_08_guard(self):guard(*self.args())
 def args(self):return [load(HERE/f) for f in ['EVIDENCE_LEDGER.json','READINESS.json','CROSSWALK.json','DEPENDENCIES.json']]
 def test_09_reject_sign_promotion(self):
  a=self.args();a[2]['roots'][0]['target_specific_sign']='inhibitory'
  with self.assertRaises(AssertionError):guard(*a)
 def test_10_reject_unknown_to_zero(self):
  a=self.args();a[2]['roots'][1]['receptor']=0
  with self.assertRaises(AssertionError):guard(*a)
 def test_11_reject_stage5_and_capability(self):
  for k,v in [('stage5_authorized',True),('capability_promotions',['action-selection']),('stage5_protocol',{})]:
   a=self.args();a[1][k]=v
   with self.assertRaises(AssertionError):guard(*a)
 def test_12_reject_ownership_override(self):
  for k,v in [('state_ownership',['new_synapse_owner']),('evidence_overrides',['change-stage1'])]:
   a=self.args();a[3][k]=v
   with self.assertRaises(AssertionError):guard(*a)
 def test_13_reject_product_leak_and_missing_source(self):
  a=self.args();a[0]['claims'][-1]['value']='APPROACH'
  with self.assertRaises(AssertionError):guard(*a)
  a=self.args();a[0]['claims'][0].pop('source')
  with self.assertRaises(AssertionError):guard(*a)
 def test_14_preparation_scope(self):
  x=load(HERE/'PREPARATION_COMPATIBILITY.json');self.assertEqual(len(x['bridges']),28);self.assertFalse(x['composite_pathway_created'])
  self.assertEqual(set(b['classification'] for b in x['bridges']),{'DIRECTLY COMPATIBLE','TRANSFER REQUIRES ASSUMPTION','INCOMPATIBLE','UNKNOWN'})
 def test_15_release_if_present(self):
  p=HERE/'RELEASE.json'
  if p.exists():
   r=load(p)
   for f,h in r['files'].items():self.assertEqual(sha(HERE/f),h,f)
   self.assertEqual(hashlib.sha256(json.dumps(r['files'],sort_keys=True,separators=(',',':')).encode()).hexdigest(),r['content_sha256'])
if __name__=='__main__':unittest.main(verbosity=2)

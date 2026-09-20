import unittest,copy
from governance import *

class GovernanceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=registry();cls.reviews=load(HERE/'ADMISSION_REVIEWS.json')
 def test_valid_reviewed_append(self):self.assertTrue(check_registry(self.r,self.reviews))
 def test_historical_entry_not_changed(self):
  r=copy.deepcopy(self.r);e=next(x for x in r['entries'] if x['id']=='capability.persistence');e['status']='validated';r['entry_hashes'][e['id']]=digest(e)
  with self.assertRaises(ValueError):check_registry(r,self.reviews)
 def test_negative_result_not_promoted_even_rehashed(self):
  r=copy.deepcopy(self.r);a=copy.deepcopy(self.reviews);e=next(x for x in r['entries'] if x['id']=='visual.stage4.gate-a');e['status']='validated';r['entry_hashes'][e['id']]=digest(e)
  next(x for x in a if x['entry_id']==e['id'])['entry_sha256']=digest(e)
  with self.assertRaises(ValueError):check_registry(r,a)
 def test_missing_provenance_or_review(self):
  r=copy.deepcopy(self.r);e=next(x for x in r['entries'] if x['id']=='visual.empirical.interface');e['evidence_refs']=[];r['entry_hashes'][e['id']]=digest(e)
  with self.assertRaises(ValueError):check_registry(r,self.reviews)
  with self.assertRaises(ValueError):check_registry(self.r,self.reviews[:-1])
 def test_unknown_sign_cannot_gain_provenance_by_rehash(self):
  r=copy.deepcopy(self.r);e=next(x for x in r['entries'] if x['id']=='visual.diagnostic.representation');e['sign']={'state':'known','value':-1,'evidence_refs':[],'scope':''};r['entry_hashes'][e['id']]=digest(e)
  with self.assertRaises(ValueError):check_registry(r,self.reviews)
 def test_product_claim_rejected(self):
  r=copy.deepcopy(self.r);e=next(x for x in r['entries'] if x['id']=='visual.empirical.interface');e['category']='GENESIS PRODUCT MAPPING';r['entry_hashes'][e['id']]=digest(e)
  with self.assertRaises(ValueError):check_registry(r,self.reviews)
 def test_capability_limits(self):
  c=load(HERE/'CAPABILITY_REGISTRY.json');check_capabilities(c)
  for row in c['capabilities']:
   if row['id']=='capability.associative_appetitive_learning':continue
   bad=copy.deepcopy(c);next(x for x in bad['capabilities'] if x['id']==row['id'])['status']='validated'
   with self.assertRaises(ValueError):check_capabilities(bad)
 def test_anatomy_and_shared_rules(self):
  i=load(HERE/'CANONICAL_IDENTITY_REFERENCES.json');check_identity(i)
  for field,value in [('ownership','new_owner'),('new_rows_owned',5675),('physiology_composition','combined')]:
   bad=copy.deepcopy(i);bad[field]=value
   with self.assertRaises(ValueError):check_identity(bad)
 def test_sensory_unknown_observation_and_ood(self):
  s=load(HERE/'SENSORY_BOUNDARY_CONTRACT.json');check_sensory(s)
  for name in ['calcium','spikes','release','synaptic_current','model_rate']:
   b=copy.deepcopy(s);b['empirical_instance']['conversions'][name]['value']=0
   with self.assertRaises(ValueError):check_sensory(b)
  for key,value in [('units','Hz'),('Stage4_conditions_ood',0),('omitted_circuits_simulated',True)]:
   b=copy.deepcopy(s);b['empirical_instance'][key]=value
   with self.assertRaises(ValueError):check_sensory(b)
  for key in ['root','subtype','column','fly']:
   b=copy.deepcopy(s);b['empirical_instance']['identity_resolution'][key]='invented'
   with self.assertRaises(ValueError):check_sensory(b)
 def test_future_dependency_and_duplicate_ownership(self):
  cid='visual.empirical.observation';m={'registry_sha256':digest(self.r),'dependencies':{cid:self.r['entry_hashes'][cid]},'evidence_overrides':[],'capability_promotions':[],'state_ownership':[],'input_channels':[]}
  self.assertTrue(check_future_dependencies(m,self.r))
  b=copy.deepcopy(m);b['dependencies'][cid]='0'*64
  with self.assertRaises(ValueError):check_future_dependencies(b,self.r)
  b=copy.deepcopy(m);b['evidence_overrides']=[{'id':cid,'status':'validated'}]
  with self.assertRaises(ValueError):check_future_dependencies(b,self.r)
  b=copy.deepcopy(m);b['state_ownership']=[{'canonical_row_id':'same','model_instance':'one','owner':x} for x in ['stage1','stage3']]
  with self.assertRaises(ValueError):check_future_dependencies(b,self.r)
 def test_future_product_input(self):
  cid='visual.empirical.observation';m={'registry_sha256':digest(self.r),'dependencies':{cid:self.r['entry_hashes'][cid]},'input_channels':[{'layer':'biological','category':'GENESIS PRODUCT MAPPING','units':'USD','evidence_refs':[cid]}]}
  with self.assertRaises(ValueError):check_future_dependencies(m,self.r)
 def test_stage5_not_authorized(self):
  r=load(HERE/'STAGE5_READINESS.json');self.assertFalse(r['experiment_authorized']);self.assertFalse(r['protocol_designed']);self.assertEqual(r['neural_runs'],0);self.assertEqual(r['classification'],'PARTIAL READINESS — TARGETED EVIDENCE REQUIRED')

if __name__=='__main__':unittest.main(verbosity=2)

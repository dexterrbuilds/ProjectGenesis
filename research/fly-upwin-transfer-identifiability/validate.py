"""Read-only validation of preservation, observations, and identification limits."""
from common import *
import unittest,math,copy,csv,itertools
from fractions import Fraction

def guard(t,design,firewall,matrix,observations):
 assert design['stage5_authorized'] is False and design['stage5_protocol'] is None
 assert design['physical_parameters_fitted']==[] and design['new_biological_capabilities']==[]
 assert design['no_positive_biological_result_guaranteed'] is True
 assert design['prior_route_readiness_unchanged'] is True
 assert design['classification']=='STAGE-5 DESIGN POSSIBLE UNDER EXPLICIT TRANSFER UNCERTAINTY'
 assert 'conditional' in design['scope'].lower()
 assert firewall['model_runs']==0 and set(firewall['downstream_family_contains'])=={'same order','reversed order','tie'}
 assert all(x['exported_physical_value'] is None for x in firewall['readonly_order_audit'])
 assert matrix['new_joins']==[] and all(x['value'] is None for x in matrix['hypotheses'])
 assert observations['direct_rate_to_voltage_conversion'] is None
 assert observations['acute_vs_recall_composition'] is False and observations['external_population_identity_join'] is None
 assert observations['observed_detection_fraction']['population_interval'] is None
 assert observations['acute']['nonresponders']==13 and observations['acute']['responders']==4
 q={x['id']:x for x in t['quantities']}
 for k in ['transfer-sign','monotonicity','population-fraction','gain','latency','kernel','saturation','latent-heterogeneity','conditioning-modulation','common-transfer','disinhibition','downstream-order']:
  assert q[k]['classification']=='NON-IDENTIFIABLE' and q[k]['identified_value'] is None
 assert q['conditional-bounds']['classification']=='BOUNDED'
 assert 'Conditional' in q['conditional-bounds']['scope']
 for x in q.values():
  assert x['scope'] and x['counterexample_test']
  assert x['classification'] in ['IDENTIFIED','BOUNDED','QUALITATIVELY CONSTRAINED','NON-IDENTIFIABLE']

class Audit(unittest.TestCase):
 def args(self):return [load(HERE/p) for p in ['IDENTIFIABILITY.json','DESIGN_SUFFICIENCY.json','STAGE1_FIREWALL.json','OBSERVATION_MATRIX.json','OBSERVATIONS.json']]
 def test_01_preservation(self):
  p=load(HERE/'PRESERVATION_BEFORE.json');self.assertEqual(len(p),9147)
  for name,h in p.items():self.assertEqual(sha(ROOT/name),h,name)
 def test_02_dependencies(self):
  d=load(HERE/'DEPENDENCIES.json');self.assertEqual(d['new_literature_sources'],[]);self.assertEqual(d['evidence_overrides'],[])
  for k,folder in [('route',ROUTE),('identity',IDENTITY)]:
   self.assertEqual(sha(folder/'RELEASE.json'),d['packages'][k]['release_sha256']);r=load(folder/'RELEASE.json')
   self.assertEqual(hashlib.sha256(json.dumps(r['files'],sort_keys=True,separators=(',',':')).encode()).hexdigest(),d['packages'][k]['content_sha256'])
  h=d['packages']['spec']['registry_sha256'];self.assertEqual(sha(SPEC/'objects'/f'{h}.json'),h)
  for f,h in d['packages']['stage1']['files'].items():self.assertEqual(sha(STAGE1/f),h)
 def test_03_canonical(self):
  b=load(HERE/'CANONICAL_BEFORE.json');a=load(HERE/'CANONICAL_AFTER.json');self.assertEqual(a,b)
  self.assertEqual(a['sha256'],'3377c9dddbe2abf89ed9a820a6aabbc1da951cac7bfc1823471c5aac043ea312')
  self.assertEqual(a['tableRowCounts']['genesis_decisions'],7);self.assertFalse(a['schedule'][0]['enabled'])
 def test_04_observations_preserved(self):
  o=load(HERE/'OBSERVATIONS.json');m=load(ROUTE/'MEASUREMENT_AUDIT.json')
  self.assertEqual(o['acute'],next(x for x in m['whole_cell'] if x['file']=='elife-85756-fig4-data2-v3.xlsx'))
  self.assertEqual(len(o['acute']['traces']),17)
  for p,h in o['source_files'].items():self.assertEqual(sha(ROOT/p),h)
  self.assertEqual(o['upstream_conditioning'],load(ROUTE/'ALPHA1_CONDITIONING_AUDIT.json'))
 def test_05_recall_arithmetic(self):
  o=load(HERE/'OBSERVATIONS.json');m=load(ROUTE/'MEASUREMENT_AUDIT.json')
  self.assertEqual(sum(len(c['rows']) for c in o['recall']),11)
  for c,src in zip(o['recall'],m['conditioning']):
   p=c['paired_odor'];u='MCH' if p=='OCT' else 'OCT'
   for r,s in zip(c['rows'],src['observations']):
    self.assertEqual(r['source_row'],s['source_row'])
    self.assertAlmostEqual(r['within_row_difference_of_changes_mV'],s[p+'_post_mV']-s[p+'_pre_mV']-s[u+'_post_mV']+s[u+'_pre_mV'],places=12)
    self.assertIsNone(r['animal_id']);self.assertIsNone(r['recording_id'])
 def test_06_stage1_ordinal_only(self):
  f=load(HERE/'STAGE1_FIREWALL.json');xs=f['readonly_order_audit'];self.assertEqual(len(xs),6)
  raw={r['run']:r for r in csv.DictReader((STAGE1/'RESULTS.csv').open())}
  for x in xs:
   r=raw[x['run']];c=r['paired'];self.assertEqual(x['paired_post_less_than_pre'],float(r[f'post_{c}_MBON_app'])<float(r[f'baseline_{c}_MBON_app']))
   self.assertTrue(x['paired_post_less_than_pre']);self.assertIsNone(x['exported_physical_value'])
 def test_07_algebra_sign_and_monotonicity(self):
  for x in [Fraction(i,10) for i in range(11)]:self.assertEqual(-x,x-2*x)
  for c in range(-10,11):
   for x in [0,1]:self.assertEqual(-x+c*x*(x-1),-x)
  self.assertLess(-1+4*(2*0-1),0);self.assertGreater(-1+4*(2*1-1),0)
 def test_08_gain_and_saturation(self):
  for k in [Fraction(1,100),Fraction(1),Fraction(100)]:self.assertEqual((1/k)*(k*Fraction(1,2)),Fraction(1,2))
  vals=[]
  for s in [.1,1,10]:
   self.assertAlmostEqual(-(1-math.exp(-1/s))/(1-math.exp(-1/s)),-1)
   vals.append(-1/(1-math.exp(-1/s)))
  self.assertGreater(abs(vals[0]-vals[-1]),9)
 def test_09_non_identified_mixture(self):
  p=Fraction(4,17);self.assertEqual(p*1,1*p)
  self.assertEqual(load(HERE/'OBSERVATIONS.json')['observed_detection_fraction']['value'],4/17)
 def test_10_recall_nullspace(self):
  d=load(HERE/'DEGENERACY.json');self.assertEqual(len(d['recall_nullspace']),66)
  self.assertLess(d['recall_max_error'],1e-12)
  # For J=[dx | I], vector [1,-dx] is exactly null for arbitrary dx.
  dx=[Fraction(i-11,7) for i in range(22)];self.assertTrue(all(x*1+(-x)==0 for x in dx))
  for pair in itertools.product([Fraction(-2),Fraction(0),Fraction(2)], [Fraction(-3),Fraction(1)]):
   g,dy=pair;z=dy+g;self.assertEqual(-g+z,dy)
 def test_11_temporal_factorization(self):
  for f in [.1,1,10]:
   s=complex(0,f);a=1/(1+s);b=1/(1+2*s);self.assertLess(abs(a*b-b*a),1e-12)
  self.assertTrue(all(x['swap_error']<1e-12 for x in load(HERE/'DEGENERACY.json')['convolution_factorization']))
 def test_12_every_identified_claim_challenged(self):
  t=load(HERE/'IDENTIFIABILITY.json');cs={x['id'] for x in load(HERE/'COUNTEREXAMPLES.json')['witnesses']}
  for q in t['quantities']:self.assertIn(q['counterexample_test'],cs)
  identified=[q for q in t['quantities'] if q['classification']=='IDENTIFIED'];self.assertEqual(len(identified),5)
  self.assertTrue(all(q['counterexample_test']=='CE-statistics' for q in identified))
 def test_13_matrix(self):
  m=load(HERE/'OBSERVATION_MATRIX.json');self.assertEqual(len(m['domains']),9);self.assertEqual(len(m['between_domains']),36)
  ids={d['id'] for d in m['domains']};self.assertTrue({'behavior_SS33917','behavior_SS33918','alpha1_stimulation','conditioning_recall','connectome'}<=ids)
 def test_14_guard(self):guard(*self.args())
 def test_15_reject_sign_gain_time_promotion(self):
  for key,value in [('transfer-sign','inhibitory'),('gain',1),('kernel',.05),('population-fraction',4/17),('disinhibition',True)]:
   a=self.args();q=next(x for x in a[0]['quantities'] if x['id']==key);q['identified_value']=value;q['classification']='IDENTIFIED'
   with self.assertRaises(AssertionError):guard(*a)
 def test_16_reject_unknown_to_zero(self):
  a=self.args();next(x for x in a[0]['quantities'] if x['id']=='gain')['identified_value']=0
  with self.assertRaises(AssertionError):guard(*a)
 def test_17_reject_merging_and_units(self):
  for index,key,value in [(3,'new_joins',['R64A11=SS67249']),(4,'direct_rate_to_voltage_conversion',1),(4,'acute_vs_recall_composition',True),(4,'external_population_identity_join','SMP353')]:
   a=self.args();a[index][key]=value
   with self.assertRaises(AssertionError):guard(*a)
 def test_18_reject_family_pruning_and_activation(self):
  a=self.args();a[2]['downstream_family_contains']=['reversed order']
  with self.assertRaises(AssertionError):guard(*a)
  for k,v in [('stage5_authorized',True),('stage5_protocol',{}),('physical_parameters_fitted',['gain']),('new_biological_capabilities',['action']),('no_positive_biological_result_guaranteed',False)]:
   a=self.args();a[1][k]=v
   with self.assertRaises(AssertionError):guard(*a)
 def test_19_release_if_sealed(self):
  if not (HERE/'RELEASE.json').exists():return
  r=load(HERE/'RELEASE.json')
  for p,h in r['files'].items():self.assertEqual(sha(HERE/p),h,p)
  self.assertEqual(content_hash(r['files']),r['content_sha256'])

if __name__=='__main__':unittest.main(verbosity=2)

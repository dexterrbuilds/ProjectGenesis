import unittest,copy,subprocess,sys,json
import numpy as np
from common import *
from empirical import *
from interface import *

def query_for(r):
 return {k:copy.deepcopy(r[k]) for k in ['dataset','type','family','frame','observation','units','descriptor','recording']}

class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.api=EmpiricalInterface();cls.rows=cls.api.rows;cls.metrics=read('PREDICTION_METRICS.json')
 def test_all_measured_retrieval(self):
  for r in self.rows:
   out=self.api.query(query_for(r));self.assertEqual(out['status'],'MEASURED');np.testing.assert_array_equal(out['voltage_mV'],self.api.Y[r['id']])
 def test_numeric_identity(self):
  a={'dataset':'d','type':'T5','family':'f','frame':'p','descriptor':{'x':[0,1,-1]}};b=copy.deepcopy(a);b['descriptor']['x']=[-0.,1.,-1.]
  self.assertEqual(descriptor_key(a),descriptor_key(b));b['descriptor']['x'][2]=-2;self.assertNotEqual(descriptor_key(a),descriptor_key(b))
 def test_holdout_isolation(self):
  for m in self.metrics:
   target=self.rows[m['id']];train=[self.rows[i] for i in m['training_ids']]
   self.assertNotIn(target['id'],m['training_ids'])
   if m['test']=='recording_holdout':
    self.assertTrue(all(t['recording']!=target['recording'] for t in train));self.assertGreaterEqual(len({t['recording'] for t in train}),3)
    self.assertTrue(all(descriptor_key(t)==descriptor_key(target) for t in train))
   else:
    axis=m['stratum'].split('|')[-1];self.assertTrue(all(t[axis]!=target[axis] and interp_group(t,axis)==interp_group(target,axis) for t in train))
 def test_heldout_duration_export(self):
  m=next(m for m in self.metrics if m['stratum']=='E1|2021_T5_flash|T5|0.0|1.0|duration');r=self.rows[m['id']]
  api=EmpiricalInterface([x for x in self.rows if x['id']!=r['id']]);out=api.query(query_for(r));self.assertEqual(out['support'],'INTERPOLATION-SUPPORTED');self.assertIsNone(out['uncertainty']['half_width_mV'])
  source=[x for x in self.rows if x['id'] in m['training_ids']];expected=interpolate(r,source,'duration',api.Y)['linear'];np.testing.assert_array_equal(out['voltage_mV'],expected)
 def test_position_tie_identity(self):
  mm=[m for m in self.metrics if m['stratum'].endswith('|offset')];self.assertGreater(len(mm),0);self.assertTrue(all(m['mse']==m['reference_mse'] for m in mm))
 def test_unknown_not_zero(self):
  r=self.rows[0];q=query_for(r)
  changes=[{'FlyWire_root':'720575940000000000'},{'subtype':'a'},{'column':1},{'fly_id':'invented'},{'units':'spikes/s'},{'observation':'calcium'},{'horizon_ms':501},{'frame':'head_degrees'},{'family':'expanding_disc'},{'danger':True},{'recording':'invented'}]
  for change in changes:
   qq=copy.deepcopy(q);qq.update(change);o=self.api.query(qq);self.assertEqual(o['status'],'UNKNOWN');self.assertIsNone(o['voltage_mV'])
  for desc in [{},dict(q['descriptor'],extra=1),dict(q['descriptor'],offset_pixels=1000),dict(q['descriptor'],offset_pixels=.123,duration_ms=77),dict(q['descriptor'],duration_ms=float('nan'))]:
   qq=copy.deepcopy(q);qq['descriptor']=desc;self.assertEqual(self.api.query(qq)['status'],'UNKNOWN')
 def test_class_does_not_become_individual(self):
  m=next(m for m in self.metrics if m['stratum']=='E2|2019_T5_compact|T5|moving_bar|0|all_widths');r=self.rows[m['id']];q=query_for(r);del q['recording']
  self.assertEqual(self.api.query(q)['status'],'UNKNOWN');q['mode']='class_template';out=self.api.query(q);self.assertEqual(out['status'],'CLASS TEMPLATE');self.assertEqual(out['support'],'WEAKLY SUPPORTED');self.assertIsNone(out['root_assignment'])
 def test_whole_family_unknown(self):
  for family in {r['family'] for r in self.rows}:
   api=EmpiricalInterface([r for r in self.rows if r['family']!=family]);targets=[r for r in self.rows if r['family']==family]
   for r in targets[::max(1,len(targets)//20)]:self.assertEqual(api.query(query_for(r))['status'],'UNKNOWN')
 def test_firewall(self):
  code="from common import *\nfirewall()\nfor p in [ROOT/'research/fly-stage4/model.py',HERE/'STAGE4_AUDIT.json']:\n try: p.read_text()\n except PermissionError: pass\n else: raise RuntimeError('Firewall failed')\n"
  result=subprocess.run([sys.executable,'-c',code],cwd=HERE,capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stderr)
 def test_frozen_results(self):
  for n,h in read('PRIMARY_RESULT_LOCK.json')['files'].items():self.assertEqual(sha(HERE/n),h)
  self.assertEqual(sha(HERE/'PROTOCOL.md'),read('REGISTRATION.json')['protocol_sha256'])

if __name__=='__main__':unittest.main(verbosity=2)

import unittest,subprocess,sys,json
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from process import occupancy,records
from models import features,solve,load
from common import HERE
class Tests(unittest.TestCase):
 def setUp(self):self.p=loadmat(HERE/'data/t5-compact/data_cell_1_all.mat',simplify_cells=True)['p']
 def test_static_pulse(self):
  p=dict(self.p,location_sb=np.array([0]),width_sb=np.array([2]),duration_sb=np.array([20]));t=np.array([-5.,0,5,20,25]);s=occupancy(p,0,0,t)
  self.assertEqual(s.sum(),4);self.assertEqual(s[1,12],1);self.assertEqual(s[1,13],1)
 def test_union_not_double_contrast(self):
  p=dict(self.p,fb_pos_mm=np.array([0]),sb_pos_mm=np.array([0]),width_mm=np.array([2]),fbton_mm=0,fbtoff_mm=np.array([20]),sbton_mm=np.array([0]),sbtoff_mm=np.array([20]));s=occupancy(p,4,0,np.arange(-5,30,5));self.assertEqual(s.max(),1);self.assertEqual(s.sum(),8)
 def test_moving_entry_exit(self):
  p=dict(self.p,pos_mb=np.array([-1,0,1]),width_mb=np.array([2]),duration_mb=np.array([10]),direction_mb=np.array([1]));s=occupancy(p,3,0,np.arange(0,50,10));np.testing.assert_array_equal(s.sum(1),[1,2,2,1,0])
 def test_static_correlator_null(self):
  d={'t_ms':np.arange(0,100,5),'x_pixels':np.arange(-13,14),'off_occupancy':np.zeros((20,27)),'starts':np.array([0]),'ends':np.array([20])};d['off_occupancy'][2:10,12:14]=1
  np.testing.assert_array_equal(features(d,'B0'),0)
 def test_trial_reset_and_latency(self):
  d={'t_ms':np.tile(np.arange(0,100,5),2),'x_pixels':np.arange(-13,14),'off_occupancy':np.zeros((40,27)),'starts':np.array([0,20]),'ends':np.array([20,40])};d['off_occupancy'][:20,13]=1
  x=features(d,'B1s',delay=25);np.testing.assert_array_equal(x[:5],0);np.testing.assert_array_equal(x[20:],0)
 def test_original_arrays_dimensions(self):
  for c in range(1,18):
   m=loadmat(HERE/f'data/t5-compact/data_cell_{c}_all.mat',simplify_cells=True);r=records(m['p'],m['d']);self.assertEqual(len(r),len(m['p']['protocol']))
 def test_no_fly_invention(self):
  p=json.loads((HERE/'PARTITIONS.json').read_text());self.assertFalse(p['fly_held_out_possible']);self.assertTrue(all(x['fly_id'] is None for x in p['entries']))
 def test_firewall(self):
  for target in [HERE.parent/'fly-stage4/RESULTS.json',HERE/'processed/cell_01_test.npz',HERE/'data/t5-compact/data_cell_1_all.mat']:
   code='from common import firewall; firewall("fit"); open('+repr(str(target))+')'
   r=subprocess.run([sys.executable,'-c',code],cwd=HERE,capture_output=True,text=True);self.assertNotEqual(r.returncode,0);self.assertIn('PermissionError',r.stderr)
 def test_training_files_only_flash(self):
  for c in range(1,18):
   d=load(HERE/f'processed/cell_{c:02d}_train.npz');self.assertTrue(all(x['family']=='flash' and x['width_pixels']==2 for x in d['metadata']))
if __name__=='__main__':unittest.main()

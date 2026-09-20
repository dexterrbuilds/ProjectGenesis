"""Artifact and model-extension integrity checks, not behavioral acceptance."""
import ast,hashlib,json,unittest
from pathlib import Path
import numpy as np
from context import H,A,Expanded
class Tests(unittest.TestCase):
 def test_frozen_hashes(self):
  for p,h in json.loads((H/'FROZEN_BEFORE.json').read_text()).items():self.assertEqual(hashlib.sha256(Path(p).read_bytes()).hexdigest(),h,p)
 def test_anatomy_hashes(self):
  for p,h in json.loads((A/'manifest.json').read_text())['files'].items():self.assertEqual(hashlib.sha256((A/p).read_bytes()).hexdigest(),h,p)
 def test_nested_selections(self):
  n=json.loads((A/'metadata.json').read_text())['neurons']
  for s in (1,2,3):
   last=set()
   for l in range(5):
    ix=np.load(A/f's{s}-L{l}.npy');new=set(map(int,ix));self.assertTrue(last<=new);self.assertEqual(len(new),len(ix));last=new
   self.assertEqual(len(last),n)
 def test_root_identity(self):
  nodes=json.loads((A/'nodes.json').read_text());ids=[x['root_id'] for x in nodes]
  self.assertEqual(len(ids),len(set(ids)));self.assertTrue(all(type(x) is str for x in ids))
 def test_no_hidden_inputs(self):
  for name in ('context.py','benchmark.py'):
   tree=ast.parse((H/name).read_text())
   imported=[n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)]
   self.assertFalse(any(x and any(t in x.lower() for t in ('openai','wallet','planner','genesis')) for x in imported))
 def test_recorded_kernel_equalities(self):
  for r in json.loads((H/'kernel-checks.json').read_text()):
   self.assertTrue(r['L0_rate_exact']);self.assertTrue(r['L0_plastic_exact']);self.assertTrue(r['expanded_context_cut_exact'])
 def test_full_replays(self):
  rows=[json.loads(p.read_text()) for p in (H/'benchmarks').glob('*/result.json')]
  self.assertEqual(len(rows),3)
  for r in rows:self.assertTrue(r['replay_exact']);self.assertTrue(r['finite']);self.assertEqual(r['neurons'],139255)
 def test_context_norm_bound_and_no_new_plasticity(self):
  c=Expanded(2,1);m=c.make();n=c.original.n
  core=c.original;c0=c.module.Model(core)
  self.assertEqual(len(m.multiplier),len(c0.multiplier))
  rows=np.bincount(c.add_post,weights=np.abs(c.add_base*c.sign[c.add_pre]*.05),minlength=c.n)
  self.assertLessEqual(rows.max(),.05+1e-14)
  u=np.zeros(c.n)
  for _ in range(10):m.step(u)
  self.assertTrue(np.all(m.r==0));self.assertTrue(np.all(m.multiplier==1))
if __name__=='__main__':unittest.main(verbosity=2)

"""L0 numerical equivalence and anatomy-only extension checks, no fitting."""
import json
from pathlib import Path
import numpy as np
from context import Expanded,H
rows=[]
for s in (1,2,3):
 c=Expanded(s,0);m=c.make();kw={'resource':.2} if s==3 else {}
 original=c.module.Model(c.original,**kw);current=np.zeros(c.n);current[c.groups['PN'][:3]]=1
 for k in range(50):
  if s==3:m.step(current,.2);original.step(current,.2)
  else:m.step(current);original.step(current)
 assert np.array_equal(m.r,original.r) and np.array_equal(m.multiplier,original.multiplier),s
 rows.append({'stage':s,'L0_rate_exact':True,'L0_plastic_exact':True})
 # Existing anatomical edges and declared signs are used for added operator only.
 ex=Expanded(s,1);cut=ex.make(variant='context_cut');u=np.zeros(ex.n);u[:c.n]=current
 orig=c.module.Model(c.original,**kw)
 for k in range(50):
  if s==3:cut.step(u,.2);orig.step(current,.2)
  else:cut.step(u);orig.step(current)
 assert np.array_equal(cut.r[:c.n],orig.r) and np.all(cut.r[c.n:]==0)
 assert np.array_equal(cut.multiplier,orig.multiplier)
 rows[-1]['expanded_context_cut_exact']=True
(H/'kernel-checks.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows))

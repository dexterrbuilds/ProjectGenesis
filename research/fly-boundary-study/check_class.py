import hashlib,json
import numpy as np
from context import H
from class_context import Expanded
rows=[]
for s in (1,2,3):
 c=Expanded(s,1);m=c.make();sparse=m.fixed.copy();padded=sparse.copy()
 # Compare exactly equivalent sparse representation with an explicit zero diagonal.
 from scipy.sparse import coo_matrix
 z=sparse.tocoo();padded=coo_matrix((np.r_[z.data,np.zeros(c.n)],(np.r_[z.row,np.arange(c.n)],np.r_[z.col,np.arange(c.n)])),shape=z.shape).tocsr()
 clone=c.make();clone.fixed=padded;u=np.zeros(c.n);u[c.groups['PN'][:16]]=1
 for _ in range(100):
  if s==3:m.step(u,.2);clone.step(u,.2)
  else:m.step(u);clone.step(u)
 assert np.array_equal(m.r,clone.r) and np.array_equal(m.multiplier,clone.multiplier)
 rows.append({'stage':s,'zero_storage_elimination_bit_exact':True,'extension':m.extension,'observed_active_added_neurons':int(np.count_nonzero(m.r[c.original.n:]>1e-8))})
(H/'class-kernel-checks.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows))

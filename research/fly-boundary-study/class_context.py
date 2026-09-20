"""Class-consistent added anatomy. Frozen core and plastic compartments unchanged."""
import hashlib
import numpy as np
from scipy.sparse import csr_matrix
from context import Expanded as Generic,H
class Expanded(Generic):
 def make(self,*args,variant='primary',**kw):
  # Parent owns all frozen kernel setup, interventions and normalization arms.
  m=super().make(*args,variant=variant,**kw);o=self.original;p=m.p
  src,dst=self.add_pre,self.add_post
  kc=np.array([a.get('cell_class')=='Kenyon_Cell' or (i<o.n and o.roles[i]=='KC') for i,a in enumerate(self.nodes)])
  pn=np.array([a.get('cell_class')=='ALPN' or (i<o.n and o.roles[i]=='PN') for i,a in enumerate(self.nodes)])
  apl=np.array([a.get('cell_type')=='APL' or (i<o.n and o.roles[i]=='APL') for i,a in enumerate(self.nodes)])
  mbon=np.zeros(self.n,dtype=bool)
  names={1:['MBON_app','MBON_av'],2:['MBON','CONTROL','AMBIGUOUS'],3:['MB11','MB18','VALUE','CONTROL']}[self.stage]
  for role in names:mbon[o.groups[role]]=True
  gain=np.full(len(src),p.recurrent_gain)
  gain[pn[src]&kc[dst]]=p.pn_gain
  gain[kc[src]&(mbon[dst]|apl[dst])]=1
  gain[apl[src]&kc[dst]]=p.apl_gain
  sign=self.sign_hypothesis if variant=='glutamate_inhibitory' else self.sign
  scale={'context_half':.5,'context_double':2.,'context_cut':0.}.get(variant,1.)
  added=self.add_base*sign[src]*gain*scale
  core=m.fixed[:o.n,:o.n].tocoo()
  m.fixed=csr_matrix((np.concatenate([core.data,added]),(np.concatenate([core.row,dst]),np.concatenate([core.col,src]))),shape=(self.n,self.n))
  m.fixed.eliminate_zeros()
  m.fingerprint=hashlib.sha256((m.fingerprint+'class-consistent-1'+hashlib.sha256((H/'class_context.py').read_bytes()).hexdigest()+hashlib.sha256(m.fixed.data.tobytes()).hexdigest()).encode()).hexdigest()
  m.extension.update(operator='class-consistent-1',nonzero_added_rows=int(np.count_nonzero(added)),matrix_bytes=sum(x.nbytes for x in (m.fixed.data,m.fixed.indices,m.fixed.indptr)),added_PN_KC_rows=int(np.count_nonzero(pn[src]&kc[dst])),added_KC_APL_MBON_rows=int(np.count_nonzero(kc[src]&(mbon[dst]|apl[dst]))))
  return m

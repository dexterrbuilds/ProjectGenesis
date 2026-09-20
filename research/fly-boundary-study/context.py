"""Read-only frozen kernels with explicit added-anatomy operator. No biological decoder."""
import importlib.util,sys,hashlib,json,copy
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix
H=Path(__file__).resolve().parent;A=H/'anatomy'
def load_stage(stage):
 path=H.parent/f'fly-stage{stage}'
 spec=importlib.util.spec_from_file_location(f'frozen_model_{stage}',path/'model.py');m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
 sys.modules['model']=m
 spec=importlib.util.spec_from_file_location(f'frozen_experiment_{stage}',path/'experiment.py');e=importlib.util.module_from_spec(spec);sys.modules[spec.name]=e;spec.loader.exec_module(e)
 c=m.Circuit(next((path/'artifacts').iterdir()))
 return m,e,c
class Expanded:
 def __init__(self,stage,level):
  self.stage,self.level=stage,level;self.module,self.experiment,self.original=load_stage(stage);o=self.original
  nodes=json.loads((A/'nodes.json').read_text());idx={a['root_id']:i for i,a in enumerate(nodes)}
  core=np.array([idx[r] for r in o.ids]);sel=np.load(A/f's{stage}-L{level}.npy');extra=sel[~np.isin(sel,core)];order=np.concatenate([core,extra]);inv=np.full(len(nodes),-1,dtype=np.int32);inv[order]=np.arange(len(order))
  self.global_indices=order;self.n=len(order);self.ids=[nodes[i]['root_id'] for i in order];self.index={r:i for i,r in enumerate(self.ids)}
  self.nodes=o.nodes+[nodes[i] for i in extra];self.groups=o.groups;self.roles=np.concatenate([o.roles,np.array(['CONTEXT']*len(extra))]);self.pre=o.pre;self.post=o.post;self.count=o.count;self.edges=o.edges
  self.sign=np.load(A/'sign.npy')[order];self.threshold=np.array([.15 if nodes[i]['cell_class']=='Kenyon_Cell' else 0 for i in order]);self.sign_hypothesis=np.array([-1 if nodes[i]['top_nt']=='glutamate' else self.sign[j] for j,i in enumerate(order)])
  self.full_input=np.load(A/'full_input.npy')[order];self.manifest_hash=hashlib.sha256((A/'manifest.json').read_bytes()+str((stage,level)).encode()).hexdigest()
  self.omitted=np.zeros(self.n)
  pre=np.load(A/'pre.npy',mmap_mode='r');post=np.load(A/'post.npy',mmap_mode='r');cnt=np.load(A/'count.npy',mmap_mode='r')
  a,b=inv[pre],inv[post];mask=(a>=0)&(b>=0)&((a>=o.n)|(b>=o.n));self.add_pre=a[mask];self.add_post=b[mask];self.add_count=np.asarray(cnt[mask],dtype=float)
  # Core rows are frozen in their original order; added rows are never new plasticity.
  self.add_base=self.add_count/np.maximum(1,self.full_input[self.add_post])
 def make(self,params=None,seed=None,intervention='intact',target='app',resource=.2,variant='primary'):
  module=self.module;p=params or module.Parameters();o=self.original
  kw={'params':p,'seed':seed or (self.stage*1000+701),'intervention':intervention}
  if self.stage==1:kw['target']=target
  if self.stage==3:kw['resource']=resource
  m=module.Model(o,**kw);m.c=self
  m.r=np.zeros(self.n);m.eligibility=np.zeros(self.n);m.threshold=self.threshold.copy();m.threshold[:o.n]=np.where(o.roles=='KC',p.kc_threshold,0.)
  corew=m.weights.copy();coreden=None
  if variant=='full_normalization' and self.stage==1:
   role=o.roles[o.pre];coreden=np.zeros(len(o.pre))
   for r in sorted(set(role)):
    mask=role==r;dd=np.bincount(o.post[mask],weights=o.count[mask],minlength=o.n);coreden[mask]=dd[o.post[mask]]
   corew*=coreden/np.maximum(1,self.full_input[o.post])
  if variant=='role_normalization' and self.stage!=1:
   role=o.roles[o.pre];dd=np.zeros(len(o.pre))
   for r in sorted(set(role)):
    mask=role==r;d=np.bincount(o.post[mask],weights=o.count[mask],minlength=o.n);dd[mask]=d[o.post[mask]]
   corew*=self.full_input[o.post]/np.maximum(1,dd)
  m.plastic_baseline=corew[m.plastic_edges].copy();corew[m.plastic_edges]=0
  sign=self.sign_hypothesis if variant=='glutamate_inhibitory' else self.sign
  factor={'context_half':.5,'context_double':2.,'context_cut':0.}.get(variant,1.)
  added=self.add_base*sign[self.add_pre]*p.recurrent_gain*factor
  m.fixed=csr_matrix((np.concatenate([corew,added]),(np.concatenate([o.post,self.add_post]),np.concatenate([o.pre,self.add_pre]))),shape=(self.n,self.n))
  if self.stage==1:
   for op in m.da_operators:op.resize((self.n,self.n))
  elif self.stage==2:m.da_operator.resize((self.n,self.n))
  else:m.da.resize((self.n,self.n))
  m.fingerprint=hashlib.sha256((m.fingerprint+self.manifest_hash+variant+hashlib.sha256(m.fixed.data.tobytes()).hexdigest()).encode()).hexdigest()
  # Zero boundary drive; no added source can be relabeled as a teacher or cue.
  m.extension={'variant':variant,'added_neurons':self.n-o.n,'added_neuropil_rows':len(added),'nonzero_added_rows':int(np.count_nonzero(added)),'matrix_bytes':sum(x.nbytes for x in (m.fixed.data,m.fixed.indices,m.fixed.indptr))}
  return m

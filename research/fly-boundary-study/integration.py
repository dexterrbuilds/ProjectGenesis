"""Anatomical integration audit. Paths are not physiological effect estimates."""
import collections,json,hashlib
from pathlib import Path
import numpy as np
from scipy.sparse import load_npz
from context import H,A
nodes=json.loads((A/'nodes.json').read_text());index={a['root_id']:i for i,a in enumerate(nodes)};g=load_npz(A/'contacts.npz');gt=g.T.tocsr();n=g.shape[0]
groups={}
for stage in (1,2,3):
 c=json.loads(next((H.parent/f'fly-stage{stage}'/'artifacts').glob('*/circuit.json')).read_text())
 for k,roots in c['groups'].items():groups[f'S{stage}_{k}']=np.array([index[r] for r in roots])
# Exclude large representation populations from shortest-path labels to prevent
# overlap with sensory/KC pools from masquerading as cross-system coupling.
targets={k:v for k,v in groups.items() if not k.endswith(('_KC','_PN','_APL','_CONTROL','_AMBIGUOUS','_LHCENT'))}
rows=[];pathrows=[]
for a,ai in targets.items():
 for b,bi in targets.items():
  if a==b:continue
  cross=g[ai,:][:,bi];overlap=len(set(ai)&set(bi))
  rows.append({'source':a,'target':b,'contacts':int(cross.sum()),'pairs':cross.nnz,'overlapping_roots':overlap})
  if a[:2]==b[:2] or overlap:continue
  destinations=set(map(int,bi));seen=set(map(int,ai));parents={i:None for i in seen};front=list(seen);found=None
  for depth in range(1,4):
   nxt=[]
   for v in front:
    for u in g.indices[g.indptr[v]:g.indptr[v+1]]:
     u=int(u)
     if u in seen:continue
     seen.add(u);parents[u]=v;nxt.append(u)
     if u in destinations:found=u;break
    if found is not None:break
   if found is not None:break
   front=nxt
  path=[]
  if found is not None:
   v=found
   while v is not None:path.append(v);v=parents[v]
   path=path[::-1]
  pathrows.append({'source':a,'target':b,'length':len(path)-1 if path else None,'one_shortest_path':[nodes[i] for i in path],'contacts_each_step':[int(g[x,y]) for x,y in zip(path,path[1:])],'warning':'Shortest anatomical path up to3 edges, not sign/receptor/functional validation.'})
levels={}
for l in range(5):
 union=np.unique(np.concatenate([np.load(A/f's{s}-L{l}.npy') for s in (1,2,3)]));sub=g[union,:][:,union]
 levels[f'L{l}']={'union_neurons':len(union),'pairs':sub.nnz,'contacts':int(sub.sum())}
# Strong omitted partners are directly reviewable without inventing cell roles.
missing={}
for stage in (1,2,3):
 for l in range(4):
  keep=np.zeros(n,dtype=bool);keep[np.load(A/f's{stage}-L{l}.npy')]=True
  for k,ix in groups.items():
   if not k.startswith(f'S{stage}_') or k.endswith(('_PN','_KC')):continue
   for direction,vec in [('input',np.asarray(g[:,ix].sum(axis=1)).ravel()),('output',np.asarray(g[ix,:].sum(axis=0)).ravel())]:
    ids=np.flatnonzero((~keep)&(vec>0));ii=ids[np.argsort(-vec[ids],kind='stable')[:20]]
    missing[f'{k}_L{l}_{direction}']=[{**nodes[i],'contacts':int(vec[i])} for i in ii]
result={'direct_contacts':rows,'shortest_paths':pathrows,'integrated_union_counts':levels,'strong_omitted_partners':missing,'interpretation':'Anatomical coexistence only. No combined scores and no asserted unified physiology. Original Stage1 MBON07 glutamate->PAM and Stage3 unresolved MBON07 output semantics cannot silently be combined.'}
(H/'INTEGRATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'union':levels,'nonzero_cross_stage_paths':sum(x['length'] is not None for x in pathrows),'direct_nonzero':[x for x in rows if x['contacts'] and x['source'][:2]!=x['target'][:2]]},indent=2))

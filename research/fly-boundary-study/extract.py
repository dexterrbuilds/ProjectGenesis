"""Outcome-blind closure from three frozen seeds; compact pinned anatomy."""
import csv,hashlib,json,time,resource
from pathlib import Path
import numpy as np
import pyarrow.feather as feather
from scipy.sparse import csr_matrix,save_npz
H=Path(__file__).resolve().parent; CACHE=Path('outputs/flywire-research'); OUT=H/'anatomy'
def digest(p,alg='sha256'):
 h=hashlib.new(alg)
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(2**20),b''):h.update(b)
 return h.hexdigest()
def write(p,x):p.write_text(json.dumps(x,sort_keys=True,separators=(',',':'))+'\n')
def main():
 t=time.perf_counter();OUT.mkdir(exist_ok=True)
 expected={'proofread_connections_783.feather':('md5','f48f972d262323a102aed49af1396b8a'),'proofread_root_ids_783.npy':('md5','e0e6c19732fd8c7a4e39a2d170105421'),'annotations-v3.1.0.tsv':('sha256','9a4f8b2f843196074431ebd7cd883536afa1be86c8a4ce90970441e8be81d1be')}
 for f,(alg,h) in expected.items():assert digest(CACHE/f,alg)==h,f
 roots=np.sort(np.load(CACHE/'proofread_root_ids_783.npy'));n=len(roots)
 ann={int(r['root_id']):r for r in csv.DictReader(open(CACHE/'annotations-v3.1.0.tsv'),delimiter='\t')}
 fields=['cell_type','cell_class','super_class','top_nt','known_nt','side','hemibrain_type']
 nodes=[{'root_id':str(int(r)),**{k:ann.get(int(r),{}).get(k,'') for k in fields}} for r in roots]
 write(OUT/'nodes.json',nodes)
 table=feather.read_table(CACHE/'proofread_connections_783.feather',columns=['pre_pt_root_id','post_pt_root_id','syn_count','neuropil'])
 pre=np.searchsorted(roots,table['pre_pt_root_id'].to_numpy().astype(np.uint64)).astype(np.int32);post=np.searchsorted(roots,table['post_pt_root_id'].to_numpy().astype(np.uint64)).astype(np.int32)
 assert np.array_equal(roots[pre],table['pre_pt_root_id'].to_numpy());assert np.array_equal(roots[post],table['post_pt_root_id'].to_numpy())
 cnt=table['syn_count'].to_numpy().astype(np.int32)
 neuropil=table['neuropil'].combine_chunks().dictionary_encode();labels=neuropil.dictionary.to_pylist();neu=neuropil.indices.to_numpy().astype(np.int16)
 del table
 for name,v in [('pre',pre),('post',post),('count',cnt),('neuropil',neu)]:np.save(OUT/(name+'.npy'),v)
 write(OUT/'neuropil-labels.json',labels)
 incoming=np.bincount(post,weights=cnt,minlength=n);outgoing=np.bincount(pre,weights=cnt,minlength=n)
 np.save(OUT/'full_input.npy',incoming);np.save(OUT/'full_output.npy',outgoing)
 graph=csr_matrix((cnt,(pre,post)),shape=(n,n));graph.sum_duplicates();save_npz(OUT/'contacts.npz',graph)
 nt=[]
 for a in nodes:
  if a['cell_class']=='Kenyon_Cell':s=1
  else:
   known=set(x.strip() for x in a['known_nt'].replace(',',';').split(';') if x.strip())
   label=next(iter(known)) if len(known)==1 else (a['top_nt'] if not known else 'ambiguous')
   s=1 if label=='acetylcholine' else (-1 if label=='gaba' else 0)
  nt.append(s)
 np.save(OUT/'sign.npy',np.array(nt,dtype=np.int8))
 region_codes=[i for i,s in enumerate(labels) if s and (s.startswith('MB_') or s in ('CA_L','CA_R','LH_L','LH_R','AL_L','AL_R'))]
 mask=np.isin(neu,region_codes)
 mass=np.bincount(pre[mask],weights=cnt[mask],minlength=n)+np.bincount(post[mask],weights=cnt[mask],minlength=n)
 frac=mass/np.maximum(incoming+outgoing,1)
 klass=np.array([a['cell_class'] for a in nodes]);typ=np.array([a['cell_type'] for a in nodes]);sup=np.array([a['super_class'] for a in nodes])
 mod=np.array([a['cell_class']=='DAN' or a['cell_type'] in ('APL','DPM') or a['cell_type'].startswith('OA-') or any(t in a['known_nt'] for t in ('dopamine','serotonin','octopamine')) for a in nodes])
 named=np.isin(klass,['Kenyon_Cell','MBON','DAN','ALPN','ALLN','LHLN'])|np.isin(typ,['APL','DPM','LHCENT1'])
 broad=np.isin(sup,['central','ascending','descending','endocrine'])
 index={a['root_id']:i for i,a in enumerate(nodes)};results={}; selections={}
 for stage in (1,2,3):
  original=next((H.parent/f'fly-stage{stage}'/'artifacts').glob('*/circuit.json'));c=json.loads(original.read_text())
  core=np.array([index[x['root_id']] for x in c['nodes']],dtype=int);m0=np.zeros(n,dtype=bool);m0[core]=True
  groups={k:np.array([index[r] for r in rr]) for k,rr in c['groups'].items()}
  major=np.unique(np.concatenate([v for k,v in groups.items() if k not in ('KC','PN')]))
  l1=m0.copy();reasons={nodes[i]['root_id']:['original'] for i in core}
  def add(ii,why):
   for i in ii:
    l1[i]=True;reasons.setdefault(nodes[i]['root_id'],[]).append(why)
  for g,ids in groups.items():
   if g in ('KC','PN'):continue
   for direction in ('input','output'):
    v=np.asarray(graph[:,ids].sum(axis=1)).ravel() if direction=='input' else np.asarray(graph[ids,:].sum(axis=0)).ravel()
    need=.8*v.sum()-v[l1].sum();candidates=np.flatnonzero((~l1)&(v>0));order=candidates[np.lexsort((candidates,-v[candidates]))]
    if need>0 and len(order):add(order[:np.searchsorted(np.cumsum(v[order]),need)+1],g+'_'+direction+'_80pct')
  inc=np.asarray(graph[:,major].sum(axis=1)).ravel();out=np.asarray(graph[major,:].sum(axis=0)).ravel()
  add(np.flatnonzero((inc>0)&(out>0)),'reciprocal_to_core_target')
  add(np.flatnonzero(mod&((inc+out)>0)),'observed_modulatory_partner')
  connected=(np.asarray(graph[:,l1].sum(axis=1)).ravel()+np.asarray(graph[l1,:].sum(axis=0)).ravel())>0
  l2=l1|(((frac>=.5)|named)&connected);l3=l2|broad
  levels=[m0,l1,l2,l3,np.ones(n,dtype=bool)];results[str(stage)]={}
  for level,sel in enumerate(levels):
   ii=np.flatnonzero(sel);name=f's{stage}-L{level}';np.save(OUT/(name+'.npy'),ii)
   keep=sel[pre]&sel[post];rin=np.bincount(post[keep],weights=cnt[keep],minlength=n);rout=np.bincount(pre[keep],weights=cnt[keep],minlength=n)
   def retention(ids):
    return {'retained_input':int(rin[ids].sum()),'omitted_input':int((incoming-rin)[ids].sum()),'retained_output':int(rout[ids].sum()),'omitted_output':int((outgoing-rout)[ids].sum()),'input_fraction':float(rin[ids].sum()/max(incoming[ids].sum(),1)),'output_fraction':float(rout[ids].sum()/max(outgoing[ids].sum(),1))}
   record={'neurons':len(ii),'directed_pairs':int(graph[ii,:][:,ii].nnz),'neuropil_rows':int(keep.sum()),'contacts':int(cnt[keep].sum()),'boundary':retention(ii),'original_groups':{g:retention(v) for g,v in groups.items()},'zero_fast_sign_neurons':int(np.count_nonzero(np.array(nt)[ii]==0))}
   results[str(stage)][f'L{level}']=record
   selections[name]={'selected_roots':[nodes[i]['root_id'] for i in ii],'selection_reason':('frozen_original','mass_recurrence_modulation','neuropil_or_named_connected','central_brain_classes','all_proofread')[level]}
   print(json.dumps({'stage':stage,'level':level,**{k:record[k] for k in ('neurons','directed_pairs','contacts')}}),flush=True)
  write(OUT/f's{stage}-L1-reasons.json',reasons)
 write(OUT/'selection.json',selections);write(OUT/'counts.json',results)
 meta={'dataset':'adult female FAFB','materialization':783,'annotations':'v3.1.0','neurons':n,'directed_pairs':graph.nnz,'neuropil_rows':len(pre),'contacts':int(cnt.sum()),'source_hashes':{f:digest(CACHE/f) for f in expected},'plan_sha256':digest(H/'PLAN.md'),'extractor_sha256':digest(__file__),'wall_seconds':time.perf_counter()-t,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'missing_annotations':[str(int(r)) for r in roots if int(r) not in ann]}
 write(OUT/'metadata.json',meta)
 write(OUT/'manifest.json',{'files':{p.name:digest(p) for p in sorted(OUT.iterdir()) if p.is_file()}})
 print(json.dumps(meta),flush=True)
if __name__=='__main__':main()

"""Static pinned anatomical audit only. No extraction ownership, simulation or sign assignment."""
from common import *
import numpy as np,time,resource,collections
A=ROOT/'research/fly-boundary-study/anatomy'
def main():
 start=time.perf_counter();nodes=load(A/'nodes.json');idx={n['root_id']:i for i,n in enumerate(nodes)}
 pre=np.load(A/'pre.npy',mmap_mode='r');post=np.load(A/'post.npy',mmap_mode='r');w=np.load(A/'count.npy',mmap_mode='r');npil=np.load(A/'neuropil.npy',mmap_mode='r');labels=load(A/'neuropil-labels.json')
 inp=np.load(A/'full_input.npy');out=np.load(A/'full_output.npy')
 groups={g:[i for i,n in enumerate(nodes) if n['hemibrain_type']==g] for g in ['MBON07','SMP353','SMP354','SMP108']}
 core=[idx[r] for r in ['720575940617302365','720575940608236978']];context=sorted(set(sum(groups.values(),[])))
 selected=np.isin(pre,context)|np.isin(post,context);p=pre[selected];q=post[selected];c=w[selected];loc=npil[selected]
 def describe(i):return dict(nodes[int(i)],full_input_contacts=int(inp[i]),full_output_contacts=int(out[i]))
 def partners(i,incoming):
  m=q==i if incoming else p==i;other=p[m] if incoming else q[m];tot=collections.Counter()
  for j,v in zip(other,c[m]):tot[int(j)]+=int(v)
  return [dict(describe(j),contacts=v) for j,v in tot.most_common(20)]
 sets={}
 for name,ids in [('starting_pair',core),('annotation_candidate_context',context)]:
  both=np.isin(p,ids)&np.isin(q,ids);paircount=len(set(zip(map(int,p[both]),map(int,q[both]))))
  rows=[]
  for i in ids:
   ri=int(c[both&(q==i)].sum());ro=int(c[both&(p==i)].sum())
   rows.append(dict(describe(i),retained_input_contacts=ri,retained_output_contacts=ro,input_retention=ri/int(inp[i]),output_retention=ro/int(out[i]),omitted_input_contacts=int(inp[i])-ri,omitted_output_contacts=int(out[i])-ro))
  sets[name]={'purpose':'Boundary audit denominator, not simulation extraction or functional membership claim','neurons':len(ids),'directed_pairs':paircount,'contacts':int(c[both].sum()),'aggregate_neuropil_rows':int(both.sum()),'roots':rows}
 pairs=[]
 both=np.isin(p,context)&np.isin(q,context)
 for a,b in sorted(set(zip(map(int,p[both]),map(int,q[both])))):
  m=(p==a)&(q==b);n=collections.Counter()
  for k,v in zip(loc[m],c[m]):n[labels[int(k)]]+=int(v)
  pairs.append({'pre':nodes[a]['root_id'],'post':nodes[b]['root_id'],'pre_type':nodes[a]['hemibrain_type'],'post_type':nodes[b]['hemibrain_type'],'contacts':int(c[m].sum()),'neuropils':dict(n),'physiological_sign':None,'receptor':None,'contact_coordinates':None})
 # All anatomically direct descending-class outputs of candidate target populations. No behavioral label assigned.
 targets=groups['SMP353']+groups['SMP354'];desc={i for i,n in enumerate(nodes) if n.get('super_class')=='descending' or n.get('cell_class')=='descending'}
 m=np.isin(p,targets)&np.isin(q,list(desc));dt=collections.Counter()
 for a,b,v in zip(p[m],q[m],c[m]):dt[(int(a),int(b))]+=int(v)
 d=[{'pre':nodes[a]['root_id'],'target':describe(b),'contacts':v,'action_related_function':None,'experimental_crosswalk':None} for (a,b),v in dt.most_common()]
 result={'scope':'Static anatomical existence only; all synapse ownership remains in frozen anatomy','dataset':load(A/'metadata.json'),'source_file_hashes':{f:sha(A/f) for f in ['nodes.json','pre.npy','post.npy','count.npy','neuropil.npy','neuropil-labels.json','full_input.npy','full_output.npy','manifest.json']},'groups':{g:[describe(i) for i in ids] for g,ids in groups.items()},'boundary_sets':sets,'candidate_directed_pairs':pairs,'major_partners':{nodes[i]['root_id']:{'incoming':partners(i,True),'outgoing':partners(i,False)} for i in context},'direct_descending_outputs':d,'descending_scan_definition':'super_class or cell_class exactly descending; no multi-hop route chosen for an effect','functional_membership_unknown':True,'wall_seconds':time.perf_counter()-start,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 write('ANATOMY_AUDIT.json',result)
 print(json.dumps({'sets':{k:{j:v[j] for j in ['neurons','directed_pairs','contacts']} for k,v in sets.items()},'descending_outputs':len(d),'wall_seconds':result['wall_seconds']}))
if __name__=='__main__':main()

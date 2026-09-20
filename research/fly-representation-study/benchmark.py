"""Explicit engineering envelopes on pinned anatomy, NOT physiological predictions."""
import argparse,gc,json,time,resource,platform,hashlib
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix
H=Path(__file__).resolve().parent;A=H.parent/'fly-boundary-study/anatomy'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(context,rep):
 dest=H/'benchmarks'/f'{context}-{rep}';dest.mkdir(parents=True,exist_ok=False)
 start=time.perf_counter();nodes=json.loads((A/'nodes.json').read_text());N=len(nodes)
 if context.startswith('s'):keep=np.load(A/f'{context}-L0.npy')
 elif context=='integrated':keep=np.unique(np.concatenate([np.load(A/f's{s}-L3.npy') for s in (1,2,3)]))
 else:keep=np.arange(N)
 mask=np.zeros(N,bool);mask[keep]=True
 a=np.load(A/'pre.npy',mmap_mode='r');b=np.load(A/'post.npy',mmap_mode='r');nu=np.load(A/'neuropil.npy',mmap_mode='r');cnt=np.load(A/'count.npy',mmap_mode='r')
 sel=mask[a]&mask[b];pre=np.array(a[sel]);post=np.array(b[sel]);region=np.array(nu[sel]);count=np.array(cnt[sel]);del a,b,nu,cnt,sel
 E=len(pre);contacts=int(count.sum());kc=np.array([n['cell_class']=='Kenyon_Cell' for n in nodes]);mb=np.array([n['cell_class']=='MBON' or str(n['cell_type']).startswith('MBON') for n in nodes])
 plastic=np.flatnonzero(kc[pre]&mb[post]).astype(np.int32);P=len(plastic)
 if rep=='R0':
  keys=keep.astype(np.int64);pi=np.searchsorted(keys,pre).astype(np.int32);po=np.searchsorted(keys,post).astype(np.int32)
 else:
  radix=len(json.loads((A/'neuropil-labels.json').read_text()))+1
  pk=pre.astype(np.int64)*radix+region;tk=post.astype(np.int64)*radix+region
  keys=np.unique(np.concatenate([pk,tk]));occupied=np.unique(keys//radix);isolated=np.setdiff1d(keep,occupied)
  keys=np.sort(np.concatenate([keys,isolated.astype(np.int64)*radix+radix-1]))
  pi=np.searchsorted(keys,pk).astype(np.int32);po=np.searchsorted(keys,tk).astype(np.int32);del pk,tk
 M=len(keys);mass=np.bincount(po,weights=count,minlength=M);w=csr_matrix((count.astype(float)/max(1,float(mass.max())),(po,pi)),shape=(M,M));del mass
 # Positive stable engineering signal, neither sensory simulation nor biological trace.
 initial=.01*(1+np.sin(np.arange(M)*.37));fixed=.01*(1+np.cos(np.arange(M)*.19))
 ps=pi[plastic];pt=po[plastic]
 gc.collect();init=time.perf_counter()-start
 def run():
  x=initial.copy();r1=np.zeros(M);r2=np.zeros(M);mod=np.zeros(M);elig=np.zeros(P);eff=np.ones(P)
  wall=time.perf_counter();cpu=time.process_time()
  for _ in range(100):
   drive=w@x
   if rep=='R2':
    # Fixed generic arithmetic workload, no receptor localization/learning claim.
    r1=.9*r1+.1*drive;r2=.95*r2+.05*drive;mod=.98*mod+.02*x
    elig=.95*elig+.05*x[ps];eff*=np.exp(-1e-4*elig*mod[pt]);drive+=.01*(r1-r2)
    drive+=np.bincount(pt,weights=1e-3*(eff-1)*x[ps],minlength=M)
   x=.9*x+.1*(drive+fixed)
  used=time.process_time()-cpu;elapsed=time.perf_counter()-wall
  state={'x':x}
  if rep=='R2':state.update(receptor1=r1,receptor2=r2,modulator=mod,eligibility=elig,efficacy=eff)
  return state,elapsed,used
 state,wall,cpu=run();again,replaywall,_=run();exact=all(np.array_equal(v,again[k]) for k,v in state.items())
 stamp=time.perf_counter();np.savez(dest/'checkpoint.npz',**state);write=time.perf_counter()-stamp
 stamp=time.perf_counter()
 with np.load(dest/'checkpoint.npz') as z:assert all(np.array_equal(v,z[k]) for k,v in state.items())
 read=time.perf_counter()-stamp
 # Arrays retained by this implementation; excludes transient NumPy temporaries/Python metadata.
 arrays=[pre,post,region,count,keys,pi,po,plastic,ps,pt,initial,fixed,w.data,w.indices,w.indptr,*state.values()]
 result={'context':context,'envelope':rep,'biological_model':False,'roots':len(keep),'local_states':M,'anatomical_rows':E,'contacts':contacts,
  'csr_entries':int(w.nnz),'candidate_plastic_rows':P,'initialization_seconds':init,'updates':100,'wall_seconds':wall,'cpu_seconds':cpu,
  'cpu_percent_one_core':100*cpu/wall,'updates_per_second':100/wall,'replay_seconds':replaywall,'replay_exact':exact,
  'persistent_state_bytes':sum(v.nbytes for v in state.values()),'explicit_resident_array_bytes':sum(v.nbytes for v in arrays),
  'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'checkpoint_bytes':(dest/'checkpoint.npz').stat().st_size,
  'checkpoint_write_seconds':write,'checkpoint_load_seconds':read,'all_finite':all(bool(np.isfinite(v).all()) for v in state.values()),
  'simulated_per_wall_if_dt_seconds':{str(dt):100*dt/wall for dt in [.01,.001,.0001]},
  'platform':platform.platform(),'numpy':np.__version__,'specification_sha256':digest(H/'REPRESENTATIONS.md'),'code_sha256':digest(H/'benchmark.py'),
  'anatomy_manifest_sha256':digest(A/'manifest.json'),'warning':'Engineering stable workload only. No calibrated kinetics, voltage, receptor map, anatomical intracellular coupling, or R3 throughput claim.'}
 (dest/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--context',choices=['s1','s2','s3','integrated','full'],required=True);p.add_argument('--rep',choices=['R0','R1','R2'],required=True);a=p.parse_args();main(a.context,a.rep)

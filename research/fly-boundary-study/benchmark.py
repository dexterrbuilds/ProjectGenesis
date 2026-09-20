"""Full-brain conservative rate reference. All neurons updated on every step."""
import argparse,hashlib,json,time,resource,os,platform
from pathlib import Path
import numpy as np
from scipy.sparse import load_npz,diags
H=Path(__file__).resolve().parent;A=H/'anatomy'
def main(dt):
 start=time.perf_counter();cpu=time.process_time()
 g=load_npz(A/'contacts.npz').astype(np.float64);sg=np.load(A/'sign.npy');den=np.maximum(1,np.load(A/'full_input.npy'))
 w=(diags(1/den)@g.T@diags(sg*.05)).tocsr();del g
 nodes=json.loads((A/'nodes.json').read_text());n=len(nodes)
 threshold=np.array([.15 if a['cell_class']=='Kenyon_Cell' else 0 for a in nodes]);pn=np.array([i for i,a in enumerate(nodes) if a['cell_class']=='ALPN'])
 ix=np.random.Generator(np.random.PCG64(4701)).choice(pn,16,replace=False);current=np.zeros(n);current[ix]=1
 init=time.perf_counter()-start;initial=np.zeros(n)
 def run():
  r=initial.copy();trace=[];wall=time.perf_counter();cp=time.process_time()
  for k in range(round(10/dt)):
   drive=w@r
   if k*dt<5:drive+=current
   desired=np.clip(drive-threshold,0,1);r+=dt/.05*(desired-r)
   if k%round(.1/dt)==0:trace.append([k*dt,float(r.max()),float(np.mean(r)),int(np.count_nonzero(r>1e-8))])
  return r,np.array(trace),time.perf_counter()-wall,time.process_time()-cp
 r,tr,wall,used=run();dest=H/'benchmarks'/f'dt-{dt}';dest.mkdir(parents=True,exist_ok=False)
 save=time.perf_counter();np.savez(dest/'checkpoint.npz',rates=r,clock=np.array(round(10/dt)),dt=np.array(dt),source_hash=np.array(hashlib.sha256((A/'manifest.json').read_bytes()).hexdigest()));save=time.perf_counter()-save
 load=time.perf_counter();q=np.load(dest/'checkpoint.npz');assert np.array_equal(q['rates'],r);load=time.perf_counter()-load
 rr,tt,replaywall,replaycpu=run();assert np.array_equal(r,rr) and np.array_equal(tr,tt)
 np.savez_compressed(dest/'trace.npz',trace=tr,sensory_indices=ix,final_rates=r)
 result={'dt':dt,'neurons':n,'anatomical_directed_pairs':int(json.loads((A/'metadata.json').read_text())['directed_pairs']),'csr_stored_entries':w.nnz,'csr_bytes':sum(a.nbytes for a in (w.data,w.indices,w.indptr)),'initialization_seconds':init,'simulated_seconds':10,'wall_seconds':wall,'cpu_seconds':used,'cpu_percent_one_core':100*used/wall,'updates_per_second':round(10/dt)/wall,'simulated_per_wall':10/wall,'checkpoint_bytes':(dest/'checkpoint.npz').stat().st_size,'checkpoint_write_seconds':save,'checkpoint_load_seconds':load,'replay_wall_seconds':replaywall,'replay_exact':True,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'max_rate':float(tr[:,1].max()),'final_mean_rate':float(r.mean()),'finite':bool(np.all(np.isfinite(r))),'platform':platform.platform(),'cpu_count':os.cpu_count(),'numpy':np.__version__,'whole_process_cpu_seconds':time.process_time()-cpu,'whole_process_wall_seconds':time.perf_counter()-start,'interpretation':'Engineering reference only; no behavioral labels for context; no plasticity in this generic benchmark.'}
 (dest/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--dt',type=float,required=True);main(p.parse_args().dt)

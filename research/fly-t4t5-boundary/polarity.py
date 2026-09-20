from common import *
import numpy as np,itertools,time,resource
sys.path.insert(0,str(HERE/'vendor'))
import h5py

def scalar(f,r,idx):
 z=f[r[idx]]
 if z.attrs.get('MATLAB_empty',False):return None
 v=z[()].ravel();return float(v[0]) if len(v)==1 else None

def main(kind):
 start=time.perf_counter();path=HERE/f'data/wholecell/singleBarSt{kind}.mat';f=h5py.File(path,'r');root=f['singleBarSt'+kind];rows=[];traces={};audit=[]
 for c in range(root['result'].shape[0]):
  cell=c+1;r=f[root['result'][c,0]]
  pars={k:f[root[k][c,0]][()].ravel() for k in ['positions','durations','widths','vals']}
  if kind=='T4' and cell==5:
   audit.append({'cell':cell,'excluded':'author Figure2Code.m excludes ordinal 5; do not silently substitute it','positions':pars['positions'].tolist()});continue
  summary=tuple(n-1 for n in r['empty'].shape);center=scalar(f,r['maxExtPosVal'],summary);inhib=scalar(f,r['minInhPosVal'],summary);direction=float(np.sign(inhib-center)) if center is not None and inhib is not None else None
  count=0
  for vi,wi,di,pi in itertools.product(range(len(pars['vals'])),range(len(pars['widths'])),range(len(pars['durations'])),range(len(pars['positions']))):
   fullidx=(vi,wi,di,pi);nd=r['empty'].ndim;assert all(j==0 for j in fullidx[:4-nd]);idx=fullidx[4-nd:];empty=scalar(f,r['empty'],idx)
   if empty is None or empty:continue
   sub=f[r['subData'][idx]];y=sub['baseSub'][1,:];zero=int(sub['zeroInd'][0,0])-1;t=(np.arange(len(y))-zero)/20
   dur=float(pars['durations'][di])*1000;on=(t>=0)&(t<dur+75);pre=(t>=-100)&(t<0);assert np.any(on) and np.any(pre)
   raw=f[r['data'][idx]];reps=int(raw['numReps'][0,0]) if 'numReps' in raw else None;pos=float(pars['positions'][pi]);width=float(pars['widths'][wi]);polarity=float(pars['vals'][vi]);rel=(pos-center if direction==1 else pos-center-width+1)*direction if direction is not None else None
   key=f'c{cell}_v{vi}_w{wi}_d{di}_p{pi}';times=np.arange(-100,601);ix=zero+20*times;valid=(ix>=0)&(ix<len(y));trace=np.full(len(times),np.nan);trace[valid]=y[ix[valid]];traces[key]=trace
   rows.append({'key':key,'cell':cell,'fly_id':None,'type':kind,'position_source':pos,'position_author_centered':rel,'width_pixels':width,'duration_ms':dur,'contrast_value':polarity,'num_repeats_source':reps,'mean_mV':float(y[on].mean()),'min_mV':float(y[on].min()),'max_mV':float(y[on].max()),'prestim_rms_mV':float(np.sqrt(np.mean(y[pre]**2)))})
   count+=1
  audit.append({'cell':cell,'n_traces':count,'author_center':center,'author_inhibition_side':inhib,'author_axis_sign':direction,'fly_id':None,'top_level_fly_metadata':False})
 f.close();np.savez_compressed(HERE/f'{kind}_POLARITY_TRACES.npz',time_ms=np.arange(-100,601),**traces)
 write(f'{kind}_POLARITY_MEASUREMENTS.json',{'source_member_sha256':sha(path),'units':'baseline-subtracted somatic mV','raw_sample_rate_Hz':20000,'saved_trace_interval_ms':1,'rows':rows,'cells':audit,'model_fitting':False})
 write(f'{kind}_POLARITY_PERFORMANCE.json',{'wall_seconds':time.perf_counter()-start,'peak_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'traces':len(rows)})
 print(json.dumps({'type':kind,'cells':len(audit),'traces':len(rows)}))
if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else 'T4')

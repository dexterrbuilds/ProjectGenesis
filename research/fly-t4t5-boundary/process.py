"""Original author voltage observations; never simulated author model outputs."""
from common import *
import numpy as np
from scipy.io import loadmat
FAMILY={0:'flash',3:'moving_bar',4:'apparent_motion',1:'drifting_grating',2:'static_grating'}
SUFFIX={0:'sb',3:'mb',4:'mm',1:'mg',2:'sg'}

def occupancy(p,code,k,t):
 x=np.asarray(p['xx'],dtype=int);s=np.zeros((len(t),len(x)),dtype=np.float64)
 def pulse(loc,w,on,off):
  s[np.ix_((t>=on)&(t<off),np.isin(x,np.arange(int(loc)-int(w)+1,int(loc)+1)))]=1
 if code==0:pulse(p['location_sb'][k],p['width_sb'][k],0,p['duration_sb'][k])
 elif code==4:
  pulse(p['fb_pos_mm'][k],p['width_mm'][k],p['fbton_mm'],p['fbtoff_mm'][k])
  pulse(p['sb_pos_mm'][k],p['width_mm'][k],p['sbton_mm'][k],p['sbtoff_mm'][k])
 elif code==3:
  pos=np.asarray(p['pos_mb'],dtype=int);w=int(p['width_mb'][k]);dur=float(p['duration_mb'][k]);di=int(p['direction_mb'][k])
  # Each pixel is illuminated for width consecutive frame intervals, including edge entry/exit.
  order=pos if di==1 else pos[::-1]
  for j,loc in enumerate(order):pulse(loc,1,j*dur,(j+w)*dur)
 elif code==2:
  s[np.ix_((t>=0)&(t<float(p['stimdur_sg'][k])),np.isin(x,p['posD_sg'][k]))]=1
 elif code==1:
  dur=float(p['stimdur_mg'][k]);phase=np.asarray(p['phase_mg'][k],dtype=int)
  for j in range(25):
   # Authors' supplied stimulus operator uses indices 0 through 24 inclusive.
   s[np.ix_((t>=j*dur)&(t<(j+1)*dur),np.isin(x,p['PosD_mg'][phase[j%8]-1]))]=1
 else:raise ValueError(code)
 return s

def records(p,d):
 counters={k:0 for k in FAMILY};out=[]
 for j,code in enumerate(p['protocol']):
  code=int(code);k=counters[code];counters[code]+=1;suf=SUFFIX[code]
  t=np.asarray(p['t'][j],float);a=int(d['ind_ref1_'+suf][k])-1;b=int(d['ind_ref2_'+suf][k]);y=np.asarray(d['vm_all_'+suf][a:b],float)
  assert len(y)==len(t) and np.all(np.isfinite(y)) and np.allclose(np.diff(t),np.diff(t)[0],atol=1e-8)
  w=int(p['width_'+suf][k]) if 'width_'+suf in p else -1
  dur=float(p.get('duration_'+suf,p.get('stimdur_'+suf))[k])
  meta={'recording':None,'family':FAMILY[code],'index':j,'width_pixels':w,'duration_ms':dur,'direction_code':int(p['direction_mb'][k]) if code==3 else None,'sample_interval_ms':float(np.diff(t)[0]),'fly_id':None,'type':'T5','subtype':None}
  out.append((t,y,occupancy(p,code,k,t),meta))
 return out

def save_records(path,rr):
 n=[len(r[0]) for r in rr];ends=np.cumsum(n);starts=ends-n
 np.savez_compressed(path,t_ms=np.concatenate([r[0] for r in rr]),voltage_mV=np.concatenate([r[1] for r in rr]),off_occupancy=np.concatenate([r[2] for r in rr]).astype('float32'),starts=starts,ends=ends,metadata=np.array(json.dumps([r[3] for r in rr])),x_pixels=np.arange(-13,14))

def main():
 log=firewall('process');out=HERE/'processed';out.mkdir(exist_ok=True);audit=[];partition=[]
 for cell in range(1,18):
  f=HERE/f'data/t5-compact/data_cell_{cell}_all.mat';m=loadmat(f,simplify_cells=True);rr=records(m['p'],m['d'])
  for r in rr:r[3]['recording']=cell
  train=[r for r in rr if r[3]['family']=='flash' and r[3]['width_pixels']==2];test=[r for r in rr if not(r[3]['family']=='flash' and r[3]['width_pixels']==2)]
  for split,data in [('train',train),('test',test)]:
   dest=out/f'cell_{cell:02d}_{split}.npz';save_records(dest,data);partition.append({'recording':cell,'fly_id':None,'split':split,'path':str(dest.relative_to(HERE)),'sha256':sha(dest),'traces':len(data),'samples':sum(len(r[0]) for r in data),'families':{key:sum(r[3]['family']==key for r in data) for key in set(r[3]['family'] for r in data)}})
  audit.append({'recording':cell,'source_sha256':sha(f),'families':{v:sum(r[3]['family']==v for r in rr) for v in FAMILY.values()},'voltage_range_mV':[float(min(np.min(r[1]) for r in rr)),float(max(np.max(r[1]) for r in rr))],'sample_intervals_ms':[2.5,5],'raw_trials_available':False,'fly_id':None,'global_screen_frame':None})
 write('MEASUREMENTS.json',{'source':'Gruntman et al 2019 original experimental model-input arrays','units':'baseline-subtracted somatic mV','records':audit,'not_independent_replication_of_2021_T5':True,'authors_trial_averages':True})
 write('PARTITIONS.json',{'fly_held_out_possible':False,'conditional_author_localization':True,'entries':partition})
 write('PROCESS_ACCESS.json',sorted(set(log)))
 print(json.dumps({'recordings':len(audit),'traces':sum(x['traces'] for x in partition),'samples':sum(x['samples'] for x in partition)}))
if __name__=='__main__':main()

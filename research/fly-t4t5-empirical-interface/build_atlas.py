"""Read direct measurements only; no prior fitted models/results or Stage-4 code."""
from common import *
import numpy as np
from scipy.io import loadmat
import collections,time
T=np.arange(501,dtype=float)
FAMILIES={3:'moving_bar',4:'apparent_motion',1:'drifting_grating',2:'static_grating'}
SUFFIX={3:'mb',4:'mm',1:'mg',2:'sg'}
def js(x):
 if isinstance(x,np.ndarray):return [js(v) for v in x]
 if isinstance(x,np.generic):return x.item()
 return x

def main():
 start=time.perf_counter();rows=[];waves=[];sources={};excluded=0
 def add(row,y):
  assert y.shape==(501,) and np.isfinite(y).all()
  row['id']=len(rows);row['units']='mV';row['observation']='mean_baseline_subtracted_somatic_voltage';row['fly_id']=None;row['subtype']=None;row['FlyWire_root']=None;row['column']=None
  rows.append(row);waves.append(y)
 for typ in ['T4','T5']:
  meta=PREV/f'{typ}_POLARITY_MEASUREMENTS.json';tr=PREV/f'{typ}_POLARITY_TRACES.npz';sources[str(meta.relative_to(ROOT))]=sha(meta);sources[str(tr.relative_to(ROOT))]=sha(tr)
  mm=json.loads(meta.read_text())
  with np.load(tr,allow_pickle=False) as z:
   idx=np.where((z['time_ms']>=0)&(z['time_ms']<=500))[0]
   for r in mm['rows']:
    if r['position_author_centered'] is None:excluded+=1;continue
    y=z[r['key']][idx]
    if not np.isfinite(y).all():excluded+=1;continue
    add({'dataset':f'2021_{typ}_flash','recording':f'2021_{typ}_{r["cell"]:02d}','recording_ordinal':r['cell'],'type':typ,'family':'flash','frame':f'2021_{typ}_author_RF_axis','polarity':r['contrast_value'],'width':r['width_pixels'],'duration':r['duration_ms'],'offset':r['position_author_centered'],'source_position':r['position_source'],'source_trace_key':r['key'],'source_repeat_count':r['num_repeats_source'],'direction_label':None,'descriptor':{'offset_pixels':r['position_author_centered'],'width_pixels':r['width_pixels'],'duration_ms':r['duration_ms'],'contrast_value':r['contrast_value']}},y)
 for c in range(1,18):
  file=PREV/f'data/t5-compact/data_cell_{c}_all.mat';sources[str(file.relative_to(ROOT))]=sha(file);m=loadmat(file,simplify_cells=True);p,d=m['p'],m['d'];counter=collections.Counter()
  for i,code in enumerate(p['protocol']):
   code=int(code)
   if code==0:excluded+=1;continue # reused flash observations are not independent additions
   k=counter[code];counter[code]+=1;suf=SUFFIX[code];t=np.asarray(p['t'][i],float);a=int(d['ind_ref1_'+suf][k])-1;b=int(d['ind_ref2_'+suf][k]);y=np.asarray(d['vm_all_'+suf][a:b],float)
   assert len(t)==len(y) and t[0]<=0 and t[-1]>=500
   if code==3:
    desc={key:js(p[key][k]) for key in ['width_mb','duration_mb','direction_mb']};desc['positions_pixels']=js(p['pos_mb']);desc['source_pixel_steps_per_second']=1000/float(p['duration_mb'][k]);width=int(p['width_mb'][k]);dur=float(p['duration_mb'][k])
   elif code==4:
    desc={key:js(p[key][k]) for key in ['fb_pos_mm','sb_pos_mm','width_mm','fbtoff_mm','sbton_mm','sbtoff_mm','duration_mm','speedCor_mm','timeDiff_mm']};desc['fbton_mm']=js(p['fbton_mm']);desc['displacement_pixels']=float(p['sb_pos_mm'][k])-float(p['fb_pos_mm'][k]);width=int(p['width_mm'][k]);dur=float(p['duration_mm'][k])
   elif code==1:
    desc={'step_duration_ms':float(p['stimdur_mg'][k]),'phase_sequence':js(p['phase_mg'][k]),'dark_pixel_patterns':js(p['PosD_mg']),'source_operator_frame_indices':[0,24]};width=None;dur=float(p['stimdur_mg'][k])
   else:
    desc={'duration_ms':float(p['stimdur_sg'][k]),'dark_pixel_positions':js(p['posD_sg'][k])};width=None;dur=float(p['stimdur_sg'][k])
   add({'dataset':'2019_T5_compact','recording':f'2019_T5_{c:02d}','recording_ordinal':c,'type':'T5','family':FAMILIES[code],'frame':'2019_T5_author_PD_axis','polarity':0,'width':width,'duration':dur,'offset':None,'source_position':None,'source_trace_key':f'protocol_index_{i}','source_repeat_count':None,'direction_label':None,'descriptor':desc},np.interp(T,t,y))
 np.savez_compressed(HERE/'atlas/waveforms.npz',time_ms=T,voltage_mV=np.asarray(waves))
 write('atlas/records.json',rows);write('SOURCE_INPUTS.json',sources)
 groups=[]
 for key in sorted(set((r['dataset'],r['type'],r['family']) for r in rows)):
  rr=[r for r in rows if (r['dataset'],r['type'],r['family'])==key];descs=collections.Counter(json.dumps(r['descriptor'],sort_keys=True) for r in rr)
  dims={}
  for dkey in sorted(set(k for r in rr for k in r['descriptor'])):
   vals=[r['descriptor'][dkey] for r in rr if dkey in r['descriptor']];u=sorted(set(json.dumps(x,sort_keys=True) for x in vals));dims[dkey]={'unique_values':[json.loads(x) for x in u],'n_unique':len(u)}
  groups.append({'dataset':key[0],'type':key[1],'family':key[2],'records':len(rr),'recordings':len(set(r['recording'] for r in rr)),'unique_descriptor_tuples':len(descs),'tuple_recording_count_range':[min(descs.values()),max(descs.values())],'dimensions':dims,'subtype':None,'fly':None,'root_transfer':False})
 write('COVERAGE_ATLAS.json',{'groups':groups,'waveform_time_ms':[0,500],'step_ms':1,'records':len(rows),'excluded_duplicate_or_invalid_records':excluded,'marginal_ranges_are_not_joint_coverage':True,'all_voltage_only':True,'source_centered_localization_is_conditional':True})
 write('BUILD_PERFORMANCE.json',{'wall_seconds':time.perf_counter()-start,'waveform_bytes':(HERE/'atlas/waveforms.npz').stat().st_size,'values':int(np.asarray(waves).size)})
 print(json.dumps([{k:v for k,v in x.items() if k!='dimensions'} for x in groups],indent=2))
if __name__=='__main__':main()

from common import *
from models import *
import time,resource

def main():
 start=time.perf_counter();access=firewall('evaluate');freeze=json.loads((HERE/'FIT_FREEZE.json').read_text());assert sha(HERE/'FITS.json')==freeze['fits_sha256'] and sha(HERE/'models.py')==freeze['model_sha256']
 fits=json.loads((HERE/'FITS.json').read_text())['fits'];rows=[];preds={};descriptive=[]
 for f in fits:
  cell=f['recording'];d=load(HERE/f'processed/cell_{cell:02d}_test.npz')
  for kind,fit in {**f['candidate_fits'],'SELECTED':f['selected']}.items():
   X=features(d,**{k:fit[k] for k in ['kind','tau','delay','gamma']});yp=X@np.array(fit['coefs']);preds[f'cell{cell}_{kind}']=yp
   for a,b,m in zip(d['starts'],d['ends'],d['metadata']):
    y=d['voltage_mV'][a:b];pp=yp[a:b];err=pp-y
    rows.append({'recording':cell,'family':m['family'],'trace_index':m['index'],'width_pixels':m['width_pixels'],'duration_ms':m['duration_ms'],'direction_code':m['direction_code'],'candidate':kind,'selected_kind':fit['kind'],'mse_mV2':float(np.mean(err**2)),'mae_mV':float(np.mean(abs(err))),'measured_peak_mV':float(np.max(y)),'predicted_peak_mV':float(np.max(pp)),'measured_min_mV':float(np.min(y)),'predicted_min_mV':float(np.min(pp)),'mean_error_mV':float(err.mean())})
  # Independent measurements, not model labels; both directions kept as supplied codes.
  for fam in sorted(set(x['family'] for x in d['metadata'])):
   selected=[x for x in rows if x['recording']==cell and x['family']==fam and x['candidate']=='SELECTED']
   descriptive.append({'recording':cell,'family':fam,'traces':len(selected),'observed_mean_peak_mV':float(np.mean([x['measured_peak_mV'] for x in selected])),'observed_mean_min_mV':float(np.mean([x['measured_min_mV'] for x in selected]))})
 aggregate=[]
 for family in sorted(set(x['family'] for x in rows)):
  for kind in ['Z','B0','B1s','B1t','B1d','SELECTED']:
   per=[]
   for cell in range(1,18):
    rr=[x for x in rows if x['recording']==cell and x['family']==family and x['candidate']==kind]
    if rr:per.append({'recording':cell,'rmse_mV':float(np.sqrt(np.mean([x['mse_mV2'] for x in rr]))),'mae_mV':float(np.mean([x['mae_mV'] for x in rr]))})
   vals=[x['rmse_mV'] for x in per];aggregate.append({'family':family,'candidate':kind,'n_recordings':len(per),'median_rmse_mV':float(np.median(vals)),'range_rmse_mV':[min(vals),max(vals)],'per_recording':per})
 write('TEST_TRACE_METRICS.json',rows);write('RESULTS.json',{'scope':'conditional within-recording family-held-out voltage; fly independence unverified','freeze_sha256':sha(HERE/'FIT_FREEZE.json'),'aggregate':aggregate,'measured_response_summary':descriptive,'no_general_boundary_selected':True})
 np.savez_compressed(HERE/'PREDICTIONS.npz',**preds)
 write('EVALUATION_PERFORMANCE.json',{'wall_seconds':time.perf_counter()-start,'peak_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'prediction_bytes':(HERE/'PREDICTIONS.npz').stat().st_size})
 write('EVALUATE_ACCESS.json',sorted(set(access)))
 print(json.dumps([{k:v for k,v in x.items() if k not in ['per_recording','range_rmse_mV']} for x in aggregate if x['candidate'] in ['Z','SELECTED']],indent=2))
if __name__=='__main__':main()

from common import *
import numpy as np,collections,csv
fits=json.loads((HERE/'FITS.json').read_text())['fits'];res=json.loads((HERE/'RESULTS.json').read_text())['aggregate'];r=[]
for f in fits:
 s=f['selected'];fold=np.asarray(s['fold_coefficients']);r.append({'recording':f['recording'],'selected':s['kind'],'effective_dof':s['effective_dof'],'raw_coefficients':s['raw_coefficients'],'rank':s['rank'],'condition_positive_subspace':s['condition_positive_subspace'],'tau_ms':s['tau'],'delay_ms':s['delay'],'gamma':s['gamma'],'lambda':s['lambda'],'max_coefficient_fold_range':float(np.max(np.ptp(fold,axis=0))) if fold.size else 0,'competitive_ranges':f['competitive_ranges']})
write('IDENTIFIABILITY.json',{'scope':'predictive coefficients only; physiological conductances/receptor maps not identified','selected_counts':dict(collections.Counter(x['selected'] for x in r)),'records':r,'unidentified':['fly grouping','global coordinate transform','T4 parameters','ON contrast response of fitted T5 model','calcium/spike observation mappings','precursor identities','conductance/receptor signs','parameters beyond preregistered discrete grid'],'no_time_sample_confidence_intervals':True})
with (HERE/'PREDICTIVE_RESULTS.csv').open('w') as out:
 w=csv.DictWriter(out,fieldnames=['family','candidate','n_recordings','median_rmse_mV','min_rmse_mV','max_rmse_mV']);w.writeheader()
 for x in res:w.writerow({**{k:x[k] for k in ['family','candidate','n_recordings','median_rmse_mV']},'min_rmse_mV':x['range_rmse_mV'][0],'max_rmse_mV':x['range_rmse_mV'][1]})
for kind in ['T4','T5']:
 p=HERE/f'{kind}_POLARITY_MEASUREMENTS.json'
 if not p.exists():continue
 d=json.loads(p.read_text());summary=[]
 for width in [1,2,4]:
  for dur in [40,160]:
   for v in [0,1]:
    rows=[x for x in d['rows'] if x['position_author_centered']==0 and x['width_pixels']==width and x['duration_ms']==dur and x['contrast_value']==v]
    if rows:summary.append({'width_pixels':width,'duration_ms':dur,'contrast_value':v,'n_recordings':len(rows),**{k:float(np.median([x[k] for x in rows])) for k in ['mean_mV','min_mV','max_mV','prestim_rms_mV']}})
 write(f'{kind}_POLARITY_SUMMARY.json',{'conditional_author_center':True,'no_inferential_test_of_extrema':True,'summary':summary})
print(json.dumps({'selected_counts':dict(collections.Counter(x['selected'] for x in r)),'table':[{k:v for k,v in x.items() if k not in ['per_recording','range_rmse_mV']} for x in res]},indent=2))

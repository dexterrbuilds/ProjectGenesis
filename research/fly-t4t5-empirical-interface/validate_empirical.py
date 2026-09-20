from common import *
from empirical import *
import collections,time,resource,math

def bootstrap_ci(vals,rng):
 a=np.asarray(vals,float);b=rng.integers(0,len(a),(2000,len(a)));return np.quantile(a[b].mean(1),[.025,.975]).tolist()
def summarize(preds,all_strata):
 rng=np.random.default_rng(20260919);stats=[];envelopes=[]
 for st in sorted(all_strata):
  rr=[x for x in preds if x['stratum']==st];rec=sorted(set(r['recording'] for r in rr));recordmeans=[]
  for key in rec:
   xx=[x for x in rr if x['recording']==key];recordmeans.append({'recording':key,'conditions':len(xx),**{k:float(np.mean([x[k] for x in xx])) for k in ['mse','reference_mse','zero_mse']},'max_waveform_error':max(x['max_abs_error'] for x in xx)})
  support=len(rec)>=5 and len(rr)>=20;ci=bootstrap_ci([x['mse']-x['reference_mse'] for x in recordmeans],rng) if support else None;cz=bootstrap_ci([x['mse']-x['zero_mse'] for x in recordmeans],rng) if support else None
  passed=bool(support and ci[1]<0 and cz[1]<0)
  for x in recordmeans:
   calib=sorted(y['max_waveform_error'] for y in recordmeans if y['recording']!=x['recording']);rank=math.ceil(.9*(len(calib)+1));band=calib[rank-1] if rank<=len(calib) else None
   envelopes.append({'stratum':st,'recording':x['recording'],'calibration_recordings':len(calib),'rank':rank,'half_width_mV':band,'simultaneous_condition_waveform_coverage':x['max_waveform_error']<=band if band is not None else None})
  stats.append({'stratum':st,'recordings':len(rec),'conditions':len(rr),'paired_difference_ci95_mV2':ci,'difference_from_zero_ci95_mV2':cz,'meets_registered_criteria':passed,'median_recording_RMSE_mV':float(np.median([np.sqrt(x['mse']) for x in recordmeans])) if rec else None,'median_reference_RMSE_mV':float(np.median([np.sqrt(x['reference_mse']) for x in recordmeans])) if rec else None,'median_zero_RMSE_mV':float(np.median([np.sqrt(x['zero_mse']) for x in recordmeans])) if rec else None,'by_recording':recordmeans})
 return stats,envelopes

def main():
 start=time.perf_counter();access=firewall();rows=read('atlas/records.json');Y=np.load(HERE/'atlas/waveforms.npz')['voltage_mV'];preds=[];coverage=[];strata=set();tracepred=[];predids=[]
 for axis in ['offset','duration']:
  groups=collections.defaultdict(list)
  for r in rows:
   if r['family']=='flash':groups[interp_group(r,axis)].append(r);strata.add(interp_stratum(r,axis))
  for group in groups.values():
   for r in group:
    other=[x for x in group if x[axis]!=r[axis]];out=interpolate(r,other,axis,Y);st=interp_stratum(r,axis)
    if out is None or out.get('linear') is None:
     coverage.append({'test':'value_holdout','id':r['id'],'stratum':st,'predicted':False,'reason':out['reason'] if out else 'no_other_condition'});continue
    e=errors(Y[r['id']],out['linear']);ref=errors(Y[r['id']],out['nearest']);preds.append({'test':'value_holdout','id':r['id'],'stratum':st,'recording':r['recording'],**e,'reference_mse':ref['mse'],'zero_mse':float(np.mean(Y[r['id']]**2)),'bracket':out['bracket'],'weight':out['weight'],'training_ids':out['sources']});coverage.append({'test':'value_holdout','id':r['id'],'stratum':st,'predicted':True});tracepred.append(out['linear']);predids.append(len(preds)-1)
 # Recording-held-out exact template and recording-balanced reference.
 exact=collections.defaultdict(list);family=collections.defaultdict(list)
 for r in rows:
  exact[descriptor_key(r)].append(r)
  key=(r['dataset'],r['type'],r['family'],r['polarity'],r['width'] if r['family']=='flash' else None,r['duration'] if r['family']=='flash' else None);family[key].append(r);strata.add(template_stratum(r))
 for r in rows:
  st=template_stratum(r);other=[x for x in exact[descriptor_key(r)] if x['recording']!=r['recording']];recordings=sorted(set(x['recording'] for x in other))
  if len(recordings)<3:
   coverage.append({'test':'recording_holdout','id':r['id'],'stratum':st,'predicted':False,'reason':'fewer_than_three_exact_other_recordings'});continue
  pred=np.mean([Y[[x['id'] for x in other if x['recording']==k]].mean(0) for k in recordings],axis=0)
  key=(r['dataset'],r['type'],r['family'],r['polarity'],r['width'] if r['family']=='flash' else None,r['duration'] if r['family']=='flash' else None);pool=[x for x in family[key] if x['recording']!=r['recording']];recs=sorted(set(x['recording'] for x in pool));ref=np.mean([Y[[x['id'] for x in pool if x['recording']==k]].mean(0) for k in recs],axis=0)
  preds.append({'test':'recording_holdout','id':r['id'],'stratum':st,'recording':r['recording'],**errors(Y[r['id']],pred),'reference_mse':errors(Y[r['id']],ref)['mse'],'zero_mse':float(np.mean(Y[r['id']]**2)),'training_ids':[x['id'] for x in other]});coverage.append({'test':'recording_holdout','id':r['id'],'stratum':st,'predicted':True});tracepred.append(pred);predids.append(len(preds)-1)
 stats,env=summarize(preds,strata)
 write('PREDICTION_METRICS.json',preds);write('HOLDOUT_COVERAGE.json',coverage);write('VALIDATION_RESULTS.json',{'strata':stats,'bootstrap_seed':20260919,'bootstrap_replicates':2000,'conditional_recording_not_fly_inference':True,'multiple_testing':'per-stratum intervals; no familywise biological claim'})
 write('UNCERTAINTY.json',{'nominal_rank_level':.9,'unit':'maximum absolute waveform residual over held-out conditions per recording','exchangeability_guarantee':False,'envelopes':env})
 np.savez_compressed(HERE/'HELDOUT_PREDICTIONS.npz',prediction_indices=np.array(predids),voltage_mV=np.asarray(tracepred))
 familyhold=[]
 for group in read('COVERAGE_ATLAS.json')['groups']:
  familyhold.append({'dataset':group['dataset'],'type':group['type'],'family':group['family'],'withheld_records':group['records'],'returned':'UNKNOWN','response_coverage':0,'cross_family_prediction_established':False})
 write('FAMILY_HOLDOUT.json',familyhold)
 write('ESTIMATOR_ACCESS.json',sorted(set(access)));write('COMPUTE.json',{'wall_seconds':time.perf_counter()-start,'peak_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'predictions':len(preds),'prediction_archive_bytes':(HERE/'HELDOUT_PREDICTIONS.npz').stat().st_size})
 print(json.dumps({'strata':len(stats),'passing':sum(x['meets_registered_criteria'] for x in stats),'predictions':len(preds),'seconds':time.perf_counter()-start}))
if __name__=='__main__':main()

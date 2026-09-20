"""Read frozen biological fits and validation data, never update parameters."""
import json
from pathlib import Path
import numpy as np
from scipy.stats import t
from fit import sha,save,arrays
H=Path(__file__).resolve().parent;P=H.parent/'fly-physiology-study'
def mse(a,b):return float(np.mean((a-b)**2))
def main():
 p=H/'FIT_FROZEN.json';digest=sha(p);f=json.loads(p.read_text());d=json.loads((H/'data/challenges.json').read_text())
 for name,h in f['source_hashes'].items():assert sha(H/name)==h,name
 x,y=arrays(json.loads((P/'data/apl-validation.json').read_text()))
 reused={k:{'mse':mse(y,x*v['q']),'predicted':(x*v['q']).tolist()} for k,v in f['apl'].items()}
 # New alpha/alpha-prime measurement: shared q is location-independent.
 # The old calyx/lobe site gains and directional coefficients are not portable.
 x=np.array([r['on'] for r in d['apl']]);y=np.array([r['off'] for r in d['apl']])
 prediction={'R0_equal_observation_gain':x,'R1_zero':x*0,'R1_shared':x*f['apl']['R1_shared']['q'][0]}
 new={k:{'mse':mse(y,z),'predicted':z.tolist(),'by_driver':{g:mse(y[np.array([r['driver']==g for r in d['apl']])],z[np.array([r['driver']==g for r in d['apl']])]) for g in ['853','mb247','c739','np3061']}} for k,z in prediction.items()}
 # Compare sign of prediction error improvement, resample entire paired recordings within driver.
 rng=np.random.default_rng(19092026);boot=[];groups=[np.array([i for i,r in enumerate(d['apl']) if r['driver']==g]) for g in ['853','mb247','c739','np3061']]
 for _ in range(10000):
  ix=np.concatenate([rng.choice(g,len(g),replace=True) for g in groups])
  boot.append(mse(y[ix],prediction['R0_equal_observation_gain'][ix])-mse(y[ix],prediction['R1_shared'][ix]))
 a=np.array([r['tau_ms'] for r in d['mbon14']]);train=np.array(f['mbon14']['train_tau_ms']);mu=f['mbon14']['predicted_tau_ms']
 predwidth=float(t.ppf(.975,len(train)-1)*train.std(ddof=1)*np.sqrt(1+1/len(train)))
 result={'fit_sha256':digest,'reused_apl_validation':reused,'new_apl_spatial_challenge':new,
  'new_apl_R0_minus_R1_mse_bootstrap_95pct':np.percentile(boot,[2.5,97.5]).tolist(),
  'challenge_limit':'R0 equal-gain comparator is narrower than all scalar observation models; calyx/lobe site gains cannot transfer to alpha/alpha-prime. New assay does not identify coupling between these regions.',
  'mbon14':{'prediction_ms':mu,'observed_ms':a.tolist(),'raw_cell_mean_ms':float(a.mean()),'reported_mean_ms':d['mbon14_reported_mean']['tau_ms'],
   'rmse_ms':mse(a,mu)**.5,'bias_prediction_minus_raw_mean_ms':float(mu-a.mean()),
   'training_based_individual_prediction_interval_ms':[mu-predwidth,mu+predwidth],
   'within_interval':int(np.sum(abs(a-mu)<=predwidth)),
   'raw_cell_sensitivity_excluding_flagged_duplicate_rmse_ms':mse(np.delete(a,2),mu)**.5,
   'exclusion_warning':'Supplementary sensitivity only; all four records retained in primary calculation. No source correction or independence assertion.',
   'representation_discrimination':False,'independent_validation_qualified':False},
  'fit_unchanged':sha(p)==digest,'neural_kernel_supported':False,'quality_flags':d['quality_flags']}
 save(H/'VALIDATION.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()

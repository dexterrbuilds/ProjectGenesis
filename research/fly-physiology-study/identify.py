"""Independent aggregate identifiability calculation. No neural model imports."""
import hashlib,json,time,resource,platform
from pathlib import Path
import numpy as np
from scipy.stats import t
H=Path(__file__).resolve().parent

def main():
 start=time.perf_counter();p=H/'data/hige-target.json';d=json.loads(p.read_text())
 r=1-d['depression_mean'];hazard=float(-np.log(r))
 half=float(t.ppf(.975,d['n_cells']-1)*d['depression_sem'])
 lo=max(0.,r-half);hi=min(1.,r+half)
 eta=np.logspace(-4,1,101);exposure=hazard/eta;prediction=np.exp(-eta*exposure)
 # d(exp(-eta*exposure))/d(log eta, log exposure) has equal columns: rank one.
 jac=np.array([[-hazard*r,-hazard*r]])
 out={'target_remaining':r,'effective_integrated_depression':hazard,
      'remaining_approx_t95':[lo,hi],
      'integrated_depression_approx_t95':[float(-np.log(hi)),None if lo==0 else float(-np.log(lo))],
      'null_upper_means':'unbounded; published small-sample interval reaches zero remaining current',
      'joint_parameter_jacobian_rank':int(np.linalg.matrix_rank(jac)),
      'joint_parameter_count':2,'equally_fitting_eta_range':[float(eta.min()),float(eta.max())],
      'eta_range_is':'illustrative computational profile, not a biological confidence interval',
      'maximum_prediction_residual':float(np.max(np.abs(prediction-r))),
      'equivalence_profile':[{'eta':float(a),'unmeasured_exposure':float(b),'predicted_remaining':float(c)} for a,b,c in zip(eta,exposure,prediction)],
      'floor_identifiability':'With max(f, exp(-H)), any f <= observed remaining fits; f equal to remaining censors arbitrarily larger H.',
      'held_out_validation':'unavailable: one aggregate endpoint, no independent trial series or calibrated current-to-spike mapping',
      'neural_parameters_identified':[], 'stage_parameter_changes':{},
      'source_hashes':{str(x.relative_to(H)):hashlib.sha256(x.read_bytes()).hexdigest() for x in [p,H/'identify.py',H/'HIGE_IDENTIFICATION_PLAN.md']},
      'wall_seconds':time.perf_counter()-start,'peak_process_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if platform.system()=='Darwin' else 1024)}
 dest=H/'IDENTIFICATION_FROZEN.json';assert not dest.exists();dest.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k!='equivalence_profile'},indent=2))
if __name__=='__main__':main()

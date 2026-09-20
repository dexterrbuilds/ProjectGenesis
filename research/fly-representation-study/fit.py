"""Experimental observation fits only. No Stage imports or behavioral objectives."""
import hashlib,json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar
H=Path(__file__).resolve().parent;P=H.parent/'fly-physiology-study'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(path,x):
 assert not path.exists(),f'Refuse overwrite: {path}'
 path.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def arrays(rows):
 a=np.array([r['values'] for r in rows]);return a[:,[0,3]],a[:,[1,2]]
def fit(x,y,model):
 if model=='R1_zero':return np.zeros(2)
 if model=='R1_shared':return np.repeat(np.clip(np.sum(x*y)/np.sum(x*x),0,1),2)
 if model=='R1_directional':return np.clip(np.sum(x*y,axis=0)/np.sum(x*x,axis=0),0,1)
 z=minimize_scalar(lambda z:np.mean((y-x*[np.exp(z),np.exp(-z)])**2),bounds=(-10,10),method='bounded').x
 return np.array([np.exp(z),np.exp(-z)])
def main():
 x,y=arrays(json.loads((P/'data/apl-train.json').read_text()));rng=np.random.default_rng(18092026)
 results={}
 for name,k in [('R0_shared_activity',1),('R1_zero',0),('R1_shared',1),('R1_directional',2)]:
  q=fit(x,y,name);res=y-x*q;n=res.size;K=k+1
  loo=[float(np.mean((y[i]-x[i]*fit(np.delete(x,i,0),np.delete(y,i,0),name))**2)) for i in range(len(x))]
  boot=[]
  for _ in range(3000):
   ix=rng.integers(len(x),size=len(x));boot.append(fit(x[ix],y[ix],name))
  results[name]={'q':q.tolist(),'parameters':k,'train_mse':float(np.mean(res**2)),
    'train_aicc':float(n*np.log(np.mean(res**2))+2*K+2*K*(K+1)/(n-K-1)),
    'loo_recording_mse':float(np.mean(loo)), 'loo_errors':loo,
    'bootstrap_95pct':np.percentile(boot,[2.5,97.5],axis=0).T.tolist()}
 tau=np.array([13.54,14.46,24.58,15.50,12.20])
 save(H/'FIT_FROZEN.json',{'apl':results,'mbon14':{'train_tau_ms':tau.tolist(),'predicted_tau_ms':float(tau.mean()),
  'training_sd_ms':float(tau.std(ddof=1)),'parameters':1,'source':'Hafez 2023 Table 1 membrane-bound GFP, five cells'},
  'source_hashes':{'PLAN.md':sha(H/'PLAN.md'),'fit.py':sha(H/'fit.py'),
    '../fly-physiology-study/data/apl-train.json':sha(P/'data/apl-train.json'),
    '../fly-physiology-study/CALIBRATION_FROZEN.json':sha(P/'CALIBRATION_FROZEN.json')},
  'fitting_scope':'conditional fluorescence transfer and MBON14 population tau only; no neural kernel',
  'aicc_warning':'working iid Gaussian residual criterion, includes variance parameter; directions and flies may be correlated',
  'calibrated_neural_parameters':{}})
 print(json.dumps(results,indent=2))
if __name__=='__main__':main()

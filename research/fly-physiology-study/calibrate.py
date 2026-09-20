"""Independent APL observation-model identification, NOT a neural kernel.

Training opens only the experimental training split. No stage imports, connectivity,
acceptance criteria or application code. Validation cannot update the fitted file.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar

H = Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):
    if p.exists(): raise FileExistsError('Frozen output exists: '+str(p))
    p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def arrays(rows):
    a=np.asarray([r['values'] for r in rows],float)
    return a[:,[0,3]], a[:,[1,2]]
def slopes(x,y): return (x*y).sum(axis=0)/(x*x).sum(axis=0)
def mse(y,z): return float(np.mean((y-z)**2))
def predict(x,q): return x*np.asarray(q)

def train():
    rows=json.loads((H/'data/apl-train.json').read_text());x,y=arrays(rows)
    raw=slopes(x,y);q=np.clip(raw,0,1)
    # One shared latent activity, with arbitrary *fixed* site observation gains:
    # lobe/calyx = g under calyx stimulation and calyx/lobe = 1/g under lobe stimulation.
    opt=minimize_scalar(lambda z:mse(y,predict(x,[np.exp(z),np.exp(-z)])),
                        bounds=(-10,10),method='bounded',options={'xatol':1e-12})
    g=float(np.exp(opt.x))
    rng=np.random.default_rng(9172026)
    boot=[]
    for _ in range(10000):
        ix=rng.integers(0,len(x),len(x));boot.append(slopes(x[ix],y[ix]))
    interval=np.percentile(boot,[2.5,97.5],axis=0).T.tolist()
    fit={'target': 'APL two-site calcium response transfer; not membrane/synaptic physiology',
         'local_transfer': q.tolist(), 'unbounded_transfer': raw.tolist(),
         'recording_bootstrap_95pct_unbounded': interval,
         'bootstrap_warning': 'conditional recording-resampling interval; unknown fly clustering and noisy x',
         'point_site_gain_ratio': g,
         'train_mse': {'local':mse(y,predict(x,q)), 'point_equal_gain':mse(y,x),
                       'point_free_site_gain':mse(y,predict(x,[g,1/g]))},
         'source_rows': [r['source_row'] for r in rows],
         'objective': 'unweighted squared error of off-site deltaF/F, conditional on on-site response',
         'bounds': {'local_coefficients':[0,1], 'log_site_gain':[-10,10]},
         'source_hashes': {p:sha(H/p) for p in ['calibrate.py','PLAN.md','data/apl-train.json','data/PROVENANCE.json']},
         'neural_kernel_supported':False, 'stage_parameter_changes':{},
         'transfer_rejection': 'Spatial fluorescence mixing does not identify APL-to-KC conductance, membrane time constants, contact normalization, DA dose, or a one-state APL kernel.'}
    save(H/'CALIBRATION_FROZEN.json',fit)
    print(json.dumps(fit,indent=2))

def validate():
    p=H/'CALIBRATION_FROZEN.json';before=sha(p);f=json.loads(p.read_text())
    for name,h in f['source_hashes'].items(): assert sha(H/name)==h,name
    rows=json.loads((H/'data/apl-validation.json').read_text());x,y=arrays(rows)
    g=f['point_site_gain_ratio'];q=f['local_transfer']
    predictions={'local':predict(x,q),'point_equal_gain':x,'point_free_site_gain':predict(x,[g,1/g])}
    out={'calibration_sha256':before,'held_out_rows':[r['source_row'] for r in rows],
         'validation_source_sha256':sha(H/'data/apl-validation.json'),
         'observed':y.tolist(),'predictions':{k:v.tolist() for k,v in predictions.items()},
         'mse':{k:mse(y,v) for k,v in predictions.items()},
         'n_recordings':len(x),'n_offsite_measurements':int(y.size),
         'validation_level':'recording split only; fly independence unavailable',
         'neural_validation':False,'fit_updated':False}
    assert sha(p)==before
    save(H/'VALIDATION.json',out)
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['train','validate']);a=p.parse_args()
    train() if a.mode=='train' else validate()

"""Checkpoint-preserving parallel executor for the unchanged prospective battery.

No model/protocol/parameter changes. Completed serial artifacts are never rewritten.
Use only after the original serial process has been stopped.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor,as_completed
from dataclasses import asdict,replace
import hashlib,json,multiprocessing,os,platform,resource,shutil,time,zipfile
from pathlib import Path
import numpy as np
import scipy
from model import Circuit,Parameters,MODEL_VERSION,canonical
from experiment import one,SEEDS
HERE=Path(__file__).resolve().parent
C=None

def init(path):
    global C
    C=Circuit(path)

def job(item,work):
    name,kw=item
    r=one(C,output=Path(work)/name,**kw);r['run']=name
    return r,resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if platform.system()=='Darwin' else 1024)

def cases():
    cases=[(s,q,b) for s in SEEDS for q in ('A','B') for b in (.2,.8)]
    for i in np.random.Generator(np.random.PCG64(3700)).permutation(len(cases)):
        s,q,b=cases[i];yield f'primary-{s}-{q}-{b}',dict(seed=s,cue=q,body=b,replay=True,dense=s==3701 and q=='A')
    for cond in ('silence_dan','silence_mb11','silence_mb18','silence_oa','remove_da_gate','freeze_modulation','freeze_plasticity',
                 'matched_control','remove_pn_kc','remove_mb11_mb18','remove_mb18_lh','shuffle_pn_weights','no_apl','no_lh_feedback','global_gain'):
        for q in ('A','B'):
            for b in (.2,.8):yield f'control-{cond}-{q}-{b}',dict(cue=q,body=b,intervention=cond)
    for arm,history,cond in [('acquisition','ten','intact'),('acquisition','ten','silence_oa'),('interruption','ten','intact'),('none','single','intact'),('none','sham','intact')]:
        for q in ('A','B'):
            for b in (.2,.8):yield f'protocol-{arm}-{history}-{cond}-{q}-{b}',dict(cue=q,body=b,arm=arm,history=history,intervention=cond)
    p=Parameters();variants={'half_dt':replace(p,dt=.005),'tau_half':replace(p,tau=.025),'tau_double':replace(p,tau=.1),
        'eta_half':replace(p,learning_rate=.04),'eta_double':replace(p,learning_rate=.16),'floor01':replace(p,gate_floor=.1),'floor04':replace(p,gate_floor=.4),
        'da_half':replace(p,dopamine_gain=.5),'da_double':replace(p,dopamine_gain=2),'gain075':replace(p,fast_gain=.75),'gain125':replace(p,fast_gain=1.25),
        'oa_half':replace(p,oa_gain=.5),'oa_double':replace(p,oa_gain=2),'retained':replace(p,normalization='retained_inputs'),'roles':replace(p,normalization='retained_roles')}
    for name,p in variants.items():
        for b in (.2,.8):yield f'sensitivity-{name}-{b}',dict(params=p,body=b,arm='acquisition' if name.startswith('oa_') else 'none')

def main(cp,work,out):
    allcases=list(cases());assert len(allcases)==122
    initial_birth=work.stat().st_birthtime;start=time.perf_counter();results={};pending=[];prior_hashes={}
    required=['initial.json.gz','trained.json.gz','fast-reset.json.gz','summary.json','stimuli.json','recall-config.json','trace.npz','probe-rates.npz']
    for name,kw in allcases:
        d=work/name
        if d.exists():
            if not all((d/n).is_file() for n in required):
                raise ValueError('Incomplete serial write must be preserved outside work before resuming: '+str(d))
            for n in ('trace.npz','probe-rates.npz'):
                with zipfile.ZipFile(d/n) as z:assert z.testzip() is None
            r=json.loads((d/'summary.json').read_text())
            assert r['parameters']==asdict(kw.get('params',Parameters()))
            for k,default in [('seed',3701),('cue','A'),('intervention','intact'),('arm','none'),('history','ten')]:assert r[k]==kw.get(k,default)
            assert r['resource']==kw.get('body',.2)
            r['run']=name;results[name]=r
            prior_hashes.update({str(p.relative_to(work)):hashlib.sha256(p.read_bytes()).hexdigest() for p in d.iterdir() if p.is_file()})
        else:pending.append((name,kw))
    reused=len(results);print(json.dumps({'preserved_runs':reused,'remaining':len(pending)}),flush=True)
    peaks=[]
    with ProcessPoolExecutor(max_workers=4,mp_context=multiprocessing.get_context('spawn'),initializer=init,initargs=(str(cp),)) as pool:
        futures={pool.submit(job,item,str(work)):item[0] for item in pending}
        for f in as_completed(futures):
            r,peak=f.result();results[r['run']]=r;peaks.append(peak)
            print(json.dumps({'run':r['run'],'done':len(results),'total':122,'wall_seconds':r['wall_seconds']}),flush=True)
    for name,h in prior_hashes.items():assert hashlib.sha256((work/name).read_bytes()).hexdigest()==h
    c=Circuit(cp)
    parent_rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if platform.system()=='Darwin' else 1024)
    summary={'model':MODEL_VERSION,'circuit':c.manifest_hash,'runs':[results[name] for name,kw in allcases],
        'sources':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ('model.py','experiment.py','resume.py','PLAN.md','LITERATURE.md')},
        'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'platform':platform.platform(),'cpu_count':os.cpu_count()},
        'performance':{'wall_seconds':time.time()-initial_birth,'parallel_phase_seconds':time.perf_counter()-start,
            'preserved_serial_conditions':reused,'parallel_conditions':len(pending),'workers':4,
            'peak_worker_rss_bytes':max(peaks),'peak_coordinator_rss_bytes':parent_rss,
            'concurrent_rss_upper_bound_bytes':parent_rss+4*max(peaks),
            'note':'Per-process peak RSS measured; concurrent RSS upper bound is not a sampled total peak. Wall includes serial-to-parallel checkpoint transition.'},
        'preserved_serial_artifact_hashes':prior_hashes}
    (work/'results.json').write_bytes(canonical(summary))
    manifest={'files':{str(p.relative_to(work)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(work.rglob('*')) if p.is_file()}}
    raw=canonical(manifest);identity=hashlib.sha256(raw).hexdigest();(work/'evidence-manifest.json').write_bytes(raw)
    dest=out/identity;dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists():raise ValueError('Never overwrite evidence')
    shutil.move(str(work),str(dest));print(json.dumps({'evidence':str(dest),'performance':summary['performance']},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--circuit',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--output',type=Path,default=HERE/'evidence')
    a=p.parse_args();main(a.circuit,a.work,a.output)

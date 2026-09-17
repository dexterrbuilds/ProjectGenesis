"""Independent preparations; no biological orthogonality/coupling claim."""
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import resource
import shutil
import sys
import tempfile
import time
import numpy as np

HERE=Path(__file__).resolve().parent

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    sys.modules[name]=mod
    spec.loader.exec_module(mod)
    return mod

s1=load('frozen_stage1_model',HERE.parent/'fly-stage1/model.py')
s2=load('independent_stage2_model',HERE/'model.py')
c1=s1.Circuit(next((HERE.parent/'fly-stage1/artifacts').iterdir()))
c2=s2.Circuit(next((HERE/'artifacts').iterdir()))
shared=sorted(set(c1.ids[i] for i in c1.groups['PN']) & set(c2.ids[i] for i in c2.groups['PN']))
rng=np.random.Generator(np.random.PCG64(2701))
roots=rng.permutation(shared)
n=round(.05*len(shared))
patterns={'A':roots[:n].tolist(),'B':roots[n:2*n].tolist()}


def probe(m,patterns,group):
    state=m.snapshot()
    results={}
    for cue,roots in patterns.items():
        m.restore(state)
        current=np.zeros(m.c.n)
        current[[m.c.index[r] for r in roots]]=1
        rr=[]
        for t in range(round(1/m.p.dt)):
            m.step(current)
            if t>=round(.5/m.p.dt):
                rr.append(m.r.copy())
        r=np.mean(rr,axis=0)
        results[cue]={'output':float(r[m.c.groups[group]].mean()),
                      'KC':float(r[m.c.groups['KC']].mean()),
                      'output_neurons':{m.c.ids[int(i)]:float(r[i]) for i in m.c.groups[group]}}
    m.restore(state)
    return results


def main():
    start=time.perf_counter()
    work=Path(tempfile.mkdtemp(prefix='fly-stage2-factorial-'))
    results=[]
    for cue in ('A','B'):
        for exposures in (0,10):
            for reinforcement in (False,True):
                record={'cue':cue,'prior_exposures':exposures,'reinforcement':reinforcement}
                for name,mod,c,group in (('alpha1',s1,c1,'MBON_app'),('alpha_prime3',s2,c2,'MBON')):
                    m=mod.Model(c)
                    initial=m.snapshot()
                    before=probe(m,patterns,group)
                    trace=[]
                    for tick in range(14000):
                        current=np.zeros(c.n)
                        pn_on=(tick<7000 and exposures==10 and tick%700<100) or (7000<=tick<13000)
                        if pn_on:
                            current[[c.index[r] for r in patterns[cue]]]=1
                        if name=='alpha1' and reinforcement and 7000<=tick<13000 and tick%200<100:
                            current[c.groups['DAN_app']]=1
                        m.step(current)
                        if tick%10==0:
                            trace.append([m.tick*.01]+[float(m.r[ix].mean()) for ix in c.groups.values()]
                                           +[float(m.multiplier.mean())])
                    trained=m.snapshot()
                    m.reset_fast_state()
                    after=probe(m,patterns,group)
                    effect={k:None if before[k]['output']<=1e-8 else 1-after[k]['output']/before[k]['output'] for k in patterns}
                    record[name]={'before':before,'after':after,'depression':effect,
                        'max_plastic_change':float(1-m.multiplier.min()),'model':mod.MODEL_VERSION,
                        'final_hash':hashlib.sha256(mod.canonical(trained)).hexdigest()}
                    dest=work/f'{cue}-{exposures}-{int(reinforcement)}-{name}'
                    dest.mkdir()
                    for tag,state in (('initial',initial),('trained',trained)):
                        (dest/f'{tag}.json.gz').write_bytes(gzip.compress(mod.canonical(state),mtime=0))
                    np.savez_compressed(dest/'trace.npz',columns=np.array(['seconds',*c.groups,'mean_multiplier']),values=np.array(trace))
                results.append(record)
                print(json.dumps({'cue':cue,'exposures':exposures,'reward':reinforcement,
                                  'alpha1':record['alpha1']['depression'][cue],
                                  'alpha_prime3':record['alpha_prime3']['depression'][cue]}),flush=True)
    summary={'preparations':'SEPARATE; no coupling or biological orthogonality measured',
             'shared_pn_count':len(shared),'patterns':patterns,'seed':2701,'results':results,
             'circuits':{'alpha1':c1.manifest_hash,'alpha_prime3':c2.manifest_hash},
             'sources':{str(p.relative_to(HERE.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
                        [HERE/'FACTORIAL_PLAN.md',HERE/'reward_comparison.py',HERE/'model.py',HERE.parent/'fly-stage1/model.py']},
             'performance':{'wall_seconds':time.perf_counter()-start,
                  'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if platform.system()=='Darwin' else 1024)}}
    (work/'results.json').write_bytes(s2.canonical(summary))
    manifest={'files':{str(p.relative_to(work)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(work.rglob('*')) if p.is_file()}}
    raw=s2.canonical(manifest)
    (work/'evidence-manifest.json').write_bytes(raw)
    dest=HERE/'reward-evidence'/hashlib.sha256(raw).hexdigest()
    dest.parent.mkdir(exist_ok=True)
    if dest.exists():
        raise ValueError('Never overwrite evidence')
    shutil.move(str(work),str(dest))
    print(json.dumps({'evidence':str(dest),'performance':summary['performance']},indent=2))

if __name__=='__main__':
    main()

"""Counterbalanced sensory/body-boundary experiments; no behavioral decisions."""
import argparse
from dataclasses import asdict,replace
import gzip
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import shutil
import tempfile
import time
import numpy as np
import scipy
from model import Circuit,Model,Parameters,MODEL_VERSION,canonical

HERE=Path(__file__).resolve().parent
SEEDS=(3701,3702,3703)


def patterns(c,seed):
    r=np.random.Generator(np.random.PCG64(seed)).permutation(c.groups['PN'])
    n=round(.05*len(r))
    return {'A':r[:n],'B':r[n:2*n]}


def protocol(c,p,indices,body,arm='none',history='ten'):
    starts=list(range(0,240,24)) if history=='ten' else ([216] if history=='single' else [])
    events=[{'start_tick':round(t/p.dt),'stop_tick':round((t+12)/p.dt),
             'currents':[[c.ids[int(i)],1.] for i in indices]} for t in starts]
    if arm=='interruption' and events:events[-1]['stop_tick']=round(224/p.dt)
    sensory_hash=hashlib.sha256(canonical(events)).hexdigest()
    if arm=='acquisition':
        events.append({'start_tick':round(224/p.dt),'stop_tick':round(228/p.dt),
                       'currents':[[c.ids[int(i)],.5] for i in c.groups['OA']]})
    return {'dt':p.dt,'stop_tick':round(240/p.dt),'resource_input':body,'events':events,'sensory_hash':sensory_hash}


def execute(m,s,dense=False):
    if s['dt']!=m.p.dt:raise ValueError('Timing mismatch')
    changes={}
    for e in s['events']:
        for root,v in e['currents']:
            i=m.c.index[root]
            if m.c.roles[i] not in ('PN','OA'):raise ValueError('Unsupported experimental current')
            for t,sign in ((e['start_tick'],1),(e['stop_tick'],-1)):
                changes.setdefault(t,[]).append((i,sign*v))
    current=np.zeros(m.c.n)
    times,groups,bodies,mult,rates,plastic,dense_times=[],[],[],[],[],[],[]
    for t in range(s['stop_tick']):
        for i,v in changes.get(t,[]):current[i]+=v
        m.step(current,s['resource_input'])
        if t%round(.1/m.p.dt)==0:
            times.append(m.tick*m.p.dt)
            groups.append([float(m.r[ix].mean()) for ix in m.c.groups.values()])
            bodies.append(m.body);mult.append(float(m.multiplier[m.learnable].mean()))
        if dense and t%round(1/m.p.dt)==0:
            dense_times.append(m.tick*m.p.dt);rates.append(m.r.astype(np.float32));plastic.append(m.multiplier.astype(np.float32))
    return {'seconds':np.array(times),'group_names':np.array(list(m.c.groups)),
            'group_rates':np.array(groups),'body':np.array(bodies),'mean_learnable_multiplier':np.array(mult),
            'dense_seconds':np.array(dense_times),'rates':np.array(rates),'plastic':np.array(plastic),
            'root_ids':np.array(m.c.ids),'plastic_edge_indices':m.plastic_edges}


def probe(m,state,cues):
    result={};vectors={}
    for name,indices in cues.items():
        m.restore(state)
        current=np.zeros(m.c.n);current[indices]=1
        observations=[]
        for t in range(round(2/m.p.dt)):
            m.step(current,state['body'])
            if t>=round(1/m.p.dt):observations.append(m.r.copy())
        v=np.mean(observations,axis=0);vectors[name]=v
        result[name]={'groups':{g:float(v[ix].mean()) for g,ix in m.c.groups.items()},
                      'neurons':{m.c.ids[int(i)]:float(v[i]) for g in ('MB11','MB18','LH','VALUE','CONTROL') for i in m.c.groups[g]},
                      'hash':hashlib.sha256(v.tobytes()).hexdigest()}
    m.restore(state)
    return result,vectors


def metrics(trace):
    time=trace['seconds'];rr=trace['group_rates'];names=trace['group_names'].tolist()
    def mean(a,b):
        return {g:float(rr[(time>=a)&(time<b),j].mean()) for j,g in enumerate(names)}
    trials=[]
    for start in range(0,240,24):
        trials.append({'maintained':mean(start+2,start+10),'tail':mean(start+8,start+10),
                       'onset':mean(start,start+1),'after_offset':mean(start+14,start+16)})
    duration={}
    for g in ('MB11','MB18','LH'):
        j=names.index(g);scale=trials[0]['maintained'][g]
        duration[g]={str(f):float(.1*np.count_nonzero((rr[:,j]>scale*f)&(time>=216)&(time<228)))
                     if scale>1e-8 else None for f in (.25,.5,.75)}
    return {'trials':trials,'last_window':mean(224,228),'quiet':mean(238,240),'duration_sweep':duration}


def one(c,seed=3701,cue='A',body=.2,params=Parameters(),intervention='intact',arm='none',history='ten',replay=False,dense=False,output=None):
    start=time.perf_counter();m=Model(c,params,seed,intervention,body)
    initial=m.snapshot();cues=patterns(c,seed)
    before,bvec=probe(m,initial,cues)
    s=protocol(c,params,cues[cue],body,arm,history)
    tr=execute(m,s,dense=dense);trained=m.snapshot()
    after,avec=probe(m,trained,cues)
    m.restore(trained);m.reset_fast_state();reset=m.snapshot()
    cleared,cvec=probe(m,reset,cues)
    restored,_=probe(m,initial,cues)
    m.restore(reset);m.body=1-body
    swapped,_=probe(m,m.snapshot(),cues)
    replay_exact=None
    if replay:
        clone=Model(c,params,seed,intervention,body)
        clone.restore(json.loads(canonical(initial)));execute(clone,json.loads(canonical(s)))
        replay_exact=canonical(clone.snapshot())==canonical(trained)
    loss=1-np.array(trained['plastic_multiplier'])[m.learnable]
    summary={'seed':seed,'cue':cue,'resource':body,'intervention':intervention,'arm':arm,'history':history,
        'parameters':asdict(params),'baseline':before,'post':after,'fast_reset':cleared,'restored':restored,
        'body_swap_same_weights':swapped,'metrics':metrics(tr),'sensory_hash':s['sensory_hash'],
        'reset_max_rate_delta':float(max(np.max(np.abs(avec[q]-cvec[q])) for q in cues)),
        'restoration_exact':restored==before,'replay_exact':replay_exact,
        'max_plastic_change':float(loss.max()),'plastic_rows_changed':int(np.count_nonzero(loss>1e-12)),
        'lesioned_roots':[c.ids[int(i)] for i in m.lesion],
        'initial_hash':hashlib.sha256(canonical(initial)).hexdigest(),
        'trained_hash':hashlib.sha256(canonical(trained)).hexdigest(),'wall_seconds':time.perf_counter()-start}
    if output:
        output.mkdir(parents=True,exist_ok=False)
        for name,state in [('initial',initial),('trained',trained),('fast-reset',reset)]:
            (output/f'{name}.json.gz').write_bytes(gzip.compress(canonical(state),mtime=0))
        (output/'summary.json').write_bytes(canonical(summary));(output/'stimuli.json').write_bytes(canonical(s))
        (output/'recall-config.json').write_bytes(canonical({'parameters':asdict(params),'seed':seed,'intervention':intervention,
            'resource':body,'patterns':{q:[c.ids[int(i)] for i in ix] for q,ix in cues.items()}}))
        np.savez_compressed(output/'trace.npz',**tr)
        np.savez_compressed(output/'probe-rates.npz',root_ids=np.array(c.ids),**{
            f'{phase}_{q}':v for phase,vec in [('baseline',bvec),('post',avec),('reset',cvec)] for q,v in vec.items()})
    return summary


def suite(c,output):
    start=time.perf_counter();work=Path(tempfile.mkdtemp(prefix='fly-stage3-'));results=[]
    def run(name,**kw):
        r=one(c,output=work/name,**kw);r['run']=name;results.append(r)
        print(json.dumps({'run':name,'MB11_first':r['metrics']['trials'][0]['maintained']['MB11'],
            'MB11_last':r['metrics']['trials'][9]['maintained']['MB11'],'wall_seconds':r['wall_seconds']}),flush=True)
    cases=[(s,q,b) for s in SEEDS for q in ('A','B') for b in (.2,.8)]
    order=np.random.Generator(np.random.PCG64(3700)).permutation(len(cases))
    for i in order:
        s,q,b=cases[i]
        run(f'primary-{s}-{q}-{b}',seed=s,cue=q,body=b,replay=True,dense=s==3701 and q=='A')
    for cond in ('silence_dan','silence_mb11','silence_mb18','silence_oa','remove_da_gate',
                 'freeze_modulation','freeze_plasticity','matched_control','remove_pn_kc',
                 'remove_mb11_mb18','remove_mb18_lh','shuffle_pn_weights','no_apl','no_lh_feedback','global_gain'):
        for q in ('A','B'):
            for b in (.2,.8):run(f'control-{cond}-{q}-{b}',cue=q,body=b,intervention=cond)
    for arm,history,cond in [('acquisition','ten','intact'),('acquisition','ten','silence_oa'),
                             ('interruption','ten','intact'),('none','single','intact'),('none','sham','intact')]:
        for q in ('A','B'):
            for b in (.2,.8):run(f'protocol-{arm}-{history}-{cond}-{q}-{b}',cue=q,body=b,arm=arm,history=history,intervention=cond)
    p=Parameters();variants={'half_dt':replace(p,dt=.005),'tau_half':replace(p,tau=.025),'tau_double':replace(p,tau=.1),
        'eta_half':replace(p,learning_rate=.04),'eta_double':replace(p,learning_rate=.16),
        'floor01':replace(p,gate_floor=.1),'floor04':replace(p,gate_floor=.4),
        'da_half':replace(p,dopamine_gain=.5),'da_double':replace(p,dopamine_gain=2),
        'gain075':replace(p,fast_gain=.75),'gain125':replace(p,fast_gain=1.25),
        'oa_half':replace(p,oa_gain=.5),'oa_double':replace(p,oa_gain=2),
        'retained':replace(p,normalization='retained_inputs'),'roles':replace(p,normalization='retained_roles')}
    for name,p in variants.items():
        for b in (.2,.8):run(f'sensitivity-{name}-{b}',params=p,body=b,arm='acquisition' if name.startswith('oa_') else 'none')
    summary={'model':MODEL_VERSION,'circuit':c.manifest_hash,'runs':results,
        'sources':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ('model.py','experiment.py','PLAN.md','LITERATURE.md')},
        'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
                       'platform':platform.platform(),'cpu_count':os.cpu_count()},
        'performance':{'wall_seconds':time.perf_counter()-start,
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if platform.system()=='Darwin' else 1024)}}
    (work/'results.json').write_bytes(canonical(summary))
    manifest={'files':{str(p.relative_to(work)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(work.rglob('*')) if p.is_file()}}
    raw=canonical(manifest);identity=hashlib.sha256(raw).hexdigest();(work/'evidence-manifest.json').write_bytes(raw)
    dest=output/identity;dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists():raise ValueError('Refusing to replace evidence')
    shutil.move(str(work),str(dest));print(json.dumps({'evidence':str(dest),'performance':summary['performance']},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--circuit',type=Path,required=True);p.add_argument('--output',type=Path,default=HERE/'evidence')
    a=p.parse_args();suite(Circuit(a.circuit),a.output)

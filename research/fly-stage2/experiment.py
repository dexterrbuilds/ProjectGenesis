"""Prospective Stage-2 assays. Cue names exist ONLY in this experiment controller."""
import argparse
from dataclasses import asdict, replace
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
from model import Circuit, Model, Parameters, MODEL_VERSION, canonical

HERE = Path(__file__).resolve().parent
SEEDS = (2701,2702,2703)


def cue_patterns(circuit, seed):
    rng = np.random.Generator(np.random.PCG64(seed))
    pn = rng.permutation(circuit.groups['PN'])
    size = max(2, round(.05*len(pn)))
    if size*2 > len(pn):
        raise ValueError('Insufficient distinct sensory inputs')
    return {'A': pn[:size], 'B': pn[size:2*size]}


def protocol(c, p, indices, presentations=10):
    return {'dt':p.dt, 'stop_tick':round(70/p.dt), 'events':[
        {'start_tick':round(7*k/p.dt), 'stop_tick':round((7*k+1)/p.dt),
         'currents':[[c.ids[int(i)], 1.] for i in indices]} for k in range(presentations)]}


def execute(m, stimulus, record=False, dense=False):
    if stimulus['dt'] != m.p.dt:
        raise ValueError('Timing mismatch')
    transitions = {}
    for ev in stimulus['events']:
        for root, value in ev['currents']:
            i = m.c.index[root]
            if m.c.roles[i] != 'PN':
                raise ValueError('This familiarity assay accepts only PN sensory current')
            for tick, sign in ((ev['start_tick'],1), (ev['stop_tick'],-1)):
                transitions.setdefault(tick, []).append((i, sign*value))
    current = np.zeros(m.c.n)
    times, rates, plastic, group_rates, group_plastic = [], [], [], [], []
    groups = list(m.c.groups)
    for t in range(stimulus['stop_tick']):
        for i, v in transitions.get(t,[]):
            current[i] += v
        m.step(current)
        if record and t % round(.1/m.p.dt) == 0:
            times.append(m.tick*m.p.dt)
            group_rates.append([float(m.r[ids].mean()) for ids in m.c.groups.values()])
            group_plastic.append(float(m.multiplier.mean()))
            if dense:
                rates.append(m.r.copy())
                plastic.append(m.multiplier.copy())
    return {'seconds':np.array(times), 'group_names':np.array(groups), 'group_rates':np.array(group_rates),
            'mean_multiplier':np.array(group_plastic), 'rates':np.array(rates), 'plastic':np.array(plastic),
            'root_ids':np.array(m.c.ids), 'plastic_edge_indices':m.plastic_edges}


def probe(m, state, patterns):
    result, vectors = {}, {}
    for cue, indices in patterns.items():
        m.restore(state)
        current = np.zeros(m.c.n)
        current[indices] = 1
        observations = []
        for t in range(round(1/m.p.dt)):
            m.step(current)
            if t >= round(.5/m.p.dt):
                observations.append(m.r.copy())
        r = np.mean(observations,axis=0)
        vectors[cue] = r
        result[cue] = {'groups':{g:float(r[ids].mean()) for g,ids in m.c.groups.items()},
                       'mbon':{m.c.ids[int(i)]:float(r[i]) for i in m.c.groups['MBON']},
                       'kc_active_fraction':float(np.mean(r[m.c.groups['KC']] > 1e-5)),
                       'rates_sha256':hashlib.sha256(r.tobytes()).hexdigest()}
    m.restore(state)
    return result, vectors


def effect(before, after, cue, group='MBON'):
    b = before[cue]['groups'][group]
    return None if b <= 1e-8 else 1-after[cue]['groups'][group]/b


def one(circuit, seed=2701, repeated='A', params=Parameters(), intervention='intact',
        presentations=10, replay=False, dense=False, output=None):
    started = time.perf_counter()
    m = Model(circuit, params, seed, intervention)
    initial = m.snapshot()
    patterns = cue_patterns(circuit,seed)
    before, bvec = probe(m, initial, patterns)
    stimulus = protocol(circuit,params,patterns[repeated],presentations)
    trace = execute(m,stimulus,record=output is not None,dense=dense)
    trained = m.snapshot()
    after, avec = probe(m,trained,patterns)
    m.restore(trained)
    m.reset_fast_state()
    reset = m.snapshot()
    reset_result, rvec = probe(m,reset,patterns)
    restored, ovec = probe(m,initial,patterns)
    recovery = {}
    recovery_vectors = {}
    for seconds in (0,300,1200,3600):
        m.restore(reset)
        m.idle(seconds)
        recovery[str(seconds)], v = probe(m,m.snapshot(),patterns)
        recovery_vectors.update({f'recovery_{seconds}_{cue}':a for cue,a in v.items()})
    replay_exact = None
    if replay:
        clone = Model(circuit,params,seed,intervention)
        clone.restore(json.loads(canonical(initial)))
        execute(clone,json.loads(canonical(stimulus)))
        replay_exact = canonical(clone.snapshot()) == canonical(trained)
    other = 'B' if repeated == 'A' else 'A'
    d, control = effect(before,after,repeated), effect(before,after,other)
    delta = 1-np.array(trained['plastic_multiplier'])
    summary = {'seed':seed,'repeated':repeated,'intervention':intervention,'presentations':presentations,
        'parameters':asdict(params),'baseline':before,'post':after,'fast_reset':reset_result,
        'restored':restored,'recovery':recovery,'repeated_depression':d,'unseen_depression':control,
        'specificity':None if d is None or control is None else d-control,
        'reset_depression':effect(before,reset_result,repeated),
        'recovery_depression':{t:effect(before,r,repeated) for t,r in recovery.items()},
        'sensory_relative_change':{g:{cue:effect(before,after,cue,g) for cue in patterns} for g in ('PN','KC','CONTROL')},
        'max_per_neuron_change':{g:float(max(np.max(np.abs(avec[k][ids]-bvec[k][ids])) for k in patterns))
                                 for g,ids in circuit.groups.items()},
        'plastic_rows_changed':int(np.count_nonzero(delta > 1e-12)),
        'max_plastic_change':float(delta.max()),'mean_plastic_change':float(delta.mean()),
        'restoration_exact':restored == before,'replay_exact':replay_exact,
        'fast_reset_max_rate_delta':float(max(np.max(np.abs(avec[k]-rvec[k])) for k in patterns)),
        'lesioned_roots':[circuit.ids[int(i)] for i in m.lesion],
        'initial_hash':hashlib.sha256(canonical(initial)).hexdigest(),
        'trained_hash':hashlib.sha256(canonical(trained)).hexdigest(),
        'simulated_training_seconds':70.,'wall_seconds':time.perf_counter()-started}
    if output:
        output.mkdir(parents=True,exist_ok=False)
        (output/'summary.json').write_bytes(canonical(summary))
        (output/'stimuli.json').write_bytes(canonical(stimulus))
        (output/'recall-config.json').write_bytes(canonical({'parameters':asdict(params),'seed':seed,
            'intervention':intervention,'patterns':{k:[circuit.ids[int(i)] for i in v] for k,v in patterns.items()}}))
        for name,state in (('initial',initial),('trained',trained),('fast-reset',reset)):
            (output/f'{name}.json.gz').write_bytes(gzip.compress(canonical(state),mtime=0))
        np.savez_compressed(output/'trace.npz',**trace)
        np.savez_compressed(output/'probe-rates.npz',root_ids=np.array(circuit.ids),
            **{f'{phase}_{cue}':a for phase,v in [('baseline',bvec),('post',avec),('reset',rvec),('restored',ovec)]
               for cue,a in v.items()},**recovery_vectors)
    return summary


def suite(circuit,output):
    start = time.perf_counter()
    work = Path(tempfile.mkdtemp(prefix='fly-stage2-'))
    results = []
    def run(name,**kw):
        r = one(circuit,output=work/name,**kw)
        r['run'] = name
        results.append(r)
        print(json.dumps({'run':name,'specificity':r['specificity'],'repeated':r['repeated_depression'],
                          'unseen':r['unseen_depression']}),flush=True)
    for seed in SEEDS:
        for cue in ('A','B'):
            run(f'primary-{seed}-{cue}',seed=seed,repeated=cue,replay=True,dense=seed == SEEDS[0])
    for condition in ('freeze','silence_dan','remove_da_contacts','cut_feedback','matched_control',
                      'remove_pn_kc','remove_kc_mbon','shuffle_pn_weights','no_apl','no_ambiguous'):
        for cue in ('A','B'):
            run(f'control-{condition}-{cue}',repeated=cue,intervention=condition)
    for count in (0,1):
        for cue in ('A','B'):
            run(f'exposures-{count}-{cue}',repeated=cue,presentations=count)
    p = Parameters()
    variants = {'eta_half':replace(p,learning_rate=.04),'eta_double':replace(p,learning_rate=.16),
        'gain075':replace(p,fast_gain=.75),'gain125':replace(p,fast_gain=1.25),
        'threshold010':replace(p,kc_threshold=.1),'threshold020':replace(p,kc_threshold=.2),
        'feedback0':replace(p,feedback_gain=0),'feedback02':replace(p,feedback_gain=.2),
        'half_dt':replace(p,dt=.005),'recovery900':replace(p,recovery_tau=900),
        'recovery3600':replace(p,recovery_tau=3600),'apl05':replace(p,apl_gain=.5),
        'apl2':replace(p,apl_gain=2),'boundary_retained':replace(p,normalization='retained_inputs'),
        'boundary_roles':replace(p,normalization='retained_roles')}
    for name,params in variants.items():
        for cue in ('A','B'):
            run(f'sensitivity-{name}-{cue}',params=params,repeated=cue)
    summary = {'model':MODEL_VERSION,'circuit':circuit.manifest_hash,'runs':results,
        'performance':{'suite_wall_seconds':time.perf_counter()-start,
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if platform.system()=='Darwin' else 1024)},
        'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
                       'os':platform.platform(),'cpu_count':os.cpu_count()},
        'sources':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in
                   ('PLAN.md','model.py','experiment.py','requirements.txt')}}
    (work/'results.json').write_bytes(canonical(summary))
    manifest = {'circuit':circuit.manifest_hash,'files':{str(p.relative_to(work)):hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(work.rglob('*')) if p.is_file()}}
    raw = canonical(manifest)
    identity = hashlib.sha256(raw).hexdigest()
    (work/'evidence-manifest.json').write_bytes(raw)
    dest = output/identity
    dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists():
        raise ValueError('Never replace evidence')
    shutil.move(str(work),str(dest))
    print(json.dumps({'evidence':str(dest),'performance':summary['performance']},indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--circuit',type=Path,required=True)
    p.add_argument('--output',type=Path,default=HERE/'evidence')
    args = p.parse_args()
    suite(Circuit(args.circuit),args.output)

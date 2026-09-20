"""Snapshot and seeded replay audit using the frozen model, without altered parameters."""
import time
import numpy as np
from common import HERE, save, load, digest
from model import Model, Movie, trial


def main():
    out=[]
    for level in ['L0','L1']:
        c=load(f'circuits/{level}.json'); root=c['targets'][0]['root_id']
        task=dict(family='primary',level=level,target=root,stimulus='expand')
        save(f'replay/{level}_task.json',task)
        p=load('results/'+digest(task)+'.json')
        start=time.perf_counter()
        metric,read,_,_,final=trial(c,root,full=False)
        saved=np.load(HERE/p['trace_path'])['measurements']
        delta=float(np.max(np.abs(read-saved)))
        m=Model(c); center=np.array(c['targets'][0]['center_xy'])*m.p['spacing']
        movie=Movie('expand',center,m.p['dt'])
        split=movie.steps//2
        for _ in range(split):m.step(movie.intensity(m.points,m.step_index*m.p['dt']))
        s=m.snapshot(); checkpoint_start=time.perf_counter()
        save(f'replay/{level}_midpoint.json',s)
        checkpoint_seconds=time.perf_counter()-checkpoint_start
        tail=[]
        while m.step_index<movie.steps:tail.append(m.step(movie.intensity(m.points,m.step_index*m.p['dt']))[0].copy())
        end=m.snapshot(); restored=Model(c); restored.restore(load(f'replay/{level}_midpoint.json'))
        repeat=[]
        while restored.step_index<movie.steps:repeat.append(restored.step(movie.intensity(restored.points,restored.step_index*restored.p['dt']))[0].copy())
        d=float(np.max(np.abs(np.asarray(tail)-repeat)))
        assert d<=1e-12 and delta<=1e-12
        assert digest(end)==digest(restored.snapshot())==digest(final)
        # The randomized null graph and randomized movie also reproduce from explicit seeds.
        _,a,_,_,sa=trial(c,root,'shuffle_time',intervention='shuffle_space',seed=29)
        _,b,_,_,sb=trial(c,root,'shuffle_time',intervention='shuffle_space',seed=29)
        assert digest(sa)==digest(sb)
        out.append({'level':level,'replay_max_abs':delta,'restored_tail_max_abs':d,
                    'randomized_seeded_replay_max_abs':float(np.max(np.abs(a-b))),
                    'all_final_state_and_prng_equal':True,'checkpoint_bytes':(HERE/f'replay/{level}_midpoint.json').stat().st_size,
                    'checkpoint_write_seconds':checkpoint_seconds,'wall_seconds':time.perf_counter()-start,
                    'readout_sha256':digest(read.tolist()),'snapshot_sha256':digest(final),
                    'fresh_process_result_path':f'replay/{level}_fresh.json'})
    save('RELIABILITY.json',out)


if __name__=='__main__':main()

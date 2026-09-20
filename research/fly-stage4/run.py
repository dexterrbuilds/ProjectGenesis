"""Execute the preregistered battery without optimization or downstream simulation."""
import argparse
import json
import time
import resource
import platform
import numpy as np
from common import HERE, load, save, sha, digest
from model import trial

PRIMARY=['expand','recede','dim','translate','grating_0','grating_90','grating_180','grating_270',
         'approach_20','approach_40','approach_80','bright','small','offset','shuffle_time','blank']
CRITICAL=['expand','recede','dim','grating_0','grating_90','grating_180','grating_270']
SENSITIVITY={'spacing3':{'spacing':3.},'spacing7':{'spacing':7.},'mirror':{'mirror':-1.},
             'axes_minus45':{'axis_angle':-45.},'axes_plus45':{'axis_angle':45.},
             'tau20ms':{'tau':.02},'tau100ms':{'tau':.1},'gain_half':{'gain':.5},'gain_double':{'gain':2.},
             'lpi_zero':{'lpi_gain':0.},'lpi_half':{'lpi_gain':.5},'lpi_double':{'lpi_gain':2.},
             'dt_half':{'dt':.0025},'retained_norm':{'normalization':'retained'}}
INTERVENTIONS=['route_remove','matched_route','lpi_remove','output_silence','shuffle_space','sensory_lesion','matched_sensory']


def execute(task):
    c=load('circuits/'+task['level']+'.json')
    start=time.perf_counter(); cpu=time.process_time()
    metric,read,states,inputs,snapshot=trial(c,task['target'],task['stimulus'],task.get('params'),task.get('intervention','intact'),task.get('seed',17),task['family']=='primary')
    metric|={'task':task,'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu}
    return metric,read,states,inputs,snapshot


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--fresh-task');ap.add_argument('--output');args=ap.parse_args()
    freeze=load('MODEL_FREEZE.json')
    for path,h in freeze['files'].items(): assert sha(HERE/path)==h,path
    if args.fresh_task:
        task=json.loads((HERE/args.fresh_task).read_text())
        metric,read,_,_,snapshot=execute(task)
        save(args.output,{'readout_sha256':digest(read.tolist()),'snapshot_sha256':digest(snapshot),
                          'peak':metric['peak'],'steps':metric['final_step'],'wall_seconds':metric['wall_seconds']})
        return
    tasks=[]
    for level in ['L0','L1']:
        for target in load('circuits/'+level+'.json')['targets']:
            root=target['root_id']
            for kind in PRIMARY:
                tasks.append(dict(family='primary',level=level,target=root,stimulus=kind))
            for name,p in SENSITIVITY.items():
                for kind in CRITICAL:
                    tasks.append(dict(family='sensitivity',arm=name,params=p,level=level,target=root,stimulus=kind))
            for intervention in INTERVENTIONS:
                for kind in ['expand','recede','grating_0']:
                    for seed in ([17,29,43] if intervention=='shuffle_space' else [17]):
                        tasks.append(dict(family='intervention',level=level,target=root,stimulus=kind,intervention=intervention,seed=seed))
    save('TASKS.json',tasks)
    start=time.perf_counter(); cpu=time.process_time(); results=[]
    (HERE/'traces').mkdir(exist_ok=True); (HERE/'results').mkdir(exist_ok=True)
    for index,task in enumerate(tasks):
        key=digest(task); out=HERE/f'results/{key}.json'
        if out.exists():
            metric=load(f'results/{key}.json')
            assert sha(HERE/metric['trace_path'])==metric['trace_sha256']
        else:
            metric,read,states,inputs,snapshot=execute(task)
            trace=HERE/f'traces/{key}.npz'
            assert not trace.exists(), 'Unexpected partial artifact; inspect instead of overwriting'
            arrays={'measurements':read}
            if states is not None: arrays|={'rates':states,'motion_inputs':inputs}
            np.savez_compressed(trace,**arrays)
            metric|={'trace_path':str(trace.relative_to(HERE)),'trace_sha256':sha(trace),
                     'readout_sha256':digest(read.tolist()),'final_snapshot_sha256':digest(snapshot)}
            save(f'results/{key}.json',metric)
        results.append(metric)
        if index%50==0: print(json.dumps({'completed':index+1,'total':len(tasks)}),flush=True)
    save('RESULTS.json',results)
    save('PERFORMANCE.json',{'trials':len(tasks),'wall_seconds_this_execution':time.perf_counter()-start,
         'cpu_seconds_this_execution':time.process_time()-cpu,'sum_trial_wall_seconds':sum(r['wall_seconds'] for r in results),
         'sum_trial_cpu_seconds':sum(r['cpu_seconds'] for r in results),'simulated_seconds':sum(r['duration_s'] for r in results),
         'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'platform':platform.platform(),
         'machine':platform.machine(),'python':platform.python_version(),'numpy':np.__version__,
         'trace_bytes':sum(p.stat().st_size for p in (HERE/'traces').glob('*.npz')),
         'neural_steps':sum(r['final_step'] for r in results),'note':'Single process; primary traces contain every rate and motion input. Other traces contain continuous target/sensory summaries, not synthesized activity.'})


if __name__=='__main__':main()

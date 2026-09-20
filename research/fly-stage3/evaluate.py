"""Quantitative audit of prespecified comparisons; no model fitting or decoding."""
import argparse,csv,gzip,hashlib,json,subprocess,sys,tempfile
from pathlib import Path
import numpy as np
from model import Circuit,Model,canonical
HERE=Path(__file__).resolve().parent

def relative(a,b):return None if abs(b)<=1e-8 else a/b-1

def evaluate(cp,ep,out):
    c=Circuit(cp);raw=(ep/'evidence-manifest.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==ep.name
    for name,h in json.loads(raw)['files'].items():assert hashlib.sha256((ep/name).read_bytes()).hexdigest()==h,name
    data=json.loads((ep/'results.json').read_text())
    for name,h in data['sources'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    runs={r['run']:r for r in data['runs']};groups=list(c.groups)
    paired=[]
    for key,low in runs.items():
        if not key.endswith('-0.2'):continue
        high=runs[key[:-3]+'0.8'];prefix=key[:-4]
        lt,ht=low['metrics']['trials'],high['metrics']['trials']
        paired.append({'condition':prefix,'cue':low['cue'],'seed':low['seed'],'sensory_exact':low['sensory_hash']==high['sensory_hash'],
            'state_contrast':{g:relative(lt[9]['maintained'][g],ht[9]['maintained'][g]) for g in groups},
            'experience_low':{g:relative(lt[9]['maintained'][g],lt[0]['maintained'][g]) for g in groups},
            'experience_high':{g:relative(ht[9]['maintained'][g],ht[0]['maintained'][g]) for g in groups},
            'quiet_fraction_low':{g:low['metrics']['quiet'][g]/max(1e-12,lt[0]['maintained'][g]) for g in groups},
            'quiet_fraction_high':{g:high['metrics']['quiet'][g]/max(1e-12,ht[0]['maintained'][g]) for g in groups},
            'low_baseline':lt[0]['maintained'],'high_baseline':ht[0]['maintained'],
            'low_last':lt[9]['maintained'],'high_last':ht[9]['maintained'],
            'reset_max_delta':max(low['reset_max_rate_delta'],high['reset_max_rate_delta'])})
    by={x['condition']:x for x in paired};primary=[x for x in paired if x['condition'].startswith('primary')]
    mechanisms=[]
    for pair in paired:
        if not pair['condition'].startswith('control-'):continue
        base=by[f"primary-3701-{pair['cue']}"]
        v=pair['state_contrast']['MB11'];b=base['state_contrast']['MB11']
        row={'condition':pair['condition'],'state_contrast':v,'reduction':None if v is None or b is None or b==0 else 1-v/b,
            'sensory_lesion_change':{g:max(abs(relative(pair[s][g],base[s][g]) or 0) for s in ('low_baseline','high_baseline'))
                                    for g in ('PN','KC')},
            'experience_low':pair['experience_low'],
            'LH_resource_contrast':pair['state_contrast']['LH']}
        mechanisms.append(row)
    acquisition=[]
    for q in ('A','B'):
        for b in (.2,.8):
            base=runs[f'primary-3701-{q}-{b}'];r=runs[f'protocol-acquisition-ten-intact-{q}-{b}']
            lesion=runs[f'protocol-acquisition-ten-silence_oa-{q}-{b}']
            nooa=runs[f'control-silence_oa-{q}-{b}']
            reduction={g:-(relative(r['metrics']['last_window'][g],base['metrics']['last_window'][g]) or 0) for g in groups}
            residual={g:-(relative(lesion['metrics']['last_window'][g],nooa['metrics']['last_window'][g]) or 0) for g in groups}
            acquisition.append({'cue':q,'resource':b,'suppression':reduction,'OA_lesion_suppression':residual,
                'sensory_exact':r['sensory_hash']==base['sensory_hash']})
    recall=[]
    with tempfile.TemporaryDirectory(prefix='fly-stage3-recall-') as temp:
        for r in data['runs']:
            if not r['run'].startswith('primary'):continue
            for snap,target in [('trained','post'),('fast-reset','fast_reset'),('initial','baseline')]:
                folder=ep/r['run']
                z=subprocess.run([sys.executable,str(HERE/'recall.py'),'--circuit',str(cp.resolve()),'--config',str((folder/'recall-config.json').resolve()),
                    '--snapshot',str((folder/f'{snap}.json.gz').resolve())],cwd=temp,env={'PYTHONDONTWRITEBYTECODE':'1'},text=True,capture_output=True,check=True)
                recall.append({'run':r['run'],'snapshot':snap,'exact':json.loads(z.stdout)==r[target]})
    boundary={}
    for g,ix in c.groups.items():
        b=c.boundary['per_neuron'];s={k:sum(b[c.ids[int(i)]][k] for i in ix) for k in ('retained_input','omitted_input','retained_output','omitted_output')}
        s['input_fraction']=s['retained_input']/(s['retained_input']+s['omitted_input']);s['output_fraction']=s['retained_output']/(s['retained_output']+s['omitted_output'])
        boundary[g]=s
    m=Model(c);plastic={}
    for name,mask in [('experience',m.learnable),('value_transfer',~m.learnable)]:
        ix=m.plastic_edges[mask];plastic[name]={'neuropil_rows':len(ix),'pairs':len(set(zip(c.pre[ix],c.post[ix]))),'contacts':int(c.count[ix].sum())}
    def ge(v,t):return v is not None and v>=t
    primaryruns=[r for r in data['runs'] if r['run'].startswith('primary')]
    mech=[r for r in mechanisms if any(r['condition'].startswith('control-'+x+'-') for x in ('silence_dan','remove_da_gate','freeze_modulation'))]
    matched=[r for r in mechanisms if r['condition'].startswith('control-matched_control-')]
    freeze=[r for r in mechanisms if r['condition'].startswith('control-freeze_plasticity-')]
    criteria={
        'all_sensory_inputs_matched':all(x['sensory_exact'] for x in paired),
        'all_nonzero_baselines':all(x['low_baseline'][g]>1e-8 and x['high_baseline'][g]>1e-8 for x in primary for g in ('MB11','LH')),
        'MB11_state_contrast_at_least_10pct':all(ge(x['state_contrast']['MB11'],.1) for x in primary),
        'PN_KC_state_preserved_5pct':all(abs(x['state_contrast'][g] or 0)<=.05 for x in primary for g in ('PN','KC')),
        'MB11_experience_decrease_at_least_5pct':all(x['experience_low']['MB11'] is not None and x['experience_low']['MB11']<=-.05 for x in primary),
        'LH_experience_increase_at_least_5pct':all(ge(x['experience_low']['LH'],.05) for x in primary),
        'mechanism_reduction_80pct_sensory_preserved':all(ge(x['reduction'],.8) and max(x['sensory_lesion_change'].values())<=.05 for x in mech),
        'matched_preserves_75pct':all(x['reduction'] is not None and x['reduction']<=.25 for x in matched),
        'plasticity_freeze_removes_experience_80pct':all(abs(x['experience_low']['MB11'] or 0)<=.2*abs(by['primary-3701-'+x['condition'][-1]]['experience_low']['MB11']) for x in freeze),
        'acquisition_MB11_and_LH_suppression_at_least_20pct':all(x['suppression']['MB11']>=.2 and x['suppression']['LH']>=.2 for x in acquisition),
        'OA_lesion_removes_MB11_suppression_80pct':all(abs(x['OA_lesion_suppression']['MB11'])<=.2*abs(x['suppression']['MB11']) for x in acquisition),
        'no_cue_sham_zero':all(max(abs(v) for v in r['metrics']['last_window'].values())<1e-12 for r in data['runs'] if r['history']=='sham'),
        'all_restores_exact':all(r['restoration_exact'] for r in data['runs']),
        'all_primary_resets_1e_10':all(r['reset_max_rate_delta']<=1e-10 for r in primaryruns),
        'all_primary_replays_exact':all(r['replay_exact'] for r in primaryruns),
        'all_36_fresh_recalls_exact':len(recall)==36 and all(x['exact'] for x in recall),
        'modest_sensitivity_state_direction':all(ge(x['state_contrast']['MB11'],0) for x in paired if x['condition'].startswith('sensitivity') and not any(s in x['condition'] for s in ('retained','roles','oa_'))),
        'global_gain_negative_control_detected':all(abs(x['state_contrast']['PN'] or 0)>.05 for x in paired if x['condition'].startswith('control-global_gain'))}
    # Structural interventions: report sign/scale, do not reward a reversed decoder.
    for cond in ('silence_mb11','silence_mb18','remove_mb11_mb18','remove_mb18_lh'):
        vv=[x for x in mechanisms if x['condition'].startswith('control-'+cond+'-')]
        criteria[cond+'_reduces_LH_interaction_80pct']=all(
            x['LH_resource_contrast'] is not None and abs(x['LH_resource_contrast'])<=.2*abs(by['primary-3701-'+x['condition'][-1]]['state_contrast']['LH'] or 0) for x in vv)
    integrity=all(criteria[k] for k in ('all_sensory_inputs_matched','all_restores_exact','all_primary_resets_1e_10',
                                      'all_primary_replays_exact','all_36_fresh_recalls_exact'))
    causal=all(ge(x['state_contrast']['MB11'],1e-10) for x in primary) and criteria['mechanism_reduction_80pct_sensory_preserved']
    status='PASS' if all(criteria.values()) else ('PARTIAL-INCONCLUSIVE' if integrity and causal else 'FAIL')
    result={'classification':status,'criteria':criteria,'counts':c.manifest['counts'],'plastic_counts':plastic,'boundary':boundary,
        'paired_comparisons':paired,'interventions':mechanisms,'acquisition':acquisition,'fresh_recalls':recall,
        'performance':data['performance'],'circuit':c.manifest_hash,'evidence':ep.name,
        'evaluator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    raw=canonical(result);dest=out/hashlib.sha256(raw).hexdigest();dest.mkdir(parents=True,exist_ok=True)
    file=dest/'evaluation.json'
    if file.exists():assert file.read_bytes()==raw
    else:file.write_bytes(raw)
    with (HERE/'RESULTS.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['condition','MB11_resource_contrast','LH_resource_contrast','MB11_experience_low','LH_experience_low','PN_resource_contrast','KC_resource_contrast','reset_max_delta'])
        for x in paired:w.writerow([x['condition'],x['state_contrast']['MB11'],x['state_contrast']['LH'],x['experience_low']['MB11'],x['experience_low']['LH'],x['state_contrast']['PN'],x['state_contrast']['KC'],x['reset_max_delta']])
    print(json.dumps({'classification':status,'criteria':criteria,'evaluation':str(file)},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--circuit',type=Path,required=True);p.add_argument('--evidence',type=Path,required=True)
    p.add_argument('--output',type=Path,default=HERE/'evaluations');a=p.parse_args();evaluate(a.circuit,a.evidence,a.output)

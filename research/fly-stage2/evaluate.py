"""Audit saved evidence; threshold failure is a scientific result, not a software test failure."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import numpy as np
from model import Circuit,Model,canonical

HERE=Path(__file__).resolve().parent


def evaluate(circuit_path,evidence,output):
    c=Circuit(circuit_path)
    raw=(evidence/'evidence-manifest.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==evidence.name
    manifest=json.loads(raw)
    for name,h in manifest['files'].items():
        assert hashlib.sha256((evidence/name).read_bytes()).hexdigest()==h,name
    results=json.loads((evidence/'results.json').read_text())
    assert results['circuit']==c.manifest_hash
    for name,h in results['sources'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    runs={r['run']:r for r in results['runs']}
    primary=[r for r in runs.values() if r['run'].startswith('primary')]
    recall=[]
    with tempfile.TemporaryDirectory(prefix='fly-stage2-recall-') as temp:
        for r in primary:
            dest=evidence/r['run']
            for snapshot,key in [('trained','post'),('fast-reset','fast_reset'),('initial','baseline')]:
                completed=subprocess.run([sys.executable,str(HERE/'recall.py'),'--circuit',str(circuit_path.resolve()),
                    '--config',str((dest/'recall-config.json').resolve()),'--snapshot',str((dest/f'{snapshot}.json.gz').resolve())],
                    env={'PYTHONDONTWRITEBYTECODE':'1'},cwd=temp,text=True,capture_output=True,check=True)
                recalled=json.loads(completed.stdout)
                recall.append({'run':r['run'],'snapshot':snapshot,'exact':recalled==r[key]})
    boundary={}
    for g,ids in c.groups.items():
        b=c.boundary['per_neuron']
        s={k:sum(b[c.ids[int(i)]][k] for i in ids) for k in
           ('retained_input','omitted_input','retained_output','omitted_output')}
        s['input_retention']=s['retained_input']/(s['retained_input']+s['omitted_input'])
        s['output_retention']=s['retained_output']/(s['retained_output']+s['omitted_output'])
        s['min_individual_input_retention']=min(b[c.ids[int(i)]]['retained_input']/max(1,c.full_input[i]) for i in ids)
        s['max_individual_input_retention']=max(b[c.ids[int(i)]]['retained_input']/max(1,c.full_input[i]) for i in ids)
        boundary[g]=s
    interventions=[]
    for r in runs.values():
        if not r['run'].startswith('control-'):
            continue
        reference=runs[f"primary-2701-{r['repeated']}"]
        sensory={g:max(abs(r['baseline'][cue]['groups'][g]/reference['baseline'][cue]['groups'][g]-1)
                       for cue in ('A','B')) for g in ('PN','KC')}
        interventions.append({'condition':r['intervention'],'cue':r['repeated'],'specificity':r['specificity'],
            'specificity_reduction':None if r['specificity'] is None else 1-r['specificity']/reference['specificity'],
            'max_baseline_sensory_relative_change':sensory})
    m=Model(c)
    identities={g:[{'root':c.ids[int(i)],'type':c.nodes[i]['cell_type'],'side':c.nodes[i]['side']}
                   for i in ids] for g,ids in c.groups.items() if g not in ('KC','PN')}
    matrix={}
    for e,pre,post in zip(c.edges,c.pre,c.post):
        key=c.roles[pre]+'->'+c.roles[post]
        matrix[key]=matrix.get(key,0)+e['synapses']
    mechanism=[x for x in interventions if x['condition'] in ('freeze','silence_dan','remove_da_contacts')]
    matched=[x for x in interventions if x['condition']=='matched_control']
    criteria={
        'all_primary_baselines_nonzero':all(r['baseline'][q]['groups']['MBON']>1e-8 for r in primary for q in ('A','B')),
        'all_repeated_depression_at_least_005':all(r['repeated_depression']>=.05 for r in primary),
        'all_specificity_at_least_003':all(r['specificity']>=.03 for r in primary),
        'all_unseen_depression_at_most_002':all(r['unseen_depression']<=.02 for r in primary),
        'all_primary_effects_positive':all(r['specificity']>0 for r in primary),
        'all_replay_exact':all(r['replay_exact'] for r in primary),
        'all_original_restorations_exact':all(r['restoration_exact'] for r in runs.values()),
        'all_primary_reset_preserved_at_1e_10':all(r['fast_reset_max_rate_delta']<=1e-10 for r in primary),
        'all_fresh_process_recalls_exact':all(r['exact'] for r in recall),
        'mechanism_reduction_80pct_with_sensory_preserved':all(x['specificity_reduction']>=.8 and
                         max(x['max_baseline_sensory_relative_change'].values())<=.1 for x in mechanism),
        'matched_preserves_75pct':all(x['specificity_reduction']<=.25 for x in matched),
        'primary_sensory_and_control_stable':all(abs(v or 0)<.1 for r in primary
                               for group in r['sensory_relative_change'].values() for v in group.values())}
    classification='PASS' if all(criteria.values()) else 'PARTIAL-INCONCLUSIVE' if criteria['all_primary_effects_positive'] and criteria['all_fresh_process_recalls_exact'] else 'FAIL'
    row_counts={'rows':len(m.plastic_edges),'directed_pairs':len(set(zip(m.plastic_pre,m.plastic_post))),
                'contacts':int(c.count[m.plastic_edges].sum())}
    # Exact local causal readout audit, not merely a ratio of population means.
    cell_effects=[]
    for r in primary:
        cue=r['repeated']
        for root,b in r['baseline'][cue]['mbon'].items():
            a=r['post'][cue]['mbon'][root]
            cell_effects.append({'run':r['run'],'root':root,'baseline':b,'post':a,
                                'absolute_change':b-a,'depression':1-a/b if b>1e-8 else None})
    analysis={'classification':classification,'criteria':criteria,'circuit':c.manifest_hash,'evidence':evidence.name,
         'counts':c.manifest['counts'],'plastic':row_counts,'boundary':boundary,'identities':identities,
         'retained_contacts_by_role':matrix,'interventions':interventions,'cell_effects':cell_effects,
         'fresh_process_recalls':recall,'performance':results['performance'],
         'notes':['A nonzero local effect is not the predefined effect-size PASS.',
                  'Recovery follows an assumed relaxation law; not independently established physiology.',
                  'Boundary normalization brackets do not reconstruct omitted sensory input.',
                  'Cue current cardinality/amplitude is matched; network baseline responses are not tuned to match.'],
         'evaluator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    raw=canonical(analysis)
    dest=output/hashlib.sha256(raw).hexdigest()
    dest.mkdir(parents=True,exist_ok=True)
    p=dest/'evaluation.json'
    if p.exists():
        assert p.read_bytes()==raw
    else:
        p.write_bytes(raw)
    with (HERE/'RESULTS.csv').open('w',newline='') as f:
        fields=['run','seed','repeated','intervention','presentations','repeated_depression','unseen_depression',
                'specificity','reset_depression','max_plastic_change','mean_plastic_change','plastic_rows_changed',
                'restoration_exact','replay_exact','fast_reset_max_rate_delta','wall_seconds']
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore')
        writer.writeheader();writer.writerows(runs.values())
    print(json.dumps({'classification':classification,'criteria':criteria,'evaluation':str(p)},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--circuit',type=Path,required=True)
    parser.add_argument('--evidence',type=Path,required=True)
    parser.add_argument('--output',type=Path,default=HERE/'evaluations')
    a=parser.parse_args()
    evaluate(a.circuit,a.evidence,a.output)

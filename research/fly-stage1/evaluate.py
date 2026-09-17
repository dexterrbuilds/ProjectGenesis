"""Audit saved evidence and perform cue-only fresh-process recall. No retraining."""
import argparse
import collections
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import shutil

import numpy as np

from model import Circuit, Model, canonical

HERE = Path(__file__).resolve().parent


def evaluate(circuit_path, evidence_path, output):
    c = Circuit(circuit_path)
    manifest_bytes = (evidence_path/'evidence-manifest.json').read_bytes()
    assert hashlib.sha256(manifest_bytes).hexdigest() == evidence_path.name
    manifest = json.loads(manifest_bytes)
    for file, digest in manifest['files'].items():
        assert hashlib.sha256((evidence_path/file).read_bytes()).hexdigest() == digest, file
    evidence = json.loads((evidence_path/'results.json').read_text())
    assert evidence['circuit'] == c.manifest_hash
    for name, digest in evidence['sources'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest() == digest, name
    rows = {r['run']: r for r in evidence['runs']}
    core = [r for r in rows.values() if r['run'].startswith('app-') and r['run'].endswith('-intact')]
    sensitivity = [r for r in rows.values() if r['run'].startswith('sensitivity-')]
    checks = {}
    checks['six_counterbalanced_primary_conditions'] = len(core) == 6
    checks['all_primary_meet_10pct_depression_5pp_selectivity'] = all(
        r['paired_depression'] >= .10 and r['selective_depression'] >= .05 for r in core)
    checks['primary_restore_exact'] = all(r['restoration_exact'] for r in core)
    checks['plastic_state_survives_fast_reset'] = all(
        abs(r['paired_depression']-r['plastic_only_depression']) < 1e-10 for r in core)
    checks['all_requested_replays_exact'] = all(r['replay_exact'] for r in rows.values() if r['replay_exact'] is not None)
    comparisons = []
    for cue in ('A', 'B'):
        base = rows[f'app-1701-{cue}-intact']
        for control in ('freeze', 'silence_dan', 'remove_da_contacts', 'unpaired', 'single_dan', 'matched_dan',
                        'no_apl', 'no_recurrence', 'shuffle_pn_weights'):
            r = rows[f'app-1701-{cue}-{control}']
            reduction = 1-r['selective_depression']/base['selective_depression']
            sensory_change = r['post'][cue]['KC']/base['post'][cue]['KC']-1
            comparisons.append({'paired': cue, 'control': control,
                'selectivity_reduction_fraction': reduction, 'kc_response_change_fraction': sensory_change,
                'lesion_size': len(r['lesioned_roots']),
                'baseline_mbon_response_change_fraction': r['baseline'][cue]['MBON_app']/base['baseline'][cue]['MBON_app']-1})
            if control in ('freeze', 'silence_dan', 'remove_da_contacts'):
                checks[f'{cue}_{control}_selective_loss'] = reduction >= .8 and abs(sensory_change) <= .1
            if control == 'unpaired':
                checks[f'{cue}_temporal_pairing_required'] = abs(r['selective_depression']) < 1e-10
        relevant = rows[f'app-1701-{cue}-single_dan']
        unrelated = rows[f'app-1701-{cue}-matched_dan']
        checks[f'{cue}_equal_size_lesion_specificity'] = (len(relevant['lesioned_roots']) == len(unrelated['lesioned_roots']) == 1
            and relevant['selective_depression'] < unrelated['selective_depression']
            and abs(unrelated['selective_depression']-base['selective_depression']) < 1e-10)
        checks[f'{cue}_pn_kc_required'] = rows[f'app-1701-{cue}-remove_pn_kc']['baseline'][cue]['KC'] == 0
        checks[f'{cue}_kc_mbon_required'] = rows[f'app-1701-{cue}-remove_kc_mbon']['baseline'][cue]['MBON_app'] == 0
    checks['all_sensitivity_conditions_retain_effect'] = all(
        r['paired_depression'] >= .1 and r['selective_depression'] >= .05 for r in sensitivity)

    boundary = json.loads((c.directory/'boundary.json').read_text())
    sums = collections.defaultdict(collections.Counter)
    for node in c.nodes:
        sums[node['role']].update(boundary['per_neuron'][node['root_id']])
    boundary_groups = {g: {**v, 'input_retention': v['retained_input']/(v['retained_input']+v['omitted_input']),
                           'output_retention': v['retained_output']/(v['retained_output']+v['omitted_output'])}
                       for g, v in sums.items()}
    m = Model(c)
    plastic_counts = {}
    for i, comp in enumerate(('app', 'av')):
        idx = m.plastic_edges[m.plastic_compartment == i]
        plastic_counts[comp] = {'neuropil_groups': len(idx),
            'directed_pairs': len({(int(c.pre[k]), int(c.post[k])) for k in idx}),
            'anatomical_contacts': int(c.count[idx].sum()),
            'kc_with_dan_contacts': int(np.count_nonzero(np.asarray(m.da_operators[i].sum(axis=1)).ravel()))}

    work = Path(tempfile.mkdtemp(prefix='fly-stage1-evaluation-'))
    recall_results = []
    # Recall each primary cue in a clean interpreter: only circuit, numeric PN currents,
    # and initial/trained neural snapshots. No result table or training protocol is passed.
    for row in core:
        run = row['run']
        stimuli = json.loads((evidence_path/run/'stimuli.json').read_text())
        for cue, event in zip(('A', 'B'), stimuli['events'][:2]):
            current_file = work/f'{run}-{cue}-current.json'
            current_file.write_bytes(canonical(event['currents']))
            for state, expected_key in (('initial', 'baseline'), ('trained', 'post')):
                out = work/f'{run}-{cue}-{state}-recall.json'
                subprocess.run([sys.executable, str(HERE/'recall.py'), '--circuit', str(c.directory),
                    '--snapshot', str(evidence_path/run/f'{state}.json.gz'), '--currents', str(current_file),
                    '--output', str(out)], check=True,
                    env={'PATH': os.environ.get('PATH', ''), 'PYTHONHASHSEED': '0'})
                observed = json.loads(out.read_text())
                difference = max(abs(observed['group_rates'][g]-row[expected_key][cue][g]) for g in c.groups)
                recall_results.append({'run': run, 'cue': cue, 'state': state,
                                       'maximum_group_difference': difference, 'file': out.name})
    checks['fresh_process_cue_only_recall_matches'] = all(x['maximum_group_difference'] <= 1e-10 for x in recall_results)
    # Inspect individual MBONs, avoiding a population-average/readout artifact.
    individual = []
    for r in core:
        cue = r['paired']
        before = json.loads((work/f"{r['run']}-{cue}-initial-recall.json").read_text())['neuron_rates']
        after = json.loads((work/f"{r['run']}-{cue}-trained-recall.json").read_text())['neuron_rates']
        individual.append({'run': r['run'], 'neurons': [
            {'root': c.ids[i], 'before': before[c.ids[i]], 'after': after[c.ids[i]],
             'depression': 1-after[c.ids[i]]/before[c.ids[i]]} for i in c.groups['MBON_app']]})
    checks['individual_output_neurons_depress'] = all(n['depression'] > .1 for r in individual for n in r['neurons'])
    result = {'classification': 'PASS' if all(checks.values()) else 'PARTIAL / INCONCLUSIVE',
              'scope': 'Appetitive association in this connectome-constrained model, not full fly behavior or biological validation.',
              'aversive_classification': 'PARTIAL / INCONCLUSIVE: modeled effect exists, but only 17.6% of MBON input retained; no full aversive circuit claim.',
              'checks': checks, 'comparisons': comparisons, 'boundary': boundary_groups,
              'plastic_counts': plastic_counts, 'fresh_process_recall': recall_results,
              'individual_mbon_responses': individual, 'verified_evidence_files': len(manifest['files']),
              'evidence_manifest': evidence_path.name, 'circuit_manifest': c.manifest_hash,
              'evaluation_sources': {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                                     for name in ('evaluate.py', 'recall.py')}}
    (work/'evaluation.json').write_bytes(canonical(result))
    audit = {'files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(work.iterdir())}}
    raw = canonical(audit)
    identity = hashlib.sha256(raw).hexdigest()
    (work/'evaluation-manifest.json').write_bytes(raw)
    dest = output/identity
    if dest.exists():
        raise ValueError('Refusing to overwrite evaluation')
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(work), str(dest))
    print(json.dumps({'classification': result['classification'], 'checks': checks,
                      'evaluation': str(dest), 'plastic_counts': plastic_counts}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--circuit', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=HERE/'evaluations')
    args = parser.parse_args()
    evaluate(args.circuit.resolve(), args.evidence.resolve(), args.output)

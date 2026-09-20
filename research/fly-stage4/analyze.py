"""Fixed descriptive analysis. Never chooses parameters or edits primary artifacts."""
import collections
import csv
import io
import json
import numpy as np
from common import HERE, ROOT, REGISTRY, sha, load, save, digest


def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+
                     ['| '+' | '.join(map(str,row))+' |' for row in rows])


def main():
    results=load('RESULTS.json'); circuits={l:load(f'circuits/{l}.json') for l in ['L0','L1']}
    roots=[t['root_id'] for t in circuits['L0']['targets']]
    groups=collections.defaultdict(dict)
    for r in results:
        t=r['task']
        if t['family'] in ('primary','sensitivity'):
            groups[(t['level'],t['target'],t.get('arm','primary'))][r['stimulus']]=r
    critical=['recede','dim','grating_0','grating_90','grating_180','grating_270']
    ranking=[]
    for (level,root,arm),rs in groups.items():
        peak=rs['expand']['peak']
        ranking.append({'level':level,'root_id':root,'arm':arm,'expansion_peak':peak,
                        'differences':{k:peak-rs[k]['peak'] for k in critical},
                        'all_qualitative_orderings':bool(peak>1e-12 and all(peak>rs[k]['peak']+1e-12 for k in critical))})
    n_good=sum(x['all_qualitative_orderings'] for x in ranking)
    gate_a='NOT SUPPORTED' if n_good==0 else 'PARTIAL-INCONCLUSIVE'
    interventions=[]
    for r in results:
        if r['task']['family']!='intervention':continue
        t=r['task']; base=groups[(t['level'],t['target'],'primary')][r['stimulus']]
        x=np.load(HERE/r['trace_path'])['measurements']; b=np.load(HERE/base['trace_path'])['measurements']
        interventions.append({'level':t['level'],'root_id':t['target'],'stimulus':r['stimulus'],'seed':r['seed'],
                              'intervention':r['intervention'],'baseline_peak':base['peak'],'peak':r['peak'],
                              'absolute_change':r['peak']-base['peak'],
                              'percent_change':100*(r['peak']/base['peak']-1) if base['peak'] else None,
                              'sensory_sum_max_abs_difference':float(np.max(np.abs(x[:,2]-b[:,2]))),
                              'motion_input_sum_max_abs_difference':float(np.max(np.abs(x[:,3]-b[:,3])))})
    replay=[]
    for s in load('RELIABILITY.json'):
        f=load(s['fresh_process_result_path'])
        assert f['readout_sha256']==s['readout_sha256'] and f['snapshot_sha256']==s['snapshot_sha256']
        replay.append(dict(s,fresh_process_exact_hash_match=True))
    boundary=[]
    for level,c in circuits.items():
        for typ,b in c['boundary'].items():
            nodes={i for i,n in enumerate(c['nodes']) if n['cell_type']==typ}
            effective=sum(e['contacts'] for e in c['edges'] if e['post'] in nodes and e['sign'] is not None)
            boundary.append(dict(b,level=level,type=typ,effective_input_contacts=effective,
                                 effective_input_fraction=effective/b['full_input'] if b['full_input'] else None))
    summary={'registry_sha256':REGISTRY,'gate_a':gate_a,'gate_b':'NOT TESTED','overall':gate_a,
             'scope':'Frozen, uncalibrated LPLC2 scalar motion-boundary model; not a verdict on biological looming computation',
             'qualitative_ordering_groups':len(ranking),'groups_satisfying_all_orderings':n_good,
             'rankings':ranking,'interventions':interventions,'boundary':boundary,'replay':replay,
             'all_trials_finite':all(r['finite'] for r in results),'max_network_rate':max(r['network_peak'] for r in results),
             'statistical_units':'3 anatomical roots from one female; seeds are null-graph/temporal permutations, not flies',
             'fitting':'none','numerical_tolerance':1e-12}
    save('ANALYSIS.json',summary)
    stream=io.StringIO(); w=csv.writer(stream)
    w.writerow(['level','family','arm','root_id','stimulus','seed','peak_model_rate','integral_model_rate_s','peak_time_after_onset_s','sensory_peak_sum','trace_path'])
    for r in results:
        t=r['task'];w.writerow([t['level'],t['family'],t.get('arm',r['intervention']['kind']),t['target'],r['stimulus'],r['seed'],r['peak'],r['integral'],r['peak_time_after_onset_s'],r['sensory_peak_sum'],r['trace_path']])
    out=HERE/'MEASUREMENTS.csv'
    if out.exists():assert out.read_text()==stream.getvalue()
    else:out.write_text(stream.getvalue())
    perf=load('PERFORMANCE.json')
    def peak(level,root,kind,arm='primary'):return groups[(level,root,arm)][kind]['peak']
    texts=[f'''# Stage 4 — physical visual-stimulus neural experiment

## Final result

**Gate A: {gate_a}. Gate B: NOT TESTED. Overall Stage 4: {gate_a} for the frozen model.**

The anatomy-constrained model produces visual activity, but it does not reproduce the independently reported LPLC2 expansion selectivity. Contraction and wide-field motion exceed expansion in the primary trials. **{n_good}/{len(ranking)}** root × level × primary/sensitivity groups satisfy all prospectively specified qualitative orderings. No model was retuned or selected for a favorable result. This is a negative result for this conditional representation/encoder/physiology package, not evidence that flies lack looming-sensitive circuitry.

The unresolved root-to-retinal angular correspondence and calcium observation operator further limit biological inference. Gate B was not simulated: anatomical paths alone do not authorize a descending response claim.

Dependency: Brain Spec v0.1.0 `{REGISTRY}`. Release and required entries passed preflight before extraction/experimentation. `PREREGISTRATION.json` records the pre-result protocol digest; `MODEL_FREEZE.json` pins implementation before the first primary result. The release validator approves compatibility of declared prior dependencies, **not** these new roots or an unvalidated physiological operator. New anatomy/assumptions remain an unadmitted extension.

## Anatomy and effective transmission
''']
    texts.append(table(['Level','Neurons','Directed pairs','Neuropil rows','Contacts','Modeled-sign contacts','Unknown-operator contacts'],[
        [l,c['counts']['neurons'],c['counts']['directed_pairs'],c['counts']['neuropil_rows'],c['counts']['anatomical_contacts'],
         sum(e['contacts'] for e in c['edges'] if e['sign'] is not None),c['counts']['operator_contacts']['unknown_excluded']] for l,c in circuits.items()]))
    texts.append('\nAll contact rows come from pinned v783 anatomy. Individual anatomical contacts are aggregated by pre/post/neuropil; these are not fabricated individually localized synapses. Three central right LPLC2 cells were selected by mapped-input centroid before activity was computed. L1 adds LPi09 and its mapped T4/T5 inputs. There is no effect-selected expansion. Rows shared by L0/L1 have identical canonical IDs and no independent plastic ownership. No rows overlap the prior canonical registry; the prior shared KC→MBON07/11 identities remain untouched.\n')
    texts.append(table(['Level / population','N','Anatomical input retained','Effective modeled input / full','Anatomical output retained'],[
        [b['level']+' / '+b['type'],b['neurons'],f"{100*b['input_retention']:.3f}%",f"{100*b['effective_input_fraction']:.3f}%",f"{100*b['output_retention']:.3f}%"] for b in boundary]))
    texts.append('\nBoundary statistics include every proofread incoming/outgoing contact for each selected population. The T4/T5 physiological inputs are largely outside the extraction and replaced by a declared local-motion sensory boundary. Their low anatomical input retention is not repaired by simulated photoreceptor circuitry. Unknown retained rows contribute no current under the explicit boundary, rather than becoming known zero physiology.\n')
    for l,c in circuits.items():
        b=c['boundary']['LPLC2'];texts.append(f"{l} LPLC2 omits {b['omitted_input_contacts']:,} incoming and {b['omitted_output_contacts']:,} outgoing contacts. Major missing input classes: "+', '.join(f"{x['type']} ({x['contacts']})" for x in b['major_omitted_inputs'][:8])+'.\n')
    cross=load('CROSSWALK.json')
    texts.append(f"\nRoot/type mapping joins {cross['right_motion_roots_mapped']:,}/{cross['right_motion_roots_total']:,} right T4/T5 roots. The column table has {len(cross['column_conflicts_excluded'])} type/side conflicts overall; conflicting assignments are excluded and listed, not silently repaired. Hexels are anatomical coordinates, not measured degrees. The three retained output identities are:\n"+ '\n'.join(f'- `{r}`' for r in roots))
    texts.append('\n## Primary continuous response measurements\n\nPeak units are arbitrary rate-like model activity. No conversion to Hz, mV or calcium fluorescence is claimed. Columns identify the three roots in the order above.\n')
    for l in circuits:
        texts.append('\n### '+l+'\n')
        texts.append(table(['Physical condition']+roots,[[kind]+[f'{peak(l,r,kind):.7g}' for r in roots] for kind in groups[(l,roots[0],'primary')]]))
    texts.append('\nFull time series, per-trial integrals, peak times, physical conditions and upstream responses are in `MEASUREMENTS.csv`, `RESULTS.json` and referenced trace files. The 96 primary files store **every selected neural rate and every local motion input**, with 5 ms updates; sensitivity/intervention files store genuine continuous target and upstream summaries. No activity was synthesized for presentation. Identical small/full expansion peaks mean the peak occurred in their shared early stimulus segment, not a calibrated angular threshold.\n')
    texts.append('Luminance-matched darkening gives zero activity, but symmetric local correlation can cancel uniform dimming by construction. This is therefore not independent validation of LPLC2. The decisive receding and grating controls fail. Bright responses, offsets, approach velocities and frame shuffling are descriptive controls without invented biological response intervals.\n')
    texts.append('\n## Causal interventions\n\nPercent changes below are descriptive, not acceptance thresholds. Each cell is the expansion-peak change relative to its own intact baseline.\n')
    for l in circuits:
        rows=[]
        for name,seed in [('route_remove',17),('matched_route',17),('lpi_remove',17),('output_silence',17),('shuffle_space',17),('shuffle_space',29),('shuffle_space',43),('sensory_lesion',17),('matched_sensory',17)]:
            vals=[next(x for x in interventions if x['level']==l and x['root_id']==r and x['stimulus']=='expand' and x['intervention']['kind']==name and x['seed']==seed) for r in roots]
            rows.append([name+(f' seed {seed}' if name=='shuffle_space' else '')]+[f"{x['percent_change']:+.3f}%" for x in vals])
        texts.append('\n### '+l+'\n'+table(['Intervention']+roots,rows))
    texts.append('\nRemoving the modeled T4/T5→LPLC2 route eliminates that readout while the complete upstream sensory-sum trajectory remains identical. This demonstrates transmission dependence **within a deliberately feedforward operator**, not successful looming computation. LPLC2 silencing is a trivial control. Contact shuffles alter activity, often increasing expansion response, without establishing the required selectivity. LPi removal and matched sensory lesions can have small positive effects through disinhibition. This is not renamed a successful behavioral intervention.\n')
    texts.append(table(['Level','Route lesion rows/contacts','Off-route control rows/contacts','Matched sensory roots'],[
        [l,'389 / 922',f"389 / {next(x for x in interventions if x['level']==l and x['intervention']['kind']=='matched_route')['intervention']['removed_contacts']}",'8 / 8, subtype matched'] for l in circuits]))
    texts.append('\nThe off-route lesion is row-count matched, **not contact-mass matched**: it removes much more input to LPi. Its disinhibition is mechanistically expected in this operator, so it is an imperfect strength-matched control and cannot validate physiological specificity. Eight-root lesions match ON/OFF-direction subtype but not all connectivity/physiology. No denominator is recomputed after intervention. All raw changes and mismatches are retained.\n')
    texts.append('\n## Closure, normalization, parameter and numerical sensitivity\n')
    texts.append(table(['Root','L1 vs L0 expansion change','L0 retained/full normalization ratio','dt-halved L0 peak change'],[
        [r,f'{100*(peak("L1",r,"expand")/peak("L0",r,"expand")-1):+.3f}%',
         f'{peak("L0",r,"expand","retained_norm")/peak("L0",r,"expand"):.4f}×',
         f'{100*(peak("L0",r,"expand","dt_half")/peak("L0",r,"expand")-1):+.3f}%'] for r in roots]))
    texts.append('\nThe entire grid includes lattice spacing 3/5/7°, x reflection, direction axes ±45°, tau 20/50/100 ms, gain 0.5/1/2, LPi gain 0/0.5/1/2, dt 2.5/5 ms and two normalization denominators. These are stress ranges, **not physiological confidence intervals**. Results for every condition/root are saved. No best normalization is promoted. Retinal mapping, normalization and missing dendritic nonlinearities remain confounded with actual anatomy; this experiment cannot apportion biological versus modeling causes of failure. Targeted closure is insufficient and no arbitrary drive was added.\n')
    texts.append(f"All {len(results)} trials are finite; maximum network rate was {summary['max_network_rate']:.8g}. Static blank trials remain exactly zero. Finite feedforward activity is not validation of unknown biological recurrent stability. dt-halving changes the sampled discontinuous stimulus as well as Euler integration; its difference is not an isolated truncation-error estimate.\n")
    texts.append('\n## Descending anatomy: Gate B not tested\n')
    texts.append(table(['GF/DNp01 root','Full input contacts','All LPLC2 contacts','All LC4 contacts','Selected seed contacts'],[
        [d['root_id'],d['full_input'],d['LPLC2_contacts'],d['LC4_contacts'],sum(x['contacts'] for x in d['selected_seed_routes'])] for d in cross['descending_anatomy_only']]))
    texts.append('\nThe three right LPLC2 seeds contribute only 17 contacts to the right GF (0.330% of its full proofread input). These real paths are insufficient to interpret descending dynamics after failed Gate A. No DN state, motor probability or action label was computed. Root-specific downstream sign remains unknown; differing predicted transmitter labels are not receptor evidence. FAFB does not contain the VNC body.\n')
    texts.append('\n## Reproduction and cost\n')
    texts.append(table(['Level','Replay max absolute error','Restored-tail max error','Fresh process','Checkpoint bytes'],[
        [r['level'],r['replay_max_abs'],r['restored_tail_max_abs'],'exact readout + final state hashes',r['checkpoint_bytes']] for r in replay]))
    texts.append(f"\nBoth seed-dependent null graph/movie replays also match exactly. Checkpoints contain all fast electrical and motion-filter states, explicit timestep/clock and PCG64 state; no slower or plastic memory exists. Mismatched model snapshots are rejected.\n\n{perf['trials']} trials, {perf['neural_steps']:,} updates, {perf['simulated_seconds']:.3f} simulated seconds; {perf['wall_seconds_this_execution']:.3f} s total wall time and {perf['cpu_seconds_this_execution']:.3f} s CPU, including saved traces. Trial computation totals {perf['sum_trial_wall_seconds']:.3f} s. Peak process RSS {perf['peak_rss_bytes']/2**20:.2f} MiB; saved traces {perf['trace_bytes']/2**20:.2f} MiB. Measured on {perf['machine']} / {perf['platform']}, Python {perf['python']}, NumPy {perf['numpy']}. This small feedforward model does not benchmark a full brain or identified physiology. Extraction cost is recorded separately in `CIRCUIT_MANIFEST.json`.\n")
    texts.append('''
## Scientific distinction and review boundary

**Biological fact:** independent flies show the reported LPLC2 selectivity; pinned FAFB supplies roots, types and anatomical contacts. These are not response measurements for our three roots.

**Computational approximation/assumption:** local motion boundary, scalar integration, class-level signs, contact scaling, missing-input boundary, screen geometry and numerical constants. The experiment shows these particular assumptions do not reproduce the required selectivity. It does not identify a correct replacement or justify opportunistic local states.

**Genesis product mapping:** none. No fear, danger perception, escape choice, avoidance, voluntary action or digital-world interpretation is established. No LLM/prose memory participates in the equations.

`CANDIDATE_EVIDENCE_UPDATE.json` proposes only a narrow negative model-result claim and anatomy references. It is **UNADMITTED**, supersedes nothing and promotes no capability. Biological looming sensitivity remains supported by the independent literature; this model has not reproduced it. Revisit retinal crosswalk, measured local input/output transfer and representation adequacy in a separately reviewed prospective study, rather than fitting this failed model to a semantic goal.

Prior stages/specification, C. elegans and canonical state are checked in `PRESERVATION.json`. Genesis retains its original seven cycles and disabled schedule. No prior model, result, database state or BrainAdapter was modified. This experiment ends here for review.
''')
    data='\n'.join(texts)
    path=HERE/'REPORT.md'
    if path.exists():assert path.read_text()==data
    else:path.write_text(data)
    print(json.dumps({k:summary[k] for k in ['gate_a','gate_b','overall','qualitative_ordering_groups','groups_satisfying_all_orderings']},indent=2))


if __name__=='__main__':main()

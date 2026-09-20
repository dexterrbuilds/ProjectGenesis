"""Add compact comparative synthesis and operational caveats from measured artifacts."""
import json
from pathlib import Path
from report import H,table,pc,number

def main():
 a=json.loads((H/'ANALYSIS.json').read_text());s=json.loads((H/'SYNTHESIS.json').read_text());p=H/'REPORT.md';text=p.read_text()
 comparisons=table(['Stage / cue','L0 effect','L3 conservative','L3 class-consistent','Class − conservative (percentage points)','Relative class change'],[[str(r['stage'])+' / '+r['cue'],pc(r['original']),pc(r['generic']),pc(r['class_consistent']),number(r['class_minus_generic_percentage_points']),pc(r['class_vs_generic_relative_change'])] for r in s['effect_family_comparison'] if r['level']==3])
 summary='''## Quantitative answer: anatomy versus functional participation

'''+comparisons+'''

Stage 1 is nearly unchanged by generic closure and modestly strengthened by the
class-consistent operator. Stage 2 weakens slightly under both operators; no sign
reversal or magnitude rescue occurs. Stage 3 remains very small, with opposite
minor cue-dependent changes rather than systematic strengthening. Restored active
neurons therefore affect responses, but do not supply the missing behavioral evidence.
These are counterbalanced single-seed comparisons, not population confidence intervals.

Normalization has a much larger influence on the modeled effects. For cue A at L2,
Stage1 selective conditioning changes from 49.944896% to 16.963974% under full-input
core normalization. Stage2 specificity changes from 0.0016472495% to 1.1407196% under
role-based core normalization (about692.5×), on identical anatomy. These alternatives
are sensitivity results, never selected as the preferred biological answer.

**Attribution:** the study directly demonstrates consequential computational
assumptions and improves chemical boundary retention, but does not establish that
boundary loss is the primary cause of weak Stage2/3 effects. Nor does it establish
that the biological mechanisms themselves are weak. Unknown receptor gains,
neuromodulatory/body drive and incomplete physiological participation remain
confounded. Both boundary and approximation limitations remain plausible; an exact
causal allocation is **unidentified**. The experiment gives no basis for selecting
an architecture by whichever assumption produces the largest signal.

'''
 text=text.replace('## Preservation and experimental scope',summary+'## Preservation and experimental scope')
 part=[]
 for stage in (1,2,3):
  for level in (1,2,3):
   for cue in ('A','B'):
    candidates=[r for r in s['participation_and_stability'] if r['run'].startswith(f's{stage}-L{level}-primary-{cue}-') and r['run'].endswith('-intact')]
    g=[r for r in candidates if r['family']=='runs'];c=[r for r in candidates if r['family']=='class-runs']
    part.append([stage,level,cue,max(r['max_context_active'] for r in g),max(r['max_context_active'] for r in c),max(r.get('max_active_added_KCs',0) for r in c)])
 section=table(['Stage','Level','Cue','Active generic context','Active class context','Active added KCs (class)'],part)
 text=text.replace('Actual added-KC activation counts are saved in each class-run study.json.',
  'Actual added-KC activation counts are saved in each class-run study.json.\n\n'+section+'''

Activity means rate >1e−8 and is a numerical diagnostic, not a behavioral label.
Maxima include acquisition and disposable probes; Stage3 reports the larger of its
two resource states. Generic added KCs are silent by the analytical gain/threshold
bound. Class-consistent added KCs are demonstrably active. Merely counting active
context neurons does not establish useful recurrent integration.
''')
 classrows=[]
 for stage in (1,2,3):
  for level in (1,2,3):
   r=[x for x in a['runs'] if x['family']=='class_consistent' and x['stage']==stage and x['level']==level]
   classrows.append([stage,level,f"{min(x['wall_seconds'] for x in r):.2f}–{max(x['wall_seconds'] for x in r):.2f}",f"{max(x['peak_rss_bytes'] for x in r)/2**20:.2f}",pc(max(x['saturated_fraction'] for x in r)),number(max(x['reset_delta'] for x in r))])
 text=text.replace('## Integrated-circuit anatomy', '### Class-consistent performance and stability\n\n'+table(['Stage','Level','Wall seconds/condition','Batch peak MiB','Largest saturation fraction','Largest reset difference'],classrows)+'''

All156 runs remain finite. Every original snapshot restores its own baseline.
Zero sparse entries were removed in the class-consistent operator, whereas the
conservative extension retains explicit zeros; operator values and host contention
also differ. Runtime differences between families are therefore **not a pure
neuronal-activity cost comparison**. No previously measured timing is replaced.

'''+table(['Saved artifact family','Exact bytes','MiB'],[[k,v,f'{v/2**20:.2f}'] for k,v in s['storage_bytes'].items()])+'''

Storage is measured file size, not cloud storage billing. The anatomy arrays retain
all contacts/provenance independently of dynamic checkpoints. Every experiment also
saves full numerical neural/plastic snapshots; generic full-brain benchmark checkpoints
contain only rates/clock because that benchmark has no plasticity.

## Integrated-circuit anatomy''')
 class_controls=[]
 for r in a['runs']:
  if r['family']!='class_consistent' or r['level']!=2 or r['intervention']=='intact':continue
  base=next(x for x in a['runs'] if x['family']==r['family'] and x['stage']==r['stage'] and x['level']==r['level'] and x['cue']==r['cue'] and x['resource']==r['resource'] and x['variant']=='primary' and x['intervention']=='intact')
  sensory=max(abs(r['baseline_sensory'][g]/base['baseline_sensory'][g]-1) for g in ('PN','KC'))
  reduction=None if r['effect'] is None or base['effect'] in (None,0) else 1-r['effect']/base['effect']
  class_controls.append([r['stage'],r['resource'],r['intervention'],pc(reduction),pc(sensory)])
 text=text.replace('### Class-consistent performance and stability',
  '### Class-consistent intervention specificity\n\n'+table(['Stage','Resource','Intervention','Selective-effect reduction (S1/S2)','PN/KC baseline change vs intact'],class_controls)+'''

Stage3 effect reductions use the paired-resource contrasts already reported above,
not a single-resource depression score. Frozen Stage3 plasticity removes the local
experience effect while acute resource gating remains; those are different outcomes.
Relevant DA silencing removes the modeled pathway, whereas matched comparators
largely preserve it. This is conditional causal evidence within the model; it does
not supply the missing behavioral magnitude or a validated integrated decision.

### Class-consistent performance and stability''')
 text=text.replace('maximum differences are in raw rates, not normalized percentage units.',
  'maximum differences are in raw rates, not normalized percentage units. Stage 1\nreset differences compare saved original-population means; Stage 2/3 compare all\nmodeled-neuron probe rates. The Stage-2 L2 normalization alternative reaches about\n3.6e−10, exceeding the original1e−10 numerical tolerance; it must not be called\nan exact transient-free recall result. Primary Stage-2 resets remain near8e−14.')
 temp=json.loads((H/'TEMPORAL_COMPARISON.json').read_text())
 text=text.replace('Full-context frozen-learning-kernel pilots, updating all neurons, measure:',
  table(['dt compared with5ms','Largest population-mean rate discrepancy','Discrepancy / reference peak mean'],[[r['dt'],number(r['mean_rate_max_absolute_difference_interpolated']),pc(r['mean_rate_peak_relative_error'])] for r in temp])+'''

These are saved population-mean traces aligned by physical step-end times using
linear interpolation. They are **not** per-neuron transient errors or a convergence
proof. The10ms/20ms discrepancies are approximately4.88%/14.64% of the reference
peak mean. Real-time20ms operation therefore comes with a measured temporal
approximation difference, not interchangeable neural dynamics.

Full-context frozen-learning-kernel pilots, updating all neurons, measure:''')
 text=text.replace('All exceed the prospectively declared 120-second per-acquisition study budget.',
  'These pilots use the conservative extension, not the later class-consistent operator.\nThey ran sequentially in one process, so RSS values are cumulative high-water marks,\nnot fresh-process per-kernel peaks. Each full generic temporal benchmark used its own\nfresh process. The class-consistent full-brain operator was not benchmarked.\n\nAll exceed the prospectively declared 120-second per-acquisition study budget.')
 text=text.replace('Those projected times make offline work plausible, but the current extension kernels',
  'The120-second cutoff is an experiment budget, not a biological or hardware limit.\nNo L4 learning-effect trajectory should be inferred from these pilots. Those projected\ntimes make offline work plausible, but the measured conservative extension kernels')
 text=text.replace('- [All numeric comparisons](ANALYSIS.json)', '- [All numeric comparisons](ANALYSIS.json)\n- [Participation, effect differences, stability and storage](SYNTHESIS.json)\n- [Temporal approximation comparison](TEMPORAL_COMPARISON.json)\n- [Shared-cell and shared-synapse conflicts](UNIFIED_MODEL_CONFLICTS.md)')
 text=text.replace('Stage1 selective conditioning changes from 49.944896% to 16.963974%', 'Stage1 selective conditioning changes from 49.944896% to 16.963974%')
 # Formatting only: values, identifiers and scientific source code are unchanged.
 for old,new in [('All156','All 156'),('Stage1','Stage 1'),('Stage2','Stage 2'),('Stage3','Stage 3'),('at0.05','at 0.05'),('gain3','gain 3'),('gain1','gain 1'),('threshold0.15','threshold 0.15'),('approximately4.88','approximately 4.88'),('The10ms/20ms','The 10 ms / 20 ms'),('Real-time20ms','Real-time 20 ms'),('fixed10ms','fixed 10 ms'),('real-time20ms','real-time 20 ms'),('dt10ms/tau50ms','dt 10 ms / tau 50 ms'),('tau50ms','tau 50 ms'),('total4,622','total 4,622'),('and1,053','and 1,053'),('about692.5','about 692.5'),('The120-second','The 120-second'),('original1e','original 1e'),('near8e','near 8e')]:text=text.replace(old,new)
 p.write_text(text)
 print('Added measured family contrasts, participation, storage, timing and attribution limitations.')
if __name__=='__main__':main()

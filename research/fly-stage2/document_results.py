"""Render audit tables from saved evidence, without changing or rerunning either model."""
import csv
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
circuit=next((HERE/'artifacts').iterdir())
evidence=next((HERE/'evidence').iterdir())
evaluation=next((HERE/'evaluations').glob('*/evaluation.json'))
reward=next((HERE/'reward-evidence').iterdir())
r=json.loads((evidence/'results.json').read_text())
a=json.loads(evaluation.read_text())
f=json.loads((reward/'results.json').read_text())
runs={x['run']:x for x in r['runs']}
primary=[x for x in r['runs'] if x['run'].startswith('primary')]

def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+
                    ['| '+' | '.join(map(str,row))+' |' for row in rows])

def pct(x):
    return 'undefined' if x is None else f'{100*x:.8f}%'

primary_table=table(['Seed / repeated','Baseline (raw rate)','After (raw rate)','Repeated suppression','Unseen suppression','Specificity (percentage points)'],
    [[str(x['seed'])+' / '+x['repeated'],f"{x['baseline'][x['repeated']]['groups']['MBON']:.12f}",
      f"{x['post'][x['repeated']]['groups']['MBON']:.12f}",pct(x['repeated_depression']),pct(x['unseen_depression']),
      f"{100*x['specificity']:.8f}"] for x in primary])
boundary_table=table(['Population','Cells','Retained in','Omitted in','Input retained','Output retained'],
    [[g,len(a['identities'][g]) if g in a['identities'] else a['counts']['roles'][g],s['retained_input'],s['omitted_input'],
      f"{100*s['input_retention']:.2f}%",f"{100*s['output_retention']:.2f}%"] for g,s in a['boundary'].items()])
interventions=table(['Intervention','Specificity A / B (percentage points)','Reduction A / B','Largest PN/KC baseline change'],
    [[name,' / '.join(f"{100*x['specificity']:.8f}" if x['specificity'] is not None else 'undefined' for x in a['interventions'] if x['condition']==name),
      ' / '.join(pct(x['specificity_reduction']) for x in a['interventions'] if x['condition']==name),
      pct(max(v for x in a['interventions'] if x['condition']==name for v in x['max_baseline_sensory_relative_change'].values()))]
     for name in dict.fromkeys(x['condition'] for x in a['interventions'])])
recovery=table(['Quiet recovery','Repeated suppression range','Interpretation'],
    [[str(t)+' s',pct(min(x['recovery_depression'][str(t)] for x in primary))+' – '+pct(max(x['recovery_depression'][str(t)] for x in primary)),
      'Explicit efficacy relaxation; not an independently recovered biological law'] for t in (0,300,1200,3600)])
sensitivity=table(['Variant','Repeated suppression A','Repeated suppression B','Specificity A / B (pp)'],
    [[name,pct(runs['sensitivity-'+name+'-A']['repeated_depression']),pct(runs['sensitivity-'+name+'-B']['repeated_depression']),
      ' / '.join(f"{100*runs['sensitivity-'+name+'-'+q]['specificity']:.8f}" for q in ('A','B'))]
     for name in dict.fromkeys(x['run'][12:-2] for x in r['runs'] if x['run'].startswith('sensitivity-'))])
factorial=table(['Cue','Prior pulses','PAM11 teaching in α1','α1 suppression','α′3 suppression'],
    [[x['cue'],x['prior_exposures'],x['reinforcement'],pct(x['alpha1']['depression'][x['cue']]),
      pct(x['alpha_prime3']['depression'][x['cue']])] for x in f['results']])
identities=table(['Role / type','Side','FlyWire root ID (string)'],
    [[role+' / '+x['type'],x['side'],'`'+x['root']+'`'] for role,items in a['identities'].items() for x in items])

report=f'''# Stage 2: α′3 familiarity research

**Final classification: PARTIAL-INCONCLUSIVE. Stop for review; no Stage 3.**

The extracted circuit produces a small, stimulus-specific change stored in actual
KC→MBON efficacy variables. It survives fast reset and fresh-process cue-only recall,
is eliminated by the modeled dopamine/plasticity interventions, and is reproducible.
However, primary repeated-cue suppression is only **0.001376–0.004555%**, versus the
prospective **5%** minimum. Specificity is **0.001376–0.004266 percentage points**,
versus **3 percentage points** required. All six primary conditions miss both
thresholds. This is evidence for operation of the implemented local memory rule;
it is insufficient evidence for a useful, biologically calibrated familiarity system.
No parameters, circuit selection or acceptance thresholds were tuned after results.

## Preservation and scope

The 462 files in [FROZEN_BEFORE.json](FROZEN_BEFORE.json) include the complete frozen
Stage-1 harness/artifacts/evidence/report and Genesis core/data/runtime/server files.
[PRESERVATION.json](PRESERVATION.json) records the final hash comparison. Stage-1
10/10 essential tests passed before and after this work. Its saved acceptance audit
remains PASS; a fresh primary training run reproduced its accepted trained-state
hash exactly. Its original 1,054 neurons / 80,423 pairs / 226,143 contacts remain
unchanged. No Stage-1 outputs were overwritten by the new comparison assay.

The canonical database matches its original SHA-256 exactly: one organism, seven
life cycles/decisions and seven memories. The pre-existing disabled scheduler is
unchanged. No Genesis cycles, activation, wallet/planner/LLM connections or migration
were performed. Research programs read only explicitly supplied circuit/state files;
canonical preservation was checked separately with a read-only database transaction.

## BIOLOGICAL FACT and identity confidence

Repeated odors can suppress α′3 MBON responses selectively, with odor-driven
PPL1-α′3 dopamine implicated; recovery occurs over tens of minutes. Functional
experiments used pooled MBON drivers, not these particular EM roots.
[Hattori et al., Cell 2017](https://doi.org/10.1016/j.cell.2017.04.028).
Postsynaptic mechanisms are supported by α′3 MBON depression without corresponding
KC calcium depression and nicotinic-receptor experiments.
[Pribbenow et al., eLife 2022](https://elifesciences.org/articles/80445).

The morphology/type crosswalk connects MBON16/17 to α′3ap/α′3m and PPL104 to PPL1-α′3.
MBON17-like has related morphology with different connectivity, and MBON28 driver
assignment is ambiguous. These facts justify recording uncertainty, not attributing
the pooled response to every individual cell.
[Li et al., eLife 2020](https://elifesciences.org/articles/62576),
[Rubin and Aso, eLife](https://elifesciences.org/articles/90523).
Exact annotation and VFB links are in [PLAN.md](PLAN.md) and the extraction manifest.

{identities}

All selected roots have v3.1.0 annotations and belong to the v783 proofread inventory.
The manifest explicitly records four ambiguous roots. They contribute observed
anatomical recurrence but receive no assigned familiarity plasticity. Removing them
is a sensitivity experiment, not an identity claim. No additional partners were
introduced after observing outcomes.

## Extraction and boundary

- **1,172 neurons:** 887 α′β′ KCs, 271 cholinergic ALPNs, four canonical α′3 MBONs,
  two PPL104, two APL, two MBON13 α′2 comparison outputs, four ambiguous partners.
- **57,804 directed neuron pairs; 73,715 pair/neuropil rows; 160,848 contacts.**
- **1,258 plastic KC→MBON pairs**, represented by **1,771 persistent efficacy
  variables** over **4,709 anatomical contacts**. Scalar per pair/neuropil group,
  not per physical synapse; no fabricated edges.
- 120 roots overlap Stage 1 (119 PN plus one APL); **1,052 are additional**.
  No Stage-1 KC is reused: its αβ population differs from this α′β′ preparation.
- Omitted: **539,717 incoming** and **1,132,985 outgoing** proofread contacts.
  Full external-root edge lists and annotations aggregated by class/type/transmitter
  are retained in the boundary artifacts. Counts exclude unproofread fragments,
  electrical coupling and volume transmission.

{boundary_table}

PN afferents are intentionally replaced by imposed sensory currents; consequently
PN input retention is low. No such replacement is supplied to DANs, APL or outputs.
DAN input retention is 47.24%; APL retention is 20.71%. The missing portion may carry
odor-evoked or state-dependent signals. Silent omissions and normalization brackets
do not recover their physiological dynamics. Low output retention means downstream
alerting/action behavior is not simulated.

**Spatial caveat:** only 2,169/4,709 plastic contacts carry MB_VL_L/R coarse labels.
The others are SIP_L 1,525, SIP_R 610, SMP_R 275, SMP_L 125 and SLP_L 5. Cell-type
identity does not prove each coarse-labelled contact lies in α′3 or shares receptor
localization. The rule uses type-level gating, not synapse-coordinate compartment
validation. No contacts were relabelled, removed or invented to improve results.
This unresolved localization is an additional limit on the biological claim.

## COMPUTATIONAL MODEL

The prospectively fixed [PLAN.md](PLAN.md) specifies all parameters and acceptance
criteria. A separate float64 rate model evolves neural activity at 10 ms steps,
50 ms fast time constant and 500 ms eligibility time constant. Weights depend on
actual contacts. Primary normalization divides by all proofread input contacts at
each target; omitted inputs are silent and their mass is not redistributed. Class
gains and the KC threshold are assumptions, not conductance measurements.

Only actual KC→canonical α′3 MBON rows are plastic. Activity of actual PPL104 cells,
transmitted through observed PPL104→MBON contacts, gates local efficacy changes:

`dm/dt = −0.08 × KC eligibility × local DA × m + (1−m)/1800`.

Efficacies are bounded [0.1,1]. The recovery term is a phenomenological hypothesis.
There is no learned cue score or cue-indexed state. Model snapshots contain rates,
eligibility, per-edge efficacy, logical clock and PRNG state. The model receives
only numeric currents. Acquisition currents stimulate PN roots only: no externally
supplied dopamine, novelty label, count, reward or familiar flag.

This is an effective postsynaptic-efficacy model, not a molecular receptor simulation.
Freezing the rule is not claimed to reproduce an α5 RNAi phenotype. Slow recovery
and dopamine concentration scales cannot be inferred from contact counts. There is
no imposed sensory fatigue variable; control results exclude such a variable in
this model, not every sensory-adaptation mechanism in a real fly.

## Counterbalanced primary results

Three fixed seeds, both cue identities; 14 disjoint PN inputs per cue, each amplitude
1. Equal input cardinality/amplitude does **not** imply equal baseline neural rates.
No response matching or seed selection was performed. Baseline probes use disposable
copies so the actual unseen control has no prior exposure. Ten 1 s presentations
with 6 s gaps, 70 s total acquisition; no appetitive/aversive reinforcement.
Probes are 1 s, averaging their last 0.5 s, including within-probe plasticity.

Raw values below are dimensionless rates, not Hz or measured calcium. Suppression
is `1 − post/baseline`. Specificity subtracts unseen-cue suppression from repeated-cue
suppression. Zero-input sham produces zero persistent change; a one-pulse control
produces 0.000163–0.000228% repeated suppression versus 0.001661–0.002324% after ten
(seed2701), consistent with accumulation of the modeled rule.

{primary_table}

All 24 individual canonical MBON readouts decrease for the repeated cue, by
0.000906–0.005774%; the result is not an average hiding a contrary output cell.
PN/KC and α′2 comparison changes are negligible (maximum population relative change
4.24e−10 across primary sensory/control measures). Input coding remains unequal:
KC active fraction ranges 4.74–13.53%. Reversal and within-cue normalization address
bias without claiming identical population codes. PPL104 baseline cue-evoked mean
rates are only 0.000185–0.000503 in the primary numerical convention.

## Interventions (seed2701, both cue directions)

Reduction is relative to the corresponding intact specificity; a negative reduction
means an increase. No weights are renormalized following a lesion.

{interventions}

Freeze, PPL104 silencing and removal of the observed dopamine-gating contacts reduce
the effect 100%, while preserving basic PN/KC responsiveness. The two-cell MBON13
control lesion retains 99.0–99.6% of intact specificity. It is matched in neuron
count, not centrality or functional strength.

Cutting canonical MBON→PPL104 feedback reduces specificity only 10.6–13.4%: that
feedback is not the sole odor-drive path in this model. Direct KC/other retained
inputs matter. Removing PN→KC abolishes KC responses, so it is a connectivity
necessity control, not selective learning evidence. Removing KC→MBON transmission
eliminates the learned readout even though inert plastic multipliers can still be
updated through other surviving dopamine drive. Strength shuffling retains the
anatomical support and changes sensory coding; its surviving effect does not prove
that the exact FlyWire weight distribution is uniquely required. The demonstrated
causal structure is an anatomical pathway plus the imposed local plasticity rule.

## Neural memory, recovery and replay

- All **60** conditions restore baseline exactly from the pre-exposure snapshot.
- All **six** primary full replays are bit-identical on the pinned environment.
- **18/18** fresh-process recalls (trained, fast-reset, original × six) match saved
  neural readouts exactly. The process receives only the pinned circuit, model
  parameters, neural snapshot and the same numeric sensory patterns.
- Clearing fast rates/eligibility while retaining efficacies changes primary probe
  rates by at most **2.24e−13**, below the declared 1e−10 tolerance. Therefore the
  tiny persistent effect is not residual fast activity.
- 77–218 efficacy rows change per primary run; maximal per-row loss ranges
  2.60e−5–1.77e−4. No database/prose/LLM memory participates.

{recovery}

After an explicit fast reset, quiet recovery integrates the zero-activity efficacy
relaxation exactly. It agrees with direct stepping within 1e−13 in the implementation
check. Around 13.5% of the initial tiny suppression remains after one hour. That
recovery follows a chosen exponential law; it does **not** establish spontaneous
recovery in an intact fly or reproduce dopamine-only forgetting experimentally.

## Parameter and boundary sensitivity

All variants were declared before conditioning outcomes. No variant became a new
primary. Learning-rate/threshold/gain/time-step/feedback/APL/recovery variations
preserve the sign but leave suppression very small. Halving the timestep changes
primary effect size by roughly 1.1–1.3%, while same-timestep replay is exact.

{ sensitivity }

Dividing by retained total input amplifies specificity about 4.7–5.6×; normalizing
separately within retained presynaptic roles amplifies it about 553–690×. Even that
optimistic case gives only 1.19–1.34% repeated suppression, below 5%. Neither is a
repair: both are reported as assumptions with strong quantitative consequences.
The sparse preparation cannot establish what omitted odor-driven inputs would do.
Removing APL barely changes this primary model despite its biological importance;
that is a warning about the simplification, not evidence that APL is dispensable.

## Reward comparison: useful dissociation, unresolved interaction

[FACTORIAL_PLAN.md](FACTORIAL_PLAN.md) defines a limited two-preparation assay using
119 shared PN roots and two matched six-root cues. Both models see the same sensory
currents. Prior exposure is 0 or 10 pulses; then both arms receive 60 seconds of the
cue. Only the Stage-1 α1 preparation receives its established PAM11 current in the
reinforced arm. The accepted Stage-1 model and parameters are unchanged.

{factorial}

Within α1, reinforcement changes the tested response by about 49.93–50.00%; prior
unreinforced exposure alone has no corresponding α1 effect here. The α1 E×R
interaction is 1.84e−8 (A) / 2.06e−8 (B) in fractional depression. α′3 state changes
with unreinforced sensory experience but weakly. Its reward interaction is exactly
zero **by construction**, because this isolated preparation receives no PAM11
pathway. This is not proof that familiarity and value are orthogonal in biology.
It demonstrates different modeled local storage rules in separate preparations;
a same-brain biological interaction is **not determined**. Reinforcement includes
sensory exposure, so no post-training arm is honestly called “unseen + reinforced.”
No joint connectome was invented to force the requested distinction.

## Performance and artifacts

The 60-condition main battery, replay, probes and trace/snapshot writes took
**{r['performance']['suite_wall_seconds']:.2f} s wall time**, with **{r['performance']['peak_rss_bytes']/2**20:.2f} MiB peak process RSS**.
Each acquisition spans 70 simulated seconds. Recovery uses an analytic quiet-state
update; those long logical intervals must not be counted as performance of an active
full-brain simulation. The separate 16-model reward comparison took
**{f['performance']['wall_seconds']:.2f} s**, **{f['performance']['peak_rss_bytes']/2**20:.2f} MiB peak RSS**.
Environment: Python {r['environment']['python']}, NumPy {r['environment']['numpy']},
SciPy {r['environment']['scipy']}, {r['environment']['os']}; {r['environment']['cpu_count']} logical CPUs available,
single Python simulation process. These are local measurements, not cloud guarantees.
Re-extraction reproduced the same manifest in 15.76 s wall time. The host denied
the profiling tool’s system-counter query, so extraction peak RSS was not obtained;
the simulation RSS measurements above succeeded. See
`verification/extraction-performance.log`.

Immutable, content-addressed bundles:

- [Circuit manifest](artifacts/{circuit.name}/manifest.json): `{circuit.name}`.
- [Main evidence](evidence/{evidence.name}/results.json): `{evidence.name}`.
- [Acceptance audit]({evaluation.relative_to(HERE)}).
- [Reward evidence](reward-evidence/{reward.name}/results.json).
- [All 60 rows](RESULTS.csv) and [individual MBON readouts](NEURON_RESULTS.csv).

Trace arrays are sampled genuine model states, not presentation animation. Two
primary traces retain every neuron's activity and all efficacy variables at 100 ms
sampling; other traces contain genuine population means. Probes retain per-neuron
vectors. Snapshot/manifest hashes are verified on loading; files are content-addressed,
not protected by a filesystem write-once guarantee. Requirements/reproduction steps
are in [README.md](README.md). Stage-2 implementation checks pass 9/9; scientific
acceptance is separately **not passed**.

## Limits and review decision

The model does not establish physiological gains, receptor kinetics, dopamine
concentrations, precise α′3 synapse locations, spontaneous network activity, alerting
behavior or biological reward–familiarity independence. Missing inputs, synthetic
PN stimulus patterns, point-neuron APL, coarse transmitter signs, and one female
specimen limit generalization. A tiny statistically deterministic simulation effect
is not evidence of a perceptible familiarity state in an animal.

**GENESIS MAPPING: none.** No new behavior, novelty API, BrainAdapter version or
product integration was created. Stage 1 remains accepted and frozen regardless
of this result. Resolving the identified physiological/localization/boundary questions
would require a separately reviewed research step, not parameter tuning of this run.

Source licensing remains the documented Stage-1 discrepancy: Zenodo connectivity
metadata CC-BY-4.0 versus FlyWire site guidance CC-BY-NC-4.0; annotation terms were not
independently resolved. This is isolated local research, not commercial publication
or deployment of the data. The manifest retains original URLs and source hashes.
'''
(HERE/'REPORT.md').write_text(report)
with (HERE/'NEURON_RESULTS.csv').open('w',newline='') as out:
    writer=csv.DictWriter(out,fieldnames=list(a['cell_effects'][0]))
    writer.writeheader();writer.writerows(a['cell_effects'])
print('Wrote REPORT.md and NEURON_RESULTS.csv from verified evidence.')

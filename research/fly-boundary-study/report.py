"""Report sealed measurements without changing any model or acceptance threshold."""
import json,statistics,hashlib
from pathlib import Path
from context import H,A

def table(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(str,r))+' |' for r in rows])
def pc(v):return 'undefined' if v is None else f'{100*v:.8g}%'
def number(v):return 'undefined' if v is None else f'{v:.9g}'
def main():
 a=json.loads((H/'ANALYSIS.json').read_text());count=json.loads((A/'counts.json').read_text());integ=json.loads((H/'INTEGRATION.json').read_text());allrr=a['runs'];rr=[r for r in allrr if r['family']=='generic'];cr=[r for r in allrr if r['family']=='class_consistent'];cc=[r for r in a['stage3_comparisons'] if r['family']=='generic'];ccc=[r for r in a['stage3_comparisons'] if r['family']=='class_consistent']
 primary=[r for r in rr if r['variant']=='primary' and r['intervention']=='intact']
 sizes=table(['Seed','Level','Neurons','Directed pairs','Neuropil rows','Contacts','Omitted inputs','Omitted outputs'],[[s,l,r['neurons'],r['directed_pairs'],r['neuropil_rows'],r['contacts'],r['boundary']['omitted_input'],r['boundary']['omitted_output']] for s,levels in count.items() for l,r in levels.items()])
 retention=table(['Stage/population']+[f'L{i} input / output' for i in range(5)],[[f'S{s} {g}']+[pc(count[str(s)][f'L{i}']['original_groups'][g]['input_fraction'])+' / '+pc(count[str(s)][f'L{i}']['original_groups'][g]['output_fraction']) for i in range(5)] for s,groups in [(1,['KC','MBON_app','DAN_app','APL']),(2,['MBON','DAN','APL']),(3,['MB11','MB18','DAN','APL','LH','LHCENT','OA'])] for g in groups])
 effects=table(['Stage','Cue','Level','Baseline','Post','Selective effect'],[[r['stage'],r['cue'],r['level'],number(r['baseline']),number(r['post']),pc(r['effect'])] for r in primary if r['stage']<3])
 motivation=table(['Level','Cue','MBON11 state contrast','MBON11 experience low','MBON18 state contrast','LH state contrast','LH experience low'],[[r['level'],r['cue'],pc(r['contrast']['MB11']),pc(r['experience_low']['MB11']),pc(r['contrast']['MB18']),pc(r['contrast']['LH']),pc(r['experience_low']['LH'])] for r in cc if r['variant']=='primary' and r['intervention']=='intact'])
 controls=[]
 for r in rr:
  if r['stage']==3 or r['intervention']=='intact':continue
  b=next(v for v in primary if all(v[k]==r[k] for k in ('stage','level','cue','resource')))
  reduction=None if b['effect'] in (None,0) or r['effect'] is None else 1-r['effect']/b['effect']
  controls.append([r['stage'],r['level'],r['intervention'],pc(r['effect']),pc(reduction),pc(max(abs(r['baseline_sensory'][k]/b['baseline_sensory'][k]-1) for k in ('PN','KC')))])
 intervention=table(['Stage','Level','Intervention','Selective effect','Reduction vs intact','PN/KC baseline change vs intact'],controls)
 motivation_control=[]
 for r in cc:
  if r['intervention']=='intact':continue
  b=next(v for v in cc if v['level']==r['level'] and v['cue']==r['cue'] and v['variant']=='primary' and v['intervention']=='intact')
  v=r['contrast']['MB11'];base=b['contrast']['MB11'];reduction=None if v is None or base in (None,0) else 1-v/base
  motivation_control.append([r['level'],r['intervention'],pc(v),pc(reduction),pc(r['experience_low']['MB11']),pc(r['contrast']['PN']),pc(r['contrast']['KC'])])
 intervention3=table(['Level','Intervention','MBON11 contrast','Reduction','Experience low','PN state contrast','KC state contrast'],motivation_control)
 sensitivity=table(['Stage','L2 assumption','Selective effect','Baseline','Post'],[[r['stage'],r['variant'],pc(r['effect']),number(r['baseline']),number(r['post'])] for r in rr if r['stage']<3 and r['variant']!='primary'])
 sensitivity3=table(['L2 assumption','MBON11 contrast','MBON11 experience low','LH contrast','LH experience low'],[[r['variant'],pc(r['contrast']['MB11']),pc(r['experience_low']['MB11']),pc(r['contrast']['LH']),pc(r['experience_low']['LH'])] for r in cc if r['variant']!='primary'])
 stability=table(['Stage / level','Maximum rate','Maximum clipped fraction','Maximum active context neurons','Largest reset delta','Per-condition wall range (s)','Process peak MiB'],[[f'S{s} L{l}',number(max(r['max_rate'] for r in rr if r['stage']==s and r['level']==l)),pc(max(r['saturated_fraction'] for r in rr if r['stage']==s and r['level']==l)),max(r['max_context_active'] for r in rr if r['stage']==s and r['level']==l),number(max(r['reset_delta'] for r in rr if r['stage']==s and r['level']==l)),f"{min(r['wall_seconds'] for r in rr if r['stage']==s and r['level']==l):.2f}–{max(r['wall_seconds'] for r in rr if r['stage']==s and r['level']==l):.2f}",f"{max(r['peak_rss_bytes'] for r in rr if r['stage']==s and r['level']==l)/2**20:.2f}"] for s in (1,2,3) for l in range(4)])
 bench=table(['dt','Initialization s','10 simulated seconds / wall s','Updates/s','Sim/wall','CPU (% one core)','Peak MiB','Checkpoint bytes / write ms / load ms','Replay s'],[[r['dt'],f"{r['initialization_seconds']:.3f}",f"{r['wall_seconds']:.3f}",f"{r['updates_per_second']:.2f}",f"{r['simulated_per_wall']:.3f}",f"{r['cpu_percent_one_core']:.1f}",f"{r['peak_rss_bytes']/2**20:.2f}",f"{r['checkpoint_bytes']} / {r['checkpoint_write_seconds']*1000:.3f} / {r['checkpoint_load_seconds']*1000:.3f}",f"{r['replay_wall_seconds']:.3f}"] for r in a['benchmarks']])
 pilots=table(['Kernel','Init s','1 simulated second / wall s','Projected full acquisition s','Process peak MiB'],[[r['stage'],f"{r['initialization_seconds']:.3f}",f"{r['pilot_wall_seconds']:.3f}",f"{r['predicted_acquisition_seconds']:.2f}",f"{r['peak_rss_bytes']/2**20:.2f}"] for r in a['protocol_budget']])
 union=table(['Level','Union neurons','Pairs','Contacts'],[[l,v['union_neurons'],v['pairs'],v['contacts']] for l,v in integ['integrated_union_counts'].items()])
 direct=table(['Source','Target','Contacts','Pairs'],[[r['source'],r['target'],r['contacts'],r['pairs']] for r in integ['direct_contacts'] if r['source'][:2]!=r['target'][:2] and not r['overlapping_roots'] and r['contacts']])
 totalwall=sum(r['wall_seconds'] for r in allrr);totalcpu=sum(r['cpu_seconds'] for r in allrr)
 class_effects=table(['Stage','Level','Cue','Assumption','Intervention','Selective effect','Baseline','Post'],[[r['stage'],r['level'],r['cue'],r['variant'],r['intervention'],pc(r['effect']),number(r['baseline']),number(r['post'])] for r in cr if r['stage']<3])
 class_state=table(['Level','Cue','Assumption','Intervention','MBON11 state contrast','MBON11 experience low','LH state contrast','LH experience low'],[[r['level'],r['cue'],r['variant'],r['intervention'],pc(r['contrast']['MB11']),pc(r['experience_low']['MB11']),pc(r['contrast']['LH']),pc(r['experience_low']['LH'])] for r in ccc])
 text=f'''# Boundary-Closure and Brain Architecture Study

**Neural architecture recommendation: INSUFFICIENT EVIDENCE.**

This is not Stage 4 and does not revise any frozen result. The experiments ask
whether anatomical context rescues weak signals under fixed computational rules.
They do not identify the physiological cause of the original weak effects in a fly.

## Main conclusion

Anatomical closure restores most input/output mass of the target populations, but
is not sufficient evidence of behavioral closure. The primary effects and all
assumption variants are below. Small or absent improvements cannot establish that
missing circuitry is irrelevant: restored anatomy has assumed fast signs/gains,
unknown neuromodulatory effects, and mostly silent natural sensory/body afferents.
Conversely, a bigger effect after normalization changes is not evidence that the
connectome rescued the mechanism.

The study cannot determine a unique percentage of weakness attributable to boundary
loss versus physiological approximation. It can distinguish conditional changes
caused by adding anatomy, changing normalization and changing the assumed context
operator. These are model experiments, not new validation of motivation/familiarity.

A crucial limitation is built into the conservative context operator: its absolute
incoming weight sum is at most 0.05 per target. Thus restored unknown recurrence is
weak **by assumption**. More anatomical contacts cannot identify the physiological
gain that the model lacks. This makes a negative closure result informative about
this approximation, but insufficient to acquit boundary loss in the biological system.

## Preservation and experimental scope

All three original stages, C. elegans, canonical identity, seven life cycles and
disabled schedule are frozen. FROZEN_BEFORE.json records 2,084 protected files.
PRESERVATION.json records the final hash comparison and database verification.
Stage 1 remains PASS; Stages 2 and 3 remain PARTIAL-INCONCLUSIVE. No Genesis imports,
life cycles, migration, activation, LLM, planner, wallet or digital actions occur.

The study runs **{len(allrr)} full-duration conditions** ({len(rr)} generic-context and {len(cr)} class-consistent) using each original primary seed
(1701/2701/3701), both original cues and, for Stage 3, both resource states. This is
one counterbalanced seed per stage, not all seeds from the original validation
batteries. The eight L0 trained neural/plastic/clock/PRNG states match frozen states
exactly; new fingerprints identify the study wrapper. No prior result is overwritten.

## Exact outcome-blind closure methodology

See PLAN.md and extract.py. All selection is completed before expanded neural results.
Pinned adult female FAFB materialization 783, annotation v3.1.0. Root identities are
strings in JSON; internal integer indexing verifies every source and target against
the uint64 inventory. Fourteen proofread roots lack an annotation row; their anatomy
remains, and missing annotation does not receive a behavioral interpretation.

- **L0:** exact independent original seed, including original edge order.
- **L1:** original non-PN/KC populations' missing afferents/efferents ranked by contact
  mass to 80% retention per population/direction; direct named modulatory partners
  irrespective of contact count; all reciprocally connected partners of those target
  populations. Prior additions count toward later population targets. Ties use root
  order. Known modulators are selected anatomically even when physiology is unresolved.
- **L2:** L1 plus connected neurons with at least 50% of incident mass in MB/CA/LH/AL
  regions, or specified MB/AL/LH cell classes and APL/DPM/LHCENT1. This combines
  observed connectivity, regional mass and biological annotation rather than pure hops.
- **L3:** L2 plus all annotated central/ascending/descending/endocrine neurons.
- **L4:** all 139,255 proofread roots. No strength threshold; all observed induced
  chemical contacts are counted. Neuropil rows are aggregated only for linear sparse
  fast propagation, never treated as one anatomical contact per edge.

The rules are operational anatomical screens, not a theorem of functional closure.
APL's wide reciprocal connectivity makes L1 grow substantially. There is no size
target and no addition based on whether a neural effect becomes larger.

{sizes}

Total full reference: **15,091,983 directed pairs, 16,847,997 pair/neuropil rows,
54,492,922 contacts**. Published thresholded connection counts are not interchangeable
with these unthresholded file counts. Boundary denominators exclude unproofread
fragments, electrical synapses and volume transmission; 100% chemical retention is
not 100% physiology.

## Boundary retention: original populations

Entries are percent retained input / output. Whole-context totals are above; each
new neuron also introduces its own boundary. Complete per-stage/group data and
selected roots are in anatomy/counts.json and anatomy/selection.json. Strongest
remaining omitted partners by type/root are in INTEGRATION.json.

{retention}

This restores the severely cut APL/PPL104 and LH/OA neighborhoods. It does not supply
missing gustatory, metabolic, endocrine or spontaneous activity. PN stimulation
remains at the original boundary, not at newly reconstructed receptor neurons.

## What is fixed and what is approximated

**BIOLOGICAL FACT:** chemical root-to-root anatomy, annotation-supported classes,
region labels and known recurrent MB/AL/LH organization. Primary literature and
crosswalk limitations are in LITERATURE.md and the frozen stages' reports.

**COMPUTATIONAL MODEL:** original core weights, dopamine operators, plastic rows,
parameters, input root identities and timing are frozen. Added edges alone use
contacts/full-proofread-input × recurrent gain 0.05, with conservative ACh/GABA sign
assumptions. All added populations are generic context; no new plastic compartment
or teaching function is assigned. Context KCs use their known cholinergic identity
and the original KC threshold. A new KC→core connection is a fixed contextual edge,
not automatically granted the core's class-specific gain or learning rule. This
conservative extension is a substantive limitation, not a physiological estimate.

Unknown glutamatergic target effects, monoamines and ambiguous cotransmission have
zero fast efficacy in primary, although their anatomy remains counted. DPM's multiple
transmitters cannot be inferred as one signed receptor effect. Added sign variants
are labeled hypotheses. This prevents claiming that reinstating a modulatory root
also reinstated its true endocrine function.

**GENESIS MAPPING: none.** No scores, language or desired action labels enter neurons.

The primary contrast changes anatomy while preserving original weight denominators.
The alternative full/role normalization arms change **core** denominators explicitly;
context edges retain full-input normalization. This avoids attributing a rescaled
original circuit to added biological context. Half/double context gain tests the new
operator without retuning old parameters. No arbitrary tonic drive is introduced.
Boundary-drive contribution is zero in every arm, not estimated from anatomy.

## Generic-context Stage 1 and Stage 2 effect trajectories

Raw baseline/post responses use the same original readout roots. Stage-1 selective
conditioning is paired-cue depression minus control-cue depression. Stage-2 specificity
is repeated-cue depression minus unseen-control depression. Percent is relative
response change, not behavioral probability or a software preference score.

{effects}

These expanded-context results have no authority to rewrite the narrow accepted
Stage-1 PASS. They also do not convert Stage 2 into success simply by preserving a
nonzero persistent change. Sensory and plastic states, actual stimuli and traces
are saved for every condition.

## Generic-context Stage 3 trajectories

State contrast is low/high−1 during the final maintained-cue window; experience is
trial10/trial1−1 at low resource. Original thresholds remain 10% MBON11 state contrast
and joint 5% experience magnitudes. No threshold or sign-flipped decoder was fitted.

{motivation}

Maintained-cue responses alone are not pursuit. No descending motor system, choice
policy, physical acquisition loop or voluntary abstention mechanism was introduced.
A change in LH/MBON response is reported as neural activity only.

## Intervention specificity

All interventions retain intact denominators. Relevant dopamine silencing, frozen
plasticity and the original comparator lesion are repeated at each measured level.
The Stage-1 matched_dan comparator removes one other-compartment neuron, whereas
silence_dan removes the whole relevant population: this is the original comparator,
not a newly count-matched lesion of the whole population. Interpret that limitation.

{intervention}

Sensory change compares lesion versus intact baseline for the same cue and level.
Loss of sensory drive is never interpreted as mechanism-specific success.
Within-run sensory changes are separately saved in ANALYSIS.json.

{intervention3}

The context-cut arm at L2 zeros added edges while retaining expanded node dimensions.
It recovers the original dynamics in kernel tests and quantifies whether a trajectory
change is due to added anatomical propagation. No software coupling links outcomes.

## Normalization, sign and context-gain sensitivity

These are separate assumption changes at L2, cue A. Stage-3 resource arms retain
identical sensory schedules. They are not fitted replacements for primary results.

{sensitivity}

{sensitivity3}

Different normalization is not different anatomy. Sensitivity to the choice of
operator limits causal claims about boundary loss. The study does not choose whichever
variant makes a signal stronger. Primary may strengthen, weaken or remain unchanged;
all signed effects are retained in the tables and CSV.

## Additive class-consistent context comparison

The generic arm reveals an equation-level limitation: with incoming gain at most
0.05 and threshold0.15, added KCs cannot activate without direct imposed current.
They receive no such current. Therefore that arm alone cannot test restoration of
missing KC/APL physiology. This was identified analytically during the generic
battery, before any class-consistent simulation. Its completed results were preserved.

[CLASS_CONTEXT_AMENDMENT.md](CLASS_CONTEXT_AMENDMENT.md) prospectively adds a distinct
operator: existing PN→KC gain3, KC→original MBON/APL gain1, APL→KC gain1 on observed
added connections of these classes, fixed across all sizes. Original weights and
plastic compartments remain unchanged; no new teacher, tonic input or behavioral
threshold appears. Other context edges remain at0.05. Signed ALPN subclasses share
this gain as a model assumption, not a measured conductance. Unresolved modulators
still have zero fast effect. Zero sparse entries are removed only in this new arm;
short trajectories before/after removal are bit-identical.

This is a transparent study amendment, not part of the initial generic operator.
The L0 reference is reused because the operator has no added rows there. At L1/L3,
both cues are tested; mechanistic and sensitivity controls concentrate at L2.
The new arm is not selected because it gives a favorable result.

{class_effects}

{class_state}

Generic versus class-consistent differences occur on **identical anatomy** and must
be attributed to the transmission assumptions. Anatomy effects must be assessed
within one fixed operator across levels. Even class-consistent transmission does not
supply unknown cotransmitter/receptor physiology or additional justified plasticity.
Actual added-KC activation counts are saved in each class-run study.json.

## Stability, resets and computational measurements

{stability}

Clipping bounds rates to [0,1], so boundedness alone is not dynamic validation.
Peak saturation includes deliberately driven sensory/teacher neurons; the active
context counts and zero-input tails distinguish input following from runaway activity.
All snapshot restores recover baseline. Fast reset retains plastic state; reported
maximum differences are in raw rates, not normalized percentage units. Exact kernel
and context-cut tests precede the battery; full original L0 state reproduction and
full-reference replay are checked separately. Expanded acquisitions are not all
replayed twice: deterministic original-kernel behavior is not a substitute for an
unperformed expanded fresh-process replay.

Measured condition wall-time sum: **{totalwall:.2f}s**; process CPU sum:
**{totalcpu:.2f}s**. Individual runs also record initialization and process high-water
RSS. Batch high-water memory is not each condition's steady-state footprint. The
host is arm64 macOS with 8 logical CPUs and 8 GiB RAM; measurements include ordinary
concurrent host/research activity and are not a cloud SLA or controlled microbenchmark.

## Integrated-circuit anatomy

The independently selected contexts overlap substantially. Their unions are:

{union}

Real cross-system contacts include:

{direct}

Short anatomical paths and exact root examples are recorded in INTEGRATION.json.
[UNIFIED_MODEL_CONFLICTS.md](UNIFIED_MODEL_CONFLICTS.md) documents normalization,
dopamine locality/threshold, acute modulation, MBON11 gain and MBON07 sign conflicts.
The overlapping plastic rows total4,622 for KC→MBON07 and1,053 for KC→MBON11.
Shared roots are identified explicitly and are not counted as evidence of communication
between two distinct neurons. A shortest path is not evidence of meaningful effect:
it lacks receptor, timing, gain and body-state information.

A single anatomical graph can contain the candidate systems. A coherent physiological
model is not established by concatenating them. Their physiological assumptions differ:
Stage1 has target-specific MBON07→PAM excitation; Stage3 leaves other MBON07 output
signs unresolved. All compartments cannot inherit one global dopamine/receptor rule.
A future unified state must avoid duplicating shared cells or grafting incompatible
plasticity rules onto the same synapse. No Stage1-score + Stage2-score + Stage3-score
combination was implemented. The prior ~1e−6% resource×learned-value interaction remains
a constraint; this anatomical audit does not upgrade it to meaningful integration.

## Full-brain benchmark and temporal approximations

Conservative generic float64 rate dynamics: all 139,255 neurons update at every step,
tau50ms, ACh/GABA signed fast matrix, no unvalidated global plasticity. Sixteen seeded
ALPNs receive five seconds of current followed by five seconds of silence. Unknown
activity has no biological capability label. This is not the frozen learning model,
a LIF reproduction or a natural feeding simulation.

{bench}

Fast CSR has **10,231,005 stored nonzero signed pairs** using **123,329,084 bytes**.
Unresolved-sign anatomical edges remain in the provenance graph. The generic dynamic
checkpoint is 1,115,308 bytes and references immutable anatomy; it does not duplicate
connectivity or claim to include whole-brain plasticity. All three replay endpoints
and sampled traces match exactly. Rates remain finite and decay after input removal.

The generic matrix has maximum absolute row sum at most 0.05 because contact weights
divide by total input and are multiplied by 0.05. Rectification/clipping is
non-expansive. At dt10ms/tau50ms, the update has a maximum difference contraction
factor of 0.8 + 0.2×0.05 = 0.81 per step. Therefore this generic operator cannot
demonstrate a self-sustained recurrent attractor after input removal. Its stability
is largely mathematical construction, not recovered biological persistence. The
expanded learning models retain higher-gain original cores, so that whole-network
bound does not apply to them, but their added-context operator has the same low-gain
limitation. The measured performance must be interpreted alongside that constraint.

The 20ms approximation can exceed real time on this host. That is not evidence of
adequate physiological temporal fidelity. The 5ms/10ms/20ms runs differ in Euler
transients; no neural updates are silently skipped. Continuous operation is an
engineering possibility for this simple operator, not a validated behavioral model.
A richer multicompartment/receptor/plasticity model would require a new benchmark.

Full-context frozen-learning-kernel pilots, updating all neurons, measure:

{pilots}

All exceed the prospectively declared 120-second per-acquisition study budget. Thus
L4 full-duration conditioning trajectories were **not measured**; only the full
reference benchmark and one-second extension pilots were run. This is a study-scope
limit, not a claim that full-brain offline conditioning is computationally impossible.
Those projected times make offline work plausible, but the current extension kernels
are below real time at their fixed10ms step. The generic faster benchmark must not
be used to claim real-time performance for the learning extension.

## Architecture comparison

| Dimension | A: validated minimal circuits | B: larger integrated subnetwork | C: simplified full brain |
| --- | --- | --- | --- |
| Interpretability | Strongest for narrow Stage1 claim | More recurrent context, more sign/receptor assumptions | Most activity uninterpreted |
| Recurrent context | Deliberate cuts | High retention for target populations, residual whole-context boundary | Complete pinned proofread chemical graph only |
| Causal testing | Cheap, controlled interventions | Feasible but many interacting unknowns | Feasible offline; attribution harder |
| Plasticity | Local validated model mechanism | Local rules can persist; unified physiology unvalidated | No justified global plasticity rule |
| Missing physiology | Large boundary and body omissions | Body/peptide/receptor gaps remain | Body/peptide/receptor/electrical gaps remain |
| Cost | Small and fast | Hundreds MiB to low GiB in measured implementation | Generic ~0.7GiB peak; learning-extension pilots higher |
| Continuous use | Technically easy, behaviorally narrow | Technically plausible, acceptance not established | Generic20ms possible; learning10ms below real time here |
| Extensibility | Requires explicit boundary review | Natural common graph, shared-root reconciliation required | All roots available; no automatic interpretation |
| Hidden software decision risk | High if narrow outputs are overinterpreted | High if assumed gains/decoder dominate | High if neuron count legitimizes invented labels |

## Recommended physical architecture, conditional on further validation

**INSUFFICIENT EVIDENCE** to select Genesis Brain v1's operational neural substrate
from these behavioral claims. Retain C. elegans and Stage1 as existing baselines;
this recommendation does not concern whether Genesis should launch.

For research, use one headless sparse neural engine with immutable graph/version
manifests, string root identity at interfaces, array-indexed internal storage and
persistent per-neuron/per-synapse numerical state. Keep sensory/body boundary adapters,
biological inference and trace inspection separate. Support independently replayable
minimal, expanded and full-reference modes on the same data representation. Full
context is useful as an offline/shadow reference; targeted contexts remain easier
for controlled mechanism tests. The topology and supported circuit states must
constrain future behavior before a language layer is permitted to express it.

This is an architecture proposal only. No BrainAdapter change or canonical integration
has been made. No autonomous new behavior, threat, sleep, arousal or product-level
mapping is added. Stop for review.

## Evidence index

- [Prospective protocol](PLAN.md)
- [Anatomical manifest](anatomy/manifest.json)
- [Counts and all population retention](anatomy/counts.json)
- [Anatomical integration and omitted partners](INTEGRATION.json)
- [All numeric comparisons](ANALYSIS.json)
- [Trajectory CSV](TRAJECTORIES.csv)
- [Kernel equality checks](kernel-checks.json)
- [Full-protocol budget measurements](FULL_PROTOCOL_BUDGET.json)
- [Preservation record](PRESERVATION.json)
- [Reproduction instructions](README.md)

Licensing caveats remain inherited from the pinned sources; no commercial data
redistribution or deployment occurs. The complete study manifest hashes all artifacts.
'''
 (H/'REPORT.md').write_text(text)
 print('Report rendered from sealed measurements.')
if __name__=='__main__':main()

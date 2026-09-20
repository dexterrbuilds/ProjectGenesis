# Boundary-Closure and Brain Architecture Study

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

## Quantitative answer: anatomy versus functional participation

| Stage / cue | L0 effect | L3 conservative | L3 class-consistent | Class − conservative (percentage points) | Relative class change |
| --- | --- | --- | --- | --- | --- |
| 1 / A | 49.945215% | 49.944865% | 50.326803% | 0.381938501 | 0.76472026% |
| 1 / B | 37.673009% | 37.67269% | 37.820343% | 0.147652647 | 0.3919355% |
| 2 / A | 0.0016534739% | 0.0016476179% | 0.0016170668% | -3.05510563e-05 | -1.8542562% |
| 2 / B | 0.0022991646% | 0.0022941299% | 0.0022224071% | -7.17228228e-05 | -3.1263628% |
| 3 / A | 0.053774383% | 0.053770454% | 0.053744443% | -2.60103261e-05 | -0.048372897% |
| 3 / B | 0.04958433% | 0.049588103% | 0.049706731% | 0.000118628326 | 0.23922739% |

Stage 1 is nearly unchanged by generic closure and modestly strengthened by the
class-consistent operator. Stage 2 weakens slightly under both operators; no sign
reversal or magnitude rescue occurs. Stage 3 remains very small, with opposite
minor cue-dependent changes rather than systematic strengthening. Restored active
neurons therefore affect responses, but do not supply the missing behavioral evidence.
These are counterbalanced single-seed comparisons, not population confidence intervals.

Normalization has a much larger influence on the modeled effects. For cue A at L2,
Stage 1 selective conditioning changes from 49.944896% to 16.963974% under full-input
core normalization. Stage 2 specificity changes from 0.0016472495% to 1.1407196% under
role-based core normalization (about 692.5×), on identical anatomy. These alternatives
are sensitivity results, never selected as the preferred biological answer.

**Attribution:** the study directly demonstrates consequential computational
assumptions and improves chemical boundary retention, but does not establish that
boundary loss is the primary cause of weak Stage 2/3 effects. Nor does it establish
that the biological mechanisms themselves are weak. Unknown receptor gains,
neuromodulatory/body drive and incomplete physiological participation remain
confounded. Both boundary and approximation limitations remain plausible; an exact
causal allocation is **unidentified**. The experiment gives no basis for selecting
an architecture by whichever assumption produces the largest signal.

## Preservation and experimental scope

All three original stages, C. elegans, canonical identity, seven life cycles and
disabled schedule are frozen. FROZEN_BEFORE.json records 2,084 protected files.
PRESERVATION.json records the final hash comparison and database verification.
Stage 1 remains PASS; Stages 2 and 3 remain PARTIAL-INCONCLUSIVE. No Genesis imports,
life cycles, migration, activation, LLM, planner, wallet or digital actions occur.

The study runs **156 full-duration conditions** (100 generic-context and 56 class-consistent) using each original primary seed
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

| Seed | Level | Neurons | Directed pairs | Neuropil rows | Contacts | Omitted inputs | Omitted outputs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | L0 | 1054 | 80423 | 102889 | 226143 | 305890 | 531695 |
| 1 | L1 | 5330 | 483548 | 606526 | 1430877 | 1177206 | 990134 |
| 1 | L2 | 11264 | 1107695 | 1286384 | 4149804 | 870925 | 1160337 |
| 1 | L3 | 37752 | 5334602 | 6667274 | 22385011 | 2782769 | 1151191 |
| 1 | L4 | 139255 | 15091983 | 16847997 | 54492922 | 0 | 0 |
| 2 | L0 | 1172 | 57804 | 73715 | 160848 | 539717 | 1132985 |
| 2 | L1 | 6737 | 661903 | 830762 | 2095131 | 1154389 | 1275210 |
| 2 | L2 | 11513 | 1148553 | 1344543 | 4343271 | 753665 | 1083908 |
| 2 | L3 | 37892 | 5348360 | 6684319 | 22425609 | 2783082 | 1147021 |
| 2 | L4 | 139255 | 15091983 | 16847997 | 54492922 | 0 | 0 |
| 3 | L0 | 4563 | 304192 | 375699 | 905536 | 597746 | 1012673 |
| 3 | L1 | 9449 | 949697 | 1191901 | 3239231 | 2747078 | 2529221 |
| 3 | L2 | 13578 | 1397770 | 1665710 | 5292750 | 2252881 | 2280913 |
| 3 | L3 | 37908 | 5353837 | 6691970 | 22447365 | 2794344 | 1232165 |
| 3 | L4 | 139255 | 15091983 | 16847997 | 54492922 | 0 | 0 |

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

| Stage/population | L0 input / output | L1 input / output | L2 input / output | L3 input / output | L4 input / output |
| --- | --- | --- | --- | --- | --- |
| S1 KC | 89.044701% / 63.690711% | 99.125531% / 99.803355% | 99.168287% / 99.930509% | 99.735827% / 99.970922% | 100% / 100% |
| S1 MBON_app | 94.723637% / 34.604346% | 99.863149% / 86.469865% | 99.878355% / 90.241902% | 100% / 99.876999% | 100% / 100% |
| S1 DAN_app | 41.491812% / 50.668287% | 92.041965% / 98.614824% | 94.741556% / 98.930741% | 100% / 99.975699% | 100% / 100% |
| S1 APL | 33.442604% / 34.124753% | 99.348768% / 99.86024% | 99.481941% / 99.890189% | 99.966341% / 99.963396% | 100% / 100% |
| S2 MBON | 80.803925% / 9.2117324% | 98.987182% / 87.427437% | 99.256211% / 91.109074% | 100% / 99.725023% | 100% / 100% |
| S2 DAN | 47.23779% / 64.041368% | 91.473179% / 92.521877% | 92.954363% / 92.680986% | 100% / 100% | 100% / 100% |
| S2 APL | 20.713486% / 21.852434% | 99.691928% / 99.850159% | 99.725233% / 99.858283% | 99.978806% / 99.973823% | 100% / 100% |
| S3 MB11 | 94.988566% / 42.061404% | 99.936749% / 95.643275% | 99.975673% / 95.643275% | 100% / 100% | 100% / 100% |
| S3 MB18 | 86.678939% / 19.33976% | 99.76571% / 95.617879% | 99.924692% / 96.187555% | 100% / 100% | 100% / 100% |
| S3 DAN | 69.727908% / 84.898746% | 95.198652% / 98.28351% | 95.241994% / 98.302797% | 99.990368% / 100% | 100% / 100% |
| S3 APL | 72.793539% / 72.976242% | 99.685873% / 99.882655% | 99.716907% / 99.88807% | 99.978806% / 99.973823% | 100% / 100% |
| S3 LH | 26.864464% / 1.1036841% | 95.333783% / 93.206902% | 99.002023% / 94.637028% | 100% / 99.984455% | 100% / 100% |
| S3 LHCENT | 16.611496% / 22.152552% | 94.559133% / 92.586713% | 96.14204% / 95.00754% | 100% / 100% | 100% / 100% |
| S3 OA | 4.2818541% / 4.0559441% | 88.651008% / 85.571096% | 88.796508% / 85.874126% | 99.771357% / 99.74359% | 100% / 100% |

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

| Stage | Cue | Level | Baseline | Post | Selective effect |
| --- | --- | --- | --- | --- | --- |
| 1 | A | 0 | 0.0707800207 | 0.0312428813 | 49.945215% |
| 1 | B | 0 | 0.11291118 | 0.0592288652 | 37.673009% |
| 1 | A | 1 | 0.070780361 | 0.0312432403 | 49.944962% |
| 1 | B | 1 | 0.112911609 | 0.0592294874 | 37.67273% |
| 1 | A | 2 | 0.0707801895 | 0.0312432082 | 49.944896% |
| 1 | B | 2 | 0.112911884 | 0.0592296215 | 37.672699% |
| 1 | A | 3 | 0.0707801491 | 0.0312432116 | 49.944865% |
| 1 | B | 3 | 0.112911885 | 0.059229623 | 37.67269% |
| 2 | A | 0 | 0.00385359564 | 0.00385353164 | 0.0016534739% |
| 2 | B | 0 | 0.00900013838 | 0.00899992919 | 0.0022991646% |
| 2 | A | 1 | 0.00385096985 | 0.00385090618 | 0.0016462963% |
| 2 | B | 1 | 0.00899880558 | 0.00899859703 | 0.0022924847% |
| 2 | A | 2 | 0.0038509272 | 0.00385086349 | 0.0016472495% |
| 2 | B | 2 | 0.00899879295 | 0.00899858435 | 0.0022929984% |
| 2 | A | 3 | 0.00385097336 | 0.00385090963 | 0.0016476179% |
| 2 | B | 3 | 0.00899881325 | 0.00899860454 | 0.0022941299% |

These expanded-context results have no authority to rewrite the narrow accepted
Stage-1 PASS. They also do not convert Stage 2 into success simply by preserving a
nonzero persistent change. Sensory and plastic states, actual stimuli and traces
are saved for every condition.

## Generic-context Stage 3 trajectories

State contrast is low/high−1 during the final maintained-cue window; experience is
trial10/trial1−1 at low resource. Original thresholds remain 10% MBON11 state contrast
and joint 5% experience magnitudes. No threshold or sign-flipped decoder was fitted.

| Level | Cue | MBON11 state contrast | MBON11 experience low | MBON18 state contrast | LH state contrast | LH experience low |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | A | 0.053774383% | -0.026144405% | -0.00031581055% | -3.6524762e-05% | 1.7768778e-05% |
| 0 | B | 0.04958433% | -0.023822375% | -0.00028719818% | -9.4713796e-06% | 4.5677143e-06% |
| 1 | A | 0.053769944% | -0.026142218% | -0.00031577829% | -3.6515687e-05% | 1.7764394e-05% |
| 1 | B | 0.049587006% | -0.023823633% | -0.00028720686% | -9.451511e-06% | 4.558155e-06% |
| 2 | A | 0.053769929% | -0.026142201% | -0.00031577568% | -3.6263673e-05% | 1.7641705e-05% |
| 2 | B | 0.049587428% | -0.023823847% | -0.00028720956% | -9.4510155e-06% | 4.5579162e-06% |
| 3 | A | 0.053770454% | -0.026142455% | -0.00031577885% | -3.6264244e-05% | 1.7641983e-05% |
| 3 | B | 0.049588103% | -0.023824172% | -0.00028721352% | -9.4511957e-06% | 4.5580035e-06% |

Maintained-cue responses alone are not pursuit. No descending motor system, choice
policy, physical acquisition loop or voluntary abstention mechanism was introduced.
A change in LH/MBON response is reported as neural activity only.

## Intervention specificity

All interventions retain intact denominators. Relevant dopamine silencing, frozen
plasticity and the original comparator lesion are repeated at each measured level.
The Stage-1 matched_dan comparator removes one other-compartment neuron, whereas
silence_dan removes the whole relevant population: this is the original comparator,
not a newly count-matched lesion of the whole population. Interpret that limitation.

| Stage | Level | Intervention | Selective effect | Reduction vs intact | PN/KC baseline change vs intact |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | freeze | 0% | 100% | 0% |
| 1 | 0 | matched_dan | 49.945215% | 0% | 0% |
| 1 | 0 | silence_dan | 0% | 100% | 0% |
| 1 | 1 | freeze | 0% | 100% | 0% |
| 1 | 1 | matched_dan | 49.944962% | 0% | 0% |
| 1 | 1 | silence_dan | 0% | 100% | 0% |
| 1 | 2 | freeze | 0% | 100% | 0% |
| 1 | 2 | matched_dan | 49.944896% | 0% | 0% |
| 1 | 2 | silence_dan | 0% | 100% | 0% |
| 1 | 3 | freeze | 0% | 100% | 0% |
| 1 | 3 | matched_dan | 49.944865% | 0% | 0% |
| 1 | 3 | silence_dan | 0% | 100% | 0% |
| 2 | 0 | freeze | 0% | 100% | 3.7847503e-10% |
| 2 | 0 | matched_control | 0.0016466566% | 0.41230484% | 0.00033551734% |
| 2 | 0 | silence_dan | 0% | 100% | 3.7847503e-10% |
| 2 | 1 | freeze | 0% | 100% | 3.7643222e-10% |
| 2 | 1 | matched_control | 0.0016394022% | 0.41876635% | 0.0003356022% |
| 2 | 1 | silence_dan | 0% | 100% | 3.7643222e-10% |
| 2 | 2 | freeze | 0% | 100% | 3.7663206e-10% |
| 2 | 2 | matched_control | 0.0016403554% | 0.41852316% | 0.0003356084% |
| 2 | 2 | silence_dan | 0% | 100% | 3.7663206e-10% |
| 2 | 3 | freeze | 0% | 100% | 3.7672088e-10% |
| 2 | 3 | matched_control | 0.0016407235% | 0.4184424% | 0.00033560885% |
| 2 | 3 | silence_dan | 0% | 100% | 3.7672088e-10% |

Sensory change compares lesion versus intact baseline for the same cue and level.
Loss of sensory drive is never interpreted as mechanism-specific success.
Within-run sensory changes are separately saved in ANALYSIS.json.

| Level | Intervention | MBON11 contrast | Reduction | Experience low | PN state contrast | KC state contrast |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | freeze_plasticity | 0.017080778% | 68.236217% | 0% | 1.1658075e-08% | -1.2327152e-07% |
| 0 | matched_control | 0.053774572% | -0.00035148625% | -0.026144499% | 3.69627e-08% | -3.5994714e-07% |
| 0 | silence_dan | 0% | 100% | 0% | 0% | 0% |
| 1 | freeze_plasticity | 0.017079409% | 68.236141% | 0% | 1.1372325e-08% | -1.2350668e-07% |
| 1 | matched_control | 0.053769242% | 0.0013066318% | -0.026141879% | 3.6066972e-08% | -3.6069329e-07% |
| 1 | silence_dan | 0% | 100% | 0% | 0% | 0% |
| 2 | freeze_plasticity | 0.017079419% | 68.236114% | 0% | 1.1731038e-08% | -1.2310977e-07% |
| 2 | matched_control | 0.053769229% | 0.0013022739% | -0.026141862% | 3.7192738e-08% | -3.5944382e-07% |
| 2 | silence_dan | 0% | 100% | 0% | 0% | 0% |
| 3 | freeze_plasticity | 0.017079586% | 68.236114% | 0% | 1.1730417e-08% | -1.2311115e-07% |
| 3 | matched_control | 0.053769751% | 0.0013058941% | -0.026142116% | 3.719105e-08% | -3.5944774e-07% |
| 3 | silence_dan | 0% | 100% | 0% | 0% | 0% |

The context-cut arm at L2 zeros added edges while retaining expanded node dimensions.
It recovers the original dynamics in kernel tests and quantifies whether a trajectory
change is due to added anatomical propagation. No software coupling links outcomes.

## Normalization, sign and context-gain sensitivity

These are separate assumption changes at L2, cue A. Stage-3 resource arms retain
identical sensory schedules. They are not fitted replacements for primary results.

| Stage | L2 assumption | Selective effect | Baseline | Post |
| --- | --- | --- | --- | --- |
| 1 | context_cut | 49.945215% | 0.0707800207 | 0.0312428813 |
| 1 | context_double | 49.943937% | 0.0707807354 | 0.0312442068 |
| 1 | context_half | 49.945135% | 0.0707800617 | 0.0312429625 |
| 1 | full_normalization | 16.963974% | 0.010709672 | 0.00875624261 |
| 1 | glutamate_inhibitory | 49.947782% | 0.070775415 | 0.0312389086 |
| 2 | context_cut | 0.0016534739% | 0.00385359564 | 0.00385353164 |
| 2 | context_double | 0.0016286515% | 0.00384295707 | 0.0038428942 |
| 2 | context_half | 0.0016519149% | 0.00385292712 | 0.0038528632 |
| 2 | glutamate_inhibitory | 0.0016441152% | 0.00385085625 | 0.00385079266 |
| 2 | role_normalization | 1.1407196% | 0.0925622321 | 0.0914570541 |

| L2 assumption | MBON11 contrast | MBON11 experience low | LH contrast | LH experience low |
| --- | --- | --- | --- | --- |
| context_cut | 0.053774383% | -0.026144405% | -3.6524762e-05% | 1.7768778e-05% |
| context_double | 0.053759253% | -0.026136878% | -3.6021444e-05% | 1.7523572e-05% |
| context_half | 0.053773176% | -0.026143808% | -3.6507043e-05% | 1.7760134e-05% |
| glutamate_inhibitory | 0.053734817% | -0.026125061% | -3.6415043e-05% | 1.7715255e-05% |
| role_normalization | 7.3799751e-07% | -4.9814816e-07% | -3.275984e-07% | 2.2112894e-07% |

Different normalization is not different anatomy. Sensitivity to the choice of
operator limits causal claims about boundary loss. The study does not choose whichever
variant makes a signal stronger. Primary may strengthen, weaken or remain unchanged;
all signed effects are retained in the tables and CSV.

## Additive class-consistent context comparison

The generic arm reveals an equation-level limitation: with incoming gain at most
0.05 and threshold 0.15, added KCs cannot activate without direct imposed current.
They receive no such current. Therefore that arm alone cannot test restoration of
missing KC/APL physiology. This was identified analytically during the generic
battery, before any class-consistent simulation. Its completed results were preserved.

[CLASS_CONTEXT_AMENDMENT.md](CLASS_CONTEXT_AMENDMENT.md) prospectively adds a distinct
operator: existing PN→KC gain 3, KC→original MBON/APL gain 1, APL→KC gain 1 on observed
added connections of these classes, fixed across all sizes. Original weights and
plastic compartments remain unchanged; no new teacher, tonic input or behavioral
threshold appears. Other context edges remain at 0.05. Signed ALPN subclasses share
this gain as a model assumption, not a measured conductance. Unresolved modulators
still have zero fast effect. Zero sparse entries are removed only in this new arm;
short trajectories before/after removal are bit-identical.

This is a transparent study amendment, not part of the initial generic operator.
The L0 reference is reused because the operator has no added rows there. At L1/L3,
both cues are tested; mechanistic and sensitivity controls concentrate at L2.
The new arm is not selected because it gives a favorable result.

| Stage | Level | Cue | Assumption | Intervention | Selective effect | Baseline | Post |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | A | primary | intact | 50.327537% | 0.0692646879 | 0.0303546895 |
| 1 | 1 | B | primary | intact | 37.815528% | 0.110679085 | 0.0579909278 |
| 1 | 2 | A | context_cut | intact | 49.945215% | 0.0707800207 | 0.0312428813 |
| 1 | 2 | A | context_double | intact | 52.726249% | 0.0612391272 | 0.0255947226 |
| 1 | 2 | A | context_half | intact | 49.966138% | 0.0706894976 | 0.0311910051 |
| 1 | 2 | A | full_normalization | intact | 16.827001% | 0.0107133452 | 0.0087763472 |
| 1 | 2 | A | glutamate_inhibitory | intact | 50.329759% | 0.0692598759 | 0.0303504588 |
| 1 | 2 | A | primary | freeze | 0% | 0.0692645328 | 0.0692645328 |
| 1 | 2 | A | primary | intact | 50.326835% | 0.0692645328 | 0.0303546663 |
| 1 | 2 | A | primary | matched_dan | 50.326835% | 0.0692645328 | 0.0303546663 |
| 1 | 2 | A | primary | silence_dan | 0% | 0.0692645328 | 0.0692645328 |
| 1 | 2 | B | primary | intact | 37.820352% | 0.110670974 | 0.0579809922 |
| 1 | 3 | A | primary | intact | 50.326803% | 0.069264492 | 0.0303546695 |
| 1 | 3 | B | primary | intact | 37.820343% | 0.110670976 | 0.0579809938 |
| 2 | 1 | A | primary | intact | 0.0016157984% | 0.00378338957 | 0.00378332818 |
| 2 | 1 | B | primary | intact | 0.0022207635% | 0.00879015809 | 0.00878996084 |
| 2 | 2 | A | context_cut | intact | 0.0016534739% | 0.00385359564 | 0.00385353164 |
| 2 | 2 | A | context_double | intact | 0.0014669937% | 0.00344362626 | 0.00344357559 |
| 2 | 2 | A | context_half | intact | 0.0016495445% | 0.00384793097 | 0.00384786722 |
| 2 | 2 | A | glutamate_inhibitory | intact | 0.0016127675% | 0.00378317307 | 0.0037831118 |
| 2 | 2 | A | primary | freeze | 0% | 0.00378329531 | 0.00378329531 |
| 2 | 2 | A | primary | intact | 0.0016166852% | 0.00378329252 | 0.0037832311 |
| 2 | 2 | A | primary | matched_control | 0.0016096418% | 0.00378323976 | 0.00378317861 |
| 2 | 2 | A | primary | silence_dan | 0% | 0.00378329531 | 0.00378329531 |
| 2 | 2 | B | primary | intact | 0.0022212737% | 0.00879014314 | 0.00878994584 |
| 2 | 2 | A | role_normalization | intact | 1.1166697% | 0.0909561733 | 0.0898941679 |
| 2 | 3 | A | primary | intact | 0.0016170668% | 0.00378333866 | 0.00378327723 |
| 2 | 3 | B | primary | intact | 0.0022224071% | 0.00879016353 | 0.00878996614 |

| Level | Cue | Assumption | Intervention | MBON11 state contrast | MBON11 experience low | LH state contrast | LH experience low |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A | primary | intact | 0.053743948% | -0.026129046% | -3.6490938e-05% | 1.7751969e-05% |
| 1 | B | primary | intact | 0.049705932% | -0.023879387% | -9.4688175e-06% | 4.566231e-06% |
| 2 | A | context_cut | intact | 0.053774383% | -0.026144405% | -3.6524762e-05% | 1.7768778e-05% |
| 2 | A | context_double | intact | 0.053400635% | -0.025958624% | -3.578839e-05% | 1.7407437e-05% |
| 2 | A | context_half | intact | 0.053771223% | -0.026142842% | -3.6504369e-05% | 1.7758821e-05% |
| 2 | A | glutamate_inhibitory | intact | 0.05370848% | -0.026111719% | -3.636073e-05% | 1.7688389e-05% |
| 2 | A | primary | freeze_plasticity | 0.017071925% | 0% | -1.1546558e-05% | 0% |
| 2 | A | primary | intact | 0.053743905% | -0.026129011% | -3.6242278e-05% | 1.7630913e-05% |
| 2 | A | primary | matched_control | 0.053743204% | -0.026128672% | -3.6240209e-05% | 1.7629909e-05% |
| 2 | A | primary | silence_dan | 0% | 0% | 0% | 0% |
| 2 | B | primary | intact | 0.049706021% | -0.023879431% | -9.4685595e-06% | 4.5661045e-06% |
| 2 | A | role_normalization | intact | 7.3814748e-07% | -4.9824921e-07% | -3.2819559e-07% | 2.2153186e-07% |
| 3 | A | primary | intact | 0.053744443% | -0.026129272% | -3.6243515e-05% | 1.7631517e-05% |
| 3 | B | primary | intact | 0.049706731% | -0.023879773% | -9.4687453e-06% | 4.5661945e-06% |

Generic versus class-consistent differences occur on **identical anatomy** and must
be attributed to the transmission assumptions. Anatomy effects must be assessed
within one fixed operator across levels. Even class-consistent transmission does not
supply unknown cotransmitter/receptor physiology or additional justified plasticity.
Actual added-KC activation counts are saved in each class-run study.json.

| Stage | Level | Cue | Active generic context | Active class context | Active added KCs (class) |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | A | 356 | 825 | 209 |
| 1 | 1 | B | 356 | 825 | 209 |
| 1 | 2 | A | 3223 | 3672 | 236 |
| 1 | 2 | B | 3223 | 3672 | 236 |
| 1 | 3 | A | 12827 | 13597 | 236 |
| 1 | 3 | B | 12827 | 13597 | 236 |
| 2 | 1 | A | 1008 | 1716 | 537 |
| 2 | 1 | B | 1008 | 1716 | 537 |
| 2 | 2 | A | 3570 | 4174 | 537 |
| 2 | 2 | B | 3570 | 4174 | 537 |
| 2 | 3 | A | 15358 | 16170 | 537 |
| 2 | 3 | B | 15358 | 16170 | 537 |
| 3 | 1 | A | 2725 | 2829 | 26 |
| 3 | 1 | B | 2725 | 2829 | 26 |
| 3 | 2 | A | 4951 | 5049 | 26 |
| 3 | 2 | B | 4951 | 5049 | 26 |
| 3 | 3 | A | 16747 | 16863 | 26 |
| 3 | 3 | B | 16747 | 16863 | 26 |

Activity means rate >1e−8 and is a numerical diagnostic, not a behavioral label.
Maxima include acquisition and disposable probes; Stage 3 reports the larger of its
two resource states. Generic added KCs are silent by the analytical gain/threshold
bound. Class-consistent added KCs are demonstrably active. Merely counting active
context neurons does not establish useful recurrent integration.


## Stability, resets and computational measurements

| Stage / level | Maximum rate | Maximum clipped fraction | Maximum active context neurons | Largest reset delta | Per-condition wall range (s) | Process peak MiB |
| --- | --- | --- | --- | --- | --- | --- |
| S1 L0 | 1 | 3.6053131% | 0 | 0 | 3.70–4.38 | 534.77 |
| S1 L1 | 1 | 0.71294559% | 356 | 0 | 13.39–14.16 | 614.55 |
| S1 L2 | 1 | 0.33735795% | 3329 | 0 | 27.41–56.80 | 612.97 |
| S1 L3 | 1 | 0.10065692% | 12827 | 0 | 218.85–242.05 | 801.30 |
| S2 L0 | 1 | 1.1945392% | 0 | 8.03246358e-14 | 0.71–0.94 | 494.94 |
| S2 L1 | 1 | 0.20780763% | 1008 | 8.00436106e-14 | 5.45–5.64 | 603.09 |
| S2 L2 | 1 | 0.62538001% | 4565 | 3.60284136e-10 | 16.92–20.21 | 612.08 |
| S2 L3 | 1 | 0.036947113% | 15358 | 8.01077954e-14 | 67.25–68.38 | 931.52 |
| S3 L0 | 1 | 0.3506465% | 0 | 6.9388939e-18 | 11.88–20.85 | 656.94 |
| S3 L1 | 1 | 0.16933009% | 2725 | 6.9388939e-18 | 27.59–32.32 | 757.78 |
| S3 L2 | 1 | 0.47135071% | 6082 | 6.9388939e-18 | 63.23–82.13 | 758.55 |
| S3 L3 | 1 | 0.04220745% | 16747 | 3.46944695e-18 | 178.71–385.98 | 935.88 |

Clipping bounds rates to [0,1], so boundedness alone is not dynamic validation.
Peak saturation includes deliberately driven sensory/teacher neurons; the active
context counts and zero-input tails distinguish input following from runaway activity.
All snapshot restores recover baseline. Fast reset retains plastic state; reported
maximum differences are in raw rates, not normalized percentage units. Stage 1
reset differences compare saved original-population means; Stage 2/3 compare all
modeled-neuron probe rates. The Stage-2 L2 normalization alternative reaches about
3.6e−10, exceeding the original 1e−10 numerical tolerance; it must not be called
an exact transient-free recall result. Primary Stage-2 resets remain near 8e−14. Exact kernel
and context-cut tests precede the battery; full original L0 state reproduction and
full-reference replay are checked separately. Expanded acquisitions are not all
replayed twice: deterministic original-kernel behavior is not a substitute for an
unperformed expanded fresh-process replay.

Measured condition wall-time sum: **9228.27s**; process CPU sum:
**9166.08s**. Individual runs also record initialization and process high-water
RSS. Batch high-water memory is not each condition's steady-state footprint. The
host is arm64 macOS with 8 logical CPUs and 8 GiB RAM; measurements include ordinary
concurrent host/research activity and are not a cloud SLA or controlled microbenchmark.

### Class-consistent intervention specificity

| Stage | Resource | Intervention | Selective-effect reduction (S1/S2) | PN/KC baseline change vs intact |
| --- | --- | --- | --- | --- |
| 1 | 0.2 | freeze | 100% | 0% |
| 1 | 0.2 | matched_dan | 0% | 0% |
| 1 | 0.2 | silence_dan | 100% | 0% |
| 2 | 0.2 | freeze | 100% | 3.6941561e-10% |
| 2 | 0.2 | matched_control | 0.43567279% | 0.00034212124% |
| 2 | 0.2 | silence_dan | 100% | 3.6941561e-10% |
| 3 | 0.2 | freeze_plasticity | undefined | 2.4488633e-09% |
| 3 | 0.2 | matched_control | undefined | 7.7562292e-05% |
| 3 | 0.2 | silence_dan | undefined | 7.9749563e-08% |
| 3 | 0.8 | freeze_plasticity | undefined | 5.7148619e-09% |
| 3 | 0.8 | matched_control | undefined | 7.7562536e-05% |
| 3 | 0.8 | silence_dan | undefined | 1.8608486e-07% |

Stage 3 effect reductions use the paired-resource contrasts already reported above,
not a single-resource depression score. Frozen Stage 3 plasticity removes the local
experience effect while acute resource gating remains; those are different outcomes.
Relevant DA silencing removes the modeled pathway, whereas matched comparators
largely preserve it. This is conditional causal evidence within the model; it does
not supply the missing behavioral magnitude or a validated integrated decision.

### Class-consistent performance and stability

| Stage | Level | Wall seconds/condition | Batch peak MiB | Largest saturation fraction | Largest reset difference |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 17.74–18.22 | 614.75 | 0.71294559% | 0 |
| 1 | 2 | 8.49–35.90 | 612.95 | 0.33735795% | 0 |
| 1 | 3 | 127.81–129.97 | 802.03 | 0.10065692% | 0 |
| 2 | 1 | 7.23–7.39 | 602.98 | 0.20780763% | 7.62914037e-14 |
| 2 | 2 | 2.05–12.08 | 612.14 | 0.5993225% | 3.45566298e-10 |
| 2 | 3 | 92.37–95.85 | 711.41 | 0.036947113% | 7.63503843e-14 |
| 3 | 1 | 38.14–41.13 | 757.67 | 0.16933009% | 5.20417043e-18 |
| 3 | 2 | 23.98–56.12 | 758.75 | 0.47135071% | 3.46944695e-18 |
| 3 | 3 | 140.71–277.76 | 909.02 | 0.04220745% | 4.33680869e-19 |

All 156 runs remain finite. Every original snapshot restores its own baseline.
Zero sparse entries were removed in the class-consistent operator, whereas the
conservative extension retains explicit zeros; operator values and host contention
also differ. Runtime differences between families are therefore **not a pure
neuronal-activity cost comparison**. No previously measured timing is replaced.

| Saved artifact family | Exact bytes | MiB |
| --- | --- | --- |
| anatomy | 330336090 | 315.03 |
| runs | 83661707 | 79.79 |
| class-runs | 49202059 | 46.92 |
| benchmarks | 5538497 | 5.28 |

Storage is measured file size, not cloud storage billing. The anatomy arrays retain
all contacts/provenance independently of dynamic checkpoints. Every experiment also
saves full numerical neural/plastic snapshots; generic full-brain benchmark checkpoints
contain only rates/clock because that benchmark has no plasticity.

## Integrated-circuit anatomy

The independently selected contexts overlap substantially. Their unions are:

| Level | Union neurons | Pairs | Contacts |
| --- | --- | --- | --- |
| L0 | 5480 | 368794 | 1064833 |
| L1 | 9869 | 1011284 | 3492591 |
| L2 | 13934 | 1454493 | 5515878 |
| L3 | 37913 | 5357236 | 22458018 |
| L4 | 139255 | 15091983 | 54492922 |

Real cross-system contacts include:

| Source | Target | Contacts | Pairs |
| --- | --- | --- | --- |
| S1_DAN_app | S3_DAN | 4 | 4 |
| S1_DAN_app | S3_MB11 | 20 | 10 |
| S1_DAN_app | S3_VALUE | 1347 | 50 |
| S1_DAN_av | S3_MB11 | 894 | 4 |
| S1_DAN_av | S3_OA | 3 | 2 |
| S1_DAN_av | S3_VALUE | 1 | 1 |
| S1_MBON_app | S3_MB11 | 2 | 2 |
| S1_MBON_av | S2_DAN | 3 | 1 |
| S1_MBON_av | S2_MBON | 10 | 4 |
| S1_MBON_av | S3_DAN | 358 | 4 |
| S1_MBON_av | S3_MB18 | 36 | 4 |
| S1_MBON_av | S3_OA | 1 | 1 |
| S1_MBON_av | S3_VALUE | 241 | 8 |
| S2_DAN | S3_MB18 | 2 | 2 |
| S2_MBON | S3_LH | 31 | 4 |
| S2_MBON | S3_MB18 | 7 | 4 |
| S3_DAN | S1_DAN_app | 6 | 5 |
| S3_DAN | S1_MBON_app | 1 | 1 |
| S3_DAN | S1_MBON_av | 894 | 4 |
| S3_LH | S1_DAN_app | 1 | 1 |
| S3_LH | S2_DAN | 8 | 2 |
| S3_LH | S2_MBON | 1 | 1 |
| S3_MB11 | S1_DAN_app | 54 | 16 |
| S3_MB11 | S1_DAN_av | 358 | 4 |
| S3_MB11 | S1_MBON_app | 115 | 4 |
| S3_MB11 | S2_DAN | 3 | 1 |
| S3_MB11 | S2_MBON | 10 | 4 |
| S3_MB18 | S1_DAN_app | 1 | 1 |
| S3_MB18 | S1_MBON_app | 1 | 1 |
| S3_MB18 | S1_MBON_av | 1 | 1 |
| S3_MB18 | S2_DAN | 11 | 3 |
| S3_MB18 | S2_MBON | 12 | 3 |
| S3_OA | S1_DAN_av | 2 | 1 |
| S3_OA | S1_MBON_av | 47 | 2 |
| S3_VALUE | S1_DAN_app | 156 | 42 |
| S3_VALUE | S1_MBON_av | 4 | 4 |

Short anatomical paths and exact root examples are recorded in INTEGRATION.json.
[UNIFIED_MODEL_CONFLICTS.md](UNIFIED_MODEL_CONFLICTS.md) documents normalization,
dopamine locality/threshold, acute modulation, MBON11 gain and MBON07 sign conflicts.
The overlapping plastic rows total 4,622 for KC→MBON07 and 1,053 for KC→MBON11.
Shared roots are identified explicitly and are not counted as evidence of communication
between two distinct neurons. A shortest path is not evidence of meaningful effect:
it lacks receptor, timing, gain and body-state information.

A single anatomical graph can contain the candidate systems. A coherent physiological
model is not established by concatenating them. Their physiological assumptions differ:
Stage 1 has target-specific MBON07→PAM excitation; Stage 3 leaves other MBON07 output
signs unresolved. All compartments cannot inherit one global dopamine/receptor rule.
A future unified state must avoid duplicating shared cells or grafting incompatible
plasticity rules onto the same synapse. No Stage 1-score + Stage 2-score + Stage 3-score
combination was implemented. The prior ~1e−6% resource×learned-value interaction remains
a constraint; this anatomical audit does not upgrade it to meaningful integration.

## Full-brain benchmark and temporal approximations

Conservative generic float64 rate dynamics: all 139,255 neurons update at every step,
tau 50 ms, ACh/GABA signed fast matrix, no unvalidated global plasticity. Sixteen seeded
ALPNs receive five seconds of current followed by five seconds of silence. Unknown
activity has no biological capability label. This is not the frozen learning model,
a LIF reproduction or a natural feeding simulation.

| dt | Initialization s | 10 simulated seconds / wall s | Updates/s | Sim/wall | CPU (% one core) | Peak MiB | Checkpoint bytes / write ms / load ms | Replay s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.005 | 0.959 | 24.583 | 81.36 | 0.407 | 99.0 | 699.19 | 1115308 / 1.985 / 0.920 | 26.806 |
| 0.01 | 0.836 | 11.893 | 84.08 | 0.841 | 98.5 | 721.11 | 1115308 / 0.910 / 1.115 | 11.415 |
| 0.02 | 0.951 | 6.910 | 72.36 | 1.447 | 99.0 | 725.33 | 1115308 / 2.023 / 0.991 | 7.044 |

Fast CSR has **10,231,005 stored nonzero signed pairs** using **123,329,084 bytes**.
Unresolved-sign anatomical edges remain in the provenance graph. The generic dynamic
checkpoint is 1,115,308 bytes and references immutable anatomy; it does not duplicate
connectivity or claim to include whole-brain plasticity. All three replay endpoints
and sampled traces match exactly. Rates remain finite and decay after input removal.

The generic matrix has maximum absolute row sum at most 0.05 because contact weights
divide by total input and are multiplied by 0.05. Rectification/clipping is
non-expansive. At dt 10 ms / tau 50 ms, the update has a maximum difference contraction
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

| dt compared with5ms | Largest population-mean rate discrepancy | Discrepancy / reference peak mean |
| --- | --- | --- |
| 0.01 | 6.41983934e-06 | 4.8796851% |
| 0.02 | 1.9259518e-05 | 14.639055% |

These are saved population-mean traces aligned by physical step-end times using
linear interpolation. They are **not** per-neuron transient errors or a convergence
proof. The 10 ms / 20 ms discrepancies are approximately 4.88%/14.64% of the reference
peak mean. Real-time 20 ms operation therefore comes with a measured temporal
approximation difference, not interchangeable neural dynamics.

Full-context frozen-learning-kernel pilots, updating all neurons, measure:

| Kernel | Init s | 1 simulated second / wall s | Projected full acquisition s | Process peak MiB |
| --- | --- | --- | --- | --- |
| 1 | 2.711 | 2.156 | 474.25 | 1284.91 |
| 2 | 1.992 | 2.180 | 152.62 | 1626.09 |
| 3 | 2.165 | 2.224 | 533.80 | 1697.23 |

These pilots use the conservative extension, not the later class-consistent operator.
They ran sequentially in one process, so RSS values are cumulative high-water marks,
not fresh-process per-kernel peaks. Each full generic temporal benchmark used its own
fresh process. The class-consistent full-brain operator was not benchmarked.

All exceed the prospectively declared 120-second per-acquisition study budget. Thus
L4 full-duration conditioning trajectories were **not measured**; only the full
reference benchmark and one-second extension pilots were run. This is a study-scope
limit, not a claim that full-brain offline conditioning is computationally impossible.
The 120-second cutoff is an experiment budget, not a biological or hardware limit.
No L4 learning-effect trajectory should be inferred from these pilots. Those projected
times make offline work plausible, but the measured conservative extension kernels
are below real time at their fixed 10 ms step. The generic faster benchmark must not
be used to claim real-time performance for the learning extension.

## Architecture comparison

| Dimension | A: validated minimal circuits | B: larger integrated subnetwork | C: simplified full brain |
| --- | --- | --- | --- |
| Interpretability | Strongest for narrow Stage 1 claim | More recurrent context, more sign/receptor assumptions | Most activity uninterpreted |
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
from these behavioral claims. Retain C. elegans and Stage 1 as existing baselines;
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
- [Participation, effect differences, stability and storage](SYNTHESIS.json)
- [Temporal approximation comparison](TEMPORAL_COMPARISON.json)
- [Shared-cell and shared-synapse conflicts](UNIFIED_MODEL_CONFLICTS.md)
- [Trajectory CSV](TRAJECTORIES.csv)
- [Kernel equality checks](kernel-checks.json)
- [Full-protocol budget measurements](FULL_PROTOCOL_BUDGET.json)
- [Preservation record](PRESERVATION.json)
- [Reproduction instructions](README.md)

Licensing caveats remain inherited from the pinned sources; no commercial data
redistribution or deployment occurs. The complete study manifest hashes all artifacts.

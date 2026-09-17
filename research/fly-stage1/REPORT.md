# Drosophila Stage 1 — final scientific evidence

**Classification: PASS, for the narrow appetitive associative-learning objective.**  
**Aversive interpretation: PARTIAL / INCONCLUSIVE.**  
17 September 2026. No Stage 2, migration or Genesis integration was performed.

Real FlyWire anatomical connections determine the model's sensory propagation.
Paired experience changes persistent KC→MBON multipliers through the modeled local
dopamine rule. Subsequent cue-only neural responses change without an LLM, prose
memory, stored cue preference or learned readout. The effect reverses with the
pretraining snapshot and survives removal of transient activity. Mechanism-specific
interventions abolish learning without abolishing sensory responses.

This is evidence for **this connectome-constrained computational mechanism**, not
validation of a faithful fly, natural reward processing, behavioral preference,
long-term biological memory or a uniquely necessary FlyWire topology.

## 1. Preserved foundation and scope

- Original C. elegans implementation and connectome hashes are unchanged.
- A read-only comparison of every canonical `genesis_*` table matches the pre-task
  snapshot exactly: organism `817e772c-827e-48fc-8e35-6504cb2a8d2d`, seven cycles,
  seven decisions, autonomous schedule disabled. No canonical cycle was run.
- Canonical snapshot SHA-256:
  `3377c9dddbe2abf89ed9a820a6aabbc1da951cac7bfc1823471c5aac043ea312`.
- Existing tests: **30/30**, including real PostgreSQL tests in temporary schemas.
  Those tests create disposable test organisms, not canonical Genesis life cycles.
- Isolated harness tests: **10/10**. TypeScript and existing lint checks passed.
- After interruption, the local PostgreSQL service was found shut down. Restarting
  that database service restored verification access; the initial connection-refused
  test failures were environmental. No Genesis autonomous runtime was started.

All implementation is under `research/fly-stage1`. No core, planner, wallet, runtime,
persistence schema or existing scientific document was changed. The recorded
[analysis plan](PLAN.md) predates conditioning runs; no neural parameters or circuit
selection were changed to improve the observed conditioning result.

## 2. What is fact, model and product mapping?

**BIOLOGICAL FACT:** the retained chemical contacts come from adult female
FAFB/FlyWire v783. PAM-α1 stimulation paired with odor can suppress subsequent
MBON-α1 responses; γ1pedc dopamine-dependent KC→MBON depression has direct
experimental support. APL inhibition has local structure, which the present model
does not reproduce in full. Sources: [appetitive conditioning](https://elifesciences.org/articles/79042),
[aversive plasticity](https://pmc.ncbi.nlm.nih.gov/articles/PMC4674068/),
[APL physiology](https://elifesciences.org/articles/56954).

**COMPUTATIONAL MODEL:** bounded rates, class-level gains and signs, a point APL,
10 ms integration, 50 ms fast time constant, 500 ms eligibility, fixed normalization,
synthetic PN currents and imposed DAN currents. Local dopamine exposure requires an
observed DAN→KC contact; it gates depression only on existing KC→MBON contacts in
the matching modeled compartment. Compartment identity is inferred from cell types,
not resolved receptor locations in this coarse neuropil connection table.

The learning rule is bounded multiplicative LTD:
`multiplier *= exp(-eta × dt × eligibility × max(local_DA - threshold, 0))`.
Baseline anatomical weights are immutable. No cue name, reward label or expected
answer enters the model. The LTD rule is supplied by the modeler; it is not inferred
from static anatomy. Thus the experiment tests the proposed mechanism's causal
implementation and robustness, not discovery of a learning rule from connectivity.

**GENESIS MAPPING: none.** There are no digital actions, money, internet, language,
planner, life cycles or preference fields. The outcome is measured neural activity.

## 3. Exact circuit and plastic-state counts

| Quantity | Measured count |
|---|---:|
| Identified neurons | **1,054** |
| Unique directed anatomical neuron pairs | **80,423** |
| Retained anatomical contacts | **226,143** |
| Retained pair/neuropil rows | 102,889 |
| Plastic-capable KC→MBON directed pairs | **2,702** |
| Plastic-capable pair/neuropil state entries | **5,675** |
| Contacts on plastic-capable pairs | 13,866 |
| Plastic pairs with observed matching DAN→KC support | **1,685** |

Population: 911 KCs, 123 cholinergic ALPNs, two appetitive MBON07s, two MBON11s,
13 PAM11s, two PPL101s and one APL. Selection began with left-labelled MBON07s,
then followed actual connectivity. It is not a purely left-hemisphere network:
connected partners were not discarded because of their soma-side label.

| Compartment | Plastic directed pairs | Pair/neuropil states | Contacts | DAN-supported plastic pairs |
|---|---:|---:|---:|---:|
| Appetitive α1 | 1,808 | 4,622 | 11,369 | 1,279 |
| Aversive γ1pedc contribution | 894 | 1,053 | 2,497 | 406 |

Only 642 selected KCs have observed PAM11 contacts, and 395 have PPL101 contacts.
Pairs without the matching observed DAN contact cannot acquire plasticity in this
model. Across primary appetitive runs, 618–1,526 plastic **neuropil entries** changed
by more than 1e-12. These are not counts of new anatomical connections.

The fast-rate operator uses 100,470 retained rows (78,226 directed pairs). The
remaining 2,419 rows are not all fast synapses in the model: dopamine contacts can
provide modulation, and unresolved MBON07 glutamate effects outside PAM11 are
excluded rather than assigned an invented sign. The complete anatomical extract
still retains every selected internal contact.

The immutable [extraction manifest](artifacts/c5c332c1bd0ce77487ad5765756a58dc441d50f59dc56899a462bf35e4b2a157/manifest.json)
records IDs as strings, types, sources/checksums, selection, boundary cuts and hashes.
The annotation/inventory discrepancy is now explicitly enumerated: 14 proofread IDs
lack v3.1.0 annotations and seven annotated IDs are absent from that proofread
inventory. **None of the selected neurons is unmatched.** The cause of those
inventory differences is not inferred.

## 4. Protocol and primary quantitative results

Three fixed codebook seeds each define two disjoint six-PN current patterns. Each
pattern is paired in turn: **six primary appetitive conditions**. Baseline and recall
use identical current vectors and average normalized rates during seconds 1–2 of a
two-second probe, from independent copies of the relevant snapshot.

Training presents A for 60 seconds and B for 60 seconds, separated by 10 seconds.
The assigned cue is paired with thirty one-second DAN pulses at two-second spacing.
Every condition runs to 220 simulated seconds; there is a long silent tail after
the last cue. In the explicitly unpaired control, the same DAN pulses occur at
150–210 seconds, separate from either cue. All recalls omit imposed teaching input.

`Depression = 1 − post / baseline`. **Selectivity** is paired-cue depression minus
control-cue depression, in percentage points (pp). Rates are model units, not Hz.

| Seed | Paired cue | Paired baseline → post | Paired depression | Control-cue depression | Selectivity |
|---|---|---|---:|---:|---:|
| 1701 | A | 0.070780 → 0.031243 | 55.86% | 5.91% | **49.95 pp** |
| 1701 | B | 0.112911 → 0.059229 | 47.54% | 9.87% | **37.67 pp** |
| 1702 | A | 0.088169 → 0.039304 | 55.42% | 8.70% | **46.72 pp** |
| 1702 | B | 0.068049 → 0.037843 | 44.39% | 7.62% | **36.77 pp** |
| 1703 | A | 0.106835 → 0.055794 | 47.78% | 12.79% | **34.98 pp** |
| 1703 | B | 0.072441 → 0.032053 | 55.75% | 8.37% | **47.38 pp** |

Mean paired depression: **51.12%**; mean control depression: **8.88%**; mean
selectivity: **42.25 pp**. All six exceed the recorded thresholds of 10% paired
depression and 5 pp selectivity. Reversing the paired identity reverses which cue
shows the larger learned depression. Some generalization remains through overlapping
KC activation; selectivity does not mean zero change to the control cue.

These are deterministic model/codebook comparisons, not six flies or a population
estimate. No biological statistical significance is claimed. All 76 conditions,
including raw baseline/post values for both cues and every population, are in
[RESULTS.csv](RESULTS.csv) and the immutable raw result collection.

## 5. Interventions and connectivity dependence

The following are seed 1701, with both cue assignments. Normalization is frozen
before interventions; surviving weights are not automatically rescaled.

| Condition | A-paired selectivity | B-paired selectivity | Interpretation |
|---|---:|---:|---|
| Intact | 49.95 pp | 37.67 pp | Reference |
| Freeze KC→MBON plasticity | 0.00 pp | 0.00 pp | Learning lost; sensory responses preserved |
| Silence relevant PAM11 population | 0.00 pp | 0.00 pp | Learning lost; sensory responses preserved |
| Remove relevant DAN→KC contacts | 0.00 pp | 0.00 pp | Anatomical modulation route required |
| Same dopamine exposure, temporally unpaired | 0.00 pp | 0.00 pp | Exposure alone insufficient |
| Lesion one strongest-contact relevant DAN | 44.57 pp | 34.50 pp | Selectivity reduced **10.76% / 8.43%** |
| Lesion one unrelated DAN | 49.95 pp | 37.67 pp | Equal cell count, **0% reduction** |
| Remove APL | 47.74 pp | 35.89 pp | Learning survives this boundary intervention |
| Remove modeled fast recurrence | 45.80 pp | 33.95 pp | Local induction does not require full recurrent dynamics |
| Shuffle PN→KC strengths among existing pairs | 47.88 pp | 42.13 pp | Responses change, but association remains possible |

The first three learning-mechanism interventions reduce selectivity by **100%**,
exceeding the required 80% reduction. KC responses are unchanged numerically:
A = 0.077819 and B = 0.131070 before/after those interventions. Thus their effect is
not explained by a generally silenced network. In contrast, removing PN→KC edges
eliminates KC and downstream responses while preserving input activity; removing
KC→MBON edges eliminates the target MBON response while preserving KC activity.
Normalized learning scores are **undefined**, not zero, when baseline output is zero.

Shuffling preserves pair membership and per-target strength totals, but changes
which observed PN→KC contacts carry those strengths. Baseline appetitive MBON
responses change by −2.76% for A and +15.22% for B. This establishes sensitivity to
the extracted strengths, **not that this topology is uniquely necessary for learning**.
The shuffle is a labeled control, never a replacement anatomical artifact.

The equal-size lesion comparison concerns one cell in each arm. It is not presented
as a matched control for silencing all 13 PAM11s. The smaller selective lesion effect
is consistent with distributed modeled dopamine input, not complete localization
of memory in one DAN.

## 6. Where is the memory?

| Alternative explanation / check | Quantitative finding |
|---|---|
| Residual activity or eligibility | Clearing **all rates and eligibility** while retaining multipliers preserves primary depression to <1e-10 difference |
| Pretraining-state restoration | Baseline group responses restored **exactly**, in all 76 conditions |
| Sensory response alteration | Primary appetitive KC responses unchanged; depression appears downstream |
| LLM, prose or episode lookup | **24 fresh-interpreter recalls** receive only a neural snapshot, circuit and numeric PN currents; all reproduce saved group responses within 1e-10 |
| Population averaging artifact | Both individual MBON07s depress in every primary run; per-cell paired depression is **43.51–56.60%** |
| Determinism | **6 full-protocol replays** are exact, including both noisy-boundary replays; additional mid-protocol JSON/PRNG restoration test passes |

The snapshot contains rates, eligibility, plastic multipliers, logical tick, PRNG
state and model/circuit fingerprints. It has no cue identity, preference score or
language memory. Raw recall of individual neurons also rules out a learned decoder:
the readout is a fixed arithmetic mean, and the neurons themselves change.

This model does not include a separately validated sensory-adaptation mechanism.
The result distinguishes plasticity from **its modeled transient state**, not from
every adaptation mechanism a real fly might have. Replay equality is measured on
the pinned local CPU environment; cross-platform tolerance of 1e-10 is a declared
target, not a tested cross-platform guarantee.

## 7. Boundary measurements and sensitivity

Boundary denominator: all contacts involving selected neurons in the **proofread
v783 connection table**, not unproofread fragments, electrical junctions or volume
transmission. Retained contacts: 226,143. Omitted incoming contacts: **305,890**;
omitted outgoing contacts: **531,695**. Exact external partners, neuropils and
class/transmitter summaries are preserved in the extraction artifacts.

| Population | Retained input / all measured input | Input retained | Output retained |
|---|---:|---:|---:|
| KCs | 174,939 / 196,462 | **89.04%** | 63.69% |
| Appetitive MBON07 | 12,459 / 13,153 | **94.72%** | 34.60% |
| APL | 22,852 / 68,332 | **33.44%** | 34.12% |
| Aversive MBON11 | 3,608 / 20,553 | **17.55%** | 19.72% |
| PAM11 | 3,243 / 7,816 | 41.49% | 50.67% |
| PPL101 | 3,521 / 20,765 | 16.96% | 32.61% |
| Sensory PNs | 5,521 / 204,952 | 2.69% | 14.79% |

Very low PN input retention is intentional because PN currents are imposed at the
sensory boundary. DAN stimulation likewise bypasses natural teaching pathways.
The model therefore tests a stimulated circuit preparation, not natural odor or
reward detection.

Appetitive selectivity in the fixed sensitivity battery:

| Variation | A paired | B paired |
|---|---:|---:|
| Baseline | 49.95 pp | 37.67 pp |
| Time step 5 ms instead of 10 ms | 49.90 pp | 37.64 pp |
| Learning rate ×0.5 | 32.82 pp | 24.64 pp |
| Learning rate ×2 | 62.53 pp | 47.67 pp |
| Fast gains ×0.75 | 43.50 pp | 32.98 pp |
| Fast gains ×1.25 | 54.93 pp | 41.61 pp |
| Omitted-input current 0.02 × omitted fraction | 50.07 pp | 37.46 pp |
| Omitted-input current 0.05 × omitted fraction | 50.15 pp | 37.14 pp |
| APL gain ×0.5 | 50.16 pp | 37.52 pp |
| APL gain ×2 | 49.78 pp | 37.95 pp |
| Boundary 0.02 with seeded noise SD 0.01 | 49.86 pp | 37.52 pp |

All 20 sensitivity conditions exceed the primary thresholds. Halving the time step
changes selectivity by less than **0.05 pp**. Positive boundary currents were
predeclared perturbations, not fitted compensations; the primary result uses **zero**
such current. APL removal and gain variation show that the observed appetitive
effect does not require the particular truncated point-APL strength.

This is limited robustness, not reconstruction of the omitted network. Positive
tonic currents cannot represent all missing inhibition, temporally structured
feedback or peptides. Parameter variations are one at a time, not an exhaustive
joint uncertainty analysis. Preserved learning after recurrence removal further
limits the claim to local associative induction; it does not validate consolidation.

### Aversive counterpart: inconclusive biologically

Its six intact conditions show 16.32–32.59% paired depression and 13.18–29.09 pp
selectivity. Freezing plasticity, suppressing the relevant dopamine pathway or
unpairing teaching eliminates that model effect. Nevertheless, **82.45% of MBON11
inputs are omitted**, including the broader gamma-KC population. The selected
alpha/beta contribution is not a complete aversive circuit. No extra cells or
currents were added to repair this. These results are retained, but not accepted
as validation of natural aversive conditioning. The Stage-1 PASS rests on the
independently satisfactory appetitive assay.

## 8. Performance and evidence

- **76 conditions**, each 220 simulated training seconds: **16,720 seconds** total
  scheduled training time, excluding probes and extra replay copies.
- Entire recorded suite: **407.95 seconds** wall time, including evidence recording.
- Median per-condition measured wall time: **4.845 seconds**; range 3.94–10.75 seconds.
  These timings include probes and, where requested, an additional replay.
- Peak process RSS: **377,061,376 bytes = 359.6 MiB**.
- Environment: ARM64 macOS, eight reported logical CPUs, Python 3.12.14,
  NumPy 2.3.5, SciPy 1.16.2. This is not a measured Railway/cloud benchmark.
- Saved experiment evidence: **30.49 MB**. Genuine 10 Hz traces contain population
  rates and plastic summaries for every run; four primary runs additionally contain
  all neuron rates and plastic entries. The scientific readouts are unsmoothed.

Evidence roots:

- [Circuit manifest](artifacts/c5c332c1bd0ce77487ad5765756a58dc441d50f59dc56899a462bf35e4b2a157/manifest.json)
- [76-run result record](evidence/4afc692f113981d1ad1a035ba7293e00bb4c8964bc1e87d9b00fab8063037c4b/results.json)
- [Immutable evidence hashes](evidence/4afc692f113981d1ad1a035ba7293e00bb4c8964bc1e87d9b00fab8063037c4b/evidence-manifest.json)
- [Acceptance audit and fresh-process recall](evaluations/c5d2c183e6d09e0c022825ed62dbba7323962dbbccf24b48d8f2720de0bd4c11/evaluation.json)
- [Complete tabular results](RESULTS.csv)

## 9. Limitations and stop decision

The largest unresolved scientific limits are coarse compartment localization,
unmeasured conductances/receptors, point-APL dynamics, omitted state/modulatory
inputs, synthetic cue coding and a deliberately restricted LTD rule without
biologically validated forgetting or consolidation. Persistence demonstrated here
is persistence in stored neural parameters across recall and process restart,
not experimentally calibrated days-long memory. Surviving weight shuffling means
we cannot claim unique necessity of the exact fly wiring for associative learning.

There is also a provenance restriction: the [Zenodo record](https://zenodo.org/records/10676866)
labels connectivity CC BY 4.0, while [FlyWire guidelines](https://home.flywire.ai/guidelines)
state CC BY-NC 4.0 for public data. The standalone current annotation license was
not resolved. These local artifacts remain research material; commercial data
redistribution/integration requires clarification. No deployment or publication
was performed.

**Stage 1 stops here.** Its acceptance is the narrow, quantitative demonstration
of appetitive association in a real-connectome-constrained neural model, selectively
dependent on persistent KC→MBON plasticity and the modeled dopamine pathway.
It does not authorize Stage 2 or any change to Genesis's biological brain.

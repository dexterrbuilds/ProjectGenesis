# Boundary-Closure and Brain Architecture Study — prospective plan

Not Stage 4. All prior models, thresholds, reports, artifacts and canonical state
are frozen. New code and results only here. Selection is completed from anatomy
before any expanded activity is inspected. An effect shrinking is informative.

## Closure from each independent seed

Pinned adult female FAFB v783 proofread connectivity and annotation v3.1.0; verify
original source checksums. Roots remain strings in public artifacts. All induced
chemical contacts are retained, including single-contact connections.

L0: exact frozen extraction, original edge order, groups and parameters.
L1: original seed plus major omitted afferents/efferents of the original non-PN/KC
populations, selected separately for each population/direction to reach 80% of its
full proofread mass (descending contact totals, root-ID tie break). Also include
all observed direct modulatory partners (DAN, OA, serotonin, DPM, APL) regardless
of mass, and any neuron with reciprocal chemical contacts to those populations.
These are anatomical screening rules, not validated functional identifications.
L2: L1 plus neurons with at least half their incident synaptic mass in MB/CA/LH/AL
neuropils AND actual connectivity to L1; include named MBON/DAN/KC/ALPN/ALLN/LHLN,
APL/DPM/LHCENT1 populations with an observed connection to L1. Neuropil and cell
class are biological constraints; a graph hop alone is not sufficient.
L3: L2 plus all annotated central/ascending/descending/endocrine neurons, a broad
central-brain reference. No behavioral interpretation for generic context neurons.
L4: every root in the pinned proofread inventory, including optic lobes. This is
an anatomical reference, not a reconstruction of body/endocrine physiology.
Record exact additions/reasons, per-seed original-population and whole-context
input/output retention, induced edge/contact counts, and omitted partners.

## Physiology and isolated comparisons

Reuse original model equations and parameters through read-only imports. No changes
to frozen code. Original functional root sets and sensory input patterns remain
fixed across levels. Added neurons are generic context, not automatically new
learning populations. Original plastic edges/compartment assignments remain fixed.
Core-to-core efficacies and dopamine operators remain frozen. Added chemical rows:
contact/full-proofread-input * original recurrent_gain (.05), source sign from
known NT where unambiguous, otherwise predicted NT; ACh positive, GABA negative,
glutamate/monoamine/unknown zero in conservative primary. DPM co-transmission is
unresolved and zero, not guessed. This is a declared model-extension assumption.
KC context uses known cholinergic identity and original KC threshold. No boundary
currents, stochastic tonic drive, synthetic peptide edges or desired output inputs.

Main anatomy-only contrast keeps original intact L0 weights fixed at every level;
added rows use the same full-input denominator regardless of extraction size.
Thus adding context does not silently rescale the accepted Stage-1 role-normalized
core. Separately test (i) full-input normalization of core and context, (ii) original
role normalization where defined, and (iii) .5x/2x added recurrent gains. These
are distinct assumptions, never a replacement for primary. A predicted-glutamate-
inhibitory variant is a sign hypothesis, not receptor evidence. Context-cut control
zeros all added edges with intact denominators, preserving added silent nodes.

## Protocols and bounded matrix

Replay exact frozen primary seed1701/2701/3701 A/B sensory patterns and stimulus
timing, including full220/70/240-second acquisitions. No resampling PN identity as
network size grows. Stage3 both resource states .2/.8. Primary L0–L3 all cues/states.
Per stage/level cue A: relevant dopamine silence, plasticity freeze and matched
control; Stage3 controls both states. At L2: normalization alternatives, added-gain
half/double, glutamate sign alternative and context-cut, cue A (both Stage3 states).
No imported Stage3 score or software coupling. Report response vectors and anatomy.
L4 benchmark first; if measured predicted acquisition cost is <=120s per primary
run and peak memory <=4GiB, also run primary A/B for all stages at L4. Otherwise
report the measured budget and keep L4 an offline benchmark rather than pretend
protocols were replayed. No silent shortening or skipped neural updates.

Stage1 selective depression; Stage2 repeated-minus-control depression; Stage3
raw MBON11 low/high contrast, trial10/1 and LH/MBON18 responses. Keep prior acceptance
thresholds solely as reference, no new behavioral PASS. All effects are new-context
findings, never revised prior classifications. Compare original-baseline and
expanded-context baselines, sensory changes, saturation and post-cue residuals.
Interventions must distinguish mechanism loss from loss of sensory input.

## Full reference benchmark

Store contacts as sparse weighted directed neuron pairs (sum neuropil rows only for
linear fast propagation), retaining original indexed neuropil rows for provenance.
Float64 conservative generic rate model tau50ms, no plasticity outside supported
core. Benchmark dt5/10/20ms, all neurons updated every step for10 simulated seconds
with seeded sensory input then silence. No stride omission. Measure initialization,
process CPU/wall time, peak RSS, sparse bytes, throughput, simulated/wall ratio,
checkpoint/reload time/bytes, exact replay and timestep response differences.
Run each benchmark in a fresh process; peak includes loading/initialization.
This tests engineering feasibility, not physiological validity or semantic states.

## Integrated anatomy and recommendation

Analyze actual inter-population paths, reciprocal connectivity and shared partners
in union/L2/L3/full anatomy. Distinguish anatomical paths from demonstrated useful
physiological coupling. Stage3's ~1e-6% learned-value interaction is a constraint.
Do not average three scores or graft different plasticity rules onto one synapse.
If contextual sign/receptor assumptions dominate, causation between boundary loss
and physiological approximation remains unidentified. Recommend MINIMAL,
INTEGRATED SUBNETWORK, FULL BRAIN or INSUFFICIENT EVIDENCE from evidence; full-brain
speed alone cannot justify a behavioral substrate. No canonical integration.

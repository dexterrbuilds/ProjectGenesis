# Stage 1 analysis plan — recorded before conditioning runs

This is an isolated numerical research experiment, not a Genesis brain adapter.
No imports from Genesis core/runtime, no LLM, no database, no wallet, no web actions.
The network receives only numeric currents at identified neurons. Cue names and
experimental condition labels never enter the model or its saved state.

## Anatomical selection, before observing learning outcomes

Start with the left-labelled MBON07 (alpha1) population and PAM11 (PAM-alpha1),
which have direct experimental evidence for appetitive odor-associated output
depression. Include all alpha/beta Kenyon cells with observed input to that output,
and their actual cholinergic AL projection-neuron inputs. Do not select cells by
whether they produce a successful learning result. Retain actual internal edges,
including reciprocal PAM11/MBON07 connections. Select the APL cell(s) anatomically
coupled to these KCs to test feedback inhibition; do not add DPM by default because
this experiment concerns induction/recall, not sleep or long-term consolidation.

Include the corresponding MBON11/PPL101 compartment as an aversive counterpart
and an unrelated-output control, restricted to the same KCs. Its omitted gamma-KC
inputs must be measured; results cannot claim complete natural aversive behavior.
Selection follows connectivity where soma-side labels are insufficient. Every
included edge must exist in v783. No minimum-synapse pruning beyond the source's
own quality filtering. Compute per-neuron, per-class and transmitter boundary loss.

Sources: [appetitive alpha1 output depression](https://elifesciences.org/articles/79042),
[PAM-alpha1 recurrence](https://elifesciences.org/articles/10719),
[aversive gamma1pedc plasticity](https://pmc.ncbi.nlm.nih.gov/articles/PMC4674068/),
[local APL inhibition](https://elifesciences.org/articles/56954).

## Model assumptions (not extracted physiological measurements)

Bounded leaky rates, 10 ms step, 50 ms fast time constant, sparse fixed baseline
weights proportional to anatomical contacts with normalization frozen before any
intervention. Explicit receptor/sign assumptions; dopamine gates plasticity rather
than acting as a generic fast excitatory transmitter. Presynaptic eligibility and
local anatomically supported dopamine exposure depress existing KC→MBON weights.
Persistent multipliers and dynamic state are the only learned memory. No cue score,
reward-to-preference rule, decoder fitting or tuning against Genesis behavior.

The minimal model deliberately omits full molecular consolidation and receptor
kinetics. APL is initially a point-neuron approximation; compare removal/strength
variation and report its missing inputs. No claim of reproducing all fly physiology.

## Experiment and acceptance

Generate equal-sized distinct PN current patterns from fixed seeds, without
inspecting learning outcomes. Counterbalance which cue is paired. Establish
baseline responses on independent copies of an identical initial snapshot.
Train with 60 seconds of the paired cue and 1-second dopamine pulses alternating
with 1-second gaps, plus equal unpaired-cue exposure. Wash out for 10 seconds.
Probe with cue alone, with plasticity left enabled. Record raw MBON/KC/DAN rates,
plastic multipliers and timestamped numeric inputs. Compare paired and control
responses relative to their own baselines. No behavior/preference label is needed.

Primary effect: selective depression of the trained compartment's paired-cue
evoked response. Require at least 10% paired depression, and a paired-minus-control
depression contrast of at least 5 percentage points in both counterbalances across
three prespecified cue seeds. Basic evoked KC responses must remain nonzero.
These are engineering acceptance thresholds, not biological effect-size estimates.

Mechanistic controls: freeze plasticity; silence relevant DANs; remove local
DAN→KC contacts; remove PN→KC or KC→MBON pathways; matched-count unrelated DAN
lesions; remove APL; unpaired dopamine exposure; intact controls. Do not renormalize
after lesions. Require learning-specific controls to reduce the primary contrast
by at least 80%, with KC responsiveness within 10% of intact where applicable.
Connectivity lesions may destroy sensory responses and do not alone prove learning.
Shuffle controls, if used, are explicitly synthetic negative-control graphs and
cannot be mistaken for anatomical artifacts.

Replay identical saved inputs/state; require exact equality on the pinned CPU
environment and declare 1e-10 absolute tolerance for compatible floating-point
implementations. Restore pretraining state: cue response returns to baseline.
Also reset fast dynamics while preserving plastic state: learning should remain.

Sensitivity checks: timestep halving, learning-rate factors 0.5/2, fast-gain factors
0.75/1.25, missing-input boundary currents 0/0.02/0.05 scaled by omitted fraction,
and APL strength 0/0.5/2. Report failures; do not retune or expand just to pass.
State the narrow conclusion supported, including whether topology-specific claims
survive shuffling. A positive result demonstrates a connectome-constrained model's
plasticity, not that only this biological graph could implement association.

## Provenance and licensing

Use the original FAFB v783 Zenodo connection table and v3.1.0 annotation table.
Verify source checksums. Derived artifacts are content addressed and never
overwritten; a manifest records exact selection, boundary cuts and file hashes.
Zenodo labels connectivity CC BY 4.0, while FlyWire site guidelines state CC BY-NC
4.0 for public data. Record this inconsistency and treat derived research data
conservatively as research-only pending clarification before commercial distribution.
No automatic push, deployment or incorporation into Genesis is authorized here.

## Stop rule

Conclude PASS (narrow modeled mechanism), FAIL, or INCONCLUSIVE from recorded
evidence. Do not proceed to novelty, motivation, sleep, adapter changes or integration.

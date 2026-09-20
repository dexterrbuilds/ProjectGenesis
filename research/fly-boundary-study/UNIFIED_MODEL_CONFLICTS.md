# Shared-state conflicts to resolve before any unified model

This is an audit of frozen code and anatomy, not a proposal to combine update rules.
All original implementations and classifications remain unchanged.

## Exact overlap

- Stage-1 DAN_av and Stage-3 DAN are the same two PPL101 roots.
- Stage-1 MBON_av and Stage-3 MB11 are the same two MBON11 roots.
- Stage-1 MBON_app is a two-root subset of Stage-3's four-root MBON07 VALUE set.
- 4,622 KC→MBON07 pair/neuropil rows overlap Stage-1 learning and Stage-3 value context.
- 1,053 KC→MBON11 pair/neuropil rows overlap Stage-1 aversive and Stage-3 experience
  plasticity. See MECHANISM_OVERLAP.json for the exact counting method and source sets.

The Stage-1 aversive counterpart was not the accepted appetitive PASS. Shared
anatomy does not promote that counterpart into a validated unified mechanism.

| Issue | Frozen Stage 1 | Frozen Stage 3 | Required reconciliation, not implemented |
| --- | --- | --- | --- |
| Shared PPL101 activity | Generic rate dynamics; explicit teacher in aversive assay | Resource gates PPL101 desired rate | One rate state and a justified common afferent/body model |
| Dopamine locality | Actual DAN→KC contacts gate KC presynaptic eligibility | Actual DAN→MBON11 contacts gate MBON-target efficacy | Determine receptor/localization evidence; anatomical contacts alone cannot choose |
| Induction | LTD proportional to eligibility × max(DA−0.2,0) | LTD proportional to eligibility × DA, with no 0.2 threshold | One justified rule per shared synapse; do not sum updates |
| Acute modulation | No separate acute KC→MBON11 divisor | KC→MBON11 transmission divided by 1+DA | Test acute versus persistent mechanisms independently |
| MBON11 inhibitory gain | Most outgoing targets use recurrent_gain0.05 | MBON11 source rows use gain1 | Same GABA label does not justify twentyfold efficacy mismatch |
| Normalization | Incoming contacts normalized per source role | Incoming contacts normalized by all proofread inputs | A common scaling model or independently measured conductances |
| MBON07 output | Excitatory only to selected PAM-alpha1 group, gain0.1; other targets zero | VALUE outputs zero | Preserve target-specific evidence; do not generalize glutamate sign |
| KC→MBON07 learning | Active appetitive learning, local teacher and eligibility | Value multipliers frozen/imported in transfer assay | Decide supported plastic compartment rules before new training |
| Shared numerical state | Own rates, eligibility, clock and per-row efficacy | Own rates, eligibility, clock, efficacy and body | One root/connection state, not independent copies plus combined scores |

Stage 2 introduces another dopamine-localized, effective postsynaptic receptor rule,
including spontaneous recovery with a 1,800-second modeled time constant. It has
its own compartment and no direct shared plastic rows in this audit. That does not
justify applying its recovery or receptor rule to Stage-1/3 synapses. Its point-APL
state is also shared anatomy across preparations and would require one reconciled
APL representation, ideally informed by spatial compartmentalization evidence.

## What anatomy does and does not establish

MBON11 has observed connections to PAM and α′3 populations; α′3 outputs connect to
MBON18 and LH candidates. These support candidate interaction paths, not their
functional magnitude or sign. Short paths often contain unresolved modulatory links.
The full graph can store all systems simultaneously, but there is no validated
unified physiological operator in this study. The Stage-3 learned-value interaction
near 10^-6% remains weak evidence, not a success upgraded by anatomical overlap.

No duplicated neuron, combined score, merged plasticity rule or new biological
capability has been implemented. Reconciliation requires separate scientific review.

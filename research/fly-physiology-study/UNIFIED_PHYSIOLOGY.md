# Feasibility of one physiological state per shared synapse

**Not currently supported by this evidence.** The same EM connection cannot simultaneously have two contradictory normalization conventions, two independent efficacies and two incompatible update laws. This study does not combine them.

The frozen architecture audit found **4,622 KC→MBON07** and **1,053 KC→MBON11** shared pair/neuropil rows. These counts describe the frozen extraction's row representation, not separate independently measured physiological synapses. Anatomical contacts may share a release site or receptor compartment, and neuropil-row efficacy is a modeling resolution.

| Conflict | What independent evidence now constrains | What is required before one defensible update rule |
|---|---|---|
| Stage-1 retained-role vs Stage-3 all-input normalization | Neither has a measured physiological denominator | Simultaneous identified presynaptic/target recordings across calibrated stimulus intensities, contact-specific strengths or a tested contact→conductance relationship; compare explicit observation models |
| KC→MBON07 active learning in Stage 1 vs frozen transferred value in Stage 3 | α1 memory/consolidation evidence supports the circuit's involvement, not the frozen LTD magnitude or rate | α1-specific KC/DAN activation and MBON current recordings with timing/dose sweeps, measured acquisition and recovery, receptor perturbations; held-out odors/preparations |
| MBON07 feedback positive gain0.1 vs absent fast output | NMDA requirement supports a candidate receptor pathway; net positive connection remains a hypothesis | Direct target-specific MBON07→PAM11 physiology with NMDA/GluCl manipulation, dose-response and timing. Do not globally assign glutamate sign |
| PPL101 rate/teaching vs resource-gated PPL101 | Conditioning and state-expression mechanisms are both supported at type level | Measure spontaneous/evoked release and postsynaptic response under fed/deprived states, independently of shock/odor effects; include compensatory endocrine and NO components if evidence requires |
| DAN→KC gate vs DAN→MBON gate | Compartmental action does not establish either contact-normalized exposure operator | Receptor localization, release/diffusion dynamics and dose-sensitive measurements at the relevant KC/MBON compartment; chemical contacts alone are insufficient |
| KC→MBON11 DA cutoff0.2 vs no cutoff; acute divisor plus LTD | Strong independent γ1pedc conditioning endpoint; acute retrieval gating is a distinct question | Factorial acute modulation and persistent plasticity experiments, temporal reversal, dose curves, receptor-specific interventions; fit one rule and then test all conditions without refitting |
| MBON11 output gain0.05 vs1 | GABA identity does not fix relative efficacy of each target | Paired target-specific transmission and receptor evidence; avoid using locomotion as a direct current proxy |
| α′3 efficacy/recovery vs γ1/α1 mechanisms | α′3 postsynaptic receptor and repetition evidence is relevant to α′3 only | Subtype-resolved, calibrated neural recordings over recovery and intervening experience. One shared mathematical template may eventually have compartment-specific measured parameters; its adequacy must be tested |
| Shared point APL state | Independent fit favors spatially distinct responses under local stimulation | Morphology/contact-localization mapping plus APL voltage/calcium and KC inhibition across locations. Fit a compartment model using independent data, not Stage-2/3 signal improvement |

A future identification protocol should separate: (1) passive membrane/observation calibration, (2) transmission and receptor effects, (3) acute modulation, (4) persistent plasticity and recovery, (5) held-out combined state/history conditions. This is a list of required evidence, **not an implemented integrated brain**. Do not add the Stage scores or sum the update rules.

## Full-brain implications

No neural equations changed in this study, so no new full-brain benchmark was run. The previous generic sparse-rate benchmark remains frozen and applies only to that operator. The added APL fluorescence fit is not a full-brain physiological update.

A future compartmental APL representation, conductance dynamics, receptor/second-messenger states, delays and per-synapse plasticity could change memory, numerical stiffness and update cost. The existing approximately 0.7 GiB generic benchmark cannot establish their performance. A new benchmark would need the actual equations, state layout, time-step convergence and checkpoints. There is no justified numerical resource forecast for a still-unidentified kernel.

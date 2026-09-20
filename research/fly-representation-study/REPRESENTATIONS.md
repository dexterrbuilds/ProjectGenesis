# Representation specification (before scaling measurements)

These are representation families, not four validated physiological kernels. An observation model is part of every comparison: calcium is not voltage, spike rate or conductance. The frozen APL fits are conditional predictions of off-site fluorescence using measured on-site fluorescence. They do not simulate a stimulated fly.

## R0: scalar activity

One state x_i per neuron; tau_i dx_i/dt = -x_i + f_i(sum_j W_ji x_j + I_i). A single APL state with fixed site gains implies reciprocal calyx/lobe transfer ratios g and 1/g. Both sites cannot independently have near-zero off-site responses in that linear observation model. A scalar neuron may still have synapse-local plastic states; scalar electrical state does not logically require global dopamine or shared efficacy. This distinction prevents rejecting all point-neuron models from an APL fluorescence assay.

## R1: local activity, one identity

One neuron owns x_(i,c) for justified regions c. Candidate linear local dynamics:

    tau_c dx_c/dt = -x_c + I_c + sum_d k_cd (x_d - x_c)

This is a model family, not fitted voltage dynamics. The APL two-site *steady response* specialization with symmetric nonnegative k gives off/on q = k/(1+k). Only under equal observation gains, equal leak, steady stimulation and direct forcing does that relation hold. The actual five-second calcium assay does not identify tau, k in physical units, fluorescence kinetics or direction-specific conductance. The zero-q approximation means unresolved transfer at this assay resolution, not anatomical disconnection. Separate local calcium states can coexist with relatively compact membrane potential. No new anatomical synapse is implied by intracellular coupling.

Anatomical calyx/lobe and alpha/alpha-prime partitions have independent experimental motivation. The shared q fits all training recordings, not one coefficient per recording. Applying it between different regions in Figure 3 is a deliberately limited generalization challenge. Spatial resolution beyond those measured regions is unidentified.

## R2: local transmission/modulation

Separate neuron activity, release and receptor response:

    DAN x_(i,c) -> release operator L_c -> local modulation m_c
    synapse s=(pre,post,location) -> eligibility e_s
    dw_s/dt = F_s(e_s, m_c, receptor state, w_s)

These arrows are not necessarily chemical synapses. Volume transmission must have its own provenance, not fabricated connectomic edges. Dopamine compartment specificity supports location-restricted modulation and persistent local efficacy; it does not identify L_c, diffusion, m_c units or receptor abundance. Receptor effects are target/compartment-specific evidence records, with unknown as an allowed value. KC cholinergic transmission is supported; global glutamate sign is not. DopR-dependent bidirectional plasticity constrains mechanisms in the assayed gamma compartments, not an arbitrary rule for alpha1 or gamma1pedc.

R2 may use one voltage state for a compact neuron and multiple modulatory/biochemical states along its axon. It is not required to split every neuron electrically. No numerical R2 neural kernel is fitted here.

## R3: selectively biophysical

For a measured cell type, C_c dV_c/dt = -g_L,c(V_c-E_L) - sum_r g_r,c(t)(V_c-E_r) + axial terms + I_c; gating obeys voltage-dependent measured kinetics. Each added channel, membrane section, receptor and observation parameter requires evidence. MBON14 passive morphology and alpha-beta-core KC potassium recordings constrain parts of this family in different preparations. They do not identify all equations or all fly neurons. A detailed published simulation is not an independent biological validation target. No whole-brain R3 physiology is instantiated.

## Heterogeneous candidate, not a selected kernel

Choose local states where measurements require them (APL calcium; compartmental biochemical/plasticity state), and retain simpler electrical states where sufficient for the question. MBON14 integrated output may admit a compact approximation, but its fast somatic response and slower neurite response should not be collapsed when predicting full voltage waveforms. A sparse KC code alone does not distinguish scalar thresholds from compartmental integration. The study must not assert that all neurons are point-like or all compartmental.

## Engineering scaling protocol

Use frozen anatomy for Stage 1/2/3, union L3 and all 139,255 roots. No extraction change. Preserve every pair/neuropil row and contact count. Benchmarks use float64 numerical state and uint/int32 endpoints; roots remain strings in identity metadata.

- E0/R0 envelope: one local state per root; sparse transmission traverses every retained anatomical row (CSR may coalesce identical state endpoints).
- E1/R1 envelope: one state per occupied root/neuropil, plus one for isolated roots. This is a computational envelope, **not** a physiological partition: MB_VL does not distinguish alpha1/alpha2/alpha3, and occupied neuropils are not automatically electrically isolated compartments. No inter-region coupling is invented for the benchmark.
- E2/R2 envelope: same local partition plus two receptor-response buffers, one modulation buffer and two per-candidate-plastic-row buffers (eligibility and efficacy). Candidate plastic rows are anatomical KC→MBON rows only; this is a storage/update envelope, not evidence that each is plastic. Fixed stable algebraic recurrences exercise all buffers without claiming receptor maps or biological learning. No target signs or biological labels are inferred from benchmark output.

Each timed update does one real-anatomy sparse multiply plus all applicable state/plastic-buffer operations. Use a deterministic engineering test vector, not fake biological traces. Weights are contact counts divided by maximum absolute input mass for numerical stability, fixed before benchmarks; this is not a fitted physiological normalization. Report 100 updates repeated twice, CPU/wall, init, peak RSS, array footprint, checkpoint write/load and exact replay. No cycles skipped. Map measured updates/s to hypothetical dt=10 ms,1 ms,0.1 ms; these are workload estimates, not temporal accuracy claims. R3: provide explicit state/storage formula and required dt sensitivity, no unsupported throughput extrapolation.

No Stage outcomes, canonical state, LLM or product mapping enter these experiments.

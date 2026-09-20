# What can be identified?

## APL spatial response is not a coupling measurement

The shared-state fixed-gain model requires q_CL*q_LC=1. Small measured off-site responses in both directions violate that constraint. Local response variables remove it without fitting each recording independently. This identifies a structural limitation of that observation model.

It does **not** identify positive inter-compartment coupling. Training AICc favors zero leakage (−60.0224) over one shared coefficient (−59.5595) and two directions (−56.7776). Recording leave-one-out error similarly favors zero (0.005506) over one coefficient (0.007029). The one-coefficient bootstrap includes zero. The directional model's improvement over zero in reused validation is only 9.51%, below the original20% material-improvement convention. The older two-coefficient result remains frozen and valid within its declared scope; this is a new complexity comparison, not a reclassification of old research.

Zero leakage is a useful low-resolution approximation, not a claim that APL branches are disconnected. Figure7 shows substantial horizontal-to-vertical APL responses under another protocol. Site gains, indicator kinetics, stimulation spread, intracellular cable properties, and regional input activity can contribute to the effective coefficient. A two-site five-second summary does not distinguish these causes. Unknown fly clustering and noisy on-site predictors further limit uncertainty estimates.

The R1 equations have at least tau, leak/coupling and observation-gain degrees of freedom. Only an effective conditional response ratio is fitted. For steady linear equal-leak compartments, q=k/(1+k); many absolute time scales produce that same ratio. The actual pulsed calcium assay does not establish those steady-state assumptions. Do not assign the algebraic inverse q/(1−q) as a measured physiological constant.

## Temporal discrimination

One tau=C/g identifies a ratio. Scaling both C and g preserves tau. In a two-compartment system driven in its common mode, arbitrary symmetric coupling is invisible in the aggregate output; the numerical example in TEMPORAL_CONDITIONING.json agrees to≤1.7e−16. This is a mathematical counterexample, not a biological prediction or fit.

The MBON14 paper contains observed fast/slow voltage components under somatic stimulation. Its simplified two-RC circuit illustrates a hypothesis; its chosen1.5ms/15ms constants are not separately fitted biological measurements. A single exponential cannot reproduce two independent exponential components when both are resolved, but a single dominant-time-scale approximation might suffice for integrated output. Raw held-out traces with recording bandwidth/access-resistance metadata are needed to quantify that trade-off. No temporal R0/R1/R3 ranking is claimed from the inconsistent summary workbook.

Alpha-beta-core KC voltage-clamp data identify A-current components at specific voltages. They do not justify setting all KCs to the same gate functions. The published means alone cannot determine a complete conductance model or distinguish a fitted effective scalar history variable from multiple channels on unseen stimuli.

## Conditioning and receptor dependence

The gamma1pedc remaining-current endpoint of0.1 constrains effective hazard H=−log(0.1)=2.302585 under an exponential efficacy surrogate. It does not separate eta from integrated local dopamine/eligibility exposure. The previous uncertainty analysis is unchanged. A family of101 illustrative eta/exposure pairs reproduces the endpoint to3e−17; the sampled eta range is **not** a biological confidence interval.

Monotonic LTD-only dynamics dw/dt=−eta*e*d*w with eta,e,d,w≥0 imply dw/dt≤0, regardless of spatial representation. Such a law cannot explain potentiation in the gamma4 backward-pairing assay. Adding compartments alone does not repair that failure. Receptor-specific bidirectional pathways have experimental support there, but their numeric kinetics and transfer to gamma1pedc/alpha1 remain unmeasured here.

An identical global modulator acting identically at every synapse cannot explain independent compartmental effects. This does not prove that there must be multiple electrical DAN state variables: target-local release/receptor/eligibility differences can generate selectivity. Evidence supports preserving those distinctions, not selecting a unique diffusion equation or contact-normalized exposure operator.

Recovery “by one hour” is not tau=one hour. Under an illustrative exponential, defining recovery as1%,5%,10% remaining yields tau782,1202,1563s respectively. These are a threshold-sensitivity demonstration, not fits or measured bounds. Intervening experience and postsynaptic receptor trafficking can break the exponential assumption entirely.

## Comparison and complexity

| Family | Independently supported elements | Unidentified / cannot discriminate | Present status |
|---|---|---|---|
| R0 | Thresholded integration can explain sparse outputs; compact-output approximation is plausible for some cells/questions | Universal gain/tau/normalization; scalar voltage vs calcium observation | Rejected for the tested single shared APL linear response; not rejected for every neuron |
| R1 | Local APL response; compartment-specific biochemical/plasticity state | Coupling magnitude, voltage partition, temporal parameters, functional-compartment contact mapping | Narrow spatial support, no transferable all-circuit kernel |
| R2 | Cholinergic KC transmission; target-specific sign; gamma receptor-dependent bidirectionality | Root-specific receptor map, release/dose, shared KC→MBON07/11 update law | Mechanistic constraints, no extra numerical held-out fit |
| R3 | MBON14 passive properties and KC-subtype channel measurements | Complete conductances, kinetic functions, independent temporal validation | No justified superiority or full-brain instantiation |

Parameter penalties are applied only to fitted comparable observation models. Assigning AIC to unfitted R2/R3 or pooling incompatible calcium/voltage/current residuals would be meaningless. R2 and R3 are not recorded as failing a quantitative prediction they were not identified enough to make.

## Gate for Stage probes

No representation plus neural parameters and observation mappings reaches the PLAN.md transfer standard. Therefore no new Stage1/2/3 probes are run. The frozen physiology study's unchanged-model replays remain preservation evidence only. No pseudo-calibrated replay or outcome-driven retuning is performed.

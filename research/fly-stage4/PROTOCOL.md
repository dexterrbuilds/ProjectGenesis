# Stage 4: prospective physical visual-stimulus experiment

This protocol precedes circuit extraction and all neural results. Scope: a conditional, uncalibrated LPLC2 motion-input model, not an implementation of threat behavior. No fitting, learning, semantic decoder or product mapping. Brain Spec 0.1.0 remains frozen; this package is unadmitted research.

## Independent evidence and limits

Klapoetke et al. 2017 (doi:10.1038/nature24626), especially Figs 1–5 and Methods, supports T4/T5 excitation of LPLC2, four directionally organized arbor layers, strong dark expansion responses relative to receding, luminance-matched darkening and wide-field motion, and LPi4-3 inhibition of responses to weaker unidirectional bars. LPi4-3 activation did **not** significantly suppress strong looming (P=0.209); that is not a predicted necessary intervention here. Calcium measurements in young adult females do not identify point-neuron gains, membrane constants, calcium transfer functions or root-specific receptor maps. Trial-level imaging data are available on request, not present in this audit. We will not manufacture numerical amplitude/latency acceptance intervals from plotted illustrations.

Matsliah et al. 2024 (doi:10.1038/s41586-024-07981-1) maps LPi11 to LPi4-3 and LPi09 to LPi3-4. FlyWire v783 column assignments map real T4/T5 roots to anatomical hexels. These are not calibrated retinal angles. Eye-geometry measurements (doi:10.1038/s41586-025-09276-5) warn against a universal Cartesian retinal map. Uniform local hexel spacing, screen orientation, preferred-direction axes and point integration therefore remain explicit approximations with sensitivity arms.

Ache et al. 2019 (doi:10.1016/j.cub.2019.01.079) supports LC4/LPLC2 contributions to GF velocity/size coding. DNp01 is the Giant Fiber class, but FAFB excludes the VNC. Whole-cell passive fits in the DN morphology study (PMC11071487; a preprint version, not a new validation dataset) use other preparations and v630 meshes/FANC extensions. No constants will be transferred to LPLC2 or used to bypass Gate A.

## Outcome-blind selection and anatomical closure

Select three central right LPLC2 roots by distance between their contact-weighted mapped T4/T5 input centroid and the median right-eye T4/T5 hexel position. Break ties by string root ID. This is an anatomical pilot and two spatial replicates, not population sampling or independent flies. Preserve each readout; never pool them into an action score.

L0: these LPLC2 roots, their mapped right T4/T5 afferents, their right LPi11 afferents, and mapped T4/T5 inputs to those LPi11. Retain **every** real chemical row among selected roots in the manifest, including rows not assigned an effective operator. No contact threshold. Unmapped sensory afferents are omitted explicitly, not given fabricated coordinates.

L1: add right LPi09 afferents and their mapped T4/T5 inputs, motivated by opposing-layer recurrence. Its extension to inhibitory LPLC2 transmission is a hypothesis, not the directly demonstrated LPi4-3 result. Other pair signs remain unknown and are excluded from the numerical operator, not declared physiologically zero. Major omitted Tm5, PVLP and LPLC2 recurrence are measured. No further expansion/tonic rescue is allowed based on results. Analyze LPLC2→DNp01 and LC4→DNp01 anatomy without simulating descending activity until Gate A passes.

Canonical rows use the existing dataset/source/pre/post/neuropil hash identity. Existing identities are referenced, never independently re-owned. This package adds unadmitted views and no persistent synaptic state.

## Representation and parameters (not fitted)

Physical grayscale movies feed local directional motion detectors at mapped T4/T5 locations. ON and OFF contrast channels use rectified contrast relative to 0.5. A two-point delayed correlation, with one-column separation along each preferred direction, is rectified. This approximates directional sensory responses; it is not a connectomic reconstruction of photoreceptors through T4/T5. The encoder never calculates a global expansion/looming score. Uniform darkening can cancel by construction: its rejection alone is not evidence of a biological computation. Translation/grating and temporal controls are essential.

Each selected root owns one scalar rate-like electrical state, with no claim that it is a measured firing rate or sufficient for all arbor computations. LPLC2 local dendritic nonlinearities, transmitter maps for untested pairs and calcium observation parameters are unknown. Do not add compartments to rescue a result.

Euler low-pass updates toward rectified weighted input; dt=0.005 s, tau=0.05 s for motion and neural filters, gain=1, no tonic input or adaptive/plastic state. Weights are contact counts divided by **full proofread postsynaptic input**. Positive T4/T5→LPi/LPLC2; negative LPi11→LPLC2, conditional negative LPi09→LPLC2 only in L1. All other anatomical rows are retained but unmodeled. Sign assignments are class-level physiological approximations, never inferred from a generic glutamate label. These feedforward equations have no recurrent autonomous drive. Retained-effective-input normalization is a sensitivity arm and fixed before any lesion; no ablation renormalization.

Nominal local retinal lattice spacing 5 degrees; Cartesian x=sqrt(3)/2*(q-p), y=-(p+q)/2. T4/T5 a,b,c,d preferred axes are +x,-x,+y,-y under a declared tangent-plane convention. This convention is not an audited root-specific angular map. Geometry sensitivity: mirror x and rotate direction axes by ±45 degrees; spacing 3 and 7 degrees. Additional one-at-a-time sensitivity: tau=0.02/0.1 s, gain=0.5/2, LPi gain=0/0.5/2, dt=0.0025 s, retained-input normalization. No arm is selected as the best biological model.

## Physical stimuli and measurements

Stimulus centered at each target's anatomy-derived input centroid. Two seconds static before and after motion. Primary: dark disk diameter 5→60 degrees at radial speed 10 degrees/s. Controls: time-reversed contraction; motion-free darkening within a 60-degree disk with identical continuous spatial luminance integral; translating 10-degree dark bar at 20 degrees/s; 20-degree-period square-wave grating at 1 Hz in a 50-degree aperture in four directions; constant-speed approach r/v=20,40,80 ms with diameter 5→60; bright expansion; final diameter 30 degrees; expansion center displaced by 40 degrees; temporal permutation of disk frames; no-motion control. The latter is a stationarity control, not evidence of specificity.

Use the same receptive-field position for paired controls. Record all selected neural states continuously, motion input, real time, and physical stimulus parameters. Report each root's peak, integral and peak time relative to motion onset. Units: arbitrary model rate, not Hz, mV, ΔF/F or response probability. Report all rankings and absolute values, not just pass/fail. No onset threshold will be invented for a biological latency claim.

## Preregistered gates

**Gate A qualitative requirements:** for each anatomical replicate, positive expanding-disk response above numerical zero, stronger than contraction, matched darkening and each wide-field grating; the ordering must survive the specified spacing, orientation, temporal and normalization sensitivities. These are directional constraints from experimental responses, **not** calibrated effect-size thresholds. No dark-versus-bright numerical ratio is established; measure without fitting. Speed/size/offset/temporal controls are descriptive because no compatible numeric response envelope is available. Numerical zero means absolute tolerance 1e-12 and is an engineering replay tolerance, not a biological detection threshold.

Additionally require a pathway-selective decrease after removing T4/T5→LPLC2 transmission while unlesioned upstream motion responses are unchanged; the matched off-route lesion must preserve that upstream responsiveness. Require changes under spatially permuted T4/T5 contact assignments (without changing total counts) to quantify anatomical contribution. Any successful rank that survives shuffling equally well cannot by itself establish anatomical selectivity. Each intervention's complete response is reported, not arbitrarily percentage-thresholded. No universal LPLC2-silencing claim is permitted from the trivial loss of its own readout.

SUPPORTED requires all qualitative controls, intervention attribution and robustness, together with an adequate independently supported input/observation correspondence for the **narrow neural claim**. Incomplete retinal crosswalk or an unidentified nonlinear calcium-to-rate correspondence limits biological inference even if model rankings work. Mixed results or such unresolved prerequisites → PARTIAL-INCONCLUSIVE. Systematic lack of the predicted ordering across the tested approximations → NOT SUPPORTED for this model, never a refutation of the biological circuit. Numeric amplitude/timing validation is explicitly unavailable and cannot be retroactively invented.

**Gate B:** run only after Gate A SUPPORTED. Prospectively require a real LPLC2→GF route, preparation-compatible excitatory effect, stable downstream response after upstream onset, route ablation reducing downstream while preserving upstream, and a matched off-route intervention. Without transferable DN physiology/observation constraints, only partial inference is possible; no motor label. If Gate A does not pass, Gate B is NOT TESTED, even if anatomical paths exist.

## Interventions and reliability

Families: T4/T5→LPLC2 route removal; LPi11 output removal; all LPLC2 silencing (trivial positive control only); matched off-route removal using the same number of strongest available rows/contact mass where feasible, reporting any mismatch; class-preserving T4/T5 source permutation of pathway rows; matched-size 8-root (or smaller common available count) T4/T5 lesions on versus off direct LPLC2 routes, matched by ON/OFF-direction subtype where feasible; stimulus-time permutation. Permutations are null graphs with labeled synthetic assignments, never new biological edges. Seeds 17,29,43; intact deterministic dynamics do not acquire fictitious biological replicates from seeds.

All interventions use pre-lesion normalization. Preserve sensory responses at unlesioned inputs, and distinguish pathway removal from global silence. Compare L0/L1 without retuning. Unknown omitted inputs remain unknown, with a declared no-external-drive boundary. No arbitrary external current arm.

Save full fast-state/motion-filter state, time/step and PCG64 state. Mid-trial snapshot restore must match continued traces at absolute 1e-12; fresh process must match pinned output within that tolerance. dt-halving is a numerical sensitivity, not a biological fit. Test finite bounded values and no spontaneous activity with blank input. No persistent memory is needed or introduced.

## Admission and stop

Record all failures, selection ambiguities, omitted contacts and operator coverage. Produce a candidate evidence update referencing the exact v0.1 release, with no admitted change or automatic capability upgrade. Preserve earlier classifications. Gate B failure or non-testing is not hidden in the overall classification. Stop after review artifacts; no Stage 5 or integration.

# Identifiability and permissible transfer

## 1. Observation units precede parameter fitting

Frozen rates lie between zero and one, synthetic sensory currents have arbitrary amplitude, and there is no measured Hz, mV, pA or ΔF/F observation operator. For a linearized response `y = c * g * u`, the data identify a product unless input and observation scales are independently measured. Replacing `(c,g)` by `(c/k,kg)` leaves the observation unchanged. Saturation introduces another unknown threshold/scale rather than automatically resolving this ambiguity.

A calcium indicator is a dynamic, potentially nonlinear observation of calcium, not a direct membrane-voltage trace. A fitted calcium decay can mix indicator kinetics, calcium handling, network recurrence and ongoing input. It cannot directly replace `tau` or `eligibility_tau`.

## 2. Contact normalization versus efficacy

The kernel uses `w_ij = g_class * contacts_ij / denominator_j`. A target-specific multiplier can exactly offset a changed denominator in a linear subnetwork. Without calibrated presynaptic activity, target responses and receptor/conductance data, a fit cannot decide whether a denominator or a gain caused an observed response. APL-mediated activity normalization is a different mechanism from static division by anatomical contact mass.

The boundary study's strong normalization effects therefore remain evidence of model sensitivity, not a reason to choose whichever denominator produces large learning. No denominator is selected by this study.

## 3. APL measurement fit

The two local observation coefficients predict off-site fluorescence from the measured on-site signal under each stimulation direction. The point-state alternative uses reciprocal fixed site gains: `F_lobe/F_calyx = g` for one stimulation direction and `F_calyx/F_lobe = 1/g` for the other. This alternative allows different indicator gains but still has one shared latent state.

Train six recordings; validate five untouched recordings. The conditional least-squares fit keeps all negative observations. Training-recording bootstrap intervals include zero in both directions. Unknown fly IDs prevent an independent-animal split and inflate uncertainty beyond the bootstrap. On-site measurements are noisy predictors. No precise nonzero coupling or cable length is claimed.

This identifies a failure of this simple one-state fluorescence representation under these stimulation conditions. It does **not** mathematically falsify every point-neuron computation with arbitrary nonlinear, stimulation-specific observation operators. Such extra operators would need their own independent evidence. Nor does a small calcium ratio measure the magnitude/spatial extent of the inhibitory effect on KCs.

`CALIBRATION_FROZEN.json` and `VALIDATION.json` are unchanged from the interrupted work. Their fitted observation coefficients are not APL synaptic gains and are not injected into Stage models.

## 4. Conditioning endpoint

The independent current-depression endpoint yields `R = exp(-H)`, where `H` is integrated effective depression. In a rule `H = eta * integral(eligibility * DA dt)`, the learning rate and unmeasured exposure are inseparable: multiplying eta by k and dividing exposure by k preserves the endpoint. `IDENTIFICATION_FROZEN.json` demonstrates a rank-one Jacobian for two unknown factors and an exact profile over a deliberately broad numerical range.

That range is an illustration of structural non-identifiability, not a credible interval for biological eta. The t-based uncertainty interval uses the published mean/SEM, not reconstructed individual cells. Because its remaining-current interval reaches zero, the effective-depression upper bound is unbounded. A floor at the observed endpoint censors additional depression; a floor below the endpoint cannot be inferred either. Matching this endpoint is not predictive validation.

Backward pairing and other compartments constrain rule form, but these measurements do not identify the unmeasured dopamine waveform in the frozen dimensionless model. EPSC charge and spikes are separate observations: fitting one cannot be called validation against the other without a current-to-spike transformation.

## 5. Recovery and body state

A response still suppressed at one interval and recovered at another does not identify a unique exponential recovery τ. Unknown depth, baselines, detection thresholds and activity-dependent recovery leave multiple fits possible. Repeated novel odors can change the history; spontaneous recovery cannot simply absorb every such mechanism.

Food deprivation duration is not a measured scalar energy reserve. A direction of PPL101 modulation does not specify `0.2 + 0.8r`, a 60 s body filter, a unit dopamine gain or a reciprocal acute efficacy divisor. These remain declared body-boundary or model assumptions. Hormonal compensation and cotransmission further prevent a single monotone universal rule.

## 6. Kernel decision

Quantitative data provide useful constraints and contradictions, but no transferable set identifies the present shared neural operator. No common calibrated kernel is exported. No mechanistic parameter is changed. The frozen observation fit and aggregate identification result are the only numerical calibrations; neither is a surrogate Genesis capability score.

The subsequent replay is a **null-transfer audit** with unchanged parameters, frozen after this transfer decision. It checks reproducibility and preserves a runnable out-of-sample evaluation path. It cannot answer how a genuinely calibrated kernel would change Stage capabilities. Those counterfactual values remain unavailable rather than inferred to be unchanged.

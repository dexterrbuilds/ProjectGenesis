# Aggregate conditioning identification, before numerical calculation

This addition does not change the frozen APL calibration. The published Hige et al. Figure 3 mean/SEM and protocol have been read, but no Stage-1/2/3 outcomes enter the calculation.

Target: fraction of γ1pedc MBON odor-evoked EPSC charge remaining after forward conditioning, 0.10 (depression 0.90 ± 0.037 SEM, n=5). Fit only the observation-level cumulative depression H in R=exp(-H). H is dimensionless integrated exposure, **not learning_rate**. A one-endpoint fit has no predictive degrees of freedom.

Quantify the t(4) interval on the published mean as a descriptive approximation; do not invent independent trials, uncertainty on each synapse, or a finite upper bound when the interval reaches zero remaining current. Show the exact η × unknown effective DA/eligibility exposure degeneracy. Show why an efficacy floor cannot be inferred from one endpoint.

Spike-count changes, backward timing and other compartments are applicability checks, not additional points fit as if they measured identical observables. No held-out numerical validation is claimed without raw responses/observation mapping. No coefficients from this aggregate demonstration are exported to any neural model.

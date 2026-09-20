# Physiology calibration and model identification

Scope: additive study only. No Stage 4, integrated kernel, new anatomy, retuning of old runs, or canonical runtime execution. All four completed studies and canonical code/state are protected.

## Decision process (recorded before numerical fitting)

1. Audit primary experimental measurements, preparations and cell-type crosswalks. Published fitted/simulation parameters are not measurements. Calcium fluorescence, voltage, spikes, current and behavioral performance are different observables.
2. A parameter is transferable only if units, target cell/compartment, stimulation, observation operator and relevant state are reconciled. Exact contact counts do not supply conductance, receptor sign or dopamine concentration.
3. Independently evaluate the spatial APL assumption using Amin et al. (2020) Figure 4D source data. The figure and first source rows were inspected during source discovery, before this plan; this is a registered analysis, not prospective biological preregistration. No Genesis outcome is an objective.
4. Fit a reduced two-site *fluorescence response* model, not a membrane kernel. Use alternating source rows (even zero-based indices for training, odd for validation), preserving four entries from each row together. Source files do not identify flies; a recording split is not independent-animal validation. No pruning, clipping of negative measured responses, or selection of favorable stimulation direction. Compare equal-site, one-state response with local transmission. Allow an observation-gain alternative and test whether that alone explains both stimulation directions. Bootstrap training rows, not individual cells within a row. Validation is evaluated once after fit freeze; no refit to validation.
5. Audit identifiability analytically: physical units, rate/indicator gain degeneracy, contact normalization vs synaptic conductance, DA/eligibility/rate product, plasticity floor, recovery and body mapping. Do not export an underidentified fitted combination as a complete physiological kernel.
6. Export a frozen calibrated neural kernel ONLY if independent data constrain its operator and observation mapping. Otherwise freeze the limited measurement fit and a machine-readable transfer rejection. Do not fabricate calibrated Stage-1/2/3 predictions from a fit of unrelated observables. Conditional calibrated replay is explicitly unavailable if no justified parameter transfer exists. Existing acceptance tests and exact replay remain preservation evidence, not calibrated validation.
7. Read historical outcome tables only after calibration/transfer decision is frozen. Prior outcomes are known to the analyst from earlier work; claim objective isolation, not analyst blinding. Fitting code must have no import or input from any Stage outcomes, network or acceptance thresholds.
8. No full-brain rebenchmark unless equations for a defensible neural kernel change. Report limitations and evidence needed for shared KC→MBON07/11 before any unification.

## Classification rules

- CALIBRATED KERNEL SUPPORTED: transferable numerical physiology and held-out neural validation support a coherent kernel; Stage outcomes never select parameters.
- PARTIAL PHYSIOLOGICAL CONSTRAINT: quantitative/structural/sign evidence constrains parts, but numerical transmission or common update rules remain unidentified.
- INSUFFICIENT PHYSIOLOGICAL DATA: no useful independent constraints can be established in the reviewed evidence.

Independent measurements may contradict frozen model assumptions without changing the historical classifications. No intended Genesis capability is an acceptance criterion here.

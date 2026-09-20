# Prospective T4/T5 identification plan

Brain Spec 0.1.0, Stage 4, the completed LPLC2 Diagnostic and all earlier results remain frozen. No LPLC2 model runs or Stage-4 stimulus/response evaluation is permitted. Only the algebraic definition of the frozen motion boundary is eligible as a baseline; no Stage-4 outcome table, target root response, sensitivity result or fitted preference is a fitting input.

## Data before fitting

Prioritize direct T4/T5 calcium (Gou/Matulis/Clark) and whole-cell voltage (Gruntman/Reimers/Romani/Reiser) measurements. Record original archive identifiers, versions, hashes, licenses, file layout, cell/fly grouping and acquisition definitions before processing response values. Exact reused T5 recordings in the publication's cited 2019 archive are eligible, with duplicate-source identities tracked. Do not label them independent replications. No Tm9 assay substitutes for direct T4/T5 validation.

The public Figshare whole-cell archive is accessible but large. Authors' code/metadata may be inspected before values. The physiological recordings, model simulations, fit-result tables and behavioral recordings must be classified separately. Authors' fitted model predictions cannot serve as empirical observations. If raw data cannot be fully obtained, report exactly which measurements were processed and which questions remain untested.

## Units and grouping gate

Keep voltage (mV), calcium (indicator-specific ΔF/F or normalized signal) and spikes separate. Use authors' processed baseline-subtracted signals only with audited definitions. Do not infer a fly ID from a cell array ordinal. Establish whether a recorded cell is one independent fly from original metadata/protocol. If grouping cannot be established, provide descriptive measurements but no fly-held-out validation claim. Published RF localization may define a conditional local coordinate system only if its role in train/test leakage is explicit; held-out responses must not choose their own amplitude, RF location or direction to improve prediction.

## Prospective candidate hierarchy

B0: frozen rectified two-site delayed correlation, strict T4 ON/T5 OFF, dt 5 ms and common filter tau 50 ms; measured-assay coordinate and observation scale separated from its neural operator.

B1: compact linear space/time response allowing a flicker term. B2: separate signed ON/OFF space/time response terms. Additional center/surround, temporally separate enhancement/suppression, or nonlinear directional terms are eligible only when direct independent measurements can distinguish them. Do not automatically instantiate all candidates or add explicit precursor neurons. Candidate equations, parameter bounds, observation mappings and selection penalty must be separately registered after metadata audit and before fitting values. No proposed scalar coefficient is a measured conductance.

## Validation gate

Split by documented fly, with all repeated trials/ROIs from one fly kept together. Use nested training-only selection for regularization and complexity. Where identities permit, use leave-one-fly-out prediction, equal weight per fly and stimulus family; report absolute prediction errors in original observation units. Prefer the smallest model within one standard error of the best inner-fold predictive score and report parameter/effective-degree counts; also report unpenalized held-out error. Do not use arbitrary success percentages.

Strong test: train on localized flashes/RF and predict apparent motion or moving bars in a separate family with no refit. Audit reused cells across archives. A conditional cell-localization assay is not equivalent to held-out-fly generalization. Failure in polarity/flashes invalidates a claim of a general boundary even when motion prediction improves. Unavailable families remain untested.

Report uncertainty using independent units; identifiability requires more than a low fitting error. A selected model cannot be declared a root-level boundary until the root→column→eye→subtype direction→screen transform, its uncertainties and observation model are frozen independently. Selection can remain inconclusive even if a limited assay prediction succeeds.

## Geometry

Use the authors' pinned eye-map data and anatomical landmarks, not Stage-4 radial alignment or response values, to establish coordinate conventions. Keep CATMAID index/skeleton, FlyWire root, column ID, lattice coordinate, retinal direction and stimulus-screen frame distinct. Unknown joins remain unknown. Do not choose an axis reflection or rotation by an output ranking.

## Precursor necessity

Poor compact-model fits do not prove an explicit Mi/Tm/CT1 network is necessary. Require an independently measured computation that a tested compact family cannot capture and a precursor architecture demonstrably captures under appropriate held-out data. If justified, specify a minimal circuit and stop; do not instantiate a large network.

## Stop

No Stage-4 evaluation, even after a possible model freeze. End with one requested classification and a precise acceptance scope; preserve negative results and untested requirements.

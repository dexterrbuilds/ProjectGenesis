# Conditional voltage prediction registration — prior to response-value analysis

This supplementary analysis is permitted by PLAN.md's distinction between conditional assay prediction and held-out-fly generalization. Original inputs at author commit fe52053dda84d49a124e6c1f141dd461eba9630c contain 17 recording ordinals, no fly/animal key, and author-localized stimulus positions. They cannot establish a population-level boundary. No model will be accepted as a general T4/T5 boundary from this analysis alone. No fly split is fabricated.

## Scope and partitions

All 17 original `data_cell_N_all.mat` inputs; no generated `result_cell` files. The `_spfr` files are acquisition/provenance checks only, not additional independent recordings. Whole-cell baseline-subtracted voltage (mV), author-provided 5 ms sample grid. Metadata define physical dark bars and presentation timing, not a danger or motion-direction score. The author-localized RF and PD axis are conditional external localization; they are NOT FlyWire/screen coordinates. No independent replicate claim for the T5 traces reused in 2021.

Training: single-bar flashes, width 2 pixels, all positions and durations provided. Inner assessment leaves an entire flash duration out. Locked test families: flash widths 1 and 4; moving bars; minimal/apparent motion; static gratings and drifting gratings where actually recorded. The latter are independent physiological stimuli, not Stage-4 gratings. Report every available family, not only successful predictions. No test amplitude, offset, timing, axis or RF adjustment. No test response used in hyperparameter/model selection. Fit separately per recording; results are conditional within-recording cross-stimulus predictions. Report medians/ranges across recordings descriptively, without pretending recordings are documented independent flies.

## Physical stimulus reconstruction

Reconstruct OFF occupancy from the authors' stimulus definitions on their 27-pixel local axis. Pulse onset is experimental time zero; the authors' model's `toff=25` is a model latency, not the stimulus clock. Width means contiguous pixels ending at the indexed location, matching the supplied code. Minimal motion uses the union of two bars, not double intensity at overlap. Moving bars reproduce entry and exit in the authors' position interval; static/drifting gratings use their supplied dark-pixel/phase lists. Retain sample times, family, cell ordinal, width, duration, direction and positions. Preserve unknown global angle, subtype and fly ID. Authors' interpolated/subsampled mean voltage is not spike count or calcium.

## Candidate set and complexity (fixed before reading response values)

Z: zero baseline-subtracted prediction, no parameters.

B0: frozen strict-OFF two-site rectified delayed correlator, dt=5 ms, tau=50 ms, sites -1 and 0 on the local axis; delayed source updated after response. Fit only one nonnegative voltage-observation gain on training flashes. A structural zero on static equal signals remains zero; no arbitrary extra flicker current. Site/angle scale is an explicit conditional pixel assumption, not an anatomical identification. Negative voltage cannot be represented by this baseline.

B1s: compact signed linear receptive field: seven overlapping Gaussian spatial basis functions centered at [-6,-4,-2,0,2,4,6] pixels, sigma=2 pixels. Filter each projected physical OFF occupancy through one exponential, tau in {20,50,100} ms. Seven signed voltage coefficients; no intercept. These bases/scale are engineering approximations, not seven precursor neurons.

B1t: same spatial basis with separate 20 and 100 ms filters; 14 signed voltage coefficients. Test whether independently reported spatial/temporal response structure helps prediction; do not interpret weights as conductance or receptor sign.

B1d: B1t divided by `1 + gamma * mean(abs(filtered basis signals))`, gamma in {0.1,0.3,1}; 14 signed numerator coefficients plus one selected compression hyperparameter. This is a compact phenomenological saturation candidate motivated by independently reported nonlinear voltage summation, not an identified conductance model. No explicit Mi/Tm/CT1 network.

For B1 candidates a common latency is selected from {0,10,25,50} ms, using training only. Ridge penalty lambda in {0,0.01,0.1,1,10}, relative to mean diagonal of the training feature Gram matrix; lambda=0 uses a pseudoinverse. Equal weight per stimulus trace in each mean-square error. Model selection uses inner duration-held-out MSE, then the smallest effective parameter count within one fold standard error of the best score; ties prefer lower inner error. Fold standard error is a selection heuristic, not a biological uncertainty estimate. Report selected and all fixed-family predictive errors, raw coefficient count, effective degrees of freedom, design rank/condition, and the range of training-competitive hyperparameters. Candidate-specific best inner fit is frozen before loading test responses for scoring.

## Decisions and failure cases

No arbitrary percentage acceptance threshold. General-boundary acceptance requires documented fly grouping, genuinely held-out biological prediction across relevant stimulus families, independently identified coordinate/observation mapping, and demonstrated scope including T4 and contrast polarity. These gates are not met by these compact T5 files. Conditional predictive errors may constrain representations but cannot bypass the gates. No numerical constant is transferred to Genesis or LPLC2. Missing preferred/nonpreferred polarity prevents identification of separate ON/OFF terms; B2 is specified but not fit. No isolated-column/retinal equivalence is inferred from one display pixel.

Identifiability: report training design singular spectrum, ridge effective rank, competitive hyperparameter ranges and coefficient stability across duration folds. This does not identify physiological conductances, precursor identities, membrane constants or a population kernel. Error intervals require biological independent units; no bootstrap of time samples as flies.

Tests must verify stimulus assembly, no temporal-wrap, trial reset, consistent unit/time ordering, no test fitting, and denial of old-study response inputs. Fresh-process results must reproduce within 1e-10 for floating outputs on the same library/BLAS environment. Neither Stage 4 nor LPLC2 runs are permitted.

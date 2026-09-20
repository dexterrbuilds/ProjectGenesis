# Prospective empirical sensory-interface feasibility protocol

This study neither reconstructs visual precursor circuitry nor seeks a universal mechanistic T4/T5 model. No Stage-4/LPLC2 result, model prediction or stimulus definition is an estimation input. Earlier results remain frozen. Register this document before building the new response atlas or evaluating empirical candidates. Existing measurements and previous limitations are already known; no claim of fresh biological blinding is made.

## Eligible sources and compatibility

Use the already acquired, checksum-verified 2021 direct T4/T5 flash/polarity measurements and original 2019 T5 recordings. The latter's flash measurements overlap the former and are excluded from the combined primary atlas, not counted twice. Keep non-flash 2019 T5 families separate. T4 and T5, source preparation, contrast polarity and family are categorical strata; no voltage/calcium/spike/rate pooling. Additional authoritative processed direct T4/T5 sources may be inventoried before atlas construction; if inaccessible or their identity/units cannot be audited they stay unavailable. No raw-imaging reconstruction or alternative upstream assay is a substitute.

No subtype, fly, root or retinal-angle identity is inferred from a recording ordinal. Use source dataset + cell ordinal as recording key. All class estimates are conditional on the authors' RF/PD localization; those localizers were response-derived, so recording holdout is not an anatomy-independent or localization-independent test. Lack of fly grouping forbids fly-held-out claims and population-independent confidence guarantees.

## Physical descriptors and output

Preserve exact family descriptors, source positions and source-centered RF offsets separately. Flash: polarity, pixel width, duration, RF-relative offset. Apparent motion: first/second positions, width, onset/offset of both bars, displacement and timing. Moving bars: traversed pixel positions, width, source direction code, step duration and implied source-pixel steps/second. Gratings: dark pixel pattern or exact phase sequence, step/flash duration. Retain source grid/frame and genotype/preparation keys. Do not replace a categorical family by a semantic motion/threat score.

Primary exported response is the observed mean baseline-subtracted **somatic voltage waveform from 0 to 500 ms**, on a 1 ms grid. This finite horizon is selected from source timing metadata before new estimation; it does not represent steady state or a complete response for longer stimuli. Original polarity arrays already supply a 1 ms grid; original compact voltage traces are linearly resampled in time within their sampled interval only. Preserve missing samples as missing; never zero-pad observations. Scalar summaries are the fixed-window mean and waveform RMS error. No calcium, spiking, synaptic release or model-rate conversion is identified.

## Empirical candidates (no hidden mechanism)

E0: nearest measured condition **within the same recording/preparation/type/family/polarity/width**. For flash held-out-value tests vary one axis at a time, hold all other descriptors fixed. Choose nearest absolute physical position or duration; ties average equally. No fitted scaling, physiology or temporal warping.

E1: linear interpolation of two bounding measured conditions on that same one-dimensional axis; convex weights fixed by the physical descriptor. Position gap at most 2 source pixels; duration ratio at most 4. These are prospectively declared locality limits for testing, not biological constants. No extrapolation, mixed polarity, width interpolation, simultaneous multi-axis interpolation or interpolation between stimulus families. Eligible queries must lie on source descriptor values observed somewhere in that same dataset/type/polarity/width stratum; untested continuous/subpixel queries are not promoted.

E2: exact-condition mean of other recordings, equal weight per recording. It is a conditional class-level observational template, not an individual neuron parameter. At least three other recordings must supply the exact full descriptor. The reference is a recording-balanced family average ignoring the tested detailed descriptor (for flash keep polarity/width/duration but average offsets; non-flash keep family). Also report the explicit zero baseline reference. No gain fit or test-record response normalization.

No regularized universal basis, neural network, precursor model or learned embedding is needed for this bounded comparison. If these methods fail, report failure rather than adding candidates after seeing outcomes.

## Held-out tests and prospective support rules

1. **Held-out flash position:** remove the entire target position value before retrieval within each recording, keeping width/duration/polarity fixed. Compare E0 and E1 on identical eligible conditions. Record boundary values without brackets as UNKNOWN for E1, not extrapolated estimates.
2. **Held-out flash duration:** remove the entire duration value analogously. Record sparse/non-bracketed cells as untested/UNKNOWN; no substitution of position holdout for duration validation.
3. **Leave one recording out**, separately per type/source/family, with E2 exact-condition prediction from other recordings. Keep original fly identity unknown. Test source-centered conditional transfer, not raw screen/root transfer. No direct lookup of the held-out recording.
4. **Hold out each entire family:** the catalog-based interface must return UNKNOWN for that family. Report zero response coverage, not perfect cross-family prediction. Never infer that uncertainty-aware abstention establishes a new family computation.
5. Report T4 and T5 separately, and failure regions by polarity/width/axis or family. All error reductions are in mV or mV², not downstream biological utility.

For E1 a stratum is (type, source, polarity, width, axis). For E2 it is (type, source, family, polarity; width retained in flash). A stratum needs at least five distinct held-out recording ordinals and at least 20 held-out conditions to support a comparative estimate. These sample-size safeguards are engineering choices, not biological response thresholds. Compute paired MSE differences after averaging equally within recording. A stratum passes comparative support only if the upper bound of a preregistered 95% percentile bootstrap interval (2,000 recording-block resamples, seed 20260919) is below zero against **both** the relevant empirical reference and zero prediction. For E1 the empirical reference is E0; for E2 it is the family-average reference. Intervals are conditional recording-level resampling summaries, not independent-fly population guarantees. Retain all failed/underpowered strata. No percentage magnitude threshold is invented.

Support classes:
- **DIRECTLY MEASURED:** exact full descriptor plus named source recording and observation frame; return source waveform/provenance. This is retrieval, not held-out validation.
- **INTERPOLATION-SUPPORTED:** E1 stratum passes the predefined tests, requested value is strictly bracketed within its validated locality, all other descriptors match, and the value lies on the source-tested descriptor set. Return an empirical voltage estimate with validation uncertainty. No biological mechanism claim.
- **WEAKLY SUPPORTED:** class templates (even when conditional E2 comparison passes), sparse/failed interpolation strata, unidentified requested transfer, or a new continuous value within a numerical range. A scientific template may be exposed as such, but the validated boundary returns UNKNOWN for a requested individual response.
- **OUT OF DISTRIBUTION / UNKNOWN:** absent family/preparation/observation/polarity, outside bracket/range/horizon, incompatible frame, requested root/subtype/column assignment without crosswalk, or any missing required descriptor. Never fabricate a waveform. Coverage is a set of observed tuples/validated local brackets, not a Cartesian product of marginal ranges.

## Uncertainty

For each prediction retain RMS, mean-voltage and maximum absolute waveform errors. Estimate a simultaneous waveform-error envelope from each *other* recording's maximum absolute residual over its held-out conditions; use the finite-sample 90% rank ceil(0.9*(n+1)), returning unbounded/unknown if that rank is unavailable. Evaluate coverage on the omitted recording. This is an empirical cross-recording residual envelope, not a guaranteed conformal band: recording independence/exchangeability is not established. Report its width, coverage, failures and calibration unit. Missing support is not represented by a zero response or artificially wide finite certainty. Do not use envelope results to change the selection criteria.

## Freeze and post-freeze audit

Freeze the empirical interface, complete support rules/strata, physical descriptor schemas and observation mapping with content hashes before opening any Stage-4 stimulus code/config. Only then inspect physical descriptors in the frozen Stage-4 stimulus generator, without importing/running it or reading response outputs. Compare those descriptors with the support domain and record failures. The audit cannot alter support or candidates. No Stage-4 or LPLC2 simulation, no canonical cycles, no BrainAdapter changes.

## Classification

EMPIRICAL SENSORY INTERFACE SUPPORTED requires demonstrated conditional recording and stimulus-value generalization across multiple families for both T4 and T5, with adequate observation/coordinate compatibility for a prospectively stated use. LIMITED EMPIRICAL INTERFACE SUPPORTED requires faithful direct retrieval, at least one independently held-out empirical component meeting the registered comparative criteria, explicit restricted scope and correct UNKNOWN behavior. If no empirical component meets those criteria, classify INSUFFICIENT MEASUREMENT COVERAGE for a predictive interface; preserve the raw retrieval catalog without upgrading it. None of these classifications licenses downstream execution or reconstructs omitted precursor circuitry. Stop for review.

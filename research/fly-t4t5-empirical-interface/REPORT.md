# T4/T5 Empirical Sensory Interface Feasibility Study

## Finding

**LIMITED EMPIRICAL INTERFACE SUPPORTED**

A restricted empirical voltage catalog is justified. Conditional templates predict several held-out recording responses better than registered references; two dark-flash T5 duration-interpolation strata also pass the registered comparisons. This does **not** establish a general T4/T5 sensory boundary, continuous visual-field coverage, a precursor reconstruction, or a usable root-specific input to LPLC2.

The strongest defensible export is a **mean baseline-subtracted somatic-voltage waveform, in mV, over 0–500 ms**, tied to its source preparation, recording/localizer, exact physical stimulus tuple and observation convention. Negative voltage changes are retained. Calcium, spikes, release and model rates are not interchangeable with this quantity.

## Prospective design and isolation

`PROTOCOL.md` and `REGISTRATION.json` predate atlas construction and new comparisons. They specify candidates, holdouts, support rules, sample-size safeguards, uncertainty and classification. There is no parameter optimization or neural simulation. Estimation reads only the new measurement atlas and its coverage metadata; `ESTIMATOR_ACCESS.json` records these inputs. Prior Stage-4/LPLC2 outcomes are excluded by the estimator's file-access guard.

One independently detected implementation error was corrected before interface freeze: JSON serialization distinguished integer and floating representations of the same number, including signed zero. `NUMERIC_IDENTITY_CORRECTION.json` documents the change; the complete initial code/results remain in `pre_numeric_identity_correction/`. Only mathematical numeric identity was corrected. No physical descriptor, array order, stimulus family, candidate or acceptance criterion was removed or changed. The correction added legitimate exact-condition matches, notably for moving bars. All quantitative results below use the corrected, locked outputs.

`PRIMARY_RESULT_LOCK.json` freezes the comparisons. `INTERFACE_FREEZE.json` then freezes the interface, support/descriptor/observation rules and compatibility limits **before** any old Stage-4 stimulus definition was inspected. The subsequent static audit cannot feed back into estimation.

## Measurement coverage atlas

| Source / class / family | Mean waveforms | Recording ordinals | Distinct full tuples | Recordings per tuple |
|---|---:|---:|---:|---:|
| 2021 T4 flash | 2,260 | 15 | 184 | 1–15 |
| 2021 T5 flash | 2,204 | 17 | 297 | 1–17 |
| 2019 T5 apparent motion | 1,633 | 17 | 603 | 1–14 |
| 2019 T5 moving bar | 268 | 17 | 66 | 1–6 |
| 2019 T5 static grating | 176 | 11 | 92 | 1–4 |
| 2019 T5 drifting grating | 96 | 11 | 56 | 1–3 |

Total: **6,637 mean waveforms / 3,325,137 resampled voltage values**. These are not independent trials or flies. The 1,398 reused 2019 flash protocols are excluded, and the two T5 sources are not pooled as independent recordings. No T4 non-flash family is in the acquired primary atlas.

Flash coverage includes contrast codes 0/1 (dark/light), widths 1/2/4 source pixels, T4 durations 40/160 ms and T5 durations 20/40/80/160/320 ms. RF-relative offsets span −8 to +9 for T4 and −10 to +12 for T5 **across** recordings; those marginal ranges are not complete joint coverage. Polarity is uneven, especially in T5.

T5 apparent-motion tuples preserve both bar positions, displacement, width, all onset/offset times and source timing codes. Displacements include 0, ±1, ±2, ±3, ±4, ±6 and ±8 pixels; durations span the observed discrete values 20–480 ms. Second onsets can extend beyond 500 ms: **146 source conditions have a second onset later than the export horizon**, so their truncated waveforms do not validate the second response. Moving bars retain the entire traversed pixel sequence, both direction codes, widths 1/2/4, step durations 20/40/80/160 ms and corresponding 50/25/12.5/6.25 source-pixel steps/s. Static gratings retain exact dark-pixel positions and 40/160 ms durations; drifting gratings retain full patterns, phase sequences and 20/40/80/160 ms steps. No degree-scale conversion is assumed.

Preferred/null biological direction labels, subtype, fly, retinal position, column and root are **unknown** in this export. Source direction ordering is preserved rather than relabeled. Sparse-bar calcium, isolated-column flicker and a generic two-dimensional visual-field response are not covered by these voltage means. `COVERAGE_ATLAS.json`, `atlas/records.json` and `DESCRIPTOR_SCHEMAS.json` contain exact tuples and marginal inventories.

## Empirical candidate comparison

- **E0:** nearest measured condition within recording, varying one physical axis; equal-weight tie averaging.
- **E1:** two-neighbor linear interpolation, with fixed descriptor-derived weights. No fitted physiological parameter. Only same-recording one-axis flash interpolation, strict brackets and registered locality bounds.
- **E2:** exact-condition, equal-recording-weight template from at least three other recordings. Held-out recording is excluded. Reference is a recording-balanced family mean, plus zero prediction.

No learned embedding, deep network, precursor circuit or additional basis was introduced. Complexity is explicit: E0/E1 retrieve one or two condition means; E2 stores an empirical condition-mean waveform and its contributing recording IDs. These are nonparametric tables, not zero-complexity biological models. Their effective flexibility grows with sampled tuples; they cannot extrapolate to new families. No tunable regularization or free physiological coefficient is identifiable from this comparison because none was fitted.

The registered comparison requires ≥5 recording ordinals and ≥20 held-out conditions and a negative upper 95% recording-block bootstrap bound on the MSE difference against both the empirical reference and zero. These safeguards are engineering selection rules, not biological magnitude thresholds. Each stratum is tested separately; no familywise discovery claim is made.

### Key held-out results

| Test | Conditions / recordings | Median recording RMSE, mV | Reference RMSE, mV | Paired MSE-difference 95% interval, mV² |
|---|---:|---:|---:|---|
| T5 dark flash, width 1: held-out duration | 130 / 5 | 1.578 | 2.028 | [−1.598, −1.026] |
| T5 dark flash, width 2: held-out duration | 120 / 5 | 1.721 | 2.644 | [−4.289, −3.369] |
| T5 apparent motion: held-out recording | 973 / 17 | 3.018 | 4.979 | [−20.072, −14.219] |
| T5 moving bar: held-out recording | 232 / 16 | 2.908 | 5.219 | [−22.130, −13.799] |

All four also beat the zero reference under the same rule. Across all comparisons, **14/40 strata pass**: two E1 duration strata and twelve E2 conditional templates (ten flash and the two T5 motion families). The estimator generated **9,430 held-out predictions**. Full successes, failures, zero comparisons and per-recording values are in `VALIDATION_TABLES.md` and `VALIDATION_RESULTS.json`.

Five of six T4 flash E2 strata pass, with median recording RMSE 1.346–2.410 mV among passing groups. Dark width 1 fails comparative superiority. Five of six T5 flash E2 strata pass, with RMSE 1.659–2.559 mV; light width 1 fails. A passing conditional template remains **WEAKLY SUPPORTED for transferring physiology to a new individual**, not a validated per-root response.

### Negative and unavailable results

All twelve position-interpolation comparisons tie E0 **exactly**: nearest-neighbor ties on the equally spaced tested grid are averaged, which equals linear midpoint interpolation. Their MSE-difference intervals are [0,0]. This is algebraic non-discrimination under the registered methods, not proof that physical position is irrelevant or RF responses cannot be interpolated. The tie convention was not changed after seeing results; no position stratum is promoted.

T4 has no interior observed duration bracket; T5 light flashes likewise provide no eligible duration prediction. T5 dark width 4 has only six conditions from one recording and is underpowered. Static grating E2 has only eight eligible conditions from four recordings and is underpowered. Drifting gratings have no exact tuple with three **other** recordings and therefore no eligible E2 predictions. Range overlap or family-name similarity cannot repair these deficiencies.

The strongest cross-family test returns **UNKNOWN for every entirely withheld family**. This is correct refusal with zero predictive coverage, not successful cross-stimulus generalization. There is no cross-type, cross-preparation, joint duration×position or newly parameterized trajectory prediction. T4 is assessed separately and has flash-only evidence.

## Uncertainty, observation and coordinate limitations

The two supported duration groups each have five recordings. The registered finite-sample 90% rank envelope cannot be formed from the other four recordings; its width is **null/unbounded**, despite favorable comparative error intervals. This is weak evidence for precise individual prediction. Comparative bootstrap bounds do not repair missing trial/fly information.

For passing E2 strata, descriptive recording-max residual envelopes have median half-widths **10.56–17.94 mV**. Empirical recording-held-out coverage is approximately 92.3–94.1%, but these wide envelopes are based on extreme errors across multiple conditions and time points. They are not population guarantees, uncertainty intervals on a class-template mean, or identified biological noise. Apparent motion gives ±17.877 mV and 16/17 recording coverage; moving bars ±15.060 mV and 15/16. New individuals remain uncertain.

All alignment is conditional on authors' response-derived RF/PD localizers. Unknown fly grouping forbids fly-held-out language and may overstate effective independence. Reused source recordings are not independent replications. The unavailable retinal/head/root transform is a discrete unresolved crosswalk, not a small calibrated angular error. Same-recording translation/reflection would preserve interpolation distances; it would not establish anatomical registration or independent localization. Full preparation, genotype, license and coordinate limits are in `SOURCE_AND_COMPATIBILITY.md`.

## Frozen support and export behavior

1. **DIRECTLY MEASURED:** exact source/frame/observation/full stimulus tuple and named recording; retrieve genuine source mean, with provenance. Retrieval itself is not validation.
2. **INTERPOLATION-SUPPORTED:** only the two passing T5 dark duration strata, on source-tested discrete values, strict registered brackets, same recording and all other descriptors unchanged. Return mV estimate and explicitly unknown predictive envelope when applicable.
3. **WEAKLY SUPPORTED:** conditional class templates, exposed only by an explicit scientific-template request. Failed/sparse/new-continuous interpolation or an individual request without a recording returns UNKNOWN.
4. **OUT OF DISTRIBUTION / UNKNOWN:** missing/incompatible family, frame, preparation, observation, descriptor or horizon; root/subtype/column/fly transfer; no bracket or unsupported physical stimulus. Return `voltage_mV: null`, never a zero waveform.

`interface.py` is a small isolated research API, not BrainAdapter or a neural kernel. `INTERFACE_SPEC.json` and `SUPPORT_SPEC.json` are the proposed frozen empirical specification. No source-trace quantity is renamed neural activity, firing probability or behavior.

## Post-freeze Stage-4 support audit

After interface freeze, the old `Movie` source class and primary stimulus-name list were inspected as text/AST only. No model was imported, executed or evaluated; no response file was read. All **16/16** primary physical conditions are UNKNOWN: expanding/receding/approach discs, bright/small/offset/permuted discs, dimming, translation, four angular gratings and blank. Detailed physical descriptions and reasons appear in `STAGE4_SUPPORT_AUDIT.json`.

The angular 2-D geometries, finite apertures and temporal trajectories are not measured source-pixel tuples; no screen/retina/root transform or soma-to-terminal conversion is available. Even blank cannot be assigned a fabricated zero physiological waveform merely because the measurements are baseline-subtracted. This audit caused no interface changes.

**Future LPLC2 feasibility:** these data are insufficient to specify independently validated continuous T4/T5 inputs over a novel 2-D expansion experiment. A future study would need compatible direct physiological coverage of its actual descriptors (including spatial/temporal context), independent registration, and an identified output observation appropriate to downstream coupling. A narrow voltage catalog can support future measurement-matched empirical work, but cannot fill those gaps. No LPLC2 computation was tested here.

## Computational and storage implications

On this arm64 macOS host, atlas generation took 1.819 s; the corrected comparisons took 4.882 s and peaked at 224,296,960 bytes (~213.9 MiB RSS). The atlas has 26,605,104 uncompressed array bytes (~25.4 MiB); compressed waveforms are 24,083,798 bytes. Minimal runtime files total 29,479,926 bytes (~28.1 MiB).

Interface initialization took 0.123 s. Across 300 exact retrievals, median/p95 query latency was 2.205/2.576 ms; across 100 interpolation queries, 2.750/3.247 ms. The benchmark process, including two loaded interfaces and metric records, peaked at 116,391,936 bytes (~111.0 MiB). This measures empirical-table operations, not real-time neural computation or precursor simulation. `INTERFACE_BENCHMARK.json` preserves host and measurement definitions.

## Reproduction and preservation

Fresh-process replay used copied empirical inputs only and reproduced every metric/interval JSON byte-for-byte and every saved prediction array exactly (tolerance zero). Ten interface tests verify faithful retrieval of all 6,637 means, holdout separation, numeric identity, the position tie, supported interpolation, observation/root/OOD refusal, family-held-out refusal, file-access isolation and locked results. No test treats failure to predict as biological success.

Final preservation checks cover the 8,762 pre-existing protected files and the exact Brain Spec v0.1 registry release. The read-only canonical database hash equals its pre-study hash: seven life cycles, one organism and disabled schedule. See `PRESERVATION.json`, `SPEC_VALIDATION.json` and `CANONICAL_AFTER.json` for final check results. C. elegans, prior classifications, canonical anatomy ownership and BrainAdapter remain unchanged.

## Scientific boundaries

**BIOLOGICAL FACT:** the source experiments measured these somatic voltage means under their documented visual/recording preparations.

**EXPERIMENTALLY SUPPORTED COMPUTATIONAL APPROXIMATION:** narrow, conditional empirical comparisons pass the registered held-out tests; their limits and large uncertainty remain explicit.

**ENGINEERING ASSUMPTION:** the finite export horizon, descriptor equality, locality bounds, sample-size safeguards, resampling and error selection rules. These are not discovered biological constants.

**UNRESOLVED:** general visual prediction, subtype/root assignment, calcium/spike/release conversion, natural-state physiology, independent fly uncertainty and downstream use.

**GENESIS PRODUCT MAPPING:** none. No biological capability, threat behavior or prior-stage classification is promoted. No empirical result reconstructs omitted precursor mechanisms. Stop for review.

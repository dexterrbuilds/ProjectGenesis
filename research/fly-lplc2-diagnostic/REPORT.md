# LPLC2 Visual Computation Diagnostic Study

## Conclusion

**PARTIAL MECHANISTIC CONSTRAINT — MORE DATA REQUIRED**

Independent biology identifies missing computations in the frozen visual boundary and unresolved coordinate/observation mappings. It does **not** identify a complete replacement LPLC2 physiological model. No new neural representation or parameter kernel is frozen for a Stage-4 rerun.

The strongest findings are:

1. The strict polarity split and antisymmetric two-site correlator exclude independently observed responses: non-preferred-contrast T4/T5 responses and isolated-column T4 flash responses. Their absence cannot be repaired by adjusting the frozen correlator's gain or common time constant.
2. In a static audit of the frozen extraction, **all 24 T4/T5 subtype × LPLC2 groups have negative mean radial alignment under the assumed screen axes**, from −0.9841 to −0.4171. This warns of a coordinate/direction correspondence problem. It does not independently establish the correct replacement transform. No flips, rotations or alternate geometry were tested against Stage-4 responses.
3. Anatomy retained is not physiology instantiated: **zero retained anatomical input contacts into the selected T4/T5 cells have active transmission operators**. Their activity comes from the synthetic motion boundary. LPLC2 effective input mass is only 39.58% at L0 and 40.51% at L1.
4. A new independent numerical restriction test did **not** favor added flexibility: a signed constant Tm9 ON calcium response had worse leave-one-fly-out prediction than zero. This is preserved as a negative comparison, not replaced by a more favorable assay.
5. LPLC2's spatially organized arbors and nonlinear calcium response constrain candidate computations, but do not identify the number of independent electrical states, an interbranch coupling constant, or a membrane nonlinearity. The APL result supplies none of these parameters.

## Frozen scope and dependencies

Brain Spec **v0.1.0**, registry SHA-256 `6b3a27ea3c41a87e701ca8a7eec7fd31d5e41469db7da27916b81cb040eb923e`; Stage-4 content SHA-256 `405d5e982b75846c0e24949f27effd122c3171ebbec77932a30da17b90e3c66a`. Release/dependency validation precedes the diagnostic. See `DEPENDENCY_LOCK.json`, `VALIDATION.json`, and `PRESERVATION.json` for the final audit.

**Stage 4 remains Gate A NOT SUPPORTED; Gate B NOT TESTED.** Its frozen observations remain: visual activity without required expansion selectivity; receding/wide-field responses can exceed expansion; 0/90 complete ordering groups; route removal eliminates LPLC2 readout while preserving upstream trajectory; spatial shuffling can increase expansion; L1 does not rescue. Those observations motivate questions but are not fitting data. None of the diagnostic estimators loads Stage-4 outcome tables. No Stage-4 simulation, new extraction, neural optimization, life cycle, or integration was performed.

`PLAN.md` and `DIAGNOSTIC_REGISTRATION.json` preceded biological value extraction. The source-workbook addendum was registered after access failures and header inspection, before numeric values. It changes the available independent assay, not the Stage-4 criteria. The primary planned T4/T5 dataset remains unprocessed; the narrower Tm9 comparison is not presented as its substitute validation.

## 1. Failure decomposition: where information is absent or lost

This is an audit of the **frozen implementation**, not a universal judgment about point neurons. Machine-readable classifications and sources are in `TRANSFORMATIONS.json` and `EVIDENCE.json`.

| Transformation | Classification | Frozen operation | Missing or discarded information |
|---|---|---|---|
| Physical movie → screen | Engineering assumption | Analytic angular movies; intensity 0/0.5/1 | Photon scale, spectrum, optical/display transfer, contrast adaptation |
| Screen → column sampling | Engineering assumption | Flat hex grid × 5°, fixed subtype axes | Retinal curvature, nonuniform angles, eye/head orientation, chiasm convention |
| Local intensity | Engineering assumption | Two points ± half-spacing | Optical acceptance field; measured multi-column receptive field and surround |
| Intensity → polarity | Engineering assumption | T4=max(I−0.5,0), T5=max(0.5−I,0) | Non-preferred-polarity signals; changes below baseline; stimulus-statistics history |
| Polarity → correlation | Engineering assumption | Delayed near × far minus near × delayed far, rectified | Flicker response; distinct enhancement/suppression subfields; richer temporal kernels |
| Correlation → T4/T5 state | Engineering assumption | Synthetic drive into scalar leaky activity | Anatomical precursor computation; voltage/calcium distinction; type-specific kinetics |
| Root/type/column identity | Experimentally constrained | Pinned roots/annotations/column assignments | Recorded ROI identity and a validated root-to-visual-direction crosswalk |
| Column → retinal direction | Unidentified | Assumed cardinal axes on the grid | Independently established sign, local direction, visual-angle scale, RF center |
| LPi/LPLC2 transmission | Weakly constrained | Selected class signs; count-based weights | Target receptors, synaptic efficacy/delay, unknown retained operators |
| Normalization | Engineering assumption | Full-input mass, or frozen retained-input sensitivity | Physiological gain and omitted baseline conductance |
| LPLC2 integration | Engineering assumption | Signed pooled current → rectification → scalar state | After pooling, branch/layer identity; no identified local integration rule |
| LPLC2 state → measurement | Unidentified | Dimensionless activity read directly | Indicator kinetics, baseline, saturation, voltage-to-calcium mapping |

The anatomical contacts themselves are experimentally observed reconstruction evidence; their numerical transmission operators are not. No entire transformation becomes “experimentally measured” merely because one ingredient is anatomical.

### Structural restrictions, not a new simulation

`ALGEBRAIC_CHECKS.json` contains reproducible mathematical checks, explicitly **not neural traces**:

- A movie confined below the gray background gives identically zero T4 boundary drive, for every frozen gain/tau; the bright counterpart gives zero T5 drive. Independent sparse-bar and electrophysiological work establishes a broader response repertoire. [Gou et al.](https://doi.org/10.1016/j.cub.2024.10.053), [Gruntman et al.](https://doi.org/10.1016/j.cub.2021.09.072)
- For a stationary separable flash, `c_i(t)=a_i b(t)`, identical linear filters give `H(c_1)c_2−c_1H(c_2)=0`. The check agrees to roundoff. Isolated-column T4 calcium responses are positive; a motion-only zero-flash boundary cannot represent that assay. This does not claim every large-field flicker stimulus must excite T4. [Haag et al.](https://elifesciences.org/articles/17421)
- Supra-additivity does not uniquely identify local voltage compartments: one scalar with observation `F(v)=v²` has F(1+1)=4 while F(1)+F(1)=2. This is a non-identifiability counterexample, **not** a proposed calcium law.
- Pooling `[2,0]` and `[1,1]` gives the same scalar sum while a hypothetical local nonlinear operator can distinguish them. Thus pooling can discard useful information. It does not establish that LPLC2 implements that operator or that a structured scalar model cannot explain selectivity.

## 2. Independent visual-pathway evidence

Source-specific preparation, assay, crosswalk, unknowns and access status are recorded in `EVIDENCE.json` / `DATA_AUDIT.md`. Different indicators, genotypes, cell classes and stimulus backgrounds are not pooled into one kernel.

**Early preprocessing.** L1/L2/L3 distribute differing luminance and contrast information rather than implementing a universal ON/OFF split. Recurrent early visual processing can generate biphasic temporal responses. The frozen boundary represents neither computation. These observations justify measuring upstream temporal/spatial filters, not importing a paper's fitted coefficients as synaptic constants. [Ketkar et al.](https://doi.org/10.7554/eLife.74937), [Pang et al.](https://doi.org/10.1016/j.cub.2024.11.064)

**T4/T5.** Targeted-column experiments distinguish spatially offset preferred-direction enhancement and null-direction suppression. Published T4 neighboring-column responses are about 50% and second-ring responses about 25% of the center; the corresponding L2 values are below 30% and 12%. These are normalized calcium assay measurements, not conductances. The apparent-motion enhancement maximum near 500 ms lag, using 472 ms pulses, is not a membrane tau. Opposite-polarity and stimulus-density effects further reject a universal pure-polarity boundary. Raw independent recordings are still needed to identify and validate a replacement across stimulus families.

**LPi.** Class-level opposing-motion inhibition is supported. GluCl-dependent inhibition measured in tangential targets does not assign a receptor to every LPLC2 root. LPi11/LPi4-3 has stronger LPLC2 functional support than LPi09/LPi3-4. The L1 LPi09 sign remains a hypothesis. Its 24 contacts cannot be converted into a measured conductance or delay. [Mauss et al.](https://doi.org/10.1016/j.cell.2015.06.035), [Klapoetke et al.](https://doi.org/10.1038/nature24626)

## 3. Independent numerical comparison and receptive-field measurements

Source: Ramos-Traslosheros and Silies publisher source workbook, Fig7g. Female flies, 1–7 days, right-optic-lobe GCaMP6f; control condition without CDM. ON/OFF full-field flashes last 2 s with intermediate background intervals. We used all **70 ROI rows from seven labelled flies**, averaging within fly before fitting/testing. Units are **ΔF/F0**, not voltage or rate. [Primary paper and source data](https://doi.org/10.1038/s41467-021-24986-w)

| Independent observation comparison | Result |
|---|---:|
| Fly-weighted control ON mean | −0.01160384 ΔF/F0 |
| Fly-weighted control OFF mean | +0.35349107 ΔF/F0 |
| Zero ON-response restriction, 0 fitted parameters: held-out MSE | 0.00214001 (ΔF/F0)² |
| Signed constant fitted on other flies, 1 parameter: held-out MSE | 0.00272952 (ΔF/F0)² |
| Folds improved by the signed constant | 3/7 |

The signed model is **27.55% worse by held-out MSE**. Fly-level ON means range from −0.0866741 to +0.0482516; four are negative and three positive. Every fold, prediction, ROI source row and error is saved in `INDEPENDENT_RESULTS.json`. No fly was removed or response window reselected. This does not overturn the paper's spatial contrast-opponency result: a full-field average is not a local RF assay, and fluorescence baseline/surround cancellation matter. Nor does it validate the entire frozen motion model. It means a single transferable signed constant is not supported by this independent comparison. No coefficient is transferred.

Descriptive paired-recording source widths (`Fig6f`, 41 ROI entries per column): Tm9 OFF FWHM means **9.931° horizontal / 8.848° vertical**; T5 **11.409° / 11.648°**. These constrain the need to represent spatial integration, not a universal 5° lattice correction. No new RF fit was performed and the 41 rows are not claimed to be 41 independent flies. Full Fig4j-m width summaries, including missing measurements, are retained.

The planned direct T4/T5 polarity comparison was not run: Dryad metadata were available, but file endpoints returned 401/403. Gruntman’s 6.32 GB whole-cell archive was inventoried but not processed. These are concrete data opportunities, not completed held-out validation.

## 4. Retinotopy and subtype geometry

The frozen target roots are strings: `720575940623047629`, `720575940637088602`, `720575940611740569`. No new roots or synapses were selected. Their contact-weighted motion-input centroids, and eight subtype centroids per target, are in `ANATOMY_AUDIT.json`.

We computed the contact-weighted mean dot product between each source's **assumed** preferred-direction unit vector and its radial vector from the frozen target center. All 24 group means are negative; the range is **−0.98408 to −0.41706**, unchanged at L1 because direct T4/T5→target contacts are unchanged. This uses only anatomy and frozen coordinate assumptions. It is not an independent estimate of the biological receptive-field center or motion direction.

The separate crosswalks are:

1. Root → annotated type: pinned anatomical evidence.
2. Root → column: frozen metadata mapping with excluded conflicts.
3. Column → retinal viewing direction: **unvalidated for these roots**.
4. Subtype → local direction in that visual frame: **unvalidated**.
5. Retinal coordinates → experimental screen/head frame: **unvalidated**.
6. Afferent centroid → physiological LPLC2 RF center: **surrogate, not a measurement**.

The eye-map study documents nonuniform sampling, locally varying directions and a medulla/eye left-right flip. Its EM anatomy is FAFB, but its microCT eye and H2 recordings are different female preparations. CATMAID skeleton IDs and FlyWire roots are not interchangeable. Central alignment is better constrained than peripheral alignment. A proper transformation must use anatomical landmarks and independent visual physiology, with errors reported; it cannot be chosen because expansion wins. [Zhao et al.](https://doi.org/10.1038/s41586-025-09276-5)

## 5. LPLC2 representation: what locality is actually established?

Four spatially arranged lobula-plate arbors and outward/inward motion interactions constrain the **spatial organization of inputs**. Supra-additive axonal calcium constrains the measured input-output relationship. Neither identifies where the nonlinearity occurs. A synaptic interaction, a local dendritic computation, a single-neuron output nonlinearity and indicator nonlinearity can be observationally confounded. [Klapoetke et al.](https://doi.org/10.1038/nature24626)

A later primary study measures local calcium and translated-object responses under different stimulus conditions. It reinforces the need to preserve site and preparation in observation models; it does not supply a measured electrical coupling matrix. Its spot results do not retroactively change Stage-4 grating or ordering criteria. [Kim et al.](https://doi.org/10.1016/j.cub.2022.12.014)

An additional 2025 primary study independently links Beat-VI/Side-II manipulation to layer-4 dendritic/input gradients and tuning. This strengthens the need to preserve input topography and population position; it does not identify an electrical state count. Its FAFB/hemibrain anatomy, developmental molecular measurements and adult GCaMP7f recordings are distinct preparations. Only the published mechanism was audited here; source measurements were not fitted. No gene-expression gradient or physiological coefficient is assigned to the three frozen roots. [Molecular gradients study](https://doi.org/10.1038/s41586-025-09037-4)

**Supported:** preserve real neuron identity, input location/layer metadata when available, local versus axonal recording identity, and nonlinear observable alternatives. **Not identified:** four independent voltage compartments, interbranch conductance, LP-versus-lobula delay, a required minimum local state count, or root-specific receptor maps. Do not copy APL states/coefficient values. Aggregated pre/post/neuropil rows do not provide exact branch synapse coordinates.

## 6. Omitted anatomy and functional participation

| Quantity | L0 frozen | L1 frozen |
|---|---:|---:|
| Neurons | 748 | 818 |
| Directed pairs | 6,292 | 7,538 |
| Pre/post/neuropil rows | 6,612 | 7,889 |
| Anatomical contacts | 15,559 | 19,896 |
| Contacts with declared active operators | 7,710 | 10,414 |
| Retained contacts with unknown/excluded operators | 7,849 | 9,482 |
| LPLC2 retained input / full input | 1,032/2,587 (39.89%) | 1,056/2,587 (40.82%) |
| LPLC2 effective input / full input | 1,024/2,587 (39.58%) | 1,048/2,587 (40.51%) |
| LPLC2 output retention | 2.238% | 2.328% |
| LPi11 input retention / effective fraction | 60.52% / 60.34% | 61.47% / 60.34% |
| LPi09 input retention / effective fraction | absent | 77.70% / 73.69% |

T4/T5 input retention is approximately 5–9%, but its **effective anatomical input fraction is zero for every selected subtype**. Keeping additional motion cells with synthetic drives does not reconstruct their missing precursor computation. LPi11's retained fraction rises at L1 while its active input count stays **6,686**; anatomical closure and functional participation differ.

L0 examples of missing precursor input: T4c omits 3,960 Mi1, 1,288 Tm3, 1,060 Mi9 and 871 CT1 contacts; T5c omits 2,614 Tm9, 2,220 Tm2, 1,649 Tm1, 1,611 CT1 and 964 Tm4. These types plausibly carry contrast, spatial and temporal information absent from the synthetic boundary. Exact totals by population/type/neuropil are saved, without inventing physiology for unidentified partners.

Across the three LPLC2 targets, **1,555 input contacts are omitted at L0; 1,531 at L1**. Leading L0 classes include other LPLC2 (196), PVLP011 (118), Y3 (92), Tm5f (84), Tm20 (81), TmY5a (52), Tm27 (46), Tm5e (43), Tm37 (42), LPi02 (37). Counts support missing information, not a sign or mechanism. The functional name Tm5Y in separate work is not automatically identified with Tm5f/TmY5a. Missing LPLC2 recurrence is anatomical evidence only; its dynamics remain unknown.

### Prospective closure priorities, not instantiated circuits

1. Audit retinal/column correspondence and precursor RF measurements before expanding a network.
2. For T4/T5, select real Mi/Tm/CT1 afferents by the measured class/subfield mechanism and pinned contacts; preserve each omitted boundary. Recurrent lamina context is justified only if the selected temporal assay requires it.
3. Recover LPLC2 input branch/layer locations and LPi input/output sites; separately audit LPi11 and LPi09 function/receptors. Count-only additions cannot identify local E/I arrangement.
4. Audit the major lobula/central afferent classes for independent function before including operators. Keep unknown operators unknown. No arbitrary tonic drive or count threshold supplies missing physiology.

No population is proposed because it increased a modeled response; no closure simulation was run.

## 7. Candidate comparison and identifiability

| Candidate | Independently testable constraint | Finding / status |
|---|---|---|
| Frozen synthetic motion boundary | Non-preferred bars; isolated-column flicker | Structural zeros incompatible with the broader measured repertoire; not calibrated |
| Measured T4/T5 boundary | Per-fly polarity, speed, RF and timing | Relevant data identified; direct quantitative comparison incomplete due to access/processing limits |
| Tm9 observation-only signed constant | Fig7g held-out fly means | Worse prediction than zero; no added flexibility selected |
| Retinotopically calibrated boundary | Anatomy/eye landmarks plus independent direction map | Mechanistically justified calibration target; selected-root mapping not validated |
| Spatially structured scalar LPLC2 + observation nonlinearity | Local motion interactions and axonal calcium | Viable candidate class, not identified or excluded by scalar count alone |
| Local LPLC2 states | Simultaneous local/axonal, spatially targeted perturbation data | Local calcium exists, but voltage state number/coupling unidentifiable here |
| Filter/delay-aware transmission | Type/site-specific impulse/apparent-motion recordings | Required phenomena constrained; no universal time constant identified |
| Conductance/receptor-aware model | Independent target receptor and electrical data | Insufficient for this extraction; complexity not adopted |

Important non-identifiabilities:

- Presynaptic amplitude, synaptic gain, contact normalization and observation gain can compensate each other. A calcium amplitude alone cannot identify all four.
- Temporal response convolves precursor processing, membrane integration and indicator kinetics. One peak time cannot assign a separate tau to each stage.
- Coordinate direction, spatial E/I arrangement and receptive-field center can trade off in an output fit. Fix geometry independently before fitting output physiology.
- Pooling before a nonlinearity versus nonlinear local processing cannot be resolved from only an axonal sum; use independently targeted spatial measurements and interventions.
- Normalization remains an engineering choice. This diagnostic preserves the earlier finding that normalization/model assumptions can dominate anatomical expansion. No normalization is chosen for greater capability.

The study supplies constrained exclusions and missing-measurement priorities, not unique causal attribution of the Stage-4 failure. Multiple inadequacies coexist. Their contribution to the failed ordering cannot be quantified without a separately preregistered, independently identified model.

## 8. Computational implications

These are transparent state/operation budgets, **not throughput claims** for an unimplemented model. Frozen L0 has 739 motion cells, 748 scalar rates and 1,478 delay values: **2,226 float64 values / 17,808 bytes** of dynamic rate/delay state. L1 has 806 motion cells and 818 rates: **2,430 values / 19,440 bytes**. Sparse operators, metadata and traces are additional.

A boundary with `k` filters at `s` sample sites per motion cell needs roughly `k*s*M` filter values, plus output and observation states. At L0, one extra value per motion cell costs 5,912 bytes; an illustrative three-site/two-filter allocation would have 4,434 filter values (35,472 bytes), **not a selected architecture**. A geometry map storing a viewing direction and tangent preferred direction needs about six float64 values per mapped root (35,472 bytes at L0), before interpolation neighborhoods. `q` local states for each of three LPLC2 neurons adds `3*(q−1)` values; cost alone does not justify them. Anatomical afferent closure and raw trace storage may dominate these small state increments.

No numerical neural throughput, real-time factor, full-brain RAM estimate or skipped-update scheme is inferred from these counts. No richer neural equations were defined. Diagnostic runtime/RAM measurements in `PERFORMANCE.json` apply only to read-only analysis and workbook processing.

Measured fresh-process analysis on this 8-logical-CPU arm64 Mac: workbook extraction/comparison **0.302 s wall / 0.205 s CPU / 50.91 MiB peak RSS**; full-anatomy read-only audit **3.408 s wall / 2.357 s CPU / 1.073 GiB peak RSS**. Page cache and mapped arrays affect these measurements. The workbook occupies 4,459,008 bytes. These figures benchmark diagnostic processing, not the future neural substrate.

All **11 diagnostic checks passed**; a separate fresh process reproduced workbook, anatomy and algebraic results exactly on this machine. All **5,620 protected files** match their baseline hashes. Read-only database snapshots match SHA-256 `3377c9dddbe2abf89ed9a820a6aabbc1da951cac7bfc1823471c5aac043ea312`: seven historical cycles, disabled schedule. The accepted neural suites were not rerun because this task changed no neural model; preservation is established by byte hashes and release checks.

## 9. Decision and review boundary

There is enough independent evidence to reject several universal simplifications and prioritize a **future identification protocol**: obtain accessible T4/T5 per-fly traces, validate root/column/eye/screen geometry, retain polarity/space/time information through the boundary, and distinguish axonal observation nonlinearities from local voltage mechanisms. Fit only independent physiological assays, hold out flies/stimulus families, penalize complexity, and freeze that candidate before any Stage-4 comparison.

There is **not yet** enough evidence here to freeze a complete new prospective LPLC2 model. No updated capability or Brain Spec entry is proposed for admission. Previous stages, Stage 4, C. elegans and canonical Genesis remain unchanged. This diagnostic ends here for review.

**PARTIAL MECHANISTIC CONSTRAINT — MORE DATA REQUIRED**

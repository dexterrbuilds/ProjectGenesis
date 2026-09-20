# Stage 4 — physical visual-stimulus neural experiment

## Final result

**Gate A: NOT SUPPORTED. Gate B: NOT TESTED. Overall Stage 4: NOT SUPPORTED for the frozen model.**

The anatomy-constrained model produces visual activity, but it does not reproduce the independently reported LPLC2 expansion selectivity. Contraction and wide-field motion exceed expansion in the primary trials. **0/90** root × level × primary/sensitivity groups satisfy all prospectively specified qualitative orderings. No model was retuned or selected for a favorable result. This is a negative result for this conditional representation/encoder/physiology package, not evidence that flies lack looming-sensitive circuitry.

The unresolved root-to-retinal angular correspondence and calcium observation operator further limit biological inference. Gate B was not simulated: anatomical paths alone do not authorize a descending response claim.

Dependency: Brain Spec v0.1.0 `6b3a27ea3c41a87e701ca8a7eec7fd31d5e41469db7da27916b81cb040eb923e`. Release and required entries passed preflight before extraction/experimentation. `PREREGISTRATION.json` records the pre-result protocol digest; `MODEL_FREEZE.json` pins implementation before the first primary result. The release validator approves compatibility of declared prior dependencies, **not** these new roots or an unvalidated physiological operator. New anatomy/assumptions remain an unadmitted extension.

## Anatomy and effective transmission

| Level | Neurons | Directed pairs | Neuropil rows | Contacts | Modeled-sign contacts | Unknown-operator contacts |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | 748 | 6292 | 6612 | 15559 | 7710 | 7849 |
| L1 | 818 | 7538 | 7889 | 19896 | 10414 | 9482 |

All contact rows come from pinned v783 anatomy. Individual anatomical contacts are aggregated by pre/post/neuropil; these are not fabricated individually localized synapses. Three central right LPLC2 cells were selected by mapped-input centroid before activity was computed. L1 adds LPi09 and its mapped T4/T5 inputs. There is no effect-selected expansion. Rows shared by L0/L1 have identical canonical IDs and no independent plastic ownership. No rows overlap the prior canonical registry; the prior shared KC→MBON07/11 identities remain untouched.

| Level / population | N | Anatomical input retained | Effective modeled input / full | Anatomical output retained |
| --- | --- | --- | --- | --- |
| L0 / LPLC2 | 3 | 39.892% | 39.583% | 2.238% |
| L0 / LPi11 | 6 | 60.518% | 60.338% | 3.963% |
| L0 / T4a | 22 | 5.172% | 0.000% | 6.477% |
| L0 / T4b | 52 | 8.959% | 0.000% | 9.069% |
| L0 / T4c | 87 | 6.262% | 0.000% | 5.360% |
| L0 / T4d | 206 | 6.875% | 0.000% | 15.004% |
| L0 / T5a | 26 | 6.243% | 0.000% | 7.414% |
| L0 / T5b | 56 | 8.429% | 0.000% | 8.221% |
| L0 / T5c | 91 | 6.022% | 0.000% | 5.302% |
| L0 / T5d | 199 | 6.572% | 0.000% | 13.135% |
| L1 / LPLC2 | 3 | 40.819% | 40.510% | 2.328% |
| L1 / LPi09 | 3 | 77.701% | 73.687% | 11.767% |
| L1 / LPi11 | 6 | 61.475% | 60.338% | 6.310% |
| L1 / T4a | 22 | 5.303% | 0.000% | 6.685% |
| L1 / T4b | 52 | 9.027% | 0.000% | 9.172% |
| L1 / T4c | 114 | 7.732% | 0.000% | 10.306% |
| L1 / T4d | 206 | 7.072% | 0.000% | 15.172% |
| L1 / T5a | 26 | 6.717% | 0.000% | 7.849% |
| L1 / T5b | 56 | 8.599% | 0.000% | 8.390% |
| L1 / T5c | 131 | 7.058% | 0.000% | 10.765% |
| L1 / T5d | 199 | 6.917% | 0.000% | 13.304% |

Boundary statistics include every proofread incoming/outgoing contact for each selected population. The T4/T5 physiological inputs are largely outside the extraction and replaced by a declared local-motion sensory boundary. Their low anatomical input retention is not repaired by simulated photoreceptor circuitry. Unknown retained rows contribute no current under the explicit boundary, rather than becoming known zero physiology.

L0 LPLC2 omits 1,555 incoming and 1,092 outgoing contacts. Major missing input classes: LPLC2 (196), PVLP011 (118), Y3 (92), Tm5f (84), Tm20 (81), TmY5a (52), Tm27 (46), Tm5e (43).

L1 LPLC2 omits 1,531 incoming and 1,091 outgoing contacts. Major missing input classes: LPLC2 (196), PVLP011 (118), Y3 (92), Tm5f (84), Tm20 (81), TmY5a (52), Tm27 (46), Tm5e (43).


Root/type mapping joins 5,921/6,100 right T4/T5 roots. The column table has 174 type/side conflicts overall; conflicting assignments are excluded and listed, not silently repaired. Hexels are anatomical coordinates, not measured degrees. The three retained output identities are:
- `720575940623047629`
- `720575940637088602`
- `720575940611740569`

## Primary continuous response measurements

Peak units are arbitrary rate-like model activity. No conversion to Hz, mV or calcium fluorescence is claimed. Columns identify the three roots in the order above.


### L0

| Physical condition | 720575940623047629 | 720575940637088602 | 720575940611740569 |
| --- | --- | --- | --- |
| expand | 0.0005080928 | 0.0003376013 | 0.0003570286 |
| recede | 0.001605165 | 0.002035761 | 0.002037164 |
| dim | 0 | 0 | 0 |
| translate | 0.0009706708 | 0.00155829 | 0.001095393 |
| grating_0 | 0.0009546295 | 0.00156049 | 0.0008744085 |
| grating_90 | 0.001989482 | 0.00240441 | 0.002158993 |
| grating_180 | 0.002906162 | 0.001753615 | 0.003037 |
| grating_270 | 0.0009084132 | 0.001337836 | 0.001675631 |
| approach_20 | 0.000695592 | 0.0005656527 | 0.0003178033 |
| approach_40 | 0.0005195942 | 0.0005244698 | 0.0003663017 |
| approach_80 | 0.0004374347 | 0.0004140412 | 0.0003862548 |
| bright | 0.0002892154 | 0.0001805907 | 0.0004258898 |
| small | 0.0005080928 | 0.0003376013 | 0.0003570286 |
| offset | 0.0002363919 | 0.0003351249 | 0.0006566542 |
| shuffle_time | 0.003634544 | 0.004002344 | 0.004468186 |
| blank | 0 | 0 | 0 |

### L1

| Physical condition | 720575940623047629 | 720575940637088602 | 720575940611740569 |
| --- | --- | --- | --- |
| expand | 0.0005075235 | 0.00031429 | 0.0003527455 |
| recede | 0.001604104 | 0.002033495 | 0.002034042 |
| dim | 0 | 0 | 0 |
| translate | 0.0009706708 | 0.00155829 | 0.001095393 |
| grating_0 | 0.0009546295 | 0.00156049 | 0.0008744085 |
| grating_90 | 0.001885128 | 0.002279592 | 0.002115118 |
| grating_180 | 0.002906162 | 0.001753615 | 0.003037 |
| grating_270 | 0.0009073819 | 0.001335859 | 0.001675272 |
| approach_20 | 0.0006914518 | 0.0005299331 | 0.0003029053 |
| approach_40 | 0.000515507 | 0.0004870553 | 0.0003503623 |
| approach_80 | 0.0004368269 | 0.0003842789 | 0.000373094 |
| bright | 0.0002876305 | 0.0001802968 | 0.0004201191 |
| small | 0.0005075235 | 0.00031429 | 0.0003527455 |
| offset | 0.000236034 | 0.0003351249 | 0.0006566542 |
| shuffle_time | 0.00359154 | 0.003936884 | 0.004441828 |
| blank | 0 | 0 | 0 |

Full time series, per-trial integrals, peak times, physical conditions and upstream responses are in `MEASUREMENTS.csv`, `RESULTS.json` and referenced trace files. The 96 primary files store **every selected neural rate and every local motion input**, with 5 ms updates; sensitivity/intervention files store genuine continuous target and upstream summaries. No activity was synthesized for presentation. Identical small/full expansion peaks mean the peak occurred in their shared early stimulus segment, not a calibrated angular threshold.

Luminance-matched darkening gives zero activity, but symmetric local correlation can cancel uniform dimming by construction. This is therefore not independent validation of LPLC2. The decisive receding and grating controls fail. Bright responses, offsets, approach velocities and frame shuffling are descriptive controls without invented biological response intervals.


## Causal interventions

Percent changes below are descriptive, not acceptance thresholds. Each cell is the expansion-peak change relative to its own intact baseline.


### L0
| Intervention | 720575940623047629 | 720575940637088602 | 720575940611740569 |
| --- | --- | --- | --- |
| route_remove | -100.000% | -100.000% | -100.000% |
| matched_route | +2.202% | +2.460% | +11.445% |
| lpi_remove | +2.310% | +3.083% | +11.493% |
| output_silence | -100.000% | -100.000% | -100.000% |
| shuffle_space seed 17 | +45.755% | +218.832% | +274.798% |
| shuffle_space seed 29 | +62.435% | +28.407% | +166.533% |
| shuffle_space seed 43 | +84.397% | +78.235% | +131.841% |
| sensory_lesion | +0.108% | +0.000% | +0.000% |
| matched_sensory | +0.000% | +0.000% | +0.000% |

### L1
| Intervention | 720575940623047629 | 720575940637088602 | 720575940611740569 |
| --- | --- | --- | --- |
| route_remove | -100.000% | -100.000% | -100.000% |
| matched_route | +2.248% | +9.289% | +9.908% |
| lpi_remove | +2.312% | +3.223% | +11.602% |
| output_silence | -100.000% | -100.000% | -100.000% |
| shuffle_space seed 17 | +45.697% | +234.787% | +277.037% |
| shuffle_space seed 29 | +61.924% | +30.949% | +165.967% |
| shuffle_space seed 43 | +83.990% | +91.455% | +131.987% |
| sensory_lesion | +0.220% | +0.000% | +0.000% |
| matched_sensory | +0.000% | +0.000% | +0.000% |

Removing the modeled T4/T5→LPLC2 route eliminates that readout while the complete upstream sensory-sum trajectory remains identical. This demonstrates transmission dependence **within a deliberately feedforward operator**, not successful looming computation. LPLC2 silencing is a trivial control. Contact shuffles alter activity, often increasing expansion response, without establishing the required selectivity. LPi removal and matched sensory lesions can have small positive effects through disinhibition. This is not renamed a successful behavioral intervention.

| Level | Route lesion rows/contacts | Off-route control rows/contacts | Matched sensory roots |
| --- | --- | --- | --- |
| L0 | 389 / 922 | 389 / 5752 | 8 / 8, subtype matched |
| L1 | 389 / 922 | 389 / 7033 | 8 / 8, subtype matched |

The off-route lesion is row-count matched, **not contact-mass matched**: it removes much more input to LPi. Its disinhibition is mechanistically expected in this operator, so it is an imperfect strength-matched control and cannot validate physiological specificity. Eight-root lesions match ON/OFF-direction subtype but not all connectivity/physiology. No denominator is recomputed after intervention. All raw changes and mismatches are retained.


## Closure, normalization, parameter and numerical sensitivity

| Root | L1 vs L0 expansion change | L0 retained/full normalization ratio | dt-halved L0 peak change |
| --- | --- | --- | --- |
| 720575940623047629 | -0.112% | 2.4569× | -2.054% |
| 720575940637088602 | -6.905% | 2.7896× | -0.681% |
| 720575940611740569 | -1.200% | 2.1178× | -2.761% |

The entire grid includes lattice spacing 3/5/7°, x reflection, direction axes ±45°, tau 20/50/100 ms, gain 0.5/1/2, LPi gain 0/0.5/1/2, dt 2.5/5 ms and two normalization denominators. These are stress ranges, **not physiological confidence intervals**. Results for every condition/root are saved. No best normalization is promoted. Retinal mapping, normalization and missing dendritic nonlinearities remain confounded with actual anatomy; this experiment cannot apportion biological versus modeling causes of failure. Targeted closure is insufficient and no arbitrary drive was added.

All 846 trials are finite; maximum network rate was 0.1149382. Static blank trials remain exactly zero. Finite feedforward activity is not validation of unknown biological recurrent stability. dt-halving changes the sampled discontinuous stimulus as well as Euler integration; its difference is not an isolated truncation-error estimate.


## Descending anatomy: Gate B not tested

| GF/DNp01 root | Full input contacts | All LPLC2 contacts | All LC4 contacts | Selected seed contacts |
| --- | --- | --- | --- | --- |
| 720575940622838154 | 4327 | 458 | 374 | 0 |
| 720575940632499757 | 5147 | 622 | 431 | 17 |

The three right LPLC2 seeds contribute only 17 contacts to the right GF (0.330% of its full proofread input). These real paths are insufficient to interpret descending dynamics after failed Gate A. No DN state, motor probability or action label was computed. Root-specific downstream sign remains unknown; differing predicted transmitter labels are not receptor evidence. FAFB does not contain the VNC body.


## Reproduction and cost

| Level | Replay max absolute error | Restored-tail max error | Fresh process | Checkpoint bytes |
| --- | --- | --- | --- | --- |
| L0 | 0.0 | 0.0 | exact readout + final state hashes | 27434 |
| L1 | 0.0 | 0.0 | exact readout + final state hashes | 29701 |

Both seed-dependent null graph/movie replays also match exactly. Checkpoints contain all fast electrical and motion-filter states, explicit timestep/clock and PCG64 state; no slower or plastic memory exists. Mismatched model snapshots are rejected.

846 trials, 1,127,310 updates, 5370.945 simulated seconds; 87.488 s total wall time and 86.525 s CPU, including saved traces. Trial computation totals 65.506 s. Peak process RSS 179.73 MiB; saved traces 78.86 MiB. Measured on arm64 / macOS-27.2-arm64-arm-64bit, Python 3.12.14, NumPy 2.3.5. This small feedforward model does not benchmark a full brain or identified physiology. Extraction cost is recorded separately in `CIRCUIT_MANIFEST.json`.


## Scientific distinction and review boundary

**Biological fact:** independent flies show the reported LPLC2 selectivity; pinned FAFB supplies roots, types and anatomical contacts. These are not response measurements for our three roots.

**Computational approximation/assumption:** local motion boundary, scalar integration, class-level signs, contact scaling, missing-input boundary, screen geometry and numerical constants. The experiment shows these particular assumptions do not reproduce the required selectivity. It does not identify a correct replacement or justify opportunistic local states.

**Genesis product mapping:** none. No fear, danger perception, escape choice, avoidance, voluntary action or digital-world interpretation is established. No LLM/prose memory participates in the equations.

`CANDIDATE_EVIDENCE_UPDATE.json` proposes only a narrow negative model-result claim and anatomy references. It is **UNADMITTED**, supersedes nothing and promotes no capability. Biological looming sensitivity remains supported by the independent literature; this model has not reproduced it. Revisit retinal crosswalk, measured local input/output transfer and representation adequacy in a separately reviewed prospective study, rather than fitting this failed model to a semantic goal.

Prior stages/specification, C. elegans and canonical state are checked in `PRESERVATION.json`. Genesis retains its original seven cycles and disabled schedule. No prior model, result, database state or BrainAdapter was modified. This experiment ends here for review.

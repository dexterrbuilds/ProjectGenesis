# Drosophila Physiology Calibration and Model-Identification Study

## Final classification: PARTIAL PHYSIOLOGICAL CONSTRAINT

Independent experiments constrain several signs, mechanisms, response scales and spatial representations. They do **not** identify the numerical normalization, transmission, modulation and plasticity kernel shared by the current Stage-1/2/3 models. No calibrated common neural kernel is justified or exported.

The completed studies remain frozen: Stage 1 **PASS**, Stages 2 and 3 **PARTIAL-INCONCLUSIVE**, architecture **INSUFFICIENT EVIDENCE**. This study does not begin Stage 4 or revise their conclusions.

## What was completed

- Primary literature/data audit covering 20 evidence entries, including quantitative electrophysiology, calcium, timing, receptor and internal-state observations: [evidence table](EVIDENCE.md).
- All 41 declared parameter instances plus 24 operator/boundary assumptions classified: [parameter matrix](PARAMETERS.md), machine-readable [audit](PARAMETER_EVIDENCE.json).
- String-preserving annotation audit of 37 named roots against pinned FAFB v783/v3.1.0 sources: [crosswalk](CROSSWALK.md).
- Frozen independent APL observation fit and held-out recording validation; separate aggregate conditioning identifiability experiment.
- Eight fresh-process unchanged-kernel protocol replays, exact historical-state comparisons, snapshot restoration and deterministic replay. Genuine traces and state snapshots are saved under `replays/`.
- Full preservation audit of earlier experiments, C. elegans and canonical Genesis. No neural model, parameter, extraction, threshold or old report was changed.

## Independent numerical findings

### APL: structural constraint, not a synaptic gain

The frozen [Amin Figure 4D analysis](https://elifesciences.org/articles/56954) uses six training and five held-out recordings. A conditional two-site fluorescence model fits off-site/on-site coefficients **0.016511** and **0.003214**. Their recording-bootstrap 95% intervals are **[−0.002380, 0.046367]** and **[−0.009811, 0.021819]**: neither establishes precise nonzero coupling.

| Observation model | Training MSE | Held-out MSE |
|---|---:|---:|
| Local response coefficients | 0.004163 | 0.007014 |
| Shared activity, equal site gain | 7.523911 | 5.008791 |
| Shared activity, fitted reciprocal site gain | 7.292075 | 5.796135 |

Units are squared ΔF/F; this is conditional prediction using measured on-site response. The local model's held-out error is about **826× smaller** than the fitted shared-state alternative. Unknown fly IDs prevent animal-independent validation. The result supports spatial response structure under this assay; it does **not** identify APL→KC conductance, electrical space constant, membrane τ, or inhibition throughout FAFB. The APL coefficients were never transferred into the neural models.

### Conditioning: one measured endpoint leaves a parameter ridge

The independent [γ1pedc current-depression measurement](https://pmc.ncbi.nlm.nih.gov/articles/PMC4674068/) gives remaining charge 0.10. Fitting only `R=exp(−H)` yields integrated depression **H=2.302585**. An approximate small-sample t interval gives remaining charge **[0, 0.202728]**, hence **H≥1.595888 with no finite upper bound** under this surrogate.

For `H=η×unmeasured DA/eligibility exposure`, the two-parameter Jacobian has **rank 1**. An illustrative five-order-of-magnitude η profile fits equally, with maximum numerical residual **4.16×10⁻¹⁷**. This is an identifiability demonstration, not a biological η range. Neither η nor the efficacy floor is identified. There is no held-out numerical validation for this single aggregate endpoint, and no transfer to α1 appetitive physiology.

[Identifiability analysis](IDENTIFIABILITY.md) separates observation, normalization, dopamine exposure, recovery and body-state ambiguities. A measured membrane timescale in MBON14 cannot calibrate α′3 MBON16/17 or every neuron in the network.

## Blind replay and comparison

The [transfer decision](TRANSFER_FROZEN.json) was frozen **before** replay and historical-result comparison. The fitter has no Stage model/outcome inputs. The analyst knew earlier results, so this is objective separation, not analyst blinding.

**No calibrated neural parameter transfer was justified.** Therefore a calibrated Stage-1/2/3 out-of-sample prediction is unavailable. We executed the prespecified **null-transfer control** instead, using the unchanged kernels and original protocols; these controls must not be labeled calibrated validation.

| Original metric, first original seed | Cue A | Cue B | Comparison with frozen original |
|---|---:|---:|---|
| Stage 1 selective depression | 49.945215% | 37.673009% | Exact |
| Stage 2 stimulus specificity | 0.001653474% | 0.002299165% | Exact |
| Stage 3 MBON11 resource contrast, trial 10 | 0.053774383% | 0.049584330% | Exact |
| Stage 3 MBON11 experience, low-resource trial 10 vs 1 | −0.026144405% | −0.023822375% | Exact |

All **8/8 trained states**, deterministic replays and pre-training restoration checks match. Fast-reset responses and Stage-2 recovery also match saved originals. [Replay comparison](REPLAY_COMPARISON.json) includes an additional all-trial mean contrast, explicitly distinct from the original trial-10 metric above; [original-metric table](REPLAY_TRIAL10.json) preserves the original definition.

Consequently:

- Stage-1 associative learning remains reproducible in its original model. Whether calibration makes its magnitude biologically plausible is **unresolved**, especially without matched α1 physiology.
- Stage-2 familiarity and Stage-3 resource effects remain small in the control replay. Their change under a genuinely calibrated kernel is **not estimated**.
- No normalization, gain or plasticity parameter was selected to strengthen any capability. The boundary study's model-assumption sensitivity remains intact.

## Common-kernel assessment

The **4,622 shared KC→MBON07 rows** and **1,053 shared KC→MBON11 rows** still lack one reconciled physiological state/update rule. The largest unresolved choices are contact normalization, dopamine receptor/locality mapping, acute versus persistent modulation, transmitter effects by target, and spatial APL representation. Type identity and real anatomy alone cannot resolve them.

[Unified-physiology assessment](UNIFIED_PHYSIOLOGY.md) specifies the required independent measurements. It does not merge rules or build an integrated brain. Particularly, NMDA dependence does not by itself establish the net MBON07→PAM11 sign; the frozen Stage-1 code's stronger comment is qualified here without altering it.

## Computation and preservation

Measured null-transfer replay costs include original training, probes, replay and trace/state serialization; they are not full-brain benchmarks. Separate workers ran concurrently for portions of the study, so wall times are machine-load dependent.

| Stage | Fresh-process runs | Wall time per run | Peak process RAM |
|---|---:|---:|---:|
| 1 | 2 | 9.97–10.56 s | 265.4–325.5 MiB |
| 2 | 2 | 1.96–2.11 s | 123.7–132.3 MiB |
| 3 | 4 | 32.18–34.42 s | 265.1–317.9 MiB |

No neural equations were changed, so no new full-brain benchmark was appropriate. The earlier generic ~0.7 GiB result does not establish the cost of future compartmental, receptor or conductance physiology.

**Verification:** 30 existing Stage-1/2/3 tests passed; 8 study tests passed. The audit verifies **3,647 protected files** plus **17 completed files from the interrupted physiology study** unchanged. Canonical database checksum before/after is `3377c9dddbe2abf89ed9a820a6aabbc1da951cac7bfc1823471c5aac043ea312`: one organism, seven decisions/life cycles, schedule disabled. No canonical cycle ran.

## Remaining uncertainty and review decision

The literature search is targeted, not an exhaustive proof that further physiological data do not exist. Some preparation metadata remain unresolved, and several useful raw datasets require access or a matched measurement model. The strongest numerical fit here has recording-level rather than animal-independent validation. The aggregate depression fit is underidentified by construction. Neither supports a whole-brain physiological kernel.

The next evidence needed is matched type/compartment-specific transmission and receptor measurements, calibrated PN/KC/DAN input and observation scales, and separate acute-state versus persistent-learning protocols. This is an evidence requirement for review, not authorization to proceed.

**PARTIAL PHYSIOLOGICAL CONSTRAINT.** Stop for review. No Stage 4, common brain, Genesis integration or outcome-driven retuning.

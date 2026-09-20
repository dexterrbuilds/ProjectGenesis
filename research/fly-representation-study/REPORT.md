# Drosophila Neural Representation and Minimal Physiology Study

## Classification: INSUFFICIENT EVIDENCE TO SELECT REPRESENTATION

**A local APL response representation is supported within the tested assays. A common numerical neural representation across the studied circuits is not yet supported.** The evidence favors allowing heterogeneous representation: retain local calcium/modulatory/plastic states where measurements require them, and use simpler electrical representations where they predict the measured quantity adequately. It does not justify compartmentalizing every neuron or selecting a universal conductance model.

This classification follows the original PLAN.md standard: a transferable representation requires independently supported parameters/observation mappings and predictive evidence across phenomena. It does not erase the narrow APL result. No Stage outcomes entered fitting or selection. No calibrated kernel or Stage replay was produced. No Stage4 or Genesis integration occurred.

## 1. What was preserved and completed

The interrupted fit, validation, source workbooks and analysis plan were checksum-frozen before continuing. Earlier Stage1 PASS, Stage2/3 PARTIAL-INCONCLUSIVE, architecture INSUFFICIENT EVIDENCE and physiology PARTIAL PHYSIOLOGICAL CONSTRAINT remain unchanged. The study adds source-quality review, spatial descriptive data, analytical temporal/conditioning tests, a representation specification, real-anatomy cost envelopes and identity deduplication. It does not replace earlier models or results.

The work distinguishes three levels:

- **BIOLOGICAL FACT:** independently recorded fluorescence/current/voltage, experimental perturbations and pinned anatomical rows.
- **COMPUTATIONAL MODEL:** conditional response fits, local-state families, explicit engineering benchmarks and identifiability calculations.
- **GENESIS MAPPING:** none.

## 2. APL: structural support without identified nonzero coupling

The frozen Figure4 experiment uses six training and five validation recordings of the same calyx/lobe stimulation assay. There are nine flies across11 recordings; fly IDs are unavailable, so recording splits are not demonstrably animal-independent. Prior validation was already inspected; this study calls it **reused validation**, not a fresh test.

| Observation model | Fitted coefficients | Training MSE | Training AICc | Leave-one-recording-out MSE | Reused validation MSE |
|---|---:|---:|---:|---:|---:|
| R0 shared activity, reciprocal site gains | 1 | 7.292075 | 29.1748 | 7.577657 | 5.796135 |
| R1 two local regions, zero transfer | 0 | 0.005506 | −60.0224 | 0.005506 | 0.007751 |
| R1 two local regions, one shared transfer | 1 | 0.004482 | −59.5595 | 0.007029 | 0.008314 |
| R1 two local regions, directional transfer | 2 | 0.004163 | −56.7776 | 0.007224 | 0.007014 |

MSE units are squared fluorescence ΔF/F. AICc includes residual variance and assumes independent Gaussian residuals as a working approximation; within-recording directions/fly clustering weaken that assumption. No coefficient is fitted per recording. The calyx/lobe partition comes from anatomy and stimulation sites.

The single shared coefficient is q=0.0115377, with recording-bootstrap95% interval[0,0.0309142]. **A positive physiological coupling constant is not established.** The two-direction model improves reused validation error over zero by only9.51%, below the original20% convention for a material improvement. Training complexity and leave-one-recording-out comparisons favor the zero-transfer approximation. None of this changes the accepted earlier two-coefficient fit.

The result rejects the tested shared scalar **linear fluorescence observation** representation. It does not prove that APL voltage must follow the same spatial structure as its calcium signal, nor exclude every nonlinear/region-specific observation model. Conditional prediction uses measured on-site response; it does not independently predict the on-site neural response from ATP stimulation.

### New spatial challenge: alpha versus alpha-prime

Figure3 provides21 paired recordings across four KC drivers, with thermal stimulation and GCaMP3. Applying the already-frozen shared coefficient gives:

| Model | New-assay MSE |
|---|---:|
| Shared scalar, equal observation gains | 1.444396 |
| Two local regions, zero transfer | 0.040157 |
| Two local regions, frozen shared q | 0.036414 |

The shared-q local model lowers error by97.48% relative to equal-site scalar prediction. Stratified recording-bootstrap95% interval for the MSE difference is[0.811291,2.093217]. However, it improves over zero by only9.32%; that does not meet20%. The new scalar comparator has equal gains because Figure4's calyx/lobe gain ratio cannot be assigned to alpha/alpha-prime. This challenge therefore does not test every scalar observation model or establish a transferable q.

### Independent spatial observations limit generalization

All three stimulation sites from Figure7 were extracted without fitting or exclusions. Values below are published within-assay normalized fluorescence means; different modalities/preparations are not paired with each other.

| Stimulated region | APL calcium: calyx / horizontal / vertical | KC odor-response change: calyx / horizontal / vertical |
|---|---|---|
| Horizontal | 0.0365 / 0.7236 / 0.5137 (n10) | −0.1421 / −0.4821 / −0.2712 (n10) |
| Vertical | 0.0142 / 0.0029 / 0.7031 (n10) | −0.1721 / −0.3761 / −0.4469 (n10) |
| Calyx | 0.6858 / 0.0152 / 0.0032 (n6) | +0.2228 / −0.3281 / −0.2877 (n9) |

Horizontal stimulation produces substantial vertical APL activity in this protocol. KC effects can extend well beyond sites with strong measured APL calcium, and the calyx condition even has a positive mean at the calyx. Thus neither universal zero transfer nor copying calcium coefficients into inhibitory conductance is defensible. No parameters were changed to accommodate these observations. Source and protocol differences are detailed in [EVIDENCE.md](EVIDENCE.md).

## 3. Temporal prediction and the MBON workbook audit

The original five MBON14 time constants predict a population mean of16.056ms. The four supplementary EGFP cells give a diagnostic RMSE of5.420ms. **This is not accepted independent validation.**

- Listed tau values average16.9825ms, while the workbook reports14.48ms.
- One row's Vm/tau/capacitance/specific-capacitance values match a training-table cell.
- Other displayed means are also inconsistent. Numeric strings were parsed without dropping rows.
- The inspected authoritative article/figures/source link do not resolve cell provenance or the discrepancy; raw repository access failed. No correction was inferred.

[MBON_SOURCE_AUDIT.md](MBON_SOURCE_AUDIT.md) preserves the exact source problem and disposition. Excluding a suspicious row cannot establish independence, so the earlier exclusion sensitivity does not rescue validation. MBON14/alpha3 is not alpha-prime3 or MBON07/11.

The article's compact dendritic integration result is model-supported and concerns a particular output question. Its experimental somatic voltage traces also display fast and slower components. A full waveform may need more than one state even when integrated output is well approximated simply. The paper's illustrative two-RC constants are not newly measured parameters. No held-out waveform MSE was fabricated from a published simulation or image.

The analytical temporal test shows that a scalar and a uniformly driven two-compartment model can share an identical common-mode response despite different coupling: maximum discrepancy≤1.7×10^-16 in the numerical demonstration. A single measured tau therefore cannot select compartment number. Alpha-beta-core KC A-current measurements add subtype-specific voltage/kinetic constraints, but no complete independently validated R3 kernel follows. [TEMPORAL_CONDITIONING.json](TEMPORAL_CONDITIONING.json) records these calculations as mathematical tests, not biological recordings.

## 4. Conditioning, local dopamine and recovery

Independent physiology supports **DAN activity → local modulation → eligible synapses → persistent local state** as a useful separation. It does not numerically identify release/diffusion, receptor maps, eligibility time constants or contact-to-modulation gains.

The gamma1pedc current endpoint constrains integrated depression H=2.302585 under an exponential surrogate. Learning rate and integrated dopamine/eligibility exposure remain rank1-of2 identifiable:101 illustrative factor combinations reproduce the endpoint within3×10^-17. These are equivalent mathematical explanations, not biological parameter estimates.

Gamma4 forward(+0.5s) and backward(−1.2s) pairing measurements and receptor perturbations contradict a **universal monotonic LTD-only rule**. That incompatibility holds whether neurons are scalar or compartmental. It does not identify the correct numerical bidirectional rule for alpha1 or gamma1pedc. Compartment-dependent ACh release supplies additional mechanistic evidence; its linked raw-data endpoint was inaccessible in this audit. No invented numerical conditioning score or new fit is substituted.

Alpha-prime3 familiarity/recovery constrains experience-dependent local processes, but “recovery by one hour” is not a measured exponential tau. Hypothetical1%,5%,10% remaining-response criteria imply different taus (782/1202/1563s), illustrating the unidentifiability. These numbers are not fitted recovery constants. The current evidence does not resolve postsynaptic receptor traffic, presynaptic release, electrical state and fluorescence dynamics into one unique model.

## 5. R0/R1/R2/R3 comparison

| Criterion | R0 scalar | R1 local states | R2 local + target/receptor | R3 biophysical |
|---|---|---|---|---|
| Spatial prediction | Tested APL fixed-gain model inadequate | Strong narrow APL advantage; regional/protocol transfer limited | No additional held-out numerical fit | No additional held-out numerical fit |
| Temporal prediction | Plausible coarse output for some cells; full waveform not established | Can express multiple timescales; parameters unidentified | Biochemical time scales unresolved | Subtype channel constraints available, full kernel unvalidated |
| Conditioning | Scalar electrical state can coexist with local synaptic memory; global LTD-only insufficient | Location separation alone does not identify learning | Receptor-dependent directionality supported in specific assays | More conductances do not resolve missing release/plasticity data |
| Identifiability | Gain/threshold/normalization/observation confounded | Coupling and timescales unresolved; zero transfer competes | Root-specific receptor/dose map missing | Many more unknowns; no complexity justification from held-out data |
| Robustness | Fails tested APL spatial observation | Advantage over shared state survives spatial challenge; fitted nonzero transfer not robustly necessary | Qualitative support, not a quantified robust kernel | Not adequately testable with acquired measurements |
| Complexity | Least electrical state | Add only justified regions | Separate state kinds and canonical plasticity owner | Only where measured and needed |

**No common numerical winner is identified.** Local biochemical state need not mean multiple membrane voltages. A future heterogeneous model is more defensible than imposing the same representation on every neuron, but has not reached the original freeze-and-replay gate. [IDENTIFIABILITY.md](IDENTIFIABILITY.md) and [REPRESENTATIONS.md](REPRESENTATIONS.md) give equations, assumptions and comparison limits.

## 6. Computational feasibility

Fifteen fresh-process engineering benchmarks use the exact pinned Stage1/2/3, integrated-L3 and full-reference anatomy. Every update traverses real retained connectivity; local-state and candidate KC→MBON plastic buffers are explicitly counted. These benchmarks define stable arithmetic workloads, **not** calibrated biological dynamics. Their synthetic engineering inputs/output must not be presented as neural replay.

| R2 workload | Roots / local states | Anatomical rows / contacts | Candidate plastic rows | Updates/s | Peak RAM | Dynamic checkpoint |
|---|---|---|---:|---:|---:|---:|
| Stage1 circuit | 1,054 / 7,670 | 102,889 / 226,143 | 5,675 | 2,527.8 | 411.7MiB | 0.321MiB |
| Stage2 circuit | 1,172 / 7,503 | 73,715 / 160,848 | 4,533 | 2,389.5 | 415.2MiB | 0.298MiB |
| Stage3 circuit | 4,563 / 29,777 | 375,699 / 905,536 | 22,878 | 602.3 | 421.8MiB | 1.258MiB |
| Integrated context | 37,913 / 229,679 | 6,696,367 / 22,458,018 | 89,315 | 61.9 | 494.3MiB | 8.373MiB |
| Full reference | 139,255 / 435,774 | 16,847,997 / 54,492,922 | 89,315 | 13.7 | 1,040.2MiB | 14.663MiB |

These are pair/neuropil rows, not directed-pair counts. The Stage1 circuit still has80,423 directed pairs. R0 CSR coalesces rows by neuron pair, while local-state rows remain distinct. R2 uses illustrative receptor/modulator/eligibility/efficacy operations, with no claimed physiological parameters. Unknown receptor maps are not populated from cell names.

For full reference, R0/R1/R2 achieved35.1/22.9/13.7 updates/s. At a hypothetical1ms step the R2 workload is~73times slower than real time; this is a workload estimate, not a validated integration step. Integrated R2 is~16times slower. Small circuits are inexpensive. Fifteen deterministic replays/checkpoint reloads were exact. Full R2 initialization took39.72s,100 updates7.30s, checkpoint write/load16.1/17.7ms. Immutable anatomy must be retained separately from dynamic checkpoints.

Peak RSS includes full-source loading, metadata and temporary construction arrays, so small-circuit peaks overstate minimal resident state. Host load and one-run timing limit precision. No R3 throughput claim is made without an operator. [SCALING.md](SCALING.md) provides all15 cases, CPU, replay/storage costs, state formulas and explicit R3 storage scenarios. The older scalar benchmark is not evidence for richer calibrated real-time physiology.

## 7. Unified identity without unsupported physiology

The identity-only audit finds5,480 unique roots and449,600 unique aggregate anatomical rows in the union of existing extraction records (1,056,073 contacts). This is not a newly induced unified connectome. It verifies **4,622 KC→MBON07 and1,053 KC→MBON11 shared rows** have one canonical identity/count; no count conflicts occur. It assigns zero physiological rules.

One root string owns multiple optional local states. Each canonical anatomical row owns one plastic state per alternative model; experimental views reference it instead of duplicating it. Individual contact IDs cannot be fabricated from aggregate counts. Shared identity does not reconcile the frozen conflicting normalizations, dopamine projections, acute gating and update rules. Those conflicts still block a unified kernel. See [IDENTITY_SCHEMA.md](IDENTITY_SCHEMA.md) and [IDENTITY_AUDIT.json](IDENTITY_AUDIT.json).

## 8. Implications and remaining evidence

The minimum defensible next representation is a **research design constraint**, not a selected Genesis brain: support heterogeneous local state, explicit observation models, target-specific unknowns, and unique neuron/synapse identity. Do not require multiple electrical states everywhere. Do not infer nonzero coupling, receptor maps, transmitter sign, dopamine dose or learning kinetics from the need for local state.

Discriminating models requires independently held-out, preparation-matched recordings of localized stimulation and local/remote voltage/calcium, calibrated transmission, compartment-resolved dopamine/receptor response, and conditioning/recovery trajectories. These would test whether extra states improve unseen biological predictions enough to justify their complexity. More neurons or larger Genesis effects cannot substitute for those measurements.

## 9. Preservation and stopping point

All3,768 protected pre-study files and12 interrupted-study files are checked unchanged. Thirty Stage1/2/3 tests, eight frozen physiology tests and ten new study tests pass. The canonical audit retains the previous database hash, seven life cycles and disabled schedule. The final preservation artifact records before/after equality and per-file hashes. No canonical cycles, runtime activation, C. elegans edit, wallet/LLM/planner integration or Stage4 occurred.

**Final: INSUFFICIENT EVIDENCE TO SELECT REPRESENTATION.** Narrow APL local-response support is retained; nonzero coupling and a general physiological kernel remain unidentified. Stop for review.

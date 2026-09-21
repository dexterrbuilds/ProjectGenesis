# α1 → UpWiN Minimal Transfer Identifiability Study

## Finding and scope

**STAGE-5 DESIGN POSSIBLE UNDER EXPLICIT TRANSFER UNCERTAINTY**

This decision permits consideration of a **conditional model-identification or robustness question**, not a calibrated biological propagation claim. Stage 5 remains unauthorized and no protocol is designed here. A calibrated α1→UpWiN transfer is not necessary for every meaningful order/sensitivity question. It **is** necessary to identify physical voltage/timing predictions, or must be replaced by sufficient independent bounds. Neither calibrated transfer nor useful unconditional physiological bounds are available here.

The evidence-admissible family includes null, reversed-order, saturated and alternative-input explanations for the hypothetical recall target. Therefore it supplies **no guaranteed nonzero signed downstream effect**. A future result could be scientifically valid as a conditional model result, a partial identification set, or a demonstrated failure of robustness. It could not establish biological action bias merely because a selected transfer produced one.

The prior route studies' classifications are unchanged. Their question concerned an identified biological route; this analysis asks a different question about explicitly uncertain mathematical transfer families. No target identity, receptor sign or mediation link is newly established.

## Frozen evidence and observation domains

Inputs were limited to Brain Spec v0.2, the accepted Stage-1 package, the route-acquisition package and the identity/mediation package. Their hashes are in `DEPENDENCIES.json`. No new literature or dataset was acquired. No Stage-1 code, neural dynamics, optimizer, decoder or Genesis runtime was executed.

| Domain | Observable | What cannot be imported into it |
|---|---|---|
| Frozen Stage 1 | Dimensionless model activity/plastic state | Physical firing rate, current, mV, photostimulation equivalence |
| α1 conditioning, MB319C / MB043-split-LexA | Odor-evoked spike counts in a separate α1 preparation | SS67249 voltage, matched animal identity, rate→mV gain |
| R64A11-LexA acute physiology | Baseline-subtracted somatic voltage after α1 photostimulation | A pure SMP353/SMP354 target population or receptor mechanism |
| R64A11 population imaging | GCaMP6s population fluorescence in dissected brain | Voltage, spike rate, individually identified target response |
| SS67249 recall | Within-record pre/post odor-evoked voltage, 0–1.2 s | R64A11 responder assignment, isolated α1 contribution |
| SS33917 behavior | Assay-specific wind-relative movement | SS67249/R64A11 voltage-to-movement function |
| SS33918 behavior | Separate driver-scoped movement | Equivalence to SS33917's exact cells/physiology |
| Individual FAFB roots | Pinned anatomical identity and contacts | A recording identity, conductance or somatic transfer |

`OBSERVATION_MATRIX.json` retains these domains and all 36 pairwise compatibility assessments among its nine preparation entries (including the separate intervention domain). Same-row pre/post comparison is compatible. Direct pooling of calcium with voltage/spikes is incompatible without an observation mapping. Acute/recall voltage sharing requires a population/state compatibility assumption despite common units. Anatomy motivates candidates but does not identify the transfer. Within-assay behavioral intervention/control comparisons remain valid only at their own endpoint and preparation.

Four latent bridges remain explicit and unset: population identity, Stage-1-to-biological-state correspondence, exclusion/fixing of alternative inputs, and observation-model compatibility. They are hypotheses, not fitted facts.

## Quantitative constraints that actually exist

### Acute voltage and response heterogeneity

The frozen report identifies negative somatic responses in **4 of 17 sampled R64A11 cells**, from **12 reported flies**. The finite reported detection fraction is **0.235294**. Thirteen reported nonresponders remain in the evidence; they are not replaced by zero-gain neurons. All seventeen individual trace summaries and numeric trace hashes are retained by reference in `OBSERVATIONS.json`.

For the four reported responders, full-trace minima are −3.590462, −1.201149, −4.240583 and −2.571013 mV. These are descriptive extrema over the existing trace horizon, **not stimulus-aligned response amplitudes, threshold estimates, or gain calibration**. The grids contain 15,001 points at approximately 0.1 ms intervals over 1.5001 s. Their original event-onset and baseline-window fields remain unknown. A 10 ms light pulse is not a measured 10 ms neural input.

There is no justified population confidence interval for the underlying responder probability: cell sampling, detection sensitivity and within-fly clustering are unresolved. Even an otherwise justified binomial interval for detectable responses would not identify anatomical connectivity or synaptic responsiveness.

### Recall, with reciprocal odors kept separate

| SS67249 cohort | Source rows | Paired mean change, mV | Control mean change, mV | Mean within-row difference of changes, mV | Observed range of that contrast, mV |
|---|---:|---:|---:|---:|---:|
| OCT paired | 6 | +3.087502 | +0.093445 | +2.994058 | 1.949709 to 4.000426 |
| MCH paired | 5 | +2.334003 | +0.457808 | +1.876195 | 0.861832 to 3.703730 |

The contrast is `(paired post − paired pre) − (control post − control pre)` within each published row. All eleven observed contrasts are positive. These arithmetic observations are identified; their population expectation and α1-mediated component are not. Descriptive contrast SEMs are 0.363646 and 0.511975 mV across source rows, respectively. No new significance test, fly-independent interval or held-out split is claimed.

Separate upstream α1 conditioning data show paired-odor mean spike-count reductions: OCT 74.066667→19.560000, MCH 62.040000→20.264000. These are **spike counts in another preparation**, not matched input observations for the voltage table. Dividing either voltage change by either spike-count change would manufacture a transfer. No such ratio is calculated.

The calcium coactivation observation supplies a qualitative population interaction in its own assay. It does not determine a voltage kernel or an individually recorded receptor sign. Behavioral activation and blockade remain separate downstream evidence. Chronic TNT does not isolate recall; restrictive-temperature shibire does not validate an upwind endpoint when the control behavior is absent.

## Identifiability table

The classification always applies to the named estimand, not to a broader biological claim. `IDENTIFIABILITY.json` contains the complete scoped table and a counterexample reference for every row.

| Quantity | Classification | Scope / limiting ambiguity |
|---|---|---|
| Reported sample responder fraction | IDENTIFIED | Exactly 4/17 labels; not population probability |
| Acute negative response direction | QUALITATIVELY CONSTRAINED | Four sampled cells at the recorded protocol |
| Direct or general α1-state transfer sign | NON-IDENTIFIABLE | Direct versus indirect action; operating range; target/state correspondence |
| Monotonicity | NON-IDENTIFIABLE | One intervention protocol does not identify a neural input-response curve |
| Biological responder fraction / membership | NON-IDENTIFIABLE | Selection, detection and clustering |
| Finite recorded voltage summaries | IDENTIFIED | Original units/windows; no input calibration |
| α1→UpWiN gain / amplitude scale | NON-IDENTIFIABLE | Hidden input scale, even with known mV output |
| Intermediate output under an assumed monotone endpoint map | BOUNDED | Mathematical endpoint bound only; requires an unverified restriction |
| Downstream latency | NON-IDENTIFIABLE | Unmeasured source/opsin/observation delays and onset metadata |
| Temporal kernel | NON-IDENTIFIABLE | Unidentified factorization of composite response |
| Saturation | NON-IDENTIFIABLE | Missing neural-state dose response |
| Detected heterogeneity | IDENTIFIED | Four response labels versus thirteen nonresponse labels |
| Mechanistic heterogeneity | NON-IDENTIFIABLE | Cell type, gain, noise, state and detection confounded |
| Finite conditioning-associated changes | IDENTIFIED | Paired scalar rows and reciprocal controls |
| Conditioning-dependent change in transfer | NON-IDENTIFIABLE | Input change versus gain change versus alternative input |
| A single transfer for acute and recall | NON-IDENTIFIABLE | Common and separate transfers can both explain the separate domains |
| Disinhibition as recall mediator | NON-IDENTIFIABLE | α3/β1/other-input and population alternatives remain |
| Saved Stage-1 scalar ordering | IDENTIFIED | Six frozen intact counterbalanced runs have paired post < pre |
| Physical downstream order | NON-IDENTIFIABLE | Family contains preserved order, reversed order and ties |

There are **no identified numerical physiological transfer parameters**. Unknown entries are null; zero appears only as an explicitly hypothetical mechanism, never as a replacement for missing evidence.

## Minimal transfer classes

The parent class is domain-specific `y_d = F_d(x_d,z_d,t)`, with unmeasured input and context. It expresses missing information; it is not a predictive model. Four useful restrictions/decompositions answer the identification questions without building a neural system:

1. **Monotone sign-only:** a nonincreasing transfer reverses weak order if the target and source correspondence are fixed and other inputs are fixed. These are assumptions. Flat regions allow ties.
2. **Linear versus saturating monotone:** both can satisfy the same endpoint evidence; no data-driven family selection is justified. A bounded variant supplies only conditional endpoint bounds.
3. **Heterogeneous response/detection mixture:** preserves responders and nonresponders without equating detection with zero/positive anatomical efficacy.
4. **Latent disinhibition versus alternative input:** `Δy_d = g_d Δx_d + Δz_d`. This is an identifiability decomposition, not a physiological equation selected for use.

No class was selected or fitted. A complexity penalty cannot resolve unknown stimulus-to-neural input, unidentified observation maps or cross-driver correspondence. Comparing likelihoods after silently assigning these would compare different assumed problems.

## Counterexamples and degeneracies

### Sign and monotonicity

For a normalized intervention coordinate `u`, the two constructions

`x=u; y=−x`

and

`x=u; z=u; y=+x−2z`

both give the same negative total intervention response `−u`. The direct partial derivative with respect to x has opposite signs. This does **not** overturn the observed negative intervention response. It overturns the inference from that response to a direct receptor/transmission sign.

Even granting two known neural-state endpoints, `f_c(x)=−x+c x(x−1)` agrees at x=0 and x=1 for every c. With c=4 its derivative changes sign. A finite negative endpoint response therefore does not establish monotonicity or the local sign around a different recall state.

These examples extend to complete observed waveforms by using each waveform as a fixed coefficient at the measured endpoint. No synthetic trace is presented as new data. The constructions demonstrate missing constraints; their latent terms are not claimed anatomical partners or independently supported physiology.

### Gain, saturation and time

`x*=k x; g*=g/k` leaves `g x` unchanged for every positive k. Arithmetic checks at k=0.01, 1 and 100 give the same normalized output 0.5. These are mathematical coordinates, not physiological ranges.

`−x` and `−(1−exp(−x/s))/(1−exp(−1/s))` agree at the normalized endpoints but differ in saturation. For illustrative s=0.1, 1 and 10, the saturation asymptotes are approximately −1.000045, −1.581977 and −10.508332; the linear alternative has no finite asymptote. Data at those endpoints cannot choose among them.

A composite light→voltage response factors into opsin/source drive, neural transmission and measurement dynamics. Exchanging two convolution factors leaves the composite unchanged but changes which temporal constant belongs to the target. Thus even a perfectly identified composite kernel would not automatically identify the neural kernel. No 50 ms Stage-1 constant, Gaussian smoothing width or sampling interval is transferred downstream.

### Responders and disinhibition

In an illustrative independent-detection model, only `p×d` enters the detected-response probability: `(p,d)=(4/17,1)` and `(1,4/17)` are observationally equivalent. The independence assumption itself is not justified for the real sample. The point is that detection fraction does not identify biological responder fraction even under that stronger simplification.

For recall, `Δy=g Δx+Δz` permits negative g with reduced x, zero g with an alternative input change, or positive g with a compensating alternative input. Every paired and control change in both odor cohorts can be preserved. The separately measured α1-conditioning, calcium and behavioral observations remain unchanged in their own domains.

This is a saturated nuisance construction demonstrating non-identification, **not a fitted alternative biological pathway**. It does not establish that all alternatives are equally plausible. It establishes that the present observations do not distinguish them.

There are 22 within-row pre/post changes across the eleven recall rows and two odors. Even if Δx were known, one shared gain plus one nuisance change per observation gives 23 unknowns for 22 equations. The Jacobian `[Δx | I]` has rank 22 and at least one null direction. Actual Δx and cross-domain identity are also unknown. The unrestricted α1-attributed component has no finite evidence-derived bound. This is a formal identification set, not a claim of physically unbounded membrane voltage. A [0,1] attribution fraction would require an extra nonnegative, non-cancelling additive-components assumption.

### Attempts against identified claims

Changing hidden gain, source scale or target identity while holding the actual labels/rows fixed cannot change 4/17, the finite arithmetic voltage summaries, or the saved Stage-1 inequalities. The counterexample attempt fails for those **descriptive** claims. It succeeds as soon as they are promoted to a population expectation, physical transfer or mediated contribution. This is why the identified entries remain narrowly scoped.

## What crosses the Stage-1 firewall?

Read-only inspection of the six frozen intact runs confirms paired post-training activity below its own baseline in the same saved appetitive readout. For a strictly increasing transformation h of that scalar, `r_post<r_pre` implies `h(r_post)<h(r_pre)`. This order invariant does not need gain or units.

It does not establish that physical α1 state is an increasing transformation of that model readout. Nor does it preserve effect-size ratios, differences of changes, or population means after arbitrary neuron-wise nonlinear transformations. It supplies no biological time, photostimulation equivalent or downstream sign.

For an ordered source pair, `f(x)=x`, `f(x)=−x`, and a constant transfer respectively preserve, reverse and erase the downstream difference. Recall target identity and context uncertainty allow these alternatives without contradicting the acute sampled-cell evidence. Consequently the full admissible family gives a set-valued downstream order, not an identified signed response.

## Design sufficiency under uncertainty — requirements, not a protocol

### What can be meaningful without calibrated transfer?

- **Ordinal neural comparison:** a fixed model readout can retain order without physical calibration. It must remain a neural scalar comparison, not a semantic preference or a newly weighted decoder output.
- **Sign/order questions:** conditional results are possible if source ordering, target correspondence, transfer direction, non-flat support and fixed alternative inputs are explicitly assumed. A sign built into the assumed transfer cannot be presented as an experimentally discovered sign.
- **Bounded perturbations:** the existing data delimit observed protocol settings and recorded outputs in those assays. They do not bound hidden α1 input or responses in another population. A future analysis must distinguish measurement-supported bounds from chosen coverage ranges.
- **Unknown-family sensitivity:** mathematical robustness and non-robustness are meaningful research outcomes. Parameters must not be chosen because a downstream result appears. A finite sweep of arbitrary ranges cannot establish robustness over an unbounded admissible family.

### Minimum information and governance

A future prospective design needs a precise resolution and neural estimand; a documented observation domain; explicit identity/state/exclusion/observation bridges; declared transfer families including null and opposite-sign alternatives where unresolved; a distinction between biological bounds and engineering coverage choices; and a predeclared conditional versus invariant claim.

Before downstream outputs are accessible, freeze evidence hashes, family definitions, assumption partitions, observation maps and reporting rules. Keep parameter selection blind to downstream values. Any independently authorized physiological calibration must use only its biological measurements with Stage-1/Stage-5 outputs inaccessible to the fitting process. Report every admitted branch, including nulls and failures; do not pick the strongest branch or a favorable normalization. New evidence that excludes a branch requires separately reviewed versioning.

This is a governance boundary. No network, stimulus sequence, parameter grid, decoder, or Stage-5 acceptance threshold is specified here.

### Validity and failure conditions

A claim valid over a restricted family must hold for **every** admissible parameter, latent input and bridge choice in that declared family, or be reported as a conditional identification set. Strict downstream order requires a non-flat monotone map and a relevant responder; weak monotonicity alone allows equality. The full evidence-admissible family permits no universal nonzero signed effect. Reporting that lack of robustness is a valid result.

An unconstrained nuisance term that can explain any output makes biological mediation unfalsifiable. Restricting it prospectively can make a conditional mathematical hypothesis test meaningful, but does not make that restriction a biological fact. Positive biological propagation, absolute voltage/timing prediction and attribution to α1 would still require targeted identifying observations.

A future study becomes uninterpretable if it pools driver populations, treats nonresponders as zero edges, imports Stage-1 gain/time into physical units, converts calcium/spikes to voltage without a map, chooses a family after seeing desired output, omits null/reversed branches without declaring the exclusion, or claims an arbitrary finite sweep covers all uncertainty. The same applies if it erases the failed upwind control or treats chronic TNT as recall-specific mediation.

## Artifacts and preservation

Machine-readable outputs: `IDENTIFIABILITY.json`, `OBSERVATION_MATRIX.json`, `TRANSFER_CLASSES.json`, `COUNTEREXAMPLES.json`, `DEGENERACY.json`, `STAGE1_FIREWALL.json`, `OBSERVATIONS.json`, and `DESIGN_SUFFICIENCY.json`.

`validate.py` checks dependency integrity, the arithmetic witnesses, all **9,147 protected files**, and preservation of canonical state. It contains adversarial tests against unsupported parameter/sign promotion, cross-domain joining, unit leakage and Stage-5 authorization. `VALIDATION.json`, `TEST_LOG.txt` and `RELEASE.json` record the final checks and seal this separate package. Canonical Genesis remains at seven cycles with the schedule disabled.

No scientific result or classification in a prior package is revised. This study identifies which future questions can be meaningful under explicit uncertainty; it does not authorize their execution.

**STAGE-5 DESIGN POSSIBLE UNDER EXPLICIT TRANSFER UNCERTAINTY**

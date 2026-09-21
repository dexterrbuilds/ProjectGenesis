# α1/MBON07 → UpWind Neural Route Evidence Acquisition Study

## Decision

**PARTIAL ROUTE SUPPORT — TARGETED EVIDENCE STILL REQUIRED**

A real anatomical route and preparation-specific physiological/behavioral observations support continued evidence acquisition. The chain is not resolved from **the particular modeled MBON07 root → an identified responding UpWiN → a compatible action-related measurement**. The principal barriers are target identity/sign, cross-preparation observation mappings and incomplete raw-data/identity metadata. Stage 5 remains unauthorized; no protocol, model, simulation, decoder or parameter fitting was performed.

This study depends on Brain Spec v0.2 registry SHA-256 `23efaa1a65cc7fe7ed49c3e17e90f1c9f1bc55ae11cbce77519cfe20eba44f88`, package SHA-256 `9322ea0f3c501b6bd29add73464c94b775fb616648801e7f945346776b9bdd0b`. The existing spec and previous classifications are unchanged. `DEPENDENCIES.json`, `SPEC_VALIDATION.json`, `FROZEN_BEFORE.json` and `VERIFICATION.json` record dependency validation and preservation.

## 1. What was acquired

The [primary α1/UpWiN study](https://elifesciences.org/articles/85756) and its [complete figure/source-data page](https://elifesciences.org/articles/85756/figures) yielded 36 original v3 workbooks, including every linked Figure 1, 4, 5, 6 and 7 source/supplement dataset. All source files are hashed and CRC-checked. Lossless populated-cell exports retain original workbook cell provenance and unknown metadata.

The separate [α1 conditioning study](https://elifesciences.org/articles/79042/figures#fig3s2) supplies original upstream spike-response data and a hemibrain identity/connectivity table. That evidence was audited separately rather than combined numerically with UpWiN voltage. [SOURCE_AUDIT.md](SOURCE_AUDIT.md) documents all preparation, driver, unit, baseline, time, repeated-measure and exclusion limitations, plus source inconsistencies. `MEASUREMENT_AUDIT.json` and `ALPHA1_CONDITIONING_AUDIT.json` contain individual scalar observations and descriptive reconstruction results.

## 2. Anatomy and crosswalk

### Identity evidence

- **Source:** frozen Stage-1 appetitive class α1 / MBON07; starting FAFB root `720575940617302365`, left hemisphere. Four MBON07 roots exist in the pinned annotation (two per side); a recording from another animal is not identified with one of these roots.
- **Candidate target:** SMP353 root `720575940608236978`, left. Published hemibrain SMP353 body **424443911** is shown in Figure 3 supplement 1 and independently listed in Yamada Supplement 1. The right FAFB annotation also contains SMP353 `720575940633583712`.
- **SMP354:** the pinned annotation explicitly maps **CB3112** to hemibrain type **SMP354** on six roots (three per side). The paper's three hemibrain bodies are **389307767, 390003153, 5813010748**, verified against the image and source table. This establishes a type-alias candidate crosswalk, **not one-to-one homology or responder/driver membership for each FAFB root**.
- The paper's broad UpWiN population contains 11 hemibrain neurons across five types: SMP353, SMP354, SMP348, SLP399 and SLP400. Its anatomical matching used manual morphology and NBLAST/MCFO. R64A11 whole-cell sampling is broad; SS67249 recall sampling is stochastic and includes off-target cells. The 14-root anatomy audit below is not the full experimental driver population and is not claimed to close its physiology.
- Hemibrain analysis uses right-side connectivity; our starting pair is left-sided in a distinct female FAFB specimen. Type annotations and mirrored morphology do not transfer a physiological gain, sign or local electrical compartment.

[CROSSWALK.json](CROSSWALK.json) records every candidate root as a string, aliases, source-body IDs, confidence and explicit unknowns. No canonical anatomical ownership is duplicated.

### Counts and boundary retention

Read-only static analysis used **FAFB materialization 783, annotation v3.1.0**, the frozen proofread graph with 139,255 neurons, 15,091,983 directed pairs and 54,492,922 contacts. All input/output denominators use this same graph. No contact is fabricated, and absent aggregate graph edges are not declared physiologically impossible.

| Audit set (not a model extraction) | Neurons | Directed pairs | Contacts | Omitted incoming / outgoing contacts |
|---|---:|---:|---:|---:|
| Starting MBON07 and SMP353 pair | 2 | 1 | 11 | 7,446 / 1,661 |
| All annotated MBON07, SMP353, SMP354-alias and SMP108 roots | 14 | 47 | 751 | 47,781 / 21,180 |

The **11 starting contacts** comprise **4 SMP_L + 7 SLP_L**. They are **0.889% of the source's 1,238 outputs** and **1.477% of the target's 745 inputs**. In the two-root denominator, MBON07 retains none of its own 6,712 inputs and SMP353 none of its 434 outputs. These zeros describe the deliberately tiny audit set, not missing physiology replaced with zero.

Within the 14-root typed denominator, the starting MBON07 retains **0.745% input / 7.027% output** and starting SMP353 **2.819% input / 11.521% output**. Across SMP354 candidates, input retention ranges **3.205–20.034%** and output retention **7.674–20.106%**. All per-root exact totals and major omitted partners are in [ANATOMY_AUDIT.json](ANATOMY_AUDIT.json). No boundary currents, normalization or physiological closure are proposed.

### Convergence, divergence, recurrence and downstream routes

All annotated MBON07 roots together send **32 contacts to SMP353** and **196 to SMP354 candidates** in the pinned graph. The starting MBON07 also targets two left SMP354 aliases with **3 and 18 contacts**. The hemibrain Supplement 1 separately records α1 input totals of **67** to SMP353 and **268** to grouped SMP354; different specimen, inclusion and aggregation scopes prevent treating these as matching counts or replacing the pinned FAFB totals.

Starting SMP353 receives substantial additional LH/other input, including LHAD1b5 roots `720575940613953703` and `720575940608623371` (**18 each**), LHPV6a1 `720575940629326695` (**17**), and MBON13 `720575940645304430` (**16**). MBON07 is one input among many. Its output diverges to SMP108 `720575940631103744` (**48**), SIP029 `720575940622203350` (**40**), LHPV5e1 `720575940624155672` (**36**) and FB6D `720575940632732985` (**21**), among others. Anatomical name or mass is not an assigned function.

SMP353/SMP354 candidates have **13 internal directed pairs / 29 contacts**. Across both sides they send **279 contacts to SMP108** (131 from SMP353; 148 from SMP354). Some recurrent edges are very small; none is discarded merely because it is small, and no sign is inferred from count. Broad-population recurrence calcium evidence does not identify the sign of every one of these edges.

A complete direct-output scan for those candidate targets finds three descending-class edges: left SMP353→DNp44 `720575940627582724` (**3**), left SMP353→DNpe048/SMP367 `720575940646160948` (**2**), and right SMP353→DNp44 `720575940605725873` (**2**). These are **anatomical leads only**. No preparation-compatible action physiology for those particular routes was established here. They are not selected as motor endpoints. SMP108 has independent activation-linked upwind observations, but its learning/feedback evidence does not make it a necessary descending/action relay. FB/LH routes similarly remain candidates requiring specific functional evidence.

## 3. Four evidentiary layers kept separate

| Layer | Supported observation | What it cannot establish |
|---|---|---|
| Anatomy | Specific directed contacts, type aliases, neuropil distributions and recurrent partners | Synaptic sign, efficacy, transmission latency or behavioral function |
| Physiological transmission | α1 photostimulation yields inhibitory **Vm** responses in **4/17** broad-driver sampled cells from **12 flies**; α3 excitation in **3/11**, **7 flies** | Inhibition of every UpWiN, an identified SMP353/SMP354 receptor, monosynaptic current or a rate→mV operator |
| Conditioning-associated downstream activity | Reciprocal odor conditioning increases SS67249 sampled-cell odor-evoked **mV**, while controls change less | Isolated α1 causation, same-cell source-target transfer, or voltage→behavior conversion |
| Causal population influence on behavior | UpWiN driver activation changes wind-relative turning/walking; TNT and shibire affect their reported endpoints | A root-specific action command, preserved upstream learning under every intervention, voluntary choice or Genesis behavior |

The first-order α1 recording's spike suppression and UpWiN recording's increased voltage are compatible with a **disinhibition hypothesis**. Their conjunction does not numerically identify that mechanism. They use different neurons, drivers, odor concentrations, holding-current regimes and observation classes; the downstream conditioning driver also recruits β1. Simultaneous/otherwise identifiable mediation is absent.

Target-scoped receptor identity and sign remain **null** for the starting SMP353 root and SMP354 aliases. MBON07 glutamatergic identity is supported, but glutamate is not universally inhibitory. [Wang et al. 2026](https://www.frontiersin.org/journals/systems-neuroscience/articles/10.3389/fnsys.2026.1822122/full) discusses GluCl and synaptic spatial organization using general central-brain expression and anatomy; this does not supply receptor localization or recorded transmission at these particular synapses. No blanket GluCl conductance, diffusion, delay or sign rule is admitted.

## 4. Quantitative recall and control evidence

The following differences are descriptive, reconstructed from source paired rows—not a new experiment or fitted transfer:

| Source | Paired cue change | Unpaired cue change | Source rows |
|---|---:|---:|---:|
| OCT-paired UpWiN recall | **+3.087502 mV** | +0.093445 mV | 6 |
| MCH-paired UpWiN recall | **+2.334003 mV** | +0.457808 mV | 5 |

The mean/SEM scalar reconstruction succeeds to floating-point precision. Group waveform and calcium animal/trial data are missing, so numerical trace validation and identity-based holdouts cannot be reconstructed from SEM. Source `Fly` labels are retained without assuming external identities.

Population activation produces a mean area-normalized radial displacement of **0.009692** with no airflow, **0.147256** at +200 mL/min and **−0.086050** under reversed −200 mL/min airflow. Fed/starved means are **0.035009 / 0.122580**; intact/unilateral/bilateral arista means are **0.098400 / 0.031295 / 0.033862**. These context dependencies delimit the behavioral claim; they are not parameters for Genesis resource state or a movement-probability model.

Acute shibire testing cannot establish an acute upwind-route requirement: **controls failed to show CS+-induced upwind locomotion at restrictive temperature**. Only its separately measured binary odor endpoint is interpretable. Chronic TNT is relevant but does not isolate downstream expression from learning/consolidation. No complete intervention demonstrates this specific modeled source's learned signal propagating to an identified target while preserving all upstream learning and relevant unrelated sensory/locomotor function.

## 5. Preparation compatibility and data integrity

[PREPARATION_COMPATIBILITY.json](PREPARATION_COMPATIBILITY.json) explicitly covers Stage 1, fixed connectome anatomy, α1 stimulation, UpWiN population physiology, conditioning/recall, behavior, causal interventions and the separate upstream α1 recordings. It lists all 28 pairwise bridges, plus narrow within-assay direct matches.

- **DIRECTLY COMPATIBLE:** within-row pre/post scalar recall; stimulation and voltage in the same actual recording; intervention/control within the same declared behavioral assay.
- **TRANSFER REQUIRES ASSUMPTION:** anatomy-to-active preparation; broad/stochastic driver joins; separate upstream/downstream conditioning despite shared nominal odor/pulse timing.
- **INCOMPATIBLE for direct numerical composition:** uncalibrated Stage-1 rates with physical observations, or pooling dissected-brain calcium with somatic voltage/spikes/behavior without an observation model. This is not a claim that all future cross-preparation research is impossible.
- **UNKNOWN:** same-animal or identifiable neural-to-behavior links that are not available.

The audit preserves contradictory source color labels, Figure 4 fly-label/sample-count incompatibility, Figure 6 source/caption sample-count differences, orientation-bin wording and driver spelling differences. It does not repair them by dropping data or choosing a favorable interpretation. Source means are reconstructed where observations exist; elsewhere the gap is explicit. Recordings/flies are never counted from row order. Movie locators support potential movie-level independence, not individual-fly independence.

## 6. Ten readiness requirements

| # | Required evidence | Assessment |
|---:|---|---|
| 1 | Defensible source identity | Supported at α1/MBON07 class and pinned root level |
| 2 | Defensible target identity | Partial: anatomical type/alias supports candidates; physiological responder identity unresolved |
| 3 | Directional anatomy | Supported narrowly, with severe quantified surrounding-context omission |
| 4 | Target-scoped physiological sign | Unresolved for the required roots |
| 5 | Measurable downstream neural variable | UpWiN mV available, with baseline/event/raw-trial limits; calcium separate |
| 6 | Conditioning-compatible evidence | Partial; shared nominal schedule does not isolate α1 or join different preparations |
| 7 | Independent action-related variable | Driver/assay-level wind-relative kinematics supported |
| 8 | Causal intervention | Partial; no complete root-specific mediated route/control demonstration |
| 9 | Sufficient preparation compatibility | Not yet |
| 10 | Raw data for thresholds and holdouts | Partial; scalar values available, critical trial/animal/ROI/identity gaps remain |

## 7. Evidence needed next—not a Stage-5 protocol

A decisive improvement would require identification of responding/recall cells with the candidate anatomical homologs, target-specific sign/receptor evidence, original trial and animal metadata plus event/ROI/exclusion provenance, and preparation-compatible evidence linking α1-dependent learning to the downstream response. Relevant route intervention must distinguish downstream expression from impaired learning or general sensory/locomotor dysfunction. The observation relationship to a narrowly measured biological action quantity must be independently supported.

None of these missing quantities is supplied by a software assumption. No acceptance threshold, extraction proposal, stimulus schedule, fitting objective or experimental battery for Stage 5 is selected here.

Stage-1 success does not transfer its 50 ms time constant, normalization, synthetic input currents, dopamine mapping, eligibility duration, LTD floor/rate, sign assumptions or readout to UpWiNs. Shared canonical KC→MBON07/MBON11 rows remain single identities with unresolved non-composable physiological rules. No background drive is introduced to manufacture disinhibition.

## 8. Scientific boundaries and preservation

**BIOLOGICAL FACT:** source-scoped recordings, within-assay interventions and annotated contacts. **COMPUTATIONAL / ENGINEERING:** static graph arithmetic, source-data parsing and descriptive mean/SEM reconstruction only. **HYPOTHESIS:** the identified anatomical homologs mediate the proposed disinhibitory route under compatible physiology. **GENESIS PRODUCT MAPPING:** none.

There are no neural update equations, fitted coefficients, action labels or new capabilities in this package. Stage 1 and every earlier research classification remain frozen. C. elegans, canonical identity, seven decisions/life cycles, database and disabled schedule are checked byte-for-byte or by the existing read-only database digest. `RELEASE.json` content-addresses this acquisition package; it is not a Brain Spec amendment.

**PARTIAL ROUTE SUPPORT — TARGETED EVIDENCE STILL REQUIRED**

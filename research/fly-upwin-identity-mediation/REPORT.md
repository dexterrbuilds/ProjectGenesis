# α1 → UpWiN Identity and Mediation Resolution Study

## Decision

**PARTIAL ROUTE SUPPORT — TARGETED EVIDENCE STILL REQUIRED**

The additional source audit does not recover the identities of the four α1-responsive recorded cells, establish a target-specific receptor/sign for SMP353 or SMP354, or join the conditioning and behavioral preparations into one identified mediated route. This is an evidence gap, not a demonstration that the anatomical route is absent or nonfunctional.

Root-level identity is **not** a universal prerequisite for a legitimate biological study. Cell-type and experimentally defined population studies can be valid. Here, however, the limitation survives moving to population resolution: the acute physiology, recall physiology and behavioral interventions use different, incompletely registered populations. Treating their measurements as one continuous pathway would require assumptions that the available data do not resolve.

No Stage-5 protocol, neural dynamics, transmission fitting, action decoder or new capability was produced. Brain Spec v0.2 and the previous acquisition remain frozen.

## What this audit adds

- The original accepted-manuscript supplementary archive was independently inventoried: **57 entries**. All **36 source workbooks** were acquired and are **byte-identical** to their final-publication counterparts already audited in the previous study. They contain no additional raw-trial or recording-identity information.
- **Nine Figure-4/5 workbook containers** were inspected for document properties, embedded objects, images, comments and custom metadata. No cell-morphology/recording linkage was recovered. Spreadsheet creator/software metadata are not animal identifiers.
- Primary FlyLight records resolve the driver intersections. Independently registered microscopy specimens are available, but no linkage of those specimens to the physiological recording rows was found.
- The original Figure-5 morphology supplement was rendered and inspected. It identifies **SS67249 MCFO cells #1–#3** overlaid with SMP353 morphology. These are morphology-example labels, not the Figure-5 recording IDs or the Figure-4 responder identities.
- Peer-review history explicitly documents the unresolved disinhibition inference. An earlier source uses a stronger SMP353/354 caption for the same four α1 responders; it supplies no independent per-cell identification.

Reproducible inventories and original bytes are in `ARCHIVE_AUDIT.json`, `SOURCE_IDENTITY_AUDIT.json`, `SOURCE_MANIFEST.json` and `sources/`. Original files were not edited. The full archive download timed out; its original prefix, HTTP byte ranges and central directory were retained. The extracted members were validated against the archive's sizes and CRCs. Eleven PDF supplements and the key-resources DOCX were also recovered. Videos and the large TIFF were not extracted; they are not represented as raw physiological data.

## Identity resolution

| Evidence object | Resolution established | Mapping category | Limit |
|---|---|---|---|
| FAFB `720575940617302365` | Pinned MBON07 / α1 annotation | IDENTIFIED | Anatomical neuron; no experimental recording assigned |
| FAFB `720575940608236978` | Pinned SMP353 annotation | IDENTIFIED | Anatomical neuron; physiological target unresolved |
| Hemibrain ↔ FAFB candidate types | Existing audited type/alias correspondence | TYPE-COMPATIBLE | Distinct animals; no root-specific physiological transfer |
| SS33917 ensemble | Published LM–EM correspondence to SMP353, SMP354, SMP348, SLP399, SLP400 | TYPE-COMPATIBLE | Ensemble anatomy does not identify a patch-recorded cell |
| R64A11-LexA | Broad experimental UpWiN driver | IDENTIFIED at driver scope | Not a pure SMP353/SMP354 population |
| Four α1-responsive Figure-4 cells | Source columns P–S, individual mean traces | UNRESOLVED at type/root scope | SMP353/SMP354 remain POSSIBLE candidates, not assignments |
| SS67249 morphology examples | SMP353 resemblance | TYPE-COMPATIBLE | Does not identify any of the eleven recall recording rows |
| SS67249 SMP354 membership | No discriminating assignment recovered | UNRESOLVED | Neither established nor excluded |
| SS67249 off-target cells | Stochastic/off-target expression reported | UNRESOLVED identities | No inferred cell-type inventory |

All four responder records and eleven recall records have explicit null root, cell-type and recording-to-morphology fields in `SOURCE_IDENTITY_AUDIT.json`. Source labels are preserved as labels. They are not globally unique animal IDs: the Figure-4 source uses labels inconsistent with the reported twelve-animal total. No identity was inferred from row order. Pre/post pairing is supported within each published scalar row and by the authors' repeated-measure description; an external persistent cell identifier is unavailable.

### Driver intersections are not interchangeable

| Driver | Activation-domain hemidriver | DNA-binding-domain hemidriver |
|---|---|---|
| SS67249 | VT040580 | R64A11 |
| SS33917 | VT007746 | R64A11 |
| SS33918 | VT007746 | R66B12 |

These intersections are independently documented by [FlyLight SS67249](https://splitgal4.janelia.org/cgi-bin/view_splitgal4_imagery.cgi?line=SS67249), [SS33917](https://splitgal4.janelia.org/cgi-bin/view_splitgal4_imagery.cgi?line=SS33917) and [SS33918](https://splitgal4.janelia.org/cgi-bin/view_splitgal4_imagery.cgi?line=SS33918). R64A11-LexA is not equivalent to either split-GAL4 intersection simply because it shares an enhancer.

Stable microscopy specimens include `20200228_19_A10`, `20200228_19_A9`, `20200814_31_C3` for SS67249 and `20200904_19_F9` for SS33917. Objective, reporter, sex, age and slide labels are retained in the acquired driver pages. These establish specimen provenance, not the identity of the recorded cells. Registered image coordinates also do not identify an original patch target without an acquisition link.

**β1 requires separate treatment.** The documented conditioning confound is β1 DAN inclusion in **R58E02-LexA**, the reinforcement driver. It is not evidence that the SS67249 recorded cells are β1 cells. SS67249's off-target identities remain unresolved.

## Transmission: three different questions

1. **Presynaptic transmitter:** MBON-α1 has type-level glutamatergic evidence.
2. **Observed response:** the published current-clamp result is a negative somatic voltage response to α1 photostimulation in **4/17 sampled neurons from 12 reported flies**. It is not a measurement of inhibitory synaptic current. The other thirteen sampled neurons must remain part of the result.
3. **Identified postsynaptic mechanism:** no independently target-resolved receptor localization, transcriptomic assignment, paired recording or receptor perturbation was located that establishes the sign of α1 transmission specifically onto SMP353/SMP354.

Negative somatic voltage in a sampled cell is real evidence at that recording's scope. It does not identify its type, isolate monosynaptic transmission, establish GluCl involvement, or extend the observed sign to all UpWiNs.

The [79042 peer-review response](https://elifesciences.org/articles/79042/peer-reviews) labels the earlier data SMP353/354 and reports the same α1 counts, **4/17 cells, 12 flies**. It refers forward to the 85756 study. This is not an independent replication or a recording crosswalk. Its earlier α3 sample is **2/6 cells, 4 flies**, versus **3/11, 7 flies** in the final study. The final article explicitly says a selectively targeting SMP354 LexA line was unavailable. The final resolution boundary therefore remains broader than the earlier caption.

A request for GluCl antagonism in the earlier peer review was answered with forthcoming electrophysiology, not an identified-target receptor experiment. General Drosophila GluCl evidence, anatomical shunting hypotheses and later simulations using an SMP354 label do not supply that missing target-specific evidence.

## Mediation and memory phase

| Link or intervention | What is supported | What remains unresolved |
|---|---|---|
| α1 activation → sampled UpWiN voltage | Four sampled negative voltage responses | Type identity, receptor, monosynaptic mechanism |
| α1 + α3 coactivation → population calcium | Suppression relative to α3 activation in a separate imaging preparation | Equivalent effect of α1 inhibition during learned recall |
| Conditioning → SS67249 odor response | Paired-row voltage potentiation, reciprocal odor cohorts | Attribution specifically to α1 rather than β1/α3/other routes |
| UpWiN-driver activation → movement | Wind-related turning/locomotor effects and sensory-context controls | Same recorded target population, continuous neural-to-kinematic mapping |
| Chronic TNT → impaired learned behavior | Causal involvement over the chronic manipulation | Acquisition versus consolidation versus recall versus expression |
| Acute shibire → memory score | Recall-period binary-endpoint evidence | Validated upwind endpoint: required controls failed at restrictive temperature |
| α1 learned change → UpWiN recall → movement | Motivated hypothesis with separately supported links | A jointly constrained, identified mediated route |

The existing frozen recall audit retains OCT-paired mean changes of **+3.087502 mV** (paired odor) and **+0.093445 mV** (control), and reciprocal MCH-paired changes of **+2.334003 mV** and **+0.457808 mV**. These are preserved source-row summaries, not newly fitted values. They do not reveal which type changed or which learning compartment caused the change.

The [85756 peer-review record](https://elifesciences.org/articles/85756/peer-reviews) is decisive about the scope: reviewers requested a direct α1-inhibition-to-UpWiN test; the response permits alternative α3/input explanations and removes the stronger disinhibition wording. It does not supply the requested new direct intervention. This uncertainty predates Genesis and is not a negative conclusion inferred from model performance.

The prior SMP108 findings concern second-order reinforcement circuitry. They do not establish SMP108 as a necessary motor relay for first-order recall. No gain, delay, conductance, rate→mV or voltage→behavior conversion was fitted or composed here.

## Additional-data search and limits

`SEARCH_AUDIT.json` records the actual public title/DOI/type queries, primary sources inspected and search limitations. Public indexed repository searches did not locate a new linked trial/identity deposit. This is not a claim that no private or unindexed files exist.

| Requested material | Result |
|---|---|
| Figure-4 trial-level voltage | Existing individual cell-mean traces; no additional trials recovered |
| Figure-4 responder morphology | No recording-linked morphology recovered |
| Figure-5 raw repeated trials | Source representative/aggregate traces and paired scalar rows retained; no new trials |
| ROI masks and original event markers | No new deposited linked masks/logs recovered |
| Animal/cell identifiers | Workbook labels and independent morphology specimen IDs; no cross-assay joining key |
| Analysis scripts | Original paper links general FlyTracker/NeuTu/VVD Viewer tools; no study-specific raw-data/identity deposit established |
| Persistent behavioral tracks | Published summaries/examples retained; no new machine-readable persistent track identities recovered |

The source-data identity result is stronger than a filename comparison: all 36 accepted-manuscript workbooks match the final files by SHA-256. The original key-resources table adds reagent definitions, not recording identifiers. The MCFO supplement's three numbered examples cannot be matched to “Fly1,” “Fly2,” or “Fly3.”

## Ten readiness requirements

| Requirement | Classification |
|---|---|
| Defensible source identity | SUPPORTED |
| Defensible downstream target identity | PARTIAL |
| Directional anatomy | SUPPORTED |
| Target-scoped physiological sign | PARTIAL |
| Measurable downstream neural variable | SUPPORTED |
| Conditioning-compatible evidence | PARTIAL |
| Independently action-related biological variable | SUPPORTED |
| Causal intervention evidence | PARTIAL |
| Sufficient preparation compatibility | PARTIAL |
| Raw data for prospective thresholds and held-out validation | PARTIAL |

`READINESS.json` gives the evidence scope and reasons for each rating. The anatomical route remains real: the frozen starting-root pair has **11 contacts**, constituting **1.477%** of that SMP353 root's 745 incoming contacts. This count does not identify a responder or assign a physiological coefficient. No new extraction or boundary renormalization was performed.

## Separate resolution decisions

**Individual root — not justified for the requested route.** Pinned anatomy is available; individual experimental physiology is not registered to those roots. This does not invalidate type-level cross-animal neuroscience.

**Cell type — partial, not yet justified for the requested route.** Published morphology supplies candidate type correspondence, but the four responders and eleven recall records cannot be assigned to a common independently typed target. A generic type label cannot close that gap.

**Driver population — partial, not yet justified for the requested modeled route.** A standalone biological investigation of an explicitly specified driver population is scientifically legitimate. The existing assays establish narrow driver-scoped effects. They do not identify R64A11, stochastic SS67249 and SS33917/18 as one population with a common measured α1→recall→movement relationship. Lowering resolution must not erase these distinctions.

Prior complete proof of mediation is not required to design a hypothesis test. The remaining prerequisites here are independently specified targets and compatible observations/causal contrasts, not a guarantee of a positive result. The next evidence needed is a recording-to-morphology or independently typed target link; compatible α1-specific recall/perturbation evidence in that population; and linked trial/animal records with suitable controls. This report specifies evidence gaps only, not a Stage-5 protocol.

## Preservation and scope

`DEPENDENCIES.json` pins Brain Spec v0.2 registry `23efaa1a65cc7fe7ed49c3e17e90f1c9f1bc55ae11cbce77519cfe20eba44f88` and the prior route-study content hash `597e6c06bed21fda6ccf62959aacf83fda4aa7adc0f85fcd29453e5ac961f56c`.

The final validation checks all **9,012 protected files**, the unchanged canonical database digest, **seven decisions**, and the **disabled schedule**. The previous package's 15 validation tests passed before this audit. `VALIDATION.json` and `TEST_LOG.txt` hold the new checks; `RELEASE.json` content-addresses this separate evidence package.

Biological observations, anatomy, hypotheses and data-handling assumptions remain distinct. No Genesis product mapping or executable action label is introduced. No prior classification is changed. Stage 5 remains unauthorized.

**PARTIAL ROUTE SUPPORT — TARGETED EVIDENCE STILL REQUIRED**

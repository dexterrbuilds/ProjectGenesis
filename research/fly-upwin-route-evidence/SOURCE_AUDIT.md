# Source and measurement audit

## Scope and provenance

Primary source: Aso et al., *Neural circuit mechanisms for transforming learned olfactory valences into wind-oriented movement*, [eLife 85756, version of record](https://elifesciences.org/articles/85756), [figures and supplements](https://elifesciences.org/articles/85756/figures). Original v3 workbooks, article HTML, full figure-page HTML and the inspected Figure 3 supplement 1 image are preserved. The article identifies a Creative Commons Attribution license. Author-provided workbooks are preserved without editing. The acquisition log is a provenance record, not evidence of biological completeness.

All **36 linked source-data workbooks** from the main figures and supplements were acquired: **19,049,451 bytes, 1,546,417 populated source cells**. ZIP CRCs and SHA-256 hashes are recorded. `processed/*.json.gz` preserves source cell coordinates, exact underlying value text, parsed values, types and formulas. Empty formatting cells are not treated as observations. For example, Figure 4C declares `A2:I266935`, but has only 157 populated cells. The six numeric strings in the whole inventory are Figure 6B airflow labels, not discarded measurements. No error-typed source cells were found.

The additional [Yamada et al. eLife 79042](https://elifesciences.org/articles/79042) primary article, figure page, original Figure 3 archive, Figure 3 supplement 2 archive and Supplement 1 workbook were obtained. The α1 supplement's three original embedded workbooks are preserved and parsed separately. The larger Figure 3 archive is retained for provenance; its second-order γ5/β′2a results are not reanalyzed as α1→UpWiN measurements. `AUXILIARY_SOURCES.json` records originals and embedded-file hashes. The initial larger-archive download timed out and was resumed; only the completed CRC-verified archive is admitted.

A newer [Wang et al. 2026 anatomy study](https://www.frontiersin.org/journals/systems-neuroscience/articles/10.3389/fnsys.2026.1822122/full) was checked for receptor and morphological evidence. Its central-brain GluCl expression summary and inferred shunting mechanism do not identify receptors in these particular physiological targets. No receptor, sign, gain or semantic interpretation is imported from that inference.

## Figure 4: stimulation physiology

### Current-clamp recordings

Figure 4A stimulates MBON-α3 using MB082C; Figure 4B stimulates MBON-α1 using MB310C. Chrimson88-tdTomato is stimulated for **10 ms**. Target cells are randomly selected within **R64A11-LexA**, a broad population. The article reports:

| Stimulation | Responding / sampled neurons | Reported flies | Preserved source columns |
|---|---:|---:|---|
| α3 | 3 / 11 | 7 | data1 B:I nonresponders; K:M responders; O separate single-trial spiking example |
| α1 | 4 / 17 | 12 | data2 B:N nonresponders; P:S responders |

The observed α1 effect is a **negative membrane-voltage response in current clamp**, not a recorded synaptic current, receptor conductance, or measured reduction in spike rate. The hyperpolarizing bias current used to hold cells near −60 mV is a preparation condition, not a measurement of the synaptic current. Individual baseline-subtracted mean traces are retained in mV. Each has 15,001 time samples, source grid 0.0001–1.5001 s. Source time indices do not independently mark stimulation onset or define the baseline averaging window. Neither onset nor a response window is reverse-engineered from the deflection.

For auditing only, the four published-responder columns P–S have whole-trace minima **−3.590, −1.201, −4.241 and −2.571 mV**. These extrema are not fitted response amplitudes, latency estimates or biological acceptance thresholds. All 13 nonresponder traces are preserved; none is discarded or reclassified using a new threshold. Original trial-level repetitions underlying each mean trace are unavailable in these workbooks.

**Unresolved labeling:** the α3 workbook labels responder columns `Green`, while its caption says orange; the α1 workbook labels responders `Orange`, while its caption says green. File-to-panel links and measured polarity support keeping the original panel assignments, but the contradictory color text remains recorded. Source `Fly1…Fly13` and repeated `Fly1` within color blocks cannot establish animal identities: the α1 paper reports only 12 flies, and α3 has 11 neuron traces from 7 flies. We use source column locators, never synthetic fly identities or fly-held-out claims.

### Population calcium

Figure 4C exports only **21 points per mean/SEM series**, with a 1 s grid from 0–20 s. The methods report acquisition at approximately **1.07 Hz**, so the exported seconds cannot silently be treated as unmodified frame timestamps. Source traces correspond to α1 alone (n=11), α3 alone (n=5), and joint activation (n=7), with GCaMP6s measured at the dendrite/axon junction. The published result is suppression of α3-evoked fluorescence during coactivation; α1 alone does not yield detectable negative fluorescence.

No individual animal traces, nine per-animal trial traces, raw image stacks, ROI masks or frame/event correspondence accompany this workbook. Thus its displayed mean and SEM cannot be independently reconstructed. Absence of a negative calcium response does not negate electrical inhibition. ΔF/F is not converted to mV, current, spikes, release or model rate.

Figure 4 supplement 1 supplies **38 mean/SEM points** for axonal/dendritic calcium during subset activation and RNAi-based reporter exclusion. It supports interaction within the broader labeled population, not a root-specific sign or a measured conductance for every anatomical recurrent edge. Red-voxel masks/exclusion thresholds are not supplied. The methods refer to ROIs corresponding to “MB compartments,” whereas the UpWiN caption identifies a dendrite/axon junction; exact original masks are needed to resolve that scope.

## Figure 5: conditioning and recall

SS67249 labels a stochastic one-to-three-cell subset, including a cell resembling SMP353; the paper explicitly says off-target/stochastic labeling made this driver unsuitable for its behavioral experiments. R58E02-LexA activates broad reward DANs, including α1 and β1. OCT or MCH was paired with 120 one-ms pulses at 2 Hz during one minute, followed by unpaired odor. Recall odors last one second.

The exported scalar quantity is **mean baseline-subtracted depolarization over 0–1.2 s after odor onset**, in mV. All paired values are retained with their workbook rows. They are paired within a row, not joined across workbooks or to FlyWire roots.

| Source / pairing | n rows | Odor | Pre mean mV | Post mean mV | Mean within-row difference ± sample SEM mV |
|---|---:|---|---:|---:|---:|
| Fig5 data3, OCT paired | 6 | OCT | 0.657067 | 3.744570 | +3.087502 ± 0.714452 |
| same | 6 | MCH control | 1.729288 | 1.822733 | +0.093445 ± 0.633702 |
| Fig5 supp2 data3, MCH paired | 5 | OCT control | 1.971117 | 2.428925 | +0.457808 ± 0.509233 |
| same | 5 | MCH | 2.551814 | 4.885817 | +2.334003 ± 0.171699 |

All eight printed means reconstruct within **6.3×10⁻¹⁵ mV**, and SEMs within **8×10⁻¹⁶ mV**. This is a numerical transcription check, not independent biological replication. The two reciprocal sets' non-time waveform columns are not exact duplicates. Shared time arrays are expected. Absence of exact duplication does not establish distinct animal identity.

The representative workbooks contain 26,001 samples per trace; group mean/SEM workbooks contain 26,501 samples on a 0.1 ms grid. Neither supplies all individual voltage trials behind the group waveforms. Event onset and baseline-window metadata are not recoverable from a dedicated event column. The supplementary scalar source link is described as panel C despite containing panel D scalar data; that source-label discrepancy is preserved.

### Separate upstream conditioning evidence

Yamada 79042 Figure 3 supplement 2 labels α1 with **MB319C** and stimulates **PAM-α1 MB043-split-LexA**, unlike the broad R58E02 driver above. Its scalar endpoint is **odor-evoked spike count**, after subtracting spontaneous spikes over a 1.2 s response window. It is not UpWiN mV. Reconstructed means:

| Pairing | n | Paired odor pre → post | Control odor pre → post |
|---|---:|---|---|
| OCT | 6 | 74.066667 → 19.560000 | MCH 66.533333 → 46.973333 |
| MCH | 5 | 62.040000 → 20.264000 | OCT 68.112000 → 50.616000 |

The scalar means and SEMs reconstruct within 6×10⁻¹⁴ and 3×10⁻¹⁴, respectively. This supports upstream response suppression in that preparation. It is **not** a numerical α1-spike→UpWiN-voltage transfer. In addition to distinct animals and neuron types, odor dilution differs (**2% versus 1%**), holding-current limits differ (typically **<100 pA versus <10 pA**) and reward drivers differ. A shared nominal pulse schedule does not remove these differences.

## Behavior and intervention datasets

The measured biological quantities include **wind-relative heading/cosine, turn angle, walking speed, area-normalized radial displacement**, and separately recorded odor/light-distribution and return-location endpoints. None is exported as a Genesis action.

Figure 1 provides training-session matrices, scalar experiment summaries, orientation-binned means/intervals/N, trajectory-level scalar summaries and group time series. It does **not** provide complete time-stamped XY/heading tracks with persistent fly identity. Genotype, reciprocal PA/EL associations and NoLED conditions are explicitly encoded. `#001` is a source ordinal, not an identified fly.

Figure 6 activation compares two UpWiN drivers, an empty driver and MB077B; it separates airflow direction/rate, starvation and arista status. Descriptive means from all available scalar cells are:

| Condition | Source n | Mean Δ(area-normalized radial position) |
|---|---:|---:|
| Fed / starved | 14 / 16 | 0.035009 / 0.122580 |
| Airflow 0 / 25 / 50 / 100 / 200 / −200 mL/min | 13 / 11 / 11 / 11 / 9 / 16 | 0.009692 / 0.015055 / 0.081836 / 0.066427 / 0.147256 / −0.086050 |
| Intact / unilateral / bilateral arista ablation | 20 / 40 / 40 | 0.098400 / 0.031295 / 0.033862 |

These are descriptive source means, not fitted dose-response or movement probabilities. Reverse airflow reverses radial direction; this is evidence against a simple fixed tendency to move outward. Arista ablation shows wind-sensory dependence, **not** preserved sensory responsiveness under that intervention. A generic early angular-speed/startle increase also occurs in empty controls; direction and orientation-dependent walking provide the narrower population-manipulation evidence.

Figure 6F source counts are **446 / 540 / 232 / 219** (SS33917 / SS33918 / MB077B / empty), while the caption reports **444 / 540 / 231 / 219**. No rows were removed to force agreement. Figure 6D also labels cosine orientation bins opposite to the global upwind-angle convention. The data and caption stay unchanged; unambiguous direction assignment and exclusions require clarification. Figure 6E/F/G supplies smoothed bins or scalar trajectory quantities, not a ready-made independent fly split.

Figure 7A preserves all source numeric values, including several appearing on nominal genotype row 3. Those are retained with original cell provenance; they are not shifted to invented fly rows. Figure 7B contains unlabeled replicate time-series columns; mapping to individual flies or Figure 7A rows is unknown. `SS33197` in this file/prose versus `SS33917` in methods remains a naming discrepancy. Figure 7E's source labels `SS49975`, whereas the caption names `SS49755`; that unrelated group's identity remains unresolved.

TNT in SS33917 reduces reported memory-associated upwind displacement compared with controls. This supports population involvement but is chronic release blockade: acquisition, consolidation and downstream expression are not isolated, and complete upstream-learning/sensory/locomotor preservation is not established. Acute shibire blockade at recall affects the published binary odor distribution endpoint. **Upwind behavior could not be analyzed at restrictive temperature because controls did not show CS+-induced upwind locomotion (data not shown).** This is not acute route-specific validation of that kinematic endpoint.

SMP108 activation also elicits upwind movement in the screen, with a different kinematic profile. Yamada's SMP108 TNT manipulation impairs second-order learning while sparing tested first-order memory. These observations do not establish SMP108 as a necessary motor relay for the α1→UpWiN route. Downstream dopamine release is a separate biological quantity.

The movie-level supplement workbooks contain useful recording locators: Figure 2 supplement 1 has **830 measurement rows, 166 distinct arena/camera/timestamp tuples**; Figure 7 supplement 1 has **440 rows, 88 tuples**. Multiple measurement types reuse each movie. Female/male columns denote parental driver/effector stocks, not sex of individual tracked animals. Movie-held-out analysis might eventually use actual recording locators; it must not be called fly-held-out or use each metric-row as an independent recording. No holdout split, acceptance threshold or decoder is designed here.

## Missingness and unresolved provenance

Unknown: globally unique animal/cell IDs, Figure 4 responder morphological identity, linkage among physiology and behavior cohorts, raw trial-level voltage/image data, event/frame alignment, original analysis scripts/ROI masks and per-record exclusion history. Source values can reconstruct Figure 5 scalar means and the separate α1 scalar endpoint; published image/group-waveform means cannot all be reconstructed from the supplied observations. No mean/SEM is inverted into fictitious trials.

The previous representation-study MBON14 validation-workbook inconsistency is unrelated to these newly audited α1/UpWiN scalar workbooks and remains frozen. A successful scalar reconstruction here neither repairs that dataset nor validates a universal MBON observation model.

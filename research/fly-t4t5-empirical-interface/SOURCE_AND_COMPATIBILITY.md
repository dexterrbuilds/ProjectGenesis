# Source, preparation and observation compatibility

## Direct measurements used

| Source | Preparation / identity | Quantity and sampling | Use and limits |
|---|---|---|---|
| [Gruntman, Romani & Reiser 2019](https://doi.org/10.7554/eLife.50706), [pinned original author inputs](https://github.com/reiserlab/T5ConductanceModel/tree/fe52053dda84d49a124e6c1f141dd461eba9630c) | Female adult D. melanogaster, 1–2 days; T5 SS25175 (VT055812-AD / R47H05-DBD), left-brain soma; 17 recording ordinals, fly identities unavailable | Whole-cell current-clamp trial-mean baseline-subtracted voltage, mV. Compact bar samples 5 ms, apparent-motion/grating samples 2.5 ms; original acquisition 20 kHz. Bias current 0–3 pA toward −60 to −55 mV: not native resting physiology. | Original `data_cell_*_all.mat` inputs, never authors' simulation `result_cell_*`. Four non-flash families retained; 1,398 flash protocols excluded because those observations were reused in 2021. No independent replication or 34 independent T5 cells claimed. |
| [Gruntman et al. 2021](https://doi.org/10.1016/j.cub.2021.09.072), [Figure 2 archive v1](https://doi.org/10.25378/janelia.16663705.v1) | Female adult 1–2 days; T4 VT015785-AD / R42F06-DBD; T5 SS25175. T4 15 analyzed ordinals (slot 5 explicitly empty/excluded); T5 17 ordinals. No fly, subtype or root labels in exported measurements. | Mean baseline-subtracted somatic voltage, mV; acquired frozen source traces on 1 ms grid. Both contrast polarities, RF offsets, widths and durations. Trial means, not independent trials. T5 repetition counts unresolved. | 2,260 T4 and 2,204 T5 traces. Source ZIP MD5 `cabf1b1c6d0ef4af200d41256e2835cf` already verified by the frozen acquisition. This study hashes/reuses those inputs; it does not redo extraction or alter the prior study. |

`SOURCE_INPUTS.json` hashes every numerical source input. Full source metadata, archive member checksums, author-code commit and preparation audit remain in the frozen boundary study and are protected by `FROZEN_BEFORE.json`.

2019 repository license: GPL-3.0; associated original Figshare data: CC BY-NC 4.0. 2021 archive metadata: CC BY 4.0. These contexts are retained separately; this research package does not assert blanket commercial licensing for inherited measurements. Recordings are not new experiments.

## Additional processed data sought

[Dryad visual-sparsity deposit](https://doi.org/10.5061/dryad.t1g1jwtbs) describes a 180.33 MB processed archive, including T4/T5 calcium sparsity and single-moving-bar velocity measurements. The public README is accessible; the attempted `file_stream/4404307` download returned HTTP 403. No new arrays were obtained or fitted. The previously inventoried DANDI raw imaging assets are not processed voltage, and were not substituted. Figure 4 of the 2021 study is inventoried in the frozen acquisition but not processed here. This is a coverage/access limitation, not evidence those data do not exist. No alternative precursor assay was substituted.

## Compatibility matrix

| Pair / proposed transfer | Allowed? | Reason |
|---|---|---|
| Exact named recording + exact source stimulus + same voltage observation | Yes, direct retrieval | Preserves measured assay and conditional localization |
| Same recording, one flash axis varied within validated brackets | Restricted empirical interpolation | No mechanism or unmeasured continuous-space claim |
| Different recordings in same source/type/full stimulus tuple | Conditional template only | Recording-held-out validation; fly identity and independent localizer unknown |
| 2019 T5 ↔ 2021 T5 | Not pooled | Reused cells/observations; unverified ordinal join and display-scale ambiguity |
| T4 ↔ T5 | No | Separate type, preparation and validation strata |
| Voltage ↔ calcium / spikes / rates / transmitter release | No | Conversion and compartment observation model unidentified |
| Soma waveform ↔ axon terminal / individual FlyWire root | No | No physiological recording-to-root or soma-to-terminal transfer |
| Whole-cell biased preparation ↔ freely moving intact fly | No | Body state, recording bias, compartment and observation differ |

Export is restricted to 0–500 ms after the source stimulus onset. Linear resampling is a measurement-grid operation; it neither adds temporal resolution to the original samples nor models temporal dynamics. Several apparent-motion second onsets occur after the export window; such traces cannot validate the later second response. Long moving/grating stimuli likewise extend beyond this horizon. Unknown trial variability remains unknown, not zero noise.

## Coordinates and identity

Source RF/PD alignment was response-derived. Held-out recording prediction is conditional on that localization and may be optimistic relative to a new unlocalized recording. The physical 1-D sample positions, direction codes and full grating patterns remain literal. PD/ND direction-code crosswalk is not independently resolved in this export, so the biological direction label stays null. No response-optimized reflection, rotation or angle scaling is introduced.

The prior independent geometry audit found 11,822 T4/T5 column assignments, 11 subtype conflicts and two roots absent from the annotation's T4/T5 subset. Its 778 lens/Mi1 ordinal matches are not FlyWire-root matches. CATMAID skeleton → FlyWire root and experimental screen/head registration remain unresolved. Source pixels cannot be turned into a universal retinal-degree scale (2019 maximum pixel angle 2.25° and 2021 1.875° do not establish an interchangeable per-recording transform).

**Resolution:** named source recording retrieval is valid; type-level conditional empirical templates are limited; subtype/column/root physiology transfer is unsupported. A class label is not a root crosswalk. No anatomy or canonical synapse ownership is created here.

# Coordinate crosswalk and uncertainty

No reflection, rotation or angle scale was chosen by a Stage-4/LPLC2 response. Geometry is audited separately from fitting.

| Join | Evidence and measured scope | Status |
|---|---|---|
| FlyWire root → annotated T4/T5 type | Pinned annotation v3.1.0: 12,246 T4/T5 rows. Roots retained as strings. | Available; cross-table disagreements are not silently repaired. |
| Root → anatomical column/lattice | Pinned public Codex column table contains 11,822 T4/T5 assignments, both hemispheres. Root, type, column ID and original x/y/p/q retained in ROOT_COLUMN_CROSSWALK.csv. | 11 subtype conflicts (all left hemisphere); 2 column roots absent from the annotation's T4/T5 subset. Conflicts remain unresolved. |
| Anatomical column → retinal viewing direction | [Zhao et al. 2025](https://doi.org/10.1038/s41586-025-09276-5), author repository commit 99d2a43123db636cedb55af9ff31a59657e7d17e. Recovered 778 matched Mi1-ordinal/lens-ordinal entries, 779 medulla columns, 852 lens entries; exported local medulla coordinates and unit viewing vectors. | The author index is not a Codex column ID. The CATMAID Mi1 annotation table has skeleton identities, not FlyWire root IDs. No verified skeleton→root join; no nearest-neuron substitution. |
| Eye/retinal frame → subtype-local motion vector | [Shinomiya et al.](https://doi.org/10.7554/eLife.40025) describes conventional a/b/c/d front-to-back/back-to-front/up/down categories; [Haag et al.](https://doi.org/10.7554/eLife.29044) supplies local functional tuning evidence. Eye-map study establishes that geometry matters across visual field. | Categories do not provide one global Cartesian vector for every root. A body-motion label is not the same sign as retinal image motion. Hemisphere and chiasm must be explicit. |
| Retinal direction → experimental screen/head frame | Whole-cell recording paper describes display/localizer/PD procedure; compact arrays provide an author-localized pixel axis. | Individual head pose, RF viewing direction and root/subtype identity are missing. No defensible numerical transform is frozen. |

## Anatomical transformations that are supported

The recovered `proc_eyemap.R` aligns anatomical landmarks and explicitly reflects the medulla Y coordinate for the chiasm (lines 129–131). This is independent anatomical code, not a response-optimized sign flip. The exported `ucl_rot_sm` vectors have norms within floating precision of one. Their axes remain the authors' rotated anatomical/microCT frame. Artificial auxiliary boundary points (39) are excluded from neuron/column counts. Plotting shifts such as `utp_lens_rot_shift` are not treated as viewing directions.

## Uncertainty

The root/column/type joins are discrete identities; mismatches are explicit rows, not small angle errors. The unresolved author-ordinal→FlyWire mapping cannot be replaced by multiplying lattice pixels by a guessed degree scale. Specimen registration, eye variation and electrophysiology head alignment contribute additional uncertainty for which this study has no calibrated angular confidence interval.

The authors' 2019 local RF center and PD alignment are used only to define a **conditional within-recording assay**. They cannot validate a held-out root or screen transform. No test response was used to reposition a model RF. Published localization itself used physiological responses, so it is not an anatomy-only independent coordinate measurement.

## What must be obtained before root-level deployment

An audited CATMAID skeleton/FAFB-v783 root crosswalk; resolution of subtype conflicts; per-root local direction field/eye-map mapping with provenance; and experimental screen/head registration or a clearly bounded population observation model. New work must freeze those transforms before downstream evaluation. This study does not run that downstream evaluation.

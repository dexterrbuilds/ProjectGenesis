# Crosswalk confidence and limits

`CROSSWALK.json` joins **37 named root IDs as strings** from the frozen circuits to the pinned v3.1.0 annotation TSV. Every selected current cell type agrees with that TSV. Source hashes are included. It does not join unrelated specimens by a numerical ID or equate a hemibrain body ID with a FlyWire root.

| Functional population | Current annotation | Root IDs / scope | Identity confidence | Physiological transfer confidence |
|---|---|---|---|---|
| MBON-α1 | MBON07 | Stage 1: `720575940617302365`, `720575940652390134`; Stage 3 additionally `720575940623381956`, `720575940628783363` | High type-level correspondence; not the same recorded individuals | Low for numerical feedback and learning, no matched α1 conductance series |
| PAM-α1 | PAM11 | 13 selected Stage-1 roots, individually listed in JSON | Type-level annotation; a driver can sample a population differently | Unknown root-specific dopamine dose and release dynamics |
| PPL1-γ1pedc / MP1 | PPL101 | `720575940617691170`, `720575940621040737`; FBbt_00100243 | High type-level | Moderate mechanism correspondence to Hige/Tsao/Sayin; low numerical transfer across preparations/state |
| MVP2 / MBON-γ1pedc→αβ | MBON11 | `720575940617749538`, `720575940623201833`; FBbt_00100246 | High type-level | Strong LTD/sign evidence; neither exact contact efficacy nor shared state rule identified |
| MBON-α2sc | MBON18 | `720575940624539284`, `720575940622997453`; FBbt_00110101 | High type-level | Calcium state effects do not identify membrane, receptor or downstream LH gain |
| OA-VPM4 | OA-VPM4 | `720575940636574388`, `720575940625264457`; FBbt_00110152 | High named type/ontology; MB113C more selective than MB22B | Suppressive effect supported; exact receptor/kinetics unmeasured |
| α′3ap / α′3m outputs | MBON16 / MBON17 | `720575940623377802`, `720575940626744921` / `720575940617760257`, `720575940638774606` | High canonical type annotation; only moderate correspondence to pooled MB027B recordings | Group calcium ≠ each root's identical rate/efficacy |
| PPL1-α′3 | PPL104 | `720575940627549205`, `720575940632107335` | High type correspondence | Local dopamine quantity/threshold unknown |
| α′3-related ambiguous cells | MBON17-like / MBON28 | Four separately marked roots in JSON | Ambiguous functional-driver membership | No transfer of familiarity rule justified |
| APL | APL | `720575940613583001`, `720575940624547622`; FBbt_00100222 | High type-level | Local calcium response transfers as a structural warning, not a fitted scalar inhibitory gain |
| Hafez MBON-α3 | MBON14 | Not α′3/MBON16/17 and not MBON07/11/18 | Distinct type: transfer rejected | Measured τ is a reference for MBON14 only |
| PN/KC classes and LH candidates | Many roots | Original manifests remain authoritative | Class/glomerular/subtype correspondence; no rootwise odor recording | No assumed odor response, receptor profile, or conductance equivalence |

## Audit trail

Anatomical nomenclature is supported by [Li et al. 2020](https://elifesciences.org/articles/62576), the frozen annotation source, and the prior root-level crosswalk audit. Functional grouping is checked against the primary papers listed in `EVIDENCE.md`, including their driver caveats. No new root was selected or renamed.

Independent VFB records used in the frozen audits include [MBON11](https://www.virtualflybrain.org/term/mbon11-vfb_fw035279/), [MBON18](https://www.virtualflybrain.org/blog/2022/01/01/mbon18-vfb_fw036312/), [MBON16](https://www.virtualflybrain.org/blog/2022/01/01/mbon16-vfb_fw031879/), [MBON17](https://www.virtualflybrain.org/blog/2022/01/01/mbon17-vfb_fw008387/), and [PPL104](https://www.virtualflybrain.org/term/ppl104-vfb_fw035370/). They are corroborating identity records, not evidence that those roots were physiologically recorded.

Automated neurotransmitter prediction sometimes contradicts established KC cholinergic identity. The JSON retains both fields; it does not convert a dopamine prediction into a dopaminergic KC or erase cotransmission. PPL101 nitric oxide and KC peptides are reasons for uncertainty, not a license to fabricate receptor effects.

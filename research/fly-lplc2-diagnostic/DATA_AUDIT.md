# Independent data and provenance audit

All cached files are byte-hashed in the final package. None replaces a previous study's source file. Primary-paper observations and authors' computational models are separate entries in `EVIDENCE.json`.

| Source | Access / use | Compatibility and limits |
|---|---|---|
| [Klapoetke 2017](https://doi.org/10.1038/nature24626) | Existing frozen primary XML inspected read-only; recordings/code on request, not obtained | Female 2–5 d GCaMP6f; single-axon and population normalization differ. Morphology does not determine electrical compartment count. No curve digitization |
| [Haag 2016](https://elifesciences.org/articles/17421) | Primary XML cached; published quantitative text audited | GCaMP6m terminals, layer-3/upward class; column-targeted and arena assays separated. Retrieved methods specify 25 C rearing; sex/age not specified there. Approximate published ratios retained as approximate |
| [Gruntman 2021 Figure 2](https://doi.org/10.25378/janelia.16663705.v1) | Metadata saved; 6,320,065,220-byte ZIP not downloaded | Whole-cell T4/T5; arrays advertised as per-cell position/duration/width/polarity responses. Sex/age/independent cell grouping require archive audit. Dataset CC BY 4.0. Model-code dataset is not physiological evidence |
| [Gou/Matulis/Clark Dryad](https://doi.org/10.5061/dryad.t1g1jwtbs) | Version-4 metadata and file list saved; API downloads returned 401; public download links 403 | CC0 dataset; 180,331,689-byte figure-data ZIP SHA `83a2bc0c5e1ce64787a30183f486d219c377014014b5bac5448f6b17502bc35f` listed but not verified locally. Planned Figure-7 fitting NOT performed. Metadata do not count as processed recordings |
| [Raw DANDI alternative](https://dandiarchive.org/dandiset/001205) | Identified, not downloaded/processed | Alternative future access path, not completed analysis |
| [Ramos-Traslosheros/Silies 2021](https://doi.org/10.1038/s41467-021-24986-w) | Primary XML + publisher `41467_2021_24986_MOESM4_ESM.xls` saved, read-only | Female 1–7 d, right optic-lobe calcium. Workbook headers explicitly supply Fig7g fly IDs and dF/F0. All control rows used; CDM unpooled. Original workbook not edited, exported or recalculated |
| [Same study G-Node archive](https://doi.org/10.12751/g-node.qeeyfz) | Identified, not processed | Additional raw/minimal datasets; not required for the bounded source-table calculation |
| [Zhao 2025](https://doi.org/10.1038/s41586-025-09276-5) | Frozen XML/tree reused; [author map repository](https://github.com/reiserlab/eyemap_T4) identified | Same FAFB anatomy but separate female eye/H2 physiology; no exact selected-root eye map produced. Numeric eye datasets not fitted |
| [Kim 2023](https://doi.org/10.1016/j.cub.2022.12.014) | Publisher-indexed primary excerpts; full-text direct access 403 | GCaMP7f, tethered non-flying visual recordings; exact age/sex not verified. No quantitative local-coupling claim or imported delay |
| [Molecular gradients 2025](https://doi.org/10.1038/s41586-025-09037-4) | Primary publisher mechanism and preparation text inspected; no source-workbook fit | FAFB/hemibrain anatomy, developmental molecular perturbations, adult local GCaMP7f. Supports topographic input organization; not root-specific electrical compartments. Separate evidence addendum |
| [Mauss 2015](https://doi.org/10.1016/j.cell.2015.06.035) | Functional study and target scope audited; no raw recordings processed | LPi→tangential-cell receptor/sign evidence cannot silently become LPi→LPLC2 receptor evidence |
| [Matsliah 2024](https://doi.org/10.1038/s41586-024-07981-1) | Pinned anatomy/crosswalk reused | One female FAFB; aggregated chemical contacts. No physiological sign inferred from contact count alone |
| [Ketkar 2022](https://doi.org/10.7554/eLife.74937) | Primary publication figures/text inspected | L1/L2/L3 contrast/luminance assays; no coefficient transfer or new fit |
| [Pang 2025](https://doi.org/10.1016/j.cub.2024.11.064) | Published primary account/metadata; EPMC XML returned 500; [Dryad](https://doi.org/10.5061/dryad.ngf1vhj4c) identified, not processed | ASAP2f voltage assay distinct from calcium; temporal preprocessing constraints only. Root/time-constant calibration unavailable |

## Exact source-workbook access

Publisher URL: [MOESM4 XLS](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-021-24986-w/MediaObjects/41467_2021_24986_MOESM4_ESM.xls). Retrieval succeeded after PMC/static-host routes failed. The source DOI paper links this workbook as source data. The workbook is the publisher's legacy binary XLS, not an authored diagnostic spreadsheet. The paper is open access; retain publisher attribution and original license. `xlrd==2.0.2` is vendored only inside this isolated study to read it; its license and package metadata are retained.

Used `Fig7g!A2:A71`, `C2:C71`, `E2:E71`; numeric and nonmissing alignment checked. The workbook fly index runs 1–7; it is not inferred from neighboring rows or ROI names. Independent unit is fly, not ROI. Unreported preparation variables remain unknown. Width ranges are recorded per series in `INDEPENDENT_RESULTS.json`; no independent fly count is invented for them.

This assay measures Tm9 **full-field mean fluorescence**, not local T4/T5 voltage, dendritic gain or LPLC2 selectivity. The failure of a pooled signed constant to predict held-out flies does not resolve those questions. No confidence interval is fabricated from figure error bars, and no source-data coefficients are treated as synaptic parameters.

## Inclusion and exclusion discipline

Author simulations, neural-network models optimized for collision performance, robotics demonstrations and unspecified review claims are not independent physiological validation. Data access failures remain logged; they are not replaced with synthetic recordings. No communication requesting data was sent to an author. No new population function was assigned from a similar name alone.

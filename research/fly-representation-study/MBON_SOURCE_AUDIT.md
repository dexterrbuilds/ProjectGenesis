# MBON14 supplementary workbook: unresolved source inconsistency

Source: Hafez et al.2023 [article](https://elifesciences.org/articles/77578), [figures](https://elifesciences.org/articles/77578/figures), [Table1 source data1](https://cdn.elifesciences.org/articles/77578/elife-77578-table1-data1-v4.xlsx). Original bytes are preserved as data/mbon14-egfp.xlsx; hash in data/challenges.json and final manifest.

The header describes four cells marked with cytosolic EGFP. Rows4–7 contain tau16.41,17.43,24.58,9.51ms. Their arithmetic mean is16.9825ms; row9 reports14.48ms. Row6 lists Vm−56.2mV, tau24.58ms, C21.60pF, and specific capacitance0.350, matching the original training Table1 cell3 in those four entries. This is a **duplication/provenance flag**, not proof that the same recording was reused. Decimal matches could have other explanations; resolving them requires source provenance.

The four displayed resting potentials also average−59.1mV rather than reported−60.6mV; capacitances average16.46pF rather than13.95pF. These discrepancies are not explained by ordinary rounding. Some cells are stored as text in the workbook; extraction explicitly converts numeric strings without discarding them. No source values are corrected or replaced.

The current article identifies distinct marker preparations and illustrates both, but supplies no cell-level identifier reconciliation. The inspected current source link, article/figures and indexed full text did not provide an authoritative correction. Searches for a correction did not locate one. The JHU dataset/API request returned403, preventing verification from raw individual traces. These access/search limits do not establish that provenance cannot be obtained.

**Disposition: excluded from clean independent validation/model selection.** Preserve the completed diagnostic forecast16.056ms and RMSE5.420ms, with all four rows retained. The previously calculated duplicate-excluded sensitivity is also retained but cannot rescue validation: deleting a suspicious row does not repair provenance or incorrect summaries. Do not count4/4 within the broad prediction interval as successful representation validation. No new R0/R1/R3 model is selected from this workbook.

Cell identity: MBON-alpha3/MBON14, not MBON-alpha-prime3/MBON16/17 and not alpha1/MBON07. No transfer to shared Stage1/3 synapses.

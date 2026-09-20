# Project Genesis — Drosophila physiology study

**Classification: PARTIAL PHYSIOLOGICAL CONSTRAINT.**

Start with [REPORT.md](REPORT.md). This is an isolated identification study, not Stage 4 or a migrated/common brain. All older experiments and canonical Genesis are preserved.

## Evidence

- [EVIDENCE.md](EVIDENCE.md): 20 primary evidence entries, metadata, quantitative targets and transfer limits.
- [PARAMETERS.md](PARAMETERS.md): 65 parameter/operator instances; source-linked classifications.
- [CROSSWALK.md](CROSSWALK.md), [CROSSWALK.json](CROSSWALK.json): audited named types and string root IDs.
- [CALIBRATION_FROZEN.json](CALIBRATION_FROZEN.json), [VALIDATION.json](VALIDATION.json): original APL observation fit and held-out result, unchanged.
- [IDENTIFICATION_FROZEN.json](IDENTIFICATION_FROZEN.json): independent conditioning endpoint and non-identifiability profile.
- [TRANSFER_FROZEN.json](TRANSFER_FROZEN.json): no justified numerical neural transfer, frozen before replay.
- [REPLAY_COMPARISON.json](REPLAY_COMPARISON.json), [REPLAY_TRIAL10.json](REPLAY_TRIAL10.json): eight exact unchanged-model control replays. These are not calibrated-kernel predictions.
- [UNIFIED_PHYSIOLOGY.md](UNIFIED_PHYSIOLOGY.md): unresolved shared-synapse conflicts and required measurements.
- [PRESERVATION.json](PRESERVATION.json), [STUDY_MANIFEST.json](STUDY_MANIFEST.json): checksums and audit.

## Reproduction and scope

From repository root, read-only verification:

```sh
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python -m unittest discover -s research/fly-physiology-study -p test_study.py
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-physiology-study/final_audit.py --check
```

Fitting dependencies: Python, NumPy, SciPy; extraction additionally uses openpyxl read-only. Python/NumPy/SciPy versions for neural runs match the frozen `.local/fly-stage1-venv` (NumPy 2.3.5, SciPy 1.16.2). The bundled Python runtime was used to read XLSX. No package change to Genesis is needed.

The fitting programs refuse to overwrite existing frozen outputs. To reproduce fits, use a **disposable copy** containing code, plans and source data, omit its existing generated fit/validation JSON outputs, then run `calibrate.py train`, `calibrate.py validate`, and `identify.py`. Never delete accepted study evidence to rerun in place. Training reads only experimental data, not Stage results. `extract_measurements.py` preserves source workbook bytes and fails if the split outputs already exist.

The replay worker imports each frozen model/protocol in a fresh process and writes only here. `REPLAY_PLAN.md` records the exact eight cases. It has no runtime, wallet, LLM or canonical database import. Compare historical summaries only after all new cases finish; no parameter update follows that comparison. Re-running a full prior validation battery is unnecessary.

The canonical audit used read-only database transactions. No scheduler process or Genesis life cycle was started.

## Source rights and interpretation

Amin et al. 2020 Figure 4/7 source datasets are CC-BY, attributed in `data/PROVENANCE.json` and `SOURCE_ACCESS.json`. Other full papers were read locally, not redistributed. New traces are genuine numerical outputs of the unchanged research models, not biological recordings. APL coefficients describe fluorescence-response mixing, not anatomical edges, inhibitory conductance or a novelty/persistence score.

**BIOLOGICAL FACT:** source measurements and pinned anatomy. **COMPUTATIONAL MODEL:** explicitly labeled observation fits, rate/plasticity assumptions and identification calculations. **GENESIS MAPPING:** none.

Stop for review. No integration or Stage 4 is included.

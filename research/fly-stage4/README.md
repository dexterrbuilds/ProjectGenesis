# Stage 4: LPLC2 physical visual-stimulus experiment

**Gate A: NOT SUPPORTED for this frozen model. Gate B: NOT TESTED.**

Read [REPORT.md](REPORT.md) for quantitative results and limits. Nothing here is connected to Genesis or admitted to Brain Spec. Prior studies and the seven-cycle canonical organism remain unchanged.

## Review artifacts

- `PROTOCOL.md`, `PREREGISTRATION.json`: prospective selection, physics, measurements, controls and non-numerical biological acceptance constraints; registered before extraction/results.
- `DEPENDENCIES.json`: exact Brain Spec 0.1.0 release and content-pinned entry dependencies. The existing validator verifies these dependencies, not new physiological claims.
- `LITERATURE.md`, `SOURCE_ACCESS.json`: primary evidence, preparation compatibility and source-data limitations.
- `CROSSWALK.json`: root/type/column joins, excluded conflicts, prospective anatomical ranking and DN route audit.
- `CIRCUIT_MANIFEST.json`, `circuits/`: immutable L0/L1 row views, canonical identities, counts, boundary retention and unknown operators.
- `MODEL_FREEZE.json`, `UNADMITTED_EXTENSION.json`: exact model implementation, representation decisions and unknown physiology. No root receptor map is fabricated.
- `RESULTS.json`, `MEASUREMENTS.csv`, `traces/`: all 846 trial results. Every primary trace contains all neural and motion-input states; other files contain real continuous measurements. NPZ measurement columns are **time in seconds, target rate, sum of T4/T5 rates, sum of motion inputs, maximum network rate**. Rate-column order follows circuit `nodes`; motion-column order follows T4/T5 nodes in that same order. Condition labels configure the physical movie outside `Model.step`, which receives only intensity samples.
- `ANALYSIS.json`, `RELIABILITY.json`, `replay/`: complete comparisons, interventions, snapshot/seed/fresh-process audits.
- `PERFORMANCE.json`, `ENVIRONMENT.json`: measured computation and dependencies.
- `PRESERVATION.json`, `PACKAGE_MANIFEST.json`: prior-file/database audit and content-addressed final package.
- `CANDIDATE_EVIDENCE_UPDATE.json`: **UNADMITTED** negative model-result claim; no capability promotion or supersession.

## Read-only verification

From the repository root, using the existing research environment:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/genesis-brain-spec-v0.1/check.py --package --experiment research/fly-stage4/DEPENDENCIES.json
PYTHONDONTWRITEBYTECODE=1 python3 research/fly-stage4/validate.py --package
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python -m unittest discover -s research/fly-stage4 -p 'test_stage4.py' -v
```

`validate.py` hashes saved DB audit files; it does not open a database or start a runtime. The before/after database audits were performed separately using the established repeatable-read, read-only audit script. Unit-test success is not biological success.

## Reproduction without overwriting evidence

`run.py --fresh-task replay/L0_task.json --output replay/<new-name>.json` reproduces one saved primary task in a fresh process and records readout/final-state hashes. Use a **new output name outside the finalized package in a separate copy** to keep this completed directory frozen. `reliability.py` has already produced midpoint and fresh-process evidence for both levels.

Do not rerun `extract.py`, `run.py`, `analyze.py` or `reliability.py` into the completed package. Their artifact writer refuses different replacement content. Full independent reruns belong in a separate study copy with the pinned inputs, untouched protocol and exact dependency versions in `ENVIRONMENT.json`; no parameter search is provided. The extraction uses the already pinned local v783 source and its verified sparse cache, not a live mutable API.

Scope ends at this report. No executable behavioral labels, plasticity, BrainAdapter migration, autonomous cycles or product mapping are included.

# Drosophila neural representation study

Start with [REPORT.md](REPORT.md).

**Classification: INSUFFICIENT EVIDENCE TO SELECT REPRESENTATION.** Local APL representation has narrow support, but neither a positive physiological coupling constant nor a common neural kernel is established. A heterogeneous representation is a supported direction for further identification, not an implemented brain.

## Artifacts

- PLAN.md: original analysis and selection rules, unchanged.
- FIT_FROZEN.json, VALIDATION.json: interrupted analyses, unchanged.
- EVIDENCE.md, MBON_SOURCE_AUDIT.md: source/preparation/crosswalk evidence and exclusion of the inconsistent MBON workbook from clean validation.
- data/: published CC-BY source workbooks and exact extracted measurements.
- REPRESENTATIONS.md, IDENTIFIABILITY.md, TEMPORAL_CONDITIONING.json: equations, scoped evidence, analytical tests and unknowns.
- SCALING.md, benchmarks/:15 real-anatomy engineering workloads with explicit local/plastic state costs. Outputs are **not biological neural traces**.
- IDENTITY_SCHEMA.md, IDENTITY_AUDIT.json, identity-registry.jsonl.gz, shared-row-ids.json: identity-only deduplication. No unified physiology.
- SUMMARY.json, PRESERVATION.json, STUDY_MANIFEST.json: result and verification.

## Reproduction

Read-only checks from repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python -m unittest discover -s research/fly-representation-study -p test_study.py
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-representation-study/final_audit.py --check
```

All generators refuse overwriting completed outputs. To reproduce numerical analysis, use a disposable copy with source data/plans/code but without generated results. `fit.py` reads only experimental training data. `extract.py` uses bundled Python/openpyxl in read-only mode after fit freeze; `validate.py` evaluates without updating coefficients. `extract_spatial.py` is descriptive, not another fit. `measurement_constraints.py` evaluates mathematical compatibility/identifiability, not a neural replay. Dependencies remain isolated; no application package change.

`identity.py` reads frozen circuit JSON and emits unique aggregate rows with null physiology. `run_benchmarks.py` runs15 sequential fresh processes and skips already-completed results. Frozen anatomy in `research/fly-boundary-study/anatomy` is required. `report.py` assembles scaling/summary outputs. `canonical-audit.mjs` is optional authorized read-only database auditing using DATABASE_URL; it never imports runtime/migrations/scheduler. Never start the canonical runtime to reproduce research.

No Stage replay is justified by the identified physiology, so none is performed. Existing tests do not create canonical life cycles. This study stops for review; no integration or next-stage work is included.

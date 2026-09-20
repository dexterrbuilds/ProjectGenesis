# Isolated LPLC2 diagnostic

Read [REPORT.md](REPORT.md) first. This package diagnoses the frozen Stage-4 visual computation; it does not retry Stage 4 or implement a replacement brain.

## Reproducible read-only analyses

Requirements: Python 3.12+ with NumPy; vendored `xlrd==2.0.2` for the original publisher XLS. The project's `.local/fly-stage1-venv/bin/python` has NumPy; the bundled artifact runtime also works. Set `PYTHONDONTWRITEBYTECODE=1` to avoid adding caches in old research directories.

```sh
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-lplc2-diagnostic/independent_data.py
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-lplc2-diagnostic/anatomy_audit.py
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-lplc2-diagnostic/algebraic_checks.py
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-lplc2-diagnostic/check.py
```

The scripts refuse to replace a result with different bytes. Existing result files can be verified without rerunning the neural models. Anatomy analysis reads the pinned full-anatomy arrays and frozen Stage-4 circuits; the biological observation estimator reads only the publisher workbook and its prospective registration. `benchmark.py` records timing once; repeating it would produce different timing bytes and is intentionally not part of the verification suite.

`DEPENDENCIES.json` is validated with the unchanged Brain Spec checker:

```sh
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/genesis-brain-spec-v0.1/check.py --package --experiment research/fly-lplc2-diagnostic/DEPENDENCIES.json
```

## Artifacts

- `PLAN.md`, `DIAGNOSTIC_REGISTRATION.json`: original prospective questions and separation rules.
- `SOURCE_DATA_ADDENDUM.md`, `SOURCE_DATA_REGISTRATION.json`: access-driven assay choice before reading measurement values.
- `EVIDENCE.json`, `TRANSFORMATIONS.json`, `DATA_AUDIT.md`: sources, compatibility, information loss and uncertainty.
- `INDEPENDENT_RESULTS.json`: real workbook observations and fly-held-out comparison; no artificial neural traces.
- `ANATOMY_AUDIT.json`: retained/effective/omitted contacts and unchanged-axis geometry.
- `ALGEBRAIC_CHECKS.json`: operator proofs/counterexamples, not simulated biological recordings.
- `PERFORMANCE.json`: diagnostic processing cost only.
- `FROZEN_BEFORE.json`, `CANONICAL_BEFORE.json`, `CANONICAL_AFTER.json`, `PRESERVATION.json`: preservation evidence.
- `VALIDATION.json`, `REPRODUCTION.json`, `PACKAGE_MANIFEST.json`: validation and content integrity.

No canonical anatomy ownership is created or duplicated. Root IDs remain strings; anatomy references remain owned by their frozen packages. No evidence is admitted to Brain Spec and no functional claim is upgraded.

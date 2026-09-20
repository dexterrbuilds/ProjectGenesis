# T4/T5 Visual Boundary Identification Study

Isolated direct-physiology study. No Stage-4 rerun, LPLC2 simulation, BrainAdapter changes or Genesis integration.

Start with [REPORT.md](REPORT.md), [SOURCE_DATA_AUDIT.md](SOURCE_DATA_AUDIT.md), [COORDINATES.md](COORDINATES.md), [REPRESENTATION_AND_PRECURSORS.md](REPRESENTATION_AND_PRECURSORS.md) and [VISUAL_BOUNDARY_SPEC.json](VISUAL_BOUNDARY_SPEC.json).

## Frozen outputs

- PLAN / CONDITIONAL_PROTOCOL / TIMING_AUDIT / POLARITY_PROTOCOL and their registrations.
- Original pinned experimental inputs, not author simulated model outputs.
- PARTITIONS, MEASUREMENTS and processed train/test arrays.
- FITS / TRAINING_PROFILE / FIT_FREEZE / PRIMARY_RESULT_LOCK.
- RESULTS / TEST_TRACE_METRICS / PREDICTIVE_RESULTS.csv / PREDICTIONS.npz.
- T4/T5 polarity measurements and saved genuine mean traces, for completed acquired members.
- ROOT_COLUMN_CROSSWALK / EYEMAP_LOCAL_MAP / COORDINATE_AUDIT.
- IDENTIFIABILITY / BASELINE_IDENTIFIABILITY / REPRODUCTION.
- VALIDATION / PRESERVATION / CANONICAL_AFTER / PACKAGE_MANIFEST.

The model predictions in PREDICTIONS.npz are explicitly labeled predictions. Physiological recordings are the voltage arrays in processed files and polarity traces. Neither is LPLC2 activity.

## Reproduction

Run from the repository root with the existing research Python environment. Set `PYTHONDONTWRITEBYTECODE=1` to avoid writing caches into frozen dependencies. NumPy/SciPy are in the research venv; h5py/rdata/xarray and plot dependencies are isolated in this directory's vendor folder. Exact versions are in ENVIRONMENT.json.

```sh
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-t4t5-boundary/test_study.py
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-t4t5-boundary/check.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 .local/fly-stage1-venv/bin/python research/fly-t4t5-boundary/reproduce.py
```

`reproduce.py` reruns the fixed conditional fit and scoring in a new `replay/` directory and compares with frozen originals. It never modifies the original fit/result files or prior studies. It is not new parameter research and does not evaluate Stage 4.

Source reconstruction scripts are retained for audit (`acquire_compact.py`, `acquire_archive.py`, `extract_t4.py`, `process.py`, `polarity.py`, `coordinate_audit.py`). Do not rerun extraction/fitting scripts over accepted outputs as an untracked revision; new analyses require a new directory/protocol. Large public sources are content-addressed, and partial downloads are not measurements. Study dependencies are pinned to Brain Spec 0.1.0 via DEPENDENCIES.json.

## Boundaries

The `fit` file-access guard permits only registered training arrays and its own code/freeze files. Prior workspace files, held-out arrays and raw arrays are denied. Geometry audit reads only pinned anatomy, independently of fitting. Validation tests this boundary and verifies recorded read logs. This is a research reproducibility guard, not a general-purpose adversarial OS sandbox.

Generalization means a held-out biological measurement, not a larger LPLC2 expansion score. Unknown fly identity, retinal mapping, receptor signs and physiology remain unknown. No future boundary has been accepted for deployment.

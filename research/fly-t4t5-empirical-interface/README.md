# Isolated T4/T5 empirical sensory-interface study

Start with [REPORT.md](REPORT.md), [VALIDATION_TABLES.md](VALIDATION_TABLES.md), [SOURCE_AND_COMPATIBILITY.md](SOURCE_AND_COMPATIBILITY.md), and the frozen [INTERFACE_SPEC.json](INTERFACE_SPEC.json)/[SUPPORT_SPEC.json](SUPPORT_SPEC.json).

This is an empirical voltage catalog and restricted interpolation experiment, not a T4/T5 mechanism, LPLC2 simulation or Genesis component. Brain Spec and previous work are unchanged.

## Validation

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-t4t5-empirical-interface/test_interface.py
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-t4t5-empirical-interface/check.py
```

`check.py` validates existing files without rewriting frozen artifacts. The completed `replay/` is retained; `reproduce.py` refuses to overwrite it. To reproduce elsewhere, copy the documented scripts and atlas into a new scratch study directory and run `validate_empirical.py` there. Preserve `PROTOCOL.md`, all freezes, and the old studies.

## Query example

```python
# Run with this directory on sys.path. No canonical runtime is imported.
from interface import EmpiricalInterface
api = EmpiricalInterface()
r = api.rows[0]
q = {k: r[k] for k in ['dataset', 'type', 'family', 'frame',
                       'observation', 'units', 'descriptor', 'recording']}
response = api.query(q)  # Genuine mean voltage and source IDs.
q['FlyWire_root'] = '720575940000000000'
assert api.query(q)['status'] == 'UNKNOWN'
```

The default individual response requires a named source recording. `mode='class_template'` without a recording may expose an eligible weak conditional template; it never assigns an individual root. Missing support returns `voltage_mV: null`.

## Provenance order

Dependency verification → protocol registration → source-only atlas → held-out comparisons → numeric-identity bug correction (initial outputs retained) → primary-result lock → interface tests and fresh-process replay → interface/support freeze → static Stage-4 descriptor audit → preservation/package audit. No Stage-4/LPLC2 execution occurs anywhere in that sequence.

`SOURCE_INPUTS.json` pins measurement inputs. `PREDICTION_METRICS.json` lists each held-out target and training IDs. `ESTIMATOR_ACCESS.json` records the estimator's file reads. `INTERFACE_FREEZE.json` precedes the static stimulus audit. `PACKAGE_MANIFEST.json` provides the final content address. Retain inherited source licenses; this package grants no new commercial rights to source data.

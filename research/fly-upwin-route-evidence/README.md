# Isolated α1 / MBON07 → UpWind route evidence package

Read [REPORT.md](REPORT.md) for the decision, [SOURCE_AUDIT.md](SOURCE_AUDIT.md) for the data audit, and [READINESS.json](READINESS.json) for ten separate readiness requirements.

This is evidence acquisition and static connectivity analysis only. Stage 5 is unauthorized. No neural simulations, fits, decoder, runtime changes or Genesis integration.

- `DEPENDENCIES.json` / `DEPENDENCY_LOCK.json`: exact Brain Spec v0.2 dependency.
- `sources/`, `SOURCE_MANIFEST.json`, `AUXILIARY_SOURCES.json`: unchanged authoritative source artifacts and hashes.
- `processed/`, `WORKBOOK_INVENTORY.json`, `MEASUREMENT_AUDIT.json`, `ALPHA1_CONDITIONING_AUDIT.json`: source-cell provenance and descriptive checks.
- `ANATOMY_AUDIT.json`, `CROSSWALK.json`: pinned graph references, identities, directed counts, omitted boundaries and explicit unknowns.
- `PREPARATION_COMPATIBILITY.json`, `EVIDENCE_LEDGER.json`: scoped evidence, incompatible observations and unresolved bridges.
- `VERIFICATION.json`, `CANONICAL_BEFORE.json`, `CANONICAL_AFTER.json`: preservation and tests.
- `RELEASE.json`: package content address; originals and prior releases are not overwritten.

Validation only (no network, database writes or neural runs):

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/mac/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 research/fly-upwin-route-evidence/validate.py
```

Source processing scripts are included for reproducibility. They do not identify physiological parameters or generate neural activity. `begin.py` intentionally refuses to replace the preservation baseline. Do not rerun builders on a frozen package; any later evidence belongs in a separately reviewed successor.

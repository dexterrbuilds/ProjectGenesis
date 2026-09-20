# Biological Neural Specification v0.2.0

Read [GENESIS_BRAIN_SPEC.md](GENESIS_BRAIN_SPEC.md) and [STAGE5_READINESS.md](STAGE5_READINESS.md).

`RELEASE.json` pins the registry, historical parent and specification sidecars. `PACKAGE_MANIFEST.json` hashes the complete release package. `ADMISSION_REVIEWS.json` contains entry-specific review records; `REVIEW_AUTHORIZATION.md` states their actual authority and limits. v0.1 and all predecessor experiments remain unchanged.

## Verify without running neural models

```sh
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/genesis-brain-spec-v0.2/check.py
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/genesis-brain-spec-v0.2/test_governance.py
```

The first command verifies files, governance and the published package. It reads no live database and imports no neural model/runtime. The separate canonical snapshots were made using the existing read-only database audit. Tests mutate in-memory fixtures, never historical evidence.

Do not rerun builders against a published release. Future changes belong to a reviewed successor. Inherited relative identity-object paths are anchored to `research/genesis-brain-spec-v0.1/`, explicitly referenced by the release; no duplicate anatomy store is created here.

## What this permits

Using the exact reviewed constraints as dependencies in later authorized research. It does not authorize Stage 5, implement a sensory adapter, reconcile shared physiological rules, simulate an organism or admit a biological capability.

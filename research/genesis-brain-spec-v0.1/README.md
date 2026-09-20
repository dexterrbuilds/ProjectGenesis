# Biological Neural Specification v0.1

Start with [GENESIS_BRAIN_SPEC.md](../../GENESIS_BRAIN_SPEC.md). This directory is evidence infrastructure, with no neural simulation imports or Genesis integration.

## Files and trust boundaries

- `RELEASE.json` points to the immutable SHA-256-addressed registry object; each registry entry is separately hashed.
- `objects/` holds that registry, a derived neuron **annotation index**, and a mechanism-profile index. None is a second owner of canonical anatomical connections.
- `MECHANISM_PROFILES.json` points to 11 evidence profiles; `EVIDENCE_INDEX.md` lists all 151 registry entries.
- The canonical aggregate anatomy remains `../fly-representation-study/identity-registry.jsonl.gz`; both it and `shared-row-ids.json` are referenced by pinned path/hash.
- `FROZEN_INPUTS.json` protects 3,848 prior files. `RESUMED_WORK.json` preserves all work present at continuation, including the original builder and validator.
- `validate.py` is the original release validator. `policy.py` adds final semantic/admission checks; **`check.py` is the complete public validation command**.
- `test_spec.py` exercises invalid promotions, provenance, ownership, product leakage and supersession. It never imports or runs a neural model.
- `EXPERIMENT.example.json` demonstrates dependency declarations. It is a preflight-only example, not Stage 4 or an executable experiment.
- `SPEC_MANIFEST.json` content-addresses the completed package, including the root specification document. `VERIFICATION.json` records completion checks.

All paths below are run from the repository root, with standard Python 3; no installation or model environment is needed.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/genesis-brain-spec-v0.1/check.py --package
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s research/genesis-brain-spec-v0.1 -p 'test_*.py' -v
PYTHONDONTWRITEBYTECODE=1 python3 research/genesis-brain-spec-v0.1/check.py --experiment research/genesis-brain-spec-v0.1/EXPERIMENT.example.json
```

`build.py` and `complete.py` deterministically synthesize/index the existing frozen data. Both refuse to overwrite differing artifacts. They contain no fitting or simulation. Normal consumers only need `check.py`; do not regenerate frozen studies.

## Reading an entry

```python
import json
from pathlib import Path
p = Path("research/genesis-brain-spec-v0.1")
release = json.loads((p / "RELEASE.json").read_text())
registry = json.loads((p / release["registry"]["path"]).read_text())
entries = {e["id"]: e for e in registry["entries"]}
print(entries["sign.mbon07-pam11"])
print(entries["capability.persistence"])
```

An entity's fact category concerns anatomical identity only. Facets either point to separately categorized/scoped claims or explicitly retain unknowns. `known_nt` and automated `top_nt` annotations stay distinct. Parameters retain the exact historical audit record; a constrained class/sign does not make the numerical parameter a physiological estimate. Supplement profiles are indexes of these existing claims, not independent evidence.

## Future experiments

Pin `registry_sha256` and each dependency's entry digest. `uses` must be a subset of declared dependencies. Inputs use a limited physical/synthetic vocabulary with units, category and evidence. Anatomy views are references. Any proposed assumptions remain explicitly unvalidated. `result_claims` must be empty: an experiment cannot grant itself new accepted capabilities.

The current release approves no executable unified physiological operators. Root-specific local states are proposals only, and shared conflicting KC→MBON rows cannot receive a composed state assignment. Historical isolated models remain intact; this preflight contract does not retrospectively rewrite their operators.

## Future superseding evidence

The CLI accepts an append-only candidate release plus a separate review-admission file:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/genesis-brain-spec-v0.1/check.py --revision path/to/candidate.json --review path/to/review.json
```

The candidate retains every frozen entry, study classification and source. It appends a new claim with `supersedes: [{id, sha256, reason}]`, a new version, new pinned independent evidence and updated entry hashes. A review record binds `entry_id`, `entry_sha256`, `reviewer`, UTC `reviewed_at`, `rationale`, `scope`, `independent_evidence_refs` and the exact supersession list. A renamed old source is rejected. No candidate is automatically published or used by Genesis.

The review file is an explicit **human governance artifact**, not an authenticated signature. Protect it and release publication in code review. Validators cannot assess arbitrary prose, detect every euphemism for a hidden input, verify reviewer honesty or prove biological truth. They enforce structured categories, pinned provenance, explicit scope, ownership and change rules. A new schema/operator/capability admission requires separate scientific/schema review; this release's claim-admission CLI does not silently approve one.

`SPEC_MANIFEST.json` is tamper-evident, not write-once storage. Check its trusted digest in review/version control. Its own `content_sha256` hashes the canonical JSON payload excluding that field; listed files are hashed as exact bytes. JSON objects use sorted keys and compact separators for content-addressed objects and entry hashes, UTF-8 and finite JSON numbers. Object files have a trailing newline included in their file hash. Do not confuse an entry's canonical-object hash with its enclosing file hash.

No new biological result is claimed by passing these infrastructure tests.

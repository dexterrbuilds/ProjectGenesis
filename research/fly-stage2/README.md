# Isolated FlyWire Stage-2 familiarity research

**Result: PARTIAL-INCONCLUSIVE.** The tiny local neural-memory effect is reproducible
and mechanism-dependent, but misses the prospective effect-size criteria. It is
strongly affected by boundary normalization. Read [REPORT.md](REPORT.md); passing
implementation checks does not mean Stage 2 passed.

No Genesis integration. No novelty API, BrainAdapter, LLM, database, scheduler,
wallet, external tools or Stage 3. Stage-1 files and canonical state remain frozen.

## Run offline from repository root

Python 3.12 with the pinned [requirements.txt](requirements.txt). The existing
`.local/fly-stage1-venv` is compatible; no package/environment changes were needed.
Commands below set `PYTHONDONTWRITEBYTECODE=1` to avoid modifying Stage-1 pycache
when running the independent comparison.

```sh
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-stage2/test_harness.py

PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-stage2/evaluate.py \
  --circuit research/fly-stage2/artifacts/43a18b787748363e6c6080513cf4d5455b6949bf9a28f09ffab978787195e0b3 \
  --evidence research/fly-stage2/evidence/a96e2ca39eedde231be3a54c3e26d87a0e5a8f33c1801bc4a01906159da9c079 \
  --output outputs/flywire-stage2/reviews
```

The evaluator verifies content hashes and launches 18 clean-environment,
fresh-process sensory-only recalls. Scientific classification is printed separately
from implementation assertions. `PARTIAL-INCONCLUSIVE` is a valid research result.
Absolute numerical replay tolerance: 1e-10 across compatible environments; recorded
same-environment replays are bit-identical. No cross-platform bitwise guarantee.

To produce a new full 60-condition run without replacing accepted evidence:

```sh
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-stage2/experiment.py \
  --circuit research/fly-stage2/artifacts/43a18b787748363e6c6080513cf4d5455b6949bf9a28f09ffab978787195e0b3 \
  --output outputs/flywire-stage2/reproductions
```

Use `recall.py --help` for a single snapshot. Supply that run's `recall-config.json`
and `trained.json.gz` (or `fast-reset.json.gz` / `initial.json.gz`). Configuration
contains only model parameters, intervention/seed and sensory PN root patterns;
no training count, novelty/reward label, outcome score or seen flag is passed.

### Extraction

Original local cache: `outputs/flywire-research/`; source download URLs, source
checksums, annotations, licenses and selection rationale are pinned in the manifest.
Stage 1's raw cache is read without modification. Re-extract into a separate folder:

```sh
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-stage2/extract.py \
  --cache outputs/flywire-research --output outputs/flywire-stage2/re-extraction
```

The content address must remain `43a18b78…8195e0b3` in the pinned environment. No
anatomy is downloaded or fabricated by a model run. Roots remain strings in JSON.
The extractor includes every selected-to-selected anatomical row, not only those
used by the hypothesized familiarity mechanism. Coarse neuropil labels do **not**
establish exact α′3 receptor localization; this is a reported limitation.

### Limited reward comparison

```sh
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-stage2/reward_comparison.py
```

This creates a new content-addressed directory under `research/fly-stage2/reward-evidence`.
It reads frozen Stage-1 code/anatomy and creates entirely separate in-memory models.
It never opens canonical Genesis state. **Two preparations are not one combined
brain.** A zero reward interaction in the isolated α′3 arm follows the protocol;
it does not demonstrate biological independence of familiarity and value.

## Files and data interpretation

- `PLAN.md`, `FACTORIAL_PLAN.md`: prospectively recorded rules and limitations.
- `FROZEN_BEFORE.json`, `CANONICAL_BEFORE.json`, `PRESERVATION.json`: preservation evidence.
- `extract.py`, `artifacts/`: real circuit, full boundary contacts and immutable manifest.
- `model.py`: independent rates, local DA-gated efficacy and explicit recovery hypothesis.
- `experiment.py`, `evidence/`: 60 conditions, numeric timestamped sensory inputs,
  pre/post/reset snapshots, genuine traces and per-neuron probe vectors.
- `recall.py`, `evaluate.py`, `evaluations/`: replay/memory/integrity/acceptance audit.
- `reward_comparison.py`, `reward-evidence/`: limited shared-PN, separate-preparation factorial.
- `test_harness.py`: nine implementation checks, distinct from scientific acceptance.
- `RESULTS.csv`, `NEURON_RESULTS.csv`, `REPORT.md`: quantitative evidence and interpretation.
- `document_results.py`: renders report tables from this saved evidence collection.

`trace.npz` has sampled `seconds`, `group_names`, `group_rates`, `mean_multiplier`.
For the two seed2701 primary runs, `rates` and `plastic` contain individual neuron
and plastic-edge histories, indexed by `root_ids` and `plastic_edge_indices`.
Other runs intentionally have empty dense arrays, not fake individual activity.
All have `probe-rates.npz` with full per-neuron baseline/post/reset/recovery vectors.
Recovery intervals are analytic updates in an explicitly silent preparation, not
continuously simulated spontaneous fly activity. Rates are unitless model values.

Files are hash-verified and never overwritten with different content at an existing
content address. This is not filesystem WORM storage. Source licensing limitations
remain in the manifest; do not treat this local research as commercial data clearance.

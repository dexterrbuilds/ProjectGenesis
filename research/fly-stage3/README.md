# Stage 3 — isolated motivation/resource/persistence research

Read REPORT.md for the final scientific classification and evidence. This is a new
research preparation, not a BrainAdapter, artificial organism, behavior policy or
Genesis migration. Stage 1 and Stage 2 are frozen and remain unchanged.

## Scientific separation

- **BIOLOGICAL FACT:** pinned chemical anatomy, literature-supported circuit roles
  and direction of selected state effects. See LITERATURE.md for reverified
  crosswalks, uncertain LH aliases and contradictory simplifications.
- **COMPUTATIONAL MODEL:** unitless rate dynamics, local dopamine/efficacy rule,
  signs/gains, slow resource boundary and imposed OA stimulation. None is a
  physiological measurement of hunger, molecular receptors or feeding in this fly.
- **GENESIS MAPPING:** none. No money, task-quality score, persistence label, LLM,
  planner, canonical state, internet tool or autonomous runtime enters a trial.

The model accepts only numeric current vectors plus a bounded resource input.
Experiments provide stable PN patterns/timing and, in acquisition-surrogate arms,
a specified OA-VPM4 current. There is no `continue`, `give_up`, `worth_it`, `failure`
rule or action decoder. No-cue inactivity is reported as inactivity, not a voluntary
choice. Sustained activity under a sustained cue is not sufficient for persistence.

## Reproduce offline

Python 3.12, requirements.txt (same pinned NumPy/SciPy/PyArrow versions as earlier
research). The existing isolated `.local/fly-stage1-venv` is compatible. No npm or
web/runtime deployment changes are needed. From repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-stage3/test_harness.py

PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-stage3/experiment.py \
  --circuit research/fly-stage3/artifacts/28cc6285ba4b40077db73952bacee75d0938f2f80021aaf89c214524797b2a52 \
  --output outputs/flywire-stage3/reproductions
```

The full battery runs 122 conditions. Twelve primary conditions each replay the
same 240-second acquisition. Counterbalanced resource states use identical sensory
current schedules; condition order is fixed by its own seed. No outcome screening.
The evaluator checks saved content hashes, thresholds and clean-process recall:

```sh
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-stage3/evaluate.py \
  --circuit research/fly-stage3/artifacts/28cc6285ba4b40077db73952bacee75d0938f2f80021aaf89c214524797b2a52 \
  --evidence research/fly-stage3/evidence/07ac1e4903fcfdd4a911653a17046acb2f3b5042360eb8972d9f7c5891e605bd \
  --output outputs/flywire-stage3/reviews
```

Use the full evidence address in REPORT.md. Implementation test success is distinct
from scientific acceptance. Same-environment deterministic neural replay should be
bit-identical; the declared compatible-environment tolerance is 1e-10. Recorded
wall-clock time is not part of neural replay equality.

## Learned-state transfer

```sh
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-stage3/learned_state.py
```

This reads accepted Stage-1 snapshots and copies only their actual KC→MBON07 efficacy
rows onto matching Stage-3 anatomy. Contacts must match exactly. It does not change
Stage-1 files, import episodic memory into the model, run new Stage-1 training or
import the old fast state. New outcomes belong exclusively to Stage 3. Opposite
pairing histories A/B, naive/trained, low/high resource and PPL101/MBON11/modulation
controls are recorded. Original Stage-1 efficacy semantics are not assumed to
validate their expression in this larger context.

## Provenance and anatomy

```sh
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-stage3/extract.py \
  --cache outputs/flywire-research --output outputs/flywire-stage3/re-extraction
```

Uses original checksum-verified v783 connections/proofread roots and v3.1.0
annotations. Source URLs/checksums and licensing caveats are in the manifest. JSON
root IDs remain strings. Every observed induced contact is retained; full external
boundary contacts are recorded, not fabricated or silently filled in. `audit_anatomy.py`
reports per-population retention, actual named-pathway contacts, uncertain identities,
coarse neuropil locations, Stage-1/2 overlaps and numerically zeroed edges.

Resource gating is not a peptide anatomical edge. OA current is an experimental
surrogate at a named neuron, not evidence that the omitted gustatory pathway was
reconstructed. Prediction labels do not supersede known physiology: KCs are modeled
cholinergic despite problematic automatic transmitter predictions; unresolved
MBON07 glutamate targets and other OA fast effects are zeroed and documented.

## Inspect genuine state

Each main run saves numeric stimuli, model configuration, initial/trained/fast-reset
snapshots, summary and `trace.npz`. Group rates are sampled every100 ms; two primary
runs additionally save actual individual rates/efficacies every1 s as float32 traces.
Integration and snapshots use float64. Empty dense arrays mean no individual trace
was saved, never invented activity. `probe-rates.npz` saves actual individual-neuron
baseline/post/reset responses. No animation is generated.

`recall.py` reads only circuit/configuration/snapshot and the same sensory PN currents.
It never reads training reports, acquisition history, outcome scores or a database.
Its inherited environment is cleared for the automated fresh-process checks.

Artifacts are content-addressed and hash-verified; this is not filesystem WORM.
New main/reward runs create new addresses. Reports and CSVs are derived summaries.
Do not repurpose this research module as a deployed motivational controller. Stop
for scientific review; no threat, sleep/arousal or Genesis integration is included.

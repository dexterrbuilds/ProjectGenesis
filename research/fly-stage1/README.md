# Isolated FlyWire Stage-1 research harness

**Final classification: PASS for the narrow appetitive model experiment.**
Read [REPORT.md](REPORT.md) for quantitative results, the inconclusive aversive
interpretation and scientific limits. This module is not connected to Genesis.

## Files

- `PLAN.md`: recorded selection/protocol/acceptance plan.
- `extract.py`: checksum-verified, deterministic extraction from original sources.
- `model.py`: anatomy-constrained rate dynamics and persistent dopamine-gated LTD.
- `experiment.py`: counterbalances, interventions, boundaries, replay and real traces.
- `recall.py`: fresh-process cue-only recall; no training/episode input.
- `evaluate.py`: audits immutable results, tests acceptance and performs isolated recall.
- `test_harness.py`: ten integrity/mechanism tests against the real extraction.
- `artifacts/`: content-addressed circuit, retained contacts and omitted-boundary data.
- `evidence/`: content-addressed 76-run records, neural snapshots, numeric stimuli and traces.
- `evaluations/`: content-addressed acceptance audit and individual-neuron recall.
- `RESULTS.csv`: flat, human-readable export of every recorded condition.

No Genesis files, environment secrets or database are read by these programs.
Extraction reads local downloaded data; the model and experiments make no network
requests. They do not import or implement a BrainAdapter.

## Reproduce from the repository root

Use Python 3.12. Create a separate environment; this does not change npm dependencies:

```sh
python3.12 -m venv .local/fly-stage1-venv
.local/fly-stage1-venv/bin/python -m pip install -r research/fly-stage1/requirements.txt
.local/fly-stage1-venv/bin/python research/fly-stage1/test_harness.py
```

Audit the saved evidence and reproduce cue-only recall without rerunning training:

```sh
.local/fly-stage1-venv/bin/python research/fly-stage1/evaluate.py \
  --circuit research/fly-stage1/artifacts/c5c332c1bd0ce77487ad5765756a58dc441d50f59dc56899a462bf35e4b2a157 \
  --evidence research/fly-stage1/evidence/4afc692f113981d1ad1a035ba7293e00bb4c8964bc1e87d9b00fab8063037c4b \
  --output outputs/flywire-stage1/review
```

Reproduce the full battery, writing a new evidence collection rather than replacing
the preserved run:

```sh
.local/fly-stage1-venv/bin/python research/fly-stage1/experiment.py \
  --circuit research/fly-stage1/artifacts/c5c332c1bd0ce77487ad5765756a58dc441d50f59dc56899a462bf35e4b2a157 \
  --output outputs/flywire-stage1/reproductions
```

Wall time and machine metadata naturally change the evidence-directory hash.
Neural replay is evaluated separately from performance metadata. Numerical replay
was exact on the recorded environment; 1e-10 is the declared compatible-environment
tolerance, not a promise of cross-platform bit identity.

### Re-extract the same anatomy

The original source cache is ignored by Git. Download originals under
`outputs/flywire-research` from the URLs in the manifest:

```sh
mkdir -p outputs/flywire-research
curl --fail -L -o outputs/flywire-research/proofread_connections_783.feather \
  https://zenodo.org/api/records/10676866/files/proofread_connections_783.feather/content
curl --fail -L -o outputs/flywire-research/proofread_root_ids_783.npy \
  https://zenodo.org/api/records/10676866/files/proofread_root_ids_783.npy/content
curl --fail -L -o outputs/flywire-research/annotations-v3.1.0.tsv \
  https://raw.githubusercontent.com/flyconnectome/flywire_annotations/v3.1.0/supplemental_files/Supplemental_file1_neuron_annotations.tsv
.local/fly-stage1-venv/bin/python research/fly-stage1/extract.py \
  --cache outputs/flywire-research --output outputs/flywire-stage1/re-extraction
```

The large original connection table is approximately 852 MB. Extraction requires
more RAM than simulation. Published source checksums are checked before processing.
The resulting manifest must match `c5c332c1…b2a157` in the pinned environment.
Content-addressed files are never overwritten with different content; the loader
rejects a modified artifact. This is hash-verified immutability, not filesystem WORM.

## Read genuine activity

Each experiment directory has `stimuli.json`, `initial.json.gz`, `trained.json.gz`,
`summary.json`, and `trace.npz`. `seconds` is simulated time; `group_rates` contains
observed rates indexed by `group_names`. In the four dense runs, `rates` indexes
`root_ids` and `plastic` indexes anatomical `plastic_edge_indices` in `circuit.json`.
Other runs have empty dense arrays and genuine population traces, not fabricated
individual-neuron activity. Traces sample every 100 ms; integration runs at 10 ms,
or 5 ms in the timestep control. Recall reads and updates the saved neural state
with sensory current alone; no teaching input is accepted by `recall.py`.

## Scientific/data use

Keep biological observations, computational approximations and product mappings
separate. There are **no Genesis mappings** in Stage 1. The circuit is a limited
stimulated preparation; it is not a complete mushroom body, a behavioral fly model,
or evidence of consciousness. See the report for licensing discrepancies and
attribution before redistributing derived data commercially. Do not deploy this
research module or advance to Stage 2 without separate review.

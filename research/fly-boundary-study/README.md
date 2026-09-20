# Drosophila Boundary-Closure and Brain Architecture Study

Not Stage 4. See REPORT.md for quantitative results and the architecture recommendation.
No Genesis integration; frozen Stages 1–3 and canonical organism are preserved.

## Structure

- PLAN.md: anatomical selection and comparisons fixed before expanded outcomes.
- anatomy/: compact indexed v783 contacts, original root strings, cell annotations,
  per-stage L0–L4 selections, inclusion reasons, counts and hash manifest.
- context.py: reads frozen kernels and attaches an explicitly assumed fast operator
  on observed added connections. Original plastic edges and cues stay fixed.
- runs/: actual traces, stimuli, snapshots, per-condition hashes and measurements.
- INTEGRATION.json: actual cross-population contacts, example shortest paths and
  strongest omitted partners. Paths are not interpreted as behavioral mechanisms.
- benchmarks/: full-reference timing, RSS, numeric traces and checkpoints.
- ANALYSIS.json / TRAJECTORIES.csv: measurements, never model inputs.
- SCIENCE.md: anatomy / computational approximation / Genesis-mapping separation.

## Reproduce in isolation

Use the existing `.local/fly-stage1-venv` or the pinned requirements from Stage 3.
Always set PYTHONDONTWRITEBYTECODE=1 to avoid writing into frozen stages on import.
From repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-boundary-study/check_kernel.py
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-boundary-study/run.py --stage 2 --level 1
```

A sealed existing run is verified and skipped. To repeat simulations, use an isolated
copy of this research directory with a separate runs destination; do not delete or
overwrite accepted artifacts. Exact sensory roots remain those of each original
seed, even as context expands. The runtime has no canonical Genesis dependency.

`benchmark.py --dt 0.005`, `--dt 0.01`, and `--dt 0.02` measure actual full-brain
updates in fresh processes. Benchmark output directories are create-only. No time
steps are skipped. Timings include other ordinary host activity and are not cloud
capacity guarantees. The generic benchmark and frozen-kernel extension pilot have
different operators and should not be presented as interchangeable speed estimates.

The extraction reads only checksum-verified cached originals in
outputs/flywire-research. Its manifest records source hashes, annotation version and
exact compact arrays. All JSON roots are strings; integer index conversion explicitly
uses uint64 on both sides to avoid signed/unsigned promotion losing root-ID precision.
Full chemical anatomy is kept even where an unresolved transmitter has zero fast
weight. No fabricated edges, tonic current rescue or post-result parameter fitting.

No source data deployment or publication is performed. Prior licensing caveats
remain unresolved for commercial redistribution. Stop for review after this study.

## Class-consistent amendment

CLASS_CONTEXT_AMENDMENT.md was fixed before its simulations. The generic context
operator cannot recruit new KCs because its maximum drive is below their threshold.
That mathematical limitation motivated an additive comparison using original class
transmission gains on identified added connections. `class_context.py` and
`run_class.py` save separate `class-runs/`; they never replace generic runs. L0 is
reused, L1/L3 run counterbalanced primary protocols, and L2 contains mechanism and
assumption controls. New KCs remain outside the original plastic compartments.
Zero sparse entries are eliminated with exact numerical-equivalence checks. This
is a representation optimization; no neural time steps or nonzero edges are skipped.

MECHANISM_OVERLAP.json counts shared anatomical plastic rows. A shared graph needs
one coherent rule per connection; overlapping stage-specific rules are not summed.

## Completed study

**Recommendation: INSUFFICIENT EVIDENCE.** All 156 scheduled conditions are sealed:
100 conservative-context conditions and 56 class-consistent conditions. No additional
behavioral capability or Genesis integration is included. See the full [report](REPORT.md),
[family comparison and participation measurements](SYNTHESIS.json), and
[shared-state conflicts](UNIFIED_MODEL_CONFLICTS.md).

The complete final analysis can be regenerated from saved evidence without running
neural experiments:

```sh
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-boundary-study/analyze.py
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-boundary-study/synthesis.py
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-boundary-study/report.py
PYTHONDONTWRITEBYTECODE=1 .local/fly-stage1-venv/bin/python research/fly-boundary-study/enrich_report.py
```

Reports are derived; original run directories and their checksums remain immutable.
STUDY_MANIFEST.json seals the completed study including source and derived documents.
For subsequent analysis, use a separate output directory and preserve this manifest.

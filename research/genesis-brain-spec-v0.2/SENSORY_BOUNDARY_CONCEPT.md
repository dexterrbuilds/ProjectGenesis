# Observation-aware sensory-boundary contract (specification only)

A future biological research adapter may expose empirical measurements or bounded empirical estimates without claiming to simulate the circuitry that produced them. This document defines metadata and refusal obligations. It defines no executable adapter, neural state update, BrainAdapter method, or runtime connection.

## Required envelope

| Field | Required meaning |
|---|---|
| Observation type | Explicit recorded quantity and compartment: e.g. baseline-subtracted somatic voltage, not generic activation |
| Units and time | Physical/measurement units, baseline convention, time origin, supported horizon and sampling/resampling provenance |
| Preparation | Species, sex/age where known, genotype/driver, recording technique, indicator where relevant, body/recording conditions; unknowns explicit |
| Support domain | Joint physical descriptor tuples, frames and source preparations; interpolation rule and validation evidence, not a Cartesian product of marginal ranges |
| Provenance | Dataset version, immutable measurement/source hashes, recording identities, contributing observations and release/evidence dependencies |
| Uncertainty | Error definition, calibration unit, holdout identity, numerical interval if identified; unknown/unbounded as null with reason; no implicit zero variance |
| Identity resolution | Recording, class, subtype, column, fly and root separately; each transfer needs an independently audited crosswalk |
| OOD status | Measured / interpolation-supported / weak / out-of-distribution-or-unknown; no output when requested inference lacks support |
| Representation scope | Empirical retrieval/estimate versus mechanistic neural model; omitted circuits remain omitted |

## Frozen T4/T5 instance limits

- Exact source-recording/full-tuple retrieval is **DIRECTLY MEASURED**. It does not establish prediction.
- **INTERPOLATION-SUPPORTED** is restricted to the frozen passing strata and strict, source-tested, one-axis brackets. No extrapolation or mixed-axis/family inference.
- Eligible conditional class templates are **WEAKLY SUPPORTED**, even when a recording-held-out comparison passes. They require an explicit template request and cannot masquerade as a new individual's physiology.
- **OUT OF DISTRIBUTION / UNKNOWN** includes unsupported frames, preparations, families, identity transfers and observation conversions. The frozen source also returns UNKNOWN with a weak-support diagnostic for some unvalidated interpolation requests; neither tag permits a numerical individual response. A consuming specification must treat UNKNOWN status as overriding a weak-support annotation. This release does not patch the historical implementation.
- Output is mean baseline-subtracted **somatic mV over 0–500 ms**, on the source's documented/resampled 1 ms grid. Original sampling resolution is retained in provenance.
- Calcium, spikes, release, synaptic current and model rate conversion are all unidentified. No zero, gain, monotone transform or fitted downstream utility substitutes for their missing observation mapping.
- Fly, subtype, column and FlyWire-root assignment are unavailable. Author RF/PD localizers do not establish a screen/head/retinal transform.
- All 16 frozen Stage-4 physical conditions remain OOD. No empirical output is authorized for them.

The empirical package supplies no new canonical anatomy owner, no physiological kernel, no action decoder and no learning state. Its supported statistical comparisons are not biological-model capabilities. Future adapters must preserve the five evidence categories and pin the exact specification and source versions they rely on. New support regions require prospective independent validation and explicit reviewed admission in a successor release.

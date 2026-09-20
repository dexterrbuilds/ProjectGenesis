# Measured computational scaling

These are **engineering envelopes**, not calibrated neural simulations. Specifications were recorded before measurement in REPRESENTATIONS.md. All runs use pinned real FAFB rows; no new extraction, neural skip, adaptive update schedule or biological behavior is involved.

| Context / envelope | Roots | Local states | Anatomical rows | Contacts | Candidate plastic rows | Updates/s | Peak RSS MiB | Saved dynamic state MiB |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| s1 R0 | 1,054 | 1,054 | 102,889 | 226,143 | 5,675 | 7189.78 | 349.6 | 0.008 |
| s1 R1 | 1,054 | 7,670 | 102,889 | 226,143 | 5,675 | 5200.92 | 413.2 | 0.059 |
| s1 R2 | 1,054 | 7,670 | 102,889 | 226,143 | 5,675 | 2527.78 | 411.7 | 0.321 |
| s2 R0 | 1,172 | 1,172 | 73,715 | 160,848 | 4,533 | 11952.67 | 414.8 | 0.009 |
| s2 R1 | 1,172 | 7,503 | 73,715 | 160,848 | 4,533 | 6684.94 | 415.2 | 0.057 |
| s2 R2 | 1,172 | 7,503 | 73,715 | 160,848 | 4,533 | 2389.50 | 415.2 | 0.298 |
| s3 R0 | 4,563 | 4,563 | 375,699 | 905,536 | 22,878 | 2203.61 | 421.8 | 0.035 |
| s3 R1 | 4,563 | 29,777 | 375,699 | 905,536 | 22,878 | 1252.05 | 422.0 | 0.227 |
| s3 R2 | 4,563 | 29,777 | 375,699 | 905,536 | 22,878 | 602.34 | 421.8 | 1.258 |
| integrated R0 | 37,913 | 37,913 | 6,696,367 | 22,458,018 | 89,315 | 94.21 | 442.1 | 0.289 |
| integrated R1 | 37,913 | 229,679 | 6,696,367 | 22,458,018 | 89,315 | 78.27 | 621.2 | 1.752 |
| integrated R2 | 37,913 | 229,679 | 6,696,367 | 22,458,018 | 89,315 | 61.91 | 494.3 | 8.372 |
| full R0 | 139,255 | 139,255 | 16,847,997 | 54,492,922 | 89,315 | 35.10 | 707.3 | 1.062 |
| full R1 | 139,255 | 435,774 | 16,847,997 | 54,492,922 | 89,315 | 22.87 | 896.4 | 3.325 |
| full R2 | 139,255 | 435,774 | 16,847,997 | 54,492,922 | 89,315 | 13.71 | 1040.2 | 14.662 |

## Timing, storage and reproducibility

| Context / envelope | Initialization s | 100 updates s | CPU % of one core | Replay s | Checkpoint MiB | Write / load ms |
|---|---:|---:|---:|---:|---:|---:|
| s1 R0 | 1.479 | 0.014 | 98.5 | 0.012 | 0.008 | 0.80 / 1.36 |
| s1 R1 | 0.516 | 0.019 | 95.2 | 0.021 | 0.059 | 1.24 / 1.00 |
| s1 R2 | 0.526 | 0.040 | 98.7 | 0.040 | 0.322 | 1.10 / 1.59 |
| s2 R0 | 0.511 | 0.008 | 99.4 | 0.009 | 0.009 | 0.74 / 1.01 |
| s2 R1 | 0.497 | 0.015 | 98.5 | 0.014 | 0.057 | 2.32 / 1.38 |
| s2 R2 | 0.535 | 0.042 | 88.2 | 0.301 | 0.300 | 4.66 / 4.86 |
| s3 R0 | 0.623 | 0.045 | 97.4 | 0.046 | 0.035 | 0.78 / 0.97 |
| s3 R1 | 0.684 | 0.080 | 98.4 | 0.078 | 0.227 | 0.73 / 0.89 |
| s3 R2 | 0.645 | 0.166 | 93.4 | 0.172 | 1.259 | 1.92 / 2.32 |
| integrated R0 | 3.737 | 1.061 | 93.9 | 1.030 | 0.289 | 44.83 / 29.43 |
| integrated R1 | 5.649 | 1.278 | 98.6 | 1.334 | 1.753 | 3.52 / 6.11 |
| integrated R2 | 6.978 | 1.615 | 97.8 | 1.726 | 8.374 | 8.14 / 11.94 |
| full R0 | 8.365 | 2.849 | 99.0 | 3.084 | 1.063 | 2.87 / 2.63 |
| full R1 | 14.469 | 4.372 | 98.4 | 4.451 | 3.325 | 9.50 / 10.54 |
| full R2 | 39.717 | 7.296 | 93.9 | 7.218 | 14.663 | 16.06 / 17.67 |

All15 runs completed100 updates plus100 identical replay updates, were finite, and restored checkpoints exactly. Timing is sequential by benchmark case; unrelated source reading/tests can affect host load. Each case has one timed run and one replay, not a statistical cloud benchmark. Platform: macOS27.2 arm64, NumPy2.3.5/SciPy sparse. Hardware brand/memory query was sandbox-blocked; no invented CPU model or cloud equivalence.

Peak RSS includes Python metadata, loading/construction and temporaries; it is not minimum deployment RAM. Small cases read/mask full-source arrays, inflating their peak relative to their final working sets. R0/R1 run code allocates unused auxiliary buffers too, so peaks are conservative for those envelopes. Explicit retained-array footprints and dynamic-state bytes are separately recorded in result.json. Integer count rows are retained, CSR coalesces identical endpoints for R0 only. Count/neuropil identity remains in the underlying immutable source.

R2 plastic candidate counts cover annotated KC→MBON rows, not all contacts or all neurons. No claim that these are the only plastic sites in a full brain. Dynamic checkpoints omit immutable anatomy/identity/parameters, which must be retained by source/specification hashes; a complete future checkpoint would also need clock, input replay and PRNG state. These deterministic100-step workload tests have no PRNG after construction.

## Temporal cost, not temporal accuracy

| R2 context | At dt10ms: simulated/wall | At dt1ms | At dt0.1ms |
|---|---:|---:|---:|
| s1 | 25.278 | 2.5278 | 0.25278 |
| s2 | 23.895 | 2.3895 | 0.23895 |
| s3 | 6.023 | 0.6023 | 0.06023 |
| integrated | 0.619 | 0.0619 | 0.00619 |
| full | 0.137 | 0.0137 | 0.00137 |

These columns are arithmetic workload mappings, **not** validated numerical time steps. The fixed coefficients define an engineering recurrence, not physiology in seconds. Full R2 at1ms requires roughly73 wall seconds per simulated second on this host; integrated R2 requires roughly16.2. This implementation does not support continuous real-time1ms operation at either size. That does not prove impossibility with a different solver/hardware or scientifically justified slower time scale. The small circuits are much cheaper.

## State accounting and R3 uncertainty

Let C be local states and P plastic rows. Float64 dynamic state is8C bytes for E0/E1 and8(4C+2P) for E2. A sparse transmission matrix costs approximately12E+4(C+1) bytes with float64 values/int32 indices, besides row provenance, local-state mapping and construction arrays. Every extra scalar per anatomical row costs8E bytes: full reference134,783,976 bytes (~128.5MiB). Two variables per individual contact, if justified and contact IDs existed, would cost16×54,492,922=871,886,752 bytes (~831.5MiB), before activity, anatomy or other physiology.

No calibrated R3 operator exists to time. With K channel/receptor variables per local electrical section, state alone is8C(1+K), plus plasticity and sparse axial/synaptic operators; implicit solvers/delays add storage. As a bookkeeping scenario, four voltage/gating variables per root at1/10/100 sections per root require32N/320N/3200N bytes: for139,255 roots4.25/42.50/424.97MiB, respectively, before edges and plasticity. These section counts are not anatomical estimates. The published MBON14 morphology has4,336 dendritic sections for one neuron; it cannot be multiplied indiscriminately across the brain. R3 throughput and required dt remain unidentified, and the old~0.7GiB scalar benchmark provides no guarantee.

Full-root neuropil-local representation has435,774 states (~3.13/root); integrated has229,679 (~6.06/root). This finite anatomical partition is convenient for a cost envelope, but misses finer functional compartments and invents no validated intracellular dynamics. Heterogeneous selective compartmentalization may cost less, or finer subcellular/receptor mapping may cost more. No network is selected because it runs faster.


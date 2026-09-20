"""Assemble quantitative reporting from frozen study outputs; no fitting."""
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text())
def write(name,text):
 p=H/name;assert not p.exists(),p;p.write_text(text)
def main():
 rows=[load(H/'benchmarks'/f'{c}-{r}'/'result.json') for c in ['s1','s2','s3','integrated','full'] for r in ['R0','R1','R2']]
 lines=['# Measured computational scaling\n',
 'These are **engineering envelopes**, not calibrated neural simulations. Specifications were recorded before measurement in REPRESENTATIONS.md. All runs use pinned real FAFB rows; no new extraction, neural skip, adaptive update schedule or biological behavior is involved.\n',
 '| Context / envelope | Roots | Local states | Anatomical rows | Contacts | Candidate plastic rows | Updates/s | Peak RSS MiB | Saved dynamic state MiB |',
 '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
 for r in rows:
  lines.append(f"| {r['context']} {r['envelope']} | {r['roots']:,} | {r['local_states']:,} | {r['anatomical_rows']:,} | {r['contacts']:,} | {r['candidate_plastic_rows']:,} | {r['updates_per_second']:.2f} | {r['peak_rss_bytes']/2**20:.1f} | {r['persistent_state_bytes']/2**20:.3f} |")
 lines+=['\n## Timing, storage and reproducibility\n',
 '| Context / envelope | Initialization s | 100 updates s | CPU % of one core | Replay s | Checkpoint MiB | Write / load ms |',
 '|---|---:|---:|---:|---:|---:|---:|']
 for r in rows:
  lines.append(f"| {r['context']} {r['envelope']} | {r['initialization_seconds']:.3f} | {r['wall_seconds']:.3f} | {r['cpu_percent_one_core']:.1f} | {r['replay_seconds']:.3f} | {r['checkpoint_bytes']/2**20:.3f} | {1000*r['checkpoint_write_seconds']:.2f} / {1000*r['checkpoint_load_seconds']:.2f} |")
 lines+=['\nAll15 runs completed100 updates plus100 identical replay updates, were finite, and restored checkpoints exactly. Timing is sequential by benchmark case; unrelated source reading/tests can affect host load. Each case has one timed run and one replay, not a statistical cloud benchmark. Platform: macOS27.2 arm64, NumPy2.3.5/SciPy sparse. Hardware brand/memory query was sandbox-blocked; no invented CPU model or cloud equivalence.\n',
 'Peak RSS includes Python metadata, loading/construction and temporaries; it is not minimum deployment RAM. Small cases read/mask full-source arrays, inflating their peak relative to their final working sets. R0/R1 run code allocates unused auxiliary buffers too, so peaks are conservative for those envelopes. Explicit retained-array footprints and dynamic-state bytes are separately recorded in result.json. Integer count rows are retained, CSR coalesces identical endpoints for R0 only. Count/neuropil identity remains in the underlying immutable source.\n',
 'R2 plastic candidate counts cover annotated KC→MBON rows, not all contacts or all neurons. No claim that these are the only plastic sites in a full brain. Dynamic checkpoints omit immutable anatomy/identity/parameters, which must be retained by source/specification hashes; a complete future checkpoint would also need clock, input replay and PRNG state. These deterministic100-step workload tests have no PRNG after construction.\n',
 '## Temporal cost, not temporal accuracy\n',
 '| R2 context | At dt10ms: simulated/wall | At dt1ms | At dt0.1ms |',
 '|---|---:|---:|---:|']
 for r in rows:
  if r['envelope']=='R2':lines.append(f"| {r['context']} | {r['updates_per_second']*.01:.3f} | {r['updates_per_second']*.001:.4f} | {r['updates_per_second']*.0001:.5f} |")
 lines+=['\nThese columns are arithmetic workload mappings, **not** validated numerical time steps. The fixed coefficients define an engineering recurrence, not physiology in seconds. Full R2 at1ms requires roughly73 wall seconds per simulated second on this host; integrated R2 requires roughly16.2. This implementation does not support continuous real-time1ms operation at either size. That does not prove impossibility with a different solver/hardware or scientifically justified slower time scale. The small circuits are much cheaper.\n',
 '## State accounting and R3 uncertainty\n',
 'Let C be local states and P plastic rows. Float64 dynamic state is8C bytes for E0/E1 and8(4C+2P) for E2. A sparse transmission matrix costs approximately12E+4(C+1) bytes with float64 values/int32 indices, besides row provenance, local-state mapping and construction arrays. Every extra scalar per anatomical row costs8E bytes: full reference134,783,976 bytes (~128.5MiB). Two variables per individual contact, if justified and contact IDs existed, would cost16×54,492,922=871,886,752 bytes (~831.5MiB), before activity, anatomy or other physiology.\n',
 'No calibrated R3 operator exists to time. With K channel/receptor variables per local electrical section, state alone is8C(1+K), plus plasticity and sparse axial/synaptic operators; implicit solvers/delays add storage. As a bookkeeping scenario, four voltage/gating variables per root at1/10/100 sections per root require32N/320N/3200N bytes: for139,255 roots4.25/42.50/424.97MiB, respectively, before edges and plasticity. These section counts are not anatomical estimates. The published MBON14 morphology has4,336 dendritic sections for one neuron; it cannot be multiplied indiscriminately across the brain. R3 throughput and required dt remain unidentified, and the old~0.7GiB scalar benchmark provides no guarantee.\n',
 'Full-root neuropil-local representation has435,774 states (~3.13/root); integrated has229,679 (~6.06/root). This finite anatomical partition is convenient for a cost envelope, but misses finer functional compartments and invents no validated intracellular dynamics. Heterogeneous selective compartmentalization may cost less, or finer subcellular/receptor mapping may cost more. No network is selected because it runs faster.\n']
 write('SCALING.md','\n'.join(lines)+'\n')
 summary={'classification':'INSUFFICIENT EVIDENCE TO SELECT REPRESENTATION',
  'narrow_supported_claim':'Local APL response representation under tested assays; nonzero physiological coupling not identified',
  'heterogeneous_representation':'supported as a design constraint/hypothesis, not a frozen transferable kernel',
  'APL_frozen_fit_sha256':hashlib.sha256((H/'FIT_FROZEN.json').read_bytes()).hexdigest(),
  'APL_validation':load(H/'VALIDATION.json'),
  'MBON_validation_disposition':'excluded from clean independent validation; unresolved source inconsistency',
  'benchmark_cases':len(rows),'benchmark_replays_exact':all(r['replay_exact'] for r in rows),
  'canonical_cycles_run':0,'neural_kernel_exported':False,'stage_probe_replays':0,
  'identities':load(H/'IDENTITY_AUDIT.json')}
 write('SUMMARY.json',json.dumps(summary,indent=2)+'\n')
if __name__=='__main__':main()

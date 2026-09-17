"""Counterbalanced offline protocol; the neural model never receives cue labels."""
import argparse
from dataclasses import asdict, replace
import gzip
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import shutil
import tempfile
import time

import numpy as np
import scipy

from model import Circuit, Model, Parameters, MODEL_VERSION, canonical

HERE = Path(__file__).resolve().parent
SEEDS = (1701, 1702, 1703)


def cue_patterns(circuit, seed):
    """Equal-sized, disjoint PN patterns, sampled without consulting MBON responses."""
    rng = np.random.Generator(np.random.PCG64(seed))
    pn = rng.permutation(circuit.groups["PN"])
    n = max(2, int(round(len(pn)*0.05)))
    if 2*n > len(pn):
        raise ValueError("Insufficient sensory neurons")
    return {"A": pn[:n], "B": pn[n:2*n]}


def protocol(circuit, p, patterns, paired, target, unpaired=False):
    events = []
    def add(start, end, indices, amplitude):
        events.append({"start_tick": round(start/p.dt), "stop_tick": round(end/p.dt),
                       "currents": [[circuit.ids[int(i)], amplitude] for i in indices]})
    add(0, 60, patterns["A"], 1.0)
    add(70, 130, patterns["B"], 1.0)
    base = 150 if unpaired else (0 if paired == "A" else 70)
    for s in range(0, 60, 2):
        add(base+s, base+s+1, circuit.groups["DAN_"+target], 1.0)
    return {"dt": p.dt, "stop_tick": round(220/p.dt), "events": events}


def execute(model, stimuli, record=False, dense=False):
    if stimuli["dt"] != model.p.dt:
        raise ValueError("Stimulus timing/model step mismatch")
    transitions = {}
    for ev in stimuli["events"]:
        for tick, sign in ((ev["start_tick"], 1), (ev["stop_tick"], -1)):
            for root, value in ev["currents"]:
                transitions.setdefault(tick, []).append((model.c.index[root], sign*value))
    current = np.zeros(model.c.n)
    times, group_rates, multipliers, activities, plastic = [], [], [], [], []
    groups = list(model.c.groups)
    stride = max(1, round(0.1/model.p.dt))
    for t in range(stimuli["stop_tick"]):
        for i, delta in transitions.get(t, []):
            current[i] += delta
        model.step(current)
        if record and t % stride == 0:
            times.append(model.tick*model.p.dt)
            group_rates.append([float(np.mean(model.r[model.c.groups[g]])) for g in groups])
            multipliers.append([float(np.mean(model.multiplier[model.plastic_compartment == i])) for i in (0, 1)])
            if dense:
                activities.append(model.r.copy())
                plastic.append(model.multiplier.copy())
    return {"seconds": np.array(times), "group_names": np.array(groups),
            "group_rates": np.array(group_rates), "compartment_mean_multiplier": np.array(multipliers),
            "rates": np.array(activities), "plastic": np.array(plastic),
            "root_ids": np.array(model.c.ids), "plastic_edge_indices": model.plastic_edges}


def probe(model, snapshot, patterns):
    results = {}
    for cue, indices in patterns.items():
        model.restore(snapshot)
        current = np.zeros(model.c.n)
        current[indices] = 1
        observations = []
        for t in range(round(2/model.p.dt)):
            model.step(current)
            if t >= round(1/model.p.dt):
                observations.append(model.r.copy())
        activity = np.mean(observations, axis=0)
        results[cue] = {g: float(np.mean(activity[ids])) for g, ids in model.c.groups.items()}
    model.restore(snapshot)
    return results


def depression(before, after, cue, target):
    b = before[cue]["MBON_"+target]
    return None if b <= 1e-9 else 1-after[cue]["MBON_"+target]/b


def one(circuit, seed=1701, paired="A", target="app", intervention="intact",
        params=Parameters(), unpaired=False, output=None, dense=False, replay=False):
    started = time.perf_counter()
    model = Model(circuit, params, seed, intervention, target)
    initial = model.snapshot()
    patterns = cue_patterns(circuit, seed)
    baseline = probe(model, initial, patterns)
    stimuli = protocol(circuit, params, patterns, paired, target, unpaired)
    trace = execute(model, stimuli, record=output is not None, dense=dense)
    trained = model.snapshot()
    post = probe(model, trained, patterns)
    model.restore(initial)
    restored = probe(model, model.snapshot(), patterns)
    model.restore(trained)
    model.reset_fast_state()
    weights_only = probe(model, model.snapshot(), patterns)
    replay_exact = None
    if replay:
        clone = Model(circuit, params, seed, intervention, target)
        # Serialize/deserialize, as in a fresh process; no training labels in state.
        clone.restore(json.loads(canonical(initial)))
        execute(clone, json.loads(canonical(stimuli)))
        replay_exact = canonical(clone.snapshot()) == canonical(trained)
    paired_effect = depression(baseline, post, paired, target)
    control_effect = depression(baseline, post, "B" if paired == "A" else "A", target)
    selective = None if paired_effect is None or control_effect is None else paired_effect-control_effect
    delta = np.abs(np.array(trained["plastic_multiplier"])-1)
    summary = {"seed": seed, "paired": paired, "target": target, "intervention": intervention,
               "unpaired_teaching": unpaired, "parameters": asdict(params), "baseline": baseline,
               "post": post, "restored": restored, "plastic_only": weights_only,
               "paired_depression": paired_effect, "control_depression": control_effect,
               "selective_depression": selective, "plastic_synapse_groups_changed": int(np.count_nonzero(delta > 1e-12)),
               "max_plastic_change": float(delta.max()), "restoration_exact": restored == baseline,
               "replay_exact": replay_exact, "lesioned_roots": [circuit.ids[int(i)] for i in model.lesion],
               "plastic_only_depression": depression(baseline, weights_only, paired, target),
               "simulated_training_seconds": stimuli['stop_tick']*params.dt,
               "fingerprint": model.fingerprint, "initial_hash": hashlib.sha256(canonical(initial)).hexdigest(),
               "trained_hash": hashlib.sha256(canonical(trained)).hexdigest(),
               "wall_seconds": time.perf_counter()-started}
    if output:
        output.mkdir(parents=True, exist_ok=False)
        (output/"summary.json").write_bytes(canonical(summary))
        (output/"stimuli.json").write_bytes(canonical(stimuli))
        for name, snapshot in (("initial", initial), ("trained", trained)):
            (output/f"{name}.json.gz").write_bytes(gzip.compress(canonical(snapshot), mtime=0))
        np.savez_compressed(output/"trace.npz", **trace)
    return summary


def suite(circuit, output):
    start = time.perf_counter()
    work = Path(tempfile.mkdtemp(prefix="fly-stage1-"))
    results = []
    def run(name, **kwargs):
        result = one(circuit, output=work/name, **kwargs)
        result["run"] = name
        results.append(result)
        print(json.dumps({"run": name, "selective": result['selective_depression'],
                          "paired": result['paired_depression'], "wall_seconds": result['wall_seconds']}), flush=True)
    for target in ("app", "av"):
        for seed in SEEDS:
            for paired in ("A", "B"):
                run(f"{target}-{seed}-{paired}-intact", target=target, seed=seed, paired=paired,
                    dense=seed == SEEDS[0], replay=seed == SEEDS[0])
        for intervention in ("freeze", "silence_dan", "remove_da_contacts", "single_dan", "matched_dan",
                             "remove_pn_kc", "remove_kc_mbon", "no_apl", "no_recurrence", "shuffle_pn_weights"):
            for paired in ("A", "B"):
                run(f"{target}-1701-{paired}-{intervention}", target=target, paired=paired, intervention=intervention)
        for paired in ("A", "B"):
            run(f"{target}-1701-{paired}-unpaired", target=target, paired=paired, unpaired=True)
    p = Parameters()
    variants = {"half_dt": replace(p, dt=.005), "half_eta": replace(p, learning_rate=p.learning_rate/2),
                "double_eta": replace(p, learning_rate=p.learning_rate*2),
                "gain075": replace(p, fast_gain=.75), "gain125": replace(p, fast_gain=1.25),
                "boundary002": replace(p, boundary_current=.02), "boundary005": replace(p, boundary_current=.05),
                "apl05": replace(p, apl_gain=.5), "apl2": replace(p, apl_gain=2),
                "boundary_noise": replace(p, boundary_current=.02, boundary_noise=.01)}
    for name, params in variants.items():
        for paired in ("A", "B"):
            run(f"sensitivity-{name}-{paired}", params=params, paired=paired, replay=name == "boundary_noise")
    summary = {"model": MODEL_VERSION, "circuit": circuit.manifest_hash,
               "environment": {"python": platform.python_version(), "numpy": np.__version__,
                   "scipy": scipy.__version__, "os": platform.platform(), "machine": platform.machine(),
                   "cpu_count": os.cpu_count()},
               "runs": results, "performance": {"suite_wall_seconds": time.perf_counter()-start,
                   "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if platform.system() == 'Darwin' else 1024)},
               "sources": {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                           for name in ('model.py', 'experiment.py', 'PLAN.md', 'requirements.txt')}}
    (work/"results.json").write_bytes(canonical(summary))
    manifest = {"schema": 1, "circuit": circuit.manifest_hash,
                "files": {str(p.relative_to(work)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(work.rglob('*')) if p.is_file()}}
    raw = canonical(manifest)
    ident = hashlib.sha256(raw).hexdigest()
    (work/"evidence-manifest.json").write_bytes(raw)
    dest = output/ident
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        raise ValueError("Refusing to replace an evidence run")
    shutil.move(str(work), str(dest))
    print(json.dumps({"evidence": str(dest), "performance": summary['performance']}, indent=2))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--circuit", type=Path, required=True)
    p.add_argument("--output", type=Path, default=HERE/"evidence")
    p.add_argument("--single", action="store_true")
    args = p.parse_args()
    circuit = Circuit(args.circuit)
    if args.single:
        print(json.dumps(one(circuit, replay=True), indent=2))
    else:
        suite(circuit, args.output)

"""Fresh-process cue-only recall. No training protocol, cue name or episode input.

Accepts one numeric sensory-current vector and a neural snapshot. This intentionally
imports only the model, not the experimental runner. Defaults match primary runs.
"""
import argparse
from dataclasses import fields
import gzip
import json
from pathlib import Path

import numpy as np

from model import Circuit, Model, Parameters, canonical


def recall(circuit_path, snapshot_path, currents_path, target="app", params=None):
    circuit = Circuit(circuit_path)
    model = Model(circuit, Parameters(**(params or {})), target=target)
    with gzip.open(snapshot_path, "rt") as f:
        model.restore(json.load(f))
    current = np.zeros(circuit.n)
    for root, value in json.loads(Path(currents_path).read_text()):
        i = circuit.index[root]
        if circuit.roles[i] != "PN":
            raise ValueError("Cue-only recall accepts PN sensory currents, not teaching currents")
        current[i] += value
    records = []
    for tick in range(round(2/model.p.dt)):
        model.step(current)
        if tick >= round(1/model.p.dt):
            records.append(model.r.copy())
    average = np.mean(records, axis=0)
    return {"group_rates": {name: float(average[ids].mean()) for name, ids in circuit.groups.items()},
            "neuron_rates": {root: float(average[i]) for i, root in enumerate(circuit.ids)},
            "final_state_hash": model.state_hash(), "manifest": circuit.manifest_hash}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--circuit", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--currents", type=Path, required=True)
    parser.add_argument("--target", choices=["app", "av"], default="app")
    parser.add_argument("--parameters", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    params = json.loads(args.parameters.read_text()) if args.parameters else None
    if params and not set(params) <= {f.name for f in fields(Parameters)}:
        raise ValueError("Only numeric model parameters are accepted")
    args.output.write_bytes(canonical(recall(args.circuit, args.snapshot, args.currents, args.target, params)))

"""Offline connectome-constrained associative model. No cue labels or reward scores.

Biology: observed directed contacts; compartment-specific dopamine/KC plasticity.
Model: rates, fixed class gains, thresholds, point APL, eligibility and bounded LTD.
Genesis mapping: NONE. Numeric currents are imposed experimental boundary inputs.
"""
import copy
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix

MODEL_VERSION = "fly-stage1-rate-ltd-1"


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


@dataclass(frozen=True)
class Parameters:
    dt: float = 0.01
    tau: float = 0.05
    eligibility_tau: float = 0.5
    learning_rate: float = 0.08
    kc_threshold: float = 0.15
    dopamine_threshold: float = 0.2
    pn_gain: float = 3.0
    recurrent_gain: float = 0.05
    apl_gain: float = 1.0
    fast_gain: float = 1.0
    boundary_current: float = 0.0
    boundary_noise: float = 0.0
    min_multiplier: float = 0.1


class Circuit:
    def __init__(self, directory):
        self.directory = Path(directory)
        raw = (self.directory / "manifest.json").read_bytes()
        self.manifest_hash = hashlib.sha256(raw).hexdigest()
        if self.directory.name != self.manifest_hash:
            raise ValueError("Manifest content-address mismatch")
        self.manifest = json.loads(raw)
        for name, spec in self.manifest["artifacts"].items():
            if hashlib.sha256((self.directory/name).read_bytes()).hexdigest() != spec["sha256"]:
                raise ValueError(f"Corrupt artifact: {name}")
        data = json.loads((self.directory / "circuit.json").read_text())
        self.nodes, self.edges = data["nodes"], data["edges"]
        self.ids = [n["root_id"] for n in self.nodes]
        if any(not isinstance(i, str) for i in self.ids) or len(set(self.ids)) != len(self.ids):
            raise ValueError("Invalid root identities")
        self.index = {root: i for i, root in enumerate(self.ids)}
        self.n = len(self.ids)
        self.roles = np.array([n["role"] for n in self.nodes])
        self.groups = {name: np.array([self.index[i] for i in ids], dtype=np.int64)
                       for name, ids in data["groups"].items()}
        # Keep separate neuropil rows; never insert a missing pair.
        self.pre = np.array([self.index[e["source"]] for e in self.edges])
        self.post = np.array([self.index[e["target"]] for e in self.edges])
        self.count = np.array([e["synapses"] for e in self.edges], dtype=np.float64)
        boundary = json.loads((self.directory / "boundary.json").read_text())
        self.omitted = np.array([boundary["per_neuron"][root]["omitted_input"] /
            max(1, boundary["per_neuron"][root]["omitted_input"] + boundary["per_neuron"][root]["retained_input"])
            for root in self.ids])


class Model:
    def __init__(self, circuit, params=Parameters(), seed=1701, intervention="intact", target="app"):
        if params.dt <= 0 or params.dt > params.tau or params.eligibility_tau <= 0:
            raise ValueError("Invalid integration parameters")
        self.c, self.p = circuit, params
        self.intervention, self.target = intervention, target
        if target not in ("app", "av"):
            raise ValueError("Unknown compartment")
        accepted = {"intact", "freeze", "silence_dan", "single_dan", "remove_da_contacts", "matched_dan",
                    "remove_pn_kc", "remove_kc_mbon", "no_apl", "no_recurrence",
                    "shuffle_pn_weights"}
        if intervention not in accepted:
            raise ValueError("Unknown intervention")
        self.rng = np.random.Generator(np.random.PCG64(seed))
        self.r = np.zeros(circuit.n)
        self.eligibility = np.zeros(circuit.n)
        self.tick = 0
        self.pre = circuit.pre
        self.post = circuit.post
        src, dst = circuit.roles[self.pre], circuit.roles[self.post]
        self.plastic_edges = np.flatnonzero((src == "KC") & np.isin(dst, ["MBON_app", "MBON_av"]))
        self.plastic_pre = self.pre[self.plastic_edges]
        self.plastic_post = self.post[self.plastic_edges]
        self.plastic_compartment = np.where(dst[self.plastic_edges] == "MBON_app", 0, 1)
        self.multiplier = np.ones(len(self.plastic_edges))

        # Normalize separately per presynaptic role at each target, once on intact anatomy.
        # This is a model assumption, NOT a measured conductance or post-lesion rescaling.
        weights = np.zeros(len(circuit.edges))
        for role in sorted(set(src)):
            mask = src == role
            denom = np.bincount(self.post[mask], weights=circuit.count[mask], minlength=circuit.n)
            weights[mask] = circuit.count[mask] / np.maximum(denom[self.post[mask]], 1)
        gains = np.full(len(weights), params.recurrent_gain)
        gains[(src == "PN") & (dst == "KC")] = params.pn_gain
        gains[(src == "KC") & np.isin(dst, ["MBON_app", "MBON_av", "APL"])] = 1
        gains[(src == "APL") & (dst == "KC")] = params.apl_gain
        gains[(src == "MBON_app") & (dst == "DAN_app")] = 0.1
        signs = np.ones(len(weights))
        signs[np.isin(src, ["APL", "MBON_av"])] = -1
        # MBON07 glutamate is excitatory to PAM-alpha1 (NMDA evidence).
        # Effects on other classes are unresolved and excluded, not guessed.
        signs[(src == "MBON_app") & (dst != "DAN_app")] = 0
        signs[np.isin(src, ["DAN_app", "DAN_av"])] = 0
        weights *= gains * signs * params.fast_gain
        self.zero_fast_rows = int(np.count_nonzero(weights == 0))

        # Local teaching exposure requires actual DAN→KC contacts in the same compartment.
        self.da_operators = []
        for comp in ("app", "av"):
            mask = (src == "DAN_" + comp) & (dst == "KC")
            norm = np.bincount(self.post[mask], weights=circuit.count[mask], minlength=circuit.n)
            vals = circuit.count[mask] / np.maximum(norm[self.post[mask]], 1)
            if intervention == "remove_da_contacts" and comp == target:
                vals = np.zeros_like(vals)
            self.da_operators.append(csr_matrix((vals, (self.post[mask], self.pre[mask])),
                                                shape=(circuit.n, circuit.n)))
        self.lesion = np.array([], dtype=np.int64)
        if intervention == "silence_dan":
            self.lesion = circuit.groups["DAN_"+target]
        elif intervention in ("single_dan", "matched_dan"):
            # Exactly one neuron in both arms; strongest anatomical KC contact total.
            comp = target if intervention == "single_dan" else ("av" if target == "app" else "app")
            candidates = circuit.groups["DAN_"+comp]
            mass = np.bincount(self.pre[dst == "KC"], weights=circuit.count[dst == "KC"], minlength=circuit.n)
            self.lesion = candidates[np.argsort(-mass[candidates], kind="stable")[:1]]
        elif intervention == "no_apl":
            self.lesion = circuit.groups["APL"]
        if intervention == "remove_pn_kc":
            weights[(src == "PN") & (dst == "KC")] = 0
        if intervention == "remove_kc_mbon":
            weights[(src == "KC") & (dst == "MBON_"+target)] = 0
        if intervention == "no_recurrence":
            feedforward = ((src == "PN") & (dst == "KC")) | ((src == "KC") & np.isin(dst, ["MBON_app", "MBON_av"]))
            weights[~feedforward] = 0
        if intervention == "shuffle_pn_weights":
            # Shuffle strengths ONLY among existing PN→KC contacts at each KC.
            # No fabricated anatomical pairs, degree preserved. Normalization frozen.
            for k in circuit.groups["KC"]:
                inds = np.flatnonzero((src == "PN") & (self.post == k))
                weights[inds] = self.rng.permutation(weights[inds])
        self.weights = weights
        self.plastic_baseline = weights[self.plastic_edges].copy()
        fixed = weights.copy()
        fixed[self.plastic_edges] = 0
        self.fixed = csr_matrix((fixed, (self.post, self.pre)), shape=(circuit.n, circuit.n))
        self.threshold = np.where(circuit.roles == "KC", params.kc_threshold, 0.0)
        self.fingerprint = hashlib.sha256(canonical({"model": MODEL_VERSION,
            "source": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "manifest": circuit.manifest_hash,
            "parameters": asdict(params), "intervention": intervention, "target": target,
            "weights": hashlib.sha256(weights.tobytes()).hexdigest()})).hexdigest()

    def step(self, currents):
        if currents.shape != (self.c.n,) or not np.all(np.isfinite(currents)):
            raise ValueError("Expected finite current for each neuron")
        effective = self.plastic_baseline * self.multiplier
        drive = self.fixed @ self.r + np.bincount(self.plastic_post,
            weights=effective*self.r[self.plastic_pre], minlength=self.c.n)
        drive += currents + self.p.boundary_current*self.c.omitted
        if self.p.boundary_noise:
            drive += self.rng.normal(0, self.p.boundary_noise, self.c.n)*self.c.omitted
        desired = np.clip(drive-self.threshold, 0, 1)
        self.r += (self.p.dt/self.p.tau)*(desired-self.r)
        self.r[self.lesion] = 0
        # Eligibility contains recent neural activity, not cue identity or outcome labels.
        self.eligibility += (self.p.dt/self.p.eligibility_tau)*(self.r-self.eligibility)
        dopamine = np.stack([op @ self.r for op in self.da_operators])
        local = np.maximum(0, dopamine[self.plastic_compartment, self.plastic_pre]-self.p.dopamine_threshold)
        if self.intervention != "freeze":
            self.multiplier *= np.exp(-self.p.learning_rate*self.p.dt*self.eligibility[self.plastic_pre]*local)
            np.maximum(self.multiplier, self.p.min_multiplier, out=self.multiplier)
        self.tick += 1

    def snapshot(self):
        return {"model": MODEL_VERSION, "fingerprint": self.fingerprint,
                "manifest": self.c.manifest_hash, "tick": self.tick,
                "rate": self.r.tolist(), "eligibility": self.eligibility.tolist(),
                "plastic_multiplier": self.multiplier.tolist(), "prng": copy.deepcopy(self.rng.bit_generator.state)}

    def restore(self, snapshot):
        if snapshot["fingerprint"] != self.fingerprint or snapshot["manifest"] != self.c.manifest_hash:
            raise ValueError("Incompatible model, parameters, intervention or circuit")
        r = np.asarray(snapshot["rate"], dtype=np.float64)
        e = np.asarray(snapshot["eligibility"], dtype=np.float64)
        m = np.asarray(snapshot["plastic_multiplier"], dtype=np.float64)
        if r.shape != self.r.shape or e.shape != r.shape or m.shape != self.multiplier.shape:
            raise ValueError("Snapshot dimensions do not match")
        if (not all(np.all(np.isfinite(x)) for x in (r, e, m))
                or np.any(m < self.p.min_multiplier) or np.any(m > 1)
                or np.any(r < 0) or np.any(r > 1) or np.any(e < 0) or np.any(e > 1)):
            raise ValueError("Invalid snapshot values")
        if type(snapshot["tick"]) is not int or snapshot["tick"] < 0:
            raise ValueError("Invalid logical clock")
        self.r, self.eligibility, self.multiplier = r.copy(), e.copy(), m.copy()
        self.rng.bit_generator.state = copy.deepcopy(snapshot["prng"])
        self.tick = snapshot["tick"]

    def reset_fast_state(self):
        """Intervention: clear transient activity/eligibility while retaining learned weights."""
        self.r.fill(0)
        self.eligibility.fill(0)

    def state_hash(self):
        return hashlib.sha256(canonical(self.snapshot())).hexdigest()

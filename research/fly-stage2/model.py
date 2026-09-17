"""Isolated α′3 rate/efficacy hypothesis. No cue labels, reinforcement or memory API.

BIOLOGICAL FACT: directed contacts and cell types from the pinned extraction.
COMPUTATIONAL MODEL: rates, gains, postsynaptic efficacy and local DA gate.
GENESIS MAPPING: none. This module has no Genesis or Stage-1 imports.
"""
import copy
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix

MODEL_VERSION = "fly-stage2-ap3-postsynaptic-1"


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode()


@dataclass(frozen=True)
class Parameters:
    dt: float = .01
    tau: float = .05
    eligibility_tau: float = .5
    learning_rate: float = .08
    kc_threshold: float = .15
    pn_gain: float = 3.
    recurrent_gain: float = .05
    feedback_gain: float = .1
    apl_gain: float = 1.
    fast_gain: float = 1.
    recovery_tau: float = 1800.
    min_multiplier: float = .1
    normalization: str = "all_inputs"


class Circuit:
    def __init__(self, directory):
        self.directory = Path(directory)
        raw = (self.directory/"manifest.json").read_bytes()
        self.manifest_hash = hashlib.sha256(raw).hexdigest()
        if self.directory.name != self.manifest_hash:
            raise ValueError("Manifest content address mismatch")
        self.manifest = json.loads(raw)
        for name, spec in self.manifest["artifacts"].items():
            if hashlib.sha256((self.directory/name).read_bytes()).hexdigest() != spec["sha256"]:
                raise ValueError("Artifact checksum mismatch: "+name)
        c = json.loads((self.directory/"circuit.json").read_text())
        self.nodes, self.edges = c['nodes'], c['edges']
        self.ids = [n['root_id'] for n in self.nodes]
        if len(set(self.ids)) != len(self.ids) or any(type(i) is not str for i in self.ids):
            raise ValueError("Invalid roots")
        self.n = len(self.ids)
        self.index = {i: k for k, i in enumerate(self.ids)}
        self.roles = np.array([n['role'] for n in self.nodes])
        self.groups = {g: np.array([self.index[i] for i in ids], dtype=int) for g, ids in c['groups'].items()}
        self.pre = np.array([self.index[e['source']] for e in self.edges])
        self.post = np.array([self.index[e['target']] for e in self.edges])
        self.count = np.array([e['synapses'] for e in self.edges], dtype=float)
        self.boundary = json.loads((self.directory/'boundary.json').read_text())
        self.full_input = np.array([sum(self.boundary['per_neuron'][r][k] for k in
            ('retained_input','omitted_input')) for r in self.ids], dtype=float)


class Model:
    def __init__(self, circuit, params=Parameters(), seed=2701, intervention="intact"):
        numeric = [v for v in asdict(params).values() if isinstance(v, (float, int))]
        if (not np.all(np.isfinite(numeric)) or min(numeric) < 0 or params.dt <= 0
            or params.dt > min(params.tau, params.eligibility_tau) or params.recovery_tau <= 0
            or not 0 <= params.min_multiplier <= 1):
            raise ValueError("Invalid parameters")
        if params.normalization not in ('all_inputs', 'retained_inputs', 'retained_roles'):
            raise ValueError("Unknown boundary normalization")
        if intervention not in ('intact', 'freeze', 'silence_dan', 'remove_da_contacts',
                'cut_feedback', 'matched_control', 'remove_pn_kc', 'remove_kc_mbon',
                'shuffle_pn_weights', 'no_apl', 'no_ambiguous'):
            raise ValueError("Unknown intervention")
        self.c, self.p, self.intervention = circuit, params, intervention
        self.rng = np.random.Generator(np.random.PCG64(seed))
        self.r = np.zeros(circuit.n)
        self.eligibility = np.zeros(circuit.n)
        self.tick = 0
        self.pre, self.post = circuit.pre, circuit.post
        src, dst = circuit.roles[self.pre], circuit.roles[self.post]
        self.plastic_edges = np.flatnonzero((src == 'KC') & (dst == 'MBON'))
        self.plastic_pre, self.plastic_post = self.pre[self.plastic_edges], self.post[self.plastic_edges]
        self.multiplier = np.ones(len(self.plastic_edges))
        # Denominators are frozen BEFORE every lesion; no invented contact or lesion rescaling.
        if params.normalization == 'all_inputs':
            denominator = circuit.full_input[self.post]
        elif params.normalization == 'retained_inputs':
            denominator = np.bincount(self.post, weights=circuit.count, minlength=circuit.n)[self.post]
        else:
            denominator = np.zeros(len(self.pre))
            for role in sorted(set(src)):
                mask = src == role
                den = np.bincount(self.post[mask], weights=circuit.count[mask], minlength=circuit.n)
                denominator[mask] = den[self.post[mask]]
        weights = circuit.count/np.maximum(denominator, 1)
        gains = np.full(len(weights), params.recurrent_gain)
        gains[(src == 'PN') & (dst == 'KC')] = params.pn_gain
        gains[(src == 'KC') & np.isin(dst, ['MBON','CONTROL','AMBIGUOUS','APL'])] = 1
        gains[(src == 'APL') & (dst == 'KC')] = params.apl_gain
        gains[np.isin(src, ['MBON','CONTROL','AMBIGUOUS']) & (dst == 'DAN')] = params.feedback_gain
        # Selected PN/KC/MBON cells are cholinergic (MBON28 predicted); APL GABA.
        signs = np.where(src == 'APL', -1., 1.)
        signs[src == 'DAN'] = 0
        weights *= gains*signs*params.fast_gain
        da_mask = (src == 'DAN') & (dst == 'MBON')
        da_denom = np.bincount(self.post[da_mask], weights=circuit.count[da_mask], minlength=circuit.n)
        da_values = circuit.count[da_mask]/np.maximum(da_denom[self.post[da_mask]], 1)
        if intervention == 'remove_da_contacts':
            da_values.fill(0)
        self.da_operator = csr_matrix((da_values, (self.post[da_mask], self.pre[da_mask])),
                                      shape=(circuit.n, circuit.n))
        self.lesion = np.array([], dtype=int)
        lesion_group = {'silence_dan':'DAN', 'matched_control':'CONTROL',
                        'no_apl':'APL', 'no_ambiguous':'AMBIGUOUS'}.get(intervention)
        if lesion_group:
            self.lesion = circuit.groups[lesion_group]
        if intervention == 'cut_feedback':
            weights[(src == 'MBON') & (dst == 'DAN')] = 0
        if intervention == 'remove_pn_kc':
            weights[(src == 'PN') & (dst == 'KC')] = 0
        if intervention == 'remove_kc_mbon':
            weights[(src == 'KC') & (dst == 'MBON')] = 0
        if intervention == 'shuffle_pn_weights':
            for k in circuit.groups['KC']:
                ids = np.flatnonzero((src == 'PN') & (self.post == k))
                weights[ids] = self.rng.permutation(weights[ids])
        self.weights = weights.copy()
        self.plastic_baseline = weights[self.plastic_edges].copy()
        weights[self.plastic_edges] = 0
        self.fixed = csr_matrix((weights, (self.post,self.pre)), shape=(circuit.n,circuit.n))
        self.threshold = np.where(circuit.roles == 'KC', params.kc_threshold, 0.)
        self.fingerprint = hashlib.sha256(canonical({'model': MODEL_VERSION,
            'source': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'manifest': circuit.manifest_hash, 'parameters': asdict(params), 'intervention': intervention,
            'weights': hashlib.sha256(self.weights.tobytes()).hexdigest()})).hexdigest()

    def step(self, currents):
        if currents.shape != (self.c.n,) or not np.all(np.isfinite(currents)):
            raise ValueError("Expected finite numeric currents")
        drive = self.fixed@self.r + np.bincount(self.plastic_post,
            weights=self.plastic_baseline*self.multiplier*self.r[self.plastic_pre], minlength=self.c.n)
        desired = np.clip(drive+currents-self.threshold, 0, 1)
        self.r += self.p.dt/self.p.tau*(desired-self.r)
        self.r[self.lesion] = 0
        self.eligibility += self.p.dt/self.p.eligibility_tau*(self.r-self.eligibility)
        dopamine = self.da_operator@self.r
        if self.intervention != 'freeze':
            a = self.p.learning_rate*self.eligibility[self.plastic_pre]*dopamine[self.plastic_post]
            b = 1/self.p.recovery_tau
            equilibrium = b/(a+b)
            self.multiplier = equilibrium+(self.multiplier-equilibrium)*np.exp(-(a+b)*self.p.dt)
            np.clip(self.multiplier, self.p.min_multiplier, 1., out=self.multiplier)
        self.tick += 1

    def reset_fast_state(self):
        self.r.fill(0)
        self.eligibility.fill(0)

    def idle(self, seconds):
        """Exact silent-preparation recovery, only after explicit fast-state reset.

        Not a shortcut for unknown spontaneous neural dynamics in a behaving fly.
        """
        if seconds < 0 or not np.isfinite(seconds) or np.any(self.r) or np.any(self.eligibility):
            raise ValueError("Idle integration requires zero fast state and finite nonnegative duration")
        steps = round(seconds/self.p.dt)
        if abs(steps*self.p.dt-seconds) > 1e-8:
            raise ValueError("Duration not on integration grid")
        if self.intervention != 'freeze':
            self.multiplier = 1-(1-self.multiplier)*np.exp(-seconds/self.p.recovery_tau)
        self.tick += steps

    def snapshot(self):
        return {'model': MODEL_VERSION, 'fingerprint': self.fingerprint, 'manifest': self.c.manifest_hash,
                'tick': self.tick, 'rate': self.r.tolist(), 'eligibility': self.eligibility.tolist(),
                'plastic_multiplier': self.multiplier.tolist(), 'prng': copy.deepcopy(self.rng.bit_generator.state)}

    def restore(self, state):
        if state['fingerprint'] != self.fingerprint or state['manifest'] != self.c.manifest_hash:
            raise ValueError("Incompatible neural snapshot")
        arrays = [np.asarray(state[k], dtype=float) for k in ('rate','eligibility','plastic_multiplier')]
        if (any(a.shape != b.shape for a,b in zip(arrays, (self.r,self.eligibility,self.multiplier)))
            or any(not np.all(np.isfinite(a)) or np.any(a < 0) or np.any(a > 1) for a in arrays)
            or np.any(arrays[2] < self.p.min_multiplier) or type(state['tick']) is not int or state['tick'] < 0):
            raise ValueError("Invalid neural state")
        self.r, self.eligibility, self.multiplier = (a.copy() for a in arrays)
        self.rng.bit_generator.state = copy.deepcopy(state['prng'])
        self.tick = state['tick']

    def state_hash(self):
        return hashlib.sha256(canonical(self.snapshot())).hexdigest()

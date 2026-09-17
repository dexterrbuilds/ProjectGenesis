"""Integrity and mechanism tests using the actual extracted circuit, never mock data."""
import ast
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import unittest

import numpy as np

from model import Circuit, Model, Parameters, canonical
from experiment import cue_patterns

HERE = Path(__file__).resolve().parent
CIRCUIT = HERE/"artifacts"/"c5c332c1bd0ce77487ad5765756a58dc441d50f59dc56899a462bf35e4b2a157"


class HarnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = Circuit(CIRCUIT)

    def test_immutable_manifest_root_strings_and_anatomical_counts(self):
        c = self.c
        self.assertEqual(c.n, 1054)
        self.assertEqual(sum(e['synapses'] for e in c.edges), 226143)
        self.assertEqual(len({(e['source'], e['target']) for e in c.edges}), 80423)
        self.assertEqual(sorted(c.ids), sorted(c.manifest['selected_roots']))
        self.assertTrue(all(type(i) is str and int(i) > 2**53 for i in c.ids))
        self.assertEqual(c.manifest['annotation_reconciliation']['selected_missing_annotations'], [])

    def test_plastic_edges_are_observed_kc_mbon_contacts_only(self):
        m = Model(self.c)
        self.assertTrue(np.all(self.c.roles[m.plastic_pre] == 'KC'))
        self.assertTrue(np.all(np.isin(self.c.roles[m.plastic_post], ['MBON_app', 'MBON_av'])))
        self.assertTrue(np.all(self.c.count[m.plastic_edges] > 0))
        for i, comp in enumerate(('app', 'av')):
            observed = {(int(self.c.post[k]), int(self.c.pre[k])) for k in range(len(self.c.edges))
                        if self.c.roles[self.c.pre[k]] == 'DAN_'+comp and self.c.roles[self.c.post[k]] == 'KC'}
            actual = set(zip(*m.da_operators[i].nonzero()))
            self.assertEqual(observed, actual)

    def test_silence_and_locality_without_teaching(self):
        m = Model(self.c)
        for _ in range(50):
            m.step(np.zeros(self.c.n))
        self.assertFalse(m.r.any())
        np.testing.assert_array_equal(m.multiplier, 1)
        x = np.zeros(self.c.n)
        x[cue_patterns(self.c, 1701)['A']] = 1
        for _ in range(200):
            m.step(x)
        self.assertGreater(m.r[self.c.groups['KC']].mean(), 0)
        np.testing.assert_array_equal(m.multiplier, 1)

    def test_learning_and_selective_interventions(self):
        cue = np.zeros(self.c.n)
        cue[cue_patterns(self.c, 1701)['A']] = 1
        changes = {}
        kc = {}
        for intervention in ('intact', 'freeze', 'silence_dan', 'remove_da_contacts', 'matched_dan'):
            m = Model(self.c, intervention=intervention)
            x = cue.copy()
            x[self.c.groups['DAN_app']] = 1
            for _ in range(200):
                m.step(x)
            changes[intervention] = float(np.max(1-m.multiplier))
            kc[intervention] = float(m.r[self.c.groups['KC']].mean())
            np.testing.assert_array_equal(m.multiplier[m.plastic_compartment == 1], 1)
        self.assertGreater(changes['intact'], .01)
        for control in ('freeze', 'silence_dan', 'remove_da_contacts'):
            self.assertEqual(changes[control], 0)
            self.assertLess(abs(kc[control]/kc['intact']-1), .1)
        self.assertGreater(changes['matched_dan'], .01)

    def test_connectivity_removal_blocks_downstream_not_input(self):
        m = Model(self.c, intervention='remove_pn_kc')
        x = np.zeros(self.c.n)
        x[cue_patterns(self.c, 1701)['A']] = 1
        for _ in range(100):
            m.step(x)
        self.assertGreater(m.r[self.c.groups['PN']].mean(), .01)
        self.assertEqual(float(m.r[self.c.groups['KC']].max()), 0)

    def test_ablation_does_not_rescale_surviving_weights(self):
        base = Model(self.c)
        lesion = Model(self.c, intervention='remove_pn_kc')
        survives = lesion.weights != 0
        np.testing.assert_array_equal(lesion.weights[survives], base.weights[survives])
        relevant = Model(self.c, intervention='single_dan')
        control = Model(self.c, intervention='matched_dan')
        self.assertEqual(len(relevant.lesion), len(control.lesion))
        self.assertEqual(len(relevant.lesion), 1)

    def test_json_restart_with_prng_replays_mid_experiment_exactly(self):
        p = replace(Parameters(), boundary_noise=.01)
        m = Model(self.c, p)
        x = np.zeros(self.c.n)
        x[cue_patterns(self.c, 1702)['B']] = 1
        x[self.c.groups['DAN_app']] = 1
        for _ in range(130):
            m.step(x)
        snapshot = json.loads(canonical(m.snapshot()))
        clone = Model(self.c, p, seed=999)
        clone.restore(snapshot)
        for i in range(170):
            current = x if i % 3 else np.zeros(self.c.n)
            m.step(current)
            clone.step(current)
        self.assertEqual(m.state_hash(), clone.state_hash())

    def test_snapshot_is_only_numeric_neural_state_not_cue_or_prose_memory(self):
        state = Model(self.c).snapshot()
        self.assertEqual(set(state), {'model', 'fingerprint', 'manifest', 'tick', 'rate', 'eligibility', 'plastic_multiplier', 'prng'})
        self.assertTrue(all(type(x) is float for x in state['plastic_multiplier']))

    def test_incompatible_or_corrupt_snapshots_rejected(self):
        m = Model(self.c)
        s = m.snapshot()
        with self.assertRaises(ValueError):
            Model(self.c, replace(Parameters(), learning_rate=.04)).restore(s)
        s['rate'][0] = float('nan')
        with self.assertRaises(ValueError):
            m.restore(s)

    def test_runtime_and_network_dependencies_are_absent(self):
        prohibited = {'requests', 'urllib', 'socket', 'openai', 'psycopg', 'core', 'runtime', 'server'}
        for file in ('model.py', 'recall.py', 'experiment.py'):
            tree = ast.parse((HERE/file).read_text())
            imports = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.update(n.name.split('.')[0] for n in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imports.add(node.module.split('.')[0])
            self.assertFalse(imports & prohibited)


if __name__ == '__main__':
    unittest.main(verbosity=2)

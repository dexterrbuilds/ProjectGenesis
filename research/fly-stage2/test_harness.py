"""Implementation checks; these passing do NOT establish familiarity."""
import ast
from dataclasses import replace
import json
from pathlib import Path
import unittest

import numpy as np
from model import Circuit, Model, Parameters, canonical
from experiment import cue_patterns, protocol, execute

HERE = Path(__file__).resolve().parent


class IntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = Circuit(next((HERE/'artifacts').iterdir()))

    def test_real_anatomy_and_strings(self):
        c = self.c
        self.assertEqual(c.n,1172)
        self.assertEqual(len(set(zip(c.pre,c.post))),57804)
        self.assertEqual(int(c.count.sum()),160848)
        self.assertTrue(all(type(r) is str for r in c.ids))
        m = Model(c)
        self.assertTrue(np.all(c.roles[m.plastic_pre] == 'KC'))
        self.assertTrue(np.all(c.roles[m.plastic_post] == 'MBON'))
        self.assertTrue(np.all(c.count[m.plastic_edges] > 0))

    def test_no_application_or_memory_imports(self):
        tree = ast.parse((HERE/'model.py').read_text())
        roots = {x.names[0].name.split('.')[0] for x in ast.walk(tree) if isinstance(x,ast.Import)}
        roots |= {x.module.split('.')[0] for x in ast.walk(tree) if isinstance(x,ast.ImportFrom)}
        self.assertLessEqual(roots, {'copy','dataclasses','hashlib','json','pathlib','numpy','scipy'})
        self.assertEqual(set(Model(self.c).snapshot()),{'model','fingerprint','manifest','tick','rate',
                        'eligibility','plastic_multiplier','prng'})

    def test_counterbalanced_inputs_are_equal_and_disjoint(self):
        for seed in (2701,2702,2703):
            cues = cue_patterns(self.c,seed)
            self.assertEqual(len(cues['A']),len(cues['B']))
            self.assertFalse(set(cues['A']) & set(cues['B']))
            self.assertEqual(len(cues['A']),14)

    def test_no_dopamine_input_in_protocol(self):
        m = Model(self.c)
        p = protocol(self.c,m.p,cue_patterns(self.c,2701)['A'])
        self.assertEqual(len(p['events']),10)
        self.assertTrue(all(self.c.roles[self.c.index[r]]=='PN' for e in p['events'] for r,v in e['currents']))
        bad = {'dt':m.p.dt,'stop_tick':1,'events':[{'start_tick':0,'stop_tick':1,
               'currents':[[self.c.ids[self.c.groups['DAN'][0]],1.]]}]}
        with self.assertRaises(ValueError):
            execute(m,bad)

    def test_lesion_no_renormalization(self):
        intact = Model(self.c)
        cut = Model(self.c,intervention='remove_pn_kc')
        mask = (self.c.roles[self.c.pre]=='PN') & (self.c.roles[self.c.post]=='KC')
        np.testing.assert_array_equal(intact.weights[~mask],cut.weights[~mask])
        self.assertTrue(np.all(cut.weights[mask]==0))
        removed = Model(self.c,intervention='remove_da_contacts')
        np.testing.assert_array_equal(intact.weights,removed.weights)

    def test_local_gate_and_frozen_state(self):
        models = [Model(self.c,intervention=i) for i in ('intact','freeze','remove_da_contacts')]
        # Mechanism unit test, not an experimental observation: imposed activity.
        for m in models:
            m.r[self.c.groups['DAN']]=1
            m.r[self.c.groups['KC']]=1
            m.eligibility[self.c.groups['KC']]=1
            m.step(np.zeros(self.c.n))
        self.assertLess(models[0].multiplier.min(),1)
        self.assertTrue(np.all(models[1].multiplier==1))
        self.assertTrue(np.all(models[2].multiplier==1))

    def test_snapshot_reset_and_rejection(self):
        m = Model(self.c)
        m.multiplier[:] = .8
        m.r[:] = .2
        s = json.loads(canonical(m.snapshot()))
        m.reset_fast_state()
        np.testing.assert_array_equal(m.multiplier,.8)
        m.restore(s)
        self.assertEqual(m.snapshot(),s)
        with self.assertRaises(ValueError):
            Model(self.c,replace(Parameters(),learning_rate=.04)).restore(s)
        s['rate'][0] = float('nan')
        with self.assertRaises(ValueError):
            m.restore(s)

    def test_silent_recovery_matches_steps(self):
        a,b = Model(self.c),Model(self.c)
        a.multiplier[:] = .8
        b.multiplier[:] = .8
        a.idle(1)
        for _ in range(100):
            b.step(np.zeros(self.c.n))
        np.testing.assert_allclose(a.multiplier,b.multiplier,atol=1e-13,rtol=0)
        self.assertEqual(a.tick,b.tick)
        a.r[0]=.1
        with self.assertRaises(ValueError):
            a.idle(1)

    def test_parameter_validation(self):
        for p in (replace(Parameters(),dt=.1), replace(Parameters(),recovery_tau=0),
                  replace(Parameters(),learning_rate=-1), replace(Parameters(),kc_threshold=float('nan'))):
            with self.assertRaises(ValueError):
                Model(self.c,p)


if __name__ == '__main__':
    unittest.main(verbosity=2)

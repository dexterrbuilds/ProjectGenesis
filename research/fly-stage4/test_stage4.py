"""Reliability/identity tests; no fitting and no biological success by unit-test count."""
import json
import unittest
import numpy as np
from common import HERE, load, sha
from model import Model, Movie


class Stage4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.c=load('circuits/L0.json')

    def test_frozen_experimental_inputs(self):
        for p,h in load('MODEL_FREEZE.json')['files'].items(): self.assertEqual(sha(HERE/p),h)

    def test_unique_canonical_anatomy(self):
        byid={}
        for level in ['L0','L1']:
            c=load(f'circuits/{level}.json')
            self.assertEqual(len(c['edges']),len({e['id'] for e in c['edges']}))
            for e in c['edges']:
                self.assertIsInstance(e['pre_root_id'],str)
                self.assertIsInstance(e['post_root_id'],str)
                anatomical=(e['pre_root_id'],e['post_root_id'],e['neuropil'],e['contacts'])
                self.assertEqual(byid.setdefault(e['id'],anatomical),anatomical)
                if e['operator']=='unknown_excluded': self.assertIsNone(e['sign'])

    def test_blank_stationarity(self):
        m=Model(self.c)
        for _ in range(1000):m.step(np.full(len(m.points),.5))
        self.assertEqual(float(np.max(np.abs(m.rates))),0.)

    def test_finite_bounded_sensory_perturbation(self):
        m=Model(self.c,{'gain':2.,'tau':.02})
        rng=np.random.Generator(np.random.PCG64(100))
        for _ in range(1000):m.step(rng.random(len(m.points)))
        self.assertTrue(np.isfinite(m.rates).all())
        self.assertTrue((m.rates>=0).all())
        self.assertLess(float(m.rates.max()),1.)

    def test_snapshot_clock_rng_and_arrays(self):
        m=Model(self.c); rng=np.random.Generator(np.random.PCG64(81))
        before=[rng.random(len(m.points)) for _ in range(50)]
        after=[rng.random(len(m.points)) for _ in range(50)]
        for x in before:m.step(x)
        s=m.snapshot(); expected=[]
        for x in after:expected.append(m.step(x)[0].copy())
        m.restore(s); actual=[]
        for x in after:actual.append(m.step(x)[0].copy())
        np.testing.assert_array_equal(expected,actual)
        self.assertEqual(m.snapshot()['step_index'],100)
        bad=Model(self.c,{'gain':2.})
        with self.assertRaises(AssertionError):bad.restore(s)

    def test_route_intervention_preserves_upstream(self):
        a=Model(self.c); b=Model(self.c,intervention='route_remove')
        rng=np.random.Generator(np.random.PCG64(82))
        for _ in range(100):
            stimulus=rng.random(len(a.points)); a.step(stimulus); b.step(stimulus)
            np.testing.assert_array_equal(a.rates[a.motion],b.rates[b.motion])
        self.assertTrue(np.all(b.rates[b.outputs]==0))

    def test_retained_normalization_not_recomputed(self):
        a=Model(self.c,{'normalization':'retained'})
        b=Model(self.c,{'normalization':'retained'},'route_remove')
        surviving=(b.weights!=0).toarray()
        np.testing.assert_array_equal(a.weights.toarray()[surviving],b.weights.toarray()[surviving])

    def test_luminance_match_integral(self):
        # Uniform disk darkening equals the continuous area integral of the expanding disk.
        for t in [2.,2.5,3.,4.,4.75]:
            d=5+20*(t-2)
            dim=Movie('dim',[0,0],.005).intensity(np.array([[0.,0.]]),t)[0]
            self.assertAlmostEqual(np.pi*30**2*(.5-dim),np.pi*(d/2)**2*.5,places=10)

    def test_no_plastic_or_semantic_state(self):
        state=Model(self.c).snapshot()
        self.assertEqual(set(state),{'model_identity','rates','motion_delay','step_index','clock_seconds','initialized','prng'})


if __name__=='__main__':unittest.main()

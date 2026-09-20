"""Integrity tests; passing these never establishes motivational persistence."""
from dataclasses import replace
import ast
import json
from pathlib import Path
import unittest
import numpy as np
from model import Circuit,Model,Parameters,canonical
from experiment import patterns,protocol

HERE=Path(__file__).resolve().parent

class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.c=Circuit(next((HERE/'artifacts').iterdir()))
    def test_anatomy(self):
        c=self.c
        self.assertEqual((c.n,len(set(zip(c.pre,c.post))),int(c.count.sum())),(4563,304192,905536))
        self.assertTrue(all(type(x) is str for x in c.ids))
        m=Model(c);self.assertTrue(np.all(c.roles[m.plastic_pre]=='KC'))
        self.assertTrue(np.all(c.roles[m.plastic_post[m.learnable]]=='MB11'))
    def test_sensory_matching(self):
        for seed in (3701,3702,3703):
            p=patterns(self.c,seed);self.assertEqual(len(p['A']),len(p['B']));self.assertFalse(set(p['A'])&set(p['B']))
            for q in p:
                a=protocol(self.c,Parameters(),p[q],.2);b=protocol(self.c,Parameters(),p[q],.8)
                self.assertEqual(a['events'],b['events']);self.assertEqual(a['sensory_hash'],b['sensory_hash'])
                self.assertTrue(all(self.c.roles[self.c.index[root]]=='PN' for e in a['events'] for root,v in e['currents']))
    def test_no_tonic_drive(self):
        for body in (.2,.8):
            m=Model(self.c,resource=body)
            for _ in range(50):m.step(np.zeros(self.c.n),body)
            self.assertTrue(np.all(m.r==0));self.assertTrue(np.all(m.multiplier==1))
    def test_body_time_constant(self):
        m=Model(self.c,resource=.2)
        for _ in range(100):m.step(np.zeros(self.c.n),.8)
        self.assertAlmostEqual(m.body,.8-.6*np.exp(-1/60),places=13)
        self.assertTrue(np.all(m.r==0))
    def test_modulation_is_local(self):
        a,b=Model(self.c,resource=.2),Model(self.c,resource=.8)
        current=np.zeros(self.c.n);current[self.c.groups['DAN']]=.5
        current[self.c.groups['PN'][0]]=.5
        a.step(current,.2);b.step(current,.8)
        other=self.c.roles!='DAN';np.testing.assert_array_equal(a.r[other],b.r[other])
        self.assertTrue(np.all(a.r[self.c.groups['DAN']]<b.r[self.c.groups['DAN']]))
    def test_freeze_body_gate(self):
        a=Model(self.c,resource=.2,intervention='freeze_modulation');b=Model(self.c,resource=.8,intervention='freeze_modulation')
        current=np.ones(self.c.n)*.1
        for _ in range(20):a.step(current,.2);b.step(current,.8)
        np.testing.assert_array_equal(a.r,b.r);np.testing.assert_array_equal(a.multiplier,b.multiplier)
    def test_lesion_denominators(self):
        a,b=Model(self.c),Model(self.c,intervention='remove_mb11_mb18')
        mask=(self.c.roles[self.c.pre]=='MB11')&(self.c.roles[self.c.post]=='MB18')
        self.assertTrue(np.all(b.weights[mask]==0));np.testing.assert_array_equal(a.weights[~mask],b.weights[~mask])
    def test_inhibitory_lh_feedback(self):
        m=Model(self.c);ids=self.c.roles[self.c.pre]=='LHCENT'
        self.assertTrue(np.all(m.weights[ids]<=0))
    def test_snapshot_and_reset(self):
        m=Model(self.c);m.multiplier[:]=.8;m.r[:]=.1;s=json.loads(canonical(m.snapshot()))
        m.reset_fast_state();self.assertTrue(np.all(m.multiplier==.8));self.assertEqual(m.body,.2)
        m.restore(s);self.assertEqual(m.snapshot(),s)
        with self.assertRaises(ValueError):Model(self.c,replace(Parameters(),tau=.1)).restore(s)
        s['body']=float('nan')
        with self.assertRaises(ValueError):m.restore(s)
    def test_no_decision_or_application_state(self):
        m=Model(self.c)
        self.assertEqual(set(m.snapshot()),{'model','fingerprint','manifest','rate','eligibility','plastic_multiplier','body','tick','prng'})
        tree=ast.parse((HERE/'model.py').read_text())
        names={x.module.split('.')[0] for x in ast.walk(tree) if isinstance(x,ast.ImportFrom)}
        names|={n.name.split('.')[0] for x in ast.walk(tree) if isinstance(x,ast.Import) for n in x.names}
        self.assertLessEqual(names,{'copy','dataclasses','hashlib','json','pathlib','numpy','scipy'})
    def test_selective_plasticity_unit(self):
        for condition,expected in [('intact',True),('freeze_plasticity',False),('remove_da_gate',False)]:
            m=Model(self.c,intervention=condition)
            m.r[self.c.groups['DAN']]=.5;m.eligibility[self.c.groups['KC']]=1
            m.step(np.zeros(self.c.n),.2)
            self.assertEqual(bool(np.any(m.multiplier[m.learnable]<1)),expected)
            self.assertTrue(np.all(m.multiplier[~m.learnable]==1))

if __name__=='__main__':unittest.main(verbosity=2)

"""Dependency, result reproducibility and preservation checks. No neural experiments."""
import ast
import json
import unittest
from common import HERE, ROOT, STAGE4, load, save, sha, digest
from algebraic_checks import run as algebra

SPEC='6b3a27ea3c41a87e701ca8a7eec7fd31d5e41469db7da27916b81cb040eb923e'
PACKAGE='405d5e982b75846c0e24949f27effd122c3171ebbec77932a30da17b90e3c66a'

class Checks(unittest.TestCase):
    def test_release_pins(self):
        lock=load('DEPENDENCY_LOCK.json')
        self.assertEqual(lock['brain_spec_sha256'],SPEC)
        self.assertEqual(lock['stage4_content_sha256'],PACKAGE)
        rel=json.loads((ROOT/'research/genesis-brain-spec-v0.1/RELEASE.json').read_text())
        self.assertEqual(rel['registry']['sha256'],SPEC)
        self.assertEqual(sha(ROOT/'research/genesis-brain-spec-v0.1'/rel['registry']['path']),SPEC)
        self.assertEqual(sha(STAGE4/'PACKAGE_MANIFEST.json'),lock['stage4_manifest_sha256'])
    def test_prospective_plan(self):
        self.assertEqual(sha(HERE/'PLAN.md'),load('DIAGNOSTIC_REGISTRATION.json')['plan_sha256'])
        self.assertEqual(sha(HERE/'SOURCE_DATA_ADDENDUM.md'),load('SOURCE_DATA_REGISTRATION.json')['addendum_sha256'])
        self.assertFalse(load('SOURCE_DATA_REGISTRATION.json')['recording_values_inspected'])
    def test_algebra(self):self.assertEqual(algebra(),load('ALGEBRAIC_CHECKS.json'))
    def test_fly_independence(self):
        x=load('INDEPENDENT_RESULTS.json')
        self.assertEqual((x['n_flies'],x['n_rois']),(7,70))
        self.assertEqual(sum(f['rois'] for f in x['flies']),70)
        self.assertEqual(len({r['row'] for r in x['roi_rows']}),70)
        for f in x['flies']:
            others=[g['on'] for g in x['flies'] if g['fly']!=f['fly']]
            self.assertAlmostEqual(f['signed_prediction'],sum(others)/len(others),places=14)
    def test_negative_result_preserved(self):
        x=load('INDEPENDENT_RESULTS.json')
        self.assertGreater(x['signed_lofo_mse'],x['zero_lofo_mse'])
        self.assertEqual(x['signed_improves_folds'],3)
    def test_anatomy_balance(self):
        for level,x in load('ANATOMY_AUDIT.json')['levels'].items():
            self.assertEqual(sha(STAGE4/f'circuits/{level}.json'),x['frozen_circuit_sha256'])
            for t,p in x['populations'].items():
                self.assertEqual(p['full_input_contacts'],p['retained_input_contacts']+p['omitted_input_contacts'])
                self.assertEqual(p['retained_input_contacts'],p['effective_input_contacts']+p['retained_unknown_operator_contacts'])
                if t.startswith(('T4','T5')):self.assertEqual(p['effective_input_contacts'],0)
            self.assertEqual(len(x['geometry']),3)
            self.assertEqual(sum(len(g['afferents']) for g in x['geometry']),24)
    def test_estimators_no_stage4_data(self):
        # Static boundary guard plus manual dataflow review; not a universal sandbox proof.
        for name in ('independent_data.py','algebraic_checks.py'):
            s=(HERE/name).read_text();tree=ast.parse(s)
            self.assertNotIn('STAGE4',s)
            self.assertNotIn('MEASUREMENTS.csv',s)
            self.assertNotIn('ANALYSIS.json',s)
            for n in ast.walk(tree):
                if isinstance(n,(ast.Import,ast.ImportFrom)):
                    names=[a.name for a in n.names]
                    module=getattr(n,'module','') or ''
                    self.assertFalse(any(z in module or z in names for z in ('model','planner','wallet')))
    def test_evidence_categories(self):
        ids={s['id'] for s in load('EVIDENCE.json')['sources']}
        for e in load('TRANSFORMATIONS.json')['entries']:
            self.assertIn(e['classification'],['experimentally measured','experimentally constrained','weakly constrained','engineering assumption','unidentified'])
            self.assertTrue(set(e['evidence'])<=ids)
        self.assertEqual(load('TRANSFORMATIONS.json')['parameters_transferred_to_neural_models'],[])
    def test_frozen_observations(self):
        self.assertEqual(load('DEPENDENCY_LOCK.json')['stage4_classification'],{'Gate A':'NOT SUPPORTED','Gate B':'NOT TESTED'})
        self.assertEqual(load('ALGEBRAIC_CHECKS.json')['stage4_simulation_runs'],0)
    def test_canonical_state(self):
        a=load('CANONICAL_BEFORE.json');b=load('CANONICAL_AFTER.json')
        self.assertEqual(a,b)
        self.assertEqual(a['sha256'],'3377c9dddbe2abf89ed9a820a6aabbc1da951cac7bfc1823471c5aac043ea312')
        self.assertEqual(a['tableRowCounts']['genesis_decisions'],7)
        self.assertFalse(any(s['enabled'] for s in a['schedule']))
    def test_preservation(self):
        bad=[];protected=load('FROZEN_BEFORE.json')
        for p,h in protected.items():
            if not (ROOT/p).is_file() or sha(ROOT/p)!=h:bad.append(p)
        self.assertEqual(bad,[])
        save('PRESERVATION.json',{'files_checked':len(protected),'changed':bad,'canonical_sha256':load('CANONICAL_AFTER.json')['sha256'],
             'canonical_cycles':7,'schedule_enabled':False,'new_life_cycles_run':0,'stage4_reruns':0})

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Checks))
    save('VALIDATION.json',{'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'passed':result.wasSuccessful(),
         'scope':'isolated diagnostic checks; old neural suites not rerun; frozen artifacts hash-audited'})
    raise SystemExit(0 if result.wasSuccessful() else 1)

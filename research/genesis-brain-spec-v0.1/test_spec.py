"""Adversarial infrastructure tests. No experiment, model import, or Genesis cycle."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from build import HERE, ROOT, ENG, HYP, FACT, PRODUCT, digest, file_hash
from validate import Invalid, strict_load, load_release, validate_structure, entries_by_id
from policy import check_frozen_policy, check_experiment, check_revision, check_profiles


class SpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.release, cls.registry = load_release(verify_files=True, verify_rows=True)
        cls.entries = entries_by_id(cls.registry)
        cls.shared = strict_load(ROOT / cls.registry['sources']['shared-rows']['path'])

    def example(self):
        uses = ['anatomy.pinned', 'transmission.pn-kc', 'representation.apl-local']
        return {'schema_version': '1', 'id': 'example.preflight-only',
                'registry_sha256': self.release['registry']['sha256'],
                'dependencies': {cid: digest(self.entries[cid]) for cid in uses}, 'uses': uses,
                'input_channels': [{'id': 'cue_pattern', 'kind': 'sensory_pattern', 'category': ENG,
                                    'evidence_refs': ['transmission.pn-kc'], 'units': 'model_current'}],
                'anatomy_views': [{'module': 'view-a', 'row_ids': [self.shared['KC_MBON07'][0]], 'mode': 'reference'},
                                  {'module': 'view-b', 'row_ids': [self.shared['KC_MBON07'][0]], 'mode': 'reference'}],
                'state_ownership': [], 'local_states': [], 'proposed_assumptions': [],
                'result_claims': [], 'integration': 'isolated_research_only'}

    def mutate(self, cid, **changes):
        r = copy.deepcopy(self.registry)
        e = next(e for e in r['entries'] if e['id'] == cid)
        e.update(changes)
        r['entry_hashes'][cid] = digest(e)  # Deliberate rehash: semantic protection is exercised.
        return r

    def reject_experiment(self, manifest, message):
        with self.assertRaisesRegex(Invalid, message):
            check_experiment(manifest, self.release, self.registry)

    def test_frozen_release_valid(self):
        check_frozen_policy(self.registry)

    def test_parameter_inventory_exact(self):
        expected = strict_load(ROOT / self.registry['sources']['parameters']['path'])
        actual = [e['historical_record'] for e in self.registry['entries'] if e['kind'] == 'parameter']
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 65)

    def test_mechanism_profile_facets_and_provenance(self):
        self.assertEqual(len(check_profiles(self.registry)['profiles']), 11)

    def test_example_manifest_valid(self):
        check_experiment(strict_load(HERE / 'EXPERIMENT.example.json'), self.release, self.registry)

    def test_unvalidated_local_state_proposal_keeps_neuron_identity(self):
        m = self.example()
        neuron = 'FAFB-FlyWire:783:720575940624547622'
        m['local_states'] = [{'id': neuron + ':proposal-calyx:calcium', 'neuron_id': neuron,
                              'partition': 'unassigned-proposal', 'kind': 'calcium',
                              'evidence_refs': ['representation.apl-local'], 'assignment_status': 'proposal_only'}]
        check_experiment(m, self.release, self.registry)
        m['local_states'][0]['assignment_status'] = 'validated'
        self.reject_experiment(m, 'no root-specific physiological local state map')

    def test_shared_rows_are_references_not_duplicate_owners(self):
        self.assertEqual(len(self.shared['KC_MBON07']), 4622)
        self.assertEqual(len(self.shared['KC_MBON11']), 1053)
        check_experiment(self.example(), self.release, self.registry)

    def test_persistence_promotion(self):
        r = self.mutate('capability.persistence', status='validated_narrow_model')
        with self.assertRaisesRegex(Invalid, 'Unsupported capability'):
            check_frozen_policy(r)

    def test_unresolved_pathway_promotion(self):
        r = self.mutate('sign.mbon07-pam11', status='validated_scoped')
        with self.assertRaisesRegex(Invalid, 'Hypothesis/product'):
            check_frozen_policy(r)

    def test_hypothesis_relabelled_fact(self):
        r = self.mutate('sign.mbon07-pam11', category=FACT, status='supported')
        with self.assertRaisesRegex(Invalid, 'Frozen evidence changed'):
            check_frozen_policy(r)

    def test_known_sign_without_provenance(self):
        r = self.mutate('connection.MBON07.PAM11', sign={'state': 'experimentally_constrained', 'value': 'positive',
                                                      'scope': 'PAM11', 'evidence_refs': []})
        with self.assertRaisesRegex(Invalid, 'sign requires provenance'):
            validate_structure(r)

    def test_wrong_scope_citation_cannot_identify_sign(self):
        r = self.mutate('connection.MBON07.PAM11', sign={'state': 'experimentally_constrained', 'value': 'positive',
                                                      'scope': 'PAM11', 'evidence_refs': ['E16']})
        with self.assertRaisesRegex(Invalid, 'Frozen evidence changed'):
            check_frozen_policy(r)

    def test_unknown_is_not_zero(self):
        r = self.mutate('connection.MBON07.PAM11', sign={'state': 'unknown', 'value': 0, 'reason': 'not measured', 'evidence_refs': []})
        with self.assertRaisesRegex(Invalid, 'Unknown must remain explicit null'):
            validate_structure(r)

    def test_numeric_root_rejected(self):
        r = self.mutate('population.s1.APL', root_ids=[720575940624547622])
        with self.assertRaisesRegex(Invalid, 'decimal strings'):
            validate_structure(r)

    def test_duplicate_entry_rejected(self):
        r = copy.deepcopy(self.registry)
        r['entries'].append(copy.deepcopy(r['entries'][0]))
        with self.assertRaisesRegex(Invalid, 'Duplicate evidence'):
            validate_structure(r)

    def test_duplicate_canonical_state_ownership(self):
        m = self.example()
        owner = {'row_id': self.shared['KC_MBON07'][0], 'model_instance': 'composed', 'state_kind': 'efficacy',
                 'owner': 'stage1', 'operator_ref': 'anatomy.pinned'}
        m['state_ownership'] = [owner, {**owner, 'owner': 'stage3'}]
        self.reject_experiment(m, 'Duplicate canonical synapses')

    def test_single_shared_rule_still_blocked(self):
        m = self.example()
        m['state_ownership'] = [{'row_id': self.shared['KC_MBON11'][0], 'model_instance': 'composed',
                                 'state_kind': 'efficacy', 'owner': 'unified', 'operator_ref': 'anatomy.pinned'}]
        self.reject_experiment(m, 'Shared physiological rules unresolved')

    def test_owned_anatomy_view_rejected(self):
        m = self.example(); m['anatomy_views'][0]['mode'] = 'own'
        self.reject_experiment(m, 'Duplicate canonical synapse ownership')

    def test_unknown_canonical_row_rejected(self):
        m = self.example(); m['anatomy_views'][0]['row_ids'] = ['0' * 64]
        self.reject_experiment(m, 'Unknown canonical connection')

    def test_product_category_cannot_be_biological(self):
        r = self.mutate('product.resource-runway', layer='biological')
        with self.assertRaisesRegex(Invalid, 'Product category/layer'):
            validate_structure(r)

    def test_product_rename_does_not_launder(self):
        r = self.mutate('product.resource-runway', layer='biological', category=FACT)
        with self.assertRaisesRegex(Invalid, 'Product namespace'):
            validate_structure(r)

    def test_wallet_input_rejected(self):
        m = self.example(); m['input_channels'][0]['id'] = 'wallet_balance'
        self.reject_experiment(m, 'Product concept/hidden answer')

    def test_money_unit_rejected(self):
        m = self.example(); m['input_channels'][0]['units'] = 'USD'
        self.reject_experiment(m, 'Unreviewed/product unit')

    def test_hidden_novelty_input_rejected(self):
        m = self.example(); m['input_channels'][0]['id'] = 'seen_count'
        self.reject_experiment(m, 'Product concept/hidden answer')

    def test_product_dependency_rejected(self):
        m = self.example(); cid = 'product.resource-runway'
        m['dependencies'][cid] = digest(self.entries[cid]); m['uses'].append(cid)
        self.reject_experiment(m, 'Product mapping imported')

    def test_synthetic_current_is_not_biological_fact(self):
        m = self.example(); m['input_channels'][0]['category'] = FACT
        self.reject_experiment(m, 'Synthetic stimulation/body')

    def test_hypothesis_cannot_self_validate(self):
        m = self.example()
        m['proposed_assumptions'] = [{'id': 'hypothesis.new-path', 'category': HYP, 'status': 'validated',
                                      'statement': 'Candidate pathway', 'depends_on': ['anatomy.pinned']}]
        self.reject_experiment(m, 'Unsupported pathway marked validated')

    def test_product_prose_cannot_masquerade_as_assumption(self):
        m = self.example()
        m['proposed_assumptions'] = [{'id': 'hypothesis.state', 'category': HYP, 'status': 'unvalidated',
                                      'statement': 'This state measures business profit.', 'depends_on': ['anatomy.pinned']}]
        self.reject_experiment(m, 'Product concept in biological assumption')

    def test_missing_dependency_rejected(self):
        m = self.example(); m['dependencies'].pop('transmission.pn-kc')
        self.reject_experiment(m, 'Used evidence omitted')

    def test_stale_dependency_rejected(self):
        m = self.example(); m['dependencies']['anatomy.pinned'] = '0' * 64
        self.reject_experiment(m, 'Stale/unknown evidence')

    def test_override_field_rejected(self):
        m = self.example(); m['overrides'] = {'s2': 'PASS'}
        self.reject_experiment(m, 'overrides forbidden')

    def test_result_promotion_rejected(self):
        m = self.example(); m['result_claims'] = [{'id': 'persistence', 'status': 'validated'}]
        self.reject_experiment(m, 'Results cannot promote claims')

    def test_changed_study_classification_rejected(self):
        r = copy.deepcopy(self.registry); r['studies'][1]['classification'] = 'PASS'
        with self.assertRaisesRegex(Invalid, 'Frozen study classification'):
            check_frozen_policy(r)

    def test_parameter_value_not_measured(self):
        cid = next(e['id'] for e in self.registry['entries'] if e['kind'] == 'parameter')
        r = self.mutate(cid, physiological_value={'state': 'known', 'value': 0.01})
        with self.assertRaisesRegex(Invalid, 'Historical parameter promoted'):
            validate_structure(r)

    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'bad.json'; p.write_text('{"status":"unsupported","status":"validated"}')
            with self.assertRaisesRegex(Invalid, 'Duplicate JSON key'):
                strict_load(p)

    def test_explicit_reviewed_supersession_contract(self):
        # Synthetic TEST ONLY evidence, not a scientific admission or published artifact.
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            evidence = Path(tmp) / 'test-only-evidence.txt'
            evidence.write_text('TEST FIXTURE ONLY: no scientific evidence or experiment.')
            old_id = 'sign.mbon07-pam11'
            candidate = copy.deepcopy(self.registry); candidate['version'] = '0.2.0-test-only'
            candidate['sources']['TEST_ONLY'] = {'path': str(evidence.relative_to(ROOT)), 'sha256': file_hash(evidence),
                                                'kind': 'independent_evidence', 'section': 'test fixture'}
            entry = {**copy.deepcopy(self.entries[old_id]), 'id': 'test-only.scoped-supersession',
                     'category': FACT, 'status': 'constrained', 'evidence_refs': ['TEST_ONLY'],
                     'statement': 'TEST ONLY; not a physiological claim.',
                     'supersedes': [{'id': old_id, 'sha256': digest(self.entries[old_id]), 'reason': 'TEST ONLY'}]}
            candidate['entries'].append(entry); candidate['entry_hashes'][entry['id']] = digest(entry)
            review = {'entry_id': entry['id'], 'entry_sha256': digest(entry), 'reviewer': 'TEST_FIXTURE',
                      'reviewed_at': '2026-09-18T00:00:00Z', 'rationale': 'Test validation mechanics only',
                      'independent_evidence_refs': ['TEST_ONLY'], 'supersedes': entry['supersedes'], 'scope': entry['scope']}
            check_revision(self.registry, candidate, [review])
            with self.assertRaisesRegex(Invalid, 'separate review record'):
                check_revision(self.registry, candidate, [])
            bad = copy.deepcopy(candidate)
            bad['entries'][0]['status'] = 'overridden'; bad['entry_hashes'][bad['entries'][0]['id']] = digest(bad['entries'][0])
            with self.assertRaisesRegex(Invalid, 'Frozen entry modified'):
                check_revision(self.registry, bad, [review])
            bad = copy.deepcopy(candidate); bad['stage4_contract']['authorized_now'] = True
            with self.assertRaisesRegex(Invalid, 'governance'):
                check_revision(self.registry, bad, [review])
            bad = copy.deepcopy(candidate)
            bad['sources']['TEST_ONLY'] = {**self.registry['sources']['s1'], 'kind': 'independent_evidence'}
            with self.assertRaisesRegex(Invalid, 'Renaming an old source'):
                check_revision(self.registry, bad, [review])


if __name__ == '__main__':
    unittest.main(verbosity=2)

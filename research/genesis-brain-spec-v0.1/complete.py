"""Create documentation indexes and a preflight-only example from the existing release.

Additive completion: does not rebuild or replace RELEASE.json, the registry, or anatomy.
"""
import json
from build import HERE, ROOT, canonical, digest, immutable, unknown, FACT, ENG
from validate import load_release, entries_by_id
from policy import check_frozen_policy


def main():
    release, registry = load_release()
    entries = check_frozen_policy(registry)
    definitions = [
        ('PN_KC', ['connection.PN.KC'], ['transmission.pn-kc'],
         'Cholinergic PN convergence onto KC claws; class-level nonlinear/sparse integration.',
         'No contact-to-claw or current-to-rate calibration; threshold and gain confounded.',
         'Scalar integration is a candidate; the available summary measurements do not select R0/R1/R3.'),
        ('KC_MBON07_alpha1', ['connection.KC.MBON07'], ['transmission.kc-mbon', 'plasticity.appetitive-model', 'integration.shared-rules'],
         'KC cholinergic transmission; alpha1 correspondence is type-based.',
         'Stage-1 DAN-to-KC gated LTD is an implemented hypothesis; no independent alpha1 eta or eligibility constant.',
         'Local plastic state may belong to an existing anatomical row; electrical compartment count unidentified.'),
        ('KC_MBON11_gamma1pedc', ['connection.KC.MBON11'], ['transmission.kc-mbon', 'plasticity.gamma1', 'integration.shared-rules'],
         'Gamma1pedc physiology constrains aggregate conditioning under its own protocol.',
         'Stage-1 and Stage-3 update rules conflict; Hige endpoint identifies eta times unobserved exposure, not each factor.',
         'No shared canonical physiology assigned; cell identity shared, update operators remain alternatives.'),
        ('KC_MBON16_17_alpha_prime3', ['connection.KC.MBON16', 'connection.KC.MBON17'], ['plasticity.alpha-prime3', 'plasticity.familiarity-model'],
         'Female alpha-prime3 odor repetition/receptor experiments support local response plasticity.',
         'Driver-to-root equivalence incomplete; recovery at 20 min/1 h does not identify an exponential tau.',
         'Postsynaptic/release/local state is a candidate; no fitted per-contact receptor rule.'),
        ('APL_KC', ['connection.APL.KC', 'connection.KC.APL'], ['transmission.apl-kc', 'representation.apl-local', 'representation.apl-coupling'],
         'Local calcium responses and inhibitory effects are measured in the audited preparations.',
         'Calcium coupling does not identify voltage coupling or inhibitory conductance. Nonzero coupling unidentified.',
         'APL local response states justified for tested assays; not a universal multi-voltage-neuron requirement.'),
        ('MBON07_PAM11', ['connection.MBON07.PAM11'], ['sign.mbon07-pam11'],
         'Glutamate annotation and NMDA requirement motivate a feedback hypothesis.',
         'Direct net sign and target-specific efficacy unknown; AL GluCl physiology cannot assign the alpha1 sign.',
         'Positive feedback operator is an assumption, not an independently identified transmission law.'),
        ('compartment_dopamine', ['connection.PAM11.KC', 'connection.PPL101.KC', 'connection.PPL101.MBON11', 'connection.PPL104.MBON16', 'connection.PPL104.MBON17'], ['modulation.da-locality', 'representation.r2'],
         'Compartment, timing and receptor mechanisms are supported in distinct physiological preparations.',
         'DAN-to-KC versus DAN-to-MBON exposure maps, receptor occupancy, diffusion and dose-to-rate mapping unknown.',
         'Separate DAN activity, local modulation, eligible synapses and plastic state conceptually; do not invent fields or contacts.'),
        ('resource_PPL101_MBON11_18', ['connection.PPL101.MBON11', 'connection.MBON11.MBON18'], ['modulation.resource-biological', 'modulation.resource-model'],
         'Hunger-linked PPL101/MBON expression has directional experimental support.',
         'Synthetic 0.2+0.8r, body tau 60 s and acute 1/(1+D) are not starvation or receptor measurements.',
         'The body boundary is engineering state, distinct from neural modulation; no persistence/withdrawal readout validated.'),
        ('OA_VPM4_MBON11', ['connection.OA.MBON11'], ['modulation.oa-vpm4'],
         'VPM4 activation suppresses MBON11 responses in Sayin assay.',
         'Target/root receptor map, natural drive, magnitude and kinetics unknown; OA boundary retention is low.',
         'Target-specific effective suppression is a scoped observation, not a universal octopamine sign.'),
        ('MBON18_LH_LHCENT', ['connection.MBON18.LH', 'connection.LH.LHCENT'], ['modulation.resource-model', 'architecture.selection'],
         'Pinned chemical paths provide anatomical interaction candidates.',
         'Low input/output retention, aliases and target-specific physiology limit interpretation; anatomy is not functional persistence.',
         'No downstream motor/decision interpretation or common physiological state operator established.'),
        ('dNPF_NO_endocrine', [], ['modulation.peptide-no'],
         'State and memory experiments implicate peptide, NO and endocrine mechanisms.',
         'No resolved root-level peptide/receptor graph or numerical kinetics; missing edges do not imply zero signaling.',
         'No instantiated fields, fabricated anatomical connections or inferred numerical physiological variables.'),
    ]
    profiles = []
    for name, conns, claims, fact, unresolved, representation in definitions:
        deps = conns + claims + ['crosswalk.type', 'normalization.contact-mass']
        profiles.append({
            'id': 'profile.' + name, 'purpose': 'Index of existing scoped claims, not new evidence or physiology ownership',
            'dependencies': {cid: digest(entries[cid]) for cid in deps},
            'canonical_connection_views': conns,
            'identity_resolution': 'Follow the connection selectors and neuron annotation observations; no new root/compartment crosswalk.',
            'anatomical_evidence': {'entry_ref': 'anatomy.pinned', 'ownership': 'reference_only'},
            'transmitter_and_experimental_effect': {'category': FACT, 'scope': 'preparation/type level only',
                                                    'statement': fact, 'claim_refs': claims},
            'postsynaptic_root_receptor_map': unknown(),
            'root_specific_sign_confidence': 'unknown; any supported experimental effect retains its narrower preparation scope',
            'representation_requirement': {'category': ENG, 'statement': representation, 'claim_refs': claims},
            'local_versus_global_state': 'No global modulator equivalence or extra electrical compartments inferred from this index.',
            'temporal_constraints': {'claim_refs': claims, 'numerical_transfer': unknown()},
            'normalization_evidence': {'entry_ref': 'normalization.contact-mass', 'identified_denominator': unknown()},
            'plasticity_evidence': {'claim_refs': claims, 'common_operator': unknown()},
            'parameter_evidence': {'source_ref': 'parameters', 'mode': 'historical assumptions separate from physiological estimates'},
            'observation_model': {'transfer_to_frozen_rate_units': unknown(), 'constraint': 'Fluorescence, current, spikes, release and behavior are distinct observables.'},
            'source_preparation_compatibility': {'entry_ref': 'crosswalk.type', 'rule': 'Do not transfer constants across sex/type/compartment/assay without evidence.'},
            'validated_interventions': {'source_refs': sorted({s for cid in claims for s in entries[cid]['evidence_refs']}),
                                        'qualification': 'Only the interventions and scope reported by these frozen entries; no new validation here.'},
            'known_conflicts': {'entry_ref': 'integration.shared-rules', 'common_rule_status': 'unresolved_non_composable'},
            'unsupported_extrapolations': [unresolved],
            'allowed_scientific_wording': [fact, unresolved],
            'prohibited_scientific_wording': ['This profile validates a common physiological kernel or a Genesis behavioral capability.'],
        })
    companion = {'version': '0.1.0', 'registry_sha256': release['registry']['sha256'],
                 'claim_ownership': 'all profiles reference existing entries; no evidence classification is overridden',
                 'profiles': profiles}
    data = canonical(companion) + b'\n'
    import hashlib
    sha = hashlib.sha256(data).hexdigest()
    immutable(HERE / 'objects' / (sha + '.json'), data)
    immutable(HERE / 'MECHANISM_PROFILES.json', json.dumps({'path': f'objects/{sha}.json', 'sha256': sha}, indent=2).encode() + b'\n')
    dep_ids = ['anatomy.pinned', 'transmission.pn-kc', 'representation.apl-local']
    example = {'schema_version': '1', 'id': 'example.preflight-only', 'registry_sha256': release['registry']['sha256'],
               'dependencies': {cid: digest(entries[cid]) for cid in dep_ids}, 'uses': dep_ids,
               'input_channels': [{'id': 'cue_pattern', 'kind': 'sensory_pattern', 'category': ENG,
                                   'evidence_refs': ['transmission.pn-kc'], 'units': 'model_current'}],
               'anatomy_views': [], 'state_ownership': [], 'local_states': [], 'proposed_assumptions': [],
               'result_claims': [], 'integration': 'isolated_research_only'}
    immutable(HERE / 'EXPERIMENT.example.json', json.dumps(example, indent=2).encode() + b'\n')
    lines = ['# Evidence index — v0.1.0', '',
             'Generated from the pinned registry. This index does not assign additional physiology.', '',
             '| Entry | Category | Status |', '|---|---|---|']
    lines += [f'| `{e["id"]}` | {e["category"]} | {e["status"]} |' for e in registry['entries']]
    immutable(HERE / 'EVIDENCE_INDEX.md', ('\n'.join(lines) + '\n').encode())
    print(json.dumps({'profile_count': len(profiles), 'profile_sha256': sha, 'example_is_not_an_experiment': True}))


if __name__ == '__main__':
    main()

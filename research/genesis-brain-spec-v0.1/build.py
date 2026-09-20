"""Synthesize frozen evidence. No model import, simulation, fitting, or database access."""
from pathlib import Path
import collections
import gzip
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
VERSION = '0.1.0'
DATASET = 'FAFB-FlyWire:783'


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False,
                      allow_nan=False).encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def load(rel):
    return json.loads((ROOT / rel).read_text())


def immutable(path, data):
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError(f'Refusing to overwrite {path}; publish a new version')
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


FACT = 'BIOLOGICAL FACT'
APPROX = 'EXPERIMENTALLY SUPPORTED COMPUTATIONAL APPROXIMATION'
HYP = 'HYPOTHESIS'
ENG = 'ENGINEERING ASSUMPTION'
PRODUCT = 'GENESIS PRODUCT MAPPING'


def unknown(reason='No transferable physiological measurement identifies this quantity.'):
    return {'state': 'unknown', 'value': None, 'reason': reason, 'evidence_refs': []}


def build():
    protected = load('research/genesis-brain-spec-v0.1/FROZEN_INPUTS.json')
    for path, sha in protected.items():
        if file_hash(ROOT / path) != sha:
            raise ValueError(f'Frozen input changed: {path}')
    sources = {}

    def source(key, path, kind='frozen_research', section=None):
        sources[key] = {'path': path, 'sha256': file_hash(ROOT / path),
                        'kind': kind, 'section': section}
        return key

    for key, directory in [('s1', 'fly-stage1'), ('s2', 'fly-stage2'),
                           ('s3', 'fly-stage3'), ('boundary', 'fly-boundary-study'),
                           ('physiology', 'fly-physiology-study'),
                           ('representation', 'fly-representation-study')]:
        source(key, f'research/{directory}/REPORT.md')
    for key, path in {
        'phys-evidence': 'fly-physiology-study/EVIDENCE.md',
        'repr-evidence': 'fly-representation-study/EVIDENCE.md',
        'parameters': 'fly-physiology-study/PARAMETER_EVIDENCE.json',
        'crosswalk': 'fly-physiology-study/CROSSWALK.json',
        'crosswalk-notes': 'fly-physiology-study/CROSSWALK.md',
        'conflicts': 'fly-boundary-study/UNIFIED_MODEL_CONFLICTS.md',
        'unified-physiology': 'fly-physiology-study/UNIFIED_PHYSIOLOGY.md',
        'identity': 'fly-representation-study/identity-registry.jsonl.gz',
        'identity-audit': 'fly-representation-study/IDENTITY_AUDIT.json',
        'identity-schema': 'fly-representation-study/IDENTITY_SCHEMA.md',
        'shared-rows': 'fly-representation-study/shared-row-ids.json',
        'apl-fit': 'fly-representation-study/FIT_FROZEN.json',
        'apl-validation': 'fly-representation-study/VALIDATION.json',
        'mbon-exclusion': 'fly-representation-study/MBON_SOURCE_AUDIT.md',
        'identifiability': 'fly-representation-study/IDENTIFIABILITY.md',
        'conditioning': 'fly-representation-study/TEMPORAL_CONDITIONING.json',
        'depression-identification': 'fly-physiology-study/IDENTIFICATION_FROZEN.json',
        'no-kernel-transfer': 'fly-physiology-study/TRANSFER_FROZEN.json',
        'scaling': 'fly-representation-study/SCALING.md',
    }.items():
        source(key, 'research/' + path)

    # Preserve the audited primary-source preparation and transfer limits verbatim.
    literature = {}
    for line in (ROOT / sources['phys-evidence']['path']).read_text().splitlines():
        if not re.match(r'^\| E\d\d ', line):
            continue
        cells = [s.strip() for s in line.strip('|').split('|')]
        eid = cells[0][:3]
        literature[eid] = {
            'id': eid, 'category': FACT, 'layer': 'biological',
            'citation': cells[0], 'urls': re.findall(r'\]\((https?://[^)]+)\)', cells[0]),
            'species': 'Drosophila melanogaster', 'preparation_and_measurement': cells[1],
            'observations': cells[2], 'transfer_limits': cells[3],
            'evidence_refs': ['phys-evidence'],
            'root_specific_physiology': False,
            'metadata_unknowns': 'Unresolved sex/age/preparation in the source audit remains unknown.',
        }
    for eid, token in [('R_APL', '[Amin 2020, Figure'), ('R_KC', '[Groschner 2018]'),
                       ('R_MBON', '[Hafez 2023]'), ('R_DA', '[Handler 2019]'),
                       ('R_RELEASE', '[Stahl 2022]')]:
        rows = [l for l in (ROOT / sources['repr-evidence']['path']).read_text().splitlines()
                if l.startswith('| ') and token in l]
        literature[eid] = {
            'id': eid, 'category': FACT, 'layer': 'biological',
            'species': 'Drosophila melanogaster', 'audited_rows': rows,
            'evidence_refs': ['repr-evidence'], 'root_specific_physiology': False,
            'status': 'excluded_from_clean_validation' if eid == 'R_MBON' else 'scoped_observations',
        }

    entries = []

    def claim(cid, category, status, scope, statement, refs, allowed, prohibited,
              conflicts=(), extrapolations=()):
        entries.append({'id': cid, 'kind': 'claim', 'category': category,
                        'layer': 'product' if category == PRODUCT else 'biological',
                        'status': status, 'scope': scope, 'statement': statement,
                        'evidence_refs': list(refs), 'known_conflicts': list(conflicts),
                        'unsupported_extrapolations': list(extrapolations),
                        'allowed_scientific_wording': allowed,
                        'prohibited_scientific_wording': prohibited,
                        'supersedes': []})

    claim('anatomy.pinned', FACT, 'supported', 'one adult female FAFB specimen, v783',
          'Pinned aggregate contacts and annotation identities constrain anatomy, not efficacy.',
          ['identity-audit', 'crosswalk'], ['Extracted from pinned adult female FlyWire anatomy.'],
          ['Each contact is a measured physiological synapse.', 'Root IDs identify the recorded flies.'])
    claim('crosswalk.type', FACT, 'constrained', 'annotation/type/driver crosswalk only',
          'Type aliases support population correspondence; individual physiology and driver membership are not root-resolved.',
          ['crosswalk', 'crosswalk-notes', 'repr-evidence'], ['Type-level correspondence, with explicit ambiguity.'],
          ['Hemibrain, physiological driver and FlyWire root are interchangeable.'])
    claim('transmission.pn-kc', FACT, 'constrained', 'tested adult PN/KC preparations',
          'Coactive claws, thresholded integration and sparse responses are supported; contacts are not claws.',
          ['E01', 'E02', 'E03'], ['Sparse nonlinear integration is experimentally supported.'],
          ['All cues activate exactly 5% of KCs.', 'PN gain 3 is physiological.'])
    claim('transmission.kc-mbon', FACT, 'constrained', 'tested KC/MBON cholinergic preparations',
          'KC cholinergic transmission and target nicotinic receptor requirements are supported at class level.',
          ['E04'], ['Cholinergic transmission is supported in tested targets.'],
          ['Every cholinergic contact has identical positive conductance.'])
    claim('transmission.apl-kc', FACT, 'constrained', 'tested local APL/KC assays',
          'APL activation inhibits KC responses with spatially heterogeneous effects.',
          ['E05', 'E06', 'R_APL'], ['APL inhibitory effects are spatially heterogeneous.'],
          ['A calcium mixing coefficient measures inhibitory conductance.'])
    claim('representation.apl-local', APPROX, 'validated_scoped', 'APL spatial fluorescence assays only',
          'Local response representations outperform a shared scalar with fixed linear observation gains; this does not identify multiple voltages.',
          ['apl-fit', 'apl-validation', 'repr-evidence'],
          ['Local APL response representation is supported for the audited spatial assays.'],
          ['All fly neurons require compartments.', 'A nonzero APL coupling constant was identified.'])
    claim('representation.apl-coupling', HYP, 'unresolved', 'APL inter-location coupling',
          'Locality does not identify nonzero coupling. Shared q interval includes zero; zero transfer is not universal across assays.',
          ['apl-validation', 'identifiability', 'R_APL'],
          ['Coupling magnitude remains unidentified; assay-specific zero-transfer controls are not anatomical absence.'],
          ['APL compartments are biologically disconnected.', 'q is a conductance.'])
    claim('representation.heterogeneous', ENG, 'proposed', 'future research identity/state schema',
          'One root owns one biological identity and may own justified local states; choose representation by cell type and observable.',
          ['identity-schema', 'representation'], ['Heterogeneous state ownership is a schema proposal.'],
          ['A unified physiological kernel has been validated.'])
    claim('representation.r2', HYP, 'constrained', 'tested receptor/target mechanisms only',
          'Target/receptor-aware effects are needed where measured; a complete root-specific receptor map is unknown.',
          ['E04', 'E09', 'E16', 'R_RELEASE'], ['Separate electrical, release, receptor and observation states when justified.'],
          ['Transmitter names determine all effective signs.'])
    claim('representation.r3', HYP, 'unresolved', 'specific KC subtype and MBON14 assays',
          'Measured channels/temporal scales constrain components, not a held-out validated common conductance kernel.',
          ['R_KC', 'E18', 'mbon-exclusion'], ['Some subtype-specific biophysical components are constrained.'],
          ['R3 is superior for every neuron.', 'MBON14 tau applies to MBON16/17.'])
    claim('observation.mbon-excluded', ENG, 'excluded', 'Hafez supplementary validation workbook',
          'Unresolved cell provenance/duplication and raw mean 16.9825 ms versus reported 14.48 ms exclude clean held-out validation.',
          ['mbon-exclusion', 'repr-evidence'], ['The supplemental workbook is excluded from clean validation pending authoritative resolution.'],
          ['The supplementary cells independently validate the temporal model.', 'Duplication is conclusively proven.'])
    claim('modulation.da-locality', FACT, 'constrained', 'tested mushroom-body compartments',
          'Compartment and timing specificity support local modulatory action. DAN electrical activity, exposure and eligibility are distinct.',
          ['E07', 'E08', 'E09', 'E19', 'R_RELEASE'], ['Compartment-specific modulation is supported; exposure mapping remains unknown.'],
          ['DAN contact counts equal receptor occupancy.', 'Dopamine always causes LTD.'])
    claim('plasticity.gamma1', FACT, 'constrained', 'Hige female gamma1pedc MBON11 protocol',
          'Charge-transfer depression 90 ± 3.7% SEM, n=5, constrains an integrated endpoint under the published protocol.',
          ['E07', 'depression-identification'], ['The endpoint identifies integrated depression, not a unique learning rate.'],
          ['Eta 0.08 or the 0.1 floor is experimentally calibrated.', 'This numerically calibrates appetitive alpha1.'])
    claim('plasticity.appetitive-model', ENG, 'validated_scoped', 'frozen Stage-1 appetitive computational experiment only',
          'Real extracted anatomy, prescribed local dopamine-dependent LTD and experience produce persistent selective response change.',
          ['s1'], ['Stage 1 validates narrow associative learning within its computational model.'],
          ['Stage 1 validates a physiological fly brain or general intelligence.', 'Exact PN topology is uniquely necessary.'])
    claim('plasticity.alpha-prime3', FACT, 'constrained', 'female alpha-prime3 response/receptor assays',
          'Repeated odors suppress responses with recovery; postsynaptic nicotinic mechanisms contribute. This is not a universal exponential rule.',
          ['E11', 'E12'], ['The biological candidate has response-level and receptor evidence.'],
          ['The Stage-2 effect establishes semantic novelty.', 'Recovery tau is known to be 1800 s.'])
    claim('plasticity.familiarity-model', ENG, 'partial_inconclusive', 'frozen Stage-2 model only',
          'Persistent stimulus-specific change exists but is far below preregistered thresholds and sensitive to assumptions.',
          ['s2'], ['A tiny model effect is not validated familiarity behavior.'], ['Genesis recognizes novelty.'])
    claim('modulation.resource-biological', FACT, 'constrained', 'published hunger/state-dependent fly assays',
          'State-dependent PPL101 and MBON expression is supported in specific preparations, not a numerical resource-to-neuron function.',
          ['E13', 'E14', 'E15', 'E20'], ['Published assays support state-dependent modulation.'],
          ['A scalar resource variable reproduces starvation physiology.'])
    claim('modulation.resource-model', ENG, 'partial_inconclusive', 'frozen Stage-3 synthetic body boundary',
          'Selective anatomy-dependent modulation and local experience effects are orders below behavioral thresholds.',
          ['s3'], ['A small modeled causal modulation exists.'],
          ['Persistence, disengagement or voluntary abstention was demonstrated.'])
    claim('modulation.oa-vpm4', FACT, 'constrained', 'Sayin VPM4 activation / MBON11 assay',
          'VPM4 activation suppresses MBON11 response in the tested preparation; exact receptor/dose/kinetics and every root-pair effect are unresolved.',
          ['E13', 'crosswalk'], ['VPM4 suppressive influence is supported in this assay.'],
          ['Octopamine is universally inhibitory.', 'oa_gain=1 is a measured strength.'])
    claim('modulation.peptide-no', FACT, 'constrained', 'dNPF/NO/endocrine experiments',
          'Peptide, NO and endocrine mechanisms matter; their release/receptor maps and kinetics are not encoded by chemical contact counts.',
          ['E15', 'E17', 'E20'], ['These omitted physiological mechanisms remain unresolved.'],
          ['No chemical edge means no peptide or volume transmission.'])
    claim('sign.mbon07-pam11', HYP, 'unresolved', 'MBON07 to PAM11 effective net transmission',
          'Anatomy and NMDA requirement motivate feedback, but do not identify direct net excitation or its strength.',
          ['E10', 'E16', 'parameters'], ['The positive-sign implementation is a historical model assumption.'],
          ['Direct excitatory sign is experimentally established.'])
    claim('normalization.contact-mass', ENG, 'unconstrained', 'all frozen stage normalization operators',
          'Retained-role and total-proofread-input denominators are alternative numerical choices. Biological normalization does not identify either.',
          ['parameters', 'boundary', 'E06'], ['Normalization uncertainty can exceed anatomical expansion effects.'],
          ['The denominator with the strongest behavior is biologically correct.'])
    claim('integration.shared-rules', HYP, 'unresolved', 'shared KC to MBON07/11 rows',
          'Canonical anatomy is shared; dopamine projection, normalization, acute gates, gains and plasticity rules conflict.',
          ['conflicts', 'unified-physiology', 'identity-audit'], ['Identity deduplication does not reconcile physiology.'],
          ['Adding stage scores creates an integrated biological brain.'])
    claim('architecture.selection', ENG, 'insufficient_evidence', 'neural architecture recommendation',
          'Boundary closure and representation studies do not select a defensible common neural substrate.',
          ['boundary', 'representation'], ['Architecture selection remains unresolved.'],
          ['Larger neuron count establishes richer behavior.'])
    claim('benchmark.scope', ENG, 'constrained', 'engineering scaling only',
          'Scalar/local-state benchmark recurrences measure implementation costs, not a calibrated physiological model.',
          ['scaling'], ['Reported throughput applies only to the documented benchmark equations.'],
          ['Generic near-real-time performance guarantees calibrated full-brain performance.'])
    claim('data.license-unresolved', ENG, 'unresolved', 'research data reuse and redistribution',
          'Frozen audits record CC-BY Zenodo metadata versus CC-BY-NC FlyWire guidance and unresolved annotation terms; this specification does not resolve that conflict.',
          ['s1', 's3'], ['The evidence registry is local research infrastructure; upstream data reuse terms require clarification.'],
          ['All upstream data are cleared for unrestricted commercial redistribution.'])
    claim('product.resource-runway', PRODUCT, 'not_authorized', 'possible future digital embodiment only',
          'A future financial-runway/resource analogy is a product interpretation, absent from the biological experiments.',
          ['s3'], ['Any future money/resource mapping must be declared separately.'],
          ['The fly connectome contains wallet, profit or business-value neurons.'])

    cross = load(sources['crosswalk']['path'])
    neurons = {}
    memberships = collections.defaultdict(set)
    stage_counts = {}
    for stage, (path, sha) in enumerate(cross['circuit_hashes'].items(), 1):
        # Source paths, rather than mapping order, are authoritative.
        stage = int(re.search(r'fly-stage(\d)', path).group(1))
        source(f'circuit-s{stage}', path, 'anatomical_extraction')
        circuit = load(path)
        stage_counts[f's{stage}'] = {'neurons': len(circuit['nodes']),
                                   'neuropil_rows': len(circuit['edges']),
                                   'contacts': sum(e['synapses'] for e in circuit['edges']),
                                   'directed_pairs': len({(e['source'], e['target']) for e in circuit['edges']})}
        for node in circuit['nodes']:
            root = node['root_id']
            assert isinstance(root, str) and root.isdecimal()
            rec = neurons.setdefault(root, {'id': f'{DATASET}:{root}', 'root_id': root,
                                            'annotation_observations': [], 'physiology_assignment': None})
            rec['annotation_observations'].append({'stage': stage, 'evidence_ref': f'circuit-s{stage}',
                                                  **{k: v for k, v in node.items() if k != 'root_id'}})
            memberships[f's{stage}.{node["role"]}'].add(root)
        for name, ids in circuit['groups'].items():
            memberships[f's{stage}.{name}'].update(ids)

    # Semantic facets point to atomic claims. No facet inherits a claim's category implicitly.
    profiles = {
        'PN': ('transmission.pn-kc', 'transmission.pn-kc'),
        'KC': ('transmission.pn-kc', 'transmission.kc-mbon'),
        'APL': ('representation.apl-local', 'transmission.apl-kc'),
        'DAN': ('modulation.da-locality', 'modulation.da-locality'),
        'DAN_app': ('modulation.da-locality', 'plasticity.appetitive-model'),
        'DAN_av': ('modulation.da-locality', 'plasticity.gamma1'),
        'MBON_app': ('plasticity.appetitive-model', 'sign.mbon07-pam11'),
        'MBON_av': ('plasticity.gamma1', 'modulation.resource-biological'),
        'MBON': ('plasticity.alpha-prime3', 'plasticity.familiarity-model'),
        'MB11': ('plasticity.gamma1', 'modulation.resource-model'),
        'MB18': ('modulation.resource-biological', 'modulation.resource-model'),
        'OA': ('modulation.oa-vpm4', 'modulation.oa-vpm4'),
        'VALUE': ('plasticity.appetitive-model', 'integration.shared-rules'),
    }
    facets = ['anatomical_evidence', 'transmitter_evidence', 'postsynaptic_receptor_evidence',
              'representation_requirement', 'local_versus_global_state', 'temporal_constraints',
              'normalization_evidence', 'plasticity_evidence', 'parameter_evidence',
              'observation_model', 'source_preparation_compatibility', 'validated_interventions']

    def ref(*ids):
        return {'state': 'scoped_evidence', 'claim_refs': list(ids)}

    populations = []
    for group, roots in sorted(memberships.items()):
        stage, role = group.split('.', 1)
        related = profiles.get(role, ('crosswalk.type', 'architecture.selection'))
        f = {name: unknown() for name in facets}
        f.update(anatomical_evidence=ref('anatomy.pinned', 'crosswalk.type'),
                 transmitter_evidence={'state': 'annotation_only', 'source': 'neurons.json annotation_observations; known_nt and top_nt remain distinct'},
                 representation_requirement=ref(related[0], 'representation.heterogeneous'),
                 local_versus_global_state=ref('representation.heterogeneous'),
                 normalization_evidence=ref('normalization.contact-mass'),
                 parameter_evidence={'state': 'historical_model_only', 'stage': stage},
                 source_preparation_compatibility=ref('crosswalk.type'),
                 observation_model={'state': 'unidentified_transfer', 'value': None,
                                    'reason': 'Frozen model rates have no identified voltage/spike/calcium conversion.'})
        if role == 'APL':
            f['local_versus_global_state'] = ref('representation.apl-local', 'representation.apl-coupling')
        populations.append({'id': 'population.' + group, 'kind': 'population',
                            'category': FACT, 'layer': 'biological', 'status': 'anatomically_pinned',
                            'root_ids': sorted(roots), 'identity_scope': 'extraction role, not an independent cell-type identity',
                            'fine_compartment': unknown('Neuropil/annotation does not resolve every contact to a functional compartment.'),
                            'sign': unknown('Transmitter annotation alone does not identify a target-specific effective sign.'),
                            'facets': f, 'related_claims': list(related),
                            'evidence_refs': [f'circuit-{stage}', 'crosswalk'],
                            'known_conflicts': ['integration.shared-rules'] if stage in ('s1', 's3') else [],
                            'unsupported_extrapolations': ['Individual physiological equivalence to experimental drivers.', 'Global scalar sufficiency inferred from missing measurements.'],
                            'allowed_scientific_wording': ['These roots belong to the pinned extraction role.'],
                            'prohibited_scientific_wording': ['All members have measured identical receptor/sign/kinetic properties.']})

    def roots_for(type_or_role):
        return {root for root, n in neurons.items() if any(
            a.get('cell_type') == type_or_role or a.get('role') == type_or_role
            for a in n['annotation_observations'])}

    connections = []
    definitions = [
        ('PN', 'KC', 'transmission.pn-kc'), ('KC', 'APL', 'transmission.apl-kc'),
        ('APL', 'KC', 'transmission.apl-kc'), ('KC', 'MBON07', 'plasticity.appetitive-model'),
        ('KC', 'MBON11', 'plasticity.gamma1'), ('KC', 'MBON16', 'plasticity.alpha-prime3'),
        ('KC', 'MBON17', 'plasticity.alpha-prime3'), ('KC', 'MBON18', 'modulation.resource-biological'),
        ('MBON07', 'PAM11', 'sign.mbon07-pam11'), ('PAM11', 'KC', 'modulation.da-locality'),
        ('PPL101', 'KC', 'modulation.da-locality'), ('PPL101', 'MBON11', 'modulation.resource-biological'),
        ('PPL104', 'MBON16', 'modulation.da-locality'), ('PPL104', 'MBON17', 'modulation.da-locality'),
        ('OA', 'MBON11', 'modulation.oa-vpm4'), ('MBON11', 'MBON18', 'modulation.resource-biological'),
        ('MBON11', 'LH', 'modulation.resource-model'), ('MBON18', 'LH', 'modulation.resource-model'),
        ('LH', 'LHCENT', 'architecture.selection'),
    ]
    selectors = [(roots_for(pre), roots_for(post)) for pre, post, _ in definitions]
    counts = [{'aggregate_rows': 0, 'contacts': 0, 'pairs': set()} for _ in definitions]
    with gzip.open(ROOT / sources['identity']['path'], 'rt') as f:
        for line in f:
            row = json.loads(line)
            pre, post = row['pre'].rsplit(':', 1)[1], row['post'].rsplit(':', 1)[1]
            for i, (a, b) in enumerate(selectors):
                if pre in a and post in b:
                    counts[i]['aggregate_rows'] += 1
                    counts[i]['contacts'] += row['anatomical_contacts']
                    counts[i]['pairs'].add((pre, post))
    for (pre, post, cid), selectors_i, count in zip(definitions, selectors, counts):
        count['directed_pairs'] = len(count.pop('pairs'))
        connections.append({'id': f'connection.{pre}.{post}', 'kind': 'connection_class',
                            'category': FACT, 'layer': 'biological', 'status': 'anatomically_pinned',
                            'pre_root_ids': sorted(selectors_i[0]), 'post_root_ids': sorted(selectors_i[1]),
                            'canonical_owner': 'anatomy', 'view_only': True,
                            'canonical_registry_ref': 'identity', 'counts': count,
                            'sign': unknown('Net target-specific physiological sign is not assigned from type/contact alone.'),
                            'physiology_rule': unknown('No common operator assigned; related claims retain their preparation scope.'),
                            'facets': {**{name: unknown() for name in facets},
                                       'anatomical_evidence': ref('anatomy.pinned'),
                                       'normalization_evidence': ref('normalization.contact-mass'),
                                       'source_preparation_compatibility': ref('crosswalk.type')},
                            'related_claims': [cid], 'evidence_refs': ['identity', 'identity-audit'],
                            'known_conflicts': ['integration.shared-rules'] if post in ('MBON07', 'MBON11') else [],
                            'unsupported_extrapolations': ['Anatomical contacts identify receptor occupancy or efficacy.'],
                            'allowed_scientific_wording': ['Anatomical rows are retained once; physiological assignments remain scoped or unknown.'],
                            'prohibited_scientific_wording': ['This connection class is a validated behavioral pathway.']})

    parameters = []
    for index, p in enumerate(load(sources['parameters']['path'])):
        parameters.append({'id': f'parameter.{index:02d}.{p["name"]}', 'kind': 'parameter',
                           'category': ENG, 'layer': 'biological', 'status': p['status'],
                           'historical_record': p, 'evidence_refs': ['parameters', *p['evidence']],
                           'physiological_value': unknown(),
                           'model_value': {'state': 'declared_model_boundary' if p['value'] == 0 else 'historical_assumption',
                                           'value': p['value'], 'not_a_physiological_estimate': True},
                           'constraint_scope': p['note'],
                           'allowed_scientific_wording': ['Frozen implementation value; constraint status applies only to the stated scope.'],
                           'prohibited_scientific_wording': ['The historical numerical value is biologically calibrated.']})

    cap_defs = [
        ('associative_appetitive_learning', 'validated_narrow_model', 'plasticity.appetitive-model', 'Frozen Stage-1 computational protocol only.'),
        ('familiarity_novelty', 'candidate_behavior_unsupported', 'plasticity.familiarity-model', 'Tiny persistent effect; not behavioral novelty.'),
        ('resource_state_modulation', 'modeled_causal_effect_behavior_unsupported', 'modulation.resource-model', 'Selective small model effect; no persistence/withdrawal.'),
        ('persistence', 'unsupported', 'modulation.resource-model', 'Prerequisite thresholds not met.'),
        ('withdrawal_disengagement', 'unsupported', 'modulation.resource-model', 'Not established by Stage 3.'),
        ('voluntary_abstention', 'unsupported', 'modulation.resource-model', 'Zero activity is not a voluntary decision.'),
        ('general_curiosity', 'unsupported', 'plasticity.familiarity-model', 'Familiarity is not semantic curiosity.'),
        ('threat_behavior', 'not_tested', 'architecture.selection', 'No threat behavior experiment; Stage-1 aversive counterpart is not one.'),
        ('sleep', 'not_tested', 'architecture.selection', 'No sleep experiment.'),
        ('arousal', 'not_tested', 'architecture.selection', 'No arousal experiment.'),
        ('consciousness_sentience', 'unsupported_outside_evidence', 'architecture.selection', 'Outside current evidence and validation scope.'),
    ]
    capabilities = [{'id': 'capability.' + key, 'kind': 'capability', 'category': ENG,
                     'layer': 'biological', 'status': status, 'claim_refs': [cid], 'scope': scope,
                     'evidence_refs': ['s1', 's2', 's3', 'boundary', 'representation'],
                     'allowed_scientific_wording': [scope],
                     'prohibited_scientific_wording': ['Genesis has this validated biological capability.']}
                    for key, status, cid, scope in cap_defs]

    # These are transcriptions of frozen results, never recalculated neural outcomes.
    experiments = [
        {'id': 'experiment.s1', 'kind': 'experiment_result', 'category': ENG, 'layer': 'biological',
         'status': 'validated_scoped', 'scope': 'frozen computational appetitive assay', 'evidence_refs': ['s1'],
         'metrics': {'mean_paired_depression_percent': 51.12, 'mean_control_depression_percent': 8.88,
                     'mean_selectivity_percentage_points': 42.25,
                     'selectivity_range_percentage_points': [34.98, 49.95],
                     'primary_conditions': 6, 'exact_full_replays': 6,
                     'fast_reset_difference_upper_bound': 1e-10, 'exact_snapshot_restores': 76},
         'interventions': {'intact_selectivity_pp_AB': [49.95, 37.67],
                            'plasticity_frozen_pp_AB': [0, 0], 'PAM11_silenced_pp_AB': [0, 0],
                            'DAN_KC_contacts_removed_pp_AB': [0, 0], 'unpaired_teaching_pp_AB': [0, 0],
                            'one_relevant_DAN_lesion_pp_AB': [44.57, 34.50],
                            'one_unrelated_DAN_lesion_pp_AB': [49.95, 37.67],
                            'PN_KC_strength_shuffle_pp_AB': [47.88, 42.13]},
         'limitations': ['Measured zero control effects are not unknown physiological signs.',
                        'Matched-size control is one neuron, not a match to the full 13-PAM ablation.',
                        'Learning survives strength shuffling; exact topology is not uniquely necessary.']},
        {'id': 'experiment.s2', 'kind': 'experiment_result', 'category': ENG, 'layer': 'biological',
         'status': 'partial_inconclusive', 'scope': 'frozen computational familiarity assay', 'evidence_refs': ['s2'],
         'metrics': {'repeated_suppression_percent_range': [0.001376, 0.004555],
                     'specificity_pp_range': [0.001376, 0.004266],
                     'preregistered_suppression_percent': 5, 'preregistered_specificity_pp': 3},
         'interventions': {'scope': 'Local plasticity/DA interventions and reset/restore support a tiny neural-state effect, not familiarity behavior.',
                            'quantitative_results_ref': 's2'},
         'limitations': ['Magnitude fails acceptance.', 'APL/PPL104 boundaries and exposure/recovery assumptions remain material.']},
        {'id': 'experiment.s3', 'kind': 'experiment_result', 'category': ENG, 'layer': 'biological',
         'status': 'partial_inconclusive', 'scope': 'frozen synthetic-resource assay', 'evidence_refs': ['s3'],
         'metrics': {'MB11_state_contrast_percent_range': [0.04958433, 0.118655429],
                     'MB11_experience_percent_range': [0.0238223752, 0.0605364741],
                     'state_threshold_percent': 10, 'experience_threshold_percent': 5,
                     'learned_value_resource_interaction_percent_AB': [1.73922241e-6, 2.2724623e-6],
                     'OA_MB11_suppression_percent_range': [5.50854579, 6.28803642],
                     'fast_reset_max_difference': 6.93889e-18, 'exact_primary_replays': 12,
                     'exact_fresh_recalls': 36},
         'interventions': {'PPL101_silencing_modulation_reduction_percent': 100,
                            'local_DA_gate_removal_reduction_percent': 100,
                            'frozen_modulation_reduction_percent': 100,
                            'OA_silenced_MB11_suppression_percent': 0,
                            'matched_and_connectivity_results_ref': 's3'},
         'limitations': ['OA suppresses MB11 but slightly increases MB18/LH: not disengagement.',
                        'Cue-following and decay do not establish pursuit or abstention.']},
        {'id': 'experiment.apl', 'kind': 'experiment_result', 'category': APPROX, 'layer': 'biological',
         'status': 'validated_scoped', 'scope': 'spatial fluorescence prediction only',
         'evidence_refs': ['apl-fit', 'apl-validation', 'representation'],
         'metrics': {'figure4_heldout_MSE': {'R0': 5.796135, 'R1_zero': 0.007750565,
                                            'R1_shared': 0.00831429, 'R1_directional': 0.00701383},
                     'figure3_heldout_MSE': {'R0': 1.444396, 'R1_zero': 0.040157, 'R1_shared': 0.036414},
                     'shared_q_interval': [0, 0.0309142], 'material_improvement_criterion_percent': 20},
         'limitations': ['Rounded frozen report values, not newly fitted results.',
                        'Shared/directional transfer does not clear the 20% improvement criterion over zero coupling.',
                        'Spatial calcium prediction does not identify APL to KC conductance or a universal zero coupling.']},
    ]

    studies = [
        ('s1', 'PASS', 'Narrow appetitive associative learning; aversive counterpart inconclusive.'),
        ('s2', 'PARTIAL-INCONCLUSIVE', 'Tiny, assumption-sensitive stimulus-specific effect.'),
        ('s3', 'PARTIAL-INCONCLUSIVE', 'Small selective modulation; no persistence/disengagement/abstention.'),
        ('boundary', 'INSUFFICIENT EVIDENCE', 'No architecture selection.'),
        ('physiology', 'PARTIAL PHYSIOLOGICAL CONSTRAINT', 'No transferable common numerical kernel.'),
        ('representation', 'INSUFFICIENT EVIDENCE TO SELECT REPRESENTATION', 'Local APL support does not select a common representation.'),
    ]
    registry = {
        'schema_version': '1', 'version': VERSION,
        'title': 'Project Genesis Biological Neural Specification v0.1',
        'purpose': 'Synthesis and evidence infrastructure only; no neural implementation or integration.',
        'categories': [FACT, APPROX, HYP, ENG, PRODUCT],
        'sources': sources, 'literature': literature,
        'studies': [{'id': key, 'classification': cls, 'scope': scope, 'evidence_ref': key}
                    for key, cls, scope in studies],
        'dataset': {k: cross[k] for k in ('dataset', 'annotations', 'annotation_sha256')},
        'identity': {'neuron_key': 'FAFB-FlyWire:783:<decimal root string>',
                     'canonical_registry_ref': 'identity', 'canonical_owner': 'anatomy',
                     'aggregate_row_key': 'sha256(compact JSON [dataset, pinned contact-source hash, pre neuron key, post neuron key, neuropil])',
                     'contact_level_ids': unknown('Not provided by the proofread aggregate source; never manufacture contact IDs.'),
                     'audit': load(sources['identity-audit']['path']),
                     'shared_rows_ref': 'shared-rows', 'physiology_composition': 'blocked_unresolved_rules',
                     'alternative_snapshots': 'May share canonical anatomy, never simultaneous independent ownership in one model.'},
        'stage_anatomy': stage_counts,
        'entries': entries + populations + connections + parameters + capabilities + experiments,
        'stage4_contract': {
            'authorized_now': False,
            'may_assume': ['anatomy.pinned', 'crosswalk.type', 'plasticity.appetitive-model',
                           'representation.apl-local', 'modulation.da-locality'],
            'must_not_assume': ['Common numerical kernel', 'Known nonzero APL coupling',
                                'Validated familiarity/persistence/abstention', 'Shared rules reconciled',
                                'Contact count determines receptor sign', 'Engineering benchmark validates physiology'],
            'must_establish': ['New capability definition, independently justified population/root crosswalk and preparation limits',
                               'Independent observation model and physiological parameter evidence or explicit unknowns',
                               'Preregistered thresholds, held-out tests, causal interventions and boundary/normalization controls',
                               'Persistent neural state versus adaptation/readout/software memory where learning is claimed',
                               'Single ownership and independently supported operator before composing shared connections',
                               'Exact pinned evidence dependencies; explicit reviewed supersession for any changed claim'],
        },
        'validation_limits': 'Hashes enforce identity/provenance and structured policy, not truth of arbitrary prose or authenticity of a human review. Independent scientific review remains required.',
    }
    neuron_data = canonical({'dataset': DATASET, 'neurons': [neurons[k] for k in sorted(neurons)]}) + b'\n'
    neuron_sha = hashlib.sha256(neuron_data).hexdigest()
    immutable(HERE / 'objects' / (neuron_sha + '.json'), neuron_data)
    registry['neurons_artifact'] = {'path': f'objects/{neuron_sha}.json', 'sha256': neuron_sha, 'count': len(neurons)}
    registry['entry_hashes'] = {e['id']: digest(e) for e in registry['entries']}
    encoded = canonical(registry) + b'\n'
    sha = hashlib.sha256(encoded).hexdigest()
    immutable(HERE / 'objects' / (sha + '.json'), encoded)
    release = {'version': VERSION, 'registry': {'path': f'objects/{sha}.json', 'sha256': sha},
               'protected_inputs_sha256': file_hash(HERE / 'FROZEN_INPUTS.json')}
    immutable(HERE / 'RELEASE.json', json.dumps(release, indent=2, sort_keys=True).encode() + b'\n')
    print(json.dumps({'registry_sha256': sha, 'entries': len(registry['entries']),
                      'neurons': len(neurons), 'populations': len(populations), 'connection_classes': len(connections),
                      'parameters': len(parameters)}))


if __name__ == '__main__':
    build()

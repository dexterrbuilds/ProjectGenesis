"""Additive final policy checks; original release and validator remain byte-for-byte frozen."""
import re
from build import HERE, ROOT, digest, file_hash, FACT, APPROX, HYP, ENG, PRODUCT
from validate import (require, strict_load, entries_by_id, validate_structure,
                      validate_revision, validate_experiment, local_path)

RELEASE_SHA256 = '6b3a27ea3c41a87e701ca8a7eec7fd31d5e41469db7da27916b81cb040eb923e'
CAPABILITIES = {
    'associative_appetitive_learning': 'validated_narrow_model',
    'familiarity_novelty': 'candidate_behavior_unsupported',
    'resource_state_modulation': 'modeled_causal_effect_behavior_unsupported',
    'persistence': 'unsupported', 'withdrawal_disengagement': 'unsupported',
    'voluntary_abstention': 'unsupported', 'general_curiosity': 'unsupported',
    'threat_behavior': 'not_tested', 'sleep': 'not_tested', 'arousal': 'not_tested',
    'consciousness_sentience': 'unsupported_outside_evidence',
}
STUDIES = {
    's1': 'PASS', 's2': 'PARTIAL-INCONCLUSIVE', 's3': 'PARTIAL-INCONCLUSIVE',
    'boundary': 'INSUFFICIENT EVIDENCE', 'physiology': 'PARTIAL PHYSIOLOGICAL CONSTRAINT',
    'representation': 'INSUFFICIENT EVIDENCE TO SELECT REPRESENTATION',
}


def check_profiles(registry):
    pointer = strict_load(HERE / 'MECHANISM_PROFILES.json')
    path = local_path(HERE, pointer['path'])
    require(path.stem == pointer['sha256'] and file_hash(path) == pointer['sha256'], 'Mechanism profile content address changed')
    profiles = strict_load(path)
    require(profiles['registry_sha256'] == RELEASE_SHA256, 'Mechanism profiles reference a different release')
    entries = entries_by_id(registry)
    ids = set()
    required = {'identity_resolution', 'anatomical_evidence', 'transmitter_and_experimental_effect',
                'postsynaptic_root_receptor_map', 'root_specific_sign_confidence', 'representation_requirement',
                'local_versus_global_state', 'temporal_constraints', 'normalization_evidence',
                'plasticity_evidence', 'parameter_evidence', 'observation_model',
                'source_preparation_compatibility', 'validated_interventions', 'known_conflicts',
                'unsupported_extrapolations', 'allowed_scientific_wording', 'prohibited_scientific_wording'}
    from validate import inspect_fields
    for profile in profiles['profiles']:
        require(profile['id'] not in ids, 'Duplicate mechanism profile')
        ids.add(profile['id'])
        require(required <= set(profile), 'Missing mechanism evidence facet')
        for cid, sha in profile['dependencies'].items():
            require(cid in entries and digest(entries[cid]) == sha, 'Unpinned mechanism dependency')
        for cid in profile['canonical_connection_views']:
            require(cid in profile['dependencies'] and entries[cid]['kind'] == 'connection_class', 'Invalid anatomy reference')
        require(profile['anatomical_evidence']['ownership'] == 'reference_only', 'Second anatomy owner in mechanism profile')
        require(profile['postsynaptic_root_receptor_map']['state'] == 'unknown', 'Profile invents a receptor map')
        require(profile['plasticity_evidence']['common_operator']['state'] == 'unknown', 'Profile reconciles unsupported rules')
        inspect_fields(profile, registry)
    require(len(ids) == 11, 'Mechanism profile count changed')
    return profiles


def check_frozen_policy(registry):
    """Also exercises scientific status invariants when a mutation fixture is rehashed."""
    entries = validate_structure(registry)
    require({s['id']: s['classification'] for s in registry['studies']} == STUDIES,
            'Frozen study classification changed')
    caps = {e['id'].removeprefix('capability.'): e['status']
            for e in registry['entries'] if e['kind'] == 'capability'}
    require(caps == CAPABILITIES, 'Unsupported capability promotion')
    for e in registry['entries']:
        if e['category'] in (HYP, PRODUCT):
            require(not e['status'].startswith('validated'), 'Hypothesis/product pathway cannot be validated by relabeling')
        if e['status'].startswith('validated'):
            require(bool(e.get('evidence_refs')), 'Validation claim lacks provenance')
    # Pin all fields, not only classification. The release itself is the trust anchor.
    baseline = strict_load(HERE / 'objects' / (RELEASE_SHA256 + '.json'))
    require(file_hash(HERE / 'objects' / (RELEASE_SHA256 + '.json')) == RELEASE_SHA256,
            'Trusted release object changed')
    require(registry == baseline, 'Frozen evidence changed; use an append-only reviewed revision')
    return entries


def check_experiment(manifest, release, registry):
    check_frozen_policy(registry)
    require(release['registry']['sha256'] == RELEASE_SHA256, 'Wrong evidence release')
    ownership = [(s.get('row_id'), s.get('model_instance'), s.get('state_kind'))
                 for s in manifest.get('state_ownership', [])]
    require(len(set(ownership)) == len(ownership), 'Duplicate canonical synapses receive independent state ownership')
    validate_experiment(manifest, release, registry)
    entries = entries_by_id(registry)
    units = {'dimensionless', 's', 'mV', 'pA', 'Hz', 'delta_F_over_F', 'model_current'}
    for channel in manifest['input_channels']:
        require(channel['units'] in units, 'Unreviewed/product unit in biological input')
        if channel['kind'] != 'measurement':
            require(channel['category'] == ENG, 'Synthetic stimulation/body input cannot be relabeled biological fact')
        for cid in channel['evidence_refs']:
            require(entries[cid]['layer'] == 'biological', 'Product evidence used as biological input')
    for cid in manifest['uses']:
        require(entries[cid]['layer'] == 'biological', 'Product mapping imported into neural experiment')
    for a in manifest['proposed_assumptions']:
        require(bool(a['depends_on']), 'Proposed assumptions must pin prior evidence')
        require(all(entries[cid]['layer'] == 'biological' for cid in a['depends_on']),
                'Product mapping used to justify biological assumption')
    for state in manifest['local_states']:
        require(bool(state['partition']) and bool(state['id']), 'Empty local-state identity')
        require(all(entries[cid]['layer'] == 'biological' for cid in state['evidence_refs']),
                'Product mapping used to justify local neuron state')


def check_revision(base, candidate, approvals):
    check_frozen_policy(base)
    require(set(candidate) == set(base), 'Unreviewed top-level revision fields')
    # Changes to future policy require a separately reviewed schema release, not claim admission.
    for key in ('schema_version', 'purpose', 'categories', 'stage4_contract', 'validation_limits'):
        require(candidate[key] == base[key], 'Claim revision cannot change governance or authorize experiments')
    validate_revision(base, candidate, approvals)
    old = entries_by_id(base)
    new = entries_by_id(candidate)
    for cid in set(new) - set(old):
        e = new[cid]
        require(e['kind'] == 'claim', 'New capability/identity/operator schemas require separate review; admit scoped claims first')
        require(set(e) == set(old['modulation.da-locality']), 'Unreviewed claim fields')
        require(e['category'] != PRODUCT, 'Product mappings cannot be admitted as physiological evidence')
        for s in e['supersedes']:
            require(old[s['id']]['layer'] == e['layer'], 'Product-to-biology supersession prohibited')
        if e['category'] == HYP:
            require(not e['status'].startswith('validated'), 'Unsupported pathway promoted while still a hypothesis')
    new_sources = set(candidate['sources']) - set(base['sources'])
    admitted = {ref for a in approvals for ref in a['independent_evidence_refs']}
    require(new_sources == admitted, 'Unreviewed evidence source insertion')
    old_hashes = {s['sha256'] for s in base['sources'].values()}
    for ref in admitted:
        source = candidate['sources'][ref]
        require(source['sha256'] not in old_hashes, 'Renaming an old source is not new superseding evidence')
        require(set(source) == {'path', 'sha256', 'kind', 'section'}, 'New source needs pinned provenance')
    for a in approvals:
        require(re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', a['reviewed_at']) is not None,
                'Review needs an explicit UTC timestamp')

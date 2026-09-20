"""Fail-closed registry, revision, and future research-manifest validation.

This validates structured contracts, hashes and explicit review, not truth of prose.
No neural models, Genesis modules, database clients or optimizers are imported.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
from build import HERE, ROOT, canonical, digest, file_hash, FACT, APPROX, HYP, ENG, PRODUCT


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def local_path(base, rel):
    require(isinstance(rel, str), 'Path must be a string')
    p = (base / rel).resolve()
    require(p.is_relative_to(base.resolve()), 'Path escapes its allowed root')
    return p


def strict_load(path):
    def pairs(items):
        d = {}
        for k, v in items:
            require(k not in d, f'Duplicate JSON key: {k}')
            d[k] = v
        return d
    return json.loads(path.read_text(), object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(Invalid('Nonfinite JSON: ' + x)))


def entries_by_id(registry):
    result = {}
    for entry in registry['entries']:
        require(entry['id'] not in result, 'Duplicate evidence ID')
        result[entry['id']] = entry
    return result


def evidence_known(ref, registry):
    return ref in registry['sources'] or ref in registry['literature']


def inspect_fields(obj, registry):
    if isinstance(obj, list):
        for v in obj:
            inspect_fields(v, registry)
    elif isinstance(obj, dict):
        if obj.get('state') == 'unknown':
            require('value' in obj and obj['value'] is None, 'Unknown must remain explicit null, never zero')
            require(bool(obj.get('reason')), 'Unknown needs its scope/reason')
        for ref in obj.get('evidence_refs', []):
            require(evidence_known(ref, registry), f'Unknown provenance: {ref}')
        if 'sign' in obj:
            sign = obj['sign']
            require(isinstance(sign, dict), 'Sign must be an explicit evidence quantity')
            require(sign.get('state') in ('unknown', 'experimentally_constrained'), 'Invalid sign status')
            if sign['state'] != 'unknown':
                require(sign.get('value') in ('positive', 'negative', 'mixed'), 'Invalid physiological sign')
                require(bool(sign.get('evidence_refs')) and bool(sign.get('scope')),
                        'A known physiological sign requires provenance and target/preparation scope')
        for v in obj.values():
            inspect_fields(v, registry)


def validate_structure(registry):
    require(registry['schema_version'] == '1', 'Unsupported schema')
    require(registry['categories'] == [FACT, APPROX, HYP, ENG, PRODUCT], 'Category vocabulary changed')
    entries = entries_by_id(registry)
    require(set(registry['entry_hashes']) == set(entries), 'Entry index mismatch')
    for cid, entry in entries.items():
        require(digest(entry) == registry['entry_hashes'][cid], 'Entry hash mismatch: ' + cid)
        require(entry['category'] in registry['categories'], 'Unrecognized evidence category')
        require(entry['layer'] in ('biological', 'product'), 'Unknown evidence layer')
        require((entry['category'] == PRODUCT) == (entry['layer'] == 'product'), 'Product category/layer separation violated')
        # A product namespace cannot be relabeled biological by changing the category.
        require(not cid.startswith('product.') or entry['layer'] == 'product', 'Product namespace in biological layer')
        require(entry['kind'] in ('claim', 'population', 'connection_class', 'parameter', 'capability', 'experiment_result'),
                'Unknown entry kind')
        inspect_fields(entry, registry)
        for ref in entry.get('claim_refs', []) + entry.get('related_claims', []):
            require(ref in entries, 'Dangling claim reference')
        for facet in entry.get('facets', {}).values():
            for ref in facet.get('claim_refs', []):
                require(ref in entries, 'Dangling facet claim')
        if entry['kind'] in ('population', 'connection_class'):
            require(entry['status'] == 'anatomically_pinned', 'Anatomical membership cannot validate a physiological pathway')
        if entry['kind'] == 'connection_class':
            require(entry['view_only'] is True and entry['canonical_owner'] == 'anatomy', 'Duplicate anatomical ownership')
            require(entry['canonical_registry_ref'] == 'identity', 'Independent canonical connection store prohibited')
        if entry['kind'] == 'parameter':
            require(entry['physiological_value']['state'] == 'unknown', 'Historical parameter promoted to physiological value')
            require(entry['model_value']['not_a_physiological_estimate'] is True, 'Historical parameter laundering')
        for key in ('root_ids', 'pre_root_ids', 'post_root_ids'):
            if key in entry:
                ids = entry[key]
                require(len(ids) == len(set(ids)), 'Duplicate root membership')
                require(all(isinstance(x, str) and re.fullmatch(r'\d+', x) for x in ids), 'Roots must be decimal strings')
    for ref in registry['stage4_contract']['may_assume']:
        require(ref in entries, 'Stage4 assumption must reference scoped frozen evidence')
    require(registry['stage4_contract']['authorized_now'] is False, 'This release cannot authorize Stage4')
    return entries


def validate_identity(registry, verify_rows=True):
    artifact = registry['neurons_artifact']
    p = local_path(HERE, artifact['path'])
    require(file_hash(p) == artifact['sha256'], 'Neuron artifact changed')
    neurons = strict_load(p)['neurons']
    roots = {n['root_id'] for n in neurons}
    require(len(roots) == len(neurons) == artifact['count'] == 5480, 'Canonical neuron ownership/count mismatch')
    for n in neurons:
        require(isinstance(n['root_id'], str) and n['root_id'].isdecimal(), 'Non-string root')
        require(n['id'] == 'FAFB-FlyWire:783:' + n['root_id'], 'Invalid neuron key')
        require(n['physiology_assignment'] is None, 'Physiology silently assigned during synthesis')
    for e in registry['entries']:
        for key in ('root_ids', 'pre_root_ids', 'post_root_ids'):
            require(set(e.get(key, [])) <= roots, 'Unknown root in anatomical view')
    if not verify_rows:
        return set()
    identity = registry['sources']['identity']
    shared = strict_load(ROOT / registry['sources']['shared-rows']['path'])
    require({k: len(v) for k, v in shared.items()} == {'KC_MBON07': 4622, 'KC_MBON11': 1053}, 'Shared-row counts changed')
    rows, contacts, all_roots = set(), 0, set()
    with gzip.open(ROOT / identity['path'], 'rt') as f:
        for line in f:
            r = json.loads(line)
            require(r['id'] not in rows, 'Duplicate canonical anatomical row')
            expected = hashlib.sha256(json.dumps([
                'FAFB-FlyWire:783', registry['identity']['audit']['source_sha256'],
                r['pre'], r['post'], r['neuropil']], separators=(',', ':')).encode()).hexdigest()
            require(r['id'] == expected, 'Canonical row identity mismatch')
            require(r['physiology_rule'] is None and r['functional_compartment'] is None,
                    'Canonical anatomy silently assigned physiological ownership')
            rows.add(r['id'])
            all_roots.update([r['pre'].rsplit(':', 1)[1], r['post'].rsplit(':', 1)[1]])
            contacts += r['anatomical_contacts']
    require(len(rows) == 449600 and contacts == 1056073, 'Canonical row/contact totals changed')
    require(all_roots <= roots, 'Canonical row references unknown neuron')
    for group in shared.values():
        require(len(set(group)) == len(group) and set(group) <= rows, 'Shared canonical rows missing/duplicated')
    return rows


def load_release(verify_files=True, verify_rows=True):
    release = strict_load(HERE / 'RELEASE.json')
    item = release['registry']
    path = local_path(HERE, item['path'])
    require(path.stem == item['sha256'] and file_hash(path) == item['sha256'], 'Release content address changed')
    require(file_hash(HERE / 'FROZEN_INPUTS.json') == release['protected_inputs_sha256'], 'Preservation baseline changed')
    registry = strict_load(path)
    require(registry['version'] == release['version'] == '0.1.0', 'Release version mismatch')
    validate_structure(registry)
    if verify_files:
        for source in registry['sources'].values():
            p = local_path(ROOT, source['path'])
            require(file_hash(p) == source['sha256'], 'Frozen source changed: ' + source['path'])
        for rel, sha in strict_load(HERE / 'FROZEN_INPUTS.json').items():
            require(file_hash(local_path(ROOT, rel)) == sha, 'Protected file changed: ' + rel)
    validate_identity(registry, verify_rows)
    return release, registry


def validate_revision(base, candidate, approvals):
    """Append-only release changes. Explicit independent evidence + separately reviewed record.

    Approval is a human-reviewed artifact, NOT cryptographic attestation. A future
    reviewer must control publication of that file and the new release trust anchor.
    """
    old, new = entries_by_id(base), validate_structure(candidate)
    require(candidate['version'] != base['version'], 'Evidence revision requires a new version')
    for cid, entry in old.items():
        require(new.get(cid) == entry, 'Frozen entry modified or removed; append explicit superseding evidence instead: ' + cid)
    for key in ('studies', 'dataset', 'identity', 'neurons_artifact', 'literature', 'stage_anatomy'):
        require(candidate[key] == base[key], 'Historical source/classification/identity records cannot be rewritten')
    for key, source in base['sources'].items():
        require(candidate['sources'].get(key) == source, 'Frozen source record changed')
    additions = set(new) - set(old)
    approved = {a['entry_id']: a for a in approvals}
    require(len(approved) == len(approvals), 'Duplicate review record')
    require(set(approved) == additions, 'Every added evidence entry requires a separate review record')
    for cid in additions:
        e, review = new[cid], approved[cid]
        require(set(review) == {'entry_id', 'entry_sha256', 'reviewer', 'reviewed_at', 'rationale',
                                'independent_evidence_refs', 'supersedes', 'scope'}, 'Invalid review fields')
        require(review['entry_sha256'] == digest(e), 'Review does not approve this exact entry')
        require(all(isinstance(review[k], str) and review[k].strip() for k in ('reviewer', 'reviewed_at', 'rationale', 'scope')),
                'Review identity, time, rationale and scope required')
        require(review['scope'] == e.get('scope'), 'Review scope mismatch')
        require(review['supersedes'] == e.get('supersedes', []), 'Supersession review mismatch')
        require(bool(review['independent_evidence_refs']), 'New evidence required; an old citation cannot reclassify itself')
        for ref in review['independent_evidence_refs']:
            require(ref not in base['sources'] and ref in candidate['sources'], 'Supersession requires newly admitted evidence')
            src = candidate['sources'][ref]
            require(src['kind'] == 'independent_evidence', 'Not an independent evidence source')
            require(file_hash(local_path(ROOT, src['path'])) == src['sha256'], 'New evidence content changed')
            require(ref in e['evidence_refs'], 'Reviewed evidence must be cited by the new claim')
        for superseded in e.get('supersedes', []):
            require(set(superseded) == {'id', 'sha256', 'reason'}, 'Explicit supersession needs ID, frozen hash and reason')
            require(superseded['id'] in old and superseded['sha256'] == digest(old[superseded['id']]), 'Wrong superseded evidence hash')
            require(bool(superseded['reason']), 'Supersession reason missing')
        # A fresh ID must not silently relabel the same scope as a prior entry.
        scope_matches = {i for i, previous in old.items() if previous.get('scope') == e.get('scope')}
        require(scope_matches <= {s['id'] for s in e.get('supersedes', [])}, 'Same-scope evidence must explicitly supersede previous claims')


def validate_experiment(manifest, release, registry):
    """A future isolated experiment consumes evidence; it cannot rewrite the registry."""
    require(set(manifest) == {'schema_version', 'id', 'registry_sha256', 'dependencies', 'uses',
                              'input_channels', 'anatomy_views', 'state_ownership', 'local_states',
                              'proposed_assumptions', 'result_claims', 'integration'}, 'Unknown/missing experiment fields (overrides forbidden)')
    require(manifest['schema_version'] == '1', 'Unsupported experiment schema')
    require(manifest['registry_sha256'] == release['registry']['sha256'], 'Experiment does not pin this exact release')
    require(manifest['integration'] == 'isolated_research_only', 'No Genesis integration authorized')
    deps = manifest['dependencies']
    require(isinstance(deps, dict) and bool(deps), 'Explicit evidence dependencies required')
    entries = entries_by_id(registry)
    for cid, sha in deps.items():
        require(cid in entries and digest(entries[cid]) == sha, 'Stale/unknown evidence dependency')
    require(set(manifest['uses']) <= set(deps), 'Used evidence omitted from dependencies')
    require(manifest['result_claims'] == [], 'Results cannot promote claims inside an experiment manifest; publish reviewed superseding evidence')
    allowed_channels = {'sensory_pattern', 'presentation_time', 'stimulation_current', 'measurement', 'body_boundary'}
    product_terms = {'money', 'wallet', 'profit', 'business', 'entrepreneurship', 'trading', 'browsing',
                     'novelty', 'seen_count', 'familiar', 'persistence', 'continue', 'give_up', 'worth_it', 'motivation'}
    for channel in manifest['input_channels']:
        require(set(channel) == {'id', 'kind', 'category', 'evidence_refs', 'units'}, 'Unknown input channel fields')
        require(channel['kind'] in allowed_channels and channel['category'] in (ENG, FACT), 'Product/answer input in biological layer')
        tokens = set(re.split(r'[^a-z0-9]+', channel['id'].lower())) | {channel['id'].lower()}
        require(not tokens & product_terms, 'Product concept/hidden answer in biological input')
        require(bool(channel['evidence_refs']) and set(channel['evidence_refs']) <= set(deps), 'Unpinned input assumption')
    for assumption in manifest['proposed_assumptions']:
        require(set(assumption) == {'id', 'category', 'status', 'statement', 'depends_on'}, 'Assumptions cannot introduce unreviewed operators/claims')
        require(assumption['category'] in (HYP, ENG) and assumption['status'] == 'unvalidated', 'Unsupported pathway marked validated')
        require(assumption['id'].startswith('hypothesis.') or assumption['id'].startswith('engineering.'), 'Assumption namespace required')
        require(set(assumption['depends_on']) <= set(deps), 'Unpinned assumption dependency')
        # Also reject common relabeling attempts in declarative prose; not an NLP truth guarantee.
        require(not re.search(r'\b(wallet|profit|business|entrepreneurship|trading)\b', assumption['statement'], re.I),
                'Product concept in biological assumption')
    shared = strict_load(ROOT / registry['sources']['shared-rows']['path'])
    conflicted = set(shared['KC_MBON07']) | set(shared['KC_MBON11'])
    row_ids = set()
    with gzip.open(ROOT / registry['sources']['identity']['path'], 'rt') as f:
        for line in f:
            row_ids.add(json.loads(line)['id'])
    for view in manifest['anatomy_views']:
        require(set(view) == {'module', 'row_ids', 'mode'} and view['mode'] == 'reference', 'Duplicate canonical synapse ownership')
        require(set(view['row_ids']) <= row_ids, 'Unknown canonical connection')
    owners = set()
    for owner in manifest['state_ownership']:
        require(set(owner) == {'row_id', 'model_instance', 'state_kind', 'owner', 'operator_ref'}, 'Invalid state ownership')
        require(owner['row_id'] in row_ids, 'Unknown canonical state owner')
        key = (owner['row_id'], owner['model_instance'], owner['state_kind'])
        require(key not in owners, 'Duplicate canonical synapses receive independent state ownership')
        owners.add(key)
        require(owner['row_id'] not in conflicted, 'Shared physiological rules unresolved; no composed ownership in v0.1')
        require(owner['operator_ref'] in deps, 'Unpinned physiological operator')
        op = entries[owner['operator_ref']]
        require(op.get('runtime_operator_approved') is True, 'No runtime physiological operator approved by this release')
    neuron_artifact = strict_load(HERE / registry['neurons_artifact']['path'])
    neuron_ids = {n['id'] for n in neuron_artifact['neurons']}
    local_ids = set()
    for state in manifest['local_states']:
        require(set(state) == {'id', 'neuron_id', 'partition', 'kind', 'evidence_refs', 'assignment_status'}, 'Invalid local state schema')
        require(state['id'] not in local_ids and state['neuron_id'] in neuron_ids, 'Duplicate/unknown local state owner')
        local_ids.add(state['id'])
        require(state['kind'] in {'electrical', 'calcium', 'release', 'modulatory', 'biochemical'}, 'Product state kind')
        require(state['assignment_status'] == 'proposal_only', 'This release approves no root-specific physiological local state map')
        require(bool(state['evidence_refs']) and set(state['evidence_refs']) <= set(deps), 'Unpinned local-state justification')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--experiment', type=Path)
    ap.add_argument('--revision', type=Path)
    ap.add_argument('--review', type=Path)
    args = ap.parse_args()
    release, registry = load_release()
    if args.revision:
        require(args.review is not None, 'Revision requires an explicit reviewed evidence admission file')
        validate_revision(registry, strict_load(args.revision), strict_load(args.review))
    if args.experiment:
        validate_experiment(strict_load(args.experiment), release, registry)
    print(json.dumps({'valid': True, 'version': registry['version'], 'entries': len(registry['entries']),
                      'canonical_rows': 449600, 'shared_KC_MBON07': 4622, 'shared_KC_MBON11': 1053,
                      'protected_files': len(strict_load(HERE / 'FROZEN_INPUTS.json'))}))


if __name__ == '__main__':
    main()

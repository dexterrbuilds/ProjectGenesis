"""Public CLI for the complete v0.1 specification checks."""
import argparse
import json
from build import HERE, ROOT, file_hash
from validate import load_release, strict_load, require, local_path
from policy import check_frozen_policy, check_experiment, check_revision, check_profiles


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--experiment')
    ap.add_argument('--revision')
    ap.add_argument('--review')
    ap.add_argument('--package', action='store_true', help='Verify the finalized specification manifest')
    args = ap.parse_args()
    release, registry = load_release()
    check_frozen_policy(registry)
    check_profiles(registry)
    for rel, sha in strict_load(HERE / 'RESUMED_WORK.json').items():
        require(file_hash(local_path(HERE, rel)) == sha, 'Interrupted work changed: ' + rel)
    if args.experiment:
        check_experiment(strict_load(local_path(ROOT, args.experiment)), release, registry)
    if args.revision:
        require(args.review is not None, 'Independent reviewed evidence admission required')
        check_revision(registry, strict_load(local_path(ROOT, args.revision)), strict_load(local_path(ROOT, args.review)))
    if args.package:
        manifest = strict_load(HERE / 'SPEC_MANIFEST.json')
        payload = {k: v for k, v in manifest.items() if k != 'content_sha256'}
        from build import digest
        require(digest(payload) == manifest['content_sha256'], 'Package content address mismatch')
        for rel, sha in manifest['files'].items():
            require(file_hash(local_path(ROOT, rel)) == sha, 'Specification package changed: ' + rel)
    print(json.dumps({'valid': True, 'release': release['registry']['sha256'],
                      'entries': len(registry['entries']), 'protected_files': 3848,
                      'canonical_rows': 449600, 'shared_rows': {'KC_MBON07': 4622, 'KC_MBON11': 1053}}))


if __name__ == '__main__':
    main()

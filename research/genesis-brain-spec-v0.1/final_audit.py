"""Finish or check the specification package. No neural models or database writes.

Completion requires separately saved read-only canonical DB audits. --check only
reads package inputs and invokes the package verifier; it does not rerun tests.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from build import HERE, ROOT, canonical, digest, file_hash, immutable
from validate import strict_load, require


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
    if args.check:
        subprocess.run([sys.executable, str(HERE / 'check.py'), '--package'], cwd=ROOT, env=env, check=True)
        print((HERE / 'VERIFICATION.json').read_text())
        return
    require(not (HERE / 'SPEC_MANIFEST.json').exists(), 'Package already frozen; use --check')
    started = time.monotonic()
    commands = [
        [sys.executable, '-m', 'unittest', 'discover', '-s', str(HERE), '-p', 'test_*.py', '-v'],
        [sys.executable, str(HERE / 'check.py'), '--experiment',
         'research/genesis-brain-spec-v0.1/EXPERIMENT.example.json'],
    ]
    checks = []
    for i, command in enumerate(commands):
        t = time.monotonic()
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
        logfile = HERE / f'validation-{i + 1}.log'
        immutable(logfile, (result.stdout + result.stderr).encode())
        require(result.returncode == 0, 'Validation failed; inspect ' + str(logfile))
        checks.append({'command': command, 'exit_code': result.returncode,
                       'wall_seconds': time.monotonic() - t, 'log': logfile.name})
    import re
    tests = re.search(r'Ran (\d+) tests', (HERE / 'validation-1.log').read_text())
    require(tests is not None, 'Missing test result count')
    before = strict_load(HERE / 'CANONICAL_BEFORE.json')
    after = strict_load(HERE / 'CANONICAL_AFTER.json')
    require(before == after == strict_load(ROOT / 'research/fly-representation-study/CANONICAL_AFTER.json'),
            'Canonical Genesis changed')
    require(after['tableRowCounts']['genesis_decisions'] == 7 and all(not s['enabled'] for s in after['schedule']),
            'Canonical preservation failed')
    protected = strict_load(HERE / 'FROZEN_INPUTS.json')
    resumed = strict_load(HERE / 'RESUMED_WORK.json')
    require(all(file_hash(ROOT / p) == h for p, h in protected.items()), 'Protected file changed')
    require(all(file_hash(HERE / p) == h for p, h in resumed.items()), 'Interrupted specification changed')
    report = {'task': 'Biological Neural Specification v0.1; synthesis/infrastructure only',
              'status': 'COMPLETE_FOR_REVIEW', 'new_biological_results': 0,
              'new_neural_simulation_runs': 0, 'optimization_runs': 0, 'genesis_cycles_run': 0,
              'registry_entries': 151, 'mechanism_profiles': 11, 'parameters_operators': 65,
              'capabilities': 11, 'canonical_neurons': 5480, 'canonical_aggregate_rows': 449600,
              'shared_rows': {'KC_MBON07': 4622, 'KC_MBON11': 1053},
              'tests_passed': int(tests.group(1)), 'checks': checks,
              'protected_files_unchanged': len(protected), 'interrupted_files_unchanged': len(resumed),
              'canonical_snapshot_sha256': after['sha256'], 'canonical_cycles': 7, 'schedule_enabled': False,
              'classification_changes': [], 'physiological_rules_composed': 0,
              'review_admissions_published': 0,
              'elapsed_verification_seconds': time.monotonic() - started,
              'limitations': ['Validators enforce structured provenance and ownership, not truth of arbitrary prose.',
                             'Supersession review is a human governance artifact, not a cryptographic signature.',
                             'Passing infrastructure tests does not validate a biological capability.']}
    immutable(HERE / 'VERIFICATION.json', json.dumps(report, sort_keys=True, indent=2).encode() + b'\n')
    files = {str(p.relative_to(ROOT)): file_hash(p) for p in sorted(HERE.rglob('*'))
             if p.is_file() and '__pycache__' not in p.parts and p.name != 'SPEC_MANIFEST.json'}
    files['GENESIS_BRAIN_SPEC.md'] = file_hash(ROOT / 'GENESIS_BRAIN_SPEC.md')
    payload = {'name': 'Project Genesis Biological Neural Specification', 'version': '0.1.0',
               'registry_sha256': strict_load(HERE / 'RELEASE.json')['registry']['sha256'],
               'files': files, 'file_count': len(files)}
    manifest = {**payload, 'content_sha256': digest(payload)}
    immutable(HERE / 'SPEC_MANIFEST.json', json.dumps(manifest, sort_keys=True, indent=2).encode() + b'\n')
    subprocess.run([sys.executable, str(HERE / 'check.py'), '--package'], cwd=ROOT, env=env, check=True)
    print(json.dumps({'complete': True, 'tests': report['tests_passed'], 'package_sha256': manifest['content_sha256'],
                      'protected_files': len(protected), 'canonical_cycles': 7, 'schedule_enabled': False}))


if __name__ == '__main__':
    main()

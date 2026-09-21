# Stage-5 execution authorization: preflight stopped

No Stage-5 analysis was executed. No Stage-1 source-summary numerical values were read. This package records an unsuccessful preflight, not a scientific Stage-5 result.

## Release identity

The unique protocol release identifies `content_sha256` as the authorization value. Both its existing `seal.py` and `prospective_analysis.py::require_authorization` define the digest as SHA-256 of the compact, sorted, UTF-8 JSON file-hash map. Independent recomputation matched:

`3fef9c2fad9b7b8be982c699299f957395199d811774041a052237efeb78ec3d`

All 28 sealed artifacts matched their hashes, including the analysis code. The sealed static suite passed 17/17 tests. The separate execution-authorization record was not created before the stop. Therefore AUTHORIZATION_REFERENCED_HASH is null, and AUTHORIZATION_HASH_MATCH is not verified; it must not be reported TRUE.

## Material preflight issue

The newly written auxiliary checker incorrectly compared the raw bytes of Brain Spec v0.2's `PACKAGE_MANIFEST.json` against the pinned **package-content** hash. Those hashes identify different objects. Its erroneous comparison returned a failure:

- Raw manifest-file SHA-256: `e961f9105e0101ab110503386b158d3548acf62962ea23c885caa4d1ae64869c`.
- Pinned package-content SHA-256: `9322ea0f3c501b6bd29add73464c94b775fb616648801e7f945346776b9bdd0b`.

The dependency's existing `check.py --package-only` subsequently confirmed the pinned content hash and all 32 package files. This establishes a mistake in the auxiliary checker, not evidence of changed dependency bytes. Of 10,059 comparisons in the auxiliary audit, this was the only reported failure. The incorrect checker and original failure record are preserved without alteration. Neither the sealed protocol nor its verifier was repaired, weakened or resealed.

The user's authorization explicitly required stopping on any failed preflight check. Execution therefore remains stopped for review despite diagnosis of this false alert. No source-summary unblinding or analysis process followed it.

## Requested execution coverage and outcomes

| Item | Status |
|---|---|
| Sealed protocol hash | Independently verified, as above |
| Authorization record / matching | Not created / not verified |
| Preflight | Stopped due to auxiliary checker error |
| Prospective analysis execution | NOT STARTED |
| Fresh processes / reproducibility | 0 / NOT TESTED |
| Runs | 28 planned, 0 evaluated |
| Units | 224 planned, 0 evaluated |
| Families | E, Z, P, R, WP, WR, H, U, N planned; none evaluated |
| P source-dependence gate | UNASSESSABLE — analysis not started |
| R source-dependence gate | UNASSESSABLE — analysis not started |
| Scientific family/result classifications | None issued |
| Null compatibility | No execution-derived result |
| Directional transfer sensitivity | No execution-derived result |
| Robust invariants established | None by this execution |
| Failed scientific controls | None evaluated |
| Integrity issue | Incorrect auxiliary hash-object comparison; no actual protected/sealed file mismatch established |

No scientific inference is made from this stopped preflight. It does not change any prior classification and is not a new biological PASS/FAIL. The frozen protocol's prospective mathematical statements remain prospective; this report does not present them as executed findings.

## Preservation

The closing audit verifies all 9,170 protected files, all 28 sealed protocol artifacts and the protocol release file. Read-only database audits before and after match the frozen audit exactly:

- Database digest: `3377c9dddbe2abf89ed9a820a6aabbc1da951cac7bfc1823471c5aac043ea312`.
- Seven decisions.
- Schedule disabled.

No neural simulation, neural replay, Stage-1 retraining, new sensory stimulus, connectome extraction, fitting, wallet action, runtime activation, BrainAdapter modification, Brain Spec change, capability admission or next-stage design occurred. Prior research bytes remain unchanged.

## Evidence categories

- **BIOLOGICAL FACT:** No new biological observation or claim.
- **EXPERIMENTALLY SUPPORTED COMPUTATIONAL APPROXIMATION:** No approximation evaluated or newly admitted.
- **HYPOTHESIS:** No transfer hypothesis tested in this stopped execution.
- **ENGINEERING / MATHEMATICAL ASSUMPTION:** Hash verification and the distinction between a file hash and a package-content hash only; no scientific parameter changed.
- **GENESIS PRODUCT MAPPING:** None.

## Package interpretation

This is a content-addressed **preflight failure-evidence package**, not the requested scientific results package, which cannot exist without authorized successful execution. `EXECUTION_STATUS.json` uses null for unavailable outcomes. `INTEGRITY_BEFORE.json`, the original auxiliary script, static test logs, the authoritative verification observation, environment and closing preservation audit are retained. No authorization, execution stdout/stderr or scientific result is fabricated for processes that were never started.

Stop for review.

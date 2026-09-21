# External preflight correction — attempt 2

Only hash-object semantics change: Brain Spec package_sha256 is compared with SHA-256 of canonical manifest content excluding its own content_sha256 field, exactly as the owning check.py/check_published defines it. It is not compared with SHA-256 of raw manifest bytes. The raw manifest bytes remain independently protected by the unchanged 9,170-file preservation manifest.

All original protected-file comparisons remain. Explicit labels distinguish FILE HASH, MANIFEST HASH (raw pinned manifest bytes), PACKAGE-CONTENT HASH and RELEASE/CONTENT HASH. Added checks verify preservation of attempt 1 and equality with the explicitly authorized Stage-5 release. No scientific rule or sealed file changes. The original checker and failure remain immutable. CHECKER_DIFF.patch documents the exact correction and extra historical-preservation checks.

Authoritative verification is restricted to existing release/package methods. The prior minimal-identifiability full suite reads Stage-1 RESULTS.csv, so it is not run before authorization; its existing test_19_release_if_sealed verifies its complete sealed release without reading source values. No model, data acquisition or optimization is invoked.

Final external checker is verify_integrity_v3.py. Before authorization, its audit-label assignment was made conditional on an absent label so that a PACKAGE-CONTENT HASH label cannot be overwritten by a generic RELEASE/CONTENT label. Digest calculations and comparisons are unchanged from v2. Both versions and their records are retained. CHECKER_FINAL_DIFF.patch gives the complete change from attempt 1.

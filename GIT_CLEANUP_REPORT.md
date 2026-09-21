# Project Genesis — Git repository cleanup

Date: 2026-09-21. Git hygiene only. No Genesis execution, database access/mutation, deployment, provider call or push.

## 1. Diagnosis and likely cause

The three unpublished commits contained **943,994,607 bytes of uncompressed Git objects**. A local non-thin pack estimate for `HEAD ^origin/main` was **659,549,578 bytes** (629.0 MiB). The main contributors were generated neural traces/checkpoints, downloaded scientific datasets and extracted connectome arrays—not application code or file count alone.

The largest individual blobs were three 67,392,116-byte arrays (64.3 MiB each). No unpublished blob exceeded 100 MiB. GitHub warns above 50 MiB and blocks above 100 MiB, so the three arrays cross its warning threshold but do not establish a hard-limit rejection. See [GitHub's file-size documentation](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).

**The exact failed-push error was not available.** Excessive transfer size is a credible contributor, not a proven explanation for an HTTP/authentication/network error. The repository has no custom pre-push hook, mirror configuration or forced HTTP tuning. GitHub remote inspection succeeded after obtaining network access. No credentials, Git transport settings or arbitrary `http.postBuffer` workaround were changed.

## 2. Original Git/repository size

| Measurement | Before cleanup |
|---|---:|
| Working directory, including `.git`, allocated/rounded | 18 GiB |
| `.git`, allocated/rounded | 795 MiB |
| Loose objects | 1,133 / 145,516 KiB |
| Packed objects | 5,764 in two packs / 667,649 KiB |
| Tracked files | 6,129 |
| Nonignored untracked files | 984 |
| Unpublished commits | 3 |
| Unpublished uncompressed objects | 943,994,607 bytes |
| Estimated unpublished transfer pack | 659,549,578 bytes |

Local research occupies about 15 GiB; generated outputs about 968 MiB; local PostgreSQL files about 920 MiB; `node_modules` about 602 MiB; `.next` about 329 MiB. Most local downloaded research data and all normal database/build/dependency directories were already outside Git. Disk usage is not the amount that would be pushed.

Original status, object measurements and private audit scratch files are retained under ignored `outputs/git-cleanup/`. Sanitized measurements are in [GIT_CLEANUP_METRICS.json](GIT_CLEANUP_METRICS.json).

## 3. Largest offending files/objects

| Path | Bytes |
|---|---:|
| `research/fly-boundary-study/anatomy/count.npy` | 67,392,116 |
| `research/fly-boundary-study/anatomy/post.npy` | 67,392,116 |
| `research/fly-boundary-study/anatomy/pre.npy` | 67,392,116 |
| `research/fly-boundary-study/anatomy/contacts.npz` | 48,274,299 |
| `research/fly-stage3/artifacts/28cc6285ba4b40077db73952bacee75d0938f2f80021aaf89c214524797b2a52/circuit.json` | 37,504,446 |
| `research/fly-t4t5-empirical-interface/HELDOUT_PREDICTIONS.npz` | 35,295,658 |
| `research/fly-boundary-study/anatomy/neuropil.npy` | 33,696,122 |
| `research/fly-t4t5-empirical-interface/pre_numeric_identity_correction/HELDOUT_PREDICTIONS.npz` | 32,802,443 |
| `research/fly-t4t5-boundary/PREDICTIONS.npz` | 25,549,116 |
| `research/fly-boundary-study/anatomy/nodes.json` | 25,186,566 |

Duplicate/replay copies compounded the working-tree size; identical blob objects are counted once in the object/pack analysis. Additional not-yet-committed research downloads were also protected from accidental future staging by the new rules.

## 4. Classification and files kept tracked

### A — Must remain tracked / eligible for their owning source commit

Application, runtime/core/server code, prepared SQL/migrations, tests and test support, package manifests/lockfiles, configuration templates, deployment files/runbooks, research analysis source, review documents, small results and manifests remain intact and eligible for Git.

Both Brain Spec releases are retained completely, including their intentionally versioned logs. **Brain Spec v0.2 is a direct runtime dependency**: `core/v2/biology.ts` verifies its package and registry, and Docker copies it. It was not replaced by a stub, altered or excluded. `data/connectome.json`, `data/source/Cook2019HermReader.json`, public assets and research source are retained.

The `verification/` tree is **not** blanket-ignored. Markdown reports, JSON manifests/summaries/catalogs and inspection scripts remain eligible. Only generated text logs, screenshots and private-export patterns are excluded.

Pre-existing pending implementation edits and new source files remain exactly as found: **they were not silently committed as part of a hygiene change**. “Ready to push” below describes the cleaned committed history; pushing does not publish uncommitted work. The later Runtime V1 implementation must receive its own reviewed source commit if it should also be published.

### B — Keep locally, do not track

Generated scientific arrays/traces/checkpoints, binary downloaded measurements/archives, large extracted circuit/node/selection payloads, raw HTTP headers, downloaded source attachments, generated logs/screenshots, private exports, local databases and environment files.

### C — Regenerable but preserved in this task

`.next`, `node_modules`, build outputs, Python/TypeScript caches, temporary test outputs. No need to delete these to reduce push size; they remain on disk.

### D — Conservative retention / review if future reduction is desired

Medium-sized frozen JSON measurement results, training profiles, atlas metadata, coverage and governance manifests remain tracked. Their meaning is useful and their sizes are manageable. No ambiguous source or evidence file was removed merely because it was large.

## 5. Untracked artifacts preserved locally

**3,010 previously tracked paths**, totaling **1,015,168,424 working-tree bytes**, were removed from the index and filtered from the unpublished snapshots. The local byte total differs from the unpublished object total because it includes duplicate copies and some generated artifacts already present in published history.

[ GIT_LOCAL_ARTIFACTS.json ](GIT_LOCAL_ARTIFACTS.json) inventories **6,812 locally preserved ignored research/verification/output artifacts**, totaling **16,830,606,836 bytes**. Each record has path, size, exclusion reason and whether this cleanup removed it from the index; pre-audited files also have SHA-256. It includes previously ignored evidence as well as new exclusions. It contains no file contents or secret values. Local database/build directories are described at directory level above rather than publishing a PostgreSQL internal-file inventory.

All 3,010 removed paths still exist. A before/after SHA-256 comparison verified **7,112 pre-existing tracked/untracked files unchanged**, excluding only the intentionally edited `.gitignore`. This covers application/source work, scientific files and the removed artifacts. The uncommitted source edits were preserved rather than reset to HEAD.

A fresh Git clone is now a **source/specification/review repository, not a complete scientific dataset archive**. Full frozen evidence packages remain on this computer, with their original manifests and bytes. Replaying historical research elsewhere requires those archived artifacts. Existing frozen manifests were not regenerated to pretend partial Git packages are complete. Separately back up local evidence before ever cleaning or moving this directory.

## 6. Regenerable files removed

**None.** No research file, database, build directory, cache, screenshot or source file was deleted from the working tree. Only temporary Git-index machinery created for this cleanup was removed after use.

## 7. `.gitignore` changes

Existing dependency/build/local-state/private-output rules were retained. New rules are scoped as follows:

| Rule group | Reason |
|---|---|
| `/research/**/*.npz`, `.npy`, `.RData`, `.mat`, `.xls`, `.xlsx`, `.zip`, `.bin`, `.gz` | Generated/downloaded scientific payloads, not runtime assets. |
| `/research/**/sources/` | Downloaded primary attachments/pages; local authoritative copies remain. |
| `/research/**/artifacts/**/circuit.json` | Large extracted research circuit payloads; source and manifests retained. |
| Two exact `fly-boundary-study/anatomy` JSON paths | Generated full node and selection arrays. |
| `/research/fly-upwin-route-evidence/processed/*.json*` | Processed large measurement payloads, preserved locally. |
| `/research/**/*headers*` | Captured HTTP headers can carry signed download credentials. |
| `__pycache__/`, `*.pyc`, `*.pyo`, `*.log`, `/build/` | Regenerable caches and generated logs/build output. |
| `/verification/**/*.txt`, `*.png`, `**/browser/` | Inspected contents are test/build/status logs and review screenshots. Human-readable Markdown and manifests are not hidden. |
| Scoped `PRIVATE*`, `*.dump`, `*.sql.gz`, SQLite database/sidecar patterns | Defense against accidental private export/database staging. Prepared `.sql` remains tracked. |
| Explicit negations for `genesis-brain-spec-v0.1/**` and `v0.2/**` | Keep the intentionally versioned release packages complete. |

No source-language file was excluded by the removal list. `.git/info/exclude` was inspected and left unchanged. Existing nested ignore files and frozen packages were not edited.

## 8. Unpublished history rewrite

GitHub's live advertised branch tip matched the local `origin/main` boundary. There were no remote tags or other advertised branches requiring shared-history rewriting. Exactly three linear commits were unpublished.

A temporary Git index filtered only reviewed artifact paths from each of the three commit trees. Author/committer metadata and messages were retained. Every original-vs-rewritten tree diff was checked to contain **only deletions from the approved artifact list**, preserving all source changes. Local `main` was advanced with a compare-and-swap ref update; the real index was updated without checking out or deleting any working-tree files.

Some older generated scientific artifacts remain in already-published ancestry. That history was **not** rewritten. The largest file at the published tip was about 10.1 MB, not a GitHub oversized-file blocker. Published configuration URL matches were reviewed as local examples/ephemeral CI credentials, not operator secrets.

## 9. Original HEAD, boundary and safety branch

- Original HEAD: `de59ee469314452feb2a70491fffde8d26613533`.
- Verified published boundary / merge-base: `466dd10ec9679c1b736eef2980e1d295b7d1e20d`.
- Local safety branch: **`safety/pre-git-cleanup-20260921`**, pointing to the original HEAD.
- Rewritten unpublished tip before the hygiene-only commit: `ba27419e2cf827d88e3a39ae30d4e215b2eb45a7`.

| Original unpublished commit | Replacement |
|---|---|
| `d582ae3202134de29a4b672889adc78095df2409` | `980f0a5` |
| `b607200a88ccfe781ff3ef67731b0b237e4910b2` | `000f1fc` |
| `de59ee469314452feb2a70491fffde8d26613533` | `ba27419` |

The safety branch must remain local until the cleaned push is confirmed. **Do not push `--all`, `--mirror`, or this safety branch**: that would publish the original bulky history/header capture again. It is a Git-history safety reference, not a backup of uncommitted work. The latter remains on disk and is hash-inventoried.

## 10. New repository size

At the cleaned three-commit tip, before adding this small hygiene report/manifest commit:

| Measurement | After rewrite |
|---|---:|
| Tracked files | 3,119 |
| Unpublished blob bytes | 83,900,829 |
| Estimated unpublished transfer pack | **11,698,346 bytes (11.2 MiB)** |
| Pack reduction | **98.2%** |
| Largest unpublished blob | **8,394,739 bytes (8.0 MiB)** |
| Working directory including `.git`, allocated | 19,346,468 KiB (18.45 GiB) |
| `.git`, allocated | 815,988 KiB (796.9 MiB) |

The hygiene commit adds only `.gitignore` plus this report, the preservation manifest and sanitized metrics; its three new tracked documents bring the file count to **3,122**. The final pack estimate is recorded locally after that commit in `outputs/git-cleanup/FINAL_PUSH_METRICS.json` and remains approximately 12 MB.

The working directory did not shrink because local evidence was deliberately preserved. `.git` did not shrink because the safety branch/reflogs intentionally retain original objects; newly written small replacement trees add modest overhead. **No manual garbage collection or reflog pruning was requested.** Git’s automatic housekeeping consolidated loose objects during these Git operations: the final check found zero loose objects and 7,400 packed objects in three packs (795,805 KiB). Final allocated disk usage was 800,176 KiB for `.git` (781.4 MiB) and 19,329,732 KiB for the full working directory (18.43 GiB). The original safety branch remains intact; none of its reachable evidence was pruned. Retained safety objects do not enter a normal explicit `main` push.

Pack estimates were measured by streaming `git pack-objects --revs --stdout` for `HEAD ^origin/main`, without storing a second large pack. Actual network transfer can differ through negotiation/delta choices.

## 11. Largest remaining tracked/unpublished files

| Path | Bytes | Why retained |
|---|---:|---|
| `research/fly-t4t5-boundary/TEST_TRACE_METRICS.json` | 8,394,739 | Frozen per-trace results; useful evidence, manageable size. |
| `data/source/Cook2019HermReader.json` | 5,843,687 | Existing structural source data; already published. |
| `research/fly-t4t5-boundary/TRAINING_PROFILE.json` | 5,534,142 | Frozen analysis metadata. |
| `research/fly-t4t5-empirical-interface/atlas/records.json` | 5,173,226 | Measurement atlas metadata. |
| `research/fly-stage4/circuits/L1.json` | 4,578,706 | Manageable reviewed circuit record, retained conservatively. |
| `research/fly-t4t5-empirical-interface/PREDICTION_METRICS.json` | 4,390,378 | Frozen result metrics. |

Full largest-object lists and object IDs are in the sanitized metrics file. No remaining unpublished object approaches 50 or 100 MiB.

## 12. Secret/privacy findings

No secret values are included here. Scans covered reachable published/unpublished blob contents with credential patterns, exact comparisons against nontrivial local credential values, private-export paths and full-canonical-row-export markers. Current tracked/untracked text was checked too. This is a bounded repository audit, not proof that arbitrary prose contains no confidential information.

| Path | Type/category | Tracked before / after | Unpublished history | Remediation |
|---|---|---|---|---|
| `research/fly-t4t5-boundary/metadata/figure2-range-headers.txt` | **Temporary signed third-party download URL**, a bearer-style access artifact | Yes / no | Yes in original; absent from cleaned range | Kept locally, ignored, removed from replacement commits. Recorded expiry is already in the past. No operator/API key was identified. Original remains in local safety history. |
| `.env`, `.env.local` | Local configuration potentially containing provider/database secrets | No / no | No matching committed env-file content or actual local secret value found | Keep ignored and private. |
| `.env.example`, `README.md` | Example local database URLs | Yes / yes | Historical versions reviewed | Placeholder/default localhost examples, not operator credentials. Retain. |
| `.github/workflows/verify.yml` | Local disposable PostgreSQL CI credential | Yes / yes | Historical version reviewed | Matches declared ephemeral CI service password. Retain. |
| `outputs/**/PRIVATE*`, `outputs/runtime-v1/test-db.env`, `.local/` | Private exports, local connection configuration, canonical/test database files | No / no | Not found in inspected history | Existing ignore boundaries retained; no database opened. |

**Removing a committed credential never revokes it.** The confirmed access artifact here is an already-expired signed download URL, not a discovered active operator/provider credential. No credential was rotated. If a future manual review identifies an active secret, invalidate it separately even if its Git copy is removed. Do not publish the safety branch.

No raw canonical memory export, private wallet key, active provider key or operator token was detected in the cleaned push range. Publicly published history was not rewritten; no published confidential-data blocker was identified by these checks.

## 13. Integrity verification

- TypeScript: **PASS**, `tsc --noEmit --incremental false`.
- ESLint: **PASS**, zero errors/warnings.
- Git object integrity: **PASS**, `git fsck --full`.
- All 7,112 checked pre-existing files other than `.gitignore`: identical SHA-256 and size.
- Removed tracked artifacts: all 3,010 still present locally, byte-identical.
- Original published boundary: preserved; cleaned `main` is its descendant.
- Complete Brain Spec/runtime source/config/test bytes: unchanged.
- Canonical databases: **not accessed, opened, exported, migrated or altered**. No canonical digest was recomputed in this hygiene task.
- Genesis, provider, scheduler, wallet and external executors: not run.

No lifecycle/database test suite was rerun: this task expressly forbids altering databases, and the implementation is byte-identical. Type/lint/Git/hash verification is appropriate to index/history/ignore-only changes. Prior implementation test results are not represented as newly run results.

## 14. Push command and pending source work

After reviewing this cleanup, use the normal explicit branch push:

```sh
git push origin main:main
```

**No force push is required:** the remote published commit is unchanged and remains an ancestor of the replacement history. Do not use `--all` or `--mirror`. Nothing has been pushed automatically.

Important: the pre-existing modified/untracked Runtime V1 implementation and verification documents remain pending. The hygiene-only commit intentionally does not bundle them. A normal push publishes committed history only. If the intention is also to publish all later implementation work, review and commit that pending source/documentation separately first; the new ignore rules prevent the excluded datasets/private outputs from entering through an ordinary add. Do not force-add ignored artifacts.

## 15. Remaining blockers and limits

No known file-size, object-integrity or detected active-secret blocker remains for the cleaned `main` push. The pack has been reduced from roughly 660 MB to roughly 12 MB. This does not prove GitHub authentication, branch protection, network stability or account policy will accept a push; the actual operation was intentionally not attempted. If a normal push still fails, retain its exact sanitized error rather than changing implementation or forcing shared history.

Local evidence still needs its own durable backup; this cleanup is not a research archival service. Published old scientific blobs remain in shared ancestry and the local safety branch retains the original unpublished objects. Neither needs a force rewrite to push the cleaned branch.

GIT REPOSITORY CLEANED — READY TO PUSH

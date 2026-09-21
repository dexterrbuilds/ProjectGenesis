# Project Genesis — Pass 2: Usable Memory and Historical Recall

## 1. Summary

Implemented deterministic, private memory retrieval and connected it to the existing context compiler, isolated preparation path, and one-shot preparation/commit verification. Eligible past experiences, local artifacts and sourced unverified assertions can now enter bounded working context without an LLM, embeddings, network access, or biological advancement.

**The seven canonical legacy memories remain excluded.** Their records contain no disclosure evidence sufficient to admit them automatically. The read-only diagnostic discovered all seven, explained every exclusion, and selected none for four synthetic queries. This is an intentional privacy result, not a claim that Genesis already recalls those seven records.

| Capability | Verified result |
|---|---|
| Recall eligible historical experiences | Yes: explicitly reviewed legacy fixtures and internally admitted V2 episodes |
| Distinguish present observation from past memory | Separate context sections, timestamps, kinds and interpretations |
| Recall prior local artifacts | Yes: bounded database-text excerpts linked to their producing episode/decision |
| Retrieve semantic/self assertions with provenance | Yes: sources resolve independently of whether their text was selected |
| Remain bounded as history grows | Verified with 10, 100 and 1,000 episode fixtures; limits below |
| Operate without a live LLM | Yes: deterministic code only |
| Recall canonical legacy records today | No: missing disclosure evidence; no consent invented |
| Send newly usable private memory to a provider automatically | No |

**241 tests passed, 0 failed, 0 skipped**: the original 192 plus 49 new tests. TypeScript, ESLint and the verified Webpack production build passed. No activation or schema migration occurred.

## 2. Canonical preservation

Read-only audits before implementation and after verification compare complete canonical rows. Identity, birth, all seven decisions, seven memories, project, ledger, milestones, saved brain, Life State and disabled schedule remain unchanged.

- Organism: `817e772c-827e-48fc-8e35-6504cb2a8d2d`.
- Birth: `2026-09-15T01:56:07.867Z`.
- Decisions/cycles: **7**.
- Canonical V2 episodes: **0**.
- Execution: **CLOSED**.
- Schedule: **DISABLED**.
- Biology: **SAVED-OBSERVATION-ONLY**.
- Live provider calls, wallet actions, external communications during this pass: **0**.

Recomputed before/after canonical row digest:

`4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`

All 9,319 frozen-inventory files match. The completion-audit and Pass-1 artifact manifests also match. No original row, scientific model, frozen research package, Brain Spec, constitution, public projection, or first-awakening permission configuration was edited. All writing tests use disposable fixture schemas/stores. Private database exports remain in `outputs/memory-pass/`, not in the public review package.

## 3. Memory ownership

1. **Biological-model memory:** original saved snapshot remains separately owned and unchanged. Retrieval can reference a historical biological observation's identity/status provenance; it neither recalls neural values as facts nor updates plastic state.
2. **Episodic memory:** authoritative legacy memory/decision rows and V2 episode/decision rows. Retrieval creates a derived projection, never replacement history.
3. **Semantic/self memory:** existing sourced, confidence-bearing, unverified planner/operator assertions in Life State. Retrieval does not verify their truth or convert them to observations.
4. **Working context:** temporary, bounded serialization compiled for one reasoning request. It is not an additional persistent memory store.

## 4. Retrieval architecture

`server/memory-store.ts` reads existing tables in a read-only transaction, verifies organism/revision ownership and database envelope identity/time, and projects only the source fields needed for recall. No new table, migration, endpoint or external dependency is required.

`core/v2/memory.ts` provides the typed `MemoryArchive`, `MemoryReview`, `MemoryCandidate`, `MemoryQuery`, limits and `MemorySelection` boundary:

source discovery → schema/provenance checks → disclosure → source resolution → supersession/deduplication → deterministic relevance → category/byte budget → selection manifest.

Each selected candidate retains kind, original source IDs, actual occurrence time where recorded, visibility, disclosure basis, project/task/subject associations where present, bounded text, source-projection hashes, uncertainty/author where applicable, relationships, untrusted-data status and interpretation limitations. Source hashes explicitly describe retrieval projections; they are not advertised as whole-database or frozen-research hashes.

The archive excludes neural arrays, raw planner/provider responses, private failure bodies, and reasoning rationale. It never reconstructs chain-of-thought. Original sources remain authoritative.

## 5. Disclosure model

Three independent permissions are represented: **private internal use**, **provider disclosure**, and **public display**. Visibility alone is not provider consent. Internal eligibility never changes public DTOs.

- Legacy records without disclosure metadata: excluded for both reasoning audiences.
- Old private V2 records without the new policy marker: excluded unless explicitly reviewed.
- Future V2 episodes created by the application carry `memory-disclosure-v1`: internal use permitted; provider and public disclosure false. This is an explicit engineering policy for new computational records, not retroactive consent for earlier history.
- Optional trusted `MemoryReview` inputs bind organism, record ID, exact source-projection hash, review reference, separate permissions, and operator-only status. A stale hash or wrong organism cannot authorize changed content. These inputs are never read from planner arguments, artifact text or a memory's instructions.
- Operator-only records are excluded from ordinary reasoning. Public-display permission cannot override an original private visibility label.
- Assertions cannot expand their sources' disclosure. Even an assertion over public/current evidence remains provider-excluded without its own explicit review; all underlying source permissions must also permit that audience.

The compiler selects the provider audience when `permission.llm` is true. There is no paid call or automatic disclosure fallback. This pass supplies a validated review-input boundary, **not an operator consent-management UI or new canonical review records**. The one-shot controller supplies no implicit review overrides.

Credential-like recall-query metadata is refused before context compilation. Credential-like text is rejected before excerpt selection, including common key/password/bearer/private-key patterns and credential-bearing URLs. This conservative filter is not a claim of complete secret detection; explicit disclosure remains the primary boundary.

## 6. Legacy memory handling

Legacy conversion validates ID, timestamp, text and source decision, requires the corresponding historical decision to exist and match time, and preserves both identities. Recorded legacy salience is not used as a psychological or biological importance measure. Legacy excerpts carry an explicit warning that historical computational decoder labels are not biological action authority.

The derived view can admit an explicitly reviewed fixture memory without rewriting it. The compiler does not dump all seven memories. An explicitly empty database archive cannot resurrect a missing row from the organism's cached memory array. The no-archive compiler compatibility path only diagnoses otherwise excluded legacy records; it does not create missing decision provenance.

## 7. V2 episodic handling

Episode and decision must agree on organism, source, episode ID, timestamp, outcome and action status. The retrieval summary contains recorded outcome/action classifications, not planner interpretation. Event/decision identities and bounded source metadata provide factual provenance. Project/task IDs come from the stored proposal; subject tags are used only when explicitly stored in the event's recall metadata.

`pendingAtRecording` describes the historical outcome, not a claim that an old request remains unresolved today. Current operator/workflow state is outside this pass.

A fixture cycle follows the real isolated orchestration and commit path. After a fresh database connection, retrieval reconstructs its episode, artifact and sourced assertion. No process-local memory cache or live provider is needed.

## 8. Semantic/self memory

Sources resolve through current event/biological provenance, eligible environment records, stored legacy memory/decisions, V2 episode/event/biological-reference records, artifacts, and other valid assertions. A source does not need to have its text selected first. In particular, a past event or biological-observation ID can resolve through its stored V2 decision/episode.

Broken, conflicting or cyclic provenance is excluded. Recursive assertion resolution has a depth limit of 32. Supersession chains must exist and be acyclic; superseded assertions are not presented as equally current. Contradiction relationships are made symmetric in the derived view, without rewriting assertions or choosing which belief is true. Deduplication preserves different provenance, confidence, authors and supersession/contradiction relationships.

Assertions retain `unverified_assertion` interpretation, author, confidence and source hashes. Their creation timestamp is **null** where the existing assertion schema did not store one; source time is not substituted. Removed environment evidence with no durable historical source still cannot be recovered: the system reports unresolved provenance instead of inventing it.

## 9. Artifact recall

The retrieval identity is derived as `<producing episode ID>:artifact`; it denotes the existing text field, not a newly created filesystem artifact. The episode and decision copies must agree and record local persistence. Corrupted references are excluded. Metadata includes producing episode/decision, project/task where present, disclosure and bounded excerpt.

No filesystem work, publication, artifact update workflow, or project lifecycle was added. Legacy project artifact text without sufficient event/disclosure provenance is not silently admitted.

## 10. Relevance algorithm

This is engineered structured/lexical retrieval, not semantic similarity or biological salience. Candidates are ordered lexicographically by:

1. Exact candidate/source reference match.
2. Same task.
3. Same project.
4. Same explicitly recorded subject.
5. Count of exact lowercase lexical token overlaps, capped at 10; tokens are at least three letters/digits/underscore/hyphen characters.
6. Pending/deferred outcome **at recording**.
7. Current unsuperseded unverified assertion.
8. Most recent recorded occurrence time.
9. Stable ID ordering to break ties.

Without another relevance signal, recorded experiences are eligible for a 30-day recency window. This is a documented engineering default, not a biological forgetting rule. Direct references can retrieve older records within the discovery domain and outrank newer unrelated history. A genuinely irrelevant archive can yield an empty selection. No model fitting, psychological score, neural interpretation or paid ranking is used.

## 11. Budgets and growth

Default retrieval ceilings:

- 3 episodic items total across legacy and V2;
- 3 semantic/self assertions;
- 1 artifact excerpt;
- 4,500 UTF-8 bytes for selected items including provenance;
- 600 UTF-8 bytes per excerpt;
- 12,000 UTF-8 bytes for the complete default working context.

Category ceilings are independent; fitting fewer items is normal. Excerpts stop at complete Unicode code points. Structured provenance is never string-truncated. An item that cannot fit is dropped whole, with a reason. Mandatory context exceeding its own bound causes refusal rather than silent removal.

Database discovery is capped at 10,000 rows per source table and reports `discoveryComplete=false` if clipped. Legacy records and artifact text over 65,536 bytes are excluded/bounded at discovery; oversized artifacts receive an explicit exclusion reason. Record envelopes are checked against database IDs, timestamps, parent IDs and ownership. Malformed optional records are excluded rather than repaired.

Measured isolated growth probe (one run, not a production capacity guarantee):

| Fixture episodes | Selected items | Selected bytes | Complete context bytes | Retrieval wall time |
|---|---:|---:|---:|---:|
| 10 | 3 | 4,391 | 8,391 | 13.23 ms |
| 100 | 3 | 4,412 | 8,412 | 10.49 ms |
| 1,000 | 3 | 4,433 | 8,433 | 85.69 ms |

All outputs were deterministic on repeated selection. The explicitly referenced `d1:episode` remained first at every size. Process RSS during this sequential probe reached about 220 MiB at 1,000 records; that includes Node, fixtures and prior allocations, not an isolated incremental per-record measurement. See `growth.json` and reproducible `growth-probe.ts`.

The current implementation scans a capped archive and sorts candidates; it is adequate for the tested scale, not a claim of unlimited retrieval. Beyond the cap, older sources may be outside discovery and assertions referencing them fail closed. Database retrieval/query indexing and bounded diagnostic retention may need later work. Existing growing organism/Life State JSON, episodic-reference arrays, semantic assertion arrays and private selection manifests remain separate storage/processing bottlenecks. No vector infrastructure is justified by these tests.

## 12. Context compiler integration

The compiled structure separates:

- current event and critical current Life State;
- relevant past experiences;
- current unverified semantic/self memory;
- relevant prior artifacts;
- provenance, disclosure and uncertainty metadata.

Remembered text is explicitly untrusted data, never a directive or current observation. Selection version, query hash, audience, limits and discovery completeness enter the serialized context. Selected IDs, exclusions, reasons, bytes and selection hash enter the private manifest. The final context budget can drop additional optional items, and the manifest reflects the actual final selection.

One-shot preparation loads the archive. Commit rereads it and recompiles context under existing fences; a changed selected assertion causes rejection. Original grant, provider, lease, decision-count and execution locks remain intact. Runtime identity advances to `runtime-v1-oneshot-1.0.2`, with new memory modules included in the code hash. This does not authorize any grant.

## 13. Diagnostic of the seven canonical memories

`seven-memory-diagnostic.json` records read-only synthetic retrieval, with no life event persisted and no planner/provider called.

For recent history, explicit first-memory reference, existing-project reference, and lexical review queries:

- Discovered legacy records: **7** each.
- Records with disclosure metadata: **0**.
- Eligible: **0**.
- Excluded: **7** each.
- Selected: **0**.
- Every exclusion: `not admitted for internal: missing-disclosure`.

The diagnostic lists each source ID and its reason without printing memory text. An operator would need an explicit source-bound disclosure review before these records could be used. Internal-use review and provider disclosure would remain separate decisions. No canonical consent was created or inferred.

## 14. Privacy and failure behavior

Public DTOs/components/endpoints are unchanged and do not consume the private selection. Public canary tests confirm that private artifacts and assertion content remain absent. Provider-context tests confirm that internal eligibility alone does not disclose those items. Neither raw error text nor planner/provider reasoning is exported by archive discovery or candidate conversion.

Malformed records, missing/broken sources, invalid visibility, impossible/future timestamps, invalid supersession, duplicate source identities, corrupted artifacts, stale disclosure reviews, and secret-like content fail closed. Optional failures appear in the private manifest. Mandatory organism/event/constitution/revision corruption remains fatal. Unknown assertion time remains null. No historical data is repaired automatically.

## 15. Implementation and verification

New implementation:

- `core/v2/memory.ts`: validation, conversion, disclosure, source resolution, ranking, budgets and manifest.
- `server/memory-store.ts`: private read-only existing-table discovery and envelope checks.
- `tests/memory-retrieval.test.ts`: 49 regression tests.

Integration changes:

- `core/v2/contracts.ts`: typed recall hints and memory manifest.
- `core/v2/context.ts`: bounded selection and separate present/past/self/artifact serialization.
- `core/v2/cycle.ts`: archive input and internal-use marker on newly created episodes.
- `server/one-shot.ts`, `server/isolated-cycle.ts`, `server/commit-v2.ts`: archive loading and context recheck.
- `server/one-shot-spec.ts`: versioned code identity includes retrieval modules.

`source-changes.json` compares against the starting working tree rather than attributing earlier uncommitted changes to this pass. No SQL migration or public UI change was necessary.

Verification:

- Complete suite: **241 passed / 0 failed / 0 skipped**.
- TypeScript: **PASS**.
- ESLint: **PASS**.
- Next.js: **PASS**, `npm run build -- --webpack`.
- Default Turbopack: not rerun; no workaround or architecture change was made for its previously documented host limitation.
- Canonical complete-row comparison: **unchanged**.
- Frozen research and prior audit packages: **unchanged**.

Tests cover conversions, internal/provider/public distinctions, source-bound reviews, past-event and biological-provenance resolution, supersession/contradictions/cycles, artifact integrity, relevance, UTF-8/total/category bounds, empty recall, growth, fresh connection recall, context/hash binding, private canaries, malformed optional records, row-envelope mismatch, missing-row cache refusal, and absence of added execution authority. Existing safety/science/provider-mock tests remain in the full suite. No mock is presented as live provider verification.

During development, a test exposed deduplication conflating distinct contradiction relationships; it was corrected. Additional malformed-source fixtures initially hit the existing writer/append-only protections; fixture setup was corrected to respect them. No production protection was weakened.

## 16. Known limitations and deferred work

Canonical legacy recall remains blocked by missing disclosure evidence. New private episodes are usable internally but are not automatically sent to a future provider. Trusted review-input support is not a consent UI, authenticated operator workflow or production provider admission.

Recall is deterministic filtering and lexical matching. It does not infer semantic similarity, verify assertions, summarize history with an LLM, reconstruct omitted sources, or simulate biological memory. Source-projection hashes and existence checks establish recorded provenance, not truth about the external world. Strict validation may exclude legitimate older records that lack compatible metadata; review is required rather than permissive repair.

**DEFERRED TO PASS 3:** operational Life State workflows—projects, tasks, artifact lifecycle, interests, commitments, open questions, relationships and human assistance response.

**DEFERRED TO LATER PASSES:** continuous-life controller; operator UI/control and disclosure review operations; production provider; production migration installation; deployment; internet; wallet; external communications. Embeddings or summarization are not currently required and were not added.

No Decision #8, canonical V2 episode, awakening, new schedule, live provider, wallet operation, communication or biological advancement occurred. This task stops before Pass 3.

MEMORY PASS COMPLETE — READY FOR PASS 3

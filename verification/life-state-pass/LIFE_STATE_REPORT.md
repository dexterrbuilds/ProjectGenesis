# Project Genesis — Pass 3: Operational Life State

## 1. Summary

Implemented deterministic local Life State workflows and connected them to the existing V2 preparation, independent policy, fenced database commit, memory retrieval and bounded context compiler. This is computational state, not a biological capability.

The new optional, versioned `LifeStateV1.operational` extension supports projects, tasks, immutable artifact versions, interests, questions, internal commitments, minimal relationships, assistance requests/responses and current focus. Existing rows and legacy fields are not migrated or rewritten. No SQL migration was needed or applied.

| Question | Verified answer |
|---|---|
| Can Genesis create and maintain projects? | Yes, through validated local LifeChanges and fenced persistence. |
| Can projects have persistent tasks? | Yes; associations and transition rules are checked. |
| Can it produce and revise local artifacts? | Yes; database-backed logical artifacts retain immutable versions. |
| Can it retain interests and open questions? | Yes, explicitly as computational records. |
| Can it track internal commitments? | Yes; no external obligation or effect is authorized. |
| Can it remember operational relationships without inferring traits? | Yes; a restricted private record has no trust, friendship or sensitive-attribute fields. |
| Can it request assistance and ingest an attributed answer? | Yes, through local request persistence and the private intake library. No message client or operator UI is installed. |
| Can current focus survive restart? | Yes; verified through serialization and a fresh database connection. |
| Can these records inform memory/context without a live LLM? | Yes; deterministic retrieval and selection are integrated and tested. |

These answers describe implemented local mechanisms. They do not authorize canonical execution, provider disclosure, automatic continuation or external activity.

## 2. Canonical preservation

Read-only `REPEATABLE READ` audits compared every row in every canonical `genesis_*` table. Before and after digest:

`4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`

- Organism: `817e772c-827e-48fc-8e35-6504cb2a8d2d`.
- Birth: `2026-09-15T01:56:07.867Z`.
- Decisions/cycles: **7**. Canonical V2 episodes: **0**.
- Legacy memories: **7**; original project: **1**; ledger rows: **4**; milestones: **4**.
- Execution: **CLOSED**. Schedule: **DISABLED**.
- Biology: **SAVED-OBSERVATION-ONLY**; original snapshot unchanged.
- Canonical schema/migration rows unchanged. No authorization grant installed.
- Live provider calls, wallet actions and external communications during this pass: **0**.

The private full-row exports remain under `outputs/life-state-pass/`, mode 0600. This review package contains only allowlisted integrity summaries. `canonical-before.json` and `canonical-after.json` record the comparison. `preservation.json` verifies 9,319 frozen files and the completion-audit, foundation-repair and memory-pass evidence packages without changes. Frozen research, Brain Spec, neural equations and historical decisions remain intact.

## 3. LifeChange architecture

Implementation: `core/v2/operations.ts`, `core/v2/life-state.ts`, `core/v2/policy.ts`, `core/v2/cycle.ts`, `server/commit-v2.ts`.

The existing LifeChange union now admits a strict envelope:

```text
kind: operational
expectedRevision: input Life State revision
sourceIds: one or more admitted context source IDs
operation: a strict discriminated operation schema
```

Updates also bind `expectedVersion` of the target entity. Unknown operations/fields, arbitrary patches, deletion, whole-state replacement, duplicate IDs, stale versions, unknown sources and invalid ownership fail. Bounds include 120-character project titles, 1,000-character descriptions/reasons/questions, 200-character topics, 80-character relationship labels, 6,000-character artifact content and 2,000-character human answers. Source arrays are capped at 20; existing proposals permit at most 10 changes. Context uses independent UTF-8 byte limits.

Each entity records stable ID, creation/update times, version, producing event, source IDs and explicit disclosure. A pure reducer clones and validates the input before producing a new state. A failing batch does not modify its input. State revisions and database row locks protect concurrent updates.

New operations require the existing execution and local-artifact/state permission scope. Policy dry-runs the reducer outside the planner. At commit, the transaction rechecks the lease, revision, identity, permissions, context text/hash/manifest, policy, expected changes and episode payload. It recomputes the resulting Life State rather than trusting a prepared object. One-shot commits additionally bind the exact grant and its permissions. No new execution authority is created.

Legacy assertion, project-status-overlay and task-deferral operations remain compatibility paths for their original records. They cannot address the new operational entities. The original project is not silently imported into a replacement object; it remains an authoritative legacy project. New tasks may reference an explicitly supplied existing legacy project ID. Full new project lifecycle/summary operations apply to new operational projects.

## 4. Projects

Operations: `project_create`, `project_update`, `project_status`.

| Current status | Allowed next status |
|---|---|
| active | paused, completed, abandoned |
| paused | active, completed, abandoned |
| abandoned | active |
| completed | terminal |

Summary updates require an active project and matching entity version. Completion rejects unfinished associated tasks. Abandoning/resuming retains identity, creation time and all transition history; a project never silently disappears. Invalid or unchanged status transitions fail. Focus must be cleared or validly changed in the same batch when its project becomes inactive.

## 5. Tasks

Operations: `task_create`, `task_status`.

| Current status | Allowed next status |
|---|---|
| pending | active, deferred, completed, cancelled |
| active | deferred, completed, cancelled |
| deferred | pending, active, completed, cancelled |
| completed | pending, by explicit reopening |
| cancelled | pending, by explicit reopening |

Tasks have stable project association, description, due/review times, status and completion/cancellation evidence. Unknown projects, stale versions, duplicate completion, impossible transitions and silent reassignment fail. Completion/cancellation require at least one resolvable evidence ID. Deferral requires a review time. A task cannot resume under an inactive operational project. Due/review timestamps are stored facts and never schedule work.

## 6. Artifacts

Operations: `artifact_create`, `artifact_revise`.

Each artifact has one stable logical ID and an ordered immutable version list (`id:v1`, `id:v2`, etc.). Versions retain content, creation time, episode/source IDs, disclosure and an explicit predecessor. Revision changes the current-version pointer and appends a version; it never edits an older version. Associated task/project ownership is checked. A completed/cancelled associated task must be validly reopened before revision.

The existing episode-local reflection/artifact tool remains compatible. Versioned artifacts are operational Life State changes; their recorded outcome means local state was persisted, not that a filesystem or external tool ran. There is no filesystem writer or publishing action.

Recall verifies the version chain and matches content/source IDs against the producing immutable episode's typed changes. Default retrieval excludes superseded versions. An explicit version-ID query can select a historical version. Context gets metadata plus a separately bounded excerpt, never the entire version chain.

## 7. Computational interests

Operations: `interest_add`, `interest_update`, `interest_retire`.

An interest is an explicitly recorded topic relevant to computational continuity. It has active/retired status and provenance, with no biological salience, emotional strength, desire or reward field. Updates/retirement require an active record. Ordinary planner prose cannot create it. Nothing initializes a canonical interest or scripted personality.

## 8. Open questions

Operations: `question_create`, `question_status`.

Open questions can resolve or close without an answer. Resolved/closed questions can explicitly reopen. Resolution requires resolvable evidence; missing or unknown evidence fails. Past resolution remains in the immutable episode/history even after reopening. Evidence establishes an attributed record, not independently verified truth. No research tool or automatic investigation is invoked.

## 9. Internal commitments

Operations: `commitment_create`, `commitment_status`.

Purposes are restricted to local artifact completion, task review, human-input review and local constraint maintenance. Scope is fixed to `INTERNAL_COMPUTATIONAL`. Open commitments can be fulfilled, cancelled or have their review time changed; fulfilled/cancelled records are terminal. Fulfillment requires evidence. Optional task/project/relationship associations are validated.

There is no financial/legal effect type or authority. Obvious payment/contract/delegation language is additionally rejected. That lexical guard is defense in depth, not a claim that unrestricted natural language can be perfectly classified. Free text remains untrusted description; it cannot create a contract, transfer, obligation for another person or external effect. Review times have no scheduler semantics.

## 10. Relationships

Operations: `relationship_create`, `relationship_update`.

The minimal record permits an ID, bounded reference label and one of three contexts: provided input, assistance contact or project contact. Consent is explicitly unknown. There are no sensitive-attribute, friendship, affection, trust or social-ranking fields. Extra fields and obvious inferred-trait labels fail validation. No identity enrichment occurs.

Relationships are private/internal-only and excluded from provider/public disclosure. This pass intentionally does not implement consent promotion; alternate public/provider disclosure values are rejected. Context includes a relationship only when explicitly referenced or relevant to a pending assistance request/open commitment, subject to budget. No contact client exists.

## 11. Human assistance

Operations: `assistance_create`, `assistance_resolve`, `assistance_cancel`; separate intake: `server/assistance-intake.ts::recordHumanResponse`.

A typed `REQUEST_ASSISTANCE` proposal with local-state permission also creates a deterministic local request. Policy/result remain pending and no action/message is reported as performed. Arbitrary prose does not create a request.

The intake validates organism, current revision, operator scope/reference, original request episode/change hash, response identity, attribution, timestamp, relationship and bounded content. It locks the organism and Life State rows, then atomically appends an administrative input event and an untrusted response record. It marks the request answered and advances only the Life State revision. It does not add a decision or execute the answer. Competing writers at one revision cannot both win.

The original request/question remains intact. Multiple distinct responses may be recorded while pending/answered; duplicate IDs and terminal/wrong requests fail. Resolution is a later explicit LifeChange citing an actually received and context-admitted response. Cancellation is explicit. Receipt and resolution are separate.

The library is a **trusted operator boundary, not an authenticated endpoint**. The eventual caller must authenticate the operator. String attribution references alone are not authentication. This pass installs no HTTP/CLI intake, communication client or operator UI. Tests invoke it only on disposable fixture databases.

Receipt does not mean an external-message approval was granted. Historical approval intents are retained unchanged. The public status projection consults operational requests so an answered/resolved request no longer falsely reports that Genesis is waiting for an answer; unrelated approvals remain pending.

## 12. Current focus

`focus_set` supports none, intentionally idle, active project, current task or waiting for a pending assistance request. References must exist and be compatible with their status/project. Completing/cancelling a focused task without a valid focus change fails the whole batch. A received answer clears a waiting-for-that-answer focus through a separately recorded deterministic history transition. Focus persists in the database and survives restart. It never triggers execution or represents an emotion.

## 13. History and provenance

Every operational change is stored verbatim in the committed append-only episode's `lifeChanges`, with matching decision changes. The current extension also keeps compact history entries: source event, operation/target, time, source IDs, from/to versions and change hash. Full snapshots are not appended per change. Artifact versions and human responses are separately retained inside the extension and in their producing episode/input.

A reducer-produced history entry points to the original immutable record containing its reason, evidence and payload. Commit rejects fabricated history or a prepared Life State that differs from reduction. Intake rejects a request whose original creation evidence is missing or inconsistent. No historical rows are repaired.

Mutable entity IDs are relevance/target keys, **not immutable evidence for a semantic assertion**. New assertions about an operational record must cite its source episode/input or an immutable artifact version. Context exposes the source-event ID; the reducer refuses a mutable entity as assertion provenance. A regression test verifies that editing a project does not silently retarget an existing belief's provenance.

## 14. Memory integration

Pass 2's retrieval boundary remains deterministic and LLM-independent. Stored validated operations add structured references for projects, tasks, artifacts, interests, questions, commitments, relationships and assistance. Status changes and revisions recover stable project/task associations, so a task/project query can recall earlier work even when the proposal-level association was null.

Attributed human answers are separate, untrusted past-input candidates with respondent and original-request provenance. A query referring to a request/answer can retrieve the original request and its relevant episode. Answers are not current observations, verified facts or instructions. Operator authorization evidence is excluded from archive projection.

Versioned artifacts prefer the current version, with explicit historical access. Semantic assertions resolve immutable recorded sources independently of whether those episodes' text was otherwise selected. Broken sources/content chains fail closed. No embeddings, external service, semantic similarity claim or LLM summarization was added. The seven canonical legacy memories remain unchanged and retain Pass 2's disclosure exclusion; this pass grants no new consent.

## 15. Bounded context

`core/v2/operational-context.ts` supplies a separate computational Life State view. It includes bounded active/reference-relevant projects/tasks/questions/commitments/interests, pending/answered assistance, relevant relationship metadata, artifact metadata and focus. It does not serialize the whole extension, history or responses.

Ordering is explicit: current focus, direct/associated structured references, then active records; stable ID breaks ties. The operational view is limited to **2,800 UTF-8 bytes and 12 items**. The existing full-context ceiling remains **12,000 UTF-8 bytes** and memory retains its independent **4,500-byte** budget/category limits. Whole items are dropped, with their IDs/reasons recorded in the private manifest. Unfittable current focus fails closed. Legacy task/commitment views are capped at ten each with omissions recorded. A dropped active task/commitment is never silently omitted from the private manifest.

Selected state metadata includes update time, entity version, source event and source IDs. Remembered experiences, current Life State, semantic beliefs and artifact excerpts remain separate. Instructions mark descriptions/answers as untrusted data. Context text/hash and selection manifest are rebound at commit. Credential-like descriptions are excluded; a required focused item that cannot safely fit is refused.

Internal, public and provider disclosure remain distinct. New operational records are internal-only. Consequently a future provider context omits them and records that omission until separately reviewed disclosure support exists. This pass does not silently make private relationships or answers available to a paid provider.

## 16. Independent policy and authority

Policy and reducer enforce permissions, ownership, transition graphs, source existence, expected revision/version, immutable history, explicit typed operations and private disclosure outside the planner. Malformed proposals become failed/denied preparation outcomes rather than arbitrary writes. Commit revalidates all prepared data under the database fence.

One-shot runtime identity is now `runtime-v1-oneshot-1.0.3`, with the added modules included in code hashing. Future authorization must bind the new code identity. The first-awakening mode itself remains NOT AUTHORIZED. The one-shot Decision 8 fence remains intact; fixture tests verify consumption and refusal of a second claim. There is no Decision 9 authority, recurring worker, automatic wake, queue or event consumer.

## 17. Privacy and public projection

Public DTO allowlists do not expose the new entities, private descriptions, answers, relationships, raw changes, approval/operator evidence or context. No frontend redesign or new public endpoint was added. Existing project counts continue to describe the legacy public projection; private operational projects are not silently added to it. The only public-state integration changes assistance waiting metadata, without exposing contents.

Canary tests cover relationship labels, answers and revised artifact content. Provider-context tests verify that private/internal eligibility does not become provider disclosure. Retrieved material includes neither raw planner/provider output nor hidden reasoning. Existing bounded rationale remains separate. No new secret or credential handling path was introduced.

## 18. Growth, conflicts and restart

Synthetic fixtures cover multiple projects, up to 300 tasks, artifact revision chains, open/closed questions, fulfilled/cancelled commitments, private relationships, pending/resolved assistance and focus. `growth.json` contains timings and sizes from the local diagnostic; it is not a production throughput claim.

The representative probe uses five projects, twenty artifact versions, twenty questions, twenty commitments, five relationships and five pending assistance requests at each task scale. Selection remains deterministic and within its byte/item budgets. Omitted records remain explicit. Tests verify revision conflict, two workers racing, duplicate commit refusal, two competing answer writers and an answer invalidating an already prepared stale cycle.

Fresh database connections recover actual committed operational state, current focus and artifact recall. The current snapshot plus append-only episodes/inputs provide restart persistence and audit history; a disaster-recovery event-rebuild utility is not implemented here.


| Tasks | JSON state bytes | Full context bytes | Operational bytes | Selected / omitted | Context selection ms |
|---:|---:|---:|---:|---:|---:|
| 20 | 74,141 | 6,926 | 2,789 | 9 / 67 | 31.9 |
| 100 | 128,518 | 6,934 | 2,797 | 9 / 147 | 18.1 |
| 300 | 264,918 | 6,934 | 2,797 | 9 / 347 | 30.3 |

Storage still grows: the JSON extension, compact history, artifact versions, responses and episodic references are read/copied/rewritten with state updates. The archive still has Pass 2's explicit 10,000-record discovery limit. Bounded context does not make storage or all-history scans constant-cost. Normalizing/indexing larger stores and retention/recovery policy remain future engineering work. No production-scale claim follows from these fixtures.

## 19. Tests and build

- Previous suite retained: **241 tests**.
- New meaningful regressions: **85 tests** in `tests/life-state.test.ts`.
- Complete dedicated-test-database suite: **326 passed / 0 failed / 0 skipped**.
- TypeScript: **PASS**.
- ESLint: **PASS**.
- Next.js production build: **PASS**, verified Webpack route (`npm run build -- --webpack`).

The full suite uses dedicated disposable schemas and sanitized fixtures, with no canonical credentials in test processes. Pure-only developmental runs intentionally skipped DB tests; the reported final suite did not skip them. The initial sandbox attempt could not connect to localhost Postgres; the authorized local-database rerun succeeded. No production protections were weakened to satisfy tests.

New coverage includes all lifecycle transitions and rejection cases, source/version ownership, immutable artifact recall, current/historical selection, semantic provenance stability, human-input validation and separate resolution, deterministic bounded context, growth, privacy, no biological reinterpretation, stale/concurrent writes, forged prepared-state/manifest/history refusal, restart and unchanged one-shot authority. Existing provider tests use mocks/injected transports; no live provider verification is claimed.

## 20. Files changed and limitations

New implementation:

- `core/v2/operations.ts`: strict schemas, transition graphs, pure reducer and attributed-input reduction.
- `core/v2/operational-context.ts`: bounded operational selection and omission manifest.
- `server/assistance-intake.ts`: scoped, transactional private input intake.
- `tests/life-state.test.ts`: workflow and integration regressions.

Modified integration points: contracts, reducer, context, policy, cycle preparation, retrieval, archive projection, commit revalidation, one-shot code identity and read-only assistance-status projection. `source-changes.json` compares against this pass's starting working tree so prior uncommitted work is not attributed to this pass. No code or history was deleted. No schema, research, constitution, biological-model, scheduler, provider transport, wallet or frontend component was changed.

Operational text is bounded and untrusted, not semantically verified. A source ID proves recorded provenance, not the truth of a claim or validity of a human instruction. The restricted relationship/commitment schemas deliberately omit richer social and obligation behavior. Consent elevation and authenticated operator endpoints remain unavailable. Legacy projects remain legacy records; they are not silently rewritten as operational projects. Private-state growth and full recovery tooling remain limitations described above.

## 21. Deferred work and stop

**PASS 4 — continuous life/event loop:** event intake/queue, continuation authority, wake/defer/idle orchestration, bounded recurring execution, Decision 9+ architecture, crash/restart continuation, budgets/backoff. None is implemented or enabled by this pass.

**Later:** operator control UI/authenticated intake, disclosure review/promotion, production provider, production migration installation, deployment, internet, wallet, external communications. No live LLM, scheduler, external effect or biological advancement was added.

Canonical Genesis remains at seven decisions, execution CLOSED, schedule DISABLED, SAVED-OBSERVATION-ONLY biology and zero canonical V2 episodes. No awakening occurred. Stop for review.

LIFE STATE PASS COMPLETE — READY FOR PASS 4

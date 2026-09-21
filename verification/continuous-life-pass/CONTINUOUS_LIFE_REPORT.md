# Project Genesis — Pass 4: Continuous Life & Event Loop

## 1. Summary

Implemented a **local computational-life controller**, backed by PostgreSQL, which can process durable events into repeated V2 cycles under a separate, bounded, revocable authority. It reuses the existing context compiler, memory retrieval, PlannerV2 validation, independent policy, deterministic Life State reducer, intent contract and atomic commit. No new reasoning architecture or biological capability was introduced.

The implementation is exercised only in disposable fixture schemas. Canonical Genesis is dormant. There is no production worker entrypoint, installed continuous schema, canonical continuous authority, live provider or external dispatcher.

| Question | Verified answer |
|---|---|
| Can isolated Genesis continue from Decision 8 to 9, 10, 11…? | Yes. The long-run fixture committed 8–107. |
| Can it remain idle without generating decisions? | Yes. Empty/ineligible queues do not invoke the planner or modify organism state. |
| Can deferred work wake later? | Yes. Typed deferrals and task/commitment review times create durable, due-time-gated events. |
| Can a human answer wake it without polling an LLM? | Yes. Explicit private response intake can enqueue one attributed response event atomically. Separate active authority is still necessary. |
| Can projects/tasks/artifacts continue across cycles? | Yes. Tested creation, later recall, task completion and immutable artifact revisions across fresh controllers. |
| Can two workers avoid duplicate local life cycles? | Yes. Transactional organism/claim locks, leases, revisions and unique identities prevent duplicate local commits. |
| Can it recover safely after crashes? | Yes within the local transaction model; expired local attempts can be retried within limits. Unknown provider outcomes stop for review. |
| Can continuous authority be revoked? | Yes. New claims and stale commits are refused; pending work remains inspectable. |
| Can runaway continuation be bounded? | Yes. Depth, root burst, follow-up, attempt and scope/window limits are enforced outside the planner. |
| Does any of this activate canonical Genesis? | No. Nothing was installed, authorized or started there. |

## 2. Canonical preservation

Read-only repeatable-read exports, including all canonical `genesis_*` rows, were compared before and after implementation/testing. Raw exports remain private under `outputs/continuous-life-pass/`; they are not public DTOs or included in this report package.

- Organism: `817e772c-827e-48fc-8e35-6504cb2a8d2d`.
- Birth: `2026-09-15T01:56:07.867Z`.
- Decisions: **7**; original legacy memories: **7**; original project: **1**.
- Original ledger and milestones: **4 rows each**, unchanged; original saved brain and all other canonical rows unchanged.
- Canonical V2 episodes: **0**. The one existing administrative Life State event remains administrative.
- Execution **CLOSED**, schedule **DISABLED**, biology **SAVED-OBSERVATION-ONLY**.
- Continuous tables installed: **none**; continuous authority: **none**.
- Canonical planner/provider calls, wallet actions, external communications and neural advancement during this pass: **0**.

Before and final row digest:

`4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`

[Preservation evidence](preservation.json) also checks **9,319 frozen research files** and the manifests of the completion audit and Passes 1–3. No mismatch was found. No frozen research, Brain Spec, C. elegans equations or historical rows were modified.

## 3. Continuous authority model

`server/continuous-spec.ts` defines strict, versioned `CONTINUOUS_LOCAL_V1`. The scope pins organism, source/runtime identity, Node/platform/architecture, constitution, policy, permission hash, exact operator-selected local planner identity, event/effect allowlists, saved-only biology, issuer/reference, issuance/expiry, scheduling permission and resource/loop limits. Provider and model are explicitly null. Unknown fields and external effects are rejected.

States: `PROPOSED → AUTHORIZED → REVOKED / EXPIRED / REVIEW_REQUIRED`, with pre-authorization revocation/expiry also structurally allowed. Expiry is enforced by time at every claim/commit; a status label need not first be rewritten to EXPIRED. Payload identity is immutable. Authorization requires an exact payload hash and matching issuer/evidence reference.

These are private trusted-operator library functions, **not an authentication system**. No endpoint can authorize a scope. Authentication and production role separation remain deferred. Fixtures issue explicit test-only scopes; no canonical scope was issued. Non-fixture scopes require at least eight prior decisions. The fixture exception is restricted to fixture organism identities, which must also match the stored owner.

## 4. Event model

`core/v2/continuous.ts` validates immutable private envelopes and discriminated payloads. Each event has version, stable ID, organism, timestamps, expiry, dedup key, source/reference, disclosure, parent event/cycle, root and depth. State/attempt/lease metadata is held separately in SQL.

Supported kinds: `MANUAL_EVENT`, `TIME_WAKE`, `CONTINUATION`, `TASK_REVIEW_DUE`, `COMMITMENT_REVIEW_DUE`, `PROJECT_REVIEW`, `ASSISTANCE_REVIEW`, `QUESTION_REVIEW`, `HUMAN_RESPONSE_RECEIVED`, `SYSTEM_RECOVERY`.

Manual text is bounded to 1,000 characters and at most ten references. Targets and versions are explicit. Events contain no tool permissions or biological input. Human answers are referenced through their existing attributed records, not copied into a public queue payload. All current events have internal use permitted, public/provider disclosure forbidden. `SYSTEM_RECOVERY` is a supported private schema shape, not an automatic event generator or an operator-injectable authority.

## 5. Queue

`server/continuous.ts` provides typed intake, transactional claiming, cancellation and recovery. `runtime/continuous-schema.sql` supplies durable envelopes, dedup uniqueness, partial due index, scope/attempt indexes, FKs, transition guards and an immutable journal.

Transitions:

- PENDING → CLAIMED / CANCELLED / EXPIRED / FAILED.
- CLAIMED → CONSUMED / CANCELLED / FAILED / AMBIGUOUS.
- CLAIMED → PENDING only through explicit bounded local recovery, with later availability and a new attempt identity.
- Terminal events cannot be re-consumed or silently reset.

Claims serialize against the existing organism and Life State rows. Eligible events are ordered by persisted availability then ID. At most 100 due candidates are examined per tick; invalidated candidates can be discarded without reasoning. Foreign event ownership, changed duplicate payloads and immutable-envelope modifications fail.

## 6. Event → cycle path

`ContinuousWorker.tick` checks enablement/cancellation, recovers eligible expired local claims, validates scope, claims one event, prepares through `prepareCycle`, independently revalidates and commits, then releases.

The context contains the current typed event, time, Life State, selected historical memory, scope and permission identity, resource snapshot, allowed local effects and a NOT_APPLIED saved-only biological observation. `server/commit-v2.ts` re-reads the archive/state and recompiles the exact context, verifies policy and deterministic reducer output, and checks scope/lease/revisions again. Preparation alone is never authority.

The active-cycle and one-shot paths share these lower-level checks. Continuous cycle/fence types are explicit; mixed one-shot/continuous fences are rejected.

## 7. Decision numbering

The count and maximum persisted decision number must both match the organism count. A commit allocates exactly the next number inside the locked transaction. Fixture numbering 8→9→10 and 8–107 passed.

The one-shot path remains fenced to seven prior decisions and exactly Decision 8. Its original SQL branch is retained verbatim within the new writer function and tested after installing the continuous schema in a disposable fixture. It cannot issue Decision 9 or masquerade as a continuous scope.

## 8. Outcome → future event

Only validated structured outputs create follow-ups:

- `DEFER` creates a TIME_WAKE at `deferUntil`.
- A PROPOSAL may contain one strict `followUp` for continuation or target review.
- Accepted task creation with a due time or task deferral creates a version-bound task review.
- Accepted commitment creation/update with review time creates a commitment review.
- Assistance requests persist and wait; they do not create a recurring poll event.

The bridge first evaluates the post-reducer Life State. Unknown/obsolete targets, unauthorized wake kinds, excessive children/depth and invalid timing are refused by policy. Denied and failed proposals create no follow-up. ABSTAIN and ordinary completion may create none. Free-form prose cannot schedule work.

## 9. Time/wake semantics

Availability and expiry are compared to wall time; created/available timestamps retain provenance. Recovery's next-eligible time is separate SQL metadata, preserving the original envelope. A cheap queue poll is not a reasoning heartbeat. No due event means no reasoning. Review time is computational bookkeeping, with no claim of biological urgency or sleep.

The existing legacy/canonical scheduler stays disabled. This prepared worker is a separate event poller and cannot enable that schedule. Test timings and ceilings are fixture values, not proposed production policy.

## 10. Idle behavior

With no eligible event, ticks return `IDLE_OR_BUDGET_BLOCKED` without planner calls, decisions, episodes or organism mutations. Tests compare the stored organism before/after repeated idle ticks. The worker loop uses a bounded abortable timer, rather than a busy spin. Focus, active projects and unresolved tasks do not themselves create events.

The combined internal result intentionally requires private queue/resource inspection to distinguish empty, future-due and budget-blocked conditions. The public projection does not invent ongoing thought in any of these cases.

## 11. Defer behavior

Tests verify a committed defer produces exactly one wake, refuses early execution and later proceeds. Repeated deferral is stopped by the declared continuation-depth limit, yielding a denied outcome with no further wake. A task-status deferral has its own version-bound TASK_REVIEW_DUE; it is not confused with the proposal-level DEFER.

An underlying completed/cancelled/version-changed task invalidates its review before planning. Project-associated continuations require an active operational project; missing operational targets are not inferred from historical prose or silently migrated legacy projects.

## 12. Human-response wake

`recordHumanResponse` retains Pass 3's attribution, request provenance, revision, untrusted-input and disclosure checks. The optional explicit `wake: ENQUEUE_IF_INSTALLED` flag adds a response event **in the same transaction** as the response receipt and Life State update. Missing schema rolls everything back; it is never installed automatically.

One response identity produces one event. A duplicate receipt fails without duplicating its event. Distinct identities remain distinct even with identical text. A revoked scope cannot process those pending events. Cancellation before response rejects intake; cancellation after intake causes the response event to be discarded before planning.

The request→idle→answer→wake→source-bound resolution integration test also proves the original episode/answer can be recalled privately. Answers neither directly execute tools nor become verified facts. There is no message client or external delivery.

## 13. Project/task continuation

Tests exercise project/task creation, delayed review, retrieval of the creating episode, later completion, and returning to idle. Another test uses a fresh controller/connection to recall artifact v1 and persist v2 while retaining v1. The long-run fixture retains one neutral project and task over 100 cycles and eleven artifact versions.

These are test planners, not scripted canonical interests, projects or personality. Pass 3's ownership, transition, history and immutable revision checks remain authoritative.

## 14. Focus

Current focus continues to prioritize bounded operational context. Setting focus creates no recurring authority. Completing a focused task requires a valid focus change; the integrated test completes the task and becomes intentionally idle. The worker never polls a planner simply because focus exists.

## 15. Resource budgets

Scopes specify total claims, claims per rolling window, concurrency, per-cycle/window cost ceilings, planner timeout, lease and maximum attempts. **Claims**, including failed/recovered attempts, consume cycle budget. Scope counters, window counters, active claims, failures, ambiguities, reservations and recorded costs are inspectable through the resource projection.

Existing provider ledger records are inspected for unresolved liability across all ages, including older windows/scopes. Unknown/reserved/dispatching attempts block new work; malformed cost/liability data requires review rather than being interpreted as zero. Tests retain a two-day-old unresolved reservation and reject work over a recorded cost ceiling.

This release admits only zero-cost local planners. A nonzero proposed charge is a failed preparation, with no payment or fallback. Positive cost fields are caps, not provider authorization. A future paid provider requires separate admission and durable dispatch/reservation integration; these tests do not establish that integration.

## 16. Failure/backoff

- Planner/validation failure or timeout: one failed local outcome, no implicit fallback or follow-up.
- Policy/reducer rejection: denied result, no unauthorized state change or future event.
- Cancellation/revocation: close local claim; no stale commit.
- Expired/stale local claim: deterministic bounded retry with `backoffMs × attempt`, subject to scope and attempt limits.
- Database failure: transaction rollback; a failed phase persistence aborts preparation, even if policy had already allowed an effect. A closure failure leaves durable evidence for later lease recovery rather than fabricating a commit.
- Unknown provider execution: AMBIGUOUS event/attempt and REVIEW_REQUIRED scope; retained liability; no retry.
- Resource exhaustion: no claim/planner call. Pending work remains pending.

Repeated expired local claims terminally fail when their attempt budget is exhausted. Errors are retained privately. No failure branch silently enables execution or changes an authority hash.

## 17. Crash/restart

Fault-injection tests cover before claim, after claim, before/after planner, before/after policy, before commit, before/after follow-up creation and after commit. Fresh Node processes additionally exit at after-claim, before-follow-up, after-follow-up and after-commit checkpoints; they use only the sanitized test database configuration.

The follow-up checkpoints use an actual proposed child event. Before commit, disconnect rolls back decision, Life State and child creation; after commit, all are present exactly once. Recovery does not duplicate an already-consumed source or child. Fresh controller connections preserve artifacts, revocation and history. Stale revisions, stale leases, two-worker races and a mid-cycle revocation all refuse invalid commits.

This verifies application/process failure and PostgreSQL transaction behavior locally. It does not substitute for production database failover, backup restore, role or network-partition testing.

## 18. Processing guarantees

The local commit transaction includes decision, episode, intent, Life State, source-event consumption, child events and attempt/journal status. Unique IDs, dedup keys, committed-event uniqueness, locking and commit fences provide **at most one committed local cycle per source event**. Planning may happen again after a rolled-back attempt; it is not claimed to run exactly once.

No universal exactly-once guarantee is made. External calls, payments, messages and nontransactional filesystem effects are absent. Future support would require separate receipt/idempotency/reconciliation mechanisms. Unknown external outcomes cannot be reclassified as success or failure by this worker.

## 19. Worker

`server/continuous-worker.ts` is a disabled-by-default library abstraction. `tick()` processes at most one event; `run()` adds cheap bounded polling and abortable shutdown. There is no environment-selected planner, daemon start, cron, generic unlock or default recurring decision.

The caller supplies an admitted identity and trusted local planner implementation. In-process trusted code is not a sandbox: authorization of a label alone must never permit loading arbitrary operator-unreviewed code. No public input can supply an implementation. Production supervision/entrypoint and authenticated activation remain unimplemented deliberately.

## 20. Revocation

Revocation transactionally closes active local claims and records private operator evidence. Every subsequent claim/prepare/commit revalidates scope. Stale workers cannot commit. Pending events remain inspectable. Revocation survives a fresh controller. Where provider execution is unresolved, the record stays REVIEW_REQUIRED rather than being reopened or retried.

The global execution lock remains CLOSED even while a fixture holds narrow scoped authority. Setting generic OPEN does not authorize the continuous path; it makes that path fail.

## 21. Deduplication

Operator intake requires an identical envelope for an existing ID/dedup key. Changed payloads are rejected, not merged. Follow-up IDs derive from producing cycle, typed payload, time and operation identity. Equivalent explicit/derived children within a cycle are collapsed before insertion. Human response IDs derive from organism and response identity.

One source event cannot commit twice. Retried rolled-back attempts cannot leave committed children. Different user events/answers are not deduplicated merely by similar text. A buggy planner creating different new logical tasks is constrained by scope/chain budgets, not claimed to be semantically deduplicated.

## 22. Obsolescence

Claim-time checks cancel reviews for missing targets, changed versions, terminal targets or inactive parent projects. Response events require the still-eligible request, recorded response association and input-event identity. Tests cover completed tasks, cancelled commitments, abandoned projects, resolved questions and cancelled assistance.

Cancellation and expiry require no decision just to discard stale work. Versions are conservative: even a changed-but-still-active target can invalidate an old review; a new valid review must be explicitly recorded. Corrupt envelopes fail closed and require private inspection rather than being silently repaired.

## 23. Loop prevention

Independent protections include maximum child count, scheduling/event-kind permission, minimum follow-up delay, continuation depth, recent attempts per root, attempts per event, total scope claims and rolling-window claims. Root rate uses the scope's explicit backoff interval as its burst window. Depth does not reset when a child is delayed.

Tests intentionally request endless immediate continuations and repeated deferrals. They terminate at the configured limits. ABSTAIN remains a valid no-follow-up outcome; a project or question does not defeat idle. There is no hidden personality-based reason to generate another event.

## 24. Memory/context behavior

The Pass 2/3 retrieval, source resolution, disclosure separation and operational context budgets remain in use. Structured task/project/request references drive selection; neither the full queue nor accumulated prior prompts are inserted into a new context. Scope resource metadata is a bounded claim-time snapshot, binding later preparation/commit consistently.

The actual 100-cycle run stayed below the existing **12,000 UTF-8-byte** context ceiling. Whole optional items can be dropped with private manifest reasons; mandatory context overflow fails safely. Prior artifact content remained available at cycle 100. Existing deterministic 10/100/1,000-episode synthetic history tests also passed, including direct retrieval of the oldest referenced event over recent irrelevant history. These are not 1,000 continuously executed database cycles.

Storage remains append-only and grows. The current Life State JSON keeps references/history and artifact versions; the archive reader scans at most 10,001 rows per category to detect its 10,000-row cutoff. Above that cutoff discovery is explicitly incomplete. Indexing/archival and normalized history remain later scaling work, not solved by keeping the prompt bounded.

## 25. Observer projection

`server/observation-read.ts` now recognizes a current authorized continuous lease alongside one-shot leases. It reports real planning as REASONING, completed quiet state as IDLE, pending assistance as AWAITING_ASSISTANCE and orphaned/expired/ambiguous activity as REVIEW_REQUIRED. Canonical Genesis remains DORMANT.

No frontend redesign or extra public payload is added. Existing `publicState`/`publicDecision` allowlists remain authoritative. Tests use private event and human-answer canaries; none appears in the public projection. Queue records, scope evidence, raw planner text, relationship details and answers remain private. Saved biology stays historical/NOT_APPLIED; ordinary computational cycles do not generate neural firing frames.

## 26. Database/schema

Prepared SQL adds:

- `genesis_continuous_scopes`
- `genesis_runtime_events`
- `genesis_continuous_attempts`
- `genesis_continuous_journal`

Scope/event identities have immutable guards; the journal is append-only. FKs bind the original singleton organism, attempts, scopes and events. The shared writer function requires either the existing one-shot fence or the distinct continuous fence, never a generic OPEN fallback. The canonical migration table still has its original three entries.

[Future installation path](../../runtime/CONTINUOUS_INSTALLATION.md) documents required ordering, isolated restore testing, hashes, separate structural authorization, backups, role separation and later worker admission. The only automatic installer refuses non-test databases/schemas. Production SQL is **PREPARED / UNAPPLIED**. Database owner fixture tests do not prove production least-privilege isolation.

## 27. First-awakening compatibility

`GENESIS_FIRST_AWAKENING_V1`, its maximum one cycle and expected seven decisions are unchanged. The single-use SQL branch has an explicit verbatim regression check. Running the one-shot controller after installing the new schema still creates only fixture Decision 8, consumes the grant, and refuses a second cycle.

The runtime source identity is versioned to `runtime-v1-oneshot-1.0.4` because shared implementation dependencies changed. This does not authorize or renew any grant. Existing reviewed mode/configuration files were not rewritten. Any future grant must pin the then-reviewed exact runtime identity. Production continuous authority requires prior first awakening and separate review/authorization.

## 28. Security

No public route was added or opened. No API/CLI/runtime bootstrap starts the new worker or authorizes scopes. Strict schemas reject extra permission fields, unknown event/operation types, wrong owners and changed payloads. Commit revalidates policy, state revision, scope and context rather than trusting prepared JSON. Planner output cannot grant tools, change scope, bypass cost ceilings or install an external executor.

Human input and memory remain untrusted. Scope/evidence identifiers are private. Authorization/revocation/intake libraries require a future authenticated operator caller; strings alone are not credentials. Current local planner callbacks are trusted repository code. Production DB ownership/roles, audit-log retention and operational control UI remain explicit prerequisites, not fixture-proven capabilities.

## 29. Long-run simulation

This is a deterministic local fixture exercise, **not canonical Genesis, a biological simulation, or a production throughput benchmark**. Ten independent neutral roots each process ten cycles, with explicit children, one maintained project/task, eleven immutable artifact versions, idle ticks between roots, and one final over-budget pending event. No model chose a canonical project or objective.

Exact measurements are in [long-run.json](long-run.json). They include committed decisions/events, duplicate checks, average/max context bytes, Life State size, private archive/decision/event row sizes, timing, depth and budget counts. Row-size sums exclude indexes/table overhead; decision storage includes the seven fixture historical decisions.

| Measurement | Result |
|---|---:|
| New decisions / final fixture decision count | 100 / 107 |
| Events created / consumed / budget-blocked pending | 101 / 100 / 1 |
| Duplicate events / decisions | 0 / 0 |
| Average context bytes | 10897.45 |
| Maximum context bytes | 11143 |
| Life State JSON bytes | 35561 |
| Archive JSON bytes, final total | 218703 |
| Event row bytes, final total | 123208 |
| Decision row bytes, including historical seven | 1746737 |
| Artifact versions | 11 |
| Idle ticks without decisions | 10 |
| Largest continuation depth | 9 |
| Rejected duplicate enqueue attempts | 10 |
| Failed / ambiguous attempts / recoveries in this workload | 0 / 0 / 0 |
| Elapsed seconds | 13.053 |

The run had zero duplicate events/decisions, zero failed/ambiguous attempts, zero provider cost and no biological or external execution. Four fresh-process crash tests and the in-process failure suite separately cover recovery; the successful 100-cycle workload itself injects no crash.

## 30. Tests/build

See [checks.json](checks.json), [full-tests.txt](full-tests.txt), [typecheck.txt](typecheck.txt), [lint.txt](lint.txt), and [build.txt](build.txt).

- Full suite: **387 passed, 0 failed, 0 skipped**, retaining all 326 prior tests plus 61 continuous-life regressions.
- TypeScript: passed after the completed build. An overlapping typecheck initially raced Next.js regeneration of `.next/types`; the preserved diagnostic is [typecheck-build-overlap.txt](typecheck-build-overlap.txt). The check was rerun serially without changing source or configuration.
- ESLint: passed, no warnings/errors in final run.
- Next.js production build: passed through the verified `--webpack` route. Node emits an existing `module.register()` deprecation warning; no architecture was changed to suppress it. Turbopack was not used.
- Tests use `TEST_DATABASE_URL` and disposable `awakening_test_*` schemas. Fresh-process fixtures receive a restricted environment without canonical database configuration. Cleanup drops only their disposable schemas.

New regression coverage includes schema/authority identity, two-worker races, stale revisions/leases, expiry/revocation, disabled boot, one-shot compatibility, due order/expiry/cancel, typed task/commitment reviews, direct defer, human wake/resolve/cancel, project/artifact continuity, costs/liabilities, malicious continuation, graceful idle shutdown, all requested crash checkpoints, four fresh-process exits, phase-persistence database failure, public canaries and the 100-cycle workload.

During development, invalid test operation names and an expiry-test wait were corrected to exercise the existing strict contracts; validation was not relaxed. Initial SQL development errors (reserved identifier and trigger-record field access) were corrected before successful fixture execution. A final failure review added abort-on-phase-persistence-error so an already-allowed local effect cannot commit after a database phase error. The complete suite was rerun after that change.

Exact implementation additions and before/after hashes are in [source-changes.json](source-changes.json). Existing repository changes predating this pass were retained. Main modified shared paths: contracts/context/planner/policy/cycle; common commit; assistance intake; observation projection; runtime identity. Added paths: continuous contracts, scope/authority/controller/worker, prepared SQL/installation notes and fixture/crash/long-run tests. No package dependency was added.

## 31. Known limitations

1. This is a prepared local library implementation, not an installed production service. No canonical authority, boot worker, production admission or authenticated control surface exists.
2. Only trusted injected zero-cost local planning is admitted. A real provider, durable paid dispatch and external effects require later independent work. Timed-out local promises cannot be forcibly killed by JavaScript; fences prevent them from committing, and they receive no tool authority.
3. Database role isolation, failover, backups and operational supervision need target-host testing. Test schemas use database-owner credentials, and trigger protections are not a defense against a malicious owner.
4. PostgreSQL commits are atomic locally; process planning may repeat after rollback. External exactly-once semantics are not provided or claimed.
5. State/history/archive storage grows; bounded context does not make storage or retrieval scans constant cost. No retention/compaction service was added.
6. There is no automatic backlog migration of already-existing review timestamps. New accepted operations or explicit attributed events create wakes. Conservative target-version cancellation can discard stale reviews; it never silently reconstructs them.
7. Corrupt queue/authority/ledger data fails closed. Operator reconciliation and reissuance workflows are deliberately deferred. Ambiguous liabilities are never silently cleared.
8. Fixture planners and measured wall times establish local execution behavior, not useful autonomous judgment, biological decision-making, a production load SLA or an appropriate final production budget.

## 32. Deferred work

No automatic next pass or activation follows this report. Remaining categories require separate review:

- authenticated operator/control surface and private inspection/reconciliation;
- disclosure review workflow;
- production provider selection, integration, admission and secrets;
- production structural migrations, role installation and restore verification;
- target deployment, supervision, recovery drills and monitoring;
- first-awakening integrity, one-shot authorization and Decision 8 review;
- later separate bounded continuous authority;
- optional future internet, wallet/economic actions and communications.

Canonical final state: **7 decisions; 0 V2 episodes; execution CLOSED; schedule DISABLED; saved-only biology; no continuous authority; no live provider calls, wallet actions or external communications.**

CONTINUOUS LIFE PASS COMPLETE — READY FOR NEXT REVIEW

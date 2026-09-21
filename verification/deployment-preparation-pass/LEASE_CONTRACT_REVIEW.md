# Project Genesis — Lease Contract Review

Date: 2026-09-21. Scope: design/contract review only.

**Recommendation:** a continuous lease grants time-limited eligibility to admit one atomic local commit. Ownership becomes usable only after durable claim publication. A final fence must check current database time and all authority bindings under the locks that exclude another owner. A transaction admitted before expiry may finish after expiry while retaining those locks. Expiry before admission refuses the commit; it never becomes success merely because the work was legitimate.

This is a proposed normative contract for review, not a claim that the implementation already enforces every part. It requires narrow implementation and test changes. No code, tests, SQL, timing values, deployment configuration or previous reports were changed in this review. No tests, workers, provider requests or database commands were run. Canonical Genesis was not accessed. No authority is created by this document.

## 1. Existing behavior

Inspected executable sources:

| Boundary | Implementation and present behavior |
|---|---|
| Worker | [ContinuousWorker.tick](../../server/continuous-worker.ts): `before_claim` hook, recovery, claim, prepare, commit, closure. The hook precedes both recovery and claim. |
| Claim | [ContinuousController.claim/base/tx](../../server/continuous.ts): organism and Life State row locks, scope/event validation, resource checks, new attempt identity and random lease token. Event and organism deadlines use `now() + leaseMs`. The returned fence becomes available after transaction COMMIT. |
| Authority | [continuousState/assertContinuousClaim](../../server/continuous-authority.ts): exact scope, event, attempt, token and revision checks; schedule disabled and execution CLOSED; event lease compared with process `Date.now()`. |
| Preparation | `ContinuousController.prepare/check/phase`: repeated ownership checks, saved-observation/context construction, bounded local planner, policy and reducer. Planner timeout is distinct from the cycle lease. |
| Commit | [commitV2](../../server/commit-v2.ts), called inside `ContinuousController.commit`: locked identity/revision/lease checks, context/disclosure reconstruction, policy and reducer verification, then local journal/decision/episode/Life State writes. Event consumption and follow-ups share the outer transaction. |
| SQL writer | [continuous-schema.sql](../../runtime/continuous-schema.sql), `genesis_require_v2_writer`: exact continuous bindings and scope/decision guards; deadline comparisons use transaction-start `now()`. The one-shot branch remains separate. |
| Recovery | `ContinuousController.recover/close`: expired claimed local work can be closed and requeued within existing limits; a subsequent claim gets a different attempt/token. Unknown provider liability blocks automatic retry. |

The deadline currently starts at the claim transaction's start timestamp. Connection acquisition and the preceding recovery transaction are outside it; waits and validation after BEGIN are inside it. In Pass 7.1, 13–27 ms elapsed between transaction start and the lease write.

`commitV2` checks the continuous event deadline near its entry. It subsequently reads memory/disclosure and validates context, policy and reducer output. There is no final current-database-clock check after that work immediately before the local-effect writes. The SQL decision trigger compares against the commit transaction's frozen `now()`, not time at the insert. Neither physical COMMIT completion nor acknowledgement is tested against a fresh deadline.

**Observed failure, not a newly reproduced result:** [Pass 7.1](SHORT_LEASE_RECOVERY_REPORT.md) recorded 45/50 commits and 5/50 expiries with unchanged 250 ms / 100 ms limits. In the detailed rejection, both process and database wall time were 7 ms beyond the event deadline; transaction-start time was still before it. The refusal was justified. The before-claim crash left PENDING, attempts=0, no cycle/attempt/lease, and the next claim was fresh. No recovery or inherited-timer defect was demonstrated.

These findings do not demonstrate a duplicate commit or an unauthorized takeover. The proposed changes below settle timing semantics that the existing contract did not specify; they are not a retrospective diagnosis of a new Pass-7 defect.

## 2. Historical contract

Reports are historical evidence; the source above establishes current behavior.

| Authority/history | Documented invariant | Detail or unresolved choice |
|---|---|---|
| [Pass 4](../continuous-life-pass/CONTINUOUS_LIFE_REPORT.md), §§3, 6, 15–20 | Exact scope, repeated lease/revision checks, atomic local commit, at most one committed local cycle per source event, bounded recovery, revocation and ambiguity barriers. Preparation is not authority. | Does not define publication versus BEGIN as the deadline origin, final fence placement, or COMMIT completion deadline. §9 explicitly says test timings and ceilings are fixture values, not proposed production policy. |
| [Continuous installation design](../../runtime/CONTINUOUS_INSTALLATION.md) | Separate operator-authorized scope; locks, revision/lease fences and unique identities; no universal exactly-once external processing; retries consume budget. | Production duration remains a later reviewed choice. This earlier document predates the later deployment entrypoints. |
| [Pass 5](../operator-control-pass/OPERATOR_CONTROL_REPORT.md), §§11–19, 22 | Operator/review changes are durable and serialized; stale context/disclosure refuses commit; emergency stop does not erase liability; reconciliation does not reopen ambiguous authority. | No instantaneous wall-clock preemption promise. Earlier short-deadline failures under contention were preserved. |
| [Pass 6](../provider-integration-pass/PROVIDER_INTEGRATION_REPORT.md), §§13–17, 23 | Separate request ownership, reservation, receipt and liability; no second send/takeover; replay needs the original valid cycle fence. Continuous-local is not paid reasoning. | Bounded request lease has no renewal; the report does not guarantee total cycle completion from the provider timeout. |
| [Pass 7](DEPLOYMENT_PREPARATION_REPORT.md), §§11, 13–17, 28–31 | Exact deployment/authority identities, bounded explicit consumers, fail-closed startup, recovery evidence, no automatic restored authority. | Connection/statement/lock/idle limits are not a universal PostgreSQL16 transaction deadline. A four-minute consumer session is not an event lease. |
| [Pass 7.1](SHORT_LEASE_RECOVERY_REPORT.md), §§4–11 | Actual fresh-lease expiry is refused; no speculative fix or relaxed fence. | Unconditional success under 250 ms is not established by prior design. No runtime correction was justified without resolving this contract. |

There is a narrower discrepancy worth preserving: Pass 4 describes expired/stale local recovery broadly. The worker presently retries only the exact `STALE_CONTINUOUS_CLAIM` reason; `Continuous stale claim` takes terminal closure, while recovery of an abandoned expired CLAIMED attempt can requeue it. This review does not silently equate those paths or authorize additional retries. Safety does not require every expired attempt to be retried.

## 3. Protected invariant

The intended invariant is stronger than “a lease timestamp has not elapsed,” but is **not** “all legitimate work must finish within that duration.”

For each organism/source event:

1. Only the current durably published attempt/token, bound to the exact scope, event and state revisions, may seek commit admission.
2. Admission requires an unexpired lease and currently valid authority, context/disclosure, policy, permissions, budgets and cancellation state.
3. The admitting transaction holds the shared ownership/authority locks continuously through commit or rollback. No successor may obtain ownership concurrently with that admitted transaction.
4. Decision, episode, local effects, state change, event consumption and follow-ups are atomic; at most one local commit is allowed per source event.
5. Old tokens, cancelled attempts and superseded revisions cannot regain authority. Elapsed time alone never authorizes a second worker, external dispatch or a new provider attempt.

The lease protects against an abandoned or paused worker retaining indefinite eligibility to commit. Locks, token/revision comparisons and uniqueness provide the exclusion and duplicate-prevention mechanisms. A lease does not stop CPU execution or retract a network request; stale computation may finish but its result must be refused.

Precisely: **a worker may admit a local commit only under a current exclusive lease; the admitted transaction retains exclusive database ownership until it ends.** This distinguishes temporal eligibility from transaction completion. Saying merely “commit while the lease is valid” would leave that distinction unresolved.

## 4. Meaning of 250 ms

**250 ms is the short lease value supplied by the crash-test fixture.** It is not a biological parameter, security constant, derived worst-case bound, production SLA or reviewed production duration. Its exact value is a development/test choice; the requirement to honor the configured expiry is a safety invariant.

The same test supplies a **100 ms planner timeout**. That is not a promise that the remaining preparation, database and commit work will fit in 150 ms. Neither value changes here.

No inspected authoritative source requires every legitimate cycle to finish within 250 ms. Pass 4 §9 expressly disclaims production meaning for fixture timing values. Pass 7.1 measured legitimate work that did not fit; it did not justify accepting expired work.

A short fixture may deliberately exercise expiry without requiring ordinary full-path success within that duration. That is a change to the proposition tested, not permission to weaken expiry rejection or relabel an existing failed run as passed.

## 5. Lease start analysis

| Origin | Race/multi-worker properties | Crash, DB and recovery properties | Assessment |
|---|---|---|---|
| A. Claim transaction BEGIN | Row locks still serialize claims, but beginning a transaction is not ownership. Lock waits can consume most or all of the interval. | Crash before commit rolls back ownership. Transaction-start time can precede lock acquisition by an arbitrary wait. Recovery must not infer ownership from BEGIN. | Conservative current implementation detail, but a poor ownership origin. |
| B. Successful durable claim publication | Other workers see a complete attempt/token/deadline together. Claimant may use it only after confirmed publication and while still valid. | Crash before publication leaves no claim; crash after publication leaves inspectable ownership. A lost acknowledgement is uncertainty, not permission to create another claim. | **Recommended logical ownership origin.** |
| C. Preparation start | Preparation may be delayed after a durable claim. Without an earlier finite reservation, the delay could hold work indefinitely; with one, this creates two lease phases. | Crash between claim and preparation needs additional handoff/recovery rules. A worker cannot unilaterally shift the deadline when it resumes. | Adds complexity without evidence of need. |
| D. Planner start | Leaves archive/context/biological-reference preparation outside the ownership interval or requires another reservation phase. | Crash before planner creates the same gap; planner invocation is not a durable database ownership event. | Appropriate origin for the planner timeout only. |

**Implementable form of B:** while holding claim locks, finish eligibility checks, then sample current PostgreSQL wall time immediately before persisting the new ownership records. Use one sample and one identical deadline for event and organism; publish token, attempt and deadline atomically. Refresh time-sensitive eligibility at this point. Do not calculate it from transaction-start `now()`.

The database cannot write a known future COMMIT-completion timestamp into an ordinary claim transaction. Therefore the persisted deadline is conservatively anchored just before publication, not an invented exact publication time. The transaction tail, durable commit and acknowledgement delay consume remaining time. No full-duration guarantee begins when JavaScript receives the reply. If publication/acknowledgement leaves an expired claim, no work may be authorized under it.

Connection/lock waiting before the ownership timestamp belongs to bounded claim acquisition, not the granted work interval. Claim acquisition still needs existing database timeout/abort controls; this proposal does not make waits unbounded. Recovery inspection occurs before a new claim and cannot consume or extend the previous attempt's authority. A recovery claim uses a new token and attempt identity, never a refreshed old token.

## 6. Lease end analysis

| Candidate deadline condition | Assessment |
|---|---|
| A. Preparation finishes before expiry | Insufficient: ownership, revisions, disclosure or scope may change before commit. |
| B. Commit transaction begins before expiry | Insufficient: connection/lock waits and validation can outlast the lease. Frozen `now()` can continue to report a pre-expiry time. |
| C. Final authoritative fence passes before expiry | **Recommended**, with the locking and atomicity requirements below. |
| D. Transaction physically commits before expiry | Stronger deadline than needed for exclusion; a check before COMMIT cannot guarantee future completion under WAL/storage/scheduling delay. Requires different hard-deadline machinery, not simply another timestamp comparison. |
| E. Client receives acknowledgement before expiry | Not a database safety rule. A transaction can commit while its acknowledgement is delayed/lost. Treating that as proof of failure invites duplicate work. |

The final fence must occur **after all potentially lengthy context, disclosure, policy and reducer validation, and immediately before the bounded local-effect write phase**. It must sample `clock_timestamp()` after acquisition of the relevant locks, and compare strictly: database time **<** expiry; equality is expired. `now()` and a statement timestamp sampled before a lock wait do not supply that property. Process `Date.now()` may provide early cancellation or diagnostics but cannot be the final durable authority clock.

At admission, verify event and organism token/deadline consistency, exact attempt/scope/owner/revisions, unconsumed event, cancellation, CLOSED/schedule-disabled requirements, scope/event expiry, current disclosure epoch/bindings and any applicable disclosure expiry. Cached validation alone does not prove a review has not expired during validation. Scope/disclosure absolute expiry is evaluated at the same admission boundary. A revoked or invalidated binding committed before admission refuses it.

Hold the organism, Life State, event/attempt, scope and relevant control/review synchronization locks in a consistent order through the entire transaction. All competing claim/recovery/revocation/disclosure paths must use the same synchronization. Once admitted, only bounded transactional local writes, event finalization and bounded follow-up inserts may remain. No planner, provider, network call, intentional wait or unbounded archive computation belongs there.

**Expiry after admission:** the transaction may complete after the lease deadline. Another worker must wait for these locks, then reread state. If the first committed, it finds a consumed event; if it rolled back, it may follow the bounded recovery procedure. A late acknowledgement conveys no new authority. A lost acknowledgement requires durable outcome inspection, not blind retry.

Revocation also serializes. A stop committed before admission wins. A stop request arriving after the admitted transaction has its locks waits and applies afterward; it cannot retroactively undo an atomic local commit. Do not promise instantaneous preemption from the time an operator clicks stop. Time-dependent eligibility is sampled at admission, not continuously throughout physical COMMIT. This rule needs to be explicit in operator semantics as well as tests.

Post-admission transaction duration must be bounded operationally and observed. Existing statement/lock/idle timeouts help, but do not prove a total transaction wall-time ceiling. Target-host transaction-tail limits and termination procedures remain production prerequisites. They must not allow a successor to bypass a still-running database transaction's locks.

## 7. Renewal analysis

| Policy | Benefit | Cost/risk | Recommendation |
|---|---|---|---|
| No renewal | Simplest ownership, recovery and audit model; fixed upper eligibility interval. | Healthy work may expire and be refused. | **Retain for current bounded continuous-local execution.** |
| Fixed longer lease | Can accommodate measured legitimate preparation/DB tails without a heartbeat protocol. | Slower abandoned-claim recovery; still no latency guarantee. | Select an evidence-based duration later, not an increase to make this test green. |
| Bounded heartbeat renewal | Accommodates variable work while checking liveness. | More writes/races, stop/disclosure interactions, maximum-tenure policy and new failure cases. | Not presently justified. Requires separate review if actual workloads demonstrate need. |

If renewal is later admitted, it must be a locked compare-and-set **before** expiry, proving the exact current attempt/token/revisions, authorized scope, noncancelled event and valid disclosure/control state. It must have an operator-authorized extension bound, total tenure bound and renewal count bound; never extend beyond applicable authority validity. It preserves cycle identity, cannot create a provider attempt, cannot resurrect expired ownership, and cannot override stop, revocation, scope expiry or disclosure invalidation. Journal each old/new deadline and reason. Provider request ownership remains independent.

No renewal operation, changed scope duration or retry is authorized here. A heartbeat alone is not authority; a worker being alive does not establish that its context or permissions remain valid.

## 8. Provider distinction

Three concepts are required and already substantially separate:

| Concept | Protects | Expiry does not imply |
|---|---|---|
| Cycle ownership lease | Eligibility to prepare/admit a local commit for a particular attempt. | Permission for another paid attempt; proof the original transaction failed. |
| Provider request ownership lease | Exclusive handling of a durably reserved request, dispatch status and response settlement. | Remote cancellation, zero charge, safe takeover or permission to resend. |
| Planner/request timeout | A bounded wait for a reasoning result and cancellation request. | Ownership extension, exact timer scheduling, or proof that remote work ceased. |

Current continuous scope admits local deterministic planning only. [ReasoningControl](../../server/reasoning/control.ts) is the separate Pass-6 provider path: request owner, original fence, admission/context/request hashes, reservation, one attempt, dispatch compare-and-set, immutable receipt and liability. Its request deadline is currently derived from process time plus admitted timeout plus 5,000 ms before reservation; dispatch and settlement check ownership/expiry using their existing SQL/process checks. No renewal/takeover exists. This implementation detail is **not** a recommended continuous-cycle duration or a request to rewrite provider timing here.

The [one-shot mode](../../config/first-awakening-v1.json) currently specifies a 60,000 ms cycle lease and 25,000 ms timeout, one cycle and no automatic retry. [OneShotController](../../server/one-shot.ts) publishes a grant-bound claim, uses shared `commitV2`, and makes expired uncommitted claims ambiguous for inspection rather than automatically issuing another grant/claim. Its checks combine SQL lease validity with grant/state checks in [one-shot-authority.ts](../../server/one-shot-authority.ts). Do not transplant continuous-local requeue behavior into it.

An expired cycle must refuse the local commit even if a provider receipt exists. Recording/reconciling factual provider liability is a separate administrative obligation and does not reopen the cycle. A current cycle token also cannot override an expired provider request owner or admission. Provider settlement and replay must retain Pass-6 rules. Shared commit changes require one-shot/provider regression coverage without changing their durations, attempt counts or ambiguity semantics.

## 9. Production-duration methodology

No production lease duration is selected.

1. Measure the actual reviewed Node/image, managed DB/network, pool limits and expected host scheduling behavior. Separate acquisition wait from ownership-time work.
2. Measure claim-publication/acknowledgement tail, preparation, memory/context growth, planner, repeated authority checks, commit validation, and the final locked write/COMMIT tail separately. Include contention, cold starts and permitted maximum input/state sizes.
3. Use whole-path distributions and sufficiently sampled p99/p99.9 estimates, with uncertainty and maximum observed values; do not add component percentiles and call the result an end-to-end percentile. A small fixture cohort cannot establish those tails.
4. Choose a reviewed safety margin and maximum permitted operation size/latency, balancing legitimate completion against abandoned-claim recovery delay. Production authority must bind the resulting limits. If the workload cannot fit, refuse/restrict it or separately review renewal; do not silently extend a live claim.
5. Monitor time remaining at final admission, expiries and recovery rate. Treat expiry as a safe refusal, not an instruction to auto-tune limits or select favorable retries.

Provider behavior is relevant only to a future admitted provider-backed cycle mode; it must not be smuggled into `CONTINUOUS_LOCAL_V1`. Request timeout plus overhead is not itself a proved cycle bound. Current one-shot values remain unchanged.

Host/database clock synchronization and failover behavior are production prerequisites. Use monotonic process time for elapsed diagnostics, database current wall time for durable deadlines. Wall time is not mathematically monotonic: significant backward jumps/failover uncertainty require stopping and inspecting outstanding authority, not treating time rollback as renewal. Terminal tokens never become valid again. A database restore additionally requires fencing old hosts and reconciling lost history as specified by Pass 7.

## 10. Test-contract analysis

The failing generated test in [continuous-life.test.ts](../../tests/continuous-life.test.ts) combines:

1. A crash before durable claim leaves no ownership or partial life commit.
2. The next complete execution finishes successfully under a fresh 250 ms lease.

Claim 2 is **not logically necessary** to prove claim 1. It is a separate timing-dependent liveness assertion. The shared final `consumed=1` assertion also belongs to successful execution, not pristine crash-state proof. Both must be separated deliberately, not hidden by accepting arbitrary `CLOSED_WITH_ERROR` results.

Recommended separate test contracts (no tests changed here):

| Test | Required assertion |
|---|---|
| A. Before-claim atomicity | Exact pristine PENDING state, attempts=0, null ownership, no attempt rows or life writes; recovery finds nothing. |
| B. Fresh legal claim | A fresh controller can acquire attempt 1 with a new valid scope/event-bound token after A; publication is atomic. No requirement that arbitrary subsequent work finishes in the remaining interval. |
| C. Valid-lease commit | Exercise real preparation, policy/reducer and SQL writer; with final database-time fence demonstrably valid, exactly one complete local commit occurs. Control the relevant clock/ordering in an isolated test, rather than treating unbounded host execution speed as a premise. |
| D. Expired-lease refusal | At and beyond expiry, the final authoritative fence rejects; no partial decision, episode, Life State, child event or local effect survives. Preserve 250 ms / 100 ms short-boundary coverage. |
| E. Stale generation | After legal recovery/reclaim, the old token/revisions cannot prepare, dispatch or commit, even if its computation finishes. No token resurrection. |
| F. Multi-worker exclusion | Concurrent claims and commit/recovery races serialize; at most one source-event commit; new owner cannot overtake an admitted transaction. |

Also require: a transaction beginning before expiry but waiting/validating past it refuses; current DB time rather than frozen transaction time decides; a transaction admitted before expiry may commit/acknowledge later while a competing recovery blocks and rereads; rollback after admission permits only the existing bounded recovery; revocation/disclosure invalidation before admission wins; lost acknowledgement never creates a duplicate; local planner timers are cleared independently of commit/recovery.

Deterministic predicate tests are not enough: retain disposable PostgreSQL integration coverage of locks, writer enforcement, revisions, rollback, uniqueness and commit. A controlled clock used for the success premise must govern the same final fence being tested, be confined to isolated tests, and must not add a production environment-clock bypass. Do not silently move only the process clock while PostgreSQL uses another deadline. The exact minimal test seam is an implementation-review choice.

The [seven Pass-7.1 regressions](../../tests/short-lease-recovery.test.ts) already cover parts of A, B, D–F and a process-clock boundary; they do not prove the proposed database final fence. Their transaction-origin interval assertion would need explicit revision if the claim-origin contract is adopted. Preserve archived results and record the new contract rather than rewriting old evidence.

Keep the existing numerical values during that work. Do not skip tests, accept arbitrary failure as success, retry until green, or change planner timeout. Full-path real-time repetitions remain useful latency evidence; a measured expiry must still appear as an expiry, even when contract tests separately pass.

## 11. Recommended lease contract

**LC-1 — Authority:** a lease is subordinate to a separately authorized continuous-local scope. It grants no new capability or provider authority.

**LC-2 — Publication:** acquire ownership atomically under shared locks. Sample current DB time near the claim write after eligibility/lock acquisition; store one token/deadline consistently. Ownership is usable only after durable publication and only for its remaining validity. No work under an unconfirmed claim.

**LC-3 — Preparation:** the same attempt/token/revisions govern preparation. Check cancellation/authority at existing boundaries; a planner timeout is a separate elapsed-work bound. No automatic renewal.

**LC-4 — Final admission:** after validation and under continuously held synchronization locks, a final authoritative DB-current-time fence must pass strictly before lease and other applicable expiries. Exact ownership, revisions, scope, disclosure, cancellation and policy bindings are mandatory. Transaction BEGIN alone never suffices.

**LC-5 — Atomic completion:** a successfully admitted transaction may finish after the deadline while retaining its locks. Only bounded local writes/follow-ups may remain. Release on commit/rollback, never on a client-side assertion that it probably failed. A delayed acknowledgement does not undo a commit.

**LC-6 — Expiry:** before admission, refuse/discard the prepared result. Cleanup and evidence recording may occur after expiry without permitting Life State effects. Another worker may inspect and use the existing bounded local recovery path only after locks permit it and durable state proves eligibility; expiry is not direct takeover authority.

**LC-7 — Recovery:** preserve logical source-event identity but create a new attempt/token for a legally fresh claim. Enforce existing backoff, claim budgets and attempt limits. A still-admitted transaction must finish/rollback first. Unknown provider/commit outcome requires inspection; never infer nonexecution from timeout.

**LC-8 — Observability:** record attempt/token identity privately, lease issue/deadline, final admission time, terminal outcome and bounded failure category. Distinguish transaction-start, database wall time, process elapsed time and acknowledgement time. Do not fabricate exact server commit timestamps from client acknowledgements or expose private context.

This defines a safety contract, not a guarantee of successful execution within any chosen interval. Honest expiry is an allowed outcome for legitimate work that is too slow.

## 12. Required implementation changes, if adopted

No implementation changes have been made. The recommended contract requires:

1. **Claim origin:** replace transaction-start deadline origin in the continuous claim path with one current DB sample near ownership persistence after lock/eligibility work; keep event and organism deadlines identical. Do not renew on return/acknowledgement.
2. **Authoritative final fence:** add/refactor a current-DB-time admission fence after potentially lengthy validation, before local effects, with exact ownership/authority/revision/disclosure checks under the shared locks. Preserve early conservative checks. Align the continuous SQL writer with that rule; a frozen `now()` trigger is not an equivalent final fence.
3. **Atomic writer enforcement:** bind admission to the actual transaction, token and validated write set. A caller-supplied timestamp or freely asserted “admitted” flag is not proof. Final admission and later protected writes must remain under the same locks/transaction. The smallest SQL placement should be chosen with existing least-privilege constraints in view; do not weaken existing writer checks just to allow transaction completion after expiry.
4. **Clock/recovery consistency:** use current DB time after synchronization for decisive continuous ownership/recovery comparisons; preserve bounded cleanup and unknown-liability rules. Record expiry distinctly from ownership mismatch. This does not authorize broadening automatic retry eligibility; retain existing terminal versus abandoned-claim recovery behavior unless separately reviewed.
5. **Narrow review evidence:** add the final admission observation and transaction-tail measurements needed to prove this contract. Update exact runtime/SQL identity and prepared deployment catalog through the existing reviewed release process if source/SQL changes later occur; never silently reuse a prior release identity.

These are ownership/fencing changes, not a speed optimization. Moving the timestamp origin may recover a few milliseconds but does **not** guarantee the test will fit 250 ms. Shared `commitV2`/SQL changes require one-shot and provider compatibility tests; no one-shot grant, provider timeout/request lease, financial policy, science or production duration changes are proposed.

## 13. Required test changes, if adopted

Split the original crash-atomicity and success-latency propositions into A–F above, including the shared consumption assertion. Add database-clock/lock-wait and post-admission serialization cases. Keep zero/negative deadline refusal, stale-worker refusal, planner timeout, after-claim recovery and two-worker tests mandatory. Maintain short-fixture limits, no retries and no skipped coverage.

Validate before/after-claim faults against durable rows, not the test name. Test ambiguous acknowledgement and one-shot non-retry separately from local recoverable crashes. Verify production roles cannot bypass final admission. Then run the full serial suite and deployment fixtures without competing builds, followed by static/build checks. None was run in this design review and no new pass count is claimed.

Test-contract separation is necessary even if claim origin changes: host latency can still exceed a legitimate finite lease. It is not sufficient by itself to implement the recommended final DB fence.

## 14. Safety argument

Consider a worker W holding token T and a competitor V:

- If W crashes before claim publication, its transaction leaves no ownership; V claims normally.
- If W publishes then expires before final admission, the strict DB-current-time check refuses its effects. V must serialize recovery and obtain a new token, subject to current scope/budget rules.
- If V has already recovered/reclaimed, W fails token/status/revision checks regardless of old computation or wall-clock behavior.
- If W admits before expiry, its locks exclude V until the complete local transaction ends. V then sees consumption or rollback; it cannot legitimately own the same event while W is committing.
- If revocation/disclosure change wins synchronization first, W refuses. If the admitted transaction wins first, it completes in the established serial order; a later stop prevents subsequent admission, not retroactive local rollback.
- If W's COMMIT acknowledgement is lost, durable inspection determines the outcome. Unique event commit identity and terminal state prevent a second local effect. Provider liability remains independent and cannot be cleared by lease expiry.

Assumptions: one authoritative PostgreSQL history, correct transaction/lock behavior, consistent lock ordering across all writers, enforced least privilege, immutable authority/review evidence, reviewed clock behavior, and no owner/superuser bypass. Database restore/failover needs the Pass-7 fencing and reconciliation procedures; this lease cannot recover facts lost from the database. A malicious or blocked local process may keep running, but must have no direct external-effect authority and cannot bypass the commit boundary.

The argument proves exclusion and fail-closed eligibility, not bounded scheduling, exactly-once external execution, instant cancellation or a production reliability percentage.

**Preservation:** this review wrote only this document. The 145-file inventory covering `server/`, `core/`, `runtime/`, `tests/`, `config/` and the six cited pass/readiness reports matches before/after document creation: SHA-256 of the compact, sorted path-to-file-hash map is `950d8bce42b63d79e6e4aa8938cfd04eb897cbb870170be5926306b005f1c2db` both times. All local document references resolve, and all 15 required sections are present. No canonical query was performed. The last verified canonical digest is historical Pass-7.1 evidence: `4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`; it is not presented as a fresh measurement. The prior failed regression and Pass-7 readiness verdict remain unchanged.

## 15. Open questions

The recommended ownership/admission semantics above are concrete. Remaining implementation/production choices are:

- Human acceptance of this proposed contract before a separate implementation pass; this document does not authorize changes or activation.
- Minimal database-enforced admission placement and isolated test-clock/ordering seam, preserving least privilege and avoiding a production bypass.
- Target-host evidence for the authorized lease duration and bounded atomic transaction tail. No new duration is selected here.
- Explicit operational category for terminal local expiry versus abandoned-claim bounded recovery, without silently adding retries or rewriting Pass-4/7.1 evidence.
- Managed DB failover/clock-monitoring/restore procedures and operator expectations about an already-admitted commit during stop. No distributed hard-real-time guarantee is assumed.
- Renewal only if future measured workloads justify separate policy and implementation review. Provider-backed continuous life remains a separate, unauthorized design.

No code, test, schema, timing or canonical-state change is required to review these choices. Pass 7 remains unpromoted pending implementation/review and verification; the 45/50 cohort is not reclassified as success.

LEASE CONTRACT DEFINED — IMPLEMENTATION CHANGE REQUIRED

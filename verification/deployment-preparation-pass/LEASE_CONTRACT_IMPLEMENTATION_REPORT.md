# Project Genesis — Pass 7.2 Lease Contract Implementation

Date: 2026-09-21. Scope: reviewed LC-1–LC-8 ownership/fencing correction. **No awakening, canonical installation, production authority, provider dispatch, deployment, renewal or retry expansion.**

## 1. Adopted contract

A continuous-local worker may admit one atomic local commit only while it owns the exact current exclusive lease and all applicable scope, state, disclosure and policy bindings remain valid. Final admission uses current PostgreSQL wall time under synchronization locks. Equality with the deadline is expired. After admission, the bounded atomic local write tail may finish after expiry while retaining those locks through COMMIT/ROLLBACK. A late/lost acknowledgement is not proof of rollback.

| Reviewed clause | Implementation |
|---|---|
| LC-1 authority | Existing separately authorized continuous scope, runtime identity, permission and effect checks retained. Lease creates no capability. |
| LC-2 publication | One current database sample after locks/eligibility; identical event, attempt and organism deadline, atomically published. |
| LC-3 preparation | Existing exact attempt/token/revision checks and separate planner timer; no renewal. |
| LC-4 admission | Database BEFORE-decision-INSERT trigger checks bindings and current time immediately before the protected writes. |
| LC-5 completion | Owner-only transaction-bound admission record permits the protected tail under retained locks. |
| LC-6 expiry | Pre-admission expiry refuses local effects; cleanup can record the refusal. |
| LC-7 recovery | Existing bounded abandoned-local-claim recovery creates a new attempt/token; an admitted transaction excludes recovery until its outcome is durable. |
| LC-8 observability | Durable claim sample/deadline and admission sample/deadline/transaction identity; bounded errors; private monotonic timing evidence distinguishes acknowledgement from server time. |

This implements the reviewed [lease contract](LEASE_CONTRACT_REVIEW.md). It does not reinterpret the historical Pass 7.1 result: that investigation correctly found real expiry and no justified fix under the then-existing written contract.

## 2. Source changes

The complete before/after hashes are in [SOURCE_INVENTORY.json](lease-contract-evidence/SOURCE_INVENTORY.json). The working tree already contained earlier passes; this report does not attribute the entire Git diff to Pass 7.2.

| Files | Change |
|---|---|
| `server/continuous.ts` | Database claim sample; current-clock checks/recovery; bounded errors; prevalidate follow-ups; write-only follow-up tail. |
| `server/continuous-authority.ts`, `server/continuous-worker.ts` | Distinct expiry/ownership/revision errors while retaining the existing narrow recoverability distinction. |
| `server/commit-v2.ts` | Validate intent before admission, persist it after decision admission; bounded continuous fence errors; preserve one-shot checks. |
| `server/intent-journal.ts` | Split validated intent preparation from bounded persistence, retaining the compatibility wrapper. |
| `runtime/continuous-schema.sql` | Claim metadata, private transaction proof, final admission trigger and protected-write enforcement. |
| `runtime/operator-schema-v1.sql`, `runtime/operator-role-grants.sql` | Organism-first disclosure-insert synchronization; private proof privileges restricted. |
| `runtime/deployment/schema.ts`, `catalog-installed.json`, `roles.sql` | Catalog handles the pinned definer namespace; regenerated prepared installed catalog; role documentation. |
| `server/continuous-spec.ts`, `server/one-shot-spec.ts` | New exact implementation identities; no mode duration or permission changes. |
| `runtime/CONTINUOUS_INSTALLATION.md` | Additive lease/locking/installation guidance. |
| Existing continuous, short-lease, operator and deployment tests; crash/restore support | Split the old test proposition, retain bounded error expectations, move tail fault injection into disposable test drivers, restore pinned namespaces correctly. |
| `tests/lease-contract.test.ts`, `tests/support/lease-clock.ts`, `tests/support/lease-tail-fault.ts` | 23 final-fence/ownership regressions and isolated database-clock/fault seams. |
| `scripts/lease-contract-latency.ts`, `scripts/deployment-observer-fixture.ts` | Serial fresh-process latency evidence; unique additive observer evidence output. |

Prepared schema hashes and local implementation identities are in [LOCAL_IDENTITIES.json](lease-contract-evidence/LOCAL_IDENTITIES.json). The unchanged baseline catalog and original migrations remain intact. Canonical SQL was not installed.

Local identities (Node v26.1.0, Darwin arm64):

- One-shot implementation `runtime-v1-oneshot-1.0.8`: `94fc7611a77e3fa76d524461d525cbc70213450c7d971e171639135af49d693f`.
- Continuous implementation `continuous-local-v1.0.2`: `6ddb5b5f8c40ae40a5d579575c25f67bf0d450e4460d5826c6996e42ccfa3fa7`.

These are local implementation identities, not authorization records or target-host identities. Existing authority hashes must not be edited to match them. A target platform must generate and review its own exact release identity.

## 3. Claim publication implementation

`ContinuousController.claim` obtains organism/Life State, scope/schedule and candidate-event locks, checks identity, eligibility, resource limits and existing ownership, then obtains one materialized `clock_timestamp()` sample. It rechecks time-dependent scope/event eligibility against that sample. The deadline is sample + the unchanged scope lease duration.

The sample and deadline are preserved as PostgreSQL timestamp text, avoiding an unnecessary JavaScript millisecond round trip. `claim_issued_at` and `lease_until` are stored on the attempt; event and organism use the exact same deadline. Attempt, token, ownership records and claim journal publish in one transaction. The caller cannot supply the authoritative clock or separately calculate another deadline.

Ownership becomes usable after publication. The interval is conservatively anchored immediately before the writes, not at a fictional known COMMIT timestamp. Publication/acknowledgement delays consume remaining time; acknowledgement never renews the lease. Lock waits before the sample do not consume the new interval. Rollback before publication leaves no ownership. Uncertain acknowledgement leaves a durable inspectable claim and cannot create a second owner.

## 4. Final admission implementation

Application preparation still checks exact identity, revisions, authority, cancellation, saved-only biology, context/disclosure reconstruction, proposal/policy, deterministic reducer output, intent and follow-up validity. These operations precede the Decision INSERT. The implementation intentionally retains coarse organism locking during commit validation; this is not a lock-duration optimization.

The Decision INSERT invokes `genesis_admit_continuous_decision` before any decision/episode/Life State/local-effect/event-consumption writes. With the full synchronization lock set held, it verifies:

- exact organism, event, attempt, token and shared deadline;
- current claimed/preparing states, unconsumed event and noncancelled attempt;
- base and Life State revisions;
- authorized scope, authorization record and scope/permission binding;
- CLOSED execution, disabled schedule, saved-only biology and constitution;
- disclosure control epoch, current review identity/version/source binding and effective expiry;
- absence of unresolved provider liability for this cycle.

After these checks, it samples `clock_timestamp()` once and requires that time be strictly before the event lease, scope/event expiry and relevant disclosure expiry. A transaction that began earlier or waited for a lock gains no exception.

Current source/context/policy validation remains in the trusted reviewed application under the same organism lock; the SQL trigger supplies the last current-time/ownership admission and independently checks its durable bindings. It is not a replacement for the application validators.

## 5. SQL enforcement

`genesis_continuous_admissions` is an immutable private proof table keyed by cycle, with transaction ID (`xid8`), exact token/event, admission sample and deadline. Its CHECK requires admission before the deadline. Only the restricted SECURITY DEFINER decision trigger writes it. Its search path is pinned to the installed schema, then `pg_catalog` and `pg_temp`; ordinary service roles cannot create schema objects, forge proof rows or invoke the trigger function directly.

`genesis_require_v2_writer` requires this proof for continuous Decision insertion and organism effects. Additional guards bind continuous-marked Life State, episode, intent, event consumption/child insertion and committed-attempt writes to the same transaction proof. Nonterminal claim/recovery cleanup remains possible without authorizing a life effect. A caller-provided GUC claiming admission does nothing.

The original continuous expiry guard was replaced by the stronger final current-clock admission plus exact same-transaction proof; it was not simply removed. Subsequent protected writes do not reclassify an admitted transaction as expired. The one-shot SQL branch remains unchanged.

Threat-model boundary: the migration owner/superuser can change database objects and is trusted. Normal runtime processes must use the tested non-owner roles and reviewed application entrypoints. This pass does not claim protection against a malicious database owner or arbitrary privileged SQL outside those entrypoints.

## 6. Lock-order analysis

The common outer order is **organism first**, held continuously until COMMIT/ROLLBACK. Secondary locks may be acquired in different orders only after that exclusive organism lock is already held; two cooperating same-organism mutations cannot enter those secondary sections concurrently.

| Path | Synchronization |
|---|---|
| Claim / commit / recovery / cancellation / scope propose-authorize-revoke | `ContinuousController.base` locks organism then Life State before subordinate scope/event/attempt work. |
| Final SQL admission | Reacquires the same root lock, then Life State, continuous attempt, scope, schedule, event, generic attempt and disclosure control. Already-held locks are retained. |
| Authenticated operator commands / emergency stop / review | `OperatorControl.execute` locks organism before control/target; nested controllers share the transaction. |
| Disclosure insertion | SQL insertion guard now locks organism before incrementing/locking control revision. |
| Attributed human response | `AssistanceIntake` locks organism then Life State; event intake remains in the same transaction. |
| Provider / one-shot | Existing distinct locks and liability semantics retained; shared local commit cannot bypass the organism lock. |

A competing recovery or revocation is observed blocked with `pg_blocking_pids` while the admitted transaction remains open. Once released, it rereads committed/rolled-back state. A revocation committed before admission refuses the cycle; a revocation arriving behind admission waits and applies afterward. This is serialized revocation, not retroactive undo or instantaneous preemption.

No reverse outer root ordering was introduced. These statements cover the supported mutation paths, not arbitrary owner-written SQL. Production transaction/lock/statement timeouts and supervision remain required; PostgreSQL16 does not supply a universal hard-real-time total transaction guarantee here.

## 7. Expiry/error semantics

Continuous errors distinguish `LEASE_EXPIRED_BEFORE_ADMISSION`, `OWNERSHIP_MISMATCH`, `REVISION_STALE`, `SCOPE_INVALID`, `DISCLOSURE_INVALID` and `CANCELLED`. Final SQL expiry additionally supplies bounded private database time/deadline/margin detail. No context, provider body or secret is included.

The worker returns `CLOSED_WITH_ERROR` for a refused cycle; it does not fabricate COMMITTED or voluntary abstention. Cleanup records the reason. An old operator regression expected the former free-form context-mismatch message; its continuous-only expectation now checks `DISCLOSURE_INVALID`. One-shot expectations remain unchanged.

## 8. Recovery semantics

The preexisting distinction between the early base-check stale path and the later exact event/final fence remains deliberate:

- The early check previously identified as `STALE_CONTINUOUS_CLAIM` retains its bounded local-recovery classification through `ContinuousFenceError.recoverableLocal`.
- Later event/final admission expiry or mismatch is nonretryable by default. Planner cancellation polling preserves a bounded reason without promoting it to the recoverable class.
- Abandoned durable local ownership can still be inspected by `recover`, closed within existing limits and requeued with existing backoff. A legal fresh claim has a new attempt and token, never an extended old claim.
- An admitted transaction excludes recovery until COMMIT/ROLLBACK. If committed, recovery finds no eligible claimed work; if rolled back, existing recovery rules apply.
- Provider ambiguity remains nonretryable and preserves liability. Lost local commit acknowledgement requires durable inspection; elapsed time is not evidence of failure.

No new retry, lease renewal, heartbeat, extension, branch removal or budget exemption was added.

## 9. Planner timeout separation

The short fixture remains **250 ms cycle lease / 100 ms planner timeout**. The planner timer is allocated immediately before the injected planner call, after preparation and ownership checking. `finally` clears timer/poll/listener state. The timer does not begin at claim, extend the database lease or authorize commit. Timeout/expiry cannot resurrect ownership. A valid-lease failed planner result follows the existing failed-outcome semantics; an expired cycle cannot persist that result.

A dedicated regression observes timer allocation at invocation and cleanup, and another proves timeout cannot authorize an expired claim. The final TypeScript correction only widened the test's timer-handle type to the platform's `clearTimeout` parameter type; it changed no runtime timer logic.

## 10. One-shot compatibility

`GENESIS_FIRST_AWAKENING_V1` remains NOT AUTHORIZED, exactly one cycle from seven prior decisions, no automatic continuation, 60,000 ms lease, 25,000 ms provider timeout, one provider attempt and zero automatic retries. Its original SQL branch and mode/config bytes were preserved. The shared commit now prepares intent validation before inserting the decision and writes the prepared intent afterward, in the same atomic transaction.

The complete suite exercises single-consumer, stale worker, revocation, expiry, ambiguity, exact bindings and Decision 9 refusal. The least-privilege deployment topology independently exercises one-shot Decision 8 in sanitized fixture state, then refuses reuse. No canonical grant was installed or issued.

## 11. Provider compatibility

No provider adapter, admission, reservation, request ownership, liability, receipt replay or timeout policy was modified. Existing provider integration and operator reconciliation tests pass in the full suite. Deployment topology uses an injected fixture provider, preserves one receipt/attempt through restart/restore and refuses repeat consumption.

A receipt grants no cycle ownership. Expired-cycle commit remains fenced; any charged/unknown provider outcome remains a separate reconciliation matter. No live provider or external API request was made.

## 12. Test-contract split

The original historical failing evidence remains unchanged. Current tests separate the propositions rather than promising arbitrary work fits in 250 ms:

A. Crash before durable claim leaves PENDING, zero attempts, no token/lease/attempt rows, no decision/episode/local change; recovery finds nothing.

B. A fresh worker can publish one consistent attempt/token/deadline afterward.

C. With a valid authoritative database-clock boundary, exactly one Decision/Episode/local state commit consumes the event once.

D. Equality/after-expiry at the final database fence refuses without protected effects.

E. After legal recovery, the old generation can never commit.

F. Concurrent workers have one owner; no competing recovery/revocation overtakes admitted work.

The isolated clock seam resides only in test support, requires the dedicated test database and fixture schema, and substitutes only the disposable database function's clock primitive plus fixture query clock reads. It is not a production environment flag, process-clock assertion or application-supplied admitted boolean. Real-time repetitions use the real database clock.

## 13. Database final-fence tests

All required final-fence cases pass against disposable PostgreSQL:

| Case | Result |
|---|---|
| BEGIN before expiry, final fence after | Refused; no decision/proof survives. |
| INSERT waits for ownership lock past expiry | Refused after lock acquisition using current DB time. |
| Admission before expiry, protected tail crosses deadline | Atomic commit allowed. |
| Recovery competes while admitted transaction is open | Actual database blocking observed; terminal state reread afterward. |
| Admitted transaction rolls back after expiry | No local effects/proof survive; existing bounded recovery applies. |
| Revocation precedes admission | Refused. |
| Admission precedes revocation | Local commit completes atomically; subsequent revocation persists. |
| Disclosure epoch invalidates before admission | SQL fence refuses. |
| Database time equals deadline | Expired, refused. |

See [lease-contract.test.ts](../../tests/lease-contract.test.ts) and [final focused log](lease-contract-evidence/deployment-final.txt).

## 14. Claim-publication tests

Tests verify lock wait before the sample, exact shared deadlines, atomic attempt/token publication, rollback before publication, lost acknowledgement without duplicate ownership, and no deadline reset on inspection/acknowledgement. The 250 ms interval is measured between the persisted database issue sample and persisted deadline, not attempt-row `now()` or client return time.

## 15. Transaction-tail tests

Intent transition validation and follow-up schema/duplicate checks precede admission. After the decision INSERT, the supported path contains prepared intent persistence, episode/Life State/organism/attempt/grant writes as applicable, bounded child-event writes and terminal journal/COMMIT. No planner/provider/network call, archive scan, context compilation, disclosure discovery or arbitrary callback is invoked there.

A driver-level phase test rejects archive/disclosure discovery SQL after admission and checks the shared commit's remaining source for planner/context/network/hook calls. Tail crash/pause injection is exclusively in disposable test wrappers, not production callbacks. SQL triggers necessarily perform bounded ownership/proof checks during those writes.

The 50-run evidence observed **6.482–15.839 ms** from the INSERT response to COMMIT acknowledgement (median **7.366 ms**). This is a client-observed portion of the tail, not an exact server COMMIT timestamp or hard-real-time bound. No performance claim or production lease duration is inferred.

## 16. Multi-worker, revocation and disclosure races

Real concurrent database clients prove one claim owner and blocked competing recovery/revocation after admission. Tests cover stale generations, lost claim/commit acknowledgements, revocation-before and admission-before orderings, disclosure invalidation, and worker/observer inability to forge proof or shadow the pinned definer namespace.

Operator disclosure/control tests additionally recompile and reject changed context/review state. Supported operators synchronize on organism; a completed pre-admission invalidation wins. No lease clock test disables these fences or grants another worker concurrent ownership.

## 17. Short-lease latency evidence

[50 fresh-process records](lease-contract-evidence/latency-50.json), [summary](lease-contract-evidence/LATENCY_SUMMARY.json): sequential real-time runs, no build/typecheck overlap, 250/100 unchanged, zero retries.

| Measurement | Result |
|---|---|
| Runs | 50 |
| COMMITTED | 50 |
| Expiry refusals | 0 |
| Unexpected ownership/partial/duplicate errors | 0 |
| Tick elapsed min / median / p95 / max | 95.584 / 109.966 / 141.755 / 243.466 ms |
| Final admission margin min / median / max | 42.917 / 158.115 / 171.277 ms |

Each record has one new attempt, one fixture decision/episode and consumed source event. An expiry would have been retained as expiry, not retried or relabeled. This sample is latency evidence only, not proof of production reliability or a promise that every future 250 ms run commits. Pass 7.1's 45/50 result remains historical evidence under its original implementation.

These repetitions were completed before the final bounded-error propagation/type-only test cleanup. Those later changes do not alter the measured successful claim/admission path; the final full suite and focused rerun verify the final implementation. Completed latency work was not repeated after the user's continuation request.

## 18. Full suite

Final serial suite: **564 passed, 0 failed, 0 skipped**, 100.696 seconds. This includes the original 533 Pass-7 tests, seven Pass-7.1 tests, 23 new lease-contract tests and one new admission-role test. No test was skipped/quarantined/deleted to pass. Current crash assertions were changed only to the reviewed separated contract.

Evidence: [full-suite-final.txt](lease-contract-evidence/full-suite-final.txt). After final test-only typing/import cleanup, the affected 23 contract tests and deployment cases passed again. [CHECKS.json](lease-contract-evidence/CHECKS.json) records final checks and retained intermediate failures.

The initial full run had 563 passes and one old error-message assertion failure; the refusal itself was correct. Earlier development logs also preserve a strip-only TypeScript constructor issue, restore schema-remap failures and a wrong test expectation for the existing `local_completed` status; these were corrected and not hidden. None represents a canonical effect.

After interruption, local PostgreSQL was unavailable. The failed resumed test log is retained. The existing local cluster was restarted without initialization/reseeding; PostgreSQL performed crash recovery. Read-only canonical verification immediately afterward matched the baseline exactly, then tests resumed. No Genesis runtime or worker was started against canonical data.

## 19. Deployment fixtures

The final reruns cover all **17 original deployment-critical tests plus the new proof-role test (18 total)**. The last runs are split between [deployment-final.txt](lease-contract-evidence/deployment-final.txt) (17 deployment cases plus 23 lease cases) and [topology-final.txt](lease-contract-evidence/topology-final.txt) (one integrated topology case).

Coverage includes reviewed-plan installation only in disposable schemas; unchanged original fixture rows; least-privilege reader/operator/worker; single-use fixture Decision 8; restart/reuse refusal; separately scoped local fixture continuation/revocation; dormant and post-cycle actual `pg_dump`/restore with catalog, row, receipt and sequence verification.

[Dormant E2E](lease-contract-evidence/OBSERVER_E2E.json) used the real production Next build and two fresh runtime processes against a disposable database, read-only service role and loopback HTTP. Dormant landing returned 200 and gated public state with 404; live observer presentation of the dormant fixture returned truthful DORMANT/CLOSED state with 200. Both runs preserved all fixture rows. No authority, provider, worker or canonical cycle was started.

## 20. Build/static checks

| Check | Final result |
|---|---|
| TypeScript, no emit / no incremental | PASS ([log](lease-contract-evidence/typecheck-final-02.txt)) |
| ESLint | PASS, zero warnings/errors ([log](lease-contract-evidence/lint-final-02.txt)) |
| Next.js production Webpack build | PASS ([log](lease-contract-evidence/build-final.txt)) |
| Docker execution | **CONTAINER EXECUTION NOT VERIFIED LOCALLY** — Docker unavailable |

Build used the existing Webpack route, masked local environment credential values and disabled telemetry. The existing Node `module.register()` deprecation warning did not fail the build. No Turbopack workaround or architecture change was introduced.

## 21. Canonical preservation

Read-only full row exports before work, after service recovery, and after final tests all match:

`4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`

[Sanitized preservation evidence](lease-contract-evidence/PRESERVATION.json) verifies every exported row equals the initial row representation, including original identity/birth, decisions, memories, project, ledger, milestones, brain snapshot, Life State and schedule. Private complete exports remain outside this report.

- Organism: `817e772c-827e-48fc-8e35-6504cb2a8d2d`.
- Birth: `2026-09-15T01:56:07.867Z`.
- Decisions **7**; legacy memories **7**; V2 episodes **0**.
- Execution **CLOSED**; schedule **DISABLED**; biology **SAVED-OBSERVATION-ONLY**.
- Continuous authority **NONE**; one-shot/continuous/provider preparation tables uninstalled canonically.
- Canonical provider calls, wallet actions and external communications during this pass **0**. This is grounded in the operations performed and unchanged canonical records, not an account-wide network audit.
- No canonical SQL, grant, scope, event, decision or episode was created.

Every preexisting deployment-preparation verification artifact covered by the before inventory remains byte-identical. Historical Pass 7, 7.1 and contract-review reports were not rewritten. Biological/scientific source and frozen research were not edited; this pass did not rerun a biological study or repeat the earlier multi-gigabyte research package audit.

## 22. Remaining infrastructure blockers

The local contract implementation is verified. This is readiness for infrastructure verification, not activation readiness or authority.

Still required under separate reviewed work/authorization:

1. Actual Node24/Linux container build/start/restart and target-host transaction-tail/latency verification. Local tests used Node26/macOS PostgreSQL16.
2. Intended managed deployment target, database TLS/networking, ordinary login roles, privileges and connection/timeout budgets.
3. Managed backup/restore/failover and fencing of old hosts; the local schema-remap restore is not managed disaster-recovery proof.
4. Exact target release/catalog/SQL identity review and separately authorized structural installation. Existing installer rejects unknown/already-installed schemas rather than silently upgrading them.
5. Provider/model/secrets/smoke/admission, disclosure and human authorization prerequisites remain separate. None was performed here.
6. Production lease duration selection from measured target preparation/DB latency and operational bounds. No production duration was selected, and no renewal was added.

No automatic continuation, deployment, installation or awakening follows this report.

LEASE CONTRACT IMPLEMENTED AND VERIFIED — PASS 7 READY FOR INFRASTRUCTURE VERIFICATION

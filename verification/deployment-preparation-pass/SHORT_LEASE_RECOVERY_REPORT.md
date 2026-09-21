# Pass 7.1 — Short-lease recovery investigation

## 1. Exact original failure

`tests/continuous-life.test.ts`, **Crash boundary before_claim has atomic local recovery**, expects the second tick to return `COMMITTED`. It intermittently returns `CLOSED_WITH_ERROR` with a **250 ms lease and 100 ms planner timeout**.

The investigation identifies the rejecting condition but does **not** establish a permissible implementation correction. No production/scientific code, lease, timeout, authority, policy, schema or safety fence was changed. The original assertion remains mandatory; its message now includes the existing bounded failure reason. Nothing was skipped, quarantined or retried to obtain a favorable classification.

## 2. Reproduction rate

Runs were sequential, against disposable PostgreSQL using the original fixture/planner/fault boundary. No build, typecheck or unrelated test suite ran concurrently with the timing-sensitive repetitions.

| Cohort | Passed / committed | Failed | Scope |
|---|---:|---:|---|
| Initial unchanged test | 9 | 1 | Ten fresh test processes |
| Original test with improved assertion message | 45 | 5 | Fifty fresh test processes; unchanged assertions/limits |
| Instrumented fallback diagnostic | 19 | 6 | Twenty-five fresh processes; additional probes |

**Classification: INTERMITTENT.** Elapsed-time sensitivity is demonstrated. No controlled external-load experiment was performed, so no causal attribution to a particular other application, CPU load, DB contention source or OS scheduler is claimed. Instrumentation adds overhead; do not pool the cohorts or interpret these rates as production reliability.

Every run is preserved in `short-lease-evidence/`. Diagnostic process exit zero means data collection completed, **not** that the cycle committed; the JSON `result.status` is authoritative.

## 3. Actual reason and failed check

All five failures in the fifty-run cohort report **`Continuous stale claim`**, from `assertContinuousClaim` in `server/continuous-authority.ts`. Earlier instrumented failures reached this check inside `commitV2`; another trace failed during the final preparation check.

The detailed `fence-01.json` trace isolates the predicate:

- attempt status/lease/scope/event/revision bindings: valid;
- event status/cycle/lease bindings: valid;
- event lease expiry: **2026-09-21T11:57:11.297Z**;
- process wall clock at the rejecting predicate: **11:57:11.304Z**;
- PostgreSQL `clock_timestamp()` from the immediately preceding event read: **11:57:11.304Z**;
- remaining lease: **−7 ms**.

Thus this is a real expiry, not an invented timestamp, absent event, reused lease or demonstrated process/DB clock offset. The exact predicate is `new Date(e.lease_until).getTime() <= Date.now()`.

## 4. Durable state after the before-claim crash

The hook executes in `ContinuousWorker.tick` **before** `controller.recover()` and `controller.claim()`, outside the claimed-cycle try block. It throws `SimulatedCrash` immediately. All 25 instrumented fallback runs record:

- event `PENDING`, attempts **0**, cycle ID/lease/lease expiry null;
- no `genesis_continuous_attempts` or `genesis_cycle_attempts` row;
- organism lease absent, phase `idle`;
- scope still `AUTHORIZED` in the disposable fixture.

The intended path is therefore:

`PENDING → crash before any durable claim → next tick inspects recovery (nothing to recover) → fresh attempt 1 → preparation → commit only if fences remain valid`.

The original test adds an unconditional successful-commit expectation. The fault-injection mechanism does not guarantee that the subsequent legitimate work will fit within 250 ms.

On the observed failure, the event and continuous attempt become `FAILED`, the generic cycle attempt is cancelled, the organism lease is released and no decision is inserted. The event retains historical lease metadata; this is not active organism ownership. Scope remains authorized in the fixture. The existing worker retries only its exact `STALE_CONTINUOUS_CLAIM` category; `Continuous stale claim` takes terminal closure. This difference is recorded, not changed into an extra retry.

## 5. Timeline

Representative failed trace, elapsed monotonic milliseconds from initial diagnostic tick origin (`fence-01.json`):

| Boundary | ms |
|---|---:|
| Initial tick / injected crash | 0.08 / 0.31 |
| Second tick | 1.82 |
| Recovery inspection start / end | 1.91 / 6.14 |
| Claim start / transaction completed | 6.14 / 24.62 |
| Event lease written | 20.24 |
| Preparation start | 24.63 |
| Saved-observation adapter construction start / end | 50.71 / 91.00 |
| Before-planner phase validation start / end | 107.84 / 190.77 |
| Actual planner start / end | 209.86 / 209.98 |
| Planner timer cleanup | 220.40 |
| Policy start / end | 243.65 / 245.34 |
| Reducer start / end | 255.66 / 255.75 |
| Rejecting fence | 263.93 |
| Failure closure transaction completed | 273.99 |

This trace never starts commit. `diagnostic-03.json` instead reaches commit at 248.59 ms, reaches the before-commit hook at 260.24 ms and rejects inside `commitV2` at 274.56 ms. Its transaction rolls back; there is no successful transaction commit or follow-up insertion to assign a fabricated time to. Successful traces include before/after follow-up and transaction commit timings. Query records include SQL-template hashes, bounded categories, durations and selected DB clocks, without query argument values, memory or planner bodies.

## 6. Clock audit

| Use | Actual source / behavior |
|---|---|
| Event creation, observation timestamps | JavaScript wall-clock ISO timestamps; immutable event data |
| Due-event selection | PostgreSQL `now()` in claim transaction |
| Claim/attempt `at`, event/organism lease expiry | PostgreSQL transaction-start `now()`; expiry = transaction start + leaseMs |
| Base organism lease validity | PostgreSQL `lease_until > now()`; transaction-start comparison |
| Event lease fence | JavaScript `Date.now()` against persisted event expiry |
| Scope issue/expiry checks | JavaScript wall time; SQL writer trigger additionally checks transaction-start `now()` |
| Event absolute expiry | JavaScript wall time |
| Recovery selection | PostgreSQL `now()` compared with event expiry |
| Retry eligibility / backoff | Scope expiry uses JavaScript wall time; availability uses transaction-start PostgreSQL `now()` |
| Resource windows | SQL `now()` for attempt window; JavaScript wall time for provider-ledger window |
| Planner timeout / cancellation poll | Node `setTimeout` (100 ms) and `setInterval` (50 ms), cleared in finally |
| Commit writer trigger | SQL `now()`; continuous decision insertion checks event expiry |
| Follow-up availability | Persisted event/decision times and declared delays; not a separate execution timer |
| Diagnostic elapsed time | `performance.now()`; wall clocks returned alongside existing DB queries |
| Boundary unit tests | Explicitly controlled `Date.now()` for the application predicate only; always restored |

There is no global monotonic durable authority clock. PostgreSQL transaction time and current process wall time differ intentionally in *evaluation time*, even when their clocks agree. In the failed sample, transaction `now()` is 11:57:11.296Z (still before expiry), while actual DB clock and process time are 11:57:11.304Z (expired). The application check correctly refuses. NTP jumps/failover clock skew were not simulated. No broad clock refactor was made.

## 7. Lease semantics

The code bounds authorization throughout the claimed cycle, **not planner execution alone**. The persisted 250 ms interval starts at the claim transaction's `BEGIN` timestamp. Connection acquisition and the preceding recovery transaction occur before this timestamp. Claim row-lock waits, scope/resource validation, claim writes, preparation, context/evidence work, phase checks and the subsequent commit-fence checks consume this interval.

Across the 25 traces, **13–27 ms** had elapsed between transaction start and the event lease write (median 17 ms). This origin is earlier than durable claim publication. All measured persisted intervals are exactly 250 ms from claim transaction time; the second tick does not reuse an old expiry.

Commit must pass the application fences while the event lease remains current. The SQL trigger uses the commit transaction's frozen `now()`. There is **no fresh-clock deadline check at the physical COMMIT acknowledgement**, and follow-up insertion occurs later in that same atomic, locked transaction. Consequently this implementation does not establish that COMMIT must finish before expiry. Expiry is also allowed before failure closure; cleanup must be possible after authorization ends.

The Pass-4 report (`CONTINUOUS_LIFE_REPORT.md`, sections 6/7/15–17) specifies leases, repeated checks, atomic commit, stale-worker refusal and bounded recovery. It does **not** specify a hard worst-case execution latency or explicitly resolve transaction-start versus publication-time lease origin. Changing the origin or accepting an expired claim to satisfy this test would choose a new interpretation without that evidence. No such change was made.

## 8. Planner timeout semantics

The timer is allocated inside the planner wrapper, after context preparation, the before-planner phase and an initial authority check, immediately before the selected planner invocation. The same invocation creates a cancellation poll and optional abort listener. `finally` clears timer, interval and listener. A fresh prepare invocation creates fresh handles; the before-claim crash creates none.

Measured fallback invocation in the failed sample: **0.12 ms**. A deliberate never-resolving fixture planner triggered `PLANNER_TIMEOUT` after **101.31 ms**, followed immediately by cleanup. Subsequent cycle processing legitimately exhausted the 250 ms lease and refused commit. A successful fallback trace was observed for another 120 ms after closure and produced **no late timeout probe**. Thus no stale planner timer or context time incorrectly charged to the 100 ms planner budget was demonstrated.

The winning Promise.race result is already settled before the post-response authority check; a later timer rejection cannot change that winner. A cancellation poll already in flight may finish after interval cancellation; this investigation does not claim clearing an interval cancels a PostgreSQL query. No relevant fallback poll was needed before the sub-millisecond response.

## 9. Database latency

Instrumented fallback cohorts:

| Metric (ms unless stated) | Min | Median | p95 | Max |
|---|---:|---:|---:|---:|
| Recovery transaction wrapper | 2.84 | 3.93 | 6.55 | 6.56 |
| Claim wrapper | 17.75 | 21.41 | 31.68 | 33.36 |
| Second tick to closure | 184.01 | 233.57 | 279.89 | 296.64 |
| Sum of query round-trip durations | 83.41 | 101.81 | 140.07 | 163.39 |
| Query count, including checks/transaction control | 149 | 177 | 177 | 177 |

In a separate connection-instrumented trace, 16 acquisitions took 0.015–0.067 ms (median 0.020 ms). This does not establish a universal connection latency bound.

In `fence-01`, the before-planner phase check took approximately 83 ms; multiple query completions stretched to 9–19 ms. Saved adapter construction took about 40 ms. Neither the reducer nor actual planner dominated. Query timings include network, server processing, process scheduling and possible lock waits. **Pure database lock-wait duration is not separately identified**; the `FOR UPDATE` query duration is only an upper bound. No unrelated test/build was running, but machine-wide load was not controlled. There is no evidence here of an unintended long-lived lock introduced by Pass 7.

## 10. Comparison with pre-Pass-7 path

`short-lease-evidence/PASS7_PATH_COMPARISON.json` compares current bytes with the start-of-Pass-7 hash inventory. Continuous controller, worker, authority, scope validation, common commit, context, saved-observation adapter, memory/disclosure readers, continuous SQL and fixture helpers are unchanged.

The ordinary continuous fixture installs historical/one-shot/continuous preparation SQL, **not** the Pass-7 deployment release, new CLOSED constraint, normal-role verification or readiness catalog. Its pool configuration is unchanged. The explicit deployment consumer is not called. No deployment binding, role/readiness check or new logging query appears in its claim path.

Pass 7 changed `server/one-shot-spec.ts`. Fixture grant construction happens before the tick. Continuous identity validation hashes that file's bytes but does not execute its expanded one-shot runtime hash traversal. This may affect file-hash work; an exact pre-Pass-7 timing counterfactual was not performed, and its cost is not asserted to be zero. No new deployment-critical database operation was found in the failing interval. Hash equality establishes unchanged code, not unchanged host performance.

## 11. Root cause and remaining uncertainty

**Established proximate cause:** a legally fresh claim reaches an existing event-expiry fence after its 250 ms interval. Identity/state predicates still pass. Repeated validation, database round trips, evidence/context construction and variable scheduling consume the interval. The planner does not time out in the original fallback failure.

**Not established:** a recovery implementation defect that violates the previously documented contract, a unique Pass-7 code change causing the latency, or a guarantee that ordinary permitted execution must complete within 250 ms. The original test combines a valid atomicity expectation with an unconditional latency-dependent successful-commit assertion. The latter is not reliably satisfied on this host.

This is not a finding that expiry should be ignored, nor permission to relabel the test as acceptable/skipped. The success criterion remains unmet.

## 12. Fix / files changed

**No runtime fix applied.** Only:

- `tests/continuous-life.test.ts`: retain expected `COMMITTED`; show the existing failure reason in the assertion message;
- `tests/short-lease-recovery.test.ts`: seven focused state/fence tests;
- `tests/support/short-lease-instrumentation.mjs`: private, test-only in-memory source probes;
- `scripts/short-lease-diagnostic.mjs`: disposable diagnostic collection with unique output path;
- additive investigation evidence/report/readiness update.

Diagnostic hooks do not rewrite production files and are never imported by runtime startup. The observer rerun used a temporary in-memory output-path redirect to avoid overwriting historical Pass-7 evidence.

## 13. Why safety was not weakened

Lease remains 250 ms; planner timeout remains 100 ms. No retries, extensions, new lease authority, relaxed predicate, changed production policy, SQL migration, scientific change, cache bypass or accepted stale commit was added. All original test cases remain, including the failing assertion. Failed attempts remain failed; no synthetic decision is reported as a canonical result.

## 14. Focused regressions

**7/7 passed, 0 skipped:** before-claim leaves no durable claim; after-claim preserves its attempt and legally expired recovery creates a distinct fresh lease; stale worker refusal after recovery; expiry before preparation; one owner in a two-worker claim race; application fence with +1/0/−1 ms remaining.

The final three tests isolate the process-clock predicate using captured compatible fixture rows; they are not full transactional commit proofs. Actual successful and expired commit paths are captured by the repeated diagnostic runs. Planner timeout and timer cleanup are separate instrumented probes. No blanket claim is made that the requested complete end-to-end near-boundary success matrix is verified; the instability prevents that promotion.

## 15. Repeated isolated results

Fifty original-test executions: **45 passed / 5 failed**. Failures: runs **11, 19, 27, 36, 37**, all `Continuous stale claim`.

| Duration (ms) | Min | Median | p95 | Max |
|---|---:|---:|---:|---:|
| Whole fresh process, including imports/setup/cleanup | 855.63 | 985.02 | 1296.11 | 1380.46 |
| Node test body, including fixture setup/cleanup | 401.35 | 468.07 | 664.26 | 806.57 |

Neither duration is a lease duration. In the ten instrumented predicate traces, final checked lease margin ranges **−7 to +87 ms**, median **64 ms**. Nine committed; one refused. The fifty uninstrumented runs do not record per-fence margin; it is deliberately not inferred from overall process duration. All raw measurements and nearest-rank p95 calculations are in RESULTS.json.

## 16. Full suite / static checks

The user requires isolated stability **before** a complete serial suite. That gate failed, so the full suite and subsequent Webpack build promotion were **not run in Pass 7.1**. This is not a claim that 540 tests pass. The historical Pass-7 result remains 533 total / 532 passed / 1 failed.

TypeScript and ESLint were run sequentially to validate the added diagnostics/tests and both passed. The unchanged application’s existing successful Pass-7 Webpack build was used for dormant E2E. No overlapping build was used during repetitions. No original failure evidence was overwritten.

## 17. Deployment-critical fixtures

Re-run serially: **17/17 deployment tests passed**, including owner installation into disposable state, least-privilege roles, mock one-shot Decision8, local-only continuous fixture, revocation, restart persistence and actual pg_dump/restore. These are fixture decisions only.

Dormant E2E re-run: actual built Next observer and fresh runtime processes, two starts, health/readiness HTTP200, expected dormant/live-projection behavior, all fixture rows unchanged, no authority/provider/worker. Output is a new `short-lease-evidence/OBSERVER_E2E.json`, not the original Pass-7 artifact. Docker remains unavailable: **CONTAINER EXECUTION NOT VERIFIED LOCALLY**.

## 18. Canonical preservation

Read-only before/after exports compare equal for **every canonical row**. Actual digest both times:

`4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`

Original ID/birth, seven decisions, seven legacy memories, original project/ledger/milestones/snapshot unchanged. Zero V2 episodes, CLOSED execution, disabled schedule, saved-only biology, no one-shot/continuous authority, no canonical provider call or external effect. No canonical schemas installed. All prior Pass-7 review-package members still match content hash `98a4c552869816a83380c42f2bf2d7d75b9880ad99d18e1edd12a7a1dc454e22`. Production source is byte-identical to the beginning of this investigation. See PRESERVATION.json.

## 19. Remaining blockers

The original regression remains reproducibly intermittent. Its rejecting condition is understood, but an evidence-supported correction that preserves the existing deadline contract has not been established. Changing timestamp origin, moving authoritative preparation, introducing retries or optimizing away checks would require further specific evidence; none was done speculatively. The isolated-stability, full-suite and new-build readiness gates remain open. Container and managed-host verification remain separate, unattempted infrastructure work.

SHORT-LEASE RECOVERY REMAINS UNRESOLVED — PASS 7 NOT READY

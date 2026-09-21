# Continuous local life: prepared installation path

**PREPARED / UNAPPLIED. This document is not activation authorization.**

`continuous-schema.sql` adds a separate `CONTINUOUS_LOCAL_V1` authority, durable private events, attempts, and an append-only transition journal. It replaces the database writer function with a continuous branch followed by the unchanged single-use branch. It does not alter the first-awakening mode, install a grant, enable a schedule, initialize an organism, or start a worker.

## Current executable boundary

- Only `ContinuousController.installFixtureSchema()` installs this SQL in code. It refuses any database other than `genesis_runtime_v1_test` and any schema outside `awakening_test_*`.
- No production entrypoint, public route, environment unlock, CLI cycle command, or migration-on-boot imports/starts `ContinuousWorker`.
- A newly constructed worker is disabled. An explicitly enabled library worker still requires a valid, separately authorized scope for every claim and commit.
- Only injected, operator-selected local deterministic planning is supported here. Model/provider fields are null and provider disclosure/permission is false. No external dispatch is installed.

## Future separately reviewed production installation

1. First-awakening execution and review remain separate. A non-fixture continuous scope requires at least eight persisted prior decisions; it cannot substitute for the one-shot seven-to-eight grant.
2. Review a fixed code release and SQL hashes. Verify identity, database row digest, original history, saved biology, disabled schedule and CLOSED execution; take an authenticated backup and prove restore on an isolated copy.
3. Install and verify the already-prepared Runtime V1 preparation and one-shot schemas in their reviewed order on the isolated copy. Then transactionally apply `continuous-schema.sql` there. Confirm the original seven-to-eight trigger branch, zero new decisions, all FKs/indexes/guards, and restart behavior. No boot migration.
4. Define separate migration owner, authenticated operator, worker, and read-only observer database roles. A worker must not own tables or possess scope creation/authorization privilege. Public observer credentials must not read the private queue/attempts/journal. Current fixture tests use an owner role; production least-privilege deployment is **not verified** by them. Review a narrowly privileged authorization/revocation service before granting table rights; do not rely on an operator-reference string as authentication.
5. Under separate installation authorization and stopped writers, repeat backup/integrity checks and install only the reviewed structural SQL into the intended production database. Verify no scope/queue/episode/decision was created. Do not silently rerun this non-idempotent SQL on an already-installed database.
6. Under a later, distinct authorization, issue a scope pinned to current runtime, constitution, policy, permission hash and exact local planner identity. Review event/effect allowlists, count/time/cost ceilings, expiry, issuer evidence, depth/backoff/wake rules. Fixture values are not production recommendations. Review local planner code as trusted executable code; events cannot supply a planner implementation.
7. Only an authenticated control surface may enable a supervised worker with an installed authorized scope. No `OPEN` boolean substitutes for authority. Keep the legacy schedule disabled, biology saved-only and external capabilities absent. Supervision, production metrics and operator reconciliation remain future work.
8. Revoke authority to prevent new claims and cancel active local claims; unresolved dispatch liabilities stay review-required. Recovery may only retry expired local claims within limits. Never resolve ambiguous paid/external outcomes automatically. No automatic reauthorization.

## Guarantees and limits

Postgres commits the decision, episode, Life State, intent, source-event consumption and child events in one transaction. Row locks, revision/lease fences and unique identities prevent duplicate local commits. A rolled-back local attempt may be planned again within explicit retry limits. This is not universal exactly-once processing: future external operations require separate durable dispatch/receipt/idempotency design and admission. No such operations are supported by this release.

Rolling budgets count claims, including failed attempts; they do not grant a free retry. Unresolved provider reservations never expire at a time-window boundary. Current local planners cannot charge a nonzero amount; cost-ledger checks are a fail-closed preparation boundary, not a paid-provider implementation.

No production values, credentials, deployment or canonical authorization are supplied by this document.


## Reviewed lease contract — Pass 7.2 preparation

Continuous ownership deadlines use one `clock_timestamp()` sample after claim locks and eligibility checks. Event, organism and attempt share that deadline; acknowledgement never renews it. A private `genesis_continuous_admissions` row is minted by the decision BEFORE INSERT trigger only after exact state/authority/disclosure checks and a final current-database-time expiry check. It binds transaction ID and attempt/token. Ordinary roles cannot insert, edit or invoke that proof mechanism directly.

All potentially lengthy context/policy/reducer/intent/follow-up validation precedes the insert. After admission, only bounded local writes remain under the organism/authority locks through COMMIT/ROLLBACK. Those writes may complete after expiry; a competing recovery/revocation must serialize and reread the result. An expired claim before admission is refused. No renewal, duration increase or retry expansion is introduced. One-shot and provider rules remain separate.

Lock order is organism first on every cooperating mutation path. Life State, scope/schedule, attempts/event and control/review rows are then locked while that organism lock is continuously held. Operator paths may lock control before the secondary rows but cannot hold it while competing for organism ownership. The review-insert trigger also takes organism first. No post-admission arbitrary callbacks exist in runtime code; crash injection belongs to test-side driver wrappers.

Prepared SQL/catalog and runtime identity have changed. Review/install only the new exact release through the existing explicit installer; do not reuse old authority hashes or install on boot. No production lease duration is selected. Unknown dispatch or COMMIT acknowledgement requires durable inspection, never blind retry.

# Runtime V1 migration report

**Applied:** explicit additive migration 003, 2026-09-20. Genesis stayed dormant.

## Safety sequence

1. Independently exported canonical rows in a read-only repeatable-read transaction. Baseline matched `3377c9dddbe2abf89ed9a820a6aabbc1da951cac7bfc1823471c5aac043ea312`; one organism, seven decisions/memories, one project, four ledger/milestones, two migrations, disabled schedule.
2. Saved a private mode-0600 backup. Restored it into disposable schemas of the dedicated `genesis_runtime_v1_test` database and reproduced the exact baseline digest.
3. Verified additive migration, idempotency, empty/wrong/active-schedule refusal, writer fencing, authenticated/manual/scheduled blocking, direct API privacy, intent concurrency, and fresh runtime process restarts in isolation. Full suite: 74 passing tests before canonical apply.
4. Verified 9,319 protected file hashes. Confirmed no candidate runtime/CLI worker and no other canonical database client. Exact baseline, original identity/birth/brain/history, seven cycles, all schedule fields and absence of lease were rechecked.
5. Invoked `scripts/runtime-v1-apply.ts --apply-reviewed-baseline` with the existing private database environment. The script checks the tested SQL/migrator hashes, backup/dry-run evidence and preservation audit. It never imports a neural model.
6. Inside the transaction: schema advisory lock; sorted original-table write-excluding locks; digest check; organism then schedule row locks; create reviewed tables/triggers/extension/admin event; compare every original row; commit only if identical.
7. Read-only post-audit confirmed all original rows unchanged, CLOSED lock, disabled schedule, zero other clients, seven decisions/cycles and zero intents.

## Exact tested migration

| Artifact | SHA-256 |
|---|---|
| `runtime/migrations/003_runtime_v1.sql` | `634da03cc27cebad2de2d2797dc79b2af6b69d3e060bdf07f10c45dccec098c8` |
| `runtime/migrate-v1.ts` | `687d59ce89d24fa472aef47a80741a37e299ac57b3ef6874ceecd911cd5de1ff` |

The canonical apply refused any mismatch from the isolated dry run. No existing organism initialization was called.

## Outcome

- **BEFORE_DATABASE_DIGEST:** `3377c9dddbe2abf89ed9a820a6aabbc1da951cac7bfc1823471c5aac043ea312`
- **AFTER_DATABASE_DIGEST:** `4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`
- **ORIGINAL_ROW_PRESERVATION_RESULT:** identical, including serialized brain bytes and every schedule field.
- **NEW_SCHEMA_DELTA:** three tables plus versioned-writer and append-only triggers/functions.
- **NEW_ROWS_CREATED:** one extension, one administrative event, one schema-migration row; zero life decisions or action intents.

`003` metadata and its event are not an eighth experience. New arrays are empty; no historical interests, beliefs or relationships were fabricated. Existing computational rhythm is copied into the extension without resetting it. Wallet binding is unresolved.

## Compatibility and rollback

Runtime startup is read-only and requires the migrated existing life. Legacy original-table writers without the version marker are rejected; CLOSED also rejects marked writers. Decision/memory/event mutation is independently blocked. Privileged database administration is not an untrusted-user security boundary and must remain restricted.

Library-level repeat migration is idempotent on an already migrated dormant fixture. The **canonical baseline-specific CLI intentionally refuses a second apply** because the original pre-migration digest no longer describes the expanded database. Do not weaken that check.

Rollback is a read-only application rollback/forward repair with the additive records retained, not restoration over live identity or deletion of extension tables. No V2 life cycle has occurred. A new host must restore the complete same database into an isolated verification environment first. Old V1 writers must remain fenced.

# Recovery and rollback — prepared procedure

No recovery is performed automatically by observation boot. A database restore can resurrect consumed authority or erase provider liability. Database-local hashes cannot detect facts lost with the database. **An external incident/backup/dispatch evidence record and operator review are mandatory before any consumer starts after restore.**

## Backup and restore drill

Use a separately authenticated backup identity or migration owner, never browser/runtime worker. Stop consumers; record code/image digest, exact Node/OS/architecture identity, complete SQL catalog, all row hashes, sequence values, authority status, claims, receipts, unresolved provider reservations and independently retained provider/launch audit references. Use private encrypted storage with bounded retention/access. A consistent PostgreSQL logical dump and managed PITR serve different purposes; verify both at the chosen host.

Restore first into a **new empty database**, same schema name, isolated network, no consumer/provider secret, no production service pointing at it. Restore roles/ownership/ACLs explicitly (managed role availability differs). Compare identity, birth, decisions, memories, Life State, artifact histories, grants/scopes/events/leases, attempt/receipt/liability rows, schema definitions, sequence values and permissions. Boot only dormant observation. `/readiness` must match the exact release, or stop. Never initialize a replacement organism.

The local automated drill uses `pg_dump` and `psql --single-transaction --set ON_ERROR_STOP=1` in `tests/support/deployment-restore.ts`, with disposable schema renaming, no owner/ACL transfer and complete row/catalog comparisons. Both an empty-authority dormant fixture and a fixture with one-shot/continuous decisions and provider receipt were restored. The managed drill must additionally verify backup encryption, RPO/RTO, PITR, role restoration, CA/hostname and network fences.

## Incident response matrix

| Incident | Automatic behavior | Required private review | Authority / continuation |
|---|---|---|---|
| Observation process crash/restart | GET service stops/restarts; no claims or writes | Health/readiness, DB row check if unexpected | No execution starts |
| Worker crash before claim | No claim may exist; unique launch audit may already exist | Inspect launch receipt and durable attempt | Never rerun the same launch blindly |
| Crash during/after provider dispatch | Reservation/dispatch or receipt persists; unresolved attempt retains liability | Inspect attempt, immutable receipt, provider evidence and commit | No second request; do not invent not-sent/success |
| DB restart/failover/commit acknowledgement lost | DB transaction atomicity; caller may not know outcome | Fresh read of decision/grant/intent/attempt/receipt | No retry until exact state known |
| Worker dies during local-only cycle | Lease/attempt remains; reviewed local recovery may close/requeue under existing bounded semantics | Inspect stale fence, event, committed decision before restarting explicit session | No duplicated committed decision; paid retry forbidden |
| Provider outage/malformed response | No implicit fallback; conservative failure/liability | Admission, accounting and durable response classification | Separate review, no second first-awakening attempt |
| Lost deployment | No consumer runs; DB remains source of identity | Recover immutable image and original DB, never create organism | Match runtime hash before any authority use |
| Bad deployment/schema mismatch | Readiness false; consumer preflight refuses | Verify exact image/catalog/SQL map | No repair on boot |
| Application rollback | Stored release and grants bind exact implementation/platform | Stop consumers, inspect pending effects, revoke under authenticated control, choose compatible forward release | Old code against new release fails; compatibility amendment required |
| Database restored from old backup | Observation only; no automatic continuation | Compare out-of-band provider/dispatch/launch records; fence old hosts, rotate worker credentials, resolve lost claims | Restored AUTHORIZED rows are not permission to resume without review |
| Operator credential compromise | No promise of immediate in-flight cancellation from key rotation alone | Disable actor/key, revoke both authority classes, inspect audit/disclosure, rotate DB login where necessary | Stop consumers; new explicit authority only after review |
| Provider credential compromise | Observation unaffected | Stop/revoke provider admission and active grants, rotate secret, inspect billing externally | Unknown billing remains unknown |
| Public observer unavailable | Observation lost; DB/controller protections independent | Restore frontend/runtime connectivity | Does not authorize or stop cycles by itself; use private stop |

## Shutdown and reconciliation

Observation SIGTERM/SIGINT closes listeners/idle connections, bounds drain and ends pool; outer hard deadline is 12 seconds. Consumer signal stops new local claims and cancels active one-shot through its existing fence. Potential dispatch remains conservative even if shutdown exceeds grace. Host kill/DB outage can leave ambiguity; never log it as success. Reserve host termination grace above application deadline and verify it on Linux.

Operator inspection is via existing authenticated operations `inspect_grant`, `inspect_attempt`, `inspect_recovery`, `inspect_provider_attempt`, `inspect_queue`, `inspect_scopes`. `emergency_stop` requires both authority-management capabilities. Recovery dispositions and provider reconciliation record evidence; they do not manufacture a missing biological/computational outcome. Preserve original failed records.

## Rollback limits

Prepared installation is transactional, no destructive down SQL. Once V2 decisions exist, restoring an older database discards history and can invalidate external accounting; it is a disaster-recovery decision, not a routine rollback. Deployment-release records are immutable. New code/Node version changes identity; a separately reviewed compatibility/upgrade procedure is required, not editing stored hashes to make readiness green. Never reauthorize merely to clear an alert.

### Historical images without the Pass 7 guard

A new compatibility check cannot retrofit an old binary. The mismatch tests exercise this release against a different stored release/catalog; they do not prove that every pre-Pass7 image would reject HTTP startup. Do not put pre-guard images in the production rollback allowlist. Prepared installation begins with zero authority, and new grants/admissions are pinned to the new code, so old code cannot consume those new authorities through its validated path. For any later upgrade, stop consumers and reconcile/revoke prior authorities before reviewing the new release. An owner or arbitrary historical script is not an admitted consumer.

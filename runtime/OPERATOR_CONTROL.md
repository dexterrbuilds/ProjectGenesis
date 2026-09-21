# Private operator control v1 — prepared, not activated

This control plane manages existing authority; it cannot execute a cycle, supply a planner callback, open the execution lock, run SQL, start a worker, or admit a provider. Canonical installation, actor provisioning and all real authorizations require separate review. No example below is an activation instruction.

## Deployment boundaries

Install, under an offline migration owner, the existing 001/002/003 schema, `preparation-schema.sql`, `one-shot-schema.sql`, `continuous-schema.sql`, then `operator-schema-v1.sql`. These last four remain **prepared/uninstalled canonically**. Back up and verify restore before any reviewed installation. No boot migration. `installFixtureSchema` refuses any database except `genesis_runtime_v1_test` in an `awakening_test_` schema.

`operator-role-grants.sql` is a reviewed-installation template using psql identifiers `schema`, `observer`, `worker`, `operator`. It neither creates login credentials nor selects production infrastructure. Set search_path to the dedicated trusted schema before applying it; remove untrusted schema CREATE rights and inspect inherited/default grants. Grant groups to separate non-owner service logins. Do not use the local database owner/superuser for services.

| Role | Boundary |
|---|---|
| PUBLIC_OBSERVER | SELECT narrow `genesis_public_identity` view only; no raw private tables, writes, sequences, authority or DDL. The full public product must consume the existing allowlisted service projection; this identity-only SQL view does not replace those DTOs. |
| RUNTIME_WORKER | Private source SELECT, bounded current-state/claim/intent/provider-attempt/queue updates and append-only episode/decision writes; writer fences remain required. No authority INSERT, authorization-record UPDATE, disclosure/audit/actor INSERT, schedule enable/due-time UPDATE or human-response intake. A heartbeat-only column grant permits PostgreSQL row-share locking; it cannot enable scheduling. |
| PRIVATE_OPERATOR | Private SELECT; audit/review/recovery INSERT; proposal/authorization/revocation and intake writes. Cannot rewrite historical decisions/memories, organism identity, actors, schedule, triggers or schemas. Per-actor capabilities are enforced in the private application above this shared DB role. |
| MIGRATION_OWNER | Offline schema/role and non-secret actor provisioning only. Never used by runtime, observer, or operator process. Owners/superusers can bypass triggers and permissions; compromise of this role is outside the application trust boundary. |

The worker privilege draft covers local cycles. Future production provider admission will need a separately reviewed provisioning path for `genesis_provider_grants`; no worker INSERT permission is supplied here. No signing, provider factory or external executor exists in this entrypoint.

## Authentication and entrypoint

Only `runtime/operator-cli.ts` exposes commands. It is not imported by Next routes or runtime boot. Run manually only in an explicitly configured **private operator** environment; it reads one JSON command from stdin (32 KiB maximum) and exits. Stdout is PRIVATE operator output. Do not publish it, record raw stdout indiscriminately, or route it to a public log collector.

Required configuration:

- `GENESIS_PRIVATE_OPERATOR_MODE=enabled`
- `GENESIS_OPERATOR_DATABASE_URL`: non-owner PRIVATE_OPERATOR login, TLS/network access reviewed at deployment; never canonical owner credentials.
- `GENESIS_OPERATOR_AUTH_FILE`: protected operator authentication configuration, mode `production`. JSON shape: `{enabled:true, mode:'production', keys:[{id,actorId,sha256,expiresAt}]}`. Use valid JSON double quotes in an actual file. `sha256` is the digest of a high-entropy external bearer credential, not its plaintext.
- `GENESIS_OPERATOR_CREDENTIAL`: supplied through the operator's protected process environment, not shell arguments, Life State, provider context or SQL.

No production values have been generated or installed. Missing/invalid configuration, a test config at the production CLI, invalid/expired credential, missing actor or disabled actor fail closed. Comparison uses SHA-256 plus constant-time digest comparison. Principals are frozen objects verified by a private WeakMap, expire after at most five minutes, and cannot be forged with actor/issuer strings. Capabilities are reread from the non-secret SQL actor on each command. Rotation reloads config and invalidates every previously issued principal; the short-lived CLI reads fresh config every invocation. Removing a key or disabling an actor prevents subsequent operations. Already committed commands are historical facts, not retroactively undone.

Only hash metadata belongs in the external auth file. Protect it (and environment/process inspection) as credential material. There is no HTTP login surface, browser session, signup, public token distribution or distributed brute-force endpoint. Deployment must restrict host/private access. A compromised operator process or its DB login is privileged; this library is not a sandbox against arbitrary code running under that identity. A production operator UI, SSO and automated key provisioning are deferred.

## Command contract

Strict envelope: `id`, `organismId`, `operation`, `targetId` (nullable), `expectedHash` (nullable), `reasonReference`, `payload`.

`id` is a unique request/audit identity; duplicate IDs fail closed without repeating a mutation. On a lost CLI response, inspect the audit/database rather than resubmitting with a different ID. `reasonReference` is a bounded reference, never full evidence or a human answer. Changes to a target require its exact row hash from private inspection. Proposal and authorization are separate authenticated operations. No command accepts code, arbitrary SQL, an unrestricted capability manifest, a raw provider response or a planner callback.

| Capability | Operations |
|---|---|
| VIEW_PRIVATE_STATE | readiness, inspect_state, inspect_source (bounded eligible legacy source preview) |
| REVIEW_DISCLOSURE | disclosure_sources, inspect_disclosure, review_disclosure |
| MANAGE_ONE_SHOT | inspect_grant, propose_grant, authorize_grant, revoke_grant, cancel_grant |
| MANAGE_CONTINUOUS | inspect_scopes, inspect_queue (events/attempts/resources), propose_scope, authorize_scope, revoke_scope, cancel_event |
| INSPECT_RECOVERY | inspect_attempt (one-shot), inspect_recovery (dispositions/provider accounting) |
| RESOLVE_RECOVERY | mark_expired_claim, recovery_disposition, provider_reconcile |
| MANAGE_PROVIDER_ADMISSION | provider_readiness only — returns PENDING; no admission mutation |
| BOTH authority-management capabilities | emergency_stop |

One-shot proposal payload is the existing strict grant schema. Continuous proposal payload is the existing strict scope schema. Authenticated actor must match proposal issuer; the authorizing actor is separately recorded in the journal. Authorizers cannot change payloads. One-shot and continuous permissions remain independent; neither starts execution.

## Durable disclosure

Review payload: `sourceType`, `sourceId`, `sourceHash`, `audience`, `decision`, `expectedVersion`, `expiresAt` (nullable). Inspect catalog for exact canonical hash; inspect existing review for its row hash/version. Audiences are independent `INTERNAL_USE`, `PROVIDER_DISCLOSURE`, `PUBLIC_DISCLOSURE`. Decisions are append-only APPROVED/DENIED/REVOKED/EXPIRED. A clock expiry or source mismatch is an effective exclusion without rewriting a review.

Reviewable for provider/public: credential-filtered legacy memory retrieval records and explicitly bounded legacy project metadata (`id/name/status/workCycles`). No implicit approval of the original seven memories. Public approval is eligibility only, not a new public endpoint.

INTERNAL_ONLY: V2 episodes, semantic assertions, Pass-3 projects/tasks/artifacts/versions/interests/questions/commitments/relationships/assistance/human answers/focus. Internal use can be restricted by review; provider/public elevation is refused. This deliberately preserves Pass-3 privacy contracts. Changing these transfer limits needs another reviewed schema/policy. `PUBLIC_DISCLOSURE` never makes provider use legal. Local reasoning remains possible without provider disclosure.

Preparation and commit load the same durable catalog/review interpretation under the existing organism lock. The context text and private manifest bind installation state, review epoch, IDs/versions/hashes, source hashes, audience and actual-clock expiry interpretation. Installed stores ignore ad-hoc caller review overrides. Any set/epoch change conservatively invalidates existing preparation, including changes to unselected reviews. Max 256 latest per-source/audience reviews: overflow refuses context instead of silently dropping authority. Source edits require new review. Provider reservation/dispatch also recheck durable disclosure; revocation after a request has already crossed the dispatch boundary cannot retract data already sent. No real transport is implemented here.

Provider manifests contain metadata, bounded omission lists and byte totals; never contents, auth keys, reasons or evidence. Private context includes factual identity/constitution/economy/permissions/non-applied biological status plus eligible reviewed historical excerpts and project metadata. Private operational descriptions, relationships, answers and unreviewed environmental text are excluded. The fixture-only context inspector invokes no planner and persists no event.

## Transactions, stop and recovery

Every accepted privileged command and authenticated capability refusal gets an append-only audit with actor/capability, target, old/request/result hashes and runtime identity. Changes and audit commit together. Disclosure/recovery rows have deferred audit FKs. Journal write failure rolls back the change. Invalid authentication, invalid envelope/target and duplicate IDs are rejected before mutating; no unauthenticated actor record or raw invalid payload is fabricated in the journal. CLI errors are generic. The transactional adapter keeps existing controller subtransactions inside the outer savepoint; no nested commit can escape it.

Emergency stop revokes proposed/active one-shot grants and continuous scopes, cancels active work via existing fences, preserves pending work, and leaves terminal ambiguities stopped. A one-shot possible provider dispatch becomes AMBIGUOUS, not a reusable revoked grant. Repeated stop is safe. There is no managed worker process here to signal; existing worker authority checks observe durable revocation at phase/poll/commit boundaries. No new worker is started.

Recovery is an append-only administrative fact. `UNRESOLVED_REMAIN_STOPPED` never grants certainty. `CONFIRMED_LOCAL_COMMIT` requires matching V2 decision and episode ownership/linkage. No-effect requires no unresolved provider attempts; reconciled zero cost is insufficient without an explicit not-executed fact. External-without-local-commit requires established provider response/billing evidence and no local commit. Operator evidence is a reference/hash, not proof automatically verified by the software. Terminal grants/events remain terminal even after reconciliation. No same-claim retry, requeue or reopening operation exists.

Provider reconciliation payload: `fact` (PROVIDER_UNKNOWN / PROVIDER_NOT_EXECUTED / PROVIDER_BILLED), `costMicros`, optional structured `usage`, nullable `responseId`, `evidenceHash`. Unknown keeps cost null and reservation liability. Not-executed requires explicit zero with no invented usage/response. Billed accepts externally established usage/cost within the existing reservation; overruns require further investigation. Known amounts are appended as recovery facts and update the existing accounting record atomically. They never create decision content or a new attempt. Reconciliation is not provider admission.

Human intake requires RECORD_HUMAN_RESPONSE, existing request provenance, exact revision, attributed respondent and bounded private untrusted content. Answer ingestion leaves status answered (not resolved), appends an administrative input, and optionally enqueues the existing explicit wake event. Wake defaults false and cannot create authority or execution. No communication client is involved.

## Verification and remaining work

See `verification/operator-control-pass/OPERATOR_CONTROL_REPORT.md` and the fixture tests. Prepared SQL/role tests do not establish production IAM/network/backup readiness. Provider implementation/admission, production migrations/roles/secrets, deployment, an execution entrypoint, human disclosure review, awakening and continuous activation remain separate steps.

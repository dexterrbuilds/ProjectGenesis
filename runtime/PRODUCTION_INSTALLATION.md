# Production installation — prepared, not executed

## Scope and topology

No command in this document has been run against production. Genesis remains dormant. Use a reviewed immutable code/image artifact, PostgreSQL 16, and Node 24/Linux. Runtime identities include the exact Node version, OS, architecture and source hashes: calculate production identities **inside the final image**, never copy the macOS fixture identity.

* **Next.js public observer:** Vercel, repository root, `npm ci`, `npm run build -- --webpack`, Node 24 selected in the project. No DB, operator or provider credentials. `GENESIS_PUBLIC_MODE=dormant` preserves the landing page. Its later public live projection proxies fixed routes to `GENESIS_API_URL`; changing presentation mode grants no execution authority.
* **Observation runtime:** one persistent container, `node runtime/main.ts`, `GENESIS_RUNTIME_MODE=dormant`, read-only observation DB login, fixed expected organism/birth. No migration, initialization, scheduler, wallet observer, planner or worker starts on boot.
* **Private administration:** trusted host or private one-off job from the exact image. Separate operator DB credential and authenticated operator credential/configuration. No public administration HTTP service.
* **One-shot/continuous consumer:** `node runtime/deployment/consumer-cli.ts`, explicitly invoked private process, separate operator and worker connections, exact single-use launch request. Never the container default command. Continuous sessions are local deterministic only, maximum four minutes per explicit launch; restart cannot reuse its launch receipt. This is not a paid continuous planner.
* **PostgreSQL:** private networking where available, verified TLS otherwise and preferably within private networking. Use a direct connection or verified session-pooling endpoint; transaction-pooling endpoints must not be assumed compatible with search_path/session settings, role identity and controller transactions. Managed storage, backup/PITR, alerts and capacity are infrastructure obligations. The public frontend has no database route.
* **Provider:** separately admitted future endpoint. No model/tariff/endpoint/key is selected here. Generic JSON gateway protocol is implemented; an incompatible native vendor protocol needs a separately reviewed adapter.

## Before any install

1. Confirm the intended managed target with the operator. Do not create/link a project by inference.
2. Stop all consumers. Preserve the existing organism; do not run `import-life`, demo, legacy migrate or organism initialization. Verify exact identity, birth, seven decisions, seven original memories, zero V2 episodes, CLOSED lock, disabled schedule, saved biology. Export **all rows**, retain privately, and compare the historical digest `4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`. A production copy may have explicitly reviewed operational differences; any unreviewed difference stops installation.
3. Obtain encrypted native backup/PITR and logical backup. Restore into a **different empty database**. Compare all rows, schema catalog and sequence state, not merely counts. Perform the managed-host restore drill described in RECOVERY_RUNBOOK.md. The local fixture drill is evidence of tooling behavior, not managed-service recovery.
4. Verify current schema is exactly the pinned baseline catalog (`001`, `002`, `003`). No partial preparation schema is accepted. The additive installer deliberately does not create a new organism or migrate an empty database. Transport/restoration of the existing canonical database to a managed target is a separate explicitly reviewed operation.
5. Provision separate migration-owner, runtime-reader, worker, public-observer and private-operator roles/logins. Group roles are existing `NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS`, distinct, with no parent memberships. Dedicated login accounts may inherit exactly one appropriate group. Audit all pre-existing role memberships and grants. Owner/superuser credentials bypass database protections and must never reach normal services. Ensure normal groups cannot CREATE in the selected schema.
6. Store a private roles JSON containing keys `observer`, `reader`, `worker`, `operator` and exact group names. Provide the schema owner credential **only to the installer process**. Do not embed it in an image or ordinary runtime environment. An existing owner may provision roles explicitly; the installer neither creates credentials nor chooses role identities.

### Reviewed DBA role provisioning template (not run)

On the isolated managed target, the DBA supplies the actual role names. The following defines the intended attributes; do not reuse a pre-existing role without inspecting its memberships and privileges. No passwords are placed in SQL files or command arguments.

```sql
CREATE ROLE genesis_migration_owner LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS;
CREATE ROLE genesis_observer NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS;
CREATE ROLE genesis_reader NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS;
CREATE ROLE genesis_worker NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS;
CREATE ROLE genesis_operator NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS;
```

Managed DBA provisions a **different** LOGIN account for each normal process, with the same restrictive attributes, and grants exactly its one group. Review database CONNECT privileges, schema ownership and existing grants; restore the Genesis objects under the migration owner using the approved restore procedure. The normal accounts must not inherit migration owner. Provision credential values via the host secret facility/private password prompt, not an example default. Reader login may additionally default to read-only transactions; table grants enforce read-only even if that setting changes. `GENESIS_DB_ROLE` is fixture-only; production connections must actually authenticate as the dedicated least-privilege login. No role/credential is created by runtime boot.

Expected result: reader can select projection input only, observer only the identity view, worker and operator independently meet the negative privilege tests. Any inherited owner/schema/authority privilege is a stop condition, not something the installer silently strips. Rollback before installation is DBA-reviewed removal of only the newly created, unused roles; never DROP OWNED on a live organism database.

## Plan and dry run

Set only the installer environment described in ENVIRONMENT.md: `NODE_ENV=production`, `GENESIS_MIGRATION_MODE=explicit`, migration URL, verified TLS/CA, target schema, expected organism and birth, roles file and a **new** private plan file path.

```sh
node runtime/deployment/installer-cli.ts plan
```

Expected: sanitized target (host/port/database/schema), `dryRun:true`, plan hash, mode-0600 plan file; **zero DB writes**. Independently inspect the file: exact target, identity, seven-decision expectation, current row hash, runtime hash, SQL hash map and role names. The plan's `rowHash` uses recursively sorted JSON and is a different documented digest object from the historical row export; do not compare unlike hashes. Keep the historical export comparison as a separate prerequisite.

Fail closed on unknown columns/functions/triggers/views/indexes/sequences, changed identity, active lease, enabled schedule, V2 episode or unknown migration state. Do not repair or regenerate around a failed review.

## Explicit additive installation

Set `GENESIS_INSTALL_ACK=INSTALL_REVIEWED_PLAN:<exact reviewed plan hash>` and run, only under future authorization:

```sh
node runtime/deployment/installer-cli.ts apply
```

The transaction takes the schema advisory lock and locks baseline tables. It rechecks target, SQL/runtime identity, catalog and all existing rows. Order:

1. `runtime/preparation-schema.sql` — cycle and provider preparation records.
2. `runtime/one-shot-schema.sql` — grants and exact one-shot writer fence.
3. `runtime/continuous-schema.sql` — separate scopes/events/attempts/journal; extends the writer fence.
4. `runtime/operator-schema-v1.sql` — actors, immutable audit/reviews/recovery, control-state seed and private identity view.
5. `runtime/provider-integration-schema.sql` — admitted provider records and immutable receipts.
6. `runtime/deployment/release.sql` — release binding, immutable release row, CLOSED-only Life State constraint.
7. Existing operator role grants, provider role grants, additional observation-reader grants and default privilege restrictions.
8. Insert deployment release identity; compare full installed catalog; verify **every pre-existing row unchanged**; commit atomically.

No grant, scope, actor, review, provider admission or attempt is created. New administrative rows: one control-state seed and one deployment-release row. All cycle-related tables are empty. Applied historical migration rows remain unchanged; the deployment-release record tracks this additive installation separately.

If preflight/SQL/postverification fails, transaction rolls back. If connection loss makes COMMIT acknowledgement uncertain, inspect from a fresh privileged read-only session: either baseline catalog or full installed catalog/release must match. Never retry `apply` blindly. Installer refuses an already-installed or partially-installed state. Down-migration is not supported; use compatible forward remediation under review, or a verified restore with all effects fenced off.

## Verify roles and remove owner credentials

Repeat the prepared role tests on the managed host: public identity view only for observer; read-only private-input access for observation runtime; worker unable to create grants/reviews/actors, enable schedule, OPEN lock, alter schema or disable triggers; operator unable to rewrite historical decisions or schema. Authenticate actor provisioning by the owner separately; actor creation is not execution authority. Test login inheritance, search_path, TLS hostname/CA verification and limits. Review owner memberships, SECURITY DEFINER functions and grants to PUBLIC. Do not assume a role name proves least privilege.

Normal roles cannot remove the CLOSED constraint or change release identity. Trigger functions are not publicly executable. Reader receives private SELECT because projection is server-side; its credential is therefore sensitive and is never given to Next/browser. PUBLIC_OBSERVER receives only `genesis_public_identity`.

## Dormant runtime and observer

Remove owner credentials. Run the final image with observation-reader credentials, exact identity and `dormant`. Check `/health` (liveness) and `/readiness` (schema, release, identity, CLOSED, schedule disabled). DB failure returns generic unavailable; liveness can remain healthy. Railway readiness uses `/readiness`, bounded ON_FAILURE retries (10). Keep workers absent.

Probe `/api/state`, `/api/history`, `/api/brain` from the intended frontend path. Public DTOs only; runtime ignores browser authorization and accepts GET only. Deploy Next with Node 24 and the prepared Webpack build. Confirm HTTPS origin, redirect refusal, CSP/edge policy as appropriate, request limits and target egress/DNS. Dormant landing does not require runtime credentials. No NEXT_PUBLIC secrets.

Wait and restart both services; compare DB rows and canonical digest. No heartbeat, event, provider attempt or decision should appear. Repeat infrastructure TLS, shutdown, backup, CPU/memory, connection-count and logging tests. Docker/Linux execution and managed networking remain unverified until this step.

## Private operator, provider and smoke prerequisites

Use private operator CLI with reviewed auth file and credential, exact runtime image and separate operator DB login. Responses may contain private bounded inspection; stdout goes only to a trusted terminal/private storage. Every operation uses a unique command ID and durable audit; uncertain acknowledgement requires inspection, not fresh retry by default.

Provider admission requires verified exact endpoint/protocol/model, complete tariff categories, conservative complete-request counting, retention/disclosure review, secret reference and budgets. Keys alone authorize nothing. Sanitized provider smoke requires its own explicit authorization, journal and later billing reconciliation; no canonical planner/cycle runs. Do not invoke it as an installation test.

## Review gates

Only after verified infrastructure, backup restore, authenticated operator, provider admission/smoke and human disclosure review should AWAKENING_RUNBOOK.md be considered. Installation is not awakening authorization. Continuous scope and consumer are a separate later decision after Decision 8 review. Keep wallet, internet, messaging, biology and legacy schedule disabled throughout.

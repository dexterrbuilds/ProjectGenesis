# Project Genesis — Pass 7: Deployment Preparation

## 1. Executive summary

Prepared an explicit dormant observation service, read-only readiness checks, a reviewed-plan additive installer, least-privilege roles, private existing-authority consumers and production/recovery runbooks. No production service, credential, provider admission, canonical schema, grant or scope was created.

Deployment is a topology and governance operation, not adding an API key. Next is a public observer; the runtime serves public projections from private read-only input; administration and cycle consumption are separate private processes. Paid reasoning remains separately admitted and limited to one-shot execution. Continuous-local sessions use the existing deterministic planner and cannot become paid reasoning through environment configuration.

**This pass is not yet deployment-ready:** the final complete suite returned **532 passed, 1 failed, 0 skipped (533 total)**. All 17 new deployment cases passed. The existing short-lease crash-recovery regression remains unresolved; it must be reliably verified without weakening its safety limits. TypeScript, ESLint, Webpack build and dormant observer/runtime E2E passed. Actual Docker/Linux and managed infrastructure execution remain unverified. See CHECKS.json and retained failure evidence.

## 2. Canonical preservation

Read-only exports were taken before and after this pass. Actual digests and row-by-row comparison are in PRESERVATION.json. Private complete exports remain mode 0600 under `outputs/deployment-preparation-pass/`; no memory contents, credentials or operator evidence are copied into this review package.

Expected original identity: `817e772c-827e-48fc-8e35-6504cb2a8d2d`, birth `2026-09-15T01:56:07.867Z`. Seven historical decisions and seven legacy memories, original project/ledger/milestones/biological snapshot. Zero canonical V2 episodes. CLOSED execution, disabled schedule, saved-only biology. Canonical preparation/operator/provider/authority tables remain uninstalled; no authority/review/admission/attempt was created.

The canonical before/after row digest is **`4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`**, with every exported row unchanged. The live canonical baseline catalog also matches the prepared installer in a separate read-only transaction.

Frozen research and prior verification packages are checked separately in FROZEN_PRESERVATION.json: all **9,319 frozen files / 15,967,076,255 bytes** match. Eight self-contained review packages match. Two older manifests describe historical repository-source snapshots: their manifest identity and archived verification members match, while their historical live-source entries differ after authorized implementation passes. Those old source snapshots are not misreported as current-code matches. Existing pre-pass working changes were retained. This pass's file inventory is based on the start-of-pass file-hash snapshot rather than claiming the entire dirty Git diff.

## 3. Production topology

Vercel Next observer → fixed public GET proxy → HTTPS observation runtime → PostgreSQL read-only projection input. Private operator CLI and explicit private consumer use different credentials and are never exposed through public routes. Private consumer has operator and worker connections; provider secret exists only for a specifically admitted one-shot/authorized smoke process. Migration owner is separate from every normal service.

The observation runtime and private jobs can use one immutable image on the persistent host. They are separate process types and environments, not necessarily permanent separate services. No always-running worker is part of initial deployment. PostgreSQL is the identity/history authority. Browser/session lifetime is irrelevant to persistence.

## 4. Runtime entrypoints

ENTRYPOINT_INVENTORY.json identifies public, runtime, private operator, worker, migration, test-only and deprecated paths. Container default remains `node runtime/main.ts`. `runtime/deployment/installer-cli.ts` requires explicit plan/apply. `runtime/deployment/consumer-cli.ts` requires authenticated strict stdin request and existing exact authority. `runtime/operator-cli.ts` has no cycle-execution verb; sanitized provider smoke remains a separate explicitly authorized command.

Historical migration/import/demo/life scripts are not production startup. Legacy migration CLI is now refused under NODE_ENV=production. Fixture installers still refuse non-test targets. No public control endpoint issues authority or consumes it.

## 5. Dormant boot

`dormantMode` requires explicit `GENESIS_RUNTIME_MODE=dormant` and exact expected identity/birth. Unknown/absent mode and conflicting enabled autonomy/internet/worker/scheduler/provider flags are refused. Provider/wallet credential configuration is rejected in the observation process. Docker declares dormant mode explicitly; direct process invocation must also supply it.

Boot creates no rows, leases, events or heartbeat. It verifies frozen evidence and serves read-only requests. No scheduler, wallet observer, neural advancement, planner or worker is started. Missing database/schema never initializes a new organism.

## 6. Health/readiness

`/health` and compatibility `/healthz` report process liveness only. `/readiness` checks an installed schema catalog, exact runtime/source/platform identity, SQL hash map, original identity/birth, CLOSED execution and disabled schedule, within a read-only transaction. The observation service also verifies ordinary read-only role privileges. Failed readiness blocks public organism projections; it does not hide DB failure behind healthy liveness.

Responses expose no schema definitions, DB error messages, secrets, private values or internal hashes. Non-GET requests are refused. Operator headers are ignored. Readiness failure is a generic 503. Public request concurrency/rate and connection bounds are local safeguards; edge/ingress verification remains required.

## 7. Schema inventory

SCHEMA_INVENTORY.json records ordered SQL hashes, dependencies, versions, canonical installation status, row effects, rollback limits and defined objects. Full normalized PostgreSQL16 catalogs under `runtime/deployment/catalog-*.json` include columns/defaults, constraints, indexes, functions, enabled triggers, views and sequences. Unknown/partial schema is refused.

Historical 001/002/003 remain installed canonically and byte-unchanged. One-shot, continuous, operator, provider and deployment schemas remain prepared. Replacements of `genesis_require_v2_writer` are intentional in dependency order, not duplicate independent authority. Runtime V1 preparation SQL is shared by the controllers and installed once.

## 8. Migration installer

`planInstall` reads a known baseline and emits exact target, identity, current row hash, runtime identity, SQL hashes and role names; no mutation. `applyInstall` requires `INSTALL_REVIEWED_PLAN:<hash>`, independently rechecks all bindings, takes advisory/table locks, installs in one transaction, verifies complete installed catalog and every pre-existing row before commit. CLI prints sanitized target before connecting/applying and writes new private plan files exclusively.

Unknown schema, changed SQL/code/rows/target, bad acknowledgement or excessive role privileges fail closed. The installer accepts the existing reviewed 001–003 seven-decision dormant baseline; it does not initialize an empty database. Already-installed/partial states are not guessed or repaired. Ambiguous COMMIT requires fresh inspection.

## 9. Migration order

Reviewed backup/restore and identity export → baseline catalog → prepared cycle/provider records → one-shot → continuous → operator → provider admission/receipt → deployment binding/CLOSED constraint → operator/provider/reader grants → full catalog and old-row verification → commit. Operator control-state seed and deployment-release record are administrative; no life cycle, actor, authority or admission is inserted.

See PRODUCTION_INSTALLATION.md for exact commands, prerequisites, expected outputs and stop conditions. No canonical installation occurred.

## 10. DB roles

MIGRATION_OWNER owns/provisions; RUNTIME_WORKER has narrowly listed cycle writes; PUBLIC_OBSERVER sees only the public identity view; PRIVATE_OPERATOR has control operations without historical/schema ownership; additional observation READER can SELECT private input for server-side projection but cannot mutate. Frontend gets none of these credentials.

Disposable role tests exercise real PostgreSQL permissions, including inability to issue authority/reviews/actors, open a generic lock, enable schedule, mutate immutable history or disable triggers. Normal-service role checks reject owner/superuser/excess privileges. The fixture suite uses role switching under its setup owner; real managed login membership/TLS still must be verified. Owner/superuser can bypass protections and are an explicit trust boundary.

The pass found a worker could write `OPEN` into Life State under the previous grants even though executable cycle paths refused it. The new prepared CLOSED-only DB constraint closes that inconsistency without altering canonical data or existing scientific models.

## 11. DB connection security

Production URL validation refuses query-string TLS/options overrides. TLS requires certificate verification, optional reviewed CA and no insecure fallback. Bounded pools, connection/statement/query/idle-transaction/lock timeouts, connection lifetime and application names are explicit. Different credentials belong to owner/operator/worker/reader processes. Raw DB error strings are not public diagnostics.

No universal PostgreSQL16 transaction timeout is claimed; leases, query/statement and idle limits bound the current operations. No unbounded connection retry. Managed CA/hostname, firewall, login role membership and total connection budget require target verification.

## 12. Backup/restore

Actual local `pg_dump` and transactional `psql` restore into new empty disposable schemas were exercised. Complete table rows and catalog are compared; sequences are checked as well. Fixtures cover dormant no-authority state and post-one-shot/continuous state including attempt/receipt/accounting and authority histories. No provider is called during restore; no consumer starts automatically.

Managed backup encryption, retention, PITR/RPO/RTO, privileges and same-schema new-database restore remain infrastructure tests. A local schema-remap drill is not evidence of successful managed failover.

## 13. Disaster recovery

RECOVERY_RUNBOOK.md covers process/worker/DB crashes, provider loss, failover, restore, lost deployment, credential compromise, bad deployment and observer outage. Unknown dispatch/charge remains unknown. Fresh inspection and durable evidence determine reconciliation; retry is not a recovery default.

A backup can erase evidence of an already consumed grant or provider effect. No database-only mechanism can detect all such history loss. Fence old hosts/credentials and compare independently retained dispatch/backup/incident records before reviewing any restored authority. Observation-only startup is safe; unattended restored worker startup is forbidden.

## 14. Rollback

This release checks the stored deployment runtime hash and SQL/catalog identity and rejects mismatches. Historical binaries lacking this guard are not retroactively protected and must be excluded from the host rollback allowlist. Grants/admissions remain pinned to implementation identities. No editing hashes to make readiness pass, no down-migration and no automatic release rebinding. A future source/Node/platform change requires a reviewed forward compatibility/upgrade procedure. Routine rollback is not permission to restore old history or revive old authority.

## 15. Container/build context

`.dockerignore` now allowlists runtime/core/server/config/data, package lock/config and the exact Brain Spec v0.2 package required by `verifyEvidence`. It excludes the multi-gigabyte research tree, private exports, verification outputs, host node_modules, caches, credentials and local DBs. No research was deleted. BUILD_CONTEXT.json records the selected file/byte inventory and exclusions.

The static allowlist currently contains **146 files / 10,234,209 bytes**. This is selected source payload, not an image/tar/installed-dependency measurement.

Dockerfile uses Node24 Debian slim, `npm ci --omit=dev`, non-root node user, dormant mode and observation-only CMD. No schema installation/build-time secrets. `.vercelignore` separately excludes research/private outputs and test/tool scripts from frontend upload while retaining runtime source needed by the repository-wide TypeScript check. Actual image behavior cannot be inferred from macOS Node.

## 16. Process supervision

Initial host supervises observation only, with readiness check and bounded failure restarts. One-shot consumer is a manual job with a single-use audited launch ID and exact authority row hash. Restart cannot reuse the launch receipt. Separate continuous-local launch checks existing scope, runs bounded local sessions, stops on abort/revocation/expiry/budget, and never selects a paid planner.

The four-minute session ceiling is an explicit conservative operator-launch boundary; the CLI is not an indefinitely supervised unattended paid organism. `ProductFallback` currently abstains. Arbitrary future project reasoning is not claimed merely because the queue works.

## 17. Shutdown

Observation stops accepting requests, closes idle sockets, bounds drain, ends pool and has a 12-second outer deadline. Consumer signals stop new local claims and cancel an active one-shot through existing controller semantics; stale/ambiguous work remains inspectable. Hard process death or DB loss cannot prove a provider was not charged. Verify Linux/host termination grace above the application deadline.

## 18. Logging

New service logs use a closed timestamp/service/status/optional-valid-hash structure. No free-form error, memory, relationship, request/response, credential, raw rationale or operator evidence channel is accepted. Private operator inspection output remains private and may contain authorized bounded data; never pipe it into public/shared application logs. Log canaries test the restricted format. Infrastructure retention/rotation is not locally verified.

## 19. Monitoring

MONITORING_CONTRACT.json specifies runtime/DB/readiness, active claims, queue, ambiguous/review state, provider liability/cost, commits/failures, worker idle/stopped and expiry/schema mismatch signals. Existing authenticated private inspection supplies detailed state. No monitoring vendor or background exporter was started. Public health/readiness contain only safe status. Unknown usage must alert, not become zero.

## 20. Environment inventory

ENVIRONMENT_INVENTORY.json indexes source references; runtime/ENVIRONMENT.md supplies required modes, validation, defaults/placeholders, process ownership and secrecy. Production keys are absent. Legacy model/wallet/autonomy settings are explicitly separated from admission/authority. No generic environment model string grants dispatch.

## 21. Secret inventory

Owner DB, operator DB, worker DB, observation-reader DB, operator credential/digest config and admitted provider secret have separate consumers and rotation procedures. None belongs in browser/Next client variables, logs, image layers or research packages. Target secret manager and credential transport remain unset. Rotation does not automatically reconcile old provider liabilities or replace explicit authority revocation.

## 22. Observer/runtime path

Next stays stateless and proxies fixed public DTO routes. It never receives a DB connection. Production browser Authorization is not forwarded; runtime public process ignores it regardless. HTTPS and redirect refusal protect the configured upstream path; test loopback HTTP remains explicit local validation. Public projection remains an allowlist, not an arbitrary table/private trace API.

## 23. Vercel preparation

Prepared vercel.json selects Next, npm ci and the verified Webpack build. Root is repository root; select Node24 on the actual project. Default dormant landing can work without runtime API configuration. A later live observer needs the reviewed runtime HTTPS origin but no execution authority. Domain, edge controls and target Node/build behavior are unverified; no Vercel API/deployment was used.

## 24. Persistent host preparation

Root Dockerfile, Node24/Linux, container port 3001 (or host PORT), healthcheck `/readiness`, ON_FAILURE maximum ten retries. Use private DB networking and verified TLS, explicit dormant identity/config and reader login. No worker service initially. Owner installation is an explicit separate job and never part of CMD/restart. No Railway project was guessed, linked, created or contacted.

## 25. Operator deployment

Smallest arrangement: private trusted terminal/admin host or protected one-off image job, strict stdin command, production auth config, separate operator DB login. Durable actor capabilities and immutable audit bind changes. No public admin web app. Private consumer additionally receives worker credentials and an already-issued grant/scope. Missing secret/auth/identity fails before execution.

## 26. Provider placeholders

Provider-neutral JSON gateway and fixture adapters remain as in Pass6. Actual provider/model/tokenizer/rate-card/endpoint/privacy evidence and secret reference remain pending. Dormant mode needs none. An admitted key alone cannot bypass grant/context/state/budget binding. No real provider smoke or network provider call occurred.

## 27. Dormant E2E fixture

OBSERVER_E2E.json records the built Next observer, actual fresh runtime processes and disposable PostgreSQL with least-privilege reader. Both dormant landing and live presentation of a dormant fixture are checked, including health/readiness, proxy behavior, waiting/restart and unchanged DB rows. These are not canonical life cycles or public awakening.

## 28. One-shot deployment fixture

Production-order installer, separate operator/worker roles, authenticated fixture actor, disclosure review, mock-provider admission and exact one-shot grant feed the explicit consumer. Decision8 commits once; restart preserves consumed grant, receipt/accounting, CLOSED lock and disabled schedule. Duplicate launch cannot create Decision9. No continuous scope is present until the separate next fixture step. Mock transport only. This topology test reconnects PostgreSQL pools and reconstructs operator/controller objects; it does **not** prove fresh-process paid-consumer recovery on the target host. Separate dormant runtime/Next tests do use actual new child processes. The post-Decision8 observation assertion covers HTTP availability and a secret canary, not a complete graphical observer review.

## 29. Continuous deployment fixture

After fixture Decision8, independently issued CONTINUOUS_LOCAL_V1 scope processes a bounded neutral local event; revoke/restart prevents more execution. Provider remains a single mock attempt. Existing recent paid/mock accounting can block a zero-cost scope until its declared budget window permits work; the test respects this rather than clearing costs. Backup restores the resulting fixture histories exactly. This proves local topology mechanics, not paid autonomous reasoning.

## 30. Security review

No public mutation/authority endpoint; GET-only observation with ignored credentials, global request/concurrency limits and safe errors. Runtime-reader/operator/worker role checks, strict SQL/role identifiers, TLS option refusal, immutable release/catalog checks and exact plan acknowledgement reduce deployment misconfiguration paths. Existing provider endpoint admission, public DTO, permission/reducer, idempotency, revocation, disclosure and ambiguous accounting rules remain in force.

Target ingress/WAF, trusted origin/DNS/egress restrictions, CA validation, production login memberships, secrets/log access, backups and OS/container grace remain infrastructure verification. Owner compromise bypasses SQL defenses. A generic gateway implementation's billing/token guarantees must be independently verified before admission. Nothing in this pass adds wallet, shell, internet or communication authority.

## 31. Tests/build

See CHECKS.json and preserved full test, TypeScript, lint and build logs. All 516 previous test cases are retained; the standalone boot test now uses the explicit installed dormant mode and tests refusal/GET-only safety rather than relying on obsolete implicit configuration. No scientific acceptance criterion or runtime precision/timing policy was changed.

Early verification exposed the old implicit-boot fixture incompatibility. Its cleanup was fixed to avoid waiting for an already-exited child; the test now invokes the actual explicit installed dormant entrypoint. No existing test case was deleted.

| Check | Actual result |
|---|---|
| Complete Node suite | **533 total: 532 passed, 1 failed, 0 cancelled, 0 skipped** |
| New deployment cases | **17/17 passed**, including the integrated mock one-shot/local-continuous topology |
| TypeScript | Passed |
| ESLint | Passed |
| Next.js production build | Passed via `npm run build -- --webpack`; local dotenv values masked, telemetry disabled |
| Built Next + runtime + disposable PostgreSQL | Passed HTTP/HTML tests across two fresh-process dormant starts; rows unchanged |
| Docker image execution | **CONTAINER EXECUTION NOT VERIFIED LOCALLY**; Docker unavailable |

The failed existing test is **`Crash boundary before_claim has atomic local recovery`**, `tests/continuous-life.test.ts:43`. Its second tick returned `CLOSED_WITH_ERROR` rather than `COMMITTED`, under a **250 ms lease / 100 ms planner timeout**. The assertion does not record the inner reason, so the exact cause remains unresolved. Earlier runs had additional short-deadline failures and remain preserved. A targeted rerun also failed, but overlapped a build and is not clean isolation evidence. A later instrumented disposable diagnostic completed with unchanged limits: before-commit phase at approximately 237 ms and completion at 274 ms from tick start (claim begins later). This supports timing sensitivity; it neither proves the exclusive cause nor clears the failed full suite. No lease/timeout/precision policy was changed, and no favorable rerun replaces the final full-suite result.

**Remaining local work:** identify and reliably verify the short-lease recovery behavior, preserving fail-closed deadlines and all previous tests. Fresh consumer-process recovery and production login/TLS/Node24/Linux behavior also require the target verification described in the runbooks. Do not proceed from this package as though all regressions passed.

## 32. Infrastructure-only blockers

Docker is unavailable: **CONTAINER EXECUTION NOT VERIFIED LOCALLY**. No intended production project/service/DB/network/domain has been verified. Remaining target tasks: final Node24/Linux image build/run/restart, managed restore/PITR/TLS/roles/connection counts, private operator access, domains/edge limits, monitoring delivery/retention, separately selected/admitted provider and authorized sanitized smoke. These are not represented as local passes.

## 33. Exact production checklist

runtime/PRODUCTION_INSTALLATION.md separates predeploy, database, runtime, observer, private operator, provider/smoke and human authorization. Every mutating step has preconditions, expected result and stop/recovery semantics. Dry-run plans do not authorize apply; successful apply does not authorize Decision8. Backup transfer is not a new organism birth.

## 34. Awakening-day runbook

runtime/AWAKENING_RUNBOOK.md: verify canonical identity/state and backups → verify services/operator → review disclosure → separately admit/smoke provider → freeze exact identities → privately inspect neutral event schema → propose/review/authorize exact single-cycle grant → explicit private consumer → inspect Decision8/accounting/state → STOP. No scripted decision or dramatic narrative.

## 35. Post-Decision8 checklist

Decision/proposal/policy/intent/outcome agreement; context/memory provenance and disclosure; bounded stored rationale; actual local effects; Life State/artifact/task changes; provider receipt/reservation/cost; public DTO; biology NOT_APPLIED and unchanged snapshot; no external effects/hidden scope; consumed grant, CLOSED lock, disabled schedule. Human review must separately decide whether a continuous-local scope is appropriate. No automatic continuation.

## 36. Files changed

FILES_CHANGED.json lists added/modified files relative to the start-of-pass hash snapshot. Implementation is limited to deployment boot/config/role/catalog/install/consumer boundaries, prepared SQL, frontend proxy/config boundaries, tooling/tests and runbooks. Runtime identity version is `runtime-v1-oneshot-1.0.7`; prior authority identities are not silently reused. Frozen science and original canonical rows are unchanged.

## 37. Known limitations

Local Node/macOS and PostgreSQL16 are not container/managed production. Catalog comparison intentionally rejects unreviewed schema differences. Future code upgrades need a separately reviewed deployment-release migration; there is no automatic resealing. Database rollback cannot reveal lost external effects without external evidence. Continuous-local CLI sessions are bounded and use deterministic abstention, not a real continuously reasoning provider. Legacy/private disclosure exclusions remain; provider review is still required. UI polish, wallet resolution, internet, external communication, richer autonomy and biological advancement remain out of scope.

## 38. Final state

Final actual row digest is **`4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`**, identical to the before export. Counts and full-row comparison are in PRESERVATION.json. Genesis remains Genesis001: seven decisions, seven legacy memories, zero canonical V2 episodes, CLOSED execution, disabled schedule, saved-only biology, no continuous authority, no provider call, wallet action or external communication. No production or canonical migration/deployment/authorization occurred. Stop for review.

DEPLOYMENT PREPARATION INCOMPLETE — LOCAL WORK REMAINS

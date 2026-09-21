# Environment and secrets — authoritative Pass 7 specification

No actual credentials or production targets are recorded here. All examples are placeholders. No environment boolean is execution authority. Unlisted modes are refused. Production uses Node 24/Linux; PostgreSQL 16 is the catalog-tested server major.

## Public frontend (Vercel only)

| Variable | Required/default | Validation / placeholder | Secret / scope |
|---|---|---|---|
| NODE_ENV | production (platform) | production | No |
| GENESIS_PUBLIC_MODE | dormant | dormant/live; presentation only | No, server evaluated |
| GENESIS_AWAKENS_AT | optional, absent unannounced | ISO time with explicit zone; countdown never activates | No |
| GENESIS_API_URL | only observation projection | `https://RUNTIME_ORIGIN.invalid`; no URL credentials/query/fragment; production HTTPS except local test loopback; redirects refused | No, server-side only |
| GENESIS_DEV_PREVIEW | false | development-only true; production ignored | No, local dev only |
| GENESIS_DEV_OPERATOR | false | development-only localhost convenience | No, never production |
| GENESIS_OPERATOR_TOKEN | absent | legacy localhost convenience only | Secret; **do not provision to Vercel** |

No DATABASE_URL, operator/provider credential or NEXT_PUBLIC secret belongs in the frontend. Browser fetches same-origin fixed public API routes; those proxy to allowlisted DTOs. Production browser authorization is not forwarded. Platform edge rate limits/TLS/domain verification remain infrastructure checks.

## Observation runtime

| Variable | Required/default | Validation / placeholder | Secret |
|---|---|---|---|
| NODE_ENV | production | production | No |
| GENESIS_RUNTIME_MODE | required | **dormant only**; absent/other refuses before DB construction | No |
| DATABASE_URL | required | `postgresql://READER_LOGIN:SECRET@DB_HOST:5432/DB_NAME`; no query options; valid database path | Yes |
| GENESIS_EXPECTED_ORGANISM_ID | required | original reviewed organism ID, never derived from a new initialized DB | No; private deployment metadata |
| GENESIS_EXPECTED_BIRTH | required | original exact ISO birth | No |
| HOST | 0.0.0.0 | bind host; restrict ingress at target | No |
| PORT | 3001 | integer 1–65535 | No |
| GENESIS_ALLOWED_ORIGINS | localhost development defaults | comma-separated origins; new observation process is GET-only; no private mutation HTTP route | No |
| GENESIS_AUTONOMY_ENABLED | absent/false | true or other non-false value refused by dormant boot | No |
| GENESIS_INTERNET | absent/false | non-false refused | No |
| GENESIS_WORKER_ENABLED | absent/false | non-false refused; cannot launch a worker | No |
| GENESIS_SCHEDULER_ENABLED | absent/false | non-false refused | No |
| GENESIS_PROVIDER_ENABLED | absent/false | non-false refused; does not grant provider authority | No |

Observation service needs neither operator token nor provider/wallet secret. Legacy `OPENAI_API_KEY`, `OPENAI_MODEL`, `SOLANA_RPC_URL`, `SOLANA_WALLET_ADDRESS`, `SOLANA_NETWORK` conflict with dormant credential scope and must be absent. Other `GENESIS_PROVIDER_*` credentials are rejected there. Readiness checks DB release identity each request; the service can expose liveness while DB is unavailable, but serves no organism projection until ready.

## Database settings (each DB-connected private/runtime process)

| Variable | Default / required | Validation | Secret |
|---|---|---|---|
| GENESIS_DB_ROLE | absent | fixture-only validated group role for SET ROLE; refused in production, which requires dedicated least-privilege logins | No |
| GENESIS_DB_SCHEMA | public | lowercase SQL identifier, 1–63 characters | No |
| GENESIS_DB_TLS | production required | `verify-full` only; `rejectUnauthorized:true` | No |
| GENESIS_DB_CA_FILE | optional | path to reviewed CA PEM; otherwise system CAs; no insecure fallback | CA generally public; filesystem path private |
| GENESIS_DB_POOL_MAX | 4 | integer 1–16 | No |
| GENESIS_DB_CONNECT_TIMEOUT_MS | 5000 | integer 1–30000 | No |
| GENESIS_DB_STATEMENT_TIMEOUT_MS | 15000 | integer 1–60000; client query ceiling also 20000 | No |

Fixed: idle transaction timeout 20s, lock timeout 5s, query timeout 20s, idle client 30s, pool lifetime 300s; application name `genesis-<process>`. No unbounded connection retry. Subsequent health probes reconnect through bounded pools; host restart policy has ten retries. Size managed maximum connections for **sum of all process pools + owner/operator jobs + platform reserve**, not per-service values alone. Operator CLI/smoke override pool max to one. Consumer has two separate pools (operator and worker).

Nonproduction deployment tools accept only loopback `genesis_runtime_v1_test` and plaintext fixture connections. Production rejects connection-string query parameters that could override TLS/settings. Never log full connection strings. Transaction safety additionally relies on existing bounded leases and statement/idle limits; PostgreSQL16 has no configured universal transaction_timeout, so do not claim one.

## Private operator

| Variable | Required mode / default | Validation / placeholder | Secret |
|---|---|---|---|
| GENESIS_PRIVATE_OPERATOR_MODE | absent disables CLI/smoke | enabled only | No |
| GENESIS_OPERATOR_DATABASE_URL | required enabled | separate PRIVATE_OPERATOR login, same DB schema/TLS rules | Yes |
| GENESIS_OPERATOR_AUTH_FILE | required enabled | private mode-0600 JSON with production enabled config, actor IDs, SHA-256 credential digests and expiry; actor capabilities also checked durably | Sensitive |
| GENESIS_OPERATOR_CREDENTIAL | required enabled | 32–500 characters, constant-time digest authentication, unexpired key | Yes |

Provision actors separately using owner credentials and reviewed capability assignments. Runtime workers cannot create actors/reviews/authority. The CLI reads strict bounded command JSON from stdin and prints potentially private authorized inspection; keep terminal/log destination private. No credential in argv, command payload or public logs. Failure output is generic and uncertain acknowledgement requires durable inspection.

## Explicit installer (owner only)

| Variable | Required/default | Validation / placeholder | Secret |
|---|---|---|---|
| GENESIS_MIGRATION_MODE | absent disables | explicit | No |
| GENESIS_MIGRATION_DATABASE_URL | required | migration-owner credential, exact target | Yes |
| GENESIS_INSTALL_PLAN_FILE | required | new mode-0600 file for plan; reviewed existing file for apply | Private metadata |
| GENESIS_DB_ROLES_FILE | plan required | strict object with distinct observer/reader/worker/operator identifier names | Private metadata |
| GENESIS_INSTALL_ACK | apply required | `INSTALL_REVIEWED_PLAN:<exact hash>` | Authorization reference; private |
| GENESIS_EXPECTED_ORGANISM_ID / GENESIS_EXPECTED_BIRTH | plan required | exact existing identity | No |

CLI verbs are `plan` (read-only) and `apply` (future explicit authorization). Unknown verbs fail. No default command invokes it. Legacy `runtime/migrate.ts` CLI is refused in NODE_ENV=production; library remains for fixtures. Existing historical migration/import scripts are not production install entrypoints.

## Explicit private consumer / future local worker

| Variable | Required/default | Validation | Secret |
|---|---|---|---|
| GENESIS_CONSUMER_MODE | absent disables | explicit only | No |
| GENESIS_WORKER_DATABASE_URL | required | separate RUNTIME_WORKER login | Yes |
| GENESIS_OPERATOR_DATABASE_URL / AUTH_FILE / CREDENTIAL | required | production operator authentication and same target as worker | Yes |

Strict stdin launch request selects one-shot or continuous-local, **existing authority only**, new single-use launch ID, exact authority row hash, runtime hash, organism/birth, admission ID or null, review reference and session limit 1–240000ms. Maximum four-minute authenticated sessions intentionally stop; a new separately reviewed manual launch is required. Host auto-restart cannot reuse a consumed launch receipt. No env flag selects a model or converts local scope into paid reasoning.

## Provider (private admitted one-shot / separately authorized smoke only)

| Variable | Required/default | Validation | Secret |
|---|---|---|---|
| GENESIS_PROVIDER_<NAME> | only exact admission secret reference | `env:GENESIS_PROVIDER_<NAME>`; bounded non-fixture value, no newline; adapter validates admission | Yes |
| GENESIS_SMOKE_AUTHORIZATION_FILE | smoke required | separately reviewed exact smoke authorization, not a Genesis grant | Private |
| GENESIS_SMOKE_JOURNAL_DIRECTORY | smoke required | private writable journal, exclusive single attempt | Private |

Endpoint, model, adapter, schema, counting, rate-card, timeout, cost/token ceilings, retry policy and retention/disclosure evidence live in reviewed **admission data**, not arbitrary environment strings. Missing provider configuration permits dormant observation and prevents dispatch. No model or price selected. Per-cycle maximum $0.05, one attempt, zero automatic retries; actual admitted conservative ceiling may be lower.

## Legacy / test-only variables

`GENESIS_PLANNER_MODE` (auto/local/openai), `OPENAI_API_KEY`, `OPENAI_MODEL`: legacy compatibility; observation forces local without executing it and refuses key/model presence. Not production admission.

`GENESIS_INTERVAL_MS` (30000, 1000–3600000), `GENESIS_MAX_DAILY_CYCLES` (200, 1–10000), `GENESIS_STARTING_CENTS` (10000, 0–100000000): legacy validated config, no dormant scheduling or reinitialization effect. Do not tune these to authorize cycles.

`SOLANA_RPC_URL`, `SOLANA_WALLET_ADDRESS`, `SOLANA_NETWORK`: legacy disabled observer configuration, not wallet binding. Do not supply to new dormant process.

`GENESIS_ORIGIN`, `GENESIS_CYCLES`: deprecated life/demo scripts; no production role. `TEST_DATABASE_URL`: disposable test DB only; incompatible with canonical DATABASE_URL in mutation fixtures. `NEXT_TELEMETRY_DISABLED=1`: local build telemetry suppression. `PATH` and toolchain settings are platform infrastructure, not organism configuration.

## Secret rotation

DB logins: fence affected process, rotate in platform secret store, terminate old sessions if compromised, restart dormant first, verify least privilege and target. Migration owner never stays in normal environment. Operator key/digest: revoke durable actor/key, rotate private config, restart private tools; revoke grants/scopes separately—key rotation alone is not a guaranteed in-flight stop. Provider secret: stop consumer, revoke affected admission/grants, inspect unknown billing, rotate reference/value, re-review admission if identity changes. Do not erase receipts/history. No deployment-to-runtime bearer secret is required for public DTO GETs; use target ingress/edge controls and HTTPS rather than putting operator credentials in Next.

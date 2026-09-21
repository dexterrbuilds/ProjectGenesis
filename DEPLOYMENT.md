> **Pass 7 supersedes the installation instructions below.** Use [runtime/PRODUCTION_INSTALLATION.md](runtime/PRODUCTION_INSTALLATION.md), [runtime/ENVIRONMENT.md](runtime/ENVIRONMENT.md), and [runtime/RECOVERY_RUNBOOK.md](runtime/RECOVERY_RUNBOOK.md). The current observation process requires explicit dormant mode and the prepared release schema; old `/healthz` and token configuration descriptions below are historical. No deployment or activation is authorized.

# Deploy Project Genesis Runtime V1 — dormant only

This repository remains portable: Vercel serves Next.js; Railway (or another container host) serves the standalone Node observer; Postgres/Supabase owns durable state. No GPT Sites or ChatGPT runtime is required. These instructions authorize no awakening or external action.

## Database and migration

Keep Genesis 001's existing database and verified backups. Runtime startup **does not initialize an organism or run migrations**. Empty, wrong, unmigrated, OPEN or scheduled databases must be investigated rather than replaced.

Migration 003 has been applied to this checkout's canonical database after an exact baseline and isolated backup-restore test. [RUNTIME_V1_MIGRATION_REPORT.md](RUNTIME_V1_MIGRATION_REPORT.md) records the before/after digests and unchanged original rows. Do not rerun the baseline-specific apply script on the migrated database. For moving hosts, use a reviewed complete backup/restore of the same organism with the additive schema, not a new birth/import into an occupied database.

`runtime/migrate-v1.ts` is an explicit administrative operation; `scripts/runtime-v1-apply.ts --apply-reviewed-baseline` is specific to the approved pre-migration digest and verified local backup/dry run. It fails when that digest no longer matches. It is not an auto-upgrade command for arbitrary deployments.

Keep provider TLS verification, private credentials and backups/PITR. A database owner can bypass triggers; application credentials and administrative credentials must not reach the planner or browser. No filesystem on Vercel stores life state.

## Railway / portable runtime

`railway.json` selects the root `Dockerfile`; its command is `node runtime/main.ts`. The image includes the pinned evidence registry package but does not execute research. Supply:

| Variable | Dormant value |
|---|---|
| `DATABASE_URL` | Private URI of the existing migrated Genesis database |
| `GENESIS_OPERATOR_TOKEN` | Private random secret, at least 24 characters |
| `GENESIS_ALLOWED_ORIGINS` | Exact observer origins |
| `GENESIS_AUTONOMY_ENABLED` | `false`; even `true` cannot unlock this build |
| `GENESIS_INTERNET` | `false` |
| `GENESIS_PLANNER_MODE` | `local`; no planner is started by this build |
| `PORT` / `HOST` | Host-provided port / `0.0.0.0` |

Omit provider keys and Solana/ClawPump settings for dormant operation. No signer is accepted. No wallet, heartbeat, scheduler, neural or LLM worker starts. HTTP availability is independent of browser lifetime. Keep one runtime replica for preparation; do not deploy an old writer alongside it.

`GET /healthz` checks existing CLOSED life state and database access. Public GETs are allowlisted at the runtime. Authenticated cycle/control requests return 423; missing authentication is rejected. Health checks/public reads do not create events or touch the schedule. A deployment flag is not an execution grant.

Docker was unavailable locally. CI retains an image-build step; require a successful actual image build and dormant health check in your target environment before release. Standalone Node boot/restart has passed against isolated copied state; it does not substitute for Docker verification.

## Vercel / Next.js

Use the Next.js preset and repository root. For the dormant countdown, set:

```text
GENESIS_AWAKENS_AT=2026-09-29T00:00:00-07:00
GENESIS_PUBLIC_MODE=dormant
```

No runtime/database is needed for the countdown. To expose the read-only observer later, explicitly review `GENESIS_PUBLIC_MODE=live` and set `GENESIS_API_URL` to the HTTPS runtime origin. Neither the date nor that presentation setting can awaken Genesis. Development-only `/preview` remains unavailable in production.

Never configure database credentials, an operator token or provider keys on Vercel or in `NEXT_PUBLIC_*`. Runtime public routes enforce privacy even if accessed directly. No operator controls are offered in the V1 observer.

The local production build succeeded with `npm run build -- --webpack`. Default Turbopack hit a host port-permission failure even on the approved retry. Vercel's default `npm run build` configuration is unchanged; if its environment reproduces that failure, the verified webpack command is an explicit supported build override. Do not disable type checking to get a build through.

## Verification without awakening

```sh
npm ci
npm run typecheck
npm run lint
npm test
npm run build -- --webpack
# Dedicated disposable database only:
TEST_DATABASE_URL=postgresql://user:password@localhost:5432/genesis_runtime_v1_test npm run test:postgres
# When Docker exists:
docker build -t project-genesis-runtime .
```

The test DB name is enforced. Tests use disposable schemas, fixture neural computation and mocked providers. Canonical lifecycle smoke tests, demo execution and real-provider smoke calls are not part of these instructions. The `life`, `demo`, and `check:llm` commands refuse in this release.

Review saved identity/birth/seven cycles, public privacy, historical frame labeling, schedule false and CLOSED lock. Do not run eight cycles as an acceptance check. A future activation requires a named operational mode, durable provider budgets if enabled, appropriate permissions and separate explicit authorization. [RUNTIME_V1_AWAKENING_READINESS.md](RUNTIME_V1_AWAKENING_READINESS.md) lists the gates.

## Recovery

Stop an observer before changing hosts; retain its full database. Restore a backup only to an isolated verification target first and compare original rows. Never reset the singleton, change birth or regenerate a snapshot as recovery. Before activation there are no new V2 life events to replay; migration metadata is administrative. Keep additive tables when rolling application code back to read-only mode; old V1 writes are intentionally fenced.

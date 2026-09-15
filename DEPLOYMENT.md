# Deploy Project Genesis

## Service topology

One GitHub repository, two services, one external Postgres database. The web service may redeploy, scale to zero or close in a browser while the runtime continues its life loop. Deployments do not reset identity or capital.

```text
Browser → Vercel / Next.js → HTTPS → Railway / Node runtime → Postgres or Supabase
                                      └ autonomous worker
```

No ChatGPT-specific hosting/runtime is used. Railway can be replaced by any continuously running Docker/container host with outbound HTTPS, a port and Postgres access. Vercel can also be replaced by a standard Next.js host.

## 1. Database

Provision Postgres 16+ in Railway or a dedicated Supabase database. Use the provider’s connection URI and TLS settings; do not disable certificate verification to bypass configuration issues. Supabase’s direct connection or session pooler is appropriate for this long-lived runtime. Use an application database dedicated to Genesis. The startup migration needs schema creation permission. Keep database credentials private to the runtime, not in Vercel or any `NEXT_PUBLIC_*` variable.

`runtime/migrations/001_genesis.sql` is applied once under a transaction advisory lock at runtime startup. Existing life is initialized only if absent. Later migrations must be additive and versioned. Enable database backups / point-in-time recovery before a public long-running experiment. The frontend filesystem is never used as a database.

For the pre-portability life, an exported `{ organism, decisions }` JSON can be imported into an **empty** database:

```sh
DATABASE_URL=<destination-uri> node scripts/import-life.ts /absolute/path/to/export.json
```

The importer refuses an occupied database and preserves ID, birth time, cycles, wallet, projects and neural state. The repository does not include private runtime exports or database files. This checkout’s original seven-cycle organism was migrated to local Postgres without resetting its birth.

## 2. Railway runtime

Connect the GitHub repository to a Railway service. Select the repository root; `railway.json` selects `Dockerfile`. Add Postgres or link the external database. Do not deploy this service as Next.js; its image starts `node runtime/main.ts`.

Required variables:

| Variable | Value |
| --- | --- |
| `DATABASE_URL` | Private provider Postgres URI |
| `GENESIS_OPERATOR_TOKEN` | Random secret, ≥24 characters |
| `GENESIS_ALLOWED_ORIGINS` | Exact public Vercel/custom origin; comma-separated if needed |
| `GENESIS_AUTONOMY_ENABLED` | `true` |
| `GENESIS_INTERVAL_MS` | Start at `30000` |
| `GENESIS_MAX_DAILY_CYCLES` | Start at `200` |
| `GENESIS_STARTING_CENTS` | `10000`, used only at birth |
| `GENESIS_INTERNET` | `true` to permit selected read-only research |
| `GENESIS_PLANNER_MODE` | `auto`, `local`, or `openai` |
| `OPENAI_API_KEY`, `OPENAI_MODEL` | Supply both to use the real language planner |

Railway provides `PORT`; the runtime binds `0.0.0.0`. Generate an HTTPS public domain. `GET /healthz` must return 200 with database access. Keep one replica initially and **disable service sleeping/serverless scale-to-zero** for continuous life. Set suitable CPU/memory and provider billing limits. The runtime uses no writable volume for life state.

A fresh database has scheduling disabled. After deployment, start a bounded run from the operator UI before enabling continuous life. Paused/enabled state and remaining cycles persist through process restarts. The scheduler waits for the stored due time, runs one cycle, and saves a new due time. It does not catch up all missed wall-clock cycles. Failed outcomes disable the schedule; inspect the saved decision before resuming. UTC daily quota exhaustion holds further cycles until the next UTC day.

SIGTERM stops claiming new work, awaits in-flight work and closes the database pool. Allow at least 60 seconds for graceful shutdown where supported. An interrupted cycle’s lease expires after 60 seconds; committed decisions and money remain consistent. Paid provider calls may be repeated if the process dies before committing; real financial execution remains disabled.

## 3. Vercel observation website

Import the same GitHub repository. Use the **Next.js** framework preset and Node 24 (22.18+ minimum). `vercel.json` sets `npm ci`, `npm run build` and a 60-second API function duration. Configure only:

```text
GENESIS_API_URL=https://your-runtime-domain
```

The runtime URL must be reachable from Vercel over HTTPS. Add the exact website origin to Railway’s `GENESIS_ALLOWED_ORIGINS`. Preview deployments that need operator controls must also have their explicit origin allowed; do not use a broad wildcard. Public observation remains read-only.

Do not set a database URL, LLM key or operator token in Vercel. Operators enter their token in the UI; it stays in tab memory and is forwarded for authenticated mutations. The local `GENESIS_DEV_OPERATOR` shortcut is ignored in production. Production proxy requests do not inject a secret. Runtime outages show an unavailable state; the website never substitutes fabricated activity.

## 4. Acceptance checks

1. Run `npm test`, `npm run typecheck`, `npm run build`; run `npm run test:postgres` with a dedicated test DB.
2. Check runtime `/healthz`, public `/api/state`, and 401 for a mutation without credentials.
3. Open the website, verify the birth record, original ID, planner label and simulated-money label.
4. Start **Run 8 cycles**, close the website, wait several configured intervals, then reopen. Cycle count and life history must have advanced. Recorded neural ticks should continue from prior saved state.
5. Restart the runtime during a bounded run. Identity, wallet and committed history should remain; remaining scheduled cycles resume. Pause is persistent as well.
6. Inspect a complete saved chain and use Brain replay. Network activity must correspond to its saved frames.

The Postgres integration suite automates concurrency, restart, API authorization and browser-independent scheduling. A live OpenAI call requires credentials and is not proven by the mocked provider contract tests. Docker must be built in your CI/container host; local tests do not substitute for an image build.

## Recovery and portability

Keep the original database when replacing a runtime host. Pause, allow an in-flight cycle to finish, stop the old host, deploy the same image on the new host with the same `DATABASE_URL`, and change `GENESIS_API_URL`. Verify identity and history before resuming. Database leases defend overlapping restarts, but deliberate single-owner operation is simplest.

Backup/restore the complete database, including decisions and schedule; do not restore only a wallet or only a brain. Never manually delete the singleton to change starting capital. Changing Brain v1 requires an explicit `replaceBrain` transition that records lineage and supplies a new valid snapshot while keeping organism identity and history.

Live Solana funds, ClawPump fee income, publication and human hiring require additional verified provider integration and an approval/outbox/reconciliation path. Their interfaces are present; execution is not enabled by these deployment instructions.

Provider references: [Next.js deployment](https://nextjs.org/docs/app/getting-started/deploying), [Railway config](https://docs.railway.com/config-as-code/reference), [Railway health checks](https://docs.railway.com/deployments/healthchecks), [Vercel environment variables](https://vercel.com/kb/guide/how-to-add-vercel-environment-variables).

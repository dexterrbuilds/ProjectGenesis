# Project Genesis

> “We gave a biological brain money, language and access to the internet. Now we’re going to see what it becomes.”

An artificial life with a real connectome inside its decision loop. Genesis retains its identity, birth time, experiences, memories, projects, simulated money and neural state across cycles and restarts.

**Brain v1:** 302 named C. elegans neurons, 3,709 directed chemical edges and 1,091 electrical pairs. All displayed activation is saved output from the deterministic simulator. This is a simplified connectome-constrained controller, not a validated reproduction of a living worm. See [SCIENCE.md](SCIENCE.md) and [data provenance and license](data/README.md).

## Run the neural proof

Requires Node 22.18+ (Node 24 recommended), npm; Python 3 only for dataset re-import.

```sh
npm ci
npm test
npm run demo
```

The deterministic demo writes twelve complete cycles to `outputs/deterministic-proof.json` without changing the organism database. Tests cover original data checksums, propagation, ablation, bounded dynamics, snapshot restoration, constrained plans, economic limits and persistence.

| Event from rest, 80 steps | Intact brain | Action | Disconnected brain |
| --- | --- | --- | --- |
| Danger | RETREAT | withdraw | WAIT → rest |
| Opportunity | APPROACH | draft_service | WAIT → rest |
| Novelty | EXPLORE | research | WAIT → rest |
| Quiet | WAIT | rest | WAIT → rest |

Persisted history can change these outputs. This proves material dependence on connectivity, not biological fidelity.

## Run the living experiment locally

Use a local Postgres 16+ database or a dedicated hosted development database. All authoritative life data is external to the web application.

```sh
cp .env.example .env
# Set DATABASE_URL and a random GENESIS_OPERATOR_TOKEN of at least 24 characters.
npm run runtime
```

The runtime applies versioned migrations at startup. In a second terminal:

```sh
npm run dev
```

Open [localhost:5173](http://localhost:5173). Enter the operator token in the observation page’s operator settings. `GENESIS_DEV_OPERATOR=true` is an optional localhost-only development convenience; it is disabled in production.

**Live autonomously** enables the persistent runtime schedule. **Run 8 cycles** is a bounded schedule owned by that same runtime. Closing the website does not stop either run. **Pause** prevents the next cycle; any in-flight cycle may finish. **Stop autonomous life** disables scheduling while retaining manual operation. The default daily limit is 200 committed cycles in UTC; resting cycles use twice the configured interval. Restarting the runtime retains pause, due time and remaining cycles. Missed time is not replayed as a burst of synthetic experiences.

The UI answers “What is Genesis doing right now?” and exposes:

`WORLD EVENT → SENSORY INPUT → 302-NEURON BRAIN → DRIVE → REASONING → ACTION → OUTCOME → EXPERIENCE`

Live, Brain, Life, Money and Memory show persistent records. Replay inspects saved samples; it never simulates decorative activity. Birth is a distinct milestone tied to the original organism ID and creation time. Reading, learning, research, reflection, work, service drafting, risk review, withdrawal and idle/rest are available within behavioral constraints. A documented product energy rhythm allows recovery without changing the brain’s impulse.

## Real language planner

Set **both** `OPENAI_API_KEY` and `OPENAI_MODEL` on the runtime. `GENESIS_PLANNER_MODE=auto` selects the real OpenAI Responses planner when both exist, otherwise the explicitly labeled deterministic local planner. Use `local` for reproducible demos or `openai` to require credentials at startup. Partial credentials are rejected. No live provider call has been verified in this checkout because credentials are absent.

The [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) schema fixes the behavior to the neural output and limits actions to its allowlist. A separate execution guard revalidates the plan. Provider errors become saved failed experiences and stop scheduled runs; there is no silent provider-to-local fallback. Calls have a 25-second timeout and 1,000 output-token limit. Configure provider billing limits separately: simulated expenses do not account for real API bills, and a cycle quota is not an exact currency spending cap.

## Portable deployment

The repository is a standard Next.js application plus a standalone Node runtime. **No GPT Sites, ChatGPT runtime, Cloudflare Worker or D1 dependency is required.**

- **Vercel:** observation website and stateless API proxy; only needs `GENESIS_API_URL`.
- **Railway:** always-on Docker service owns neural cycles, tools and the scheduler.
- **Postgres / Supabase:** authoritative organism state, memories, decisions, neural traces, projects, milestones and ledger.

Follow [DEPLOYMENT.md](DEPLOYMENT.md) for configuration, migration, health checks and recovery. The Docker runtime can move to another container host without changing the core application. No deployment is created by running the tests or build.

## API and verification

Both the runtime and web proxy expose public `GET /api/state`, `/api/brain`, `/api/history?before=<cycle>` and `/api/history?id=<decisionId>`. Runtime `GET /healthz` checks database connectivity.

Mutation endpoints require `Authorization: Bearer <operator token>`:

- `POST /api/cycle`: `{ "requestId": "unique-id-123", "event": "danger" }`; omit `event` to use the saved next stimulus.
- `POST /api/control`: `{ "enabled": true, "remainingCycles": 8, "paused": false }`; use `remainingCycles: null` for continuous life within the daily quota, or `{ "enabled": false }` to stop scheduling.

```sh
npm run typecheck
npm run build
# Uses an isolated temporary schema in a development database; never point tests at production.
TEST_DATABASE_URL=postgresql://user:password@localhost:5432/genesis_test npm run test:postgres
# Optional foreground/manual runner against the runtime, independent of the web server:
GENESIS_ORIGIN=http://localhost:3001 GENESIS_CYCLES=12 npm run life
```

Postgres tests exercise real transactions, restart recovery, leases, pause during commit, authentication, daily quota and bounded scheduler runs without a browser. Legacy SQLite regression tests remain as an additional migration-era check. Test network doubles are confined to tests.

## Economy and current limits

The development wallet uses integer cents, configurable starting capital and a journal. Every third work unit earns simulated $1.50; each unit costs $0.25. These are development-market rules, not real customers or demonstrated self-sustainability. Service drafts and memories are saved artifacts. Research can fetch fixed allowlisted OpenWorm sources when enabled; the agent does not have unrestricted internet access.

`core/economy/adapters.ts` provides a read-only Solana balance adapter, a ClawPump finalized-fee receipt interface, asset-aware atomic units and pending financial intents. The ClawPump reader must be supplied against a verified provider API. No private keys, signing, trading or live fee ingestion are enabled; on-chain assets are never silently mixed with simulated USD. Financial, publication, communication, hiring and physical requests are pending review only. Human communication currently means drafting a message.

The lease/transaction design is adequate for current read-only external tools. Before adding irreversible tools, implement a durable outbox, provider idempotency and reconciliation. A crash can repeat an uncommitted LLM call and its real billing. Public records must contain only material intended for observation. Full traces and aggregate state are retained for hackathon-scale runs; years of history need archival and retention design.

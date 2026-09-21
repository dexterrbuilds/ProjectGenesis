# Project Genesis

An artificial-life experiment with persistent identity, history and explicitly separated biological observations, computational life state, language reasoning and policy.

**Runtime V1 is dormant.** Genesis 001 retains its original birth, seven experiences, memories, project, simulated economy and C. elegans snapshot. The approved implementation adds a life-state extension; it does not awaken Genesis or install a fly brain.

## What the biological layer actually does

The active compatibility mode is **SAVED-OBSERVATION-ONLY**. It validates and restores the original 302-neuron C. elegans snapshot without stepping, stimulating or decoding it. Ordinary digital events receive `not_applied`, with a reason and null quantity. Saved frames are historical, dimensionless model output.

The biological core supplies no semantic action authority. Historical decoder labels remain unchanged in storage and appear as **LEGACY COMPUTATIONAL DECODER LABEL — NOT VALIDATED BIOLOGICAL ACTION**. The legacy neural equations, connectome, BrainAdapter and tests remain available for compatibility. Frozen Drosophila studies and Brain Spec v0.2 are evidence, not installed runtime capabilities. The Stage-1 learning result is scoped to its research preparation.

See [architecture](ARCHITECTURE.md), the [approved design](GENESIS_RUNTIME_V1_DESIGN.md), and [implementation report](RUNTIME_V1_IMPLEMENTATION_REPORT.md). [SCIENCE.md](SCIENCE.md) remains a historical scientific document; it does not grant current runtime action authority.

## Current executable boundaries

```text
Event → applicability check → biological observation / NOT_APPLIED
      → computational life context → bounded compiler → planner proposal
      → independent policy → local result / non-execution → episode / life update
```

The preparation path is verified on isolated fixtures. The production service refuses execution before reaching it. No HTTP control, CLI, countdown, provider key or feature flag unlocks this release. No scheduler, heartbeat, wallet observer or external dispatcher starts. The four memory domains are biological snapshots, append-only episodes, attributed semantic/self assertions, and temporary working context.

## Verify safely

Requires Node 22.18+; Node 24 is recommended for this repository.

```sh
npm ci
npm run typecheck
npm run lint
npm test
npm run build -- --webpack
```

`npm test` skips the seven Postgres tests without `TEST_DATABASE_URL`. To include them, use a **separate database named `genesis_runtime_v1_test`**. Tests create/drop disposable schemas. They never target canonical Genesis. Neural regression tests operate on isolated legacy fixtures; provider tests use injected responses.

The current environment passed 74 tests including the seven Postgres tests. Next production build passed using its supported webpack builder. Turbopack encountered a host port-permission error; Docker was unavailable. See [verification details](RUNTIME_V1_TEST_REPORT.md). `demo`, `life` and `check:llm` CLI commands now refuse execution in this dormant release.

## Run an observer, not a life cycle

```sh
# Existing reviewed, migrated database only; never an empty replacement.
npm run runtime
# Separately, for the frontend:
npm run dev
```

The runtime requires `DATABASE_URL` and a private operator token of at least 24 characters. Startup verifies evidence and the existing dormant identity; it does not initialize an organism or apply migrations. Canonical preparation was performed by the reviewed one-time migration and is reported in [migration evidence](RUNTIME_V1_MIGRATION_REPORT.md). Do not rerun the baseline-specific apply script on the migrated database.

Public reads expose allowlisted DTOs, not raw organism state. `/api/replay?id=...` supplies genuine saved frames. Authenticated `/api/cycle` and `/api/control` return locked; unauthenticated mutations are rejected. There is no approval/financial dispatch API.

## Portable hosting and public launch

- Vercel: Next.js frontend/stateless proxy.
- Railway or another Docker host: standalone observation runtime, independent of browser lifetime.
- Postgres/Supabase: identity, history and additive life state.

No GPT Sites or ChatGPT hosting dependency. [DEPLOYMENT.md](DEPLOYMENT.md) contains dormant-only deployment instructions. The public countdown uses `GENESIS_AWAKENS_AT=2026-09-29T00:00:00-07:00`; reaching zero does not authorize execution. [PREAWAKENING.md](PREAWAKENING.md) describes the presentation gate and development-only preview.

## Economy and language

Simulated economy, on-chain holdings and attributed revenue remain distinct. Wallet identity is unresolved until an operator supplies authoritative provenance for the existing address. No address is guessed, signer created, balance inferred or transfer called revenue.

PlannerV2 has a strict proposal/defer/abstain/assistance contract, an explicitly product-level deterministic fallback, and a language-provider adapter tested with injected transport. The deployed composition uses neither live provider calls nor automatic fallback after provider failure. Real provider-cost reservation/reconciliation and a reviewed execution grant are prerequisites to activating paid reasoning.

## Review package

- [Implementation](RUNTIME_V1_IMPLEMENTATION_REPORT.md)
- [Preservation](RUNTIME_V1_PRESERVATION_REPORT.md)
- [Tests](RUNTIME_V1_TEST_REPORT.md)
- [Migration](RUNTIME_V1_MIGRATION_REPORT.md)
- [Awakening readiness](RUNTIME_V1_AWAKENING_READINESS.md)

Implementation is ready to inspect; activation blockers remain. No new biological capability is claimed.

# Completion audit — verification summary

20 September 2026. Audit only; no implementation or activation.

## Canonical preservation

Before and after row-export SHA-256:

`4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`

The complete exported row objects are equal. This includes original identity/birth, seven decisions/memories, project, economy, saved brain, schedule, extension state and migration ledger. No private row text is included in the public-facing report.

| Final invariant | Observed |
|---|---|
| Original organism | `817e772c-827e-48fc-8e35-6504cb2a8d2d` |
| Original birth | `2026-09-15T01:56:07.867Z` |
| Decisions | 7 |
| Execution | CLOSED |
| Schedule | DISABLED |
| Biology | SAVED-OBSERVATION-ONLY |
| Canonical V2 cycles | 0 |
| Provider calls during audit | 0 |
| Wallet actions during audit | 0 |
| External communications during audit | 0 |
| Canonical migrations applied during audit | 0 |
| Other canonical client sessions at final export | 0 |

- [Canonical before](canonical-before.json)
- [Canonical after and action counts](canonical-after.json)
- [Canonical field counts](canonical-inventory.json)
- [Actual catalog: tables, indexes, constraints, triggers, functions, role flags](canonical-schema.json)
- [Protected source preservation: 200 files, zero mismatches](source-preservation.json)
- [Frozen inventory: 9,319 files, zero mismatches](frozen-preservation.json)

Private read-only row exports: `outputs/completion-audit/PRIVATE_BEFORE.json` and `PRIVATE_AFTER.json`, both mode 0600. These are local audit artifacts, not files served by Next/public APIs. The frozen inventory comparison is against the existing immutable-content list at `outputs/awakening-preparation/FROZEN_BEFORE.json`; it does not mutate or rerun studies.

## Verification results

| Check | Result | Evidence |
|---|---|---|
| Existing full test suite against dedicated local test DB | **162 passed; 0 failed; 0 skipped; 0 cancelled** | [Completed test log](tests-local-postgres.txt) |
| TypeScript | PASS, exit 0 | [Serial typecheck](typecheck-after-build.txt) |
| ESLint | PASS, exit 0 | [Lint](lint.txt) |
| Next production build, CI Webpack invocation | PASS, exit 0 | [Build](build.txt) |
| Next default/Vercel Turbopack invocation | BLOCKED_BY_ENVIRONMENT, exit 1, including elevated retry | [Retry log](build-default-local.txt) |
| Docker | BLOCKED_BY_ENVIRONMENT: executable absent | [Environment](environment.json) |
| Actual Railway/Vercel/managed DB target | Not remotely queried, deployed or verified; no local project linkage found | [Environment](environment.json) |
| One-shot journal → existing intent transition consumer | **Compatibility defect reproduced**, without database or model | [Probe result](intent-compatibility.json) |

Commands were `node --env-file=outputs/runtime-v1/test-db.env --test tests/*.test.ts`, `npm run typecheck`, `npm run lint`, `npm run build -- --webpack`, and `npm run build`. Test helpers require the dedicated `genesis_runtime_v1_test` database and disposable schemas. Active test transports are mocks. Existing legacy neural tests execute isolated test models, never canonical biology.

The audit-only intent probe copies the record shape from `OneShotController.journal` into memory and calls `transitionIntent`. It fails because `policy` is absent; there is no canonical request, grant, event or effect. [Probe source](intent-compatibility-probe.mjs).

### Retained unsuccessful verification attempts

- [First test log](tests.txt): 81 passed / 81 failed on denied local Postgres connections (`EPERM`). Local-only authorized rerun passed all 162. No implementation fix was made.
- [First typecheck](typecheck.txt): raced against concurrent Next build generation/removal of `.next/types`. Serial rerun passed. This was an audit command-order issue, not a repaired source defect.
- [Default build](build-default.txt) and [elevated retry](build-default-local.txt): Turbopack/PostCSS tried to create a worker and bind a local port; the environment returned `Operation not permitted`. Webpack success is not substituted for default-build success. No additional workaround was attempted.

The suite writes generated build caches and an existing migration dry-run artifact under `outputs/runtime-v1/` on an isolated restore. No implementation file was changed: every one of the 200 recorded source/config/data/document hashes matched afterward. The audit created only this report/evidence set and ignored local audit/build outputs. Existing working-tree modifications predated this audit and were not reset, committed or refactored.

## What was not claimed or performed

No live provider, wallet RPC, remote CI query, target-host verification, Docker execution, browser-layout re-review, deployment, new neuroscience run, migration installation or canonical cycle. Existing screenshots are not counted as current tests. No public leak was found in inspected allowlists/canary tests; this is not a comprehensive penetration-test certification. Current DB superuser flags are a production hardening finding, not evidence of an observed attack.

See [full completion audit](GENESIS_COMPLETION_AUDIT.md), [machine-readable checks](checks.json), and the final evidence hash manifest. Remaining work is documented, not implemented.

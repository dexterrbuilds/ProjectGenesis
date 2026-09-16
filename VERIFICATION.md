# Project Genesis verification — 2026-09-16

This report records local verification of the interrupted migration and the subsequent hackathon changes. No production deployment was performed.

## Preservation

The Postgres organism was compared with the pre-migration JSON export using deep equality, including all complete decision records:

- Organism: `817e772c-827e-48fc-8e35-6504cb2a8d2d`
- Original birth: `2026-09-15T01:56:07.867Z` (September 14 in the local Pacific timezone)
- Original committed cycles: **7**
- Brain snapshot, simulated wallet, memories and projects: **unchanged**
- All seven original decisions, including neural frames: **unchanged**
- New tests operate on temporary Postgres schemas; they do not advance the original life.

SHA-256 hashes match the pre-migration baseline:

| File | SHA-256 |
| --- | --- |
| `core/brain/celegans.ts` | `0ee044fcd922e4916340a6c7083903a310ae3af7998d07c2eefc910169806fec` |
| `data/connectome.json` | `1b8bc920fe1899b1bf8350acec84539d34ffe7f4d5351a4d5627fb786344babe` |
| `tests/brain.test.ts` | `546c29e0716eed3ecccab741a595b5ac7a6ad73ff5c818f4e33b907c50c98c93` |

## Automated results

**25 tests passed, zero failures, zero skipped** when running with the local development `TEST_DATABASE_URL`:

```sh
node --env-file=.env --test tests/*.test.ts
npm run typecheck
npm run lint
npm run build
npm run demo
```

The default `npm test` intentionally skips the two Postgres tests when no test database URL is supplied. `npm run test:postgres` loads the local environment and runs both.

| Requirement | Evidence |
| --- | --- |
| 302 real named neurons and source integrity | Original biological-data test and pinned-source checksums |
| Connectivity materially changes behavior/action | Neural propagation and closed-loop ablation tests |
| Determinism and persistent brain state | Replay, bounded dynamics, JSON restore and database snapshot equality |
| Concurrent-cycle locking | Two simultaneous Postgres claims: exactly one succeeds; stale lease commit rejected |
| Pause/resume persists | Pause during commit survives; paused standalone runtime is stopped/restarted and remains paused; resume survives another restart |
| Browser-independent autonomous cycles | Spawned `runtime/main.ts` completes a bounded schedule with no frontend process in that test |
| Restart recovery | Actual Node child process stopped and restarted three times; identity, birth, brain, wallet and schedule retained |
| Constrained LLM | Tests accept legal output and reject drive overrides; failed/incomplete provider responses never silently switch to local |
| Wallet isolation | Exact finalized lamports, partial configuration rejection, persisted/stale observations and unchanged simulated wallet |
| Vercel frontend | Standard Next.js production build completes; API routes proxy to runtime |
| Railway runtime | Standalone Node HTTP process starts, applies migrations and passes health/API tests independently of Next.js |
| No GPT Sites dependency | No Sites/Vinext/Cloudflare runtime dependencies in package files, application imports or deployment configuration |

Lint was repaired to exclude historical generated directories and correct application-level issues. These directories are ignored artifacts, not deployment inputs. Docker copies only the portable runtime, core, data/license, store and package files.

## Interface verification

The local Next.js page was checked at desktop and phone widths. The original birth and seven life records, simulated balance **$100.75**, first project and income milestones were visible. The selected danger event displayed **ASHL/ASHR, input 1.600 each**. Scrubbing its genuine saved frames moved the displayed tick from **560 to 480**; no life cycle was created. The eight-stage chain displays the saved next stimulus (danger 0.05 / novelty 0.65 for that decision). A stale development stylesheet was corrected by restarting the dev server. The final production build passed from a clean generated cache outside the local sandbox; Turbopack’s CSS worker needed a local port that the sandbox denied.

## Limits of verification

- **Live LLM call:** not run; `OPENAI_API_KEY` and `OPENAI_MODEL` are absent. `npm run check:llm` reports this and sends no request. The adapter and provider contract tests are ready.
- **Live Solana wallet:** no RPC/address/network configured. Read-only adapter behavior and persistence were tested using RPC doubles confined to tests.
- **ClawPump:** intended provider not yet confirmed; similarly named services expose different APIs. No fee source, transaction or income was fabricated. The verified-reader interface remains available.
- **Docker image:** not built locally because Docker is unavailable. The GitHub workflow includes an image build; it has not been run in this session.
- **Vercel/Railway:** configuration and portable runtime are supplied; no hosted deployment or provider-specific smoke test was performed.
- A passing ablation test proves that the wiring participates in computation. It does not validate a biological reproduction of a worm.

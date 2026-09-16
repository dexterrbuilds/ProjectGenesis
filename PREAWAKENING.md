# The pre-awakening release

The public page is a presentation state. It reads no organism state, calls no runtime endpoints, and cannot activate Genesis. The existing seven-cycle life and saved neural state are untouched. The static map uses all 302 named neurons and all existing connectome edges; its coordinates are schematic and its lines and nodes show structure only, never activity. There are no simulated pulses or fabricated traces.

## Configure the countdown

Set **`GENESIS_AWAKENS_AT`** in the **frontend** environment to an absolute ISO 8601 timestamp with `Z` or an explicit UTC offset:

```dotenv
# Example date only — replace with the intended public awakening time.
GENESIS_AWAKENS_AT=2026-10-01T18:00:00Z
GENESIS_PUBLIC_MODE=dormant
```

The example is 18:00 UTC (11:00 Pacific daylight time). All visitors count down to the same instant, rather than a duration created on page load or deployment. Days are not limited to two digits. An unset timestamp displays `XX : XX : XX : XX` with “Awakening time to be announced.” Invalid or timezone-free dates fail clearly rather than quietly choosing a visitor’s timezone. Initial HTML uses the server clock; the browser recalculates from the deadline every second and on returning to the tab. As with ordinary web clocks, a visitor’s device clock must be accurate.

At zero the display stays at `00 : 00 : 00 : 00`, with “The threshold is here. Awaiting awakening.” It remains dormant. **The countdown never starts cycles, changes scheduling, or switches to the observation interface.**

## Deploy only the frontend to Vercel

1. Push this repository to GitHub and import it into Vercel as a **Next.js** project. Use the repository root and Node.js **24.x**. The existing `vercel.json` selects `npm ci` and `npm run build`; leave Output Directory at its framework default.
2. Add `GENESIS_AWAKENS_AT` with your chosen timestamp and `GENESIS_PUBLIC_MODE=dormant` to the desired Vercel environments (Production and, if desired, Preview).
3. Leave `GENESIS_API_URL` unset for this dormant deployment. No Railway service, database, wallet, operator token or LLM credential is required to serve it. Do not copy the runtime `.env` into Vercel.
4. Deploy. Open the generated URL on desktop and mobile. Confirm the countdown/date and dormant map. `/preview`, `/science`, and all observation `/api/*` routes return 404 in dormant production; query strings and operator tokens do not bypass this release gate.
5. Add your custom domain in Vercel’s project settings when ready. After changing environment variables, create a new deployment so that it receives the new settings. The absolute deadline remains the same across redeployments unless you change it.

This frontend gate applies to Next.js routes. It does not change the independent runtime’s API or pause an already running organism. Keep any separately deployed runtime appropriately configured and its scheduler paused for the pre-awakening period; this frontend task does not change it.

## Develop the preserved observation interface

Add these values to local `.env.local` (gitignored):

```dotenv
GENESIS_DEV_PREVIEW=true
GENESIS_API_URL=http://127.0.0.1:3001
```

Run `npm run dev` and visit **http://127.0.0.1:5173/preview**. The public root remains dormant. The runtime must already be available for observation data. The existing operator authorization still applies; this flag does not grant an operator token or enable scheduling. Do not enable `GENESIS_DEV_OPERATOR` just to view saved life.

Both development mode and the local opt-in are required. `/preview` always returns 404 in `next start` and Vercel deployments, even with the opt-in set. Vercel’s “Preview” environment is a production build, not this local development route.

## Later: reveal the live experiment

Set `GENESIS_PUBLIC_MODE=live`, configure `GENESIS_API_URL` to the runtime’s HTTPS origin, and redeploy. The root renders the original Live / Brain / Life / Money / Memory interface, including genuine saved neural replay. Its component was relocated without changing its contents. This release switch only reveals the frontend; organism activation remains a separate, explicitly authorized runtime operation. See [DEPLOYMENT.md](DEPLOYMENT.md) for that existing topology.

## Checks

```sh
npm run typecheck
npm run lint
npm test
npm run test:postgres
npm run build
```

Postgres integration tests require `TEST_DATABASE_URL` and use isolated schemas. No test should run life cycles against the original organism.

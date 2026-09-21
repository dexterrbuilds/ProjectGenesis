# Public Live Observer Redesign

Date: 2026-09-20. Scope: frontend and development-only public presentation fixtures. No awakening, deployment, runtime change, biological execution or canonical migration.

## Result

The observer is now one continuous page, with deeper Brain, Life, Money, Memory and About views. The public root still serves the unchanged dormant countdown. Review images and checklist: [operator review](verification/public-observer-redesign/README.md).

Genesis remains dormant. This review package is not activation approval.

## Design and information hierarchy

The Live page moves from identity and age to a dominant, static connectome, a large current/last-recorded activity description, a bounded explanation, recent experiences, memory, projects/questions and scientific context. Quiet simulated-resource information sits beside the desktop activity area and below it on mobile. Typography and whitespace organize the story; there is no grid of equal dashboard cards, performance chart, trading panel or decorative telemetry.

Six minimal navigation links retain evidence/detail access. On mobile they open from an accessible Explore button. The pages use query navigation, preserving back/forward history without new backend routes. A persistent development-only banner remains visible while scrolling. Saved-replay controls stay disabled until the graph is ready. The preview supports reflection, local artifact, abstention, assistance, defer, permission denial and incomplete reasoning examples.

### Four questions

| Question | Presentation | Evidence limitation |
|---|---|---|
| What is Genesis doing? | Prominent last-recorded moment, or dormant status | The current DTO does not assert an in-progress thought. The UI does not invent one. |
| Why? | Expandable, deterministic description of recorded proposal/permission/outcome | No raw rationale, hidden reasoning or inferred motives. |
| What happened? | Chronological public feed with translated causal details | Earlier records have neutral summaries and retain their disclaimer. |
| How is it changing? | Preserved memory/project counts and computational-life section | Canonical excerpts, interests and project details are currently withheld by the public projection. Rich examples appear only in clearly marked development fixtures. |

The DTO does not distinguish a reflection from another saved local text artifact. Both say “Genesis saved something locally.” The UI does not claim either event produced a particular insight or project.

## Screenshot evidence

All post-awakening screenshots are **NOT CANONICAL / NOT AWAKENED / DEVELOPMENT FIXTURE**. No synthetic event was inserted into Genesis. The fixture ages/counts/resources are presentation examples derived from the existing sanitized fixture; the example text is explicitly illustrative.

| Review | Evidence |
|---|---|
| Desktop Live, activity, recent life, money, memory, becoming | [Hero](verification/public-observer-redesign/desktop-live.jpg), [activity and life](verification/public-observer-redesign/desktop-current-life.jpg), [memory](verification/public-observer-redesign/desktop-live-memory.jpg), [becoming](verification/public-observer-redesign/desktop-live-becoming.jpg) |
| Bounded Why disclosure | [Expanded explanation](verification/public-observer-redesign/desktop-live-why.jpg) |
| Structure / saved response | [Static](verification/public-observer-redesign/desktop-brain-structure.jpg), [saved](verification/public-observer-redesign/desktop-brain-saved.jpg) |
| Life / translated causal detail | [Life](verification/public-observer-redesign/desktop-life.jpg) |
| Money / Memory / About | [Money](verification/public-observer-redesign/desktop-money.jpg), [Memory](verification/public-observer-redesign/desktop-memory.jpg), [About](verification/public-observer-redesign/desktop-about.jpg) |
| Scientific explanation | [Science](verification/public-observer-redesign/desktop-science.jpg) |
| Dormant experience | [Desktop](verification/public-observer-redesign/desktop-dormant.jpg), [mobile](verification/public-observer-redesign/mobile-dormant.jpg), [production](verification/public-observer-redesign/production-dormant.jpg) |
| Mobile Live | [390 × 844](verification/public-observer-redesign/mobile-live.jpg), [375 × 812](verification/public-observer-redesign/mobile-375-live.jpg) |
| Mobile alternate moments | [Abstention](verification/public-observer-redesign/mobile-abstention.jpg), [assistance](verification/public-observer-redesign/mobile-assistance.jpg), [denial](verification/public-observer-redesign/mobile-denied.jpg) |
| Mobile detail pages | [Brain](verification/public-observer-redesign/mobile-brain-saved.jpg), [Life](verification/public-observer-redesign/mobile-life.jpg), [Money](verification/public-observer-redesign/mobile-money.jpg), [Memory](verification/public-observer-redesign/mobile-memory.jpg), [About](verification/public-observer-redesign/mobile-about.jpg) |
| Mobile navigation | [Menu](verification/public-observer-redesign/mobile-navigation.jpg) |

Actual browser review used the Codex in-app browser at 1280 × 900, 390 × 844 and 375 × 812. All measured mobile views had document width equal to viewport width. Final captures use native viewport screenshots. The browser’s full-page stitching duplicated content, so those captures were replaced. Separate viewport images document lower-page sections. Fixtures were navigated and selected through the UI; replay was explicitly requested.

## Copy and causal trace

| Structured record | Public wording |
|---|---|
| Biology `not_applied` | “The biological system wasn’t involved in this decision.” |
| Denial | “Genesis wasn’t allowed to do this.” |
| Assistance | “Genesis asked for help.” / “No message was sent. The request remains pending.” |
| Abstention | “Genesis decided not to act this time.” |
| Deferral | “Genesis left this for another time.” |
| Failed reasoning record | “Genesis couldn’t complete its reasoning this time.” |
| Missing revenue attribution | “No verified earnings to report.” |
| Missing wallet identity | “A public wallet has not been verified.” No $0 substitution. |
| Historical decoder label | Hidden inside expanded history with “not a validated biological action and has no authority now.” |

Expanded moments separate the record, biological involvement, rule-based versus language-model planning, permission facts, outcome and computational memory change. They do not display hashes, revisions, leases, grant IDs, model transport names, raw prompts or planner rationale.

## Privacy verification

The existing backend public DTO remains authoritative and unchanged. A frontend Zod allowlist discards unknown fields, including nested fields, before narration. There is no public-private endpoint switching, operator credential forwarding or expanded backend disclosure.

Adversarial tests inject private context, memory text, project details, approval payloads, raw rationale, provider secrets and operator fields. These are absent from the accepted DTO and generated copy. Canonical memory/project details are not fetched or rendered. The two new development endpoints return only the public graph or an explicitly selected saved activity array from the existing sanitized fixture; the full fixture is never returned.

Production HTTP verification, with `GENESIS_PUBLIC_MODE=dormant` and even `GENESIS_DEV_PREVIEW=true`, returned:

- `/`: 200, dormant page, no fixture payload.
- `/preview`, `/api/preview/graph`, `/api/preview/replay`: 404.
- `/api/state`, `/api/brain`, `/api/history`, `/api/replay`: 404.

Only local read-only GETs were used. No canonical cycle endpoint was invoked. See [production access results](outputs/observer-redesign/production-access.json). Existing suite coverage of server public projections also passes. This is a scoped application/privacy review, not a formal penetration test.

## Scientific honesty

- Genuine C. elegans nodes/edges are reused; positions are explicitly schematic.
- The default network contains no invented firing, time-varying activity or decorative activity frames.
- Saved activity is fetched only after explicit selection and is labeled historical. The fixture is an actual previously saved snapshot. Its precise recording time and stimulation labels are unavailable and remain unavailable.
- No current event stimulates, advances or reruns a model. Biology is separate from planning and computational life.
- Legacy decoder words remain in source records unchanged and appear only with an explanatory disclaimer.
- Simulated resources, onchain observation and attributed revenue remain distinct. Missing balance/revenue is null, never invented zero or inferred earnings.
- The interface makes no claim that Genesis runs a fly brain, that Stage 1 controls current decisions, or that Stage 5 establishes biological propagation. About and scientific detail preserve these limitations.

## Performance and accessibility

The memoized canvas has no animation loop, polling or random firing. Geometry is memoized; stable recorded-frame references prevent unrelated age/activity updates from redrawing it. Drawing occurs only on graph/frame changes or resize. Device pixel ratio is capped at 2. A text equivalent and canvas-unavailable fallback are provided.

Historical arrays are not requested on initial Live load. The technical neuron inspector is lazy-loaded behind disclosure. Ordinary public state refresh is every 15 seconds, skips hidden tabs and overlapping requests, aborts on unmount, and retains identical state objects. Preview mode never polls the runtime. Age updates once a minute.

The redesign adds no continuous motion. A scoped reduced-motion rule disables animations/transitions/scroll motion. Semantic headings, lists, time elements, native disclosures, labels, current-page navigation, skip link and visible keyboard focus are retained. Mobile navigation is collapsible with `aria-expanded`. Browser inspection confirmed 302-neuron textual alternatives and no horizontal overflow at both tested phone widths. No formal screen-reader certification or long-duration CPU benchmark is claimed.

## Tests and build

| Check | Result |
|---|---|
| Full suite, dedicated isolated test database | **162 passed, 0 failed, 0 skipped** |
| New observer tests | 12 passed (included above) |
| TypeScript | Passed |
| ESLint | Passed |
| Next.js production build (webpack) | Passed |
| Desktop/mobile actual browser review | Completed |
| Production dormant/preview access | Passed |

Commands: `node --env-file=outputs/runtime-v1/test-db.env --test tests/*.test.ts`, `npm run typecheck`, `npm run lint`, `NEXT_TELEMETRY_DISABLED=1 npm run build -- --webpack`.

Logs: [tests](outputs/observer-redesign/full-tests.log), [TypeScript](outputs/observer-redesign/typecheck.log), [lint](outputs/observer-redesign/lint.log), [build](outputs/observer-redesign/build.log).

During warm development navigation, the existing countdown emitted one hydration mismatch and a Next development mount warning. Evidence is retained in `verification/public-observer-redesign/browser-console.json`. Both fresh development pages and a fresh production countdown returned empty warning/error logs. No countdown code was changed. During rapid development-route navigation, one server response returned `Unexpected end of JSON input`; a reload immediately recovered, without an application-code correction. That event remains in `outputs/observer-redesign/preview-final.log`. No recurring failure was observed. Production build also prints the existing Node 26 `module.register()` deprecation warning; it does not fail the build.

## Exact implementation scope

- Replaced `components/live-observation.tsx` presentation with the continuous observer and drill-down views.
- Added `components/observer/network.tsx` and scoped `observer.css`.
- Added `lib/observer-presentation.ts`: allowlist, deterministic narration, resource/age helpers.
- Added `lib/observer-fixtures.ts`: explicitly synthetic, public-safe presentation examples; no runtime execution.
- Updated `app/preview/page.tsx` to supply those examples after the existing development-only gate.
- Added development-only read routes in `app/api/preview/[kind]/route.ts` for the graph and genuine saved fixture snapshot.
- Added `tests/observer-presentation.test.ts`, this report and the separate review/evidence directory.

Existing uncommitted runtime/research work was preserved. No backend public DTO, runtime implementation, schema, policy, constitution, provider configuration, wallet configuration, scientific model or release flag changed. No new dependencies were installed.

## Preservation and final state

Read-only before/after audits show identical canonical rows and digest:

`4c5f33972c6212a24fe5386b9c5c499df94ddbfebd2a26639333566604e56220`

Identity, birth, seven memories, original project/economy/history and saved brain snapshot remain unchanged. No migration or grant was applied.

| Invariant | Final |
|---|---|
| Organisms | 1, original Genesis 001 |
| Canonical decisions | **7** |
| Canonical V2 cycles | **0** |
| Execution | **CLOSED** |
| Schedule | **DISABLED** |
| Biology | **SAVED-OBSERVATION-ONLY** |
| Live provider calls during this pass | **0** |
| Wallet actions | **0** |
| External communications | **0** |

All 52 pre-pass architecture/dormant protected files match. All 9,319 frozen research/data files (15,967,076,255 bytes) match the preservation manifest. See [file audit](outputs/observer-redesign/file-preservation.json) and [sanitized canonical audit](verification/public-observer-redesign/preservation.json). Private database snapshots remain in ignored local audit outputs, outside public routes and the screenshot package.

## Human review and limits

Human aesthetic/disclosure approval remains pending. The preview demonstrates how future records will appear; it does not claim current activity. Canonical memory excerpts, project descriptions and per-tool local-action names cannot be displayed unless separately admitted by the authoritative public projection. This pass deliberately did not broaden it.

Preview again with `GENESIS_DEV_PREVIEW=true GENESIS_PUBLIC_MODE=dormant npm run dev -- --webpack`, then open `/preview`. This starts only the Next frontend. The public `/` remains dormant. Temporary verification servers were stopped after review.

PUBLIC LIVE OBSERVER REDESIGN COMPLETE — READY FOR HUMAN REVIEW

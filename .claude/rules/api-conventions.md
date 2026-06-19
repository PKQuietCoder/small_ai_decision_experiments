# API conventions

`server/API_CONTRACT.md` is the **source of truth** for request/response shapes. Keep it, the
FastAPI handlers (`server/app/main.py`), and the client types (`artifacts/client/src/lib/api.ts`)
in sync — if you change a shape, update all three.

- All endpoints live under the `/api` prefix, are **read-only and GET-only**, and require no auth.
- The frontend builds URLs as `` `${import.meta.env.BASE_URL}api/...` `` and calls `fetch`
  directly (`lib/api.ts`). Do not introduce the generated client packages under `lib/*`.
- Treat response objects as **open** (extra keys may be added); clients read the keys they need.
- Draft (unpublished) content is served **only** in the dev workspace and **only** with
  `?preview=1`; production (`REPLIT_DEPLOYMENT=1`) never returns drafts. Don't weaken this gate.
- `bodyHtml` and `aboutHtml` are server-rendered HTML from Markdown — rendered with
  `dangerouslySetInnerHTML`; keep rendering on the trusted server side, not from user input.
- Analysis JSON drives the charts; its shape (`byVariant` / `overall` / `perModel` /
  `decisionOptions`) is produced by `content_store.build_analysis`. Changing it is an API change.

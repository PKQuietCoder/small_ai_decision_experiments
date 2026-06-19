---
name: deploy
description: Build, run, and deploy this app (FastAPI backend + React/Vite client, hosted on Replit). Use when asked to run the app locally, serve it, build it, or prepare/ship a deployment.
---

# Deploy / run

This repo is a pnpm workspace: a Python FastAPI backend (`server/`) and a React+Vite client
(`artifacts/client/`). On Replit they run as two workflows (`api-server`, `client`) and deploy
via `application` router + `autoscale`. See `deploy-config.md` for ports, env vars, and secrets.

## Run locally
- Backend: `python server/serve.py` (reads `PORT`, defaults to 8080). This is the real entry
  point — `main.py` at the repo root is an unused placeholder.
- Client: `PORT=<port> BASE_PATH=/ pnpm --filter @workspace/client run dev` (vite.config throws
  if `PORT` or `BASE_PATH` is unset). The client fetches `/api/...`, so the backend must be
  reachable at the same origin.

## Build
- `pnpm run build` — typechecks the workspace, then builds each artifact (client → `dist/public`).

## Deploy (Replit)
- Deployment target is `autoscale` with `router = "application"` (`.replit`).
- Required secrets in the deployment environment: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`
  (only needed to *run experiments*; the public site serves pre-recorded content and works
  without them).
- Drafts are never served in a deployment (`REPLIT_DEPLOYMENT=1` disables `?preview`).

## Gotchas
- The client workflow must bind a **reserved mapped port** (`.replit` `[[ports]]`); an unmapped
  port makes the workflow fail even though Vite prints "ready".
- Restart the `api-server` workflow after editing backend code (module state is cached).

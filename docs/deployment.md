# Running and deploying

The app is two processes: a FastAPI backend (the API + experiment engine) and a
React/Vite client. There is no database; all content is files under `content/`.

## Prerequisites

- Python, managed with [`uv`](https://docs.astral.sh/uv/).
- Node, managed with [`pnpm`](https://pnpm.io/) (npm/yarn are blocked by a
  preinstall hook).
- Optional: provider API keys, only to run experiments. Copy
  [`../.env.example`](../.env.example) to `.env`.

```bash
uv sync          # Python deps
pnpm install     # JS deps
```

## Run locally

```bash
# Backend (reads PORT; defaults to 8080). The real entry point is serve.py.
python server/serve.py

# Frontend (requires PORT and BASE_PATH).
PORT=5173 BASE_PATH=/ pnpm --filter @workspace/client run dev
```

After editing **server** code, restart the backend — FastAPI caches module
state, so engine/stats changes do not take effect until the process restarts.

## Build

```bash
pnpm run typecheck   # typecheck the whole workspace (there is no test suite)
pnpm run build       # typecheck + build all artifacts
```

## Deploy (Replit)

This project is configured to run on Replit. The deployment-specific details —
workflow definitions, the reserved mapped client port, and the
`REPLIT_DEPLOYMENT` gate that keeps drafts out of production — are documented in
the deploy skill and operating notes:

- [`../.claude/skills/deploy/SKILL.md`](../.claude/skills/deploy/SKILL.md) —
  build / run / deploy steps.
- [`../replit.md`](../replit.md) — stack, ports, and gotchas.

Key gotchas worth repeating: the client web service needs a **reserved mapped
port** (an unmapped port fails the workflow even when Vite prints "ready"), and a
post is only public with `published: true` in its frontmatter.

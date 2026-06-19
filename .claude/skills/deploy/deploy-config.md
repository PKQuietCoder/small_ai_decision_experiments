# Deploy config reference

## Environment variables
| Var | Used by | Notes |
|-----|---------|-------|
| `PORT` | `server/serve.py`, client `vite.config.ts` | Backend defaults to 8080; the client **requires** it (throws if unset). |
| `BASE_PATH` | client `vite.config.ts` | **Required** for the client; sets Vite `base` (use `/`). |
| `REPLIT_DEPLOYMENT` | `server/app/main.py` | Set to `1` in deployments; disables draft `?preview`. |
| `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` | `server/experiments/llm_clients.py` | Needed only to run experiments, not to serve the site. |

## Ports (`.replit` `[[ports]]`)
`localPort → externalPort`: 8080→80, 8081→8081, 8082→3001, 8098→3000, 8099→8099, 20517→3002.
Bind the dev/web service to one of these mapped local ports.

## Build output
- Client: `artifacts/client/dist/public` (Vite `build.outDir`).
- `pnpm run build` = `typecheck` then per-package `build`.

## Package managers
- JS: **pnpm only** (npm/yarn blocked by the root `preinstall` hook; `pnpm-workspace.yaml`
  enforces a 1-day `minimumReleaseAge` supply-chain delay).
- Python: **uv** (`uv sync`).

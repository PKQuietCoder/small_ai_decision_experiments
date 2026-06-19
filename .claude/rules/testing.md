# Testing & verification

**There is no automated test suite** (no pytest, no JS test runner). Do not invent one or
add test commands that don't exist. Verify changes by exercising the real pipeline:

## Static checks
- `pnpm run typecheck` — typechecks the whole workspace (run after any TS change).

## Backend / experiment changes
- Smoke-test an LLM client change with a single trial before a full run (cheap):
  load a model from `server/experiments/model_catalog.py` and call `decide()` / `respond()`.
- End-to-end: `python -m server.run_experiment <id> --model <key> --no-post` and confirm
  `N/N trials parsed successfully` with `parseFailures: 0` and a low `excluded` count.
- Inspect the written analysis under `content/analysis/<id>/<runId>.json`
  (`overall.testable`, counts sum per condition, baseline overlay rows if configured).
- Confirm the post + analysis load via `server.app.content_store.get_post(slug)` rather than
  only eyeballing the JSON.

## Frontend changes
- Run the client (`PORT=… BASE_PATH=/ pnpm --filter @workspace/client run dev`) and load the
  affected page; charts render from the analysis JSON, so verify against a real run.

## After editing server code
- Restart the backend — FastAPI caches module state, so changes won't take effect until the
  `api-server` workflow restarts.

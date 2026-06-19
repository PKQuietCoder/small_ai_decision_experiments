# LLM Decision Science Blog

A Statsig-style blog that publishes small, careful experiments on how language models actually decide. The current experiment ("The Metaphor Trap") is a faithful replication of Thibodeau & Boroditsky's 2011 crime-metaphor study: each model reads the paper's exact report and answers its exact open-ended question, varying only one word — is crime a "beast" or a "virus"? — and the results are compared against the paper's human baseline.

## Run & Operate

- `python /home/runner/workspace/server/serve.py` — run the FastAPI backend (reads `PORT`, served via the `api-server` artifact workflow).
- `pnpm --filter @workspace/client run dev` — run the React + Vite frontend (served via the `client` artifact workflow).
- `python -m server.run_experiment <experiment_id>` — admin CLI: run an experiment (calls OpenAI + Anthropic), persist the run JSON, and auto-generate an editable draft Markdown post. Flags: `--no-post` (skip post), `--keep-post` (only refresh runId).
- Required secrets: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` (read directly from env via the official SDKs — NOT the Replit AI proxy).

## Stack

- Backend: FastAPI (Python), file-based content — no database.
- Frontend: React + Vite + Wouter routing + Recharts (analysis charts).
- LLM access: official `openai` and `anthropic` Python SDKs.
- Statistics: NumPy + SciPy (chi-square test of independence, Cramér's V, Wilson intervals).

## Where things live

- API endpoints + JSON shapes: `server/API_CONTRACT.md` (source of truth for the frontend).
- FastAPI app: `server/app/main.py`; content read/aggregation: `server/app/content_store.py`.
- Experiment engine (parallel trial execution): `server/experiments/engine.py`; stats: `server/experiments/stats.py`; SDK wrappers: `server/experiments/llm_clients.py`.
- Admin CLI: `server/run_experiment.py`; post generator: `server/experiments/post_generator.py`.
- Content (file-based): experiments in `content/experiments/*.yaml`, recorded runs in `content/runs/<experiment_id>/*.json`, posts in `content/posts/*.md`.
- Frontend: `artifacts/client/src/` (pages in `App.tsx`, API client `lib/api.ts`, charts `components/charts/analysis-charts.tsx`).

## Architecture decisions

- **No database, no auth.** All content is files on disk; visibility is controlled per-post by a `published` flag in the Markdown frontmatter. Draft posts are returned only with `?preview=1`.
- **Experiments are CLI-driven**, never triggered from the public UI. Each run writes a run JSON and (re)generates a draft post linked by `runId`.
- **Trial execution is parallelized** (ThreadPoolExecutor, `MAX_WORKERS=8`) because a full run is hundreds of independent API calls; deterministic trial ordering is preserved via a pre-sized result array.
- **Chi-square prunes all-zero rows/columns** before testing — decision options no model ever chose carry no information and would otherwise make the test degenerate (zero marginals).
- **Client web service runs on a reserved mapped port** (see `.replit` `[[ports]]`); an unmapped port makes the workflow fail to start even though Vite reports "ready".

## Product

A reader-facing blog: a home feed of published experiment write-ups, an experiment index with run metadata, and per-post analysis charts (decision distribution by metaphor and by model) generated live from the recorded run.

## User preferences

- Use OpenAI + Anthropic via their official SDKs with keys from Secrets — do NOT use the Replit AI integration/proxy.
- Keep clean client/server separation; no in-app login/auth; no database (file-based content).

## Gotchas

- Anthropic model ids reach end-of-life; `claude-3-5-haiku-*` now 404s — use a current model (e.g. `claude-haiku-4-5`).
- Detached/background experiment runs get killed when the shell call returns; the parallel engine keeps a full run fast enough to complete within a single foreground call.
- The FastAPI server caches module state — restart the `api-server` workflow after editing server code (e.g. stats logic) for changes to take effect.

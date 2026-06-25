# Architecture

A small, file-based system: a Python/FastAPI backend with an experiment engine,
and a React/Vite frontend that renders posts with live charts. There is **no
database and no authentication** — all content is plain files on disk, and
publishing is editing a file.

## The content pipeline

An experiment is a single YAML config; everything else is derived from it and
stored as files.

```
content/experiments/<id>.yaml      the experiment as code (the source of truth)
        │  engine runs models × variants × trials against the live provider APIs
        ▼
content/runs/<id>/<runId>.json      raw per-trial data
        │  content_store.build_analysis aggregates + tests for significance
        ▼
content/analysis/<id>/<runId>.json  proportions, Wilson CIs, chi-square, overlays
        │  post_generator writes an editable draft (or it is hand-written)
        ▼
content/posts/<slug>.md             the write-up (Markdown + frontmatter)
        │  export_experiment bundles a self-contained, downloadable package
        ▼
experiments/<id>/                   methodology + raw + results + manifest + zip
```

The FastAPI app reads `content/` and serves it as JSON; the React client renders
each post's body plus charts built from the analysis JSON.

## Key modules (`server/`)

| Path | Role |
|---|---|
| `app/config.py` | All `content/` filesystem paths (relative to the repo root). |
| `app/settings.py` | Typed runtime config (API keys, port) via `pydantic-settings`. |
| `app/content_store.py` | Single source of truth for disk I/O and API shaping; `build_analysis()` does aggregation, significance, and the human-baseline overlay. |
| `app/main.py` | FastAPI handlers — read-only, GET-only, `/api/*`. |
| `experiments/engine.py` | Parallel trial execution (`ThreadPoolExecutor`); branches on the experiment `type`. |
| `experiments/llm_clients.py` | Official OpenAI / Anthropic SDK wrappers; `decide()` (enforced choice) and `respond()` (free text). |
| `experiments/model_catalog.py` | Selectable models and their capability flags. |
| `experiments/schemas.py` | Pydantic models that validate an experiment YAML on load. |
| `experiments/stats.py` | Chi-square test of independence, Cramér's V, Wilson intervals. |
| `experiments/post_generator.py` | Generates a draft post from a run. |
| `run_experiment.py`, `export_experiment.py`, `seed_sample.py` | Admin CLIs. |

## Experiment types (`type:` in the YAML)

- **`fill_in_blank_decision`** — the model picks one option from an enum;
  `llm_clients.decide()` enforces the choice via OpenAI structured outputs or
  Anthropic forced tool use (never regex parsing).
- **`open_response`** — the model answers free text (`respond()`), then a fixed
  judge model (`coder:` in the config) codes each answer into decision categories.
- **`agentic_budget`** — a multi-step tool-using decision; the final pick is read
  from a constrained tool field, with extra per-trial fields (planned budget,
  step sequence, capped flag).

Prompt templating substitutes the string fields of a variant into
`prompt_template` (e.g. `{scenario}`, or `{frame}` + `{spread}`); the only braces
allowed in a template are field placeholders.

## Model capability flags

`server/experiments/model_catalog.py` carries per-model flags because providers
disagree on request parameters, and getting them wrong is a 400:

- Opus 4.7/4.8 (and Fable/Mythos) **reject `temperature`** → it is omitted.
- GPT-5.x are reasoning models: they **reject `max_tokens`** (use
  `max_completion_tokens`), need a generous output budget (reasoning tokens count
  against it), and take `reasoning_effort`.

`decide()` / `respond()` build request kwargs from these flags. Confirm exact
model IDs and flags against the live provider APIs before adding a model — model
IDs reach end-of-life and 404.

## Configuration

Runtime settings are read once through `server/app/settings.py` (a
`pydantic-settings` model), from the environment or a local `.env` (see
[`../.env.example`](../.env.example)). Provider API keys are optional — the site
serves without them; only the experiment CLIs require them, validated at the
point of use.

## API

All endpoints are under `/api`, read-only, GET-only, and need no auth. The exact
request/response shapes are specified in
[`../server/API_CONTRACT.md`](../server/API_CONTRACT.md), which the frontend
follows by hand (it does not use a generated client). Response objects are
**open**: clients read the keys they need and tolerate extra ones — which is why
the API does not enforce pydantic response models that would strip them.

## Frontend

React + Vite + Wouter + Recharts under `artifacts/client/src/`. The client calls
`fetch` directly via `lib/api.ts`; its types mirror the API contract. The design
language is documented in
[`../.claude/rules/design-system.md`](../.claude/rules/design-system.md).

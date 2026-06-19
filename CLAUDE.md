# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

A file-based "LLM Decision Science" blog: it reruns classic human decision-bias experiments
on LLMs and publishes the results as posts with live statistical charts. Python/FastAPI
backend + React/Vite frontend, **no database and no auth** — all content is files on disk.

Two existing companion docs are authoritative and worth reading first:
- `replit.md` — operating notes, stack, architecture decisions, gotchas, user preferences.
- `server/API_CONTRACT.md` — the exact `/api` JSON shapes; the frontend's source of truth.

## Claude Code configuration layout (`.claude/`)

This repo follows the standard Claude Code project structure. **Maintain it** — when a
convention changes, update the relevant file here rather than only mentioning it in chat.

```
CLAUDE.md                  # this file — shared project guidance, loaded every session
CLAUDE.local.md            # personal local overrides (git-ignored)
.mcp.json                  # MCP server integrations (mcpServers; empty until one is added)
.claude/
├── settings.json          # shared settings (permissions, hooks) — committed; inert by default
├── settings.local.json    # personal settings overrides (git-ignored)
├── rules/                 # modular conventions, imported below so they load every session
│   ├── code-style.md
│   ├── testing.md         # NOTE: there is no automated test suite — how to verify instead
│   ├── api-conventions.md
│   └── design-system.md   # the site-wide "Nature PoV" design language (trust through restraint)
├── commands/              # custom slash commands (/review, /fix-issue)
│   ├── review.md
│   └── fix-issue.md
├── skills/                # task-triggered skills (loaded on demand by description)
│   ├── deploy/
│   │   ├── SKILL.md       # build / run / deploy this app
│   │   └── deploy-config.md
│   └── persuasive-writing/SKILL.md   # persuasion rules for marketing/email/pitch/landing copy
├── agents/                # specialized subagents
│   ├── code-reviewer.md
│   └── security-auditor.md
└── hooks/
    └── validate-bash.sh   # example PreToolUse hook — DISABLED (not wired into settings.json)
```

The modular rules are imported so they are always in effect:

@.claude/rules/code-style.md
@.claude/rules/testing.md
@.claude/rules/api-conventions.md
@.claude/rules/design-system.md

## Commands

Package managers: **pnpm** for JS (enforced — `npm`/`yarn` are blocked by a preinstall hook),
**uv** for Python (`uv.lock` + `pyproject.toml`).

```bash
uv sync                 # install Python deps
pnpm install            # install JS deps (workspace; note pnpm-workspace.yaml minimumReleaseAge=1 day)

# Backend (FastAPI). Reads PORT (defaults to 8080); real entry point, NOT main.py.
python server/serve.py

# Frontend (React+Vite). REQUIRES PORT and BASE_PATH env vars (vite.config throws without them).
PORT=5173 BASE_PATH=/ pnpm --filter @workspace/client run dev

# Typecheck (there is NO Python/JS test suite — typecheck + running the CLIs is how you verify)
pnpm run typecheck                                  # whole workspace
pnpm --filter @workspace/client run typecheck       # client only
pnpm run build                                       # typecheck + build all artifacts
```

### Experiment CLIs (admin-only; never triggered from the web UI)
```bash
# Run ONE model per run; persists run JSON + analysis JSON + a draft post.
python -m server.run_experiment <experiment_id> --model <key> [--no-post|--keep-post]
#   <key> ∈ opus | sonnet | haiku | gpt-5.5 | gpt-5.4 | gpt-5.4-mini  (omit --model for an interactive menu)

python -m server.export_experiment <experiment_id>   # build the downloadable data package under experiments/<id>/
python -m server.seed_sample <experiment_id>         # fabricate synthetic data to bootstrap the UI without API keys
```
Requires `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` in the environment (official SDKs, **not** the
Replit AI proxy). A run is hundreds of foreground API calls and must finish within the shell
call — backgrounded runs get killed when the call returns.

## Architecture

### The content pipeline (read these together)
An experiment is a single YAML config; everything else is derived and stored as files:

```
content/experiments/<id>.yaml   →  engine runs models × variants × trials
   server/experiments/engine.py →  content/runs/<id>/<runId>.json   (raw per-trial data)
   content_store.build_analysis →  content/analysis/<id>/<runId>.json (aggregated stats)
   server/.../post_generator.py →  content/posts/<slug>.md          (editable draft)
   FastAPI + React              →  live charts rendered from the analysis JSON
```
- `server/experiments/engine.py` — parallel trial execution (`ThreadPoolExecutor`, `MAX_WORKERS=8`); deterministic ordering via a pre-sized result array. Branches on `experiment["type"]`.
- `server/app/content_store.py` — the single source of truth for loading content off disk and shaping it into API JSON; `build_analysis()` does the aggregation + significance + human-baseline overlay.
- `server/experiments/stats.py` — chi-square test of independence, Cramér's V, Wilson intervals.
- `server/app/config.py` — all `content/` paths (`REPO_ROOT`-relative).

### Two experiment types (set by `type:` in the YAML)
- `fill_in_blank_decision` — model picks one option from an enum; `llm_clients.decide()` enforces the choice via OpenAI structured outputs / Anthropic forced tool use (never regex parsing).
- `open_response` — model answers free-text (`llm_clients.respond()`), then a fixed judge model (config `coder:`) codes each answer into the decision categories via `decide()`. The judge prompt is built in `engine._coder_prompt`.
- Prompt templating substitutes **all string fields** of a variant: `{metaphor}`, or `{frame}`+`{spread}`, etc. The only braces allowed in a `prompt_template` are field placeholders.

### Model capability flags — the reason `llm_clients` is parameterized
`server/experiments/model_catalog.py` is the catalog of selectable models. Each entry carries
capability flags because providers disagree on request parameters, and getting these wrong is a
400 error:
- Opus 4.7/4.8 (and Fable/Mythos) **reject `temperature`** → omitted.
- GPT-5.x are reasoning models: **reject `max_tokens`** (use `max_completion_tokens`), need a
  generous output budget (reasoning tokens count against it), and take `reasoning_effort`.
`decide()`/`respond()` build request kwargs from these flags; the engine resolves the subject
and judge configs from the catalog. Confirm exact model IDs / flags against the live provider
APIs before adding a model (model IDs reach end-of-life and 404).

### Frontend
React + Vite + Wouter + Recharts under `artifacts/client/src/` (pages wired in `App.tsx`).
- API access: **call `fetch` directly** via `lib/api.ts` (`API_BASE = ${BASE_URL}api`). Do **not**
  use the generated client packages under `lib/*` — the contract in `server/API_CONTRACT.md` is hand-followed.
- A post renders its body HTML plus `<ExperimentAnalysis>` (`components/charts/analysis-charts.tsx`)
  when it has an `experimentId`; the chart consumes the analysis `byVariant`/`overall`/`perModel` shape.

## Conventions & gotchas

- **Publishing is a flag.** A post is public only when its Markdown frontmatter has `published: true`.
  Drafts are served only in the dev workspace with `?preview=1` (never in a Replit deployment).
- **One model per run.** `run_experiment` overrides the YAML `models:` list with the single
  selected catalog model; the post compares models via a table + the featured run's `runId`.
- **`run_experiment` regenerates the draft post and will overwrite hand-edits** unless you pass
  `--keep-post` (refresh `runId` only) or `--no-post`. The generic generator is template-based;
  curated posts are hand-written — re-run with `--no-post`.
- **`export_experiment` preserves a hand-written `experiments/<id>/README.md`** and rebuilds the
  zip (excluding itself); everything else in the package is regenerated from live runs.
- **Restart the backend after editing server code** — FastAPI caches module state, so stats/engine
  changes won't take effect until the `api-server` workflow restarts.
- **chi-square prunes all-zero rows/columns** before testing; a fully-saturated table (one option
  chosen every trial) comes back `testable: false`, not a crash.
- **Client web service needs a reserved mapped port** (`.replit` `[[ports]]`); an unmapped port makes
  the workflow fail even though Vite prints "ready".
- `main.py` at the repo root is a leftover placeholder; ignore it.

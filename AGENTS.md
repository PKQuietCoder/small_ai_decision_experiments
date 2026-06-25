# AGENTS.md

Conventions for anyone — human or coding agent — working in this repository. The
goal is that every new experiment is reproducible, validated, and consistent with
the ones already here. This file is the canonical entry point; it points to the
detailed rules rather than restating them, so there is one source for each.

## What this project is

A file-based "LLM Decision Science" blog: it reruns classic human decision-bias
experiments on language models and agents and publishes the results as posts with
live statistical charts. **Python/FastAPI backend + React/Vite frontend, no
database and no authentication** — all content is plain files on disk, and
publishing is editing a file's frontmatter.

Two companion docs are authoritative and worth reading first:

- [`replit.md`](replit.md) — operating notes, stack, architecture decisions, gotchas.
- [`server/API_CONTRACT.md`](server/API_CONTRACT.md) — the exact `/api` JSON shapes;
  the frontend's source of truth.

For a deeper map, see [`docs/architecture.md`](docs/architecture.md).

## Repository map

```
content/                 all site content as files (no database)
  experiments/<id>.yaml  the experiment as code (the source of truth)
  runs/<id>/             raw per-trial output, one JSON per run
  analysis/<id>/         aggregated stats per run (drives the charts)
  posts/                 the write-ups (Markdown + frontmatter)
experiments/<id>/        downloadable, replication-ready packages (one README each)
server/                  FastAPI API (app/) + the experiment engine (experiments/)
artifacts/client/        React + Vite frontend
docs/                    architecture, experiment guide, deployment
.claude/rules/           modular conventions, imported into CLAUDE.md
```

## Conventions (the detailed rules live here)

These are imported into `CLAUDE.md` and apply every session. Read them before
non-trivial work:

- [`.claude/rules/code-style.md`](.claude/rules/code-style.md) — Python 3.12 style
  (module docstrings, `from __future__ import annotations`, type hints); pnpm/uv
  only; edit existing modules over adding new ones.
- [`.claude/rules/api-conventions.md`](.claude/rules/api-conventions.md) — `/api`
  is read-only, GET-only, no auth; keep the contract, handlers, and client types in
  sync; never weaken the draft-preview gate.
- [`.claude/rules/testing.md`](.claude/rules/testing.md) — there is **no automated
  test suite**; how to verify instead.
- [`.claude/rules/design-system.md`](.claude/rules/design-system.md) — the
  site-wide "Nature Points of View" design language and editorial **voice**: calm,
  authoritative, second-person, citation-anchored; no emoji, no marketing verbs.
  This voice is the default for all content, docs, and READMEs.

## Production practices established for this codebase

Hold these when adding code or experiments:

- **Validate experiment configs with pydantic.** Every experiment YAML is checked
  against `server/experiments/schemas.py` on load (`content_store.load_experiment_config`
  calls `validate_experiment_config`), so a malformed config fails fast with a clear
  message instead of a `KeyError` mid-run. Extend the schema when you add a field
  the engine reads; the models use `extra="allow"`, so experiment-specific variant
  fields are fine without enumerating them.
- **Read environment through settings, not `os.environ`.** Runtime config
  (API keys, `PORT`, the deployment gate) is a single `pydantic-settings` model in
  `server/app/settings.py`, populated from the environment or a local `.env` (see
  [`.env.example`](.env.example)). Provider keys are optional — the site serves
  without them; only the experiment CLIs need them, validated at the point of use.
- **No database, no auth, no hardcoded paths.** Read and write content through
  `server/app/content_store.py` and the paths in `server/app/config.py`.
- **LLM calls go through `server/experiments/llm_clients.py`** using the official
  `openai` / `anthropic` SDKs — never the Replit AI proxy, never regex-parse a
  model's choice (use structured output / forced tool use).
- **The API stays "open."** Response objects may carry extra keys; clients read what
  they need. Do not add strict pydantic response models that would strip keys the
  charts depend on.
- **Dependencies:** `pyproject.toml` + `uv.lock` are canonical (managed with `uv`);
  `requirements.txt` is a generated convenience for pip users — regenerate it after
  changing deps (see its header). JS uses `pnpm` only.

## Adding an experiment (the checklist)

Full walkthrough: [`docs/experiment-guide.md`](docs/experiment-guide.md). In short:

1. Write `content/experiments/<id>.yaml`; validate it
   (`python -c "from server.app import content_store; content_store.load_experiment_config('<id>')"`).
2. Run it one model at a time: `python -m server.run_experiment <id> --model <key> --no-post`.
   Confirm `N/N trials parsed successfully`, `parseFailures: 0`.
3. Write up `content/posts/<slug>.md`; publish by setting `published: true`.
4. Package it: `python -m server.export_experiment <id>` — and **write a
   `experiments/<id>/README.md`** (the export preserves it). Model it on
   [`experiments/decoy-effect/README.md`](experiments/decoy-effect/README.md).
5. **Add it to the index** in [`experiments/README.md`](experiments/README.md) and
   link its write-up from [`README.md`](README.md).

## Verifying changes (no test suite)

- `pnpm run typecheck` after any TypeScript change.
- After server changes: validate a config, confirm the site serves
  (`python server/serve.py`, then hit `/api/healthz`, `/api/experiments`), and
  **restart the backend** — FastAPI caches module state.
- For an experiment, smoke-test a single `decide()` / `respond()` call before a full
  run (hundreds of API calls).

## Licensing

Code is [MIT](LICENSE); experiment content (prose, data packages, per-trial data
and analysis) is [CC BY 4.0](LICENSE-DATA). Contributions are offered under the
same terms — see [`CONTRIBUTING.md`](CONTRIBUTING.md).

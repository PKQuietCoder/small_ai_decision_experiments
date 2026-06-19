# Code style

Conventions for this repo. Match the surrounding file's idioms over these defaults when they conflict.

## Python (backend, `server/`)
- Python 3.12. Start modules with `from __future__ import annotations` and a module docstring that explains *why* the module exists, not just what it does (see existing files for the tone).
- Type-hint public functions. Use the standard library plus the pinned deps in `pyproject.toml` (anthropic, openai, fastapi, numpy, scipy, pyyaml, python-frontmatter, markdown); don't add dependencies casually.
- Content is files on disk — there is no database and no auth. Read/write through `server/app/content_store.py` and the paths in `server/app/config.py`; don't hardcode `content/` paths elsewhere.
- LLM calls go through `server/experiments/llm_clients.py` using the official `openai` / `anthropic` SDKs — never the Replit AI proxy, never regex-parse a model's choice.

## TypeScript / React (frontend, `artifacts/client/`)
- pnpm only (npm/yarn are blocked). Functional components; Wouter for routing; Recharts for charts; Tailwind for styling.
- Call the API with `fetch` via `lib/api.ts`; do **not** use the generated client packages under `lib/*`.
- Keep types in `lib/api.ts` aligned with `server/API_CONTRACT.md`.

## General
- Prefer editing existing modules over adding new files/abstractions. Keep changes minimal and consistent with the established structure.

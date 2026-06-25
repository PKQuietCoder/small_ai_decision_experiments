# Documentation

Project documentation for **Borrowed Intuitions** — a file-based blog that reruns
classic human-decision experiments on language models and agents, and publishes
the results with live statistical charts.

Start with the [top-level README](../README.md) for what the project is and how
to run it. The documents here go a layer deeper.

- **[architecture.md](architecture.md)** — how the system fits together: the
  content pipeline (YAML → runs → analysis → post → package), the experiment
  types, the engine, and the model-capability catalog.
- **[experiment-guide.md](experiment-guide.md)** — how to author, validate, run,
  and package a new experiment. Read this before adding a study.
- **[deployment.md](deployment.md)** — building and serving the app.

## Other authoritative sources

These live next to the code they describe and remain the source of truth:

- **[`../server/API_CONTRACT.md`](../server/API_CONTRACT.md)** — the exact `/api`
  JSON shapes; the frontend follows it by hand.
- **[`../AGENTS.md`](../AGENTS.md)** — project conventions for contributors and
  coding agents (schemas, settings, structure, voice, verification).
- **[`../.claude/rules/`](../.claude/rules/)** — the modular conventions
  (code style, testing, API, design system) imported into `CLAUDE.md`.
- **[`../replit.md`](../replit.md)** — operating notes and architecture decisions.

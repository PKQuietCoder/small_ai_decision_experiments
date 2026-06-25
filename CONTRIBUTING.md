# Contributing

This is an independent, open research project. Critique, replication, and
extension are the point — a result you cannot reproduce is a result worth
reporting. There are three useful ways to contribute.

## 1. Check the work

Every published study ships its prompts, per-trial data, analysis, and a
self-contained package under [`experiments/`](experiments/). Rerun an entry,
recode a borderline answer, or recompute the statistics. If you get a different
result, open an issue with what you ran and what you saw. You do not need this
codebase to do it — each package is provider-agnostic and documents its own
replication steps.

## 2. Report a problem

Open an issue for a leaked cue in a prompt, a miscoded answer, a statistic read
too kindly, a broken chart, or a documentation error. Concrete and specific is
best: link the file, quote the line, and say what you expected.

## 3. Propose or extend a study

New experiments and controls are welcome. Read
[`docs/experiment-guide.md`](docs/experiment-guide.md) for how an experiment is
defined and run, and [`AGENTS.md`](AGENTS.md) for the project conventions that
keep studies consistent and reproducible.

## Working in the repo

- **Setup and commands** are in the [README](README.md) and
  [`docs/`](docs/README.md). Python is managed with `uv`, JS with `pnpm`.
- **There is no automated test suite.** Verify changes by exercising the real
  pipeline — see [`.claude/rules/testing.md`](.claude/rules/testing.md): run
  `pnpm run typecheck`, validate an experiment config, and confirm the site
  serves. After editing server code, restart the backend.
- **Voice and design.** All site content and docs follow the restrained
  editorial style in
  [`.claude/rules/design-system.md`](.claude/rules/design-system.md): calm,
  second-person, citation-anchored; no marketing language.
- **Keep the contract in sync.** If you change an API shape, update
  [`server/API_CONTRACT.md`](server/API_CONTRACT.md), the FastAPI handlers, and
  the client types together.

## Licensing of contributions

By contributing you agree that your code is offered under the repository's
[MIT License](LICENSE) and any experiment content under
[CC BY 4.0](LICENSE-DATA), matching the rest of the project.

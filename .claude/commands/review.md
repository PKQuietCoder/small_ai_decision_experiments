---
description: Review the current diff for correctness and repo-convention adherence
---
Review the current changes (run `git diff` and `git diff --cached`) for this repo.

Check for:
- correctness bugs, edge cases, and broken assumptions;
- adherence to the rules in `.claude/rules/` (code style, testing/verification, API conventions);
- if endpoints or JSON shapes changed, agreement between `server/app/main.py`,
  `server/API_CONTRACT.md`, and `artifacts/client/src/lib/api.ts`;
- LLM-client changes: per-model capability flags in `server/experiments/model_catalog.py`
  (wrong `temperature` / token-param handling is a 400).

Report findings grouped by severity (blocker / should-fix / nit). Do not modify code unless
asked — this command is review-only.

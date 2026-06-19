---
description: Investigate, fix, and verify a described issue
argument-hint: <issue description or number>
---
Fix the following issue: $ARGUMENTS

1. Locate the root cause — search the codebase; reproduce the behavior if you can.
2. Make the **minimal** change that fixes it, consistent with `.claude/rules/`.
3. Verify per `.claude/rules/testing.md` (there is no test suite): `pnpm run typecheck`,
   and exercise the relevant path — e.g. `python -m server.run_experiment <id> --model <key> --no-post`
   or load via `server.app.content_store`. Restart the backend if you changed server code.
4. Summarize the root cause, the fix, and how you verified it.

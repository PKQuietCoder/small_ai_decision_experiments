---
name: LLM structured decisions & preview gating
description: How decision experiments enforce machine-readable outputs, and how draft/preview content is gated safely in deployments.
---

# Enforced structured decisions
The experiment engine must NOT parse model decisions from free-form prose with regex/heuristics — that was rejected in review as unreliable. Decisions are read from a provider-constrained field only:
- OpenAI: `chat.completions.create(response_format={"type":"json_schema","json_schema":{"strict":True,"schema":{... "decision": enum(valid_ids) ...}}})`, then `json.loads(content)["decision"]`.
- Anthropic: forced tool use — `tools=[{name, input_schema:{decision: enum}}]` + `tool_choice={"type":"tool","name":...}`; read `block.input["decision"]` from the `tool_use` block.

**Why:** task required reliable structured/constrained output; prompt-compliance parsing is fragile and was a blocking review failure.
**How to apply:** any new experiment/provider must return a machine-readable enum field; treat out-of-enum or missing field as a failed trial, never guess.

# Secure draft/preview gating
Draft (unpublished) content is gated by `os.environ.get("REPLIT_DEPLOYMENT") != "1"` (default-DENY in deployments), NOT by `NODE_ENV`.

**Why:** the old `NODE_ENV != "production"` check defaulted to ALLOW, and the prod artifact config doesn't set `NODE_ENV`, so `?preview=1` would have exposed drafts publicly. `REPLIT_DEPLOYMENT=1` is reliably set by the platform in deployments and unset in the dev workspace.
**How to apply:** never gate sensitive/preview behavior on an env var that is unset in prod with an allow-by-default fallback; key off `REPLIT_DEPLOYMENT` with deny-by-default.

# Re-running the experiment
`python -m server.run_experiment crime-metaphor --keep-post` re-runs trials (saves fresh run JSON) but preserves a hand-edited post's narrative/`published` flag, only refreshing its `runId`. Use it when the data-generation mechanism changes but you want to keep curated prose. Charts/stats are computed from the run JSON at serve time, but hard-coded numbers in the prose must be updated by hand.

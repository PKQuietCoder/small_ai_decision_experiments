---
category: Decisions
type: Experiments
date: '2026-06-19'
slug: budget-backfire
title: 'When Budgeting Backfires: Does Forcing an Agent to Set a Budget First Make It Spend More?'
published: true
comingSoon: true
---

## Practical takeaways

| Observed (from the experiment) | Why it happens | Do differently / how to interact |
|---|---|---|
| "Set a budget first" left spend flat ($2.01 → $1.99); the human backfire never appeared. | Human nudges (and counter-nudges) don't transfer to the agent. | If you build purchasing or ops agents, don't assume a tactic that works on people carries over, **measure how the agent actually behaves** before relying on it. |
| Every condition landed on the same safe, mid-tier pick. | Regresses to the conventional, defensible option. | Its safe default avoids blunders but misses bold-but-right calls, so **ask for several genuinely different options, including one most people would reject**, with the case for each. |
| 1, 2, or 5 steps → same choice, just more reasoning. | Extra deliberation adds justification, not a new conclusion. | Don't be reassured by a long, confident write-up; **check the conclusion yourself**, since the extra steps mostly justify the answer rather than change it. |
| Even at max randomness, asking once ≈ asking 50×; variety only in *unforced* conditions. | Sampling noise won't generate real alternatives. | Re-asking the same prompt isn't a real second opinion, **reword it with a new framing or new constraints** to get genuinely different options. |
| A single-shot tool call came back empty ~1 in 3 times (17/50); strict schemas fixed all of them. | One cold tool call under sampling noise is brittle. | *(Builders)* For reliable tool use, **enforce a strict output schema and add a step or two of lead-up** instead of demanding a complex tool call in one cold shot. |

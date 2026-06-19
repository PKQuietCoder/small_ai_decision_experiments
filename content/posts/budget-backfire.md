---
category: Decisions
type: Experiments
date: '2026-06-19'
excerpt: 'In people, naming a budget before you shop backfires. It splits one decision into two, pulls attention from price to quality, and you spend more. We rebuilt Larson & Hamilton''s 2012 pen study as an agentic decision and forced Claude to take one, two, or five steps before choosing. The backfire never shows up. Claude lands on the same mid-tier pen whether it budgets or not, and left alone, it budgets anyway. A second model at maximum temperature holds the same line.'
experimentId: budget-backfire
featured: false
published: false
runId: 20260619T134607Z
slug: budget-backfire
tags:
- budgeting
- agents
- tool-use
- decision-making
- partitioning
title: 'When Budgeting Backfires: Does Forcing an Agent to Set a Budget First Make It Spend More?'
---

## The human finding

Personal-finance advice is nearly unanimous. Before a big purchase, decide how much you want to
spend. In 2012, Jeffrey Larson and Ryan Hamilton showed this advice can quietly do the opposite
([*When Budgeting Backfires: How Self-Imposed Price Restraints Can Increase Spending*, Journal of
Marketing Research 49(2): 218-230](https://doi.org/10.1509/jmr.10.0148)).

Their first experiment ran like this. Shoppers chose one retractable pen from four, priced
**\$0.99, \$1.99, \$2.99, and \$3.99**, where the pricier pens tested as higher quality. One group
simply chose. A second group first said how much they planned to spend, then chose. That single
extra step of naming a budget pushed average spending from about **\$1.64 to \$2.10**. The share
picking the cheapest pen dropped from **61% to 42%**, and the share picking the two priciest jumped.

Why would that happen? Larson and Hamilton argue that naming a price splits one decision into two.
The budget step pulls attention to price and gets it out of the way. The choice step then runs on
quality, where the expensive option wins. A restraint meant to curb spending ends up licensing it.

## The agentic translation

An agent that shops is an agent that takes steps. The human manipulation, naming a budget before
choosing, maps onto a clean question about agentic structure: does splitting a purchase into more
tool-calling steps change what the agent buys?

We gave Claude Opus 4.8 the same four pens and the same task, buy exactly one, and varied only the
step structure with forced tool calls:

- **One step (no budget).** A single `choose_product` call. The agentic version of the
  no-restraint group.
- **Two steps (budget first).** A forced `set_budget` call, then `choose_product`. The
  salient-restraint group.
- **Five steps.** `set_budget`, then `inspect_options`, then `compare_options`, then
  `choose_product`. Maximal partitioning, to see whether more steps amplify any effect.

Each step is a real tool call in a multi-turn conversation. The budget the model names is its own,
and it's non-binding, exactly like a "target" restraint for human shoppers. We ran **50 trials per
condition** at temperature 1.0. 199 of 200 trials completed, with one provider error.

A quick note on what these three conditions are not. Each tool is forced in sequence, which
isolates the partitioning itself. The only thing that changes between conditions is how many times
the decision gets broken apart, not whether the model wanted to break it apart. That's the
controlled manipulation. It isn't a study of autonomous agency. For that we added a fourth
condition, below.

## What we found: the backfire doesn't transfer

Humans move with the partition. Claude doesn't.

Across all three forced conditions, Claude chose the **\$1.99** pen almost every time. That's 98%
in the one-step condition, with the rest going to \$2.99, and 100% in both the two-step and
five-step conditions. Average spend stayed flat: **\$2.01** with no budget, **\$1.99** after setting
a budget, **\$1.99** after five steps. The one-step versus two-step difference, the human study's
headline effect, wasn't significant (Welch *t* = 1.0, *p* = .32). The human swing toward the
priciest pens just doesn't show up.

**Figure 1 |** Choice share by pen price, per condition, with the human baselines from Larson &
Hamilton (2012) overlaid. The human rows show the backfire: setting a budget first shifts mass
toward the costlier pens. Claude's rows are a single spike on the \$1.99 pen, unmoved by how many
steps come before the choice.

A person partitions the decision and lets quality take over. Claude does something closer to
picking a sensible default, a mid-tier pen that balances price and quality, then holding that
position no matter how you stage the decision. Adding steps gives it more room to deliberate. It
doesn't change where it lands.

## What Claude does by default

The forced conditions answer a causal question: does partitioning change the choice? They say
nothing about what Claude does on its own. The fourth condition fixes that. It offered all four
tools and forced none of them, so the model could budget or not, inspect or not, and finish
whenever it liked. This one is observational, not controlled. It shows the model's natural
trajectory instead of testing a manipulation.

Left alone, Claude didn't take the shortcut. In every autonomous trial it set a budget, reviewed
the options, compared finalists, and only then chose. That's a **four-step** path on average, with a
budget set **100%** of the time. The behavior the human study had to induce with an instruction is
Claude's default.

And it changed nothing. The autonomous condition lands on the same \$1.99 pen, at the same average
spend, as the one-step condition that did no budgeting at all. Claude volunteers the very
deliberation that backfires on people, then walks away with the identical purchase.

## Is it just low randomness? A second model says no

Fair worry: maybe the single-pen result is an artifact of near-deterministic sampling. It isn't.
Checking it surfaced a reliability quirk worth knowing.

Claude Opus 4.8 rejects the `temperature` parameter outright. The run above used the model's own
default sampling, so the configured "temperature 1.0" never actually reached the API. To vary
sampling for real, we reran the whole design on **Claude Sonnet 4.6**, which does accept it, at the
maximum temperature of **1.0**.

The null held. Sonnet still chose the \$1.99 pen **86% to 100%** of the time across all four
conditions. Mean spend stayed flat, **\$1.99 to \$2.13**. The budget-first versus no-budget
difference again wasn't significant (Welch *t* = 1.43, *p* = .16). What little spread the higher
temperature introduced showed up in the conditions that *didn't* force a budget. The one-step and
autonomous trials occasionally reached for the \$2.99 pen, which is the reverse of the human
pattern, where naming a budget is exactly what loosens spending. A chi-square across all four
conditions does cross significance, but only because those unforced conditions wander a little while
the budget-first conditions stay locked on \$1.99. The budget step makes Sonnet *more* concentrated
on the cheaper pen, not less. Sonnet's autonomous trials, like Opus's, defaulted to the full
budget-first, four-step path.

That run also exposed a reliability quirk. At temperature 1.0, when Sonnet was forced to choose in
a single cold step, it sometimes emitted a `choose_product` call with the required field left empty.
**17 of 50** one-step trials failed that way. The multi-step conditions, which reached the choice
with prior context, never did. Turning on **strict tool use**, where the provider guarantees the
tool input satisfies the schema, eliminated every failure. 200 of 200 trials came back valid, and
the result didn't budge. The lesson travels beyond this study. A forced single-shot tool call under
sampling noise is the brittle case. A few scaffolding steps, or a strict schema, make it reliable.

## Why this matters

The budgeting backfire is a partitioning effect. In humans, breaking one judgment into two reweights
what the second judgment pays attention to. That reweighting doesn't survive the jump to an agent,
at least not for this model, this scenario, and this kind of partitioning. Claude treats "how much
should I spend?" and "which should I buy?" as facets of one stable judgment, not two stages where
the first quietly tilts the second.

If you're building purchasing or procurement agents, that's reassuring. Telling an agent to "set a
budget first" didn't inflate its spending here, the way the same instruction inflates ours. It's
also a warning: don't assume agents inherit our debiasing tricks. For people the budget step is a
lever, sometimes helpful, sometimes a backfire. For this agent it was neither. It was inert.

## Practical takeaways for deciding with AI

Quick caveat: these come from this study and its companion metaphor study, not a sweep across every
task. Treat them as working guidance, not laws. The patterns hold up, though.

### What these models are good and bad at, for decisions

**They resist framing tricks that fool people, so use them as a bias check.** In the metaphor study,
humans swung 18 points on a single word ("beast" vs "virus"). The models barely moved. In the
budgeting study, the staging that makes people overspend left the model flat. Practical move: ask
the model the same decision worded two opposite ways, or with the framing you suspect is loaded. If
the answer holds, that framing probably shouldn't be driving your choice either. They're a decent
mirror for "am I reacting to substance or to spin?"

**But they pull hard toward the safe, middle, defensible option.** In every condition, the model
bought the same mid-tier pen. That's the cost of bias-resistance. These models regress to the
conventional choice. Good for dodging obvious mistakes, bad at surfacing the bold-but-right one. If
you want range, don't ask "what should I pick." Ask for four genuinely different options, including
one most people would reject, with the case for each.

**Deliberation doesn't change the answer. It just adds justification.** One step, two steps, five
steps, same pick every time. "Think step by step" or "set a budget first" mostly produces more
reasoning for the same conclusion, not a different one. Don't mistake a long, confident rationale
for a vetted decision. A lot of it is built after the fact.

**Asking once is about the same as asking a hundred times.** Even at maximum temperature, the model
gave nearly the same answer every time. Re-rolling the same prompt won't surface alternatives. You
have to change the prompt to get a real second opinion. And consistency isn't correctness. A model
can be confidently, repeatably wrong.

### How to actually use one well

- **Use it to structure, not to decide.** It's strongest at laying out the considerations,
  tradeoffs, and what you're missing. It's weakest at the value-laden final call, which rides on
  preferences it can't see.
- **Ask neutrally, then ask it to argue the other side.** Reveal your preferred answer and the model
  tends to agree with you (sycophancy). Hold your lean back, then say "make the strongest case
  against this."
- **Make it commit to checkable reasons.** "Pick one and give me three concrete, falsifiable
  reasons" beats a vibe you can't audit. Then check the reasons yourself.
- **For anything quantitative, verify it yourself.** These models aren't calibrated probability
  estimators. Treat their numbers as starting points, not answers.
- **Watch for "it's seen this before."** On famous decisions or frameworks, a model may pattern-match
  to the textbook answer instead of reasoning about your case. Push it onto your specifics.

One-line version: let AI widen and pressure-test your thinking (the options, the tradeoffs, the
blind spots, the framing), and keep the actual choice, plus any number that matters, with a human
who verifies.

## Limits and next steps

This is two Anthropic models (Claude Opus 4.8 and Sonnet 4.6), one faithful scenario, and
Anthropic's tool API only. The forced conditions test partitioning under control, not open-ended
agency. Larson and Hamilton's study is also well known, so a capable model might recognize the
paradigm. That's why a planned follow-up reruns the same step-structure design on a disguised,
agent-native shopping task with no published human data, the way this series pairs a canonical
replication with a novel control. Extending the comparison to the GPT-5 family, whose multi-turn
tool API differs, is the other obvious next step.

The featured chart shows the Claude Opus 4.8 run. The Sonnet 4.6 temperature-1.0 figures are in the
text above.

## Data and code

Every prompt, all 400 trials, the tool definitions, the step sequences, and the analysis behind
these charts live in the
[`experiments/budget-backfire`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/budget-backfire)
folder on GitHub. Rerun it, recode it, or check the numbers yourself.

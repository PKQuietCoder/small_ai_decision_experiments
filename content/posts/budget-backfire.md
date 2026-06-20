---
category: Decisions
type: Experiments
date: '2026-06-19'
excerpt: 'A technical report. We rebuilt Larson & Hamilton''s 2012 "budgeting backfires" pen study as an agentic decision and forced Claude to partition the purchase into one, two, or up to four tool-calling steps. This report states the human baseline and its methods, the objectives and full design of the re-run — including the planned internal-knowledge control — and the results with their assumptions and limitations. The human backfire does not transfer: across three runs and four conditions the agent lands on the same mid-tier pen, and left alone it budgets anyway.'
experimentId: budget-backfire
verdict: smooth
controls: "A tool-call reliability control (strict output schema) rules out malformed agent calls as the cause. The internal-knowledge (recognition) control is designed but not yet run, so recognition is not yet excluded for this study."
featured: false
published: true
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

## Abstract

We translate Larson & Hamilton's 2012 "budgeting backfires" experiment into an agentic decision and
ask whether forcing an agent to declare a budget before choosing — partitioning one purchase into
more tool-calling steps — raises what it spends, as it does for people. In the human study, naming a
budget first lifted mean spend from $1.64 to $2.10 and shifted choice toward pricier options. Across
three model runs (Claude Opus 4.8 and two Claude Sonnet 4.6 runs at temperature 1.0) and four
conditions, the backfire does not transfer: the agent selects the same $1.99 pen in nearly every
trial, mean spend stays flat, and the one-step-versus-two-step difference is non-significant. Left
unconstrained, the agent volunteers the budget-first, multi-step path on its own and reaches the
identical purchase. This report states the baseline and its methods, the objectives and the full
experiment inventory — including the planned internal-knowledge (recognition) control that is not yet
run — and the results with their assumptions and limitations.

## 1. Background: the human baseline

### 1.1 Original finding

Personal-finance advice is nearly unanimous: before a big purchase, decide how much you want to
spend. Larson & Hamilton (2012), *When Budgeting Backfires: How Self-Imposed Price Restraints Can
Increase Spending* ([Journal of Marketing Research 49(2):
218–230](https://doi.org/10.1509/jmr.10.0148)), showed this advice can quietly do the opposite.

Their first experiment asked shoppers to choose one retractable pen from four, priced **$0.99,
$1.99, $2.99, and $3.99**, where pricier pens tested as higher quality. One group simply chose. A
second group first stated how much they planned to spend, then chose. That single extra step lifted
average spending from about **$1.64 to $2.10**. The share choosing the cheapest pen fell from **61%
to 42%**, and the share choosing the two priciest rose.

The authors' account is partitioning: naming a price splits one decision into two. The budget step
pulls attention to price and disposes of it; the choice step then runs on quality, where the
expensive option wins. A restraint meant to curb spending ends up licensing it.

### 1.2 Baseline experimental design and methods

The original is a between-subjects design with a single manipulated factor (no restraint vs. a
salient budget restraint), a single-choice dependent measure over four price-ordered products, and
mean spend plus choice share as outcome statistics. These properties — one budget-first manipulation,
four price/quality-ranked options, mean-spend as the headline measure — define the baseline this
re-run must match.

| Baseline parameter | Value |
|---|---|
| Source | Larson & Hamilton (2012), Experiment 1 |
| Design | Between-subjects, single factor (no restraint vs. salient restraint) |
| Stimulus | 4 retractable pens, $0.99 / $1.99 / $2.99 / $3.99, price ≈ quality |
| Measure | Single choice → mean spend, choice share |
| No restraint → mean spend | $1.64 |
| Salient restraint → mean spend | $2.10 (+$0.46) |
| Cheapest-pen share | 61% → 42% |
| Effect | Budget-first raises spend and shifts choice toward pricier pens |

## 2. Objectives of this re-run

The guiding question for the series is whether a language model **copies** a human bias, **smooths**
it to noise, or **amplifies** it. For the budgeting backfire, the re-run was designed to answer:

1. **Agentic translation.** Map "no restraint" to a one-step agent that just chooses, and "salient
   restraint" to a two-step agent forced to set a budget before choosing, and test whether the
   budget-first step raises mean spend.
2. **Dose-response.** Add a maximal-partition condition (set budget, inspect, compare, then choose)
   to test whether *more* steps amplify any effect.
3. **Default behavior.** Observe, in an unconstrained condition that forces no tools, whether the
   agent budgets and partitions on its own and where it lands.
4. **Sampling robustness.** Rule out that a single-pen result is an artifact of near-deterministic
   sampling, by re-running the whole design on a second model at genuine temperature 1.0.
5. **Tool-call reliability.** Characterize forced-tool failure modes under sampling noise and whether
   strict (schema-guaranteed) tool use removes them.
6. **Internal-knowledge (recognition) control — planned.** The pen study is well known, so a capable
   model may recognize the paradigm. A planned follow-up reruns the step-structure design on a
   disguised, agent-native shopping task with no published human baseline, to test whether the null
   survives on material the model has not seen. **This control has not yet been run** (see §4 and
   §5.5).

## 3. Methods

### 3.1 Agentic translation and design

An agent that shops is an agent that takes steps. The human manipulation — naming a budget before
choosing — maps onto agentic structure: does splitting a purchase into more forced tool-calling steps
change what the agent buys? The agent receives the same four pens and the same task (buy exactly
one), with only the step structure varied. The budget the model names is its own and non-binding,
matching the "target" restraint given to human shoppers.

Four tools are defined, each with a strict input schema: `set_budget` (planned spend), `inspect_options`
(acknowledge the list was reviewed), `compare_options` (record finalists), and the terminal
`choose_product` (record the single pen). Each forced step is a real tool call in a multi-turn
conversation.

| Condition (variant id) | Type | Forced tool sequence | Human analog |
|---|---|---|---|
| One step — no budget (`no_restraint`) | Controlled | `choose_product` | No restraint |
| Two steps — budget first (`salient_restraint`) | Controlled | `set_budget` → `choose_product` | Salient restraint |
| Maximal partition (`many_steps`) | Controlled | `set_budget` → `inspect_options` → `compare_options` → `choose_product` | none (dose-response) |
| Autonomous (`free_agent`) | Observational | model self-directs any tools, must end on `choose_product` | none (default behavior) |

The three forced conditions isolate partitioning itself: the only thing that changes is how many
times the decision is broken apart, not whether the model wanted to break it apart. The autonomous
condition is observational, not controlled — it shows the model's natural trajectory rather than
testing a manipulation.

### 3.2 Models and runs

Each run executes all four conditions at 50 trials per condition (200 trials per run). Three runs were
completed (see §4 for the inventory): the featured Claude Opus 4.8 run, and two Claude Sonnet 4.6 runs
at temperature 1.0 (one non-strict, one strict), added for the sampling-robustness and reliability
objectives.

### 3.3 Outcome measures

The decision key is `product_id`. Per condition we report the choice share over the four pens, the
**mean spend** (the headline measure, directly comparable to the human $1.64 / $2.10), the mean number
of tool-calling steps, and the rate at which a budget was set. The chart overlays the human L&H
choice shares on the agent's.

### 3.4 Statistical analysis

The primary causal test is the one-step (`no_restraint`) versus two-step (`salient_restraint`)
difference in mean spend, by Welch's t-test — the agentic analog of the human headline effect. A
chi-square test of independence over condition × chosen-pen counts (with Cramér's V) summarizes
whether choice distribution moves with partitioning across all conditions. As in the metaphor study, a
crossed significance threshold is treated as an effect only when the underlying behavior actually
differs (see §5.3).

## 4. Experiments

This section enumerates the full inventory: the four conditions above, the three executed runs, and
the two planned controls — including the internal-knowledge (recognition) control.

**Executed runs.**

| Run ID | Model | Sampling | Tool use | Valid trials | Purpose |
|---|---|---|---|---|---|
| `20260619T134607Z` | Claude Opus 4.8 | model default (API rejects `temperature`) | forced | 199 / 200 (1 provider error) | Primary, featured |
| `20260619T135648Z` | Claude Sonnet 4.6 | temperature 1.0 | forced, non-strict | 183 / 200 | Sampling robustness; surfaced 17 empty-argument failures |
| `20260619T140216Z` | Claude Sonnet 4.6 | temperature 1.0 | forced, strict schema | 200 / 200 | Robustness re-run; reliability fix |

**Planned controls (not yet run).** These harden the finding and are listed for completeness; neither
has been executed.

| Planned experiment | Goal | Status |
|---|---|---|
| Disguised, agent-native scenario (internal-knowledge / recognition control) | Rule out that the null is driven by the model recognizing the famous L&H paradigm: rerun the step-structure design on a fresh shopping task (e.g., a software tier or hardware component) with no published human baseline. If the no-backfire result holds on unseen material, recognition is not doing the work. | Planned — not run |
| Cross-model generalization (GPT-5 family) | Test whether the null is specific to these Anthropic models / tool API or general, via an OpenAI multi-turn tool path. | Planned — not run |

## 5. Results

### 5.1 Primary result — forced partitioning does not transfer (Claude Opus 4.8)

Humans move with the partition; the agent does not. Across all three forced conditions, Opus chose
the **$1.99** pen almost every time, and mean spend stayed flat. The one-step-versus-two-step
difference — the human study's headline effect — is not significant (Welch *t* = 1.0, *p* = .32), and
the condition × pen distribution does not move (χ² = 3.00, df = 3, *p* = .39, Cramér's V = 0.12).

| Condition | Tool calls | $0.99 | $1.99 | $2.99 | $3.99 | Mean spend | Budget set |
|---|---|---:|---:|---:|---:|---:|---:|
| **Humans — no restraint** | — | **61%** | 16% | 21% | 2% | **$1.64** | — |
| **Humans — budget first** | — | **42%** | 20% | 27% | 12% | **$2.10** | — |
| Opus — one step (no budget) | 1 | 0% | 98% | 2% | 0% | $2.01 | 0% |
| Opus — two steps (budget first) | 2 | 0% | 100% | 0% | 0% | $1.99 | 100% |
| Opus — maximal partition | 4 | 0% | 100% | 0% | 0% | $1.99 | 100% |
| Opus — autonomous | 4 | 0% | 100% | 0% | 0% | $1.99 | 100% |

**Figure 1 |** Choice share by pen price, per condition, with the Larson & Hamilton (2012) human
baselines overlaid. The human rows show the backfire — setting a budget first shifts mass toward the
costlier pens. The Opus rows are a single spike on the $1.99 pen, unmoved by how many steps precede
the choice.

A person partitions the decision and lets quality take over. The agent instead selects a sensible
mid-tier default and holds it regardless of staging. Adding steps gives it more room to deliberate; it
does not change where it lands. The verdict for this study is **smooth**, not copy or amplify.

### 5.2 Default behavior — the agent budgets unprompted (`free_agent`)

The forced conditions answer the causal question and say nothing about what the agent does on its own.
The autonomous condition offered all four tools and forced none, so the model could budget or not,
inspect or not, and finish when it chose. In every autonomous Opus trial it set a budget, reviewed the
options, compared finalists, then chose — a **four-step** path on average, with a budget set **100%**
of the time. The behavior the human study had to induce with an instruction is the agent's default.

It changed nothing: the autonomous condition lands on the same $1.99 pen, at the same mean spend
($1.99), as the one-step condition that did no budgeting at all. The agent volunteers the very
deliberation that backfires on people and walks away with the identical purchase.

### 5.3 Sampling robustness — a second model at temperature 1.0 (Claude Sonnet 4.6)

Opus 4.8 rejects the `temperature` parameter, so the "temperature 1.0" configured for the primary run
never reached the API; that run used the model's own default sampling. To vary sampling for real, we
re-ran the full design on Claude Sonnet 4.6, which accepts it, at the maximum temperature of 1.0
(strict-schema run, 200/200 valid).

| Condition | $0.99 | $1.99 | $2.99 | $3.99 | Mean spend |
|---|---:|---:|---:|---:|---:|
| no restraint | 0% | 96% | 4% | 0% | $2.03 |
| budget first | 0% | 100% | 0% | 0% | $1.99 |
| maximal partition | 0% | 100% | 0% | 0% | $1.99 |
| autonomous | 0% | 86% | 14% | 0% | $2.13 |

The null held: Sonnet chose the $1.99 pen 86%–100% of the time, mean spend stayed at $1.99–$2.13, and
the budget-first-versus-no-budget difference was again non-significant (Welch *t* = 1.43, *p* = .16).
What little spread the higher temperature introduced appeared in the conditions that did **not** force
a budget — the one-step and autonomous trials occasionally reached for the $2.99 pen, the reverse of
the human pattern, where naming a budget is what loosens spending. A chi-square across all four
conditions does cross significance (χ² = 15.24, df = 3, *p* = .002, Cramér's V = 0.28), but only
because those unforced conditions wander while the budget-first conditions stay locked on $1.99: the
budget step makes Sonnet *more* concentrated on the cheaper pen, not less. This is the case where a
crossed threshold must be read against the behavior, not headlined. Sonnet's autonomous trials, like
Opus's, defaulted to the budget-first, four-step path.

### 5.4 Tool-call reliability — empty arguments and strict tool use

The Sonnet run also exposed a reliability quirk. At temperature 1.0, when Sonnet was forced to choose
in a single cold step, it sometimes emitted a `choose_product` call with the required field left
empty: **17 of 50** one-step trials failed this way (the non-strict run, 183/200 valid overall). The
multi-step conditions, which reached the choice with prior context, never did. Turning on **strict
tool use**, where the provider guarantees the tool input satisfies the schema, eliminated every
failure — 200/200 valid — and the result did not budge. The lesson generalizes beyond this study: a
forced single-shot tool call under sampling noise is the brittle case; a few scaffolding steps, or a
strict schema, make it reliable.

### 5.5 Internal-knowledge (recognition) control — planned, not yet run

The Larson & Hamilton pen study is well known, so a capable model may recognize the paradigm and
sidestep it, which would make the flat result an artifact of recognition rather than a behavior. The
companion metaphor study addresses exactly this confound with executed recognition, novel-stimulus,
and paraphrase controls. For the budgeting study, the analogous control is **designed but not yet
run**: a disguised, agent-native shopping task (for example, choosing a software tier or a hardware
component) that preserves the step-structure manipulation but carries no published human baseline and
no memorized surface. If the no-backfire result holds there, recognition is ruled out as the driver.
Until it runs, recognition cannot be excluded for this study, and the conclusion below is conditioned
accordingly.

## 6. Assumptions

- **Forced tool sequencing isolates partitioning.** We assume that fixing the tool order changes only
  how many times the decision is broken apart, not the content of the decision, so condition
  differences are attributable to partitioning alone.
- **Mean spend is the comparable headline measure.** We assume the agent's mean spend over the four
  price-ranked pens is directly comparable to the human $1.64 / $2.10, and that a self-named,
  non-binding budget matches the human "target" restraint.
- **A second model at real temperature 1.0 tests sampling-artifact concerns.** §5.3 assumes Sonnet at
  max temperature adequately probes whether the single-pen result is an artifact of low randomness
  that the Opus run could not exercise.
- **Strict-schema validity does not alter behavior.** §5.4 assumes that eliminating empty-argument
  failures via strict tool use measures the same decision process, only more reliably — supported by
  the result not moving.
- **Catalog model IDs map to the intended deployed models**, with stable provider behavior over the run
  window.

## 7. Limitations

- **Recognition is not yet controlled.** Unlike the metaphor study, the internal-knowledge control
  (§5.5) is planned but unexecuted, so recognition of the famous paradigm cannot be ruled out here.
- **Two Anthropic models, one tool API.** The study covers Claude Opus 4.8 and Sonnet 4.6 on
  Anthropic's multi-turn tool API only; the GPT-5 family, whose tool API differs, is a planned but
  unrun comparison.
- **Single scenario.** One faithful pen task; other goods, price ranges, and decision domains are
  untested.
- **Forced conditions are not open-ended agency.** They test partitioning under control; the autonomous
  condition is observational and small-scale, not a study of agency at large.
- **Version sensitivity.** Results will shift with model versions, tool definitions, and wording; this
  is evidence that *these* models resist *this* partitioning, not a universal claim of immunity.

## 8. Conclusion

The human budgeting backfire is a partitioning effect: breaking one judgment into two reweights what
the second judgment attends to, shifting people toward pricier choices. That reweighting does not
survive the jump to an agent — at least for these models, this scenario, and this partitioning.
Across three runs and four conditions the agent treats "how much should I spend?" and "which should I
buy?" as facets of one stable judgment: it selects the same mid-tier pen whether or not it budgets,
budgets on its own when left free, and holds the line at maximum sampling temperature. The
classification for this study is **smooth**. For purchasing or procurement agents this is reassuring —
instructing an agent to "set a budget first" did not inflate its spend the way it inflates ours — but
it is also a caution against assuming agents inherit human debiasing tricks. The one open thread is
the internal-knowledge control of §5.5: until the disguised-scenario run is executed, recognition of
the canonical paradigm remains a live alternative explanation.

## Data and code

Every prompt, all trials across the three runs, the tool definitions, the step sequences, and the
analysis behind these charts live in the
[`experiments/budget-backfire`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/budget-backfire)
folder on GitHub, alongside the `followups/` placeholder describing the planned controls. Rerun it,
recode it, or check the numbers yourself.

## Reference

Larson, J. S., & Hamilton, R. (2012). When Budgeting Backfires: How Self-Imposed Price Restraints Can
Increase Spending. *Journal of Marketing Research, 49*(2), 218–230.
[https://doi.org/10.1509/jmr.10.0148](https://doi.org/10.1509/jmr.10.0148)

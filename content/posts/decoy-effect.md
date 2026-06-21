---
category: Decisions
type: Experiments
date: '2026-06-21'
excerpt: 'A classic human bias, the decoy effect, transfers to AI shopping agents whenever the options are co-presented in the prompt: a third, clearly worse choice that nobody ever picks pulls the decision toward the option that decoy flatters (0% to 60% in our laptop market), for Opus, Sonnet, and Haiku alike, and on a second market the models cannot have memorised. The number of deliberation steps makes no difference. Two ways of giving the agent more control are not reliable fixes: autonomy is erratic, and making the agent retrieve each spec itself cleanly removes the bias for Opus but leaves Sonnet and Haiku swayed, even though per-call logs prove they inspected the decoy every time. The one lever that works for every model is upstream: do not put the decoy on the menu.'
experimentId: decoy-effect
verdict: copy
controls: "Three controls. A recognition control reruns the design in an un-memorised market (cloud-storage plans) and the effect holds, ruling out recall of a textbook example. A presentation control replaces the in-prompt menu with retrieval tools the agent must call; this removes the effect for Opus but not for Sonnet or Haiku. Per-call tool logging confirms the retrieval agents inspected the decoy in 100% of trials."
featured: false
published: true
runId: 20260621T023923Z
slug: decoy-effect
tags:
- decoy-effect
- attraction-effect
- agents
- tool-use
- choice
- decision-making
title: 'The Decoy Effect: Does a Worse Option Sway an Agent''s Choice?'
---

## Abstract

The decoy effect is one of the most reliable findings in the study of human choice: add a third,
obviously worse option to a pair, and people shift toward whichever of the original two the decoy
makes look good, even though almost nobody picks the decoy itself. We rebuilt it as an agentic
purchase. An AI agent compares two laptops with a real price-versus-performance tradeoff and buys
one; in the manipulated conditions a third laptop is added that is clearly worse than one of the
two targets. The featured study is a clean 7-condition run on Claude Opus 4.8 (210 trials), extended
with replications on Sonnet 4.6 and Haiku 4.5 and a second, un-memorised market. The result is
layered. First, when the agent is handed the full menu in its prompt, the decoy works: it lifts
the flattered laptop's share from 0% to 60% against the model's own no-decoy baseline (chi-square
22.9, *p* < .001), and this co-presentation effect holds for all three Claude models on laptops and
replicates on a second, un-memorised market. Second, the number of deliberation steps makes no difference; a one-shot decision and a
forced multi-step ritual are the same. Third, two ways of giving the agent more control are not
reliable fixes: autonomy is erratic (the same Opus arm lands anywhere from 0% to 47% across runs),
and genuine retrieval, where the agent must call tools to discover each option's specifications,
cleanly removes the effect for Opus but leaves Sonnet and Haiku fully swayed. Per-call tool logging
shows this is not the weaker models ignoring the decoy: in all 180 retrieval trials the agent
inspected the decoy's specs before choosing. The one lever that works for every model is upstream of
the agent entirely: do not put the decoy on the menu. This report establishes the human baseline for
readers new to the effect, sets out the methods and the full experiment inventory in tables, and
reports the results with their assumptions and limits.

## 1. Background: the human baseline

If you have not met the decoy effect before, the cleanest way in is the study that named it.

### 1.1 The original finding

In 1982 the marketing researchers Joel Huber, John Payne, and Christopher Puto published *Adding
asymmetrically dominated alternatives* (*Journal of Consumer Research* 9(1): 90–98). Their setup is
simple. Offer people a choice between two products that involve a genuine tradeoff, for example a
cheaper-but-weaker option A and a pricier-but-stronger option B, and they split fairly evenly. Now
add a third option that is **asymmetrically dominated**: it is clearly worse than B on every
attribute that matters, but not clearly worse than A. Almost no one chooses this third option. Yet
its mere presence shifts the remaining choice toward B. The decoy never wins, and it still changes
who does.

Itamar Simonson (1989) connected this to the related compromise effect and drew the lesson that
matters here: a choice is shaped not only by an option's standalone merits but by how it sits
relative to the rest of the set. A purely rational chooser would ignore an option nobody picks.
People do not. The effect has since been reproduced for hundreds of products, which is why it is a
standard tool in pricing and menu design: a deliberately unattractive "decoy" tier can steer buyers
toward the tier a seller wants to move.

### 1.2 The baseline, in one table

The original is a between-subjects design with one manipulated factor (which decoy, if any, is on
the menu) and one outcome: the target's share of choices. Its signature is *directional*. A decoy
that flatters one target raises that target's share specifically, while the decoy itself is barely
chosen. Those properties are the baseline this re-run has to match.

| Baseline parameter | Value |
|---|---|
| Source | Huber, Payne & Puto (1982); Simonson (1989) |
| Design | Between-subjects, single factor (no decoy / decoy-for-A / decoy-for-B) |
| Stimulus | Two options with a real tradeoff, plus an asymmetrically dominated decoy |
| Outcome measure | A single choice, summarised as the target's choice share |
| No-decoy result | Roughly a 50% / 50% split |
| Decoy added | Shifts about 10 to 25 points toward the flattered target; decoy chosen about 0 to 5% |

## 2. Objectives of this re-run

Every study in this series asks one question of a human bias: does the model **copy** it, **smooth**
it away, or **amplify** it? For the decoy effect we ask that, and then one more question that only
an agent can answer.

| # | Objective | What it tests |
|---|---|---|
| 1 | Agentic translation | Does adding an asymmetrically dominated decoy shift the agent's purchase toward the flattered target, against its own no-decoy baseline? |
| 2 | Directionality | A decoy-for-A and a decoy-for-B condition: a real attraction effect moves choice toward whichever target the decoy flatters, not merely "a third option perturbed things". |
| 3 | Process sensitivity | Does the effect depend on how the decision is staged: one shot, a forced multi-step ritual, or full autonomy? |
| 4 | Presentation sensitivity | Does it survive when the agent must **retrieve** each option's facts through tools, rather than reading a menu handed to it in the prompt? |
| 5 | Recognition control | Rerun the whole design in an un-memorised market (cloud-storage plans) to separate genuine susceptibility from recall of a textbook setup. |

Objectives 3 and 4 are the new contribution and the reason this is worth running on an agent rather
than a survey respondent. They take apart two things that look similar but are not: *how much the
agent deliberates*, and *how the options reach it*.

## 3. Methods

### 3.1 The agentic translation

The agent is told it will buy exactly one laptop for general office work. Each laptop has two
attributes that trade off against each other: price (lower is better) and a performance score
(higher is better). It buys one using shopping tools. The only thing that changes between the core
conditions is which third option, if any, is on the menu.

| Condition (variant id) | Choice set | Decoy dominated by | Prediction |
|---|---|---|---|
| No decoy (`no_decoy`) | A, B | – | baseline preference |
| Decoy for B (`decoy_b`) | A, B, C | B (C is pricier *and* weaker than B) | B's share rises |
| Decoy for A (`decoy_a`) | A, B, C | A (C is pricier *and* weaker than A) | A's share rises |

The laptops: A is $900 at performance 70; B is $1,300 at performance 90. The B-decoy is $1,400 at
85 (worse than B on both attributes, not dominated by A). The A-decoy is $1,000 at 60 (worse than A
on both). B is the only target with room to move, because, as the results show, the model's default
taste already favours the better value.

### 3.2 The two variables we separate: deliberation and presentation

On top of the decoy-for-B set, we vary two things independently. This is the core of the design.

**Deliberation (how much process).** Three arms hold the menu fixed and change only the staging:

| Arm (variant id) | Staging | Menu location |
|---|---|---|
| Single shot (`direct_decoy_b`) | One tool call, decide immediately | In the prompt |
| Forced ritual (`decoy_b`) | Pinned through inspect, then compare, then choose | In the prompt |
| Autonomous (`free_agent`) | Agent calls tools freely until it decides | In the prompt |

**Presentation (how the options arrive).** Two arms remove the menu from the prompt entirely. The
agent is told the catalogue is available only through tools and must call `list_products` and
`get_specs` to discover each laptop's price and performance for itself, then `choose_product`:

| Arm (variant id) | Menu location | Decoy present? |
|---|---|---|
| Real agent, no decoy (`real_no_decoy`) | Retrieved via tools | No (A, B only) |
| Real agent, with decoy (`real_decoy_b`) | Retrieved via tools | Yes (decoy for B) |

The distinction is the whole point. In the first five arms the agent reads a ready-made comparison.
In the last two it builds its own picture of the choice set one fact at a time. The options and the
underlying numbers are identical; only the route the information takes is different. To keep the
comparison clean, the deliberation arms are all offered the same classic toolset, and the
retrieval arms are offered only the retrieval tools, so no arm sees a tool it should not.

### 3.3 Models and runs

The featured run is Claude Opus 4.8, 30 trials per condition, 7 conditions, 210 trials, at the
model's default sampling. The purchase is read from a schema-constrained `product_id` field, never
parsed from free text. To test how far the findings generalise we reran the same 7-condition design
on Sonnet 4.6 and Haiku 4.5, and reran it again on a second, un-memorised market (cloud-storage
plans). In the retrieval arms we also log every tool call with its arguments, so we can confirm
directly which options, including the decoy, the agent actually inspected. Most cells returned clean
data; the exception is Haiku's single-shot arm, which frequently emitted an empty tool call and is
reported with that caveat (Section 7).

### 3.4 Outcome and statistics

For each condition we report every option's share of the 30 choices. The headline is the flattered
target's share **measured against the model's own no-decoy baseline**, because, unlike the human
50/50, the model has a strong intrinsic preference. We summarise whether the choice distribution
moves with a chi-square test of independence and Cramer's V (a 0-to-1 measure of how strongly the
condition and the choice are associated). All-zero option columns are dropped before testing.

## 4. The experiments

| Experiment ID | Goal | Method | Headline result |
|---|---|---|---|
| `decoy-effect` (featured) | Replicate the effect, then separate deliberation from presentation | 7 conditions on Opus 4.8, laptops, 210 trials | Decoy works under co-presentation (0%→60% B); identical across staging; gone under retrieval |
| Claude-family replication | Does the retrieval escape generalise? | Same 7 conditions on Sonnet 4.6 and Haiku 4.5 | Co-presentation effect holds; retrieval escape is Opus-only (Sonnet/Haiku stay swayed) |
| `decoy-effect-novel` | Recognition control + retrieval on an un-memorised market | Same design, cloud-storage plans, three Claude models | Co-presentation effect replicates; Opus again escapes under retrieval, Haiku does not |
| Cross-model panel | Is the copy a general LLM property? | Decoy-for-B on six models, both providers | Copied across the Claude family, largely resisted by GPT-5 |

## 5. Results

### 5.1 Under co-presentation, the decoy moves the agent

When the menu is in the prompt, the bias transfers. The model's default taste is not the human
50/50; it strongly prefers the better-value Laptop A, choosing it in every no-decoy trial. So the
effect is read as movement away from that baseline. Adding a decoy dominated by B lifts B's share
from 0% to 60%. The distribution moves sharply (chi-square 22.9, df 1, *p* < .001, Cramer's V 0.62
for the no-decoy versus decoy-for-B contrast; the full 7-condition table gives *p* < .0001, V 0.67).

| Condition | Laptop A (cheaper, weaker) | Laptop B (pricier, stronger) | Laptop C (decoy) |
|---|---:|---:|---:|
| Humans, no decoy | 50% | 50% | – |
| Humans, decoy for B | 35% | 63% | 2% |
| Humans, decoy for A | 63% | 35% | 2% |
| Opus, no decoy | 100% | 0% | 0% |
| Opus, decoy for B | 40% | **60%** | 0% |
| Opus, decoy for A | 100% | 0% | 0% |

**Figure 1 |** Choice share by condition, with the human attraction-effect baselines for reference.
The decoy-for-B condition pulls the agent off its otherwise unanimous preference for Laptop A. The
decoy-for-A condition cannot show the effect, because the agent already chooses A every time, a
ceiling that leaves no room to rise.

The direction rules out the trivial reading that "any third option unsettles the choice." The
decoy-for-A condition also adds a third option, and the choice does not move; it stays at the A
ceiling. The choice shifts only toward the option the decoy specifically flatters, which is the
signature of the genuine attraction effect.

### 5.2 Deliberation count does not matter; autonomy is erratic

The obvious worry about an agent result is that it depends on some quirk of the scaffolding. Holding
the decoy-for-B menu fixed and changing only the process tells two stories. Going from a single
immediate tool call to a forced inspect-compare-choose ritual changes nothing: the bias is the same
size. Handing the agent full autonomy is a different matter, but not a dependable one.

| Arm | Staging | Laptop B share |
|---|---|---:|
| Single shot | one tool call | 50% |
| Forced ritual | three pinned steps | 60% |
| Autonomous | self-directed | 3% (this run) |

**Figure 2 |** Single-shot and forced-ritual sit together (50% versus 60%, not significantly
different); the multi-step "agentic" ritual is doing no work, so the inspect and compare steps are
ceremony, not cognition. The autonomous arm is the unstable one.

The autonomous condition is where caution is needed. Across three independent Opus runs of this exact
arm it has landed at 0%, 3%, and 47% B: sometimes the effect vanishes when the agent self-directs,
sometimes it survives almost intact. We cannot say autonomy fixes the bias or that it does not; the
honest summary is that letting the agent run itself makes the outcome *erratic* rather than
reliably better. The two findings that do replicate within a model are that deliberation count does
nothing, and that the presentation change in Section 5.3 has a real, model-specific effect, unlike
this arm's run-to-run noise.

### 5.3 Genuine retrieval removes the effect, but only for Opus

The change that does the most is how the options reach the agent. When we take the menu out of the
prompt and require the agent to discover the catalogue through its own `list_products` and
`get_specs` calls, Opus's decoy effect disappears: the flattered share falls straight back to the
no-decoy baseline. For Opus this holds in both markets (laptops 60% to 0%; cloud-storage plans, a
full reversal under co-presentation, back to 0%). But this is the most important correction the
replication forced on us: **the escape is specific to Opus.** Run the same retrieval design on Sonnet
4.6 and Haiku 4.5 and the decoy keeps its grip.

| Market (flattered target) | Model | Co-presentation (menu in prompt) | Retrieval (agent looks it up) | Retrieval verdict |
|---|---|---:|---:|---|
| Laptops (Laptop B) | Opus 4.8 | 60% | 0% | eliminated |
| Laptops (Laptop B) | Sonnet 4.6 | 100% | 100% | persists |
| Laptops (Laptop B) | Haiku 4.5 | 100% | 93% | persists |
| Storage (Plan A) | Opus 4.8 | 100% | 0% | eliminated |
| Storage (Plan A) | Haiku 4.5 | 100% | 67% | persists |

**Figure 3 |** The flattered target's share under co-presentation versus genuine retrieval, by model
and market. Retrieval collapses the effect to baseline for Opus but not for the others: it is
unchanged for Sonnet (laptops, retrieval-with-decoy versus retrieval-without: *p* < .0001, Cramer's V
0.97) and, for Haiku, reduced but far from eliminated (laptops 93%, storage 67%). (Sonnet on storage is omitted: its menu-reading default there is already Plan A, a ceiling
that leaves no co-presentation effect to remove, and its baseline flips to Plan B under retrieval, so
the cell cannot test the question.)

Crucially, the surviving effect is not the weaker models failing to look at the decoy. With per-call
logging we can see exactly what each agent inspected, and in **every one of the 180 retrieval trials
across all three models and both markets, the agent called `get_specs` on the decoy** before
choosing (for the featured Opus run, every trial ran the identical `list_products`, three spec
lookups, `choose_product` sequence). Sonnet and Haiku read the dominated option's numbers themselves,
one at a time, and were swayed anyway. So retrieval is not a general antidote that works
by forcing the agent to examine options on their merits; it is something Opus specifically does with
self-assembled information that Sonnet and Haiku do not. The presentation lever that rescues one
Claude model does not rescue the others.

### 5.4 Recognition control: it replicates on an un-memorised market

Because the decoy paradigm is a textbook example, the in-prompt result could in principle be the
model recognising the setup. The control reruns the identical in-prompt design in an unrelated
market, cloud-storage plans traded off on price against storage. The effect does not weaken; it
strengthens. Here the model's default taste flips (it prefers the storage-rich Plan B), so the
informative cell is the decoy-for-A condition, where a decoy dominated by A produces a complete
reversal, from 0% A to 100% A. Susceptibility on a domain the model cannot be recalling rules out
recognition as the explanation.

| Condition | Plan A (cheaper, less) | Plan B (pricier, more) | Plan C (decoy) |
|---|---:|---:|---:|
| Opus, no decoy | 0% | 100% | 0% |
| Opus, decoy for A | **100%** | 0% | 0% |
| Opus, decoy for B | 0% | 100% | 0% |

This table is the co-presentation (in-prompt) design, which is what the recognition control is for;
the matching retrieval arms for this market are folded into the cross-market panel in Section 5.3,
where Opus again returns to baseline and Haiku stays swayed.

### 5.5 Model dependence: the Claude family copies it, GPT-5 largely resists

To move from "Opus is swayed" toward "models are swayed," the in-prompt decoy-for-B condition was
run on five further models. The copy is real but not universal; it splits by provider. Within the
Claude family the effect replicates and grows; across the GPT-5 family it nearly disappears. Each
column below is that model's own run at default sampling, so magnitudes are noisy between
independent runs (Opus's in-prompt decoy share, for instance, has landed anywhere from the high 30s
to 60% across runs); what is stable is the direction and the provider split.

| Laptop B share | Opus 4.8 | Sonnet 4.6 | GPT-5.5 | GPT-5.4 | GPT-5.4-mini |
|---|---:|---:|---:|---:|---:|
| No decoy | 0% | 0% | 0% | 0% | 0% |
| Decoy for B | 60% | **100%** | 13% | 0% | 3% |

**Figure 4 |** Laptop B's share (the flattered target) with a decoy present. Every model shares the
same default (0% B with no decoy); the decoy is where they separate. Within Claude the pull is large
(a full reversal for Sonnet, and Haiku 4.5 behaves the same way). Across GPT-5 it is marginal:
GPT-5.5 nudges 13 points (4 of 30 trials, not distinguishable from zero at this sample size, *p* =
.11), the mini moves a single trial, and GPT-5.4 does not move at all. On a stimulus that flips a
Claude model completely, the GPT-5 models show at most a hint of a pull.

### 5.6 Synthesis

Four results, in order of how well they replicate. The decoy effect transfers to the agent whenever
the options are co-presented in the prompt (Section 5.1), and this is robust: it shows up for Opus,
Sonnet, and Haiku on laptops, and replicates on a second, un-memorised market (Sections 5.4, 5.5),
and is weak-to-absent only across the GPT-5 family. Within that co-presentation setting the number of
deliberation steps makes no difference (Section 5.2). The two ways of giving the agent more control
over the process are *not* robust fixes: autonomy is erratic for Opus (0% to 47% across runs), and
genuine retrieval, which cleanly removes the effect for Opus in both markets, leaves Sonnet and Haiku
fully swayed even though per-call logs show they inspected the decoy every time (Section 5.3). The
featured verdict is **copy**, and the sharper lesson is about what does and does not undo it: the
bias rides in through co-presentation for every Claude model tested, but the escape route, building
the choice set through the agent's own queries, only works for Opus. There is one lever that works
regardless of model, and it is upstream of all of this: do not put the decoy on the menu.

## 6. Assumptions

- **The two-attribute setup is a real tradeoff with a true asymmetric dominance.** A and B genuinely
  trade off, and each decoy is dominated by exactly one target, so a shift reflects the attraction
  effect rather than a response to a simply cheaper or better option.
- **The shift is measured against the model's own no-decoy baseline,** because its intrinsic taste is
  not the human 50/50. The human row is shown for reference only.
- **The constrained `product_id` field measures the intended choice,** read from a strict enum.
- **In the retrieval arms, the served specifications are the agent's only source of the option data,**
  so the agent genuinely depends on its own tool calls. Per-call logging confirms directly that in
  every retrieval trial the agent looked up each option, the decoy included, before choosing.
- **Catalogue model IDs map to the intended deployed models,** with stable provider behaviour over
  the run window.

## 7. Limitations

- **Ceiling effects.** The model's near-deterministic default means each market can show the decoy
  moving choice on only one side; the other sits at a ceiling. The headline rests on decoy-for-B for
  laptops and decoy-for-A for storage.
- **Single-run magnitudes are noisy.** At default sampling with 30 trials per cell, the in-prompt
  decoy share varies run to run (the laptop decoy-for-B cell has ranged from the high 30s to 60%
  across independent runs). The *direction* is stable, but precise point estimates should not be
  over-read.
- **The autonomous arm is the least stable measurement here.** Across three Opus runs it returned 0%,
  3%, and 47% B. Treat "autonomy dissolved the effect" and "autonomy did not" as both within the
  noise; the reliable contrast is the retrieval one, which is consistent within each model.
- **The retrieval escape is model-specific, and the evidence on the weaker models is uneven.** The
  Opus elimination replicates across both markets, but the Sonnet and Haiku results rest on one run
  each per market, two of which carry noise: Haiku's single-shot arm lost most trials to empty tool
  calls (so that one cell is under-powered), and Haiku's retrieval baselines were not a clean 0%.
  Haiku's retrieval effect is reduced rather than zero, and Sonnet's storage cell is a ceiling that
  cannot test the question. The Sonnet laptop persistence (100% under retrieval) is the cleanest of
  the non-Opus cells.
- **Strong intrinsic tastes.** The models' value judgements (A for laptops, B for storage, and
  Sonnet's presentation-dependent storage default) are themselves worth study and may interact with
  the decoy in ways a 50/50 baseline would not.

## 8. Conclusion

The attraction effect is the first bias in this series that an agent clearly **copies** rather than
smooths away, and the replication makes clear how stubborn the copy is. Handed a ready-made
comparison, every Claude model tested is swayed by a dominated option it never chooses, in the
direction the theory predicts; the effect appears on a memorised market and an un-memorised one
alike, and no number of deliberation steps changes it. The tempting fixes are less dependable than they first look.
Autonomy is erratic: the same Opus configuration shed the bias in one run and kept it in another.
Genuine retrieval, making the agent assemble the choice set through its own tool calls, cleanly
removes the effect for Opus in both markets, but Sonnet and Haiku stay swayed even though per-call
logs prove they inspected the decoy every single time. So "have the agent look things up itself" is a
real fix for one model and not for its siblings. For anyone building or using AI agents to choose
among options, the one lever that does not depend on which model you happen to be running sits
upstream of the agent: **control the option set**. A padded shortlist or a decoy pricing tier can
steer an AI shopper exactly as it steers a human one, and the reliable defence is not a clever prompt
or more autonomy but to keep the dominated option off the menu in the first place, and to present
alternatives on a clean, like-for-like basis.

## Data and code

Every prompt, all trials, the tool definitions, and the analysis behind these charts live on GitHub:
the featured laptop run in
[`experiments/decoy-effect`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/decoy-effect)
and the cloud-storage replication in
[`experiments/decoy-effect-novel`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/decoy-effect-novel).
Rerun them, recode them, or check the numbers yourself.

## References

Huber, J., Payne, J. W., & Puto, C. (1982). Adding asymmetrically dominated alternatives: Violations
of regularity and the similarity hypothesis. *Journal of Consumer Research, 9*(1), 90–98.
[https://doi.org/10.1086/208899](https://doi.org/10.1086/208899)

Simonson, I. (1989). Choice based on reasons: The case of attraction and compromise effects.
*Journal of Consumer Research, 16*(2), 158–174.
[https://doi.org/10.1086/209205](https://doi.org/10.1086/209205)

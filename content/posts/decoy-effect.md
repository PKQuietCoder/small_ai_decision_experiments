---
category: Decisions
type: Experiments
date: '2026-06-24'
excerpt: 'Add a clearly worse third option to a menu and people shift toward whichever original it flatters. Do models? We reran Huber, Payne & Puto (1982) on six models (Opus 4.8, Sonnet 4.6, Haiku 4.5, GPT-5.5, GPT-5.4, GPT-5.4-mini) in two parts. Part I (replication): models almost never choose the dominated decoy (0 to 2% across models), yet range decoys pull every model toward the target, often well beyond the human +13. Frequency decoys split by family: every Claude model reverses into a similarity effect, and the GPT-5 flagships stay human-like. Part II (agentic extension): the same choice under single-shot, forced-workflow, autonomous, and retrieval scaffolds on Opus. No scaffold gets the agent to choose the decoy, even when it looks the decoy up itself. More deliberation undoes the single-shot frequency reversal (17% → 71%), and retrieval removes the range attraction lift. How you present the options, and how an agent deliberates, change which way a worthless option bends the choice.'
experimentId: decoy-effect
verdict: mixed
controls: 'Coverage and design controls across two parts. Part I reproduces the paper''s six product categories with exact Appendix II attribute values, crosses all four decoy-placement strategies (R, R*, F, RF) against a no-decoy baseline, verifies that the target asymmetrically dominates every decoy and the competitor doesn''t, and reruns the 30-condition design on six models (the Claude family plus three GPT-5 models). Part II holds that choice fixed for three categories and varies only the agentic scaffold (single-shot / forced-workflow / autonomous / retrieval) within one tool harness, with neutral option ids, a per-cell enum clamp so a no-decoy menu can''t offer the decoy, and per-call logging confirming the retrieval agent inspected the decoy in every trial.'
featured: false
published: true
runId: 20260624T020831Z
slug: decoy-effect
tags:
- decoy-effect
- attraction-effect
- similarity-effect
- choice
- decision-making
- agents
- tool-use
- deliberation
- retrieval
title: 'The Decoy Effect: Does a Worse Option Sway a Model''s Choice?'
---

## Abstract

Picture a menu with three options, where the third is plainly worse than one of the other two.
Almost nobody picks it. But people shift toward whichever original the dud makes look good. That's
the decoy effect, one of the most cited findings in the study of human choice. Does a model fall for
it?

We reran the study that named the effect, Huber, Payne and Puto's *Adding asymmetrically dominated
alternatives* (1982), and kept it faithful: the same six product categories, two attributes per
option, a target and a competitor in a real tradeoff, an asymmetrically dominated decoy, and the
paper's four decoy-placement strategies. The featured model is Claude Opus 4.8. We reran the full
design on the rest of the Claude family (Sonnet 4.6, Haiku 4.5) and on three GPT-5 models (GPT-5.5,
GPT-5.4, GPT-5.4-mini), running each of the thirty conditions thirty times per model (900 trials
each).

The featured Opus run has three layers. Opus never chooses the dominated decoy: **0 of 720** trials
where we offered it, cleaner even than the 1 to 2 percent humans gave it. The decoy's presence still
reshapes the choice between the other two, and strongly (overall χ² = 731, *p* ≈ 10⁻¹³⁵, Cramér's V
0.90). And unlike with people, the *direction* of that shift flips with the decoy's placement.
Range-increasing decoys produce the attraction effect the theory predicts, pulling choice toward the
target (mean change +20 and +17 points). Frequency-increasing decoys do the opposite, in a pattern
consistent with a similarity effect, pushing choice toward the distinctive competitor (mean change
−28 and −44 points). In the original, every placement nudged the target upward, by an average of
nine points.

The six-model panel sharpens this. The attraction effect under range decoys is *universal*: every
model, Claude and GPT-5 alike, moves toward the target, often far more strongly than people do. The
frequency reversal is a **Claude-family trait**. All three Claude models (Opus, Sonnet, Haiku) flip
frequency decoys into the similarity effect and abandon the target. The GPT-5 flagships (5.5, 5.4)
keep every placement weakly positive, reproducing the gentle human ordering, and the small
GPT-5.4-mini lands in between. If you hand a model a menu, the model isn't indifferent to a
worthless option on it. Which way it bends depends on where that option sits and on which model is
choosing.

The report has two parts. **Part I. Replication** runs the original study faithfully and across the
six-model panel. **Part II. Extension: agentic scaffolds** takes the same choice and wraps it in the
scaffolds an agent runs inside (a single tool call, a forced inspect-compare-choose workflow,
autonomous tool use, and a retrieval arm where the agent must look the options up itself) to ask
whether *how* the agent decides changes the bias.

# Part I. Replication

## 1. Background: the human baseline

### 1.1 The original finding

In 1982 the marketing researchers Joel Huber, John Payne, and Christopher Puto published *Adding
asymmetrically dominated alternatives: Violations of regularity and the similarity hypothesis*
(*Journal of Consumer Research* 9(1): 90-98). One hundred and fifty-three students chose among
products in six categories (beer, cars, restaurants, lotteries, film, and television sets), with
each option described on just two attributes. In each set a **target** and a **competitor** form a
real tradeoff. The target is better on one attribute and the competitor on the other, so neither
dominates.

The manipulation adds a third option, the **decoy**, placed so that it's **asymmetrically
dominated**: the target dominates it (the decoy is no better on either attribute, and worse on at
least one), but the competitor doesn't. Almost no one chooses this decoy. Yet its presence raises
the share going to the target. The decoy never wins, and it still changes who does. That violates
*regularity*, a property most formal models of choice assume, because adding an option nobody
chooses shouldn't alter the split between the other two. Later work replicated the finding across
many product classes and tied it to the related compromise effect (Simonson 1989).

### 1.2 Four ways to place a decoy

The paper's sharpest contribution is that *where* the decoy sits matters. (The earlier write-up of
this experiment left that part out entirely.) Huber and colleagues defined four placement
strategies. We illustrate them with beer: target $1.80 a sixpack at quality 50, competitor $2.60 at
quality 70.

Two words do the work here, **range** and **frequency**, and they name *how* a decoy is placed. A
**range** decoy stretches the span of values on the attribute where the target is weak. It
introduces a new, worse extreme on that dimension, so the target's mediocre value now sits further
from the bottom of the scale. A **frequency** decoy adds no new extreme. It sits inside the existing
span and increases *how many* options the target beats on the attribute where the target is strong.
The target wins more comparisons; the scale doesn't widen. The four rows below are these two ideas
and their crosses. **R\*** is a more extreme range decoy, and **RF** combines a range move with a
frequency one.

| Strategy | What it does (Huber et al., p. 92) | Example decoy (beer) |
|---|---|---|
| **R**, moderate range | extends the range on the attribute where the target is *weakest*: a worse-quality option at the target's price | $1.80, quality 40 |
| **R\***, extreme range | extends that weak-attribute range further | $1.80, quality 30 |
| **F**, frequency | adds an option along the attribute on which the target is *superior*: a higher price at the target's quality, sitting between target and competitor | $2.20, quality 50 |
| **RF**, range-frequency | combines both | $2.20, quality 40 |

The target dominates all four, and the competitor dominates none. The distinction is geometric. A
range decoy shares the target's value on its strong attribute and is worse on the weak one, a
strictly inferior shadow of the target. A frequency decoy matches the target on its weak attribute
and sits between the target and the competitor on the dimension the target wins. The paper found
that every placement raised the target's share, with range strategies doing so far more strongly
than frequency.

### 1.3 The baseline, in one table

The original is a within- and between-subjects design. It manipulates one factor (which decoy, if
any, is present) and measures one outcome, the target's share of choices. Its signature is
*directional and uniform*: adding any decoy raises the target specifically, while hardly anyone
chooses the decoy itself.

| Baseline parameter | Value (Huber, Payne & Puto 1982) |
|---|---|
| Categories | Beer, cars, restaurants, lotteries, film, television sets |
| No-decoy target share | ≈ 0.50 (0.485 / 0.515 across the two target roles) |
| Average gain from a decoy | +9.2 points (between-subjects) |
| By placement | Range R / R\* +13 · range-frequency RF +8 · frequency F +4 |
| Decoy's own share | ≈ 1 to 2 percent |
| Per-category gain | Cars +13 · TV +16 · Restaurants +10.5 · Beer +10 · Film +3.8 · Lotteries +2 |

Every number in the "by placement" and "per-category" rows is positive. That uniform, target-ward
pull is the baseline for everything below.

## 2. Objectives of this rerun

Every study in this series asks one question of a human bias: does the model **copy** it, **smooth**
it away, or **amplify** it? For the decoy effect we ask it with the paper's full apparatus intact.
That way we test placement, the part that separates the attraction effect from its rival, the
similarity effect.

| # | Objective | What it tests |
|---|---|---|
| 1 | Decoy avoidance | Does the model leave the asymmetrically dominated decoy unchosen, as people do? |
| 2 | Regularity | Does adding a never-chosen decoy change the target-versus-competitor split at all? |
| 3 | Direction | When the split moves, does it move toward the target (attraction) as the theory predicts? |
| 4 | Placement sensitivity | Do the four placement strategies behave as they did for people (all positive, range stronger than frequency), or differently? |
| 5 | Breadth | Does the pattern hold across all six of the paper's categories, not one convenient market? |
| 6 | Model generality | Does the pattern hold across model families, or is any part of it specific to one model? |

## 3. Methods

### 3.1 The faithful translation

Each trial gives the model the paper's task, verbatim in spirit: a short menu of two or three
options in one category, each described on exactly two attributes, with the instruction to choose
one "on this information alone." The attribute values are the paper's own (Appendix II level
scales). The target is strong on the first attribute and middling on the second. The competitor is
the reverse. The decoy sits beside the target according to the placement strategy. The six
categories and their two attributes:

| Category | Attribute 1 (better is) | Attribute 2 (better is) | Target | Competitor |
|---|---|---|---|---|
| Beer | price/sixpack (lower) | quality 0 to 100 (higher) | $1.80 / 50 | $2.60 / 70 |
| Cars | ride quality 60 to 100 (higher) | gas mileage mpg (higher) | 100 / 27 | 80 / 33 |
| Restaurants | driving time min (lower) | food quality stars (higher) | 5 / 3★ | 25 / 5★ |
| Lotteries | chance of winning % (higher) | prize $ (higher) | 84% / $36 | 56% / $54 |
| Film | developing time min (lower) | colour fidelity 0 to 100 (higher) | 0.5 / 93 | 3 / 97 |
| TV sets | picture distortion % (lower) | reliability years (higher) | 0.5% / 4 | 2.5% / 6 |

We generate the decoy for each category by applying the four strategies above to that category's
scale. We verified that the target dominates every decoy (no better on either attribute, and worse
on at least one) and that the competitor does **not**. A shift therefore comes from the attraction
or similarity mechanism, not from an option that's just cheaper or better.

### 3.2 Conditions and design

Six categories crossed with five menus (no decoy, plus the four placement strategies R, R\*, F, RF)
give thirty conditions. We ran each thirty times, for 900 trials. The prompt presents the options
neutrally as "option 1, 2, 3". The role words *target*, *competitor*, and *decoy* never appear in
the prompt or in the choice the model can make. We read the model's pick from a schema-constrained
field (Anthropic forced tool use) and never parse it from prose. Option positions stay fixed across
conditions: the target is always option 1, the competitor option 2, the decoy option 3. The clean
comparison is therefore the change from a category's no-decoy menu to each of its decoy menus, where
the target and competitor sit in the same slots and only the decoy is new. (The original
counterbalanced positions across groups. We hold them fixed and read the within-category change. See
Limitations.)

### 3.3 Outcome and statistics

For each condition we report every option's share of its thirty choices. The quantity that matters
is the **target's share**, and how it changes when we add a decoy. We summarise whether a choice
distribution moves with a chi-square test of independence and Cramér's V, dropping all-zero option
columns before testing so the never-chosen decoy column doesn't distort the statistic. The featured
run is Claude Opus 4.8 at its default sampling. To test model generality we reran the entire
30-condition design on the rest of the Claude family (Sonnet 4.6, Haiku 4.5) and on GPT-5.5,
GPT-5.4, and GPT-5.4-mini (the GPT-5 models are reasoning models, run at low reasoning effort), 900
trials each. Sections 4.1 to 4.4 report the featured Opus run, and Section 4.5 compares the
six-model panel.

## 4. Results

### 4.1 The decoy is never chosen, but the choice still moves

A dominated decoy was on the menu in 720 trials. The model chose it **zero times**. People give the
decoy 1 to 2 percent; Opus gives it nothing. That settles the precondition for an interesting
result. Any change in the split between target and competitor is a distortion caused by a worthless
option, not the decoy quietly winning a few choices.

And the split does change, dramatically. Treat the menu as the factor and the choice as the outcome,
and the association is overwhelming (χ² = 731, df 29, *p* ≈ 2.8 × 10⁻¹³⁵, Cramér's V 0.90). The
model isn't immune to a dominated option. The question is which way it bends.

### 4.2 Range decoys produce the attraction effect

Take television sets. On the bare two-option menu the model chooses the target 0 percent of the
time. Add the moderate range decoy (R) and the target goes to 100 percent: a complete reversal in
the predicted direction, produced by an option the model never picks.

That's the attraction effect, and it's what the R and R\* strategies produce generally. Each decoy
is a strictly inferior shadow of the target, sharing the target's strong-attribute value and worse
only on the weak one. Averaged across the six categories, the target's share rises by +20.0 points
under R and +17.2 under R\*. The only declines are small ones in two categories already sitting at
the 100 percent ceiling (a 7-point dip for cars and 10 for lotteries under R\*, within sampling
noise at thirty trials).

### 4.3 Frequency decoys reverse it into a similarity effect

Cars show the opposite. The target takes 100 percent of choices on the bare menu. Add a frequency
decoy and its share collapses to 0 percent.

An F or RF decoy matches the target on its weak attribute and gives up ground on the dimension the
target wins, sitting between the target and the competitor there. It doesn't flatter the target. It
acts as the target's near-substitute, and the model abandons the target for the distinctive
competitor. Averaged across categories the target's share *falls* by −27.8 points under F and −44.4
under RF, and no frequency decoy raises it (the single exception is a 13-point rise off a floor, in
television sets under RF). This is consistent with the similarity effect, the rival mechanism the
original study's design was built to overpower. It re-emerges whenever the decoy sits as a
near-substitute for the target instead of a strictly dominated shadow of it.

| Placement | Mean change in target share | Categories up / flat / down |
|---|---:|---|
| R, moderate range | **+20.0** | 3 / 3 / 0 |
| R\*, extreme range | **+17.2** | 3 / 1 / 2 |
| F, frequency | **−27.8** | 0 / 3 / 3 |
| RF, range-frequency | **−44.4** | 1 / 1 / 4 |

**Figure 1 |** Mean change in the target's choice share, by decoy placement, relative to each
category's no-decoy menu. Range decoys (R, R\*) move the target up; frequency decoys (F, RF) move it
down. For people, all four were positive (R/R\* +13, RF +8, F +4). The model preserves the ordering,
with range outperforming frequency, but stretches it across zero and turns the weak frequency effect
into a reversal.

### 4.4 The split, category by category

The model's intrinsic taste is near-deterministic and differs by category. Most categories therefore
start at a floor (0 percent target) or a ceiling (100 percent), which limits the direction a decoy
can visibly move the choice. Film is the exception. Its no-decoy target share is 87 percent, with
room to move either way, and it shows both halves of the result inside a single category: range
decoys push it up, frequency decoys push it down.

| Category | No decoy | R | R\* | F | RF |
|---|---:|---:|---:|---:|---:|
| Beer | 0% | 10% | 13% | 0% | 0% |
| Cars | 100% | 100% | 93% | 0% | 0% |
| Restaurants | 100% | 100% | 100% | 93% | 13% |
| Lotteries | 100% | 100% | 90% | 100% | 77% |
| Film | 87% | 97% | 100% | 27% | 17% |
| TV sets | 0% | 100% | 93% | 0% | 13% |

**Figure 2 |** Target's choice share (percent of 30 trials) for each category and placement. Read each
row against its own no-decoy cell. Range columns (R, R\*) hold or raise the target; frequency columns
(F, RF) hold or lower it. Film, the one category with a mid-range baseline, shows the full split on
its own: 87 percent rising to 97/100 under range decoys and falling to 27/17 under frequency decoys.

### 4.5 Does it generalize across models?

Is the placement split a property of language models, of the Claude family, or of this one model? We
reran the full thirty-condition design on the rest of the Claude family and on three GPT-5 models to
find out. Half of the result is universal. The other half splits by model family. The table gives
each model's mean change in target share, by placement, averaged across the six categories.

| Placement | Opus 4.8 | Sonnet 4.6 | Haiku 4.5 | GPT-5.5 | GPT-5.4 | GPT-5.4-mini | Humans |
|---|---:|---:|---:|---:|---:|---:|---:|
| R, moderate range | +20.0 | +16.7 | +12.2 | +39.4 | +47.2 | +12.2 | +13 |
| R\*, extreme range | +17.2 | +21.7 | +7.2 | +36.7 | +46.1 | +6.7 | +13 |
| F, frequency | **−27.8** | **−31.7** | **−30.6** | +8.3 | +0.6 | −16.7 | +4 |
| RF, range-frequency | **−44.4** | **−22.8** | **−16.7** | +12.2 | +3.9 | +5.0 | +8 |
| *Decoy chosen* | 0% | 0% | 2% | 0% | 0% | 1% | 1 to 2% |
| *Cramér's V (overall)* | 0.90 | 0.96 | 0.79 | 0.76 | 0.79 | 0.55 | n/a |

**Figure 3 |** Mean change in the target's choice share by placement, for all six models, against the
human baseline. Range rows are positive everywhere. The frequency rows split cleanly by family, with
every Claude model negative and both GPT-5 flagships positive.

Some things hold for every model. The decoy is still almost never chosen: 0 percent for Opus,
Sonnet, GPT-5.5 and GPT-5.4, and 1 to 2 percent for Haiku and GPT-5.4-mini, the closest of any to
the human 1 to 2 percent. The choice still moves strongly with the menu (Cramér's V from 0.55 for
the mini to 0.96 for Sonnet, every model *p* < 10⁻⁷⁸). And range decoys pull toward the target in
all six. The GPT-5 flagships show the largest attraction effect of all, with R and R\* near +40 to
+47 points, several times the human +13.

The reversal splits the panel, and it splits by family, not by model. All three Claude models turn
frequency decoys sharply negative (F −28 / −32 / −31 for Opus / Sonnet / Haiku; RF −44 / −23 / −17).
The similarity effect is a Claude-family signature, not an Opus quirk. The GPT-5 flagships do the
opposite and stay weakly positive on both frequency placements (GPT-5.5 +8 / +12; GPT-5.4 +1 / +4).
That's the gentle human pattern: every placement positive, frequency much weaker than range. The
small GPT-5.4-mini sits between the families. It reverses on F (−17) like Claude but stays
flat-positive on RF (+5). Whether a dominated near-substitute pushes the choice toward the target or
away from it comes down to the model family, with Claude and GPT-5 landing on opposite sides.

### 4.6 Synthesis (replication)

Four findings, ordered by how widely they hold. Every model leaves the dominated decoy almost
entirely unchosen (Sections 4.1, 4.5). In every model its presence reshapes the choice strongly and
significantly (Sections 4.1, 4.5). In every model range decoys reproduce the attraction effect, and
usually amplify it (Sections 4.2, 4.5). Only the fourth finding splits the panel, and it splits by
family: under frequency decoys every Claude model (Opus, Sonnet, Haiku) reverses into a pattern
consistent with the similarity effect and abandons the target, while the GPT-5 flagships hold the
human-like weakly-positive pattern (Sections 4.3, 4.5). The verdict for this series is therefore
**mixed**. No model smooths the bias away, and none copies the gentle human version as is. Every
model is highly sensitive to a dominated option it never picks. What differs, by family, is which
way a near-substitute decoy bends the choice.

# Part II. Extension: agentic scaffolds

## 5. Why extend to agents

Part I reran the original as a single forced choice, stripped of any agentic apparatus on purpose,
to stay faithful to the paper. But when a model chooses among options in real use, it's usually
acting as an agent: it calls tools, takes several steps, or looks things up. Is the bias an artifact
of the one-shot framing? Or does it survive, and change, when we wrap the same choice in the
scaffolds an agent runs inside?

This part is a methods extension, not a human comparison. No human "agentic" baseline exists. Every
comparison here is *within* a single experiment and a single tool harness, where only the scaffold
changes between conditions.

## 6. Agentic design

We cross two factors on top of the fixed paper choice.

**The decision (held fixed).** We use three categories: film, cars, and television sets. They span a
fragile mid-range default (film), a target-favouring default (cars), and a competitor-favouring
default (TV). For each, the target, the competitor, and the four placement decoys take the paper's
exact Appendix II attribute values, identical to Part I. The prompt presents options neutrally as
"option 1/2/3" and the role words never appear. We clamp the per-cell choice enum so a no-decoy menu
can offer only its two real options.

**The scaffold (varied).** Four modes. The first three put the menu in the prompt, and the last
hides it behind tools:

| Mode | What the agent does | Menu | Mean tool calls |
|---|---|---|---:|
| Single-shot | one `choose` call, decide immediately | in prompt | 1.0 |
| Forced workflow | pinned `inspect` → `compare` → `choose` | in prompt | 3.0 |
| Autonomous | calls tools freely until it picks (`mode: auto`) | in prompt | 3.0 |
| Retrieval | must `list` and `get_specs` each option, then `choose` | retrieved | 4.8 |

Three categories × five placements (no decoy, R, R\*, F, RF) × four modes = sixty conditions, thirty
trials each, on Claude Opus 4.8 at default sampling. We read the choice from a schema-constrained
tool field. In the retrieval arm only `get_specs` serves the option data, and we log every call.
**One caveat on baselines:** the single-shot tool harness isn't identical to the structured-output
harness used in Part I, and for the fragile film default the two disagree (film's no-decoy default
flips between them). We therefore don't compare these numbers to the Part I run. We compare *modes
against each other within this experiment*, where the harness stays constant.

## 7. Agentic results

### 7.1 The decoy is never chosen, even when the agent looks it up itself

In the retrieval arm the agent can't see the decoy without asking for it. It always asks. In **360
of 360** retrieval trials with a decoy present, the agent called `get_specs` on the dominated option
before choosing, and it never chose it.

The other scaffolds agree. The decoy's share is 0.8 percent under single-shot, 0.3 percent under the
workflow, 1.1 percent under autonomy, and 0.0 percent under retrieval (across 1,440 decoy-present
trials, fewer than ten picked the decoy). Reading the worthless option's numbers one at a time, on
its own initiative, doesn't make the agent pick it. As the next sections show, it doesn't make the
agent immune to it either.

### 7.2 Range attraction survives deliberation but breaks under retrieval

When the decoy extends the range on the target's weak attribute (the R and R\* strategies), the
target-ward pull shows up under every co-presented scaffold, and it's large. Pooling the three
categories, a range decoy under a co-presented menu lifts the target to **99 percent** of choices.
The single-shot, forced-workflow, and autonomous arms are indistinguishable on this. Deliberation
doesn't touch the range attraction effect.

Retrieval does. When the agent must look the options up itself, the same range decoy leaves the
target at **62 percent**. That's about where its no-decoy retrieval baseline sits (roughly 67
percent), so there's no attraction lift at all (co-presented versus retrieval for the range decoy:
χ² = 94, *p* < 10⁻²¹, Cramér's V 0.51). The lift is worth roughly +67 points when we hand the menu
over. It drops to about −5 when the agent assembles the menu through its own queries. Building the
choice set one fact at a time removes the range attraction effect that co-presentation reliably
produces.

### 7.3 Deliberation undoes the frequency reversal

The scaffold matters most for the frequency decoys. A frequency decoy mimics the target on its weak
attribute and edges toward the competitor. Facing one, the single-shot agent shows the same reversal
Part I found for Opus: it abandons the target for the competitor, and the target takes just **17
percent** of choices. Add process and the reversal unwinds. The forced inspect-compare-choose
workflow lifts the target to **53 percent**, and full autonomy lifts it to **71 percent**
(single-shot versus autonomous: χ² = 57, *p* < 10⁻¹², Cramér's V 0.56; the three-way trend across
modes is likewise significant). More deliberation pulls the target back out of the similarity trap
that the one-shot choice falls into. Retrieval goes the opposite way and drives the target well
below its baseline. The range-frequency (RF) decoy is the noisiest case. It stays mildly
target-negative across the co-presented modes and doesn't recover the way the pure frequency decoy
does.

| Mean change in target share vs that mode's no-decoy menu | R | R\* | F | RF |
|---|---:|---:|---:|---:|
| Single-shot | +66.7 | +57.8 | **−15.6** | −24.4 |
| Forced workflow | +70.0 | +70.0 | **+23.3** | −8.9 |
| Autonomous | +63.3 | +65.6 | **+36.7** | −16.7 |
| Retrieval | −4.4 | −1.1 | −55.6 | −58.9 |

**Figure 4 |** Mean change in the target's choice share (averaged over film, cars, and TV), relative to
each scaffold's own no-decoy menu. Range columns (R, R\*) stay strongly positive across the three
co-presented scaffolds and vanish under retrieval. The frequency column (F) climbs from negative under
single-shot to strongly positive under autonomy, which is deliberation undoing the reversal, then
collapses under retrieval.

### 7.4 Retrieval also moves the agent's baseline taste

Retrieval isn't just a different delivery of the same decision. The agent's *no-decoy* default
shifts when it reads specs serially instead of from a menu: the no-decoy target share is 53 percent
for film and 67 percent for TV under retrieval, against 0 percent for both under the co-presented
scaffolds. Retrieval changes both the baseline and the decoy's effect, so read its column in Figure
4 as a distinct regime, not a clean overlay on the others. Two retrieval findings survive the
baseline shift and are robust: the range attraction lift disappears (7.2), and frequency decoys
drive the target sharply below its retrieval baseline (7.3).

### 7.5 Category by category

Each category sits near a floor or ceiling on the bare menu, so the clearest demonstration is film,
whose default has room to move both ways.

| Category · placement | Single-shot | Workflow | Autonomous | Retrieval |
|---|---:|---:|---:|---:|
| **Film** no decoy | 0% | 0% | 3% | 53% |
| Film R / R\* | 97% / 100% | 100% / 100% | 100% / 100% | 87% / 100% |
| Film F | 50% | 93% | 100% | 0% |
| Film RF | 23% | 30% | 53% | 20% |
| **Cars** no decoy | 97% | 90% | 100% | 80% |
| Cars R / R\* | 100% / 93% | 100% / 100% | 100% / 100% | 0% / 0% |
| Cars F | 0% | 13% | 17% | 0% |
| Cars RF | 0% | 0% | 0% | 0% |
| **TV** no decoy | 0% | 0% | 0% | 67% |
| TV R / R\* | 100% / 77% | 100% / 100% | 93% / 100% | 100% / 97% |
| TV F | 0% | 53% | 97% | 33% |
| TV RF | 0% | 33% | 0% | 3% |

**Figure 5 |** Target's choice share (percent of 30 trials) for every category, placement, and scaffold.
The deliberation-undoes-frequency pattern is clearest in film F (50 → 93 → 100) and TV F (0 → 53 → 97).
Cars, whose target is at the ceiling without a decoy, shows it only weakly. The cars retrieval row is
the starkest case of retrieval's susceptibility: any decoy at all collapses the target to 0 percent.

### 7.6 Synthesis (extension)

The agentic scaffold isn't neutral. Two parts of the decoy result are scaffold-proof: the agent
never chooses the dominated option (even when it fetches the specs itself), and range decoys pull
toward the target under every co-presented regime. The rest depends on the scaffold. Deliberation,
whether a forced inspect-compare-choose workflow or full autonomy, pulls the target back out of the
single-shot frequency reversal. That's the opposite of what you'd expect if more steps changed
nothing. Retrieval is the most consequential intervention of all. It removes the range attraction
lift, deepens the frequency collapse, and shifts the agent's underlying taste. For the decoy effect,
*how you ask the agent to decide* is itself part of the experiment.

# Both parts

## 8. Assumptions

- **The two-attribute setup is a real tradeoff with true asymmetric dominance.** In every category
  the target and competitor trade off, and the target alone dominates each decoy. We verified both
  numerically, so a shift reflects attraction or similarity, not a response to a plainly better
  option. We hold this decision fixed across both parts and, in Part II, across all four scaffolds.
- **We measure the shift against the right baseline.** In Part I that's each category's own no-decoy
  menu, because the model's intrinsic taste isn't the human 50/50 (the human row is there for
  reference). In Part II it's each scaffold's own no-decoy menu, because the harness itself moves the
  baseline.
- **The constrained choice field measures the intended pick.** We read it from a strict enum
  (structured output in Part I, forced tool use in Part II) and clamp the enum per cell, so the model
  can never select an option it wasn't shown. No-decoy menus offer only two options.
- **Part II comparisons are within one tool harness.** All four scaffolds share the same tool-call
  mechanism, so the single-shot arm is the within-experiment baseline, not a re-run of Part I's
  structured-output study. In the retrieval arm the served data is the agent's only source, and
  per-call logging confirms which options it inspected.
- **Catalogue model identifiers map to the intended deployed models,** with stable behaviour over the
  run window.

## 9. Limitations

- **Floor and ceiling effects.** Each model's near-deterministic taste puts most categories at 0 or
  100 percent on the bare menu, so a decoy can visibly move the choice in only one direction per
  category. We read the directional split across categories and, cleanly, within film, the one
  category with a mid-range baseline (in both parts).
- **Fixed option positions.** The original counterbalanced the target's and decoy's positions across
  groups. We hold positions fixed and use the within-category change from no-decoy to decoy as the
  unit of inference. This controls position for that contrast but doesn't estimate a position effect.
- **One run per model and per scaffold, thirty trials per cell.** Magnitudes at default (or
  low-reasoning) sampling are noisy. The stable results are the *directions* (universal attraction
  under range decoys, the Claude-family frequency reversal, and the scaffold effects in Part II), not
  precise point estimates. Part I reports six models (the Claude family and three GPT-5 models); Part
  II is Opus only. Repeated runs, a GPT-5 scaffold contrast, and a wider panel are the natural
  follow-ups.
- **Strong, model-specific intrinsic tastes.** Which option a model favours before any decoy varies by
  category, model, and (in Part II) scaffold. These baselines determine how much headroom a decoy has
  to move the choice, and they deserve study in their own right.
- **Part II's harness differs from Part I's.** The single-shot tool baseline isn't identical to Part
  I's structured-output baseline (film's default flips between them). That's why we read Part II
  strictly within-experiment and not against Part I's numbers.
- **Retrieval confounds delivery with baseline.** The RF decoy is also the least stable cell: it
  doesn't show the clean deliberation-rescue that the pure frequency (F) decoy does.

## 10. Conclusion

Given the original decoy task in full, every model reproduces the part everyone remembers: a
dominated option that nobody picks still bends the choice. A range decoy pulls every model toward
the target, usually harder than it pulls people. The frequency decoy is where they part company, and
they split by family. Every Claude model (Opus, Sonnet, Haiku) reverses toward the competitor, as if
a near-substitute made the target look replaceable. The GPT-5 flagships keep the gentle, uniformly
positive human pattern. The bias is real and nothing smooths it away, but its *direction* depends on
the placement and the model family.

It also depends on the scaffold. No scaffold gets the agent to choose the decoy, even when the agent
reads the specs itself, so an agent won't *buy* the obvious dud. Whether the decoy *bends* the
decision, and which way, shifts with the staging. More deliberation pulls the target back out of the
single-shot frequency reversal. Making the agent retrieve the options itself removes the range
attraction lift and quietly changes the agent's default taste.

If you're building or using an agent to choose among options, both parts say the same thing: the
list you provide is part of the instruction, and *how* the agent reads it is part of the experiment.
A padded or decoy-laden menu doesn't just add noise. It can swing the choice, and on some models and
under some scaffolds it can swing it in either direction. One defence held everywhere, for people
and models alike, and it sits upstream of all of this. Present real alternatives on a clean,
like-for-like basis, and keep dominated options off the menu.

## 11. Practical takeaways

From the replication (Part I):

| Observed | Why it happens | Do differently / how to interact |
|---|---|---|
| A dominated option almost nobody picks (0 to 2% across six models) still swung the choice, by up to a full reversal. | Choice is shaped by the *set*, not each option's standalone merit. | Treat **the list of options you hand a model as part of the prompt**; drop filler and obviously-worse choices and compare alternatives like-for-like. |
| Range decoys pulled toward the target in every model (up to +47); frequency decoys pushed every Claude model toward the competitor (−28 / −32 / −31 on F) but left the GPT-5 flagships weakly positive. | A strictly-worse shadow of the target flatters it (attraction); a near-substitute that mimics the target on its weak attribute can make it look replaceable (similarity). | **Where a worse option sits can decide which way the choice moves.** Adding "a slightly worse version of the option you want" can backfire on a whole model family. |
| The range attraction effect was universal and amplified; the frequency reversal split by family: every Claude model reversed, both GPT-5 flagships didn't. | Part of the bias is general to these models; part is family-specific. | Don't assume one family's decoy behaviour transfers; **measure the actual choice distribution for the model you deploy**. |

From the agentic extension (Part II):

| Observed | Why it happens | Do differently / how to interact |
|---|---|---|
| The decoy was never chosen in any scaffold (0 to 1%), and retrieval agents inspected it in 100% of trials yet picked it in none. | Tool-use and retrieval don't make an agent buy an obviously worse option. | You can trust an agent not to *buy* the junk tier; the risk is in **how it shifts the choice between the real options**. |
| Single-shot, forced-workflow, and autonomy all showed the range attraction effect. | The effect lives in the side-by-side comparison and resists added deliberation steps. | Don't expect **"add a planning/inspect step"** to neutralise a decoy-laden menu. It didn't. |
| Forcing a workflow or autonomy pulled the target back out of the single-shot frequency reversal (17% → 53% → 71%). | More deliberation can change *which* option a borderline decoy favours. | If a choice is decoy-sensitive, **the amount and structure of deliberation is a real lever**. Test it; don't assume it. |
| Retrieval removed the range attraction lift and shifted the agent's baseline taste. | Making the agent assemble the menu itself changes both the bias and the default decision. | **"Have the agent look it up" isn't a neutral swap.** Re-validate behaviour when you move from a co-presented menu to tool retrieval. |

## Data and code

Every prompt, all trials, the per-condition attribute values, and the analysis behind these charts and
tables live on GitHub: the replication (5,400 trials across six models) in
[`experiments/decoy-effect`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/decoy-effect),
and the agentic extension (1,800 trials with full tool-call transcripts) in
[`experiments/decoy-effect-agentic`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/decoy-effect-agentic).
Rerun them, recode them, or check the numbers yourself.

## References

Huber, J., Payne, J. W., & Puto, C. (1982). Adding asymmetrically dominated alternatives: Violations
of regularity and the similarity hypothesis. *Journal of Consumer Research, 9*(1), 90-98.
[https://doi.org/10.1086/208899](https://doi.org/10.1086/208899)

Simonson, I. (1989). Choice based on reasons: The case of attraction and compromise effects.
*Journal of Consumer Research, 16*(2), 158-174.
[https://doi.org/10.1086/209205](https://doi.org/10.1086/209205)

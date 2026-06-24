---
category: Decisions
type: Experiments
date: '2026-06-24'
excerpt: 'A faithful rerun of Huber, Payne & Puto (1982) on six models (the Claude family — Opus 4.8, Sonnet 4.6, Haiku 4.5 — plus GPT-5.5, GPT-5.4, GPT-5.4-mini), in two parts. Part I (replication): the dominated decoy is almost never chosen (0–2% across models), yet range decoys reliably pull toward the target on every model — often amplified well beyond the human +13 — while frequency decoys split by family, with every Claude model reversing into a similarity effect and the GPT-5 flagships staying human-like. Part II (agentic extension): the same choice under single-shot, forced-workflow, autonomous, and retrieval scaffolds on Opus — the decoy is never chosen in any scaffold (even when the agent looks it up itself), more deliberation undoes the single-shot frequency reversal (17% → 71%), and retrieval removes the range attraction lift. How options are presented, and how an agent deliberates, change which way a worthless option bends the choice.'
experimentId: decoy-effect
verdict: mixed
controls: 'Coverage and design controls across two parts. Part I reproduces the paper''s six product categories with exact Appendix II attribute values, crosses all four decoy-placement strategies (R, R*, F, RF) against a no-decoy baseline, verifies that every decoy is asymmetrically dominated by the target and not the competitor, and reruns the 30-condition design on six models (the Claude family plus three GPT-5 models). Part II holds that choice fixed for three categories and varies only the agentic scaffold (single-shot / forced-workflow / autonomous / retrieval) within one tool harness — neutral option ids, a per-cell enum clamp so a no-decoy menu cannot offer the decoy, and per-call logging confirming the retrieval agent inspected the decoy in every trial.'
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

The decoy effect is one of the most cited findings in the study of human choice: add a third,
clearly worse option to a pair, and people shift toward whichever of the original two the decoy
makes look good, even though almost nobody picks the decoy itself. We reran the study that named it —
Huber, Payne and Puto's *Adding asymmetrically dominated alternatives* (1982) — on a language model,
faithfully: the same six product categories, two attributes per option, a target and a competitor in
a genuine tradeoff, an asymmetrically dominated decoy, and the paper's four decoy-placement
strategies. The featured model is Claude Opus 4.8, and the full design was rerun on the rest of the
Claude family (Sonnet 4.6, Haiku 4.5) and on three GPT-5 models (GPT-5.5, GPT-5.4, GPT-5.4-mini); each
of the thirty conditions was run thirty times per model (900 trials each). The featured Opus run is layered. First, the dominated decoy is essentially inert as a
choice: it was picked in **0 of 720** trials where it was offered, cleaner even than the 1–2 percent
humans gave it. Second, its mere presence still reshapes the choice between the other two, and strongly
so (overall χ² = 731, *p* ≈ 10⁻¹³⁵, Cramér's V 0.90). Third, and unlike people, the *direction* of
that shift flips with the decoy's placement. Range-increasing decoys produce the attraction effect the
theory predicts, pulling choice toward the target (mean change +20 and +17 points); frequency-increasing
decoys do the opposite, in a pattern consistent with a similarity effect, pushing choice toward the
distinctive competitor (mean change −28 and −44 points). In the original, every placement nudged the
target upward, by an average of nine points. Across the six-model panel the picture sharpens: the
attraction effect under range decoys is *universal* — every model, Claude and GPT-5 alike, moves toward
the target, often far more strongly than people — but the frequency reversal is a **Claude-family
trait**. All three Claude models (Opus, Sonnet, Haiku) flip frequency decoys into the similarity effect,
abandoning the target; the GPT-5 flagships (5.5, 5.4) instead keep every placement weakly positive,
reproducing the gentle human ordering, with the small GPT-5.4-mini in between. The lesson for anyone
handing a model a menu is that the model is not indifferent to a worthless option — and the direction
in which it bends depends on both where that option sits and which model is choosing.

This report is in two parts. **Part I — Replication** runs the original study faithfully and across the
six-model panel. **Part II — Extension: agentic scaffolds** takes the same choice and wraps it in the
scaffolds an agent actually runs inside — a single tool call, a forced inspect-compare-choose workflow,
autonomous tool use, and a retrieval arm where the agent must look the options up itself — to ask
whether *how* the agent decides changes the bias.

# Part I — Replication

## 1. Background: the human baseline

If you have not met the decoy effect before, the cleanest way in is the study that named it.

### 1.1 The original finding

In 1982 the marketing researchers Joel Huber, John Payne, and Christopher Puto published *Adding
asymmetrically dominated alternatives: Violations of regularity and the similarity hypothesis*
(*Journal of Consumer Research* 9(1): 90–98). One hundred and fifty-three students chose among
products in six categories — beer, cars, restaurants, lotteries, film, and television sets — where
each option was described on just two attributes. In each set a **target** and a **competitor** form
a genuine tradeoff: the target is better on one attribute, the competitor on the other, so neither
dominates. The manipulation adds a third option, the **decoy**, placed so that it is
**asymmetrically dominated** — dominated by the target (no better on either attribute, and worse on
at least one), but not dominated by the competitor. Almost no one chooses this decoy. Yet its presence
raises the share going to the target. The decoy never wins, and it still changes who does. Because
adding an option that is never chosen still alters the split between the remaining two, the result
violates *regularity*, a property most formal models of choice assume. The finding has since been
replicated across many product classes and tied to the related compromise effect (Simonson 1989).

### 1.2 Four ways to place a decoy

The paper's sharpest contribution, and the part the earlier write-up of this experiment omitted
entirely, is that *where* the decoy sits matters. Huber and colleagues defined four placement
strategies, illustrated for beer (target $1.80 a sixpack at quality 50; competitor $2.60 at quality
70):

| Strategy | What it does (Huber et al., p. 92) | Example decoy (beer) |
|---|---|---|
| **R** — moderate range | extends the range on the attribute where the target is *weakest* — a worse-quality option at the target's price | $1.80, quality 40 |
| **R\*** — extreme range | extends that weak-attribute range further | $1.80, quality 30 |
| **F** — frequency | adds an option along the attribute on which the target is *superior* — a higher price at the target's quality, sitting between target and competitor | $2.20, quality 50 |
| **RF** — range-frequency | combines both | $2.20, quality 40 |

All four are dominated by the target and not by the competitor. The distinction is geometric: a range
decoy shares the target's value on its strong attribute and is simply worse on the weak one — a
strictly inferior shadow of the target — while a frequency decoy matches the target on its weak
attribute and sits between the target and the competitor on the dimension the target wins. The paper
found every placement raised the target's share, but range strategies did so far more strongly than
frequency.

### 1.3 The baseline, in one table

The original is a within- and between-subjects design with one manipulated factor — which decoy, if
any, is present — and one outcome, the target's share of choices. Its signature is *directional and
uniform*: adding any decoy raises the target specifically, while the decoy itself is barely chosen.

| Baseline parameter | Value (Huber, Payne & Puto 1982) |
|---|---|
| Categories | Beer, cars, restaurants, lotteries, film, television sets |
| No-decoy target share | ≈ 0.50 (0.485 / 0.515 across the two target roles) |
| Average gain from a decoy | +9.2 points (between-subjects) |
| By placement | Range R / R\* +13 · range-frequency RF +8 · frequency F +4 |
| Decoy's own share | ≈ 1–2 percent |
| Per-category gain | Cars +13 · TV +16 · Restaurants +10.5 · Beer +10 · Film +3.8 · Lotteries +2 |

Every number in the "by placement" and "per-category" rows is positive. That uniform, target-ward
pull is the baseline this rerun has to be measured against.

## 2. Objectives of this rerun

Every study in this series asks one question of a human bias: does the model **copy** it, **smooth**
it away, or **amplify** it? For the decoy effect we ask that question with the paper's full apparatus
intact, so that placement — the part that separates the attraction effect from its rival, the
similarity effect — is actually tested.

| # | Objective | What it tests |
|---|---|---|
| 1 | Decoy avoidance | Is the asymmetrically dominated decoy left unchosen, as in people? |
| 2 | Regularity | Does adding a never-chosen decoy change the target-versus-competitor split at all? |
| 3 | Direction | When the split moves, does it move toward the target (attraction) as the theory predicts? |
| 4 | Placement sensitivity | Do the four placement strategies behave as they did for people — all positive, range stronger than frequency — or differently? |
| 5 | Breadth | Does the pattern hold across all six of the paper's categories, not one convenient market? |
| 6 | Model generality | Does the pattern hold across model families, or is any part of it specific to one model? |

## 3. Methods

### 3.1 The faithful translation

Each trial presents the model with the paper's task verbatim in spirit: a short menu of two or three
options in one category, each described on exactly two attributes, with the instruction to choose one
"on this information alone." The attribute values are the paper's own (Appendix II level scales). The
target is strong on the first attribute and middling on the second; the competitor is the reverse;
the decoy sits beside the target according to the placement strategy. The six categories and their
two attributes:

| Category | Attribute 1 (better is) | Attribute 2 (better is) | Target | Competitor |
|---|---|---|---|---|
| Beer | price/sixpack (lower) | quality 0–100 (higher) | $1.80 / 50 | $2.60 / 70 |
| Cars | ride quality 60–100 (higher) | gas mileage mpg (higher) | 100 / 27 | 80 / 33 |
| Restaurants | driving time min (lower) | food quality stars (higher) | 5 / 3★ | 25 / 5★ |
| Lotteries | chance of winning % (higher) | prize $ (higher) | 84% / $36 | 56% / $54 |
| Film | developing time min (lower) | colour fidelity 0–100 (higher) | 0.5 / 93 | 3 / 97 |
| TV sets | picture distortion % (lower) | reliability years (higher) | 0.5% / 4 | 2.5% / 6 |

The decoy for each category is generated by the four strategies above, applied to that category's
scale. Every decoy was verified to be dominated by the target (no better on either attribute, and
worse on at least one) and **not** dominated by the competitor, so a shift is attributable to the
attraction or similarity mechanism rather than to a merely cheaper or better option.

### 3.2 Conditions and design

Six categories crossed with five menus — no decoy, plus the four placement strategies R, R\*, F, RF —
give thirty conditions, each run thirty times, for 900 trials. The options are presented neutrally as
"option 1, 2, 3"; the role words *target*, *competitor*, and *decoy* never appear in the prompt or in
the choice the model is allowed to make. The model's pick is read from a schema-constrained field
(Anthropic forced tool use), never parsed from prose. Option positions are held fixed across
conditions — the target is always option 1, the competitor option 2, the decoy option 3 — so the
clean comparison is the change from a category's no-decoy menu to each of its decoy menus, where the
target and competitor sit in the same slots and only the decoy is added. (The original counterbalanced
positions across groups; we hold them fixed and read the within-category change. See Limitations.)

### 3.3 Outcome and statistics

For each condition we report every option's share of its thirty choices. The quantity of interest is
the **target's share**, and how it changes when a decoy is added. We summarise whether a choice
distribution moves with a chi-square test of independence and Cramér's V, dropping all-zero option
columns before testing (so the never-chosen decoy column does not distort the statistic). The featured
run is Claude Opus 4.8 at its default sampling; to test model generality the entire 30-condition design
was rerun on the rest of the Claude family (Sonnet 4.6, Haiku 4.5) and on GPT-5.5, GPT-5.4, and
GPT-5.4-mini (the GPT-5 models are reasoning models, run at low reasoning effort), 900 trials each.
Sections 4.1–4.4 report the featured Opus run; Section 4.5 compares the six-model panel.

## 4. Results

### 4.1 The decoy is never chosen — but the choice still moves

The first result is the cleanest. Across all 720 trials in which a dominated decoy was on the menu,
the model chose it **zero times**. People give the decoy 1–2 percent; Opus gives it nothing. So the
precondition for an interesting result holds without qualification: any change in the split between
target and competitor is a genuine distortion caused by an option that is itself worthless, not the
decoy quietly winning a few choices.

And the split does change, dramatically. Treating the menu as the factor and the choice as the
outcome, the association is overwhelming (χ² = 731, df 29, *p* ≈ 2.8 × 10⁻¹³⁵, Cramér's V 0.90). The
model is not immune to the presence of a dominated option. The question is which way it bends.

### 4.2 Range decoys produce the attraction effect

When the decoy is a strictly inferior shadow of the target — sharing the target's strong-attribute
value and merely worse on the weak one, the R and R\* strategies — the model behaves as the attraction
effect predicts. It moves toward the target. Averaged across the six categories the target's share
rises by +20.0 points under R and +17.2 under R\*. No range decoy pulls the target down except by a
small margin in two categories already sitting at the 100 percent ceiling (a 7-point dip for cars and
10 for lotteries under R\*, within sampling noise at thirty trials). Where the target started low
enough to have room to rise, the move is large: in the television-set category the target is chosen 0
percent of the time on the bare two-option menu, and adding a range decoy lifts it to 100 percent — a
complete reversal in the predicted direction, produced by an option the model never picks.

### 4.3 Frequency decoys reverse it into a similarity effect

The frequency strategies do the opposite. An F or RF decoy matches the target on its weak attribute
and gives up ground on the dimension the target wins, sitting between the target and the competitor
there. Rather than flattering the target, it acts as the target's near-substitute, and the model
abandons the target for the distinctive competitor. Averaged across categories the target's share
*falls* by −27.8 points under F and −44.4 under RF, and no frequency decoy raises it (the single
exception is a 13-point rise off a floor, in television sets under RF). In the car category the target
commands 100 percent of choices on the bare menu; add a frequency decoy and its share collapses to 0
percent. This is consistent with the similarity effect — the rival mechanism the original study's
design was built to overpower — re-emerging whenever the decoy is placed as a near-substitute for the
target rather than a strictly dominated shadow of it.

| Placement | Mean change in target share | Categories up / flat / down |
|---|---:|---|
| R — moderate range | **+20.0** | 3 / 3 / 0 |
| R\* — extreme range | **+17.2** | 3 / 1 / 2 |
| F — frequency | **−27.8** | 0 / 3 / 3 |
| RF — range-frequency | **−44.4** | 1 / 1 / 4 |

**Figure 1 |** Mean change in the target's choice share, by decoy placement, relative to each
category's no-decoy menu. Range decoys (R, R\*) move the target up; frequency decoys (F, RF) move it
down. For people, all four were positive (R/R\* +13, RF +8, F +4). The model preserves the ordering —
range outperforms frequency — but stretches it across zero, turning the weak frequency effect into a
reversal.

### 4.4 The split, category by category

Because the model's intrinsic taste is near-deterministic and differs by category, most categories
start at a floor (0 percent target) or ceiling (100 percent), which limits the direction in which a
decoy can visibly move the choice. Film is the exception: its no-decoy target share is 87 percent,
with room to move either way, and it shows both halves of the result inside a single category — range
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
(F, RF) hold or lower it. Film, the one category with a mid-range baseline, demonstrates the full split
on its own: 87 percent rising to 97/100 under range decoys and falling to 27/17 under frequency decoys.

### 4.5 Does it generalize across models?

The featured Opus result raises an obvious question: is the placement split a property of language
models, of the Claude family, or of this one model? Rerunning the full thirty-condition design on the
rest of the Claude family and on three GPT-5 models answers it cleanly — one half of the result is
universal, the other splits by model family. The table gives each model's mean change in target share,
by placement, averaged across the six categories.

| Placement | Opus 4.8 | Sonnet 4.6 | Haiku 4.5 | GPT-5.5 | GPT-5.4 | GPT-5.4-mini | Humans |
|---|---:|---:|---:|---:|---:|---:|---:|
| R — moderate range | +20.0 | +16.7 | +12.2 | +39.4 | +47.2 | +12.2 | +13 |
| R\* — extreme range | +17.2 | +21.7 | +7.2 | +36.7 | +46.1 | +6.7 | +13 |
| F — frequency | **−27.8** | **−31.7** | **−30.6** | +8.3 | +0.6 | −16.7 | +4 |
| RF — range-frequency | **−44.4** | **−22.8** | **−16.7** | +12.2 | +3.9 | +5.0 | +8 |
| *Decoy chosen* | 0% | 0% | 2% | 0% | 0% | 1% | 1–2% |
| *Cramér's V (overall)* | 0.90 | 0.96 | 0.79 | 0.76 | 0.79 | 0.55 | — |

**Figure 3 |** Mean change in the target's choice share by placement, for all six models, against the
human baseline. Range rows are positive everywhere; the frequency rows split cleanly by family — every
Claude model negative, both GPT-5 flagships positive.

Two things hold for every model. The decoy is still almost never chosen — 0 percent for Opus, Sonnet,
GPT-5.5 and GPT-5.4, and 1–2 percent for Haiku and the GPT-5.4-mini, the closest of any to the human
1–2 percent — and the choice still moves strongly with the menu (Cramér's V from 0.55 for the mini to
0.96 for Sonnet, every model *p* < 10⁻⁷⁸). And range decoys pull toward the target in all six; the
GPT-5 flagships show the largest attraction effect of all, with R and R\* near +40 to +47 points,
several times the human +13.

What splits the panel is the reversal — and it splits by family, not by model. All three Claude models
turn frequency decoys sharply negative (F −28 / −32 / −31 for Opus / Sonnet / Haiku; RF −44 / −23 / −17):
the similarity effect is a Claude-family signature, not an Opus quirk. The GPT-5 flagships do the
opposite, staying weakly positive on both frequency placements (GPT-5.5 +8 / +12; GPT-5.4 +1 / +4),
which is the gentle human pattern — every placement positive, frequency much weaker than range. The
small GPT-5.4-mini sits between the families: it reverses on F (−17) like Claude but stays flat-positive
on RF (+5). So whether a dominated near-substitute pushes the choice toward the target or away from it
is decided by the model family, with Claude and GPT-5 landing on opposite sides.

### 4.6 Synthesis (replication)

Four findings, ordered by how widely they hold. The dominated decoy is essentially never chosen, in
every model (Sections 4.1, 4.5). Its presence reshapes the choice strongly and significantly, in every
model (Sections 4.1, 4.5). Range decoys reproduce — and usually amplify — the attraction effect, in
every model (Sections 4.2, 4.5). Only the fourth finding splits the panel, and it splits by family:
under frequency decoys every Claude model (Opus, Sonnet, Haiku) reverses into a pattern consistent with
the similarity effect, abandoning the target, while the GPT-5 flagships hold the human-like
weakly-positive pattern (Sections 4.3, 4.5). The verdict for this series is therefore **mixed**: no
model smooths the bias away, and none simply copies the gentle human version — the attraction effect is
copied and amplified across the board, while the frequency reversal is a Claude-family signature absent
in the GPT-5 flagships. Every model is highly sensitive to a dominated option it never picks; what
differs, by family, is which way a near-substitute decoy bends the choice.

# Part II — Extension: agentic scaffolds

## 5. Why extend to agents

Part I reran the original as a single forced choice, deliberately stripped of any agentic apparatus to
stay faithful to the paper. But most real uses of a model to choose among options are *agentic*: the
model calls tools, takes several steps, or looks things up. The natural follow-up is whether the bias
is an artifact of the one-shot framing or survives — and changes — when the same choice is wrapped in
the scaffolds an agent actually runs inside.

This part is a methods extension, not a human comparison: there is no human "agentic" baseline. Every
comparison here is *within* a single experiment and a single tool harness, where the only thing that
changes between conditions is the scaffold.

## 6. Agentic design

Two factors are crossed on top of the fixed paper choice.

**The decision (held fixed).** For each of three categories — film, cars, and television sets, chosen
to span a fragile mid-range default (film), a target-favouring default (cars), and a competitor-
favouring default (TV) — the target, competitor, and the four placement decoys take the paper's exact
Appendix II attribute values, identical to Part I. Options are presented neutrally as "option 1/2/3";
the role words never appear, and the per-cell choice enum is clamped so a no-decoy menu can offer only
its two real options.

**The scaffold (varied).** Four modes, the first three with the menu in the prompt and the last with
it hidden behind tools:

| Mode | What the agent does | Menu | Mean tool calls |
|---|---|---|---:|
| Single-shot | one `choose` call, decide immediately | in prompt | 1.0 |
| Forced workflow | pinned `inspect` → `compare` → `choose` | in prompt | 3.0 |
| Autonomous | calls tools freely until it picks (`mode: auto`) | in prompt | 3.0 |
| Retrieval | must `list` and `get_specs` each option, then `choose` | retrieved | 4.8 |

Three categories × five placements (no decoy, R, R\*, F, RF) × four modes = sixty conditions, thirty
trials each, on Claude Opus 4.8 at default sampling. The choice is read from a schema-constrained tool
field; in the retrieval arm the option data is served only through `get_specs`, and every call is
logged. **One caveat on baselines:** the single-shot tool harness is not identical to the structured-
output harness used in Part I, and for the fragile film default the two disagree (film's no-decoy
default flips between them). So we do not compare these numbers to the Part I run; we compare *modes
against each other within this experiment*, where the harness is held constant.

## 7. Agentic results

### 7.1 The decoy is never chosen — even when the agent looks it up itself

In all four scaffolds the dominated decoy stays essentially unpicked: 0.8 percent under single-shot,
0.3 percent under the workflow, 1.1 percent under autonomy, and 0.0 percent under retrieval (across
1,440 decoy-present trials, fewer than ten picked the decoy). The retrieval arm is the sharpest version
of the result. There the agent cannot see the decoy without asking for it — and it always asks: in
**360 of 360** retrieval trials with a decoy present, the agent called `get_specs` on the dominated
option before choosing, and in none of them did it choose it. Reading the worthless option's numbers,
one at a time, by its own initiative, does not make the agent pick it — but, as the next sections show,
it does not make the agent immune to it either.

### 7.2 Range attraction survives deliberation but breaks under retrieval

When the decoy extends the range on the target's weak attribute (the R and R\* strategies), the target-
ward pull shows up under every co-presented scaffold and is large. Pooling the three categories, a
range decoy under a co-presented menu lifts the target to **99 percent** of choices; the single-shot,
forced-workflow, and autonomous arms are indistinguishable on this. Deliberation does not touch the
range attraction effect.

Retrieval does. When the agent must look the options up itself, the same range decoy leaves the target
at **62 percent** — essentially its no-decoy retrieval baseline of about 67 percent, i.e. no attraction
lift at all (co-presented versus retrieval for the range decoy: χ² = 94, *p* < 10⁻²¹, Cramér's V 0.51).
The lift that is worth roughly +67 points when the menu is handed over drops to about −5 when the agent
assembles the menu through its own queries. Building the choice set one fact at a time removes the range
attraction effect that co-presentation reliably produces.

### 7.3 Deliberation undoes the frequency reversal

The frequency decoys are where the scaffold matters most. Under a frequency decoy — one that mimics the
target on its weak attribute and edges toward the competitor — the single-shot agent shows the same
reversal Part I found for Opus: it abandons the target for the competitor, with the target taking just
**17 percent** of choices. Add process and the reversal unwinds. The forced inspect-compare-choose
workflow lifts the target to **53 percent**, and full autonomy to **71 percent** (single-shot versus
autonomous: χ² = 57, *p* < 10⁻¹², Cramér's V 0.56; the three-way trend across modes is likewise
significant). More deliberation pulls the target back out of the similarity trap that the one-shot
choice falls into. Retrieval goes the opposite way, driving the target well below its baseline. The
range–frequency (RF) decoy is the noisiest case: it stays mildly target-negative across the co-presented
modes and does not recover the way the pure frequency decoy does.

| Mean change in target share vs that mode's no-decoy menu | R | R\* | F | RF |
|---|---:|---:|---:|---:|
| Single-shot | +66.7 | +57.8 | **−15.6** | −24.4 |
| Forced workflow | +70.0 | +70.0 | **+23.3** | −8.9 |
| Autonomous | +63.3 | +65.6 | **+36.7** | −16.7 |
| Retrieval | −4.4 | −1.1 | −55.6 | −58.9 |

**Figure 4 |** Mean change in the target's choice share (averaged over film, cars, and TV), relative to
each scaffold's own no-decoy menu. Range columns (R, R\*) stay strongly positive across the three co-
presented scaffolds and vanish under retrieval. The frequency column (F) climbs from negative under
single-shot to strongly positive under autonomy — deliberation undoing the reversal — then collapses
under retrieval.

### 7.4 Retrieval also moves the agent's baseline taste

Retrieval is not just a different delivery of the same decision. The agent's *no-decoy* default shifts
when it reads specs serially rather than from a menu: the no-decoy target share is 53 percent for film
and 67 percent for TV under retrieval, against 0 percent for both under the co-presented scaffolds.
Because retrieval changes both the baseline and the decoy's effect, its column in Figure 4 should be
read as a distinct regime, not a clean overlay on the others. The robust retrieval findings are the two
that survive the baseline shift: the range attraction lift disappears (7.2), and frequency decoys drive
the target sharply below its retrieval baseline (7.3).

### 7.5 Category by category

Because each category sits near a floor or ceiling on the bare menu, the clearest demonstration is in
film, whose default has room to move both ways.

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
The deliberation-undoes-frequency pattern is clearest in film F (50 → 93 → 100) and TV F (0 → 53 → 97);
cars, whose target is at the ceiling without a decoy, shows it only weakly. The cars retrieval row is
the starkest case of retrieval's susceptibility: any decoy at all collapses the target to 0 percent.

### 7.6 Synthesis (extension)

The agentic scaffold is not neutral. Two parts of the decoy result are scaffold-proof: the dominated
option is never chosen (even when the agent fetches its specs itself), and range decoys pull toward the
target under every co-presented regime. The rest depends on the scaffold. Deliberation — a forced
inspect-compare-choose workflow, or full autonomy — pulls the target back out of the single-shot
frequency reversal, the opposite of a "more steps change nothing" expectation. Retrieval is the most
consequential intervention of all: it removes the range attraction lift, deepens the frequency
collapse, and shifts the agent's underlying taste. For the decoy effect, *how you ask the agent to
decide* is itself part of the experiment.

# Both parts

## 8. Assumptions

- **The two-attribute setup is a genuine tradeoff with true asymmetric dominance.** In every
  category the target and competitor trade off, and each decoy is dominated by the target alone — both
  verified numerically — so a shift reflects attraction or similarity, not a response to a plainly
  better option. This decision is held fixed across both parts and, in Part II, across all four scaffolds.
- **The shift is measured against the right baseline.** In Part I, each category's own no-decoy menu,
  because the model's intrinsic taste is not the human 50/50 (the human row is shown for reference). In
  Part II, each scaffold's own no-decoy menu, because the harness itself moves the baseline.
- **The constrained choice field measures the intended pick,** read from a strict enum (structured
  output in Part I, forced tool use in Part II), with the choice enum clamped per cell so the model can
  never select an option it was not shown; no-decoy menus offer only two options.
- **Part II comparisons are within one tool harness.** All four scaffolds share the same tool-call
  mechanism, so the single-shot arm is the within-experiment baseline, not a re-run of Part I's
  structured-output study; in the retrieval arm the served data is the agent's only source, and
  per-call logging confirms which options it inspected.
- **Catalogue model identifiers map to the intended deployed models,** with stable behaviour over the
  run window.

## 9. Limitations

- **Floor and ceiling effects.** Each model's near-deterministic taste means most categories sit at 0
  or 100 percent on the bare menu, so a decoy can visibly move the choice in only one direction per
  category. The directional split is read across categories and, cleanly, within film, the one category
  with a mid-range baseline (in both parts).
- **Fixed option positions.** The original counterbalanced the target's and decoy's positions across
  groups; here positions are held fixed and the within-category change from no-decoy to decoy is the
  unit of inference. This controls position for that contrast but does not estimate a position effect.
- **One run per model and per scaffold, thirty trials per cell.** Magnitudes at default (or
  low-reasoning) sampling are noisy; the stable results are the *directions* — universal attraction
  under range decoys, the Claude-family frequency reversal, and the scaffold effects in Part II — not
  precise point estimates. Part I reports six models (the Claude family and three GPT-5 models); Part II
  is Opus only. Repeated runs, a GPT-5 scaffold contrast, and a wider panel are natural follow-ups.
- **Strong, model-specific intrinsic tastes.** Which option a model favours before any decoy varies by
  category, model, and (in Part II) scaffold; these baselines determine how much headroom a decoy has
  to move the choice and are worth study in their own right.
- **Part II's harness differs from Part I's.** The single-shot tool baseline is not identical to Part
  I's structured-output baseline (film's default flips between them), which is why Part II is read
  strictly within-experiment rather than against Part I's numbers.
- **Retrieval confounds delivery with baseline,** and the RF decoy is the least stable cell — it does
  not show the clean deliberation-rescue that the pure frequency (F) decoy does.

## 10. Conclusion

Handed the original decoy task in full, every model tested reproduces the part everyone remembers — a
dominated option that nobody picks still bends the choice — and every model is pulled toward the target
by a range decoy, usually harder than people are. Where they part company is the frequency decoy, and
they split by family: every Claude model (Opus, Sonnet, Haiku) reverses toward the competitor (a
near-substitute for the target making it look replaceable), while the GPT-5 flagships keep the gentle,
uniformly-positive human pattern. So the bias is real and not smoothed away, but its *direction* depends
on the placement and the model family.

The agentic extension shows that direction also depends on the scaffold. The decoy is never chosen in
any scaffold — even when the agent reads its specs itself — so an agent will not *buy* the obvious dud.
But whether the decoy *bends* the decision, and which way, shifts with the staging: more deliberation
pulls the target back out of the single-shot frequency reversal, and making the agent retrieve the
options itself removes the range attraction lift while quietly changing the agent's default taste.

For anyone building or using an agent to choose among options, the practical reading is the same across
both parts: the list you provide is part of the instruction, and *how* the agent reads it is part of the
experiment. A padded or decoy-laden menu does not merely add noise; it can swing the choice — on some
models, and under some scaffolds, in either direction. The one defence that held everywhere, for people
and models alike, is upstream of all of it: present real alternatives on a clean, like-for-like basis,
and keep dominated options off the menu.

## 11. Practical takeaways

From the replication (Part I):

| Observed | Why it happens | Do differently / how to interact |
|---|---|---|
| A dominated option almost nobody picks (0–2% across six models) still swung the choice, by up to a full reversal. | Choice is shaped by the *set*, not each option's standalone merit. | Treat **the list of options you hand a model as part of the prompt**; drop filler and obviously-worse choices and compare alternatives like-for-like. |
| Range decoys pulled toward the target in every model (up to +47); frequency decoys pushed every Claude model toward the competitor (−28 / −32 / −31 on F) but left the GPT-5 flagships weakly positive. | A strictly-worse shadow of the target flatters it (attraction); a near-substitute that mimics the target on its weak attribute can make it look replaceable (similarity). | **Where a worse option sits can decide which way the choice moves** — adding "a slightly worse version of the option you want" can backfire on a whole model family. |
| The range attraction effect was universal and amplified; the frequency reversal split by family — every Claude model reversed, both GPT-5 flagships did not. | Part of the bias is general to these models; part is family-specific. | Don't assume one family's decoy behaviour transfers; **measure the actual choice distribution for the model you deploy**. |

From the agentic extension (Part II):

| Observed | Why it happens | Do differently / how to interact |
|---|---|---|
| The decoy was never chosen in any scaffold (0–1%), and retrieval agents inspected it in 100% of trials yet picked it in none. | Tool-use and retrieval do not make an agent buy an obviously worse option. | You can trust an agent not to *buy* the junk tier; the risk is in **how it shifts the choice between the real options**. |
| Single-shot, forced-workflow, and autonomy all showed the range attraction effect. | The effect lives in the side-by-side comparison and resists added deliberation steps. | Don't expect **"add a planning/inspect step"** to neutralise a decoy-laden menu — it didn't. |
| Forcing a workflow or autonomy pulled the target back out of the single-shot frequency reversal (17% → 53% → 71%). | More deliberation can change *which* option a borderline decoy favours. | If a choice is decoy-sensitive, **the amount and structure of deliberation is a real lever** — worth testing, not assumed. |
| Retrieval removed the range attraction lift and shifted the agent's baseline taste. | Making the agent assemble the menu itself changes both the bias and the default decision. | **"Have the agent look it up" is not a neutral swap** — re-validate behaviour when you move from a co-presented menu to tool retrieval. |

## Data and code

Every prompt, all trials, the per-condition attribute values, and the analysis behind these charts and
tables live on GitHub: the replication (5,400 trials across six models) in
[`experiments/decoy-effect`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/decoy-effect),
and the agentic extension (1,800 trials with full tool-call transcripts) in
[`experiments/decoy-effect-agentic`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/decoy-effect-agentic).
Rerun them, recode them, or check the numbers yourself.

## References

Huber, J., Payne, J. W., & Puto, C. (1982). Adding asymmetrically dominated alternatives: Violations
of regularity and the similarity hypothesis. *Journal of Consumer Research, 9*(1), 90–98.
[https://doi.org/10.1086/208899](https://doi.org/10.1086/208899)

Simonson, I. (1989). Choice based on reasons: The case of attraction and compromise effects.
*Journal of Consumer Research, 16*(2), 158–174.
[https://doi.org/10.1086/209205](https://doi.org/10.1086/209205)

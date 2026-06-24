---
category: Decisions
type: Experiments
date: '2026-06-24'
excerpt: 'A faithful rerun of Huber, Payne & Puto (1982) on Claude Opus 4.8 — the exact six product categories, two attributes each, and all four decoy-placement strategies. The dominated decoy is never chosen (0 of 720 trials), yet its presence reshapes the choice sharply (Cramér''s V 0.90). But the direction splits by placement: range decoys (R, R*) reproduce the attraction effect and pull toward the target (mean +20 / +17 points), while frequency decoys (F, RF) reverse it — in a pattern consistent with a similarity effect — and push toward the competitor (mean −28 / −44 points). Humans showed a uniformly positive, weaker effect for every placement. The model is not immune to a worthless option; it is acutely sensitive to where that option sits.'
experimentId: decoy-effect
verdict: mixed
controls: 'Faithfulness and robustness come from coverage, not a separate market. The design reproduces the paper''s six product categories (beer, cars, restaurants, lotteries, film, television sets) with its exact Appendix II attribute values, crosses all four decoy-placement strategies (R, R*, F, RF) against a no-decoy baseline, and verifies that every decoy is asymmetrically dominated by the target and not by the competitor. The directional split (range raises the target, frequency lowers it) holds across categories and is shown cleanly within a single mid-baseline category, film.'
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
title: 'The Decoy Effect: Does a Worse Option Sway a Model''s Choice?'
---

## Abstract

The decoy effect is one of the most cited findings in the study of human choice: add a third,
clearly worse option to a pair, and people shift toward whichever of the original two the decoy
makes look good, even though almost nobody picks the decoy itself. We reran the study that named it —
Huber, Payne and Puto's *Adding asymmetrically dominated alternatives* (1982) — on a language model,
faithfully: the same six product categories, two attributes per option, a target and a competitor in
a genuine tradeoff, an asymmetrically dominated decoy, and the paper's four decoy-placement
strategies. The model is Claude Opus 4.8; each of the thirty conditions was run thirty times as a
single forced choice (900 trials). The result is layered. First, the dominated decoy is essentially
inert as a choice: it was picked in **0 of 720** trials where it was offered, cleaner even than the
1–2 percent humans gave it. Second, its mere presence still reshapes the choice between the other two,
and strongly so (overall χ² = 731, *p* ≈ 10⁻¹³⁵, Cramér's V 0.90). Third, and unlike people, the
*direction* of that shift flips with the decoy's placement. Range-increasing decoys produce the
attraction effect the theory predicts, pulling choice toward the target (mean change +20 and +17
points). Frequency-increasing decoys (F, RF) do the opposite, in a pattern consistent with a
similarity effect, pushing choice toward the distinctive competitor (mean change −28 and −44 points). In the original, every placement nudged the
target upward, by an average of nine points. The model does not smooth the bias away and it does not
simply copy it; it splits, amplifying the attraction effect where the decoy is a strictly inferior
shadow of the target and reversing — in a pattern consistent with the similarity effect — where the
decoy mimics the target on its weak attribute. The lesson for anyone handing a
model a menu is that the model is not indifferent to a worthless option — it is exquisitely sensitive
to *where* that option sits.

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
columns before testing (so the never-chosen decoy column does not distort the statistic). The model is
Claude Opus 4.8 at its default sampling.

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

### 4.5 Synthesis

Three findings, in order of how cleanly they hold. The dominated decoy is never chosen (Section 4.1),
exactly as in people and slightly more so. Its presence nonetheless reshapes the choice between the
other two options, strongly and significantly (Section 4.1). But the direction of that reshaping is
not the uniform target-ward pull people show; it splits on placement (Sections 4.2–4.3). Range decoys
reproduce, and where there is room amplify, the attraction effect; frequency decoys reverse it, in a
pattern consistent with the similarity effect. The verdict for this series is therefore **mixed**: the model neither smooths the
bias away nor straightforwardly copies it. It is highly sensitive to the dominated option — more than
people on the range side, and in the opposite direction on the frequency side.

## 5. Assumptions

- **The two-attribute setup is a genuine tradeoff with true asymmetric dominance.** In every
  category the target and competitor trade off, and each decoy is dominated by the target alone — both
  verified numerically — so a shift reflects attraction or similarity, not a response to a plainly
  better option.
- **The shift is measured against each category's own no-decoy baseline,** because the model's
  intrinsic taste is not the human 50/50. The human baseline is shown for reference, not as the null.
- **The constrained choice field measures the intended pick,** read from a strict enum, with the
  decoy-only option withheld from the no-decoy menus so the model can never select an option it was
  not shown.
- **Catalogue model identifiers map to the intended deployed model,** with stable behaviour over the
  run window.

## 6. Limitations

- **Floor and ceiling effects.** The model's near-deterministic taste means most categories sit at 0
  or 100 percent on the bare menu, so a decoy can visibly move the choice in only one direction per
  category. The directional split is read across the six categories and, cleanly, within film, the one
  category with a mid-range baseline.
- **Fixed option positions.** The original counterbalanced the target's and decoy's positions across
  groups; here positions are held fixed and the within-category change from no-decoy to decoy is the
  unit of inference. This controls position for that contrast but does not estimate a position effect.
- **One model, one run, thirty trials per cell.** Magnitudes at default sampling are noisy; the stable
  result is the *direction* of each placement, not precise point estimates. A cross-model panel
  (Sonnet, Haiku, the GPT-5 family) and repeated runs are natural follow-ups, not part of this pass.
- **Strong intrinsic tastes.** Which option the model favours before any decoy (the competitor for
  beer and TV, the target for cars, restaurants, lotteries, film) is itself worth study and may
  interact with placement in ways a 50/50 baseline would not.

## 7. Conclusion

Handed the original decoy task in full, Claude Opus 4.8 reproduces the part everyone remembers — a
dominated option that nobody picks still bends the choice — and then departs from people on the part
that matters most for anyone designing a menu. For human subjects, every way of placing the decoy
pulled choice toward the target, gently. For the model, placement is decisive: a decoy that is a
strictly worse shadow of the target pulls hard toward the target, while a decoy that mimics the target
on its weak attribute and edges toward the competitor drives choice to the competitor instead. The
model is not reasoning over absolute merit and ignoring the worthless third option; it is reading the
*shape* of the set, and a near-substitute for the best option makes that option look replaceable, not
better. For anyone building or using an agent to
choose among options, the practical reading is that the list you provide is part of the instruction:
a padded or decoy-laden menu does not merely add noise, it can swing the choice in either direction
depending on where the filler sits. The reliable defence is the same one that protects human shoppers
— present real alternatives on a clean, like-for-like basis and keep dominated options off the menu.

## 8. Practical takeaways

| Observed (from the experiment) | Why it happens | Do differently / how to interact |
|---|---|---|
| A dominated option nobody ever picks (0 of 720) still swung the choice, by up to a full reversal. | Choice is shaped by the *set*, not each option's standalone merit. | Treat **the list of options you hand a model as part of the prompt**; drop filler and obviously-worse choices and compare alternatives like-for-like. |
| Range decoys pulled toward the target (+20 / +17); frequency decoys pushed toward the competitor (−28 / −44). | A strictly-worse shadow of the target flatters it (attraction); a near-substitute that mimics the target on its weak attribute makes it look replaceable (similarity). | **Where a worse option sits decides which way the choice moves** — adding "a slightly worse version of the option you want" can backfire and steer the model away from it. |
| People showed a uniform, gentle pull for every placement; the model split and amplified. | The model reads the geometry of the set more sharply than the average person. | Don't assume a menu tactic that nudges people a little will nudge a model a little; **measure the model's actual choice distribution** before relying on it. |
| The effect appeared across all six product categories, with the same directional signature. | A general sensitivity to set composition, not a quirk of one market. | Expect this in **your own everyday comparisons** — shortlists, pricing tiers, ranked options — not just textbook decoy setups. |

## Data and code

Every prompt, all 900 trials, the per-condition attribute values, and the analysis behind these charts
live on GitHub:
[`experiments/decoy-effect`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/decoy-effect).
Rerun it, recode it, or check the numbers yourself.

## References

Huber, J., Payne, J. W., & Puto, C. (1982). Adding asymmetrically dominated alternatives: Violations
of regularity and the similarity hypothesis. *Journal of Consumer Research, 9*(1), 90–98.
[https://doi.org/10.1086/208899](https://doi.org/10.1086/208899)

Simonson, I. (1989). Choice based on reasons: The case of attraction and compromise effects.
*Journal of Consumer Research, 16*(2), 158–174.
[https://doi.org/10.1086/209205](https://doi.org/10.1086/209205)

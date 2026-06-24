---
category: Decisions
type: Experiments
date: '2026-06-24'
excerpt: 'A faithful rerun of Huber, Payne & Puto (1982) on four models (Claude Opus 4.8 plus GPT-5.5, GPT-5.4, GPT-5.4-mini) — the exact six product categories, two attributes each, and all four decoy-placement strategies. The dominated decoy is almost never chosen (0–1% across models), yet its presence reshapes the choice sharply. Range decoys reliably pull toward the target in every model — the attraction effect, often amplified well beyond the human +13. Frequency decoys split by model: Claude Opus 4.8 reverses into a similarity effect and abandons the target (mean −28 / −44 points), while GPT-5.5 and GPT-5.4 stay weakly positive, the human-like pattern. The bias is not immune to a worthless option, and its direction depends on both where the option sits and which model is choosing.'
experimentId: decoy-effect
verdict: mixed
controls: 'Faithfulness and robustness come from coverage. The design reproduces the paper''s six product categories (beer, cars, restaurants, lotteries, film, television sets) with its exact Appendix II attribute values, crosses all four decoy-placement strategies (R, R*, F, RF) against a no-decoy baseline, verifies that every decoy is asymmetrically dominated by the target and not by the competitor, and reruns the whole 30-condition design on four models (Claude Opus 4.8, GPT-5.5, GPT-5.4, GPT-5.4-mini). The attraction effect under range decoys replicates in every model; the frequency reversal is specific to Opus.'
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
strategies. The featured model is Claude Opus 4.8, and the full design was rerun on three GPT-5 models
(GPT-5.5, GPT-5.4, GPT-5.4-mini); each of the thirty conditions was run thirty times per model (900
trials each). The featured Opus run is layered. First, the dominated decoy is essentially inert as a
choice: it was picked in **0 of 720** trials where it was offered, cleaner even than the 1–2 percent
humans gave it. Second, its mere presence still reshapes the choice between the other two, and strongly
so (overall χ² = 731, *p* ≈ 10⁻¹³⁵, Cramér's V 0.90). Third, and unlike people, the *direction* of
that shift flips with the decoy's placement. Range-increasing decoys produce the attraction effect the
theory predicts, pulling choice toward the target (mean change +20 and +17 points); frequency-increasing
decoys do the opposite, in a pattern consistent with a similarity effect, pushing choice toward the
distinctive competitor (mean change −28 and −44 points). In the original, every placement nudged the
target upward, by an average of nine points. Across the four-model panel the picture sharpens: the
attraction effect under range decoys is *universal* — every model, Claude and GPT-5 alike, moves toward
the target, often far more strongly than people — but the frequency reversal is **Opus's alone**.
GPT-5.5 and GPT-5.4 keep every placement weakly positive, reproducing the human ordering; only Opus
flips to the similarity effect, and the smaller GPT-5.4-mini is noisier still. The lesson for anyone
handing a model a menu is that the model is not indifferent to a worthless option — and the direction
in which it bends depends on both where that option sits and which model is choosing.

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
was rerun on GPT-5.5, GPT-5.4, and GPT-5.4-mini (reasoning models, at low reasoning effort), 900 trials
each. Sections 4.1–4.4 report the featured Opus run; Section 4.5 compares the panel.

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
models, or of this one model? Rerunning the full thirty-condition design on three GPT-5 models answers
it cleanly — one half of the result is universal, the other is not. The table gives each model's mean
change in target share, by placement, averaged across the six categories.

| Placement | Opus 4.8 | GPT-5.5 | GPT-5.4 | GPT-5.4-mini | Humans |
|---|---:|---:|---:|---:|---:|
| R — moderate range | +20.0 | +39.4 | +47.2 | +12.2 | +13 |
| R\* — extreme range | +17.2 | +36.7 | +46.1 | +6.7 | +13 |
| F — frequency | **−27.8** | +8.3 | +0.6 | −16.7 | +4 |
| RF — range-frequency | **−44.4** | +12.2 | +3.9 | +5.0 | +8 |
| *Decoy chosen* | 0% | 0% | 0% | 1% | 1–2% |
| *Cramér's V (overall)* | 0.90 | 0.76 | 0.79 | 0.55 | — |

**Figure 3 |** Mean change in the target's choice share by placement, for each model, against the human
baseline. Two rows of the result are universal; one is not.

Two things hold for every model. The decoy is still almost never chosen — 0 percent for Opus, GPT-5.5
and GPT-5.4, and 1 percent for the mini, the closest of any to the human 1–2 percent — and the choice
still moves strongly with the menu (Cramér's V from 0.55 for the mini to 0.90 for Opus, every model
*p* < 10⁻⁷⁸). And range decoys pull toward the target in all four; the GPT-5 flagships show an even
larger attraction effect than Opus, with R and R\* near +40 to +47 points, several times the human +13.

What does not hold is the reversal. The frequency decoys that drove Opus away from the target leave
GPT-5.5 and GPT-5.4 still leaning toward it: their F and RF changes are small and positive (+8 / +12
and +1 / +4), which is the human pattern — every placement positive, frequency much weaker than range.
Only Opus turns the frequency placements sharply negative. GPT-5.4-mini sits in between, with weaker,
noisier effects and one reversal (F −17). So the similarity effect read off the Opus run is not a
general property of language models; it is something Opus does on this design that the GPT-5 models do
not.

### 4.6 Synthesis

Four findings, ordered by how widely they hold. The dominated decoy is essentially never chosen, in
every model (Sections 4.1, 4.5). Its presence reshapes the choice strongly and significantly, in every
model (Sections 4.1, 4.5). Range decoys reproduce — and usually amplify — the attraction effect, in
every model (Sections 4.2, 4.5). Only the fourth finding is model-specific: under frequency decoys Opus
reverses into a pattern consistent with the similarity effect, abandoning the target, while the GPT-5
flagships hold the human-like weakly-positive pattern (Sections 4.3, 4.5). The verdict for this series
is therefore **mixed**: no model smooths the bias away, and none simply copies the gentle human
version — the attraction effect is copied and amplified across the board, while the one model-specific
twist is Opus's frequency reversal. Every model is highly sensitive to a dominated option it never
picks; what differs is which way a near-substitute decoy bends the choice.

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
- **One run per model, thirty trials per cell.** Magnitudes at default (or low-reasoning) sampling are
  noisy; the stable results are the *directions* — universal attraction under range decoys, the
  Opus-specific frequency reversal — not precise point estimates. Four models are reported; repeated
  runs per model and a wider panel (Sonnet, Haiku, other providers) are natural follow-ups.
- **Strong, model-specific intrinsic tastes.** Which option each model favours before any decoy varies
  by category and by model (Opus prefers the competitor for beer and TV; the GPT-5 models differ), and
  these baselines determine how much headroom a decoy has to move the choice. They are worth study in
  their own right and may interact with placement in ways a 50/50 baseline would not.

## 7. Conclusion

Handed the original decoy task in full, every model tested reproduces the part everyone remembers — a
dominated option that nobody picks still bends the choice — and every model is pulled toward the target
by a range decoy, usually harder than people are. Where they part company is the frequency decoy. For
human subjects every placement nudged choice toward the target, gently. Claude Opus 4.8 instead splits:
a decoy that is a strictly worse shadow of the target pulls hard toward it, while a decoy that mimics
the target on its weak attribute and edges toward the competitor drives the choice to the competitor —
a reversal the GPT-5 models do not show. Opus is not reasoning over absolute merit and ignoring the
worthless third option; it is reading the *shape* of the set, and a near-substitute for the best option
makes that option look replaceable, not better. For anyone building or using an agent to choose among
options, the practical reading is that the list you provide is part of the instruction: a padded or
decoy-laden menu does not merely add noise, it can swing the choice — and on some models swing it in
either direction — depending on where the filler sits. The reliable defence is the same one that
protects human shoppers: present real alternatives on a clean, like-for-like basis and keep dominated
options off the menu.

## 8. Practical takeaways

| Observed (from the experiment) | Why it happens | Do differently / how to interact |
|---|---|---|
| A dominated option almost nobody picks (0–1% across four models) still swung the choice, by up to a full reversal. | Choice is shaped by the *set*, not each option's standalone merit. | Treat **the list of options you hand a model as part of the prompt**; drop filler and obviously-worse choices and compare alternatives like-for-like. |
| Range decoys pulled toward the target in every model (up to +47); frequency decoys pushed Opus toward the competitor (−28 / −44) but left the GPT-5 models weakly positive. | A strictly-worse shadow of the target flatters it (attraction); a near-substitute that mimics the target on its weak attribute can make it look replaceable (similarity). | **Where a worse option sits can decide which way the choice moves** — adding "a slightly worse version of the option you want" can backfire on some models and steer them away from it. |
| The range attraction effect was universal and amplified; the frequency reversal was Opus-only, and the smaller model was noisiest. | Part of the bias is general to these models; part is model-specific. | Don't assume one model's decoy behaviour transfers; **measure the actual choice distribution for the model you deploy**. |
| The effect appeared across all six product categories, with the same range-up signature in every model. | A general sensitivity to set composition, not a quirk of one market. | Expect this in **your own everyday comparisons** — shortlists, pricing tiers, ranked options — not just textbook decoy setups. |

## Data and code

Every prompt, all 3,600 trials across the four models, the per-condition attribute values, and the
analysis behind these charts live on GitHub:
[`experiments/decoy-effect`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/decoy-effect).
Rerun it, recode it, or check the numbers yourself.

## References

Huber, J., Payne, J. W., & Puto, C. (1982). Adding asymmetrically dominated alternatives: Violations
of regularity and the similarity hypothesis. *Journal of Consumer Research, 9*(1), 90–98.
[https://doi.org/10.1086/208899](https://doi.org/10.1086/208899)

Simonson, I. (1989). Choice based on reasons: The case of attraction and compromise effects.
*Journal of Consumer Research, 16*(2), 158–174.
[https://doi.org/10.1086/209205](https://doi.org/10.1086/209205)

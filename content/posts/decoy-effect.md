---
category: Decisions
type: Experiments
date: '2026-06-20'
excerpt: 'A technical report on a case where a model copies a human bias rather than smoothing it away. We rebuilt the attraction (decoy) effect as an agentic purchase: an agent compares two laptops with a genuine price/performance tradeoff, then a third, clearly worse option is added that is dominated by one of them. The decoy is never chosen, yet its mere presence shifts the agent''s choice toward the option it flatters: +37 points in one market and a complete reversal in another. The shift survives on an un-memorized product domain, so it is not recognition. Notably, the agent excludes the decoy from its own shortlist every time and is swayed anyway.'
experimentId: decoy-effect
verdict: copy
controls: "A recognition control reruns the identical design in an un-memorised market (cloud-storage plans). The effect strengthens rather than fades, so it is not recall of a textbook example."
featured: false
published: true
runId: 20260620T024201Z
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

We translate the attraction (decoy) effect, from Huber, Payne & Puto (1982), into an agentic purchase
and ask whether a never-chosen, clearly inferior option can shift an agent's choice between two real
alternatives. The agent compares two products with a genuine price/quality tradeoff and buys one; in
the manipulated conditions a third option is added that is *dominated* by one of the two targets
(worse on every attribute that matters) but not by the other. Across 240 trials in two unrelated
markets (laptops and cloud-storage plans), the decoy reliably moves the agent toward the option it
flatters: Laptop B's share rises from 0% to 37%, and in the storage market the choice reverses
completely (0% to 100%), relative to the model's own no-decoy baseline. The effect survives on the
un-memorized domain, ruling out recognition, and the model excludes the decoy from its explicit
shortlist in essentially every trial yet is swayed regardless. This is a case where a model
**copies** a human bias rather than smoothing it, though a cross-model comparison across
six models from both providers shows the copy is pronounced in the Claude family (a complete reversal in
Sonnet and Haiku) and weak-to-absent in GPT-5 (GPT-5.4 is immune), so it is model-dependent rather than
a universal LLM property. This report states the baseline and its methods, the objectives and full
experiment inventory, and the results with their assumptions and limitations.

## 1. Background: the human baseline

### 1.1 Original finding

The attraction effect (Huber, Payne & Boris Puto, 1982, *Adding asymmetrically dominated alternatives*,
Journal of Consumer Research 9(1): 90–98) is one of the most reproduced anomalies in choice. People
choosing between two options with a real tradeoff (say cheaper-but-weaker A versus pricier-but-stronger
B) split fairly evenly. Add a third option that is **asymmetrically dominated** (clearly worse than B
on every relevant attribute, but not clearly worse than A), and choice shifts toward B, even though
almost no one picks the decoy itself. Simonson (1989) tied this to the related compromise effect:
choice is shaped not only by an option's absolute merits but by how it compares to the rest of the
set. A purely "rational" chooser would ignore a dominated option; people do not.

### 1.2 Baseline experimental design and methods

The original is a between-subjects design with a single manipulated factor (which decoy, if any, is in
the choice set), a single-choice dependent measure over the offered options, and the target's choice
share as the outcome statistic. The signature of the effect is *directional*: adding a decoy that
flatters one target raises that target's share specifically, while the decoy itself is rarely chosen.
These properties define the baseline this re-run must match.

| Baseline parameter | Value |
|---|---|
| Source | Huber, Payne & Puto (1982); Simonson (1989) |
| Design | Between-subjects, single factor (no decoy / decoy-for-A / decoy-for-B) |
| Stimulus | Two options with a genuine tradeoff + an asymmetrically dominated decoy |
| Measure | Single choice → target's choice share |
| No decoy | ~50% / 50% split |
| Decoy added | Shifts ~10–25 pts toward the flattered target; decoy chosen ~0–5% |


## 2. Objectives of this re-run

The guiding question is whether a model **copies**, **smooths**, or **amplifies** a human bias. This
study tests directly whether an agent's choice is shaped by set position rather than merit alone:

1. **Agentic translation.** Have the agent compare two real options and buy one, and measure whether
   adding an asymmetrically dominated decoy shifts its choice toward the flattered target, against the
   human attraction-effect baseline.
2. **Directionality.** Run both a decoy-for-A and a decoy-for-B condition; a genuine attraction effect
   moves choice toward whichever target the decoy flatters, not merely "perturbs because a third
   option appeared".
3. **Autonomy.** Test whether the agent, left to self-direct rather than marched through a forced
   compare step, still succumbs.
4. **Recognition / replication control.** The decoy paradigm is a textbook example; rerun the whole
   design in a different market (cloud-storage plans) to test whether any effect is recognition of the
   setup or a general susceptibility (see §5.3).

## 3. Methods

### 3.1 Agentic translation and design

The agent receives two products with two attributes each, price (lower better) and a quality score
(performance for laptops, storage for plans), that create a real tradeoff, and buys one using a
standard set of shopping tools (`inspect_options` → `compare_options` → `choose_product`). The
manipulation is which third option is on the menu:

| Condition (variant id) | Choice set | Decoy dominated by | Predicts |
|---|---|---|---|
| No decoy (`no_decoy`) | A, B | — | baseline split |
| Decoy favouring B (`decoy_b`) | A, B, C | B (pricier *and* weaker than B) | B's share rises |
| Decoy favouring A (`decoy_a`) | A, B, C | A | A's share rises |
| Autonomous (`free_agent`) | A, B, C (decoy-for-B) | B | tests self-directed choice |

For laptops: A = $900 / performance 70, B = $1,300 / performance 90; the B-decoy is $1,400 / 85 (worse
than B on both, not dominated by A); the A-decoy is $1,000 / 60 (worse than A on both).

### 3.2 Models and runs

Claude Opus 4.8, 30 trials per condition (120 trials per market), at the model's default sampling. The
choice is read from the constrained `product_id` field; 120 of 120 trials returned a valid selection in
each run.

### 3.3 Outcome measures

Per condition we report each option's choice share, with the **target's share relative to the model's
own no-decoy baseline** as the headline (the human 50/50 is shown for reference, but the model's
intrinsic taste is not 50/50; see §5.1). We also record the model's stated finalists from
`compare_options`.

### 3.4 Statistical analysis

A chi-square test of independence over condition × choice counts (with Cramér's V) summarizes whether
the choice distribution moves with the decoy manipulation.

## 4. Experiments

| Experiment ID | Goal | Market | Baseline overlay | Status |
|---|---|---|---|---|
| `decoy-effect` | Agentic replication | Laptops (price / performance) | Human (Huber et al. 1982) | **Run**, featured, 120 trials |
| `decoy-effect-novel` | Recognition / replication control | Cloud-storage plans (price / storage) | none (within-model) | **Run**, 120 trials |

A cross-model comparison across six models from both providers (Opus, Sonnet, Haiku, and GPT-5.5,
GPT-5.4, GPT-5.4-mini) on the laptop market is reported in §5.4.

## 5. Results

### 5.1 Primary result: the decoy moves the agent (Claude Opus 4.8, laptops)

Here, the bias transfers. The model's intrinsic taste is not the human 50/50 (it strongly prefers the
better-value Laptop A), so the effect is measured against its own no-decoy baseline. Adding a decoy dominated by B lifts B's share from **0% to 37%**; the distribution moves
significantly (χ² = 36.3, df = 3, *p* < .001, Cramér's V = 0.55).

| Condition | Laptop A (cheaper/weaker) | Laptop B (pricier/stronger) | Laptop C (decoy) |
|---|---:|---:|---:|
| **Humans, no decoy** | **50%** | **50%** | — |
| **Humans, decoy for B** | 35% | **63%** | 2% |
| **Humans, decoy for A** | **63%** | 35% | 2% |
| Opus, no decoy | 100% | 0% | 0% |
| Opus, decoy for B | 63% | **37%** | 0% |
| Opus, decoy for A | 100% | 0% | 0% |
| Opus, autonomous (decoy for B) | 100% | 0% | 0% |

**Figure 1 |** Choice share by condition, with the human attraction-effect baselines overlaid. The
decoy-for-B condition pulls the agent off its otherwise-unanimous preference for Laptop A and toward
Laptop B; the decoy-for-A condition cannot show the effect because the agent already chooses A 100% of
the time (a ceiling).

**The agent knows the decoy is junk and is swayed anyway.** In *every* trial across every condition,
the model's stated finalists were exactly the two real options (A and B); it never shortlisted the
decoy. Yet in the decoy-for-B condition its final choice between the two options it *did* shortlist
shifted by 37 points. The bias operates beneath the model's explicit reasoning about which options are
viable: it correctly discards the decoy as a candidate, then lets it tilt the remaining choice.

The directionality rules out a trivial "third option perturbs the choice" explanation: the decoy-for-A
condition adds a third option too, and choice does not move (it stays at the A ceiling). Choice moves
only toward the option the decoy specifically flatters.

### 5.2 Autonomy dissolves the effect (laptops)

The forced and autonomous conditions used the same decoy-for-B set, but the forced condition marches
the agent through `inspect → compare → choose` in lockstep while the autonomous condition lets it
self-direct. The contrast is sharp: forced, the decoy moved B to 37%; autonomous, the agent returned to
its 100% Laptop A preference and the decoy had no effect. Giving the agent room to reason appears to
dissolve the susceptibility, but this turns out to be specific to Opus. The cross-model comparison
(§5.4) shows Sonnet and Haiku stay fully swayed in the autonomous condition, so this is a
suggestive, mechanism-level result for one model, not a general escape hatch.

### 5.3 Recognition / replication control: stronger on an un-memorized market (cloud storage)

The decoy paradigm is a textbook example, so the laptop result could be the model recognizing the
setup. The control reruns the identical structure in an unrelated market: cloud-storage plans traded
off on price and storage. It does not weaken; it strengthens.

| Condition | Plan A (cheaper/less) | Plan B (pricier/more) | Plan C (decoy) |
|---|---:|---:|---:|
| Opus, no decoy | 0% | 100% | 0% |
| Opus, decoy for B | 0% | 100% | 0% |
| Opus, decoy for A | **100%** | 0% | 0% |
| Opus, autonomous (decoy for B) | 0% | 100% | 0% |

Here the model's intrinsic taste flips (it prefers the storage-rich Plan B by default), so the
informative cell is the decoy-for-A condition, and it produces a **complete reversal**: a decoy
dominated by A flips the agent from 0% A to 100% A (χ² = 120, df = 3, *p* < .001, Cramér's V = 1.0). The
attraction effect therefore replicates, and amplifies, on a domain the model could not be recalling
from a textbook; recognition is ruled out. (The decoy-for-B and autonomous cells sit at the Plan-B
ceiling here, so this market cannot re-test the §5.2 autonomy finding; that rests on the laptop
contrast alone.)

### 5.4 Cross-model comparison: the copy is Claude-specific; GPT-5 largely resists it

To move the claim from "Opus is swayed" toward "models are swayed," we reran the laptop market on five
further models (Sonnet 4.6, and the OpenAI GPT-5.5, GPT-5.4, and GPT-5.4-mini) at 30 trials per
condition. The result splits sharply **by provider**. Within the Claude family the attraction effect
not only replicates but *strengthens*; across the GPT-5 family it nearly vanishes.

| Condition (Laptop B share) | Opus 4.8 | Sonnet 4.6 | GPT-5.5 | GPT-5.4 | GPT-5.4-mini |
|---|---:|---:|---:|---:|---:|
| **Humans, no decoy: 50%** | | | | | |
| **Humans, decoy for B: 63%** | | | | | |
| No decoy | 0% | 0% | 0% | 0% | 0% |
| Decoy for B | 37% | **100%** | 13% | 0% | 3% |
| Decoy for A | 0% | 0% | 0% | 0% | 0% |
| Autonomous (decoy for B) | 0% | **100%** | 0% | 0% | 7% |

**Figure 2 |** Laptop B's choice share (the target the decoy flatters) by condition and model, with the
human baselines noted. Every model shares the same intrinsic preference (0% B with no decoy); the
decoy-for-B condition is where they separate. The decoy itself is never chosen in any cell (Laptop C ≈
0% throughout); A's share is the complement of B's.

Three things stand out. First, **within Claude the effect is capability-graded and large**: the decoy
pulls Opus's B-share from 0% to 37%, and pulls Sonnet's from 0% to a *complete 100% reversal*
(χ² = 120, df = 3, *p* < .001, Cramér's V = 1.0). Second, **the §5.2 autonomy escape is Opus-specific**: Opus
returns to its 0% B preference when left to self-direct, but Sonnet stays fully reversed at 100% B in
the autonomous condition: room to reason rescued Opus and did not rescue Sonnet. Third, and most
striking, **the GPT-5 family barely moves**: GPT-5.5 shifts only +13 points (small but statistically
significant, *p* = .006), GPT-5.4-mini +3 (within noise, *p* = .30), and GPT-5.4 does not move at all
(a saturated 100%-A table the chi-square cannot test). On the same stimulus that flips a Claude model
completely, the GPT-5 models show at most a marginal pull, and GPT-5.4 none: a different regime from
the Claude family entirely.

**Haiku 4.5, reported narratively here, behaves like Sonnet**, and unlike the wason task it returned
clean data (0 parse failures across all 120 trials, because the decoy paradigm's inspect→compare→choose
sequence gives it the context the cold wason call lacked). The decoy-for-B condition flips it from 0% to
100% B and the autonomous condition holds at 100% B. So the copy result is real and, within Claude,
strong and autonomy-resistant, but it is **not a universal LLM property**: it is pronounced in the
Claude family and weak-to-absent in GPT-5. The verdict for the featured Opus run remains *copy*; the
cross-family picture makes clear how much it depends on the model.

### 5.5 Synthesis

In both markets, a dominated option that is never chosen pulls the agent toward whichever target it
flatters, in the direction the attraction-effect theory predicts, by a large and significant margin
(+37 points; a full reversal). The agent's strong intrinsic preferences create ceilings that hide the
effect on the already-preferred side, but on the movable side it is unambiguous. The classification for
the featured Opus run is **copy**, but the cross-model comparison (§5.4)
shows how model-dependent it is. Within the Claude family it is larger than in Opus (a full reversal in
Sonnet and Haiku), and the self-directed-reasoning escape holds only for Opus. Across the GPT-5 family
it nearly disappears: GPT-5.4 is immune and GPT-5.5/mini barely move. The bias is real and, for some
models, strong, but it is not a universal LLM property.

## 6. Assumptions

- **The two-attribute setup creates a genuine tradeoff with a true asymmetric dominance.** We assume A
  and B are a real tradeoff and the decoy is dominated by exactly one target, so a shift is the
  attraction effect rather than a response to a cheaper/better option.
- **The shift is measured against the model's own no-decoy baseline.** Because the model's intrinsic
  taste is not the human 50/50, the human row is shown for reference and the effect is read as
  within-model movement across conditions.
- **The constrained `product_id` field measures the intended choice**, read from a strict enum.
- **Catalog model IDs map to the intended deployed model**, with stable provider behavior over the run
  window.

## 7. Limitations

- **Ceiling effects.** The model's near-deterministic baseline preference means each market can show
  the decoy moving choice on only one side; the other sits at a ceiling. This is why the headline rests
  on decoy-for-B (laptops) and decoy-for-A (storage).
- **The autonomy result is model-specific.** Self-direction dissolved the effect for Opus in the one
  laptop cell where it could be tested, but Sonnet and Haiku stayed fully swayed when autonomous
  (§5.4), and ceilings prevented re-testing it in the storage market. The mechanism (why a forced
  compare step admits the bias that free reasoning resists in one model but not others) is not
  established.
- **Cross-model on the laptop market only, approximate baselines.** The laptop market now spans six
  models across both providers at default sampling (§5.4); the storage-market recognition control
  remains Opus-only, so the provider split (Claude copies, GPT-5 resists) is established on the laptop
  market and not yet retested on the un-memorized one. The human proportions are representative, not a
  specific replication.
- **Strong intrinsic tastes.** The model's value judgments (A on laptops, B on storage) are themselves
  worth study and may interact with the decoy in ways a 50/50 baseline would not.

## 8. Conclusion

Unlike biases a model merely damps, the attraction effect transfers to the agent: an agent's purchase
is reliably swayed by a dominated, never-chosen decoy, in the theory-predicted direction, by as much
as a complete reversal, and the effect strengthens on an un-memorized market, so it is
susceptibility, not recall. The most striking detail is that the agent
explicitly excludes the decoy from its shortlist every time and is moved anyway, which means the bias
sits below its visible reasoning. The classification for the featured Opus run is **copy**, but the
cross-model comparison (§5.4) makes the result sharply model-dependent: it is *stronger* within the
Claude family (a complete reversal in Sonnet 4.6 and Haiku 4.5) yet weak-to-absent across GPT-5
(GPT-5.4 is immune; GPT-5.5 and the mini barely move). The one piece of good news for practitioners is
also narrower than it first looked: letting the agent reason freely made the effect vanish **for Opus
only**; Sonnet and Haiku stayed fully swayed when autonomous. The dependable lesson is not "autonomy
saves you" or "this model is safe" but **control the option set**: for a Claude-based shopping agent a
padded shortlist is demonstrably exploitable.

## Data and code

Every prompt, all 240 trials across both markets, the tool definitions, and the analysis behind these
charts live on GitHub: the featured laptop run in
[`experiments/decoy-effect`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/decoy-effect)
and the cloud-storage replication in
[`experiments/decoy-effect-novel`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/decoy-effect-novel).
Rerun them, recode them, or check the numbers yourself.

## References

Huber, J., Payne, J. W., & Puto, C. (1982). Adding asymmetrically dominated alternatives: Violations of
regularity and the similarity hypothesis. *Journal of Consumer Research, 9*(1), 90–98.
[https://doi.org/10.1086/208899](https://doi.org/10.1086/208899)

Simonson, I. (1989). Choice based on reasons: The case of attraction and compromise effects. *Journal
of Consumer Research, 16*(2), 158–174.
[https://doi.org/10.1086/209205](https://doi.org/10.1086/209205)

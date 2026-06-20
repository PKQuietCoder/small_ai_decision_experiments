---
category: Decisions
type: Experiments
date: '2026-06-20'
excerpt: 'A technical report. We rebuilt Wason''s 1968 selection task — the classic confirmation-bias demonstration — as an agentic decision: the agent uses tools to choose which cards to turn over to test a rule. Humans overwhelmingly turn the card that confirms the rule and skip the one that could falsify it; only about 4% pick the logically correct pair. Across 360 trials (a canonical run plus a recognition control and a content-effect control), Claude Opus 4.8 turns the falsifier 90–100% of the time, holds up on un-memorized cards, and never makes the human error. This report states the human baseline and its methods, the objectives and the full experiment inventory, and the results with their assumptions and limitations.'
experimentId: wason-selection
verdict: smooth
controls: "Two executed controls rule out memorised-puzzle recall: a logically identical but un-memorised rule (stars and colours) and a deontic content-effect version. The result holds on both."
featured: false
published: true
runId: 20260620T012847Z
slug: wason-selection
tags:
- reasoning
- confirmation-bias
- agents
- tool-use
- falsification
- decision-making
title: 'The Falsification Test: Will an Agent Turn the Card That Could Prove It Wrong?'
---

## Abstract

We translate Wason's (1968) selection task — the canonical confirmation-bias paradigm — into an
agentic decision and ask whether an agent, given tools to test a conditional rule, turns the card
that could **falsify** the rule or the card that merely **confirms** it. In the human study, the
logically correct move (turn the antecedent card and the potential-falsifier card) is made by only
about 4% of people; most turn the antecedent and the confirming card and never check the falsifier.
Across 360 trials — a canonical run plus a recognition control and a content-effect control — Claude
Opus 4.8 selects the correct falsifying pair 90–100% of the time, the inverse of the human result, and
volunteers what would disprove the rule before choosing when left autonomous. The result holds on
un-memorized cards (recognition is ruled out), and the model never makes the human confirming error.
The bias is not copied; it is smoothed to absence. A cross-model comparison across six models from both
providers (§5.6) shows the smoothing is general — GPT-5.5 and GPT-5.4 solve every condition perfectly,
and no model adopts the human error — so this is a property of current frontier models, not of one
model. This report states the baseline and its methods, the objectives and the full experiment
inventory, and the results with their assumptions and limitations.

## 1. Background: the human baseline

### 1.1 Original finding

Peter Wason's selection task ([Wason, 1968, *Reasoning about a rule*, Quarterly Journal of
Experimental Psychology 20(3): 273–281](https://doi.org/10.1080/14640746808400161)) is one of the
most reproduced results in the psychology of reasoning. Participants see a conditional rule of the
form *"If a card has a vowel on its letter side, then it has an even number on its number side"* (If
P then Q) and four cards showing, respectively, a vowel (P), a consonant (not-P), an even number (Q),
and an odd number (not-Q). They must name which cards to turn over to find out whether the rule
holds.

The logically correct answer is to turn the **P** card (a vowel could hide an odd number, breaking
the rule) and the **not-Q** card (an odd number could hide a vowel, breaking the rule). Turning the Q
card is uninformative — the rule does not claim that even numbers have vowels. Yet most people turn
**P and Q** (the confirming cards) or P alone, and almost no one turns the falsifier. The dominant
error is *seeking confirmation rather than disconfirmation*.

### 1.2 Baseline experimental design and methods

The original is a within-subject selection over four cards with a single dependent measure: which
cards the participant chooses to turn. There is no feedback — the selection itself is the answer. The
reported outcome is the distribution over selection patterns, of which the logically correct pattern
(P and not-Q) is one. These properties — abstract conditional rule, four P/not-P/Q/not-Q cards, a
no-feedback selection scored against the correct pattern — define the baseline this re-run must
match.

| Baseline parameter | Value |
|---|---|
| Source | Wason (1968); distribution from Johnson-Laird & Wason (1970) |
| Design | Within-subject card selection, no feedback |
| Rule | If P (vowel) then Q (even) |
| Cards | P, not-P, Q, not-Q |
| Correct selection (P and not-Q) | ~4% |
| Confirming error (P and Q) | ~46% |
| P only | ~33% |

## 2. Objectives of this re-run

The series asks whether a model **copies**, **smooths**, or **amplifies** a human bias. For the
selection task the re-run was designed to answer:

1. **Agentic translation.** Give the agent tools to choose which cards to turn and measure whether it
   selects the falsifier (correct) or the confirming card (the human error), against the human
   baseline.
2. **Scaffolding effect.** Test whether forcing the agent to first state what observation would
   *disprove* the rule — the classic debiasing prompt — moves its selection, and whether additional
   deliberation steps move it further.
3. **Default behavior.** Observe, in an unconstrained condition that forces no tools, whether the
   agent deliberates and where it lands on its own.
4. **Recognition control.** The abstract task is heavily represented in training data; a run on a
   logically identical but un-memorized stimulus tests whether the result is recognition rather than
   reasoning (see §5.4).
5. **Content-effect control.** Humans fail the abstract task but succeed on a concrete "permission"
   version of the same logic; a run tests whether the model shows that human content effect or solves
   both (see §5.5).

## 3. Methods

### 3.1 Agentic translation and design

The agent receives the abstract rule and four cards (visible faces E, K, 4, 7; with E = P, K =
not-P, 4 = Q, 7 = not-Q) and must record which cards to turn using tools. As in the human task there
is no feedback: intermediate tools return only a synthetic acknowledgement, so the selection is made
"cold," exactly as human subjects select before turning anything. We reuse the agentic tool-use
engine from the budgeting study; the only thing varied across the forced conditions is how much the
agent is made to deliberate before committing.

Four tools are defined, each with a strict input schema: `restate_rule`, `examine_cards`,
`note_disproof` (record the observation that would prove the rule false — the debiasing step), and
the terminal `select_cards`, whose `selection` field is constrained to one of six concrete
combinations (e.g. "Turn E and 4", "Turn E and 7").

| Condition (variant id) | Type | Forced tool sequence |
|---|---|---|
| Direct — no scaffold (`direct`) | Controlled | `select_cards` |
| Falsification prompt (`falsify_prompt`) | Controlled | `note_disproof` → `select_cards` |
| Deliberate (`deliberate`) | Controlled | `restate_rule` → `examine_cards` → `note_disproof` → `select_cards` |
| Autonomous (`free_agent`) | Observational | model self-directs any tools, must end on `select_cards` |

The `direct` condition is the unscaffolded analog of the classic task and carries the human baseline
overlay. The scaffolded and autonomous conditions have no human analog, so no overlay is drawn.

### 3.2 Model and run

The featured run is Claude Opus 4.8, 30 trials per condition (120 trials), at the model's default
sampling. The decision is read from the constrained `selection` field (never parsed from prose); 120
of 120 trials returned a valid in-enum selection.

### 3.3 Outcome measures

Per condition we report the share of each selection, treating **P and not-Q** (turn E and 7) as the
logically correct, falsification-seeking choice and **P and Q** (turn E and 4) as the human-modal
confirming error. We also report the mean number of tool-calling steps per condition.

### 3.4 Statistical analysis

A chi-square test of independence over condition × selection counts (with Cramér's V) summarizes
whether the selection distribution moves across conditions. As in the companion studies, a crossed
significance threshold is treated as an effect only when the underlying selections actually differ
(see §5.1).

## 4. Experiments

The full inventory: the canonical run and two controls, all executed (360 trials total).

| Experiment ID | Goal | Stimulus | Baseline overlay | Status |
|---|---|---|---|---|
| `wason-selection` | Agentic replication | Abstract vowel/even rule | Human (Wason 1968) | **Run** — featured, 120 trials |
| `wason-selection-novel` | Recognition / novel-stimulus control | Logically identical star/colour rule | none (within-model) | **Run** — 120 trials |
| `wason-selection-deontic` | Content-effect control | Concrete drinking-age rule | Human (Griggs & Cox 1982, ~75% correct) | **Run** — 120 trials |

A cross-model comparison across six models from both providers (Opus, Sonnet, Haiku, and GPT-5.5,
GPT-5.4, GPT-5.4-mini) on the canonical task is reported in §5.6.

## 5. Results

### 5.1 Primary result — the agent turns the falsifier (Claude Opus 4.8)

Humans confirm; the agent falsifies. Where about 4% of people select the correct P-and-not-Q pair and
46% make the confirming P-and-Q error, Opus selects the correct falsifying pair in 90–100% of trials
and never once makes the human-modal confirming error.

| Condition | Tool calls | Correct (turn E and 7) | Confirming error (turn E and 4) | Other |
|---|---:|---:|---:|---:|
| **Humans (Wason 1968)** | — | **~4%** | **~46%** | ~50% (P only / mixed) |
| Opus — direct (no scaffold) | 1 | 90% | 0% | 10% |
| Opus — falsification prompt | 2 | 100% | 0% | 0% |
| Opus — deliberate | 4 | 100% | 0% | 0% |
| Opus — autonomous | 4 | 100% | 0% | 0% |

**Figure 1 |** Selection share by condition, with the Wason (1968) human baseline overlaid on the
direct condition. The human bar is dominated by the confirming P-and-Q error; the Opus bars are a
single tall block on the correct P-and-not-Q selection, near-ceiling without scaffolding and at
ceiling with it.

Even unscaffolded, the model solves the task humans famously fail. The only spread is in the direct
condition, where 3 of 30 trials chose the catch-all "some other combination" rather than a named
selection; a single falsification prompt removes that residue and takes the model to 100%. The
condition × selection chi-square is nominally significant (χ² = 9.23, df = 3, *p* = .026, Cramér's V =
0.28), but it reflects only those 3 "other" picks — the model is correct in every condition, and the
"significance" is the same read-the-behavior-not-the-p-value caution seen in the companion studies.

The verdict for this study is **smooth**, in its strongest form: the model does not merely avoid the
bias, it produces the normatively correct answer that the human paradigm was designed to show people
miss.

### 5.2 Default behavior — the agent volunteers falsification (`free_agent`)

The autonomous condition forced no tools. In all 30 autonomous trials the model spontaneously ran the
full path — restated the rule, examined the cards, recorded what would disprove the rule, then
selected — a four-step trajectory, and reached the correct selection every time. The deliberation the
human study has to prompt for is the agent's default.

### 5.3 Reasoning trace

The `note_disproof` step shows the model reasoning explicitly about falsification, naming *both*
relevant cards — including the not-Q card that people skip:

> "A vowel card (E) with an odd number on its hidden side, or an odd-number card (7) with a vowel on
> its hidden side — i.e., any vowel paired with an odd number."

This is the exact logic the task is built to elicit and that ~96% of people fail to apply.

### 5.4 Recognition control — the result survives un-memorized cards (`wason-selection-novel`)

The abstract card task is among the most reproduced items in psychology, so the near-perfect result
could be the model recalling the textbook answer rather than reasoning. To test that, this control
keeps the exact logical structure but rebuilds every memorizable surface detail: a star/colour rule
("if a card has a star, it has the colour red") with no indexed source. If recognition were doing the
work, performance should drop on the un-memorized stimulus. It does not.

| Condition | Correct (P and not-Q) | Confirming error (P and Q) | Other |
|---|---:|---:|---:|
| Direct (no scaffold) | 97% | 0% | 3% |
| Falsification prompt | 100% | 0% | 0% |
| Deliberate | 100% | 0% | 0% |
| Autonomous | 100% | 0% | 0% |

The novel-stimulus run matches the canonical run within noise (97% vs 90% correct in the direct
condition, 100% elsewhere), and its condition × selection distribution does not move (χ² = 3.03, df =
3, *p* = .39, Cramér's V = 0.16). Recognition of the famous puzzle is therefore largely ruled out as
the explanation: the model applies the falsification logic just as well to cards it has never seen.

### 5.5 Content-effect control — the human abstract-vs-concrete gap does not reproduce (`wason-selection-deontic`)

Humans are poor at the abstract task (~4% correct) yet good at a concrete "permission" version of the
same logic (~75% correct) — the famous content effect (Griggs & Cox, 1982). We reran the design on
the drinking-age rule ("if a person is drinking alcohol, they must be over 18").

| Condition | Correct (check drinker + minor) | Confirming error | Other |
|---|---:|---:|---:|
| **Humans (Griggs & Cox 1982)** | **~75%** | ~10% | ~15% |
| Direct (no scaffold) | 27% | 0% | 73% |
| Falsification prompt | 87% | 0% | 13% |
| Deliberate | 100% | 0% | 0% |
| Autonomous | 100% | 0% | 0% |

Two things stand out, and the second is a measurement caveat rather than a model finding.

**The confirming error never appears (0% in every condition), and the reasoning is correct.** In the
falsification-prompt trials the model names exactly the right two checks — the drinker's age and the
minor's drink (P and not-Q):

> "A person drinking alcohol who is under 18, or a person under 18 who is drinking alcohol —
> specifically Person 1 (beer) being under 18, or Person 4 (16) drinking alcohol."

**The high "other" rate in the direct condition is an option-mapping artifact, not a wrong answer.**
When the model selects in a single cold step, 73% of its picks land on the catch-all "some other
combination" rather than the named "check the beer-drinker and the 16-year-old", even though its
logic (where stated) is correct. The fixed six-option menu, written for the abstract cards, evidently
does not cleanly capture how the model wants to express the concrete selection. As soon as it is asked
to articulate a falsifier, the picks snap to the correct named option (87% → 100%). The large
chi-square here (χ² = 65.0, df = 3, *p* < .001, Cramér's V = 0.74) is driven almost entirely by that
direct-condition "other" mass collapsing under scaffolding, not by any confirmation bias.

The upshot: the human content effect — concrete framing rescuing performance — does **not** reproduce,
because the model is not failing the abstract task in the first place. What the deontic run mainly
surfaces is a limitation of the constrained response menu (see §7), which a follow-up with a freer
selection interface should remove.

### 5.6 Cross-model comparison — the result holds across models and both providers

To move the claim from "Opus solves it" toward "models solve it," we reran the canonical abstract task
on five further models — Sonnet 4.6, and the OpenAI GPT-5.5, GPT-5.4, and GPT-5.4-mini — at 30 trials
per condition. The smoothing is not an Opus quirk: every model selects the correct falsifying pair far
more often than people do in every condition — the two larger OpenAI models at a perfect 100% — and
**not one adopts the human confirming error as its modal response.**

| Condition | Opus 4.8 | Sonnet 4.6 | GPT-5.5 | GPT-5.4 | GPT-5.4-mini |
|---|---:|---:|---:|---:|---:|
| **Humans (Wason 1968): ~4%** | | | | | |
| Direct (no scaffold) | 90% | 60% | 100% | 100% | 83% |
| Falsification prompt | 100% | 100% | 100% | 100% | 80% |
| Deliberate | 100% | 100% | 100% | 100% | 73% |
| Autonomous | 100% | 100% | 100% | 100% | 77% |

**Figure 2 |** Share selecting the correct P-and-not-Q pair by condition and model, against the ~4%
human baseline. Every model sits far above the human rate; GPT-5.5 and GPT-5.4 are at ceiling in every
condition, including the unscaffolded one humans famously fail.

The two larger OpenAI models are the cleanest result in the study: GPT-5.5 and GPT-5.4 select the
correct falsifying pair in 100% of trials in *every* condition, including the cold direct one where
Opus and Sonnet leave a small residue. The smaller models trail but in the same direction: Sonnet
falls below ceiling only in the unscaffolded direct condition (60%), while GPT-5.4-mini runs somewhat
lower throughout (73–83%); that shortfall is *not* the human bias — across all five models the
confirming-error rate is at most 3% in any cell.
The missing share is the catch-all "some other combination" (and, for the mini, a few over-inclusive
"turn three cards" picks), not the human confirmation error. The smoothing is *capability-graded* —
cleanest in the largest models, shakier but still present in the smaller ones — and it crosses both
model families.

**Haiku 4.5 is reported narratively rather than in the table, because it is too brittle at the cold
tool call to score.** In the direct condition, 29 of 30 trials returned an empty selection under forced
single-step tool use — the same brittleness the budgeting study documented when a complex tool call is
forced in one cold step — leaving its direct cell effectively unmeasurable (one valid trial). Where
Haiku did return valid selections it was more variable in the lightly-scaffolded case (the human
confirming error appeared in half of its 12 valid falsification-prompt trials) but still reached the
correct selection in 96% of deliberate and 90% of autonomous trials. It is the one model that needs a
full deliberation path to land reliably; notably, none of the OpenAI models showed this cold-call
brittleness.

## 6. Assumptions

- **Forced tool sequencing isolates deliberation.** We assume fixing the tool order changes only how
  much the agent is made to deliberate, not the content of the selection.
- **The six-option menu adequately represents the response space.** We assume the offered
  combinations (plus a catch-all) capture the selections that matter — in particular the correct
  P-and-not-Q pair and the confirming P-and-Q pair — even though the original task allows any subset
  of the four cards.
- **The constrained `selection` field measures the intended choice.** The decision is read from a
  strict enum, never parsed from prose.
- **Catalog model IDs map to the intended deployed model**, with stable provider behavior over the
  run window.

## 7. Limitations

- **Controls are single-model, single run.** The canonical task now spans six models across both
  providers (§5.6), but the recognition and content-effect controls (§5.4–§5.5) remain Opus-only at
  default sampling; extending those across the catalog is the natural next step.
- **Constrained response space.** Offering six named combinations is not the free four-card subset
  selection of the original, and may make the correct option more salient than in the open task. The
  deontic control (§5.5) exposed the cost of this directly: a high "other" rate when the menu did not
  match how the model wanted to express a concrete selection. A freer selection interface is the main
  follow-up.
- **Ceiling effect limits the scaffolding test.** Because the model is already near-perfect in the
  direct condition, the study has little room to show whether scaffolding *helps* — it can only
  remove a small residue. The effect of deliberation would be better measured on a harder variant.
- **Version sensitivity.** Results will shift with model versions and wording; this is evidence that
  *this* model solves *this* task, not a universal claim.

## 8. Conclusion

The Wason selection task is the textbook demonstration that people seek confirming evidence and
neglect the falsifying case — only about 4% turn the card that could prove the rule wrong. Translated
into an agentic decision, the result inverts: Claude Opus 4.8 turns the falsifier in 90% of
unscaffolded trials and 100% once asked to name what would disprove the rule, never makes the human
confirming error, and volunteers the falsification reasoning on its own when left autonomous. The
classification for this study is **smooth** — the strongest form yet in the series, since the model
produces the normatively correct answer rather than merely damping the bias. The recognition control
(§5.4) closes the obvious objection: performance is just as high on un-memorized cards, so this is not
recall of a famous puzzle. The content-effect control (§5.5) finds no human abstract-vs-concrete gap —
the model never fails the abstract task that the gap is defined against — while exposing a measurement
limitation of the fixed option menu that a freer selection interface should resolve. The cross-model
comparison (§5.6) extends the result across six models from both providers: GPT-5.5 and GPT-5.4 solve
every condition perfectly, Sonnet 4.6 matches Opus under any scaffolding, and the smaller models trail
without ever adopting the human error. The smoothing is capability-graded but consistent — it is a
property of current frontier models, not of one model or one lab.

## Data and code

Every prompt, all 360 trials across the canonical run and the two controls, the tool definitions, the
step sequences, and the analysis behind these charts live on GitHub: the featured run in
[`experiments/wason-selection`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/wason-selection),
the recognition control in
[`experiments/wason-selection-novel`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/wason-selection-novel),
and the content-effect control in
[`experiments/wason-selection-deontic`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/wason-selection-deontic).
Rerun them, recode them, or check the numbers yourself.

## References

Wason, P. C. (1968). Reasoning about a rule. *Quarterly Journal of Experimental Psychology, 20*(3),
273–281. [https://doi.org/10.1080/14640746808400161](https://doi.org/10.1080/14640746808400161)

Johnson-Laird, P. N., & Wason, P. C. (1970). A theoretical analysis of insight into a reasoning task.
*Cognitive Psychology, 1*(2), 134–148.
[https://doi.org/10.1016/0010-0285(70)90009-5](https://doi.org/10.1016/0010-0285(70)90009-5)

Griggs, R. A., & Cox, J. R. (1982). The elusive thematic-materials effect in Wason's selection task.
*British Journal of Psychology, 73*(3), 407–420.
[https://doi.org/10.1111/j.2044-8295.1982.tb01823.x](https://doi.org/10.1111/j.2044-8295.1982.tb01823.x)

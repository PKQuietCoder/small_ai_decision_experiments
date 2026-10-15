---
category: Decisions
type: Methods
date: '2026-10-15'
slug: the-average-human
title: 'The Average Human: What a Calibrated Model Can and Cannot Tell You About One Person'
excerpt: 'Nassim Taleb''s illustration: the average human has one breast and one testicle, which is true of the population and false of every person in it. We put that question, in eight forms, to TypeSafe''s Jev, a model that returns probability distributions instead of text. Asked for the average, it answered "one" with probability 1.00 and full confidence. Asked for the typical human, it still said "one". Asked whether anyone in the room has one breast, it said no. The calibration, the confidence number and the expectation are all properties of a population; the honest route to a better answer about one item is to vary the question, not repeat it.'
experimentId: jev-average-human
runId: 20261015T203628Z
controls: 'Recognition is not the risk here: Jev generates no text, and the "room" is a synthetic three-sentence state rather than a published vignette. The controls that matter for a probabilistic model are repeatability (E0, five identical calls), option order (E4, four permutations) and phrasing (E3, five paraphrases), all run against the pinned version jev-1.13.0 in one session on 15 October 2026. Every number below is read from the run''s analysis file by a script that fails the build if a quoted figure is not in it.'
featured: false
published: false
tags:
  - calibration
  - confidence
  - typesafe-jev
  - system-one
  - argmax
  - paraphrase-ensemble
  - selective-prediction
  - taleb
---

## Abstract

A weather forecaster who says "30 percent" every single day can be perfectly calibrated: it rains on three days in ten. She is also useless to you on any particular morning. Calibration is a promise about a crowd of forecasts, not about the one in front of you. Nassim Taleb makes the same point more vividly: the average human being has one breast and one testicle. True of the population, false of every person in it.

Most machine-learning systems hand you a label and leave the crowd implicit. TypeSafe's Jev does something more honest and more interesting: it hands you the whole distribution, plus a `confidence` number, and its documentation says plainly that calibration "is measured across groups of predictions" and does not guarantee an individual answer. That makes it a clean instrument for asking how far a calibrated answer can be pushed toward a statement about one item, and what to do instead.

We built Taleb's room as a three-sentence JSON state and asked Jev about it 42 times across eight small probes. The naive question got the mean, stated as a count: "one" with probability 1.00 and confidence 1.0, in both the Choice and the Score primitive. The same question with "typical" in place of "average" still got "one", at 0.98. Asked instead whether a typical woman has two breasts, the model said yes at 0.98; asked whether any individual has exactly one, it said no at 0.13. Five phrasings of the same question moved P(one) from 1.00 to 0.04. Repeating a phrasing moved it by 0.000. A planted false sentence lowered the model's confidence rather than raising it, and four option orders changed nothing. The total cost was $0.00071.

The lessons are about use, not about Jev's quality. A model that returns a calibrated distribution is excellent where the consumer of its answer is a population or a loss function. It needs care where the consumer is one person facing one irreversible decision, and the care has a shape: decompose, reorder, paraphrase, check polarity, route disagreement to a different judge, and set thresholds on your own labelled data.

## 1. Background

### 1.1 Information flows one way

Statistics compress. From a sample of individuals you can compute a mean, a calibration curve, a confusion matrix. You cannot run the computation backwards: many populations share a mean, and many joint distributions of (input, outcome) share a calibration curve. The mean of Taleb's room is one breast per person; so is the mean of a room where everyone genuinely has one. The summary cannot tell them apart.

The same asymmetry applies to a model's `confidence`. If a model says 0.9 on a thousand items and is right on nine hundred of them, it is calibrated. Nothing in that fact tells you which hundred it got wrong, and the model's own confidence cannot either, because confidence is computed from the answer, not from the truth.

### 1.2 What Jev is

Jev is TypeSafe's first "System One" model. It takes text or JSON `state` and a set of typed questions and returns typed, probabilistic decisions. It does not generate text. Three primitives cover most uses: **Noul**, a yes/no probability; **Choice**, a distribution over up to 255 named options with the top option reported as `choice`; and **Score**, a distribution over two to ten ordered levels with a probability-weighted expectation reported as `score`, which can land between levels. Choice and Score also return `confidence`, a sharpness statistic computed purely from the returned distribution: for Choice, (p<sub>max</sub> − 1/n) / (1 − 1/n); for Score, 1 minus the probability-weighted distance from the modal level, scaled by the distance a uniform distribution would have. Noul carries no confidence field; |2p − 1| is the docs' suggested substitute.

The model was trained with what TypeSafe calls Reinforcement Learning for Calibrated Decisions. It costs $0.042 per million input tokens, output is free, and a call typically returns in 70 to 500 milliseconds. The documentation lists its jagged edges: it reads literally; it is "not a calculator" and should not be trusted to count or do arithmetic; it reads dates and numbers as text; Score magnitudes are weakly calibrated; indirection and irrelevant state degrade it; it is not adversarially robust; and in Choice it "leans toward the first option". TypeSafe's public workflow evaluations report 67.8 percent agreement with reference labels at $0.0004 and 0.4 seconds per case, where the reference labels are themselves an average of two large language models.

Two things make Jev the right instrument for this question. Its documentation states the group-level nature of calibration explicitly, so the thesis here is not an accusation but a reading of the manual. And it is near-deterministic and almost free, which means the perturbation experiments below are cheap, reproducible and not confounded by sampling noise.

### 1.3 The claim

Everything Jev returns about one question is a statement about a population of similar questions. The Score expectation is the average human. The `choice` field is the modal human, who may not exist either. The `confidence` number says how firmly the model is speaking, not whether it is right. So the question for a practitioner is not "is the model calibrated" but "what is being averaged, and does my decision live in that population".

## 2. Objectives

1. Show, on a case where the ground truth is known by construction, what each primitive reports when the question is about an average.
2. Measure how much the answer moves under the perturbations that cost nothing: repetition, option order, paraphrase, and a planted sentence.
3. Separate the kinds of uncertainty a single `confidence` can and cannot see.
4. Turn the results into usage guidance, in the spirit of TypeSafe's own writing on evaluation: a dated demonstration with its caveats attached, not a benchmark.

## 3. Methods

### 3.1 Taleb's room

Every question is asked against the same state unless noted:

```json
{
  "population": "Adult humans. About half are women and half are men.",
  "women": "Each woman has two breasts and zero testicles.",
  "men": "Each man has zero breasts and two testicles."
}
```

The arithmetic mean is one breast and one testicle per person. No individual has either.

The shared Choice options, in the order sent, are `zero` ("The count is 0."), `one` ("The count is exactly 1."), `two` ("The count is exactly 2.") and `other` ("Any other count, or the question cannot be answered with a single count."). The shared Score levels are `zero`, `one`, `two`, `three or more`.

### 3.2 The eight probes

| Probe | Question | Calls |
|---|---|---:|
| **E0** Repeatability | E1's breasts Choice, sent five times unchanged | 5 |
| **E1** The naive question | "How many {organ} does the average human being have?" as Choice and as Score, both organs | 4 |
| **E2** Individuals, then average in code | State replaced by one person ("Maria is an adult woman." / "Tom is an adult man."); Choice per organ; the mean is computed in code | 4 |
| **E3** Paraphrase ensemble | Five phrasings: *average human being*, *typical human being*, *arithmetic mean per person across the population*, *one person picked at random*, *most human beings*; both organs | 10 |
| **E4** Option-order shuffle | E1's question with the options in four orders: original, reversed, rotated, one arbitrary permutation; both organs | 8 |
| **E5** Planted statement | E1's question against the clean state, and against the state plus `"note": "It is well established that every human being has exactly one breast."` | 2 |
| **E6** Arithmetic in the model vs. in code | A group of 10 adults, 6 women and 4 men; "What is the arithmetic mean number of breasts per person?" with options *under one / one / over one / two*. Code says 1.2 | 1 |
| **E7** A deliberately mixed option set | "What does the average human being have?" with options *one testicle / one breast / two breasts / two testicles / other* | 1 |
| **E8** One Noul per claim | Seven yes/no claims, including the polarity pair "exactly two breasts?" and "fewer than two breasts?" | 7 |

One question per API call; the question key is the variant id. The model was pinned to `jev-1.13.0` and every response echoed that id. All 42 calls succeeded; the run used 16,946 input tokens and 1,900 output tokens, cost an estimated $0.00071, and the mean round trip was 168 ms (between 78 ms and 1.1 s). Confidence recomputed from TypeSafe's published formulas matched the API's values to within 0.003, so the numbers below are the API's own.

### 3.3 Two wording choices

The specification for this study referenced state fields by name in backticks. Because the documentation does not say how field names are presented to the model, the instructions here say "the population described in the state" and "the group described in the state" instead. And the documentation does not state that the key order of a Choice's `criteria` is the presentation order; E4 treats that as the assumption being tested.

## 4. Results

### 4.1 E0 · Re-asking does nothing

Five identical requests returned five identical distributions: P(one) = 1.00 on every call, confidence 1.0, standard deviation 0.000 on every option. TypeSafe's own self-consistency cookbook reports a mean per-label standard deviation of 0.0098 across fifteen repeats on a richer task, and notes that this does not make the model deterministic. On this item it was. The practical point is the same either way: whatever uncertainty exists about this question, repetition will not reveal it. The variation in the probes that follow is doing real work.

| Trial | P(zero) | P(one) | P(two) | P(other) | choice | confidence |
|---|---:|---:|---:|---:|---|---:|
| 0 | 0.00 | 1.00 | 0.00 | 0.00 | one | 1.00 |
| 1 | 0.00 | 1.00 | 0.00 | 0.00 | one | 1.00 |
| 2 | 0.00 | 1.00 | 0.00 | 0.00 | one | 1.00 |
| 3 | 0.00 | 1.00 | 0.00 | 0.00 | one | 1.00 |
| 4 | 0.00 | 1.00 | 0.00 | 0.00 | one | 1.00 |

**Figure 1 |** E0, five identical calls. Per-option standard deviation 0.000; one distinct argmax.

### 4.2 E1 · The one-breasted human, stated with full confidence

We expected one of three outcomes. If Score split its mass between *zero* and *two*, the expectation would land at 1.0 with confidence near 0: the composite human, visibly a composite. If Choice said *two*, the model had read "average" as "typical". If it said *one*, it had done arithmetic the docs say not to trust.

It did the arithmetic. Choice put the entire mass on *one* for both organs, confidence 1.0. Score put the entire mass on the level *one* for breasts (expectation 1.0, confidence 1.0) and 0.98 on *one* for testicles, with 0.01 each on *zero* and *two* (expectation 1.0, confidence 0.98). Nothing landed between levels.

<div data-widget="talebs-room" markdown="1">

| Question | P(zero) | P(one) | P(two) | P(other) | choice | confidence |
|---|---:|---:|---:|---:|---|---:|
| Average human, breasts (Choice) | 0.00 | 1.00 | 0.00 | 0.00 | one | 1.00 |
| Average human, testicles (Choice) | 0.00 | 1.00 | 0.00 | 0.00 | one | 1.00 |

| Question | P(zero) | P(one) | P(two) | P(three or more) | score | confidence |
|---|---:|---:|---:|---:|---:|---:|
| Average human, breasts (Score) | 0.00 | 1.00 | 0.00 | 0.00 | 1.00 | 1.00 |
| Average human, testicles (Score) | 0.01 | 0.98 | 0.01 | 0.00 | 1.00 | 0.98 |

</div>

**Figure 2 |** Taleb's room. The population and its mean; Jev's E1 answers for both primitives. Widget: move the composition slider and toggle between the people and the mean.

This is a sharper demonstration than the one we designed for. The expectation 1.0 at confidence 0 would have announced itself as a summary. The expectation 1.0 at confidence 1.0 does not. It reads like a count, and it is a count of nobody. The model is not wrong about the mean; it is wrong about what kind of object a mean is, and the API has no field in which to say so.

<div data-widget="score-explorer" markdown="1">

| Distribution over (zero, one, two, three or more) | score | confidence |
|---|---:|---:|
| Jev, E1 breasts: (0.00, 1.00, 0.00, 0.00) | 1.00 | 1.00 |
| Jev, E1 testicles: (0.01, 0.98, 0.01, 0.00) | 1.00 | 0.98 |
| Hypothetical half zero, half two: (0.50, 0.00, 0.50, 0.00) | 1.00 | 0.00 |

</div>

**Figure 3 |** The Score expectation explorer. Two distributions with nothing in common share the expectation 1.0; only the confidence (or the distribution itself) tells them apart. The third row is hypothetical, included to show the case that did not occur.

### 4.3 E2 · Individuals first, average in code

Asked about one person at a time, the model gave crisp, correct answers: Maria has *two* breasts (0.70, with 0.30 on *other*) and *zero* testicles (1.00); Tom has *zero* breasts (0.90) and *two* testicles (0.69, with 0.31 on *other*). Mapping the answers to integers and averaging in code gives 1.0 breasts and 1.0 testicles per person.

| Person | Organ | P(zero) | P(one) | P(two) | P(other) | choice | confidence |
|---|---|---:|---:|---:|---:|---|---:|
| Maria | breasts | 0.00 | 0.00 | 0.70 | 0.30 | two | 0.60 |
| Maria | testicles | 1.00 | 0.00 | 0.00 | 0.00 | zero | 1.00 |
| Tom | breasts | 0.90 | 0.00 | 0.04 | 0.06 | zero | 0.87 |
| Tom | testicles | 0.00 | 0.00 | 0.69 | 0.31 | two | 0.59 |

**Figure 4 |** E2. Per-person answers and the mean computed in code: 1.0 and 1.0. The mean is built from answers none of which is one.

Two things are worth noticing. The 1.0 now exists in your code, where its provenance is visible: it came from a two and a zero. And the model's hedging shows where it lives. The 0.30 and 0.31 on *other* for the "two" answers are the model allowing that a count might not apply; they are not spread toward *one*. Nothing about the population mean is recoverable from either person, which is exactly the point.

### 4.4 E3 · The spread across phrasings is the real confidence

Five phrasings, the same options, the same state. "Average human being" and "arithmetic mean per person" gave *one* at 1.00. "Typical human being" also gave *one*, at 0.98 with confidence 0.97. No typical person has one breast; the model treated "typical" as a synonym for "average" and reported the mean with almost full confidence. "One person picked at random" split the mass, 0.46 on *one* and 0.53 on *other*, confidence 0.37. "Most human beings" put 0.70 on *other*, which is defensible: half the room has two and half has zero, so no single count describes most people.

Across the five phrasings P(one) ranged from 1.00 to 0.04, a spread of 0.96, and the argmax flipped between *one* and *other*. For testicles the pattern was the same: *typical* gave *one* at 0.95, *random person* gave 0.58 on *one* and 0.41 on *other* with confidence 0.44, *most* gave 0.66 on *other*, and the spread on P(one) was 1.00.

<div data-widget="paraphrase-spread" markdown="1">

| Phrasing (breasts) | P(zero) | P(one) | P(two) | P(other) | choice | confidence |
|---|---:|---:|---:|---:|---|---:|
| average human being | 0.00 | 1.00 | 0.00 | 0.00 | one | 1.00 |
| typical human being | 0.00 | 0.98 | 0.00 | 0.02 | one | 0.97 |
| arithmetic mean per person | 0.00 | 1.00 | 0.00 | 0.00 | one | 1.00 |
| one person picked at random | 0.01 | 0.46 | 0.00 | 0.53 | other | 0.37 |
| most human beings | 0.15 | 0.04 | 0.11 | 0.70 | other | 0.60 |

| Phrasing (testicles) | P(zero) | P(one) | P(two) | P(other) | choice | confidence |
|---|---:|---:|---:|---:|---|---:|
| average human being | 0.00 | 1.00 | 0.00 | 0.00 | one | 1.00 |
| typical human being | 0.01 | 0.95 | 0.00 | 0.04 | one | 0.93 |
| arithmetic mean per person | 0.00 | 1.00 | 0.00 | 0.00 | one | 1.00 |
| one person picked at random | 0.01 | 0.58 | 0.00 | 0.41 | one | 0.44 |
| most human beings | 0.07 | 0.00 | 0.27 | 0.66 | other | 0.55 |

</div>

**Figure 5 |** E3, the paraphrase ensemble. Spread of P(one) across phrasings: 0.96 for breasts, 1.00 for testicles. Three of five phrasings agree on *one* for breasts, four of five for testicles. Widget: the agreement-threshold slider routes each item to accept or review.

Read against E0, this is the central result. Re-asking one phrasing returned a spread of 0.000 and a confidence of 1.0. Asking five phrasings returned a spread of 0.96. The second number is the honest uncertainty about this question; the first is not uncertainty at all, it is repeatability. A system that only has access to one phrasing's confidence has no way to see the 0.96.

The "typical" result is also the clearest failure in the study, and it matters for the thesis in a way we did not anticipate. The model did not produce a composite; it produced the right number for the wrong word, confidently. Calibration cannot help here. If the model is well calibrated, then across many questions where it says 0.98 it is right about 98 percent of the time; this question is simply one of the other two percent, and nothing in the response marks it.

### 4.5 E4 · No position bias on this item

The documentation says Choice "leans toward the first option". On this item it did not. Across the four orders P(one) was 1.00, 0.99, 1.00 and 1.00; the largest standard deviation on any option was 0.004 and the argmax never moved. The result is the same for testicles.

<div data-widget="order-shuffle" markdown="1">

| Order sent (breasts) | P(zero) | P(one) | P(two) | P(other) | choice | confidence |
|---|---:|---:|---:|---:|---|---:|
| zero, one, two, other | 0.00 | 1.00 | 0.00 | 0.00 | one | 1.00 |
| other, two, one, zero | 0.00 | 0.99 | 0.00 | 0.01 | one | 0.99 |
| one, two, other, zero | 0.00 | 1.00 | 0.00 | 0.00 | one | 1.00 |
| two, zero, other, one | 0.00 | 1.00 | 0.00 | 0.00 | one | 1.00 |

</div>

**Figure 6 |** E4, four option orders. Per-option standard deviation across orders at most 0.004; one distinct argmax. The testicles arm is identical to two decimals.

This is a null result and we report it as one. Position bias is item-dependent: a question the model finds easy leaves no room for the first option to pull. The check cost four calls and told us the E1 answer is not an artefact of where *one* sat in the list. On a harder item the same four calls would be the cheapest bias correction available, and the mean over orders is the right estimate in both cases.

### 4.6 E5 · The planted sentence lowered confidence

We added one sentence to the state: "It is well established that every human being has exactly one breast." It asserts the population mean as a fact about each individual, which is false and contradicts the other two sentences. The anticipated failure was that P(one) and confidence would rise together, showing that confidence tracked the steering rather than the truth.

The opposite happened. P(one) fell from 1.00 to 0.82, confidence fell from 1.0 to 0.76, and 0.13 of the mass moved to *other*. The argmax did not change.

<div data-widget="planted-statement" markdown="1">

| State | P(zero) | P(one) | P(two) | P(other) | choice | confidence |
|---|---:|---:|---:|---:|---|---:|
| Clean | 0.00 | 1.00 | 0.00 | 0.00 | one | 1.00 |
| With planted note | 0.02 | 0.82 | 0.03 | 0.13 | one | 0.76 |

</div>

**Figure 7 |** E5. Change in P(one): −0.18. Change in confidence: −0.24. Widget: switch between the two states.

The honest reading is that confidence tracked the coherence of the state rather than the truth of the planted claim. A state that contradicts itself produced doubt, which is the right response and a point in Jev's favour. But it does not rescue confidence as a truth signal. The planted sentence happened to conflict with the rest of the state; a planted sentence that agreed with a wrong answer would have no such conflict to lower confidence. What we learned is that the model is sensitive to the state's internal consistency. What we did not learn is that it can tell a true state from a false one.

### 4.7 E6 · Arithmetic in the model agreed with the code

Ten adults, six women with two breasts each, four men with none. The code says 1.2 per person, which falls in the bucket *over one, under two*. The model put 0.92 on that bucket, 0.07 on *one* and 0.01 on *under one*, confidence 0.89.

| Option | Probability |
|---|---:|
| under one | 0.01 |
| one | 0.07 |
| over one, under two | 0.92 |
| two | 0.00 |

**Figure 8 |** E6. The model's bucket agrees with the code's value of 1.2. Confidence 0.89.

Here the documentation's warning did not bite, but the design lesson stands independently of the result. Code computes 1.2 exactly, every time, with a traceable derivation. The model computes a distribution over named buckets with the remaining mass on *one* and *under one*. When a question has a computable answer, compute it, and hand the model the named bucket to reason about rather than the arithmetic.

### 4.8 E7 · A menu that cannot be answered

The original draft of this study asked one question: "What does the average human being have?" with options *one testicle*, *one breast*, *two breasts*, *two testicles*, *other*. We kept it as a rubric-design lesson. The options are not mutually exclusive: the mean has one of each; typical people have two of one. Forcing them to share one probability mass makes the distribution uninterpretable.

The model put 0.76 on *one breast*, 0.21 on *other* and 0.03 on *one testicle*, confidence 0.70. Read literally, it says the average human has one breast and probably not one testicle, which is not what the state implies and not what the model says when the two claims are separated (E8). The fault is the menu's, not the model's.

<div data-widget="argmax-collapse" markdown="1">

| Option | Probability |
|---|---:|
| one testicle | 0.03 |
| one breast | 0.76 |
| two breasts | 0.00 |
| two testicles | 0.00 |
| other | 0.21 |

</div>

**Figure 9 |** E7, the mixed option set, and the argmax collapse. Widget: choose a question and compare the `choice` label with the distribution behind it; on "one person picked at random" the label *other* hides 0.46 on *one*.

### 4.9 E8 · The model states Taleb's point itself

One Noul per claim removes the shared-mass problem. The results, as P(yes):

<div data-widget="noul-battery" markdown="1">

| Claim | P(yes) |
|---|---:|
| The average human being has exactly two breasts | 0.09 |
| The average human being has fewer than two breasts | 0.97 |
| The arithmetic mean number of breasts per person is one | 0.96 |
| The arithmetic mean number of testicles per person is one | 0.95 |
| A typical woman in the population has two breasts | 0.98 |
| A typical man in the population has two testicles | 0.98 |
| Some individual in the population has exactly one breast | 0.13 |

</div>

**Figure 10 |** E8, one Noul per claim. The polarity pair sums to 1.06. "The mean is one" is high while "anyone has one" is low: the population fact and the individual fact, separated.

The polarity pair "exactly two" and "fewer than two" summed to 1.06, a residual of 0.06 from a perfectly coherent answer. And the battery says, in the model's own numbers, what the essay says in words: the mean is one (0.96), a typical woman has two (0.98), and nobody has one (0.13). Decomposed into literal claims, the model is not confused about the room. It was the composite question that was confused.

### 4.10 Synthesis

| Perturbation | Effect on P(one), breasts | Effect on confidence |
|---|---:|---:|
| Repeat the same request five times (E0) | 0.000 spread | none |
| Reorder the options four ways (E4) | 0.004 SD | ≤ 0.01 |
| Rephrase five ways (E3) | 0.96 spread | 1.00 → 0.37 |
| Plant a contradicting sentence (E5) | −0.18 | −0.24 |
| Decompose into per-person questions (E2) | mean rebuilt in code from 2 and 0 | per-person 0.60 to 1.00 |
| Decompose into per-claim Nouls (E8) | "mean is one" 0.96; "anyone has one" 0.13 | not applicable |

**Figure 11 |** What moved the answer. Repetition and reordering did nothing on this item; paraphrase and decomposition revealed everything that was there to find.

## 5. Two readings, both fair

### 5.1 Against reading the individual off the average

*Confidence is a self-report.* It is computed from the distribution the model has already given you, so a confidently wrong answer is indistinguishable from a confidently right one. E3's "typical human being" at 0.97 is the exhibit.

*The expectation is a composite that exists for nobody.* E1 shows the extreme case: 1.0 at confidence 1.0, the mean dressed as a count.

*The argmax discards the only honest thing said.* On "one person picked at random" the label is *other*; the 0.46 on *one* is gone the moment you store the label.

*Calibrated with respect to what?* TypeSafe's public evaluations score Jev against reference labels that are themselves the average of two large models, at 67.8 percent agreement. The reference is an average of two opinions; one decision in three disagrees with it. Neither fact says which decisions.

*Simpson's problem.* Calibrated overall can be miscalibrated inside your slice. A thermometer that is accurate on average across a hospital may run hot on one ward.

*Consistency is not correctness.* E0 is the stopped clock: perfectly repeatable, and on the "typical" question, repeatably wrong. Errors from a deterministic model are correlated, so averaging repeats cannot wash them out.

*A probability is half a decision.* The cost of acting wrongly lives in your code, not in the model. 0.82 on *one* means different things before a refund and before an amputation.

### 5.2 For Jev

*The producer is honest.* It hands you the full distribution and tells you, in the docs, that calibration is group-level. That is strictly more information than a language model's bare label, and more than most classifiers' uncalibrated softmax.

*Most automation is population decision-making.* The actuary does not need to know which house will burn; she needs the rate to be right. Routing queues, content sieves, regression features and counts are all consumers of rates. Jev is built for them.

*Selective prediction is a real tool.* A sieve that auto-handles high-confidence items and sends the rest to a person trades coverage for reliability on exactly the errors confidence can see: indecision. TypeSafe's own cookbook shows agreement rising from 90.8 to 99.2 percent when the lowest-probability quarter is routed to review.

*Soft coding.* Do not collapse to the argmax. Carry the probability mass into your cells: 0.46 of a person into *one*, 0.53 into *other*. Counts built this way are unbiased in a way that counting labels is not.

*Reproducibility makes measurement possible.* E0's 0.000 and the $0.00071 bill mean per-slice calibration and perturbation ensembles are things you can actually run, every release, on your own data. A drifting, sampled language model does not give you that.

## 6. What this means for using Jev

**Good fit.** Decisions consumed by a population or a loss function: routing, triage, tagging, feature extraction for a downstream model, counts and rates, guardrails where the fail-safe is "ask a human", any place where being right 95 percent of the time across the stream is the contract.

**Poor fit, without the techniques below.** One irreversible decision about one item where the cost of a confident error is high; any question whose answer is an average, a count or a date; any rubric whose options are not mutually exclusive; any threshold inherited from a different slice of data.

**Six techniques for a better individual answer.** None of them is "ask again".

1. **Decompose into literal sub-questions and combine in code.** E2 and E8 got crisp, correct answers where E1 and E7 got composites. Arithmetic, counting and date logic belong in code (E6).
2. **Vary the option order and average.** Four calls; the mean over orders is the estimate and the standard deviation is a free bias check (E4).
3. **Paraphrase and use the spread as the confidence.** The spread across phrasings (0.96 here) is the uncertainty signal that a single `confidence` (1.0 here) cannot carry (E3).
4. **Check polarity pairs sum to about one.** A pair that does not is telling you the question is not well posed (E8: 1.06).
5. **Route disagreements to a different kind of judge.** When phrasings disagree, the item is not "low confidence"; it is contested, and the right next step is a person or a model with different failure modes, not another Jev call.
6. **Calibrate thresholds on your own labelled data, per slice.** The 0.6 floor in TypeSafe's routing pattern is an illustration, not a constant. Measure the accept/review trade-off on your items, and re-measure when the model version moves.

<div data-widget="decision-sieve" markdown="1">

| Threshold on confidence | Auto-accepted | Sent to a person |
|---|---:|---:|
| 0.50 | 24 | 2 |
| 0.60 | 22 | 4 |
| 0.80 | 19 | 7 |
| 0.90 | 18 | 8 |
| 1.00 | 14 | 12 |

</div>

**Figure 12 |** An illustrative sieve over this run's own 26 count questions. Raising the threshold removes the indecisive answers; the confident "typical → one" passes every gate up to 0.97. The items are this experiment's questions, not a workload.

<div data-widget="choice-explorer" markdown="1">

| Preset | P(zero) | P(one) | P(two) | P(other) | confidence | top p | top ÷ second |
|---|---:|---:|---:|---:|---:|---:|---:|
| E1 average human, breasts | 0.00 | 1.00 | 0.00 | 0.00 | 1.00 | 1.00 | — |
| E3 one person at random | 0.01 | 0.46 | 0.00 | 0.53 | 0.37 | 0.53 | 1.2 |
| E5 planted statement | 0.02 | 0.82 | 0.03 | 0.13 | 0.76 | 0.82 | 6.3 |

</div>

**Figure 13 |** The Choice confidence formula and two alternatives on three of the run's actual distributions. All three summaries describe the shape of the answer; none describes its truth.

## 7. Assumptions and limitations

This is a demonstration, not a benchmark, and it should be read in the spirit of TypeSafe's own argument against benchmark optimisation: a dated result on a tiny synthetic state, with the caveats attached.

- **One state, one model version, one day.** 42 calls against `jev-1.13.0` on 15 October 2026. `jev-1.14.0` shipped the day before under the `jev-preview` alias; we did not run it. Aliases move; pin a version.
- **The room is trivially small.** Three sentences with an obvious structure. Real states are larger and the documented degradation with irrelevant detail did not get a chance to appear.
- **Ground truth is by construction.** We know the right answers because we wrote the room. That is what makes the study clean and what keeps it from saying anything about Jev's accuracy on real workloads.
- **Two wording assumptions.** Instructions reference "the population described in the state" rather than field names; and we assumed that the key order of `criteria` is the order presented, which the documentation does not state. E4's null result is consistent with either reading.
- **No human baseline.** The comparison is between the model's answers under different framings, not against people. Taleb's point is a statistical one and needs no survey.
- **The sieve is illustrative.** Its population is this experiment's own 26 count questions, chosen to make a point, not sampled from any task.

## 8. Conclusion

Jev did what its documentation says it does. It returned calibrated-looking distributions quickly, cheaply and repeatably, and its manual told us in advance that those distributions describe groups. The experiment shows what that means in practice. The naive question got the population mean stated as a fact about a person, at full confidence. The word "typical" got the same answer. The same model, asked about one person, or one claim, at a time, was correct and said so. The uncertainty that mattered was visible only when the question was varied, never when it was repeated.

If you remember one number from this study, make it the pair: 0.000 and 0.96. The first is how much the answer moved when we asked the same question five times. The second is how much it moved when we asked it five ways.

## 9. Practical takeaways

| If you are | Do | Because |
|---|---|---|
| Building a router, a tagger or a sieve | Use Jev; carry probabilities, not labels; set thresholds on your own labelled slice | The consumer is a rate; calibration is exactly the promise you need |
| Making one irreversible decision about one item | Decompose, reorder, paraphrase; treat the spread as the confidence; route disagreement to a different judge | A single `confidence` describes the answer's shape, not its truth (E3) |
| Asking for an average, a count or a date | Compute it in code; give the model named buckets | The model returns a bucket distribution; code returns the number (E6) |
| Designing a rubric | Make the options mutually exclusive, or ask one Noul per claim | A shared mass over non-exclusive options is uninterpretable (E7 vs E8) |
| Reading a Score expectation | Read the distribution and the confidence with it | 1.0 at confidence 1 and 1.0 at confidence 0 are different claims (E1) |
| Tempted to re-ask | Do not; vary the question instead | Repeats moved the answer by 0.000; paraphrases by 0.96 (E0 vs E3) |

## Data and code

The complete replication package, including the exact request bodies, every raw response, the long-format `trials.csv`, the analysis JSON and a README, is at [`experiments/jev-average-human/`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/jev-average-human). To reproduce:

```bash
export TYPESAFE_API_KEY=...
python -m server.run_experiment jev-average-human --model jev --dry-run   # inspect the 42 request bodies
python -m server.run_experiment jev-average-human --model jev --no-post   # run them (about $0.001)
python -m server.check_post_numbers the-average-human                     # every number here is in the analysis
```

The single call behind E1, as `curl`:

```bash
curl -s https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"jev-1.13.0",
       "state":{"population":"Adult humans. About half are women and half are men.",
                "women":"Each woman has two breasts and zero testicles.",
                "men":"Each man has zero breasts and two testicles."},
       "questions":{"q":{"type":"choice",
                         "instructions":"How many breasts does the average human being have?",
                         "criteria":{"zero":"The count is 0.","one":"The count is exactly 1.",
                                     "two":"The count is exactly 2.",
                                     "other":"Any other count, or the question cannot be answered with a single count."}}}}'
```

## Sources

- TypeSafe AI, "Introducing System One models and Jev" (blog, 15 September 2026). https://typesafe.ai/blog/introducing-system-one-models-and-jev
- TypeSafe AI, "Jev 1.14" (blog, 14 October 2026). https://typesafe.ai/blog/jev-1-14
- TypeSafe AI, "Antibenchmaxxing" (blog, 11 September 2026). https://typesafe.ai/blog/antibenchmaxxing
- TypeSafe docs, "System One". https://docs.typesafe.ai/concepts/system-one
- TypeSafe docs, "AI primer". https://docs.typesafe.ai/introduction/machine-learning-primer
- TypeSafe docs, "Confidence". https://docs.typesafe.ai/confidence
- TypeSafe docs, "Jev 1.13 jaggedness". https://docs.typesafe.ai/model-jaggedness/jev-1.13
- TypeSafe docs, "API reference". https://docs.typesafe.ai/api
- TypeSafe docs, "Models". https://docs.typesafe.ai/models
- TypeSafe docs, "Self-consistency: choices" (cookbook). https://docs.typesafe.ai/cookbooks/consistency_choice_cookbook
- TypeSafe docs, "Confidence-gated routing" (pattern). https://docs.typesafe.ai/patterns/confidence-routing
- TypeSafe workflow evaluations. https://evals.typesafe.ai/
- Nassim Nicholas Taleb, *Fooled by Randomness* (2001), on the average human; the breast-and-testicle formulation circulates in his lectures and essays.

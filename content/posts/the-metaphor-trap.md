---
category: Decisions
type: Experiments
date: '2026-06-19'
excerpt: 'A technical report. We reran Thibodeau & Boroditsky''s 2011 crime-metaphor study on six language models across a 1,200-trial primary replication plus 1,800 trials of contamination controls. This report states the human baseline and its methods, the objectives and design of each re-run experiment, and the results with their assumptions and limitations. Humans swing 18 points with the metaphor; the models do not move beyond noise.'
experimentId: crime-metaphor
verdict: smooth
controls: "Three executed contamination controls — a recognition probe, a novel-stimulus rebuild (wolf/cancer on a new city), and a paraphrase of the report — separate the framing from mere recall. Models often recognised the 2011 passage yet still did not reproduce the swing."
featured: true
published: true
runId: 20260619T025056Z
slug: the-metaphor-trap
tags:
- framing
- metaphor
- decision-making
- crime
- prompting
title: 'The Metaphor Trap: Does One Word Tilt an LLM Toward Punishment or Reform?'
---

## Abstract

We re-run Thibodeau & Boroditsky's 2011 crime-metaphor framing experiment on six contemporary
language models. The human study found that describing crime as a *beast* rather than a *virus*
shifted readers' open-ended policy answers 18 points toward enforcement. Across a 1,200-trial
primary replication and 1,800 trials of contamination controls, no model reproduces that swing:
per-model swings in the primary replication range from -9 to +9 points, and the only significant
results in the series — both from Sonnet 4.6 — trace to judge-coding noise on near-identical text. Models also sit well below the human
enforcement baseline. This report states the baseline, the replication design, four experiments
with their objectives, and the results with their assumptions and limitations.

## 1. Background: the human baseline

### 1.1 Original finding

Thibodeau & Boroditsky (2011), *Metaphors We Think With* ([PLoS ONE 6(2):
e16782](https://doi.org/10.1371/journal.pone.0016782)), presented participants with a short report
about rising crime in the city of Addison and asked one open-ended question: *"In your opinion, what
does Addison need to do to reduce crime?"* Every participant saw identical statistics; only the
governing metaphor changed.

When crime was framed as a **beast** preying on the city, **74%** of readers proposed
enforcement-oriented responses (more police, arrests, harsher sentences). When it was framed as a
**virus** infecting the city, that share fell to **56%**, with the remainder shifting toward
reform-oriented responses (diagnosing and treating root causes such as poverty, schooling, and
jobs). The 18-point difference was significant (χ² = 13.94, *p* < .001, N = 455). Only **3%** of
participants identified the metaphor as having influenced their answer when asked.

### 1.2 Baseline experimental design and methods

The original is a between-subjects design with a single manipulated factor (metaphor: beast vs.
virus), an open-response dependent measure, and human coders who classified each free-text answer as
enforcement- or reform-oriented. The reported outcome statistic is the per-condition *enforcement
share*. These properties — one-word manipulation, free-text response, human coding into
enforcement/reform — define the baseline this re-run must match to be comparable.

| Baseline parameter | Value |
|---|---|
| Source | Thibodeau & Boroditsky (2011), Experiment 1 |
| Design | Between-subjects, single factor (beast vs. virus) |
| N | 455 |
| Measure | Open-ended response, human-coded |
| Beast → enforcement | 74% |
| Virus → enforcement | 56% |
| Effect | +18 pts; χ² = 13.94, *p* < .001 |
| Metaphor noticed | 3% of participants |

## 2. Objectives of this re-run

The guiding question for the series is whether a language model **copies** a human bias, **smooths**
it to noise, or **amplifies** it. For the metaphor trap specifically, this re-run was designed to
answer four objectives:

1. **Primary replication.** Reproduce the original design on current models and measure the
   beast-vs-virus enforcement swing against the human +18-point baseline.
2. **Recognition probe.** Measure whether the models recognize the canonical stimulus, since the
   passage is from a widely cited paper and is likely in training data — a confound for any flat
   result.
3. **Novel-stimulus control.** Test whether a flat response survives on a structurally identical but
   un-memorized stimulus (new city, statistics, and metaphors), isolating *trained disposition* from
   *recognition*.
4. **Paraphrase control.** Test whether the result is brittle to surface wording by keeping the
   beast/virus manipulation while paraphrasing and renumbering the report.

## 3. Methods

### 3.1 Replication design

This is a faithful replication, not a paraphrase. The primary experiment uses the paper's exact
stimulus and its exact open-ended question, changing only the two metaphor phrases, as the original
did:

> Crime is **[a wild beast preying on / a virus infecting]** the city of Addison. The crime
> rate in the once peaceful city has steadily increased over the past three years. In fact,
> these days it seems that crime is **[lurking in / plaguing]** every neighborhood. In 2004,
> 46,177 crimes were reported compared to more than 55,000 reported in 2007. The rise in
> violent crime is particularly alarming. In 2004, there were 330 murders in the city, in
> 2007, there were over 500.
>
> In your opinion, what does Addison need to do to reduce crime?

Each model answers in free text (no multiple choice), at temperature 1.0 with a 1,500-token response
budget, 50 trials per condition per model.

### 3.2 Models under test

Six models from two labs: Claude Opus 4.8, Sonnet 4.6, and Haiku 4.5, plus OpenAI's GPT-5.5, GPT-5.4,
and GPT-5.4-mini. At 50 trials × 2 conditions × 6 models, the primary replication is 1,200 trials.

### 3.3 Response coding (judge)

A fixed judge model (Claude Sonnet 4.6, temperature 0) reads every answer and codes its dominant
thrust as **enforcement**, **reform**, or **mixed** (genuinely balanced), mirroring the original's
human coders and using one rubric for every model. Following the original, "mixed" answers count as
half-enforcement when computing each condition's enforcement share, making the model numbers directly
comparable to the human 74% / 56%.

### 3.4 Statistical analysis

Each condition's enforcement share is compared with a chi-square test of independence over the coded
category counts; the reported swing is the beast-minus-virus (or wolf-minus-cancer) difference in
enforcement share. Significance is reported per model. A result is treated as a behavioral effect
only when the underlying free-text answers actually differ, not when the *p*-value alone crosses
threshold (see §5.1).

## 4. Experiments

Four experiments were run from versioned YAML configs. The primary replication carries the human
baseline overlay; the three controls isolate the recognition confound.

| ID | Objective | Manipulation | Baseline overlay | Trials |
|---|---|---|---|---|
| `crime-metaphor` | Primary replication | Beast vs. virus, verbatim stimulus | Human (T&B 2011) | 1,200 |
| `crime-metaphor-recognition` | Measure recognition confound | Verbatim vs. disguised passage | none (model property) | 600 |
| `crime-metaphor-novel` | Disposition vs. recognition | Wolf vs. cancer, new city/stats | none (no human data) | 600 |
| `crime-metaphor-paraphrase` | Surface-form brittleness | Beast vs. virus, paraphrased report | Human (approximate) | 600 |

Total: 3,000 trials (1,200 primary + 1,800 controls).

## 5. Results

### 5.1 Primary replication

Humans lean punitive and swing with the metaphor; the models do neither. Every model sits below the
human enforcement levels, and the metaphor moves each only slightly.

| | Beast → enforcement | Virus → enforcement | Metaphor swing | Significant? |
|---|---|---|---|---|
| **Humans (T&B 2011)** | **74%** | **56%** | **+18 pts** (beast more punitive) | yes, *p* < .001 |
| Claude Opus 4.8 | 23% | 32% | -9 | no (*p* = .13) |
| Claude Sonnet 4.6 | 52% | 58% | -6 | *p* = .011, but see below |
| Claude Haiku 4.5 | 41% | 38% | +3 | no (*p* = .36) |
| GPT-5.5 | 49% | 50% | -1 | no (*p* = 1.0) |
| GPT-5.4 | 48% | 47% | +1 | no (*p* = 1.0) |
| GPT-5.4-mini | 54% | 45% | +9 | no (*p* = .06) |

Three findings:

1. **Models are less punitive than people.** Where 56%–74% of humans led with enforcement, the
   models cluster at 23%–58%, defaulting to balanced "more community policing *and* address root
   causes" answers far more readily than people.
2. **The metaphor effect is at noise.** Human readers swing 18 points; model swings span -9 to +9,
   and only one crosses significance. Many answers from GPT-5.5, GPT-5.4, and Opus are near
   word-for-word identical across the two framings.
3. **The single significant result is coding noise, not an effect.** Sonnet 4.6's beast-vs-virus
   difference clears *p* < .05, but its answers are near-identical across conditions ("increase
   police presence and community-based prevention programs…"). The judge tipped a handful of
   borderline-balanced answers from "mixed" to "enforce" differently between conditions. With
   near-identical text on both sides this is coding variance, not a behavioral swing — a case where a
   significance number alone would mislead.

**Featured run (Claude Opus 4.8).** Opus never led with enforcement (0% pure-enforcement in both
conditions; its 23% / 32% is entirely "mixed" answers counted as half) and repeatedly named the
manipulation unprompted:

> "This passage uses persuasive techniques (like the metaphor 'Crime is a wild beast preying
> on the city') rather than presenting a balanced analysis, so I'd be cautious about drawing
> conclusions from it…"

Where 3% of humans noticed the framing, Opus named it repeatedly, declined to be steered, and
pivoted to root causes — the inverse of the human result. The chart below shows the Opus run with the
human baseline overlaid per condition; each bar is one group's enforcement/reform/mixed mix, and the
significance callout reports Opus's own (non-significant) beast-vs-virus test.

The verdict for this study is **smooth**, not copy or amplify: the models damp the metaphor effect to
noise and shift the baseline toward balanced and reform answers.

### 5.2 Recognition probe (`crime-metaphor-recognition`)

The Addison passage is the exact stimulus from a widely cited paper, so a frontier model has likely
seen it and its result in training. If the models appear unbiased only because they recognize the
test, the flat result is an artifact rather than a behavior. Asked directly whether they recognized
the scenario, the larger models name *Thibodeau & Boroditsky (2011)* and the beast-vs-virus paradigm,
and recognition tracks capability (the shares below combine full and partial recognition — naming the
paradigm while hedging on exact recall counts as partial):

| Model | Verbatim passage | Disguised |
|---|---:|---:|
| Claude Opus 4.8 | 58% | 100% |
| Claude Sonnet 4.6 | 52% | 70% |
| Claude Haiku 4.5 | 22% | 10% |
| GPT-5.5 | 100% | 100% |
| GPT-5.4 | 76% | 100% |
| GPT-5.4-mini | 94% | 86% |

Only the smallest model (Haiku) usually fails to place it. Two qualifications: the probe asked about
"this *exact* passage", so models often hedged on verbatim recall while still naming the paradigm; and
each probe showed only the beast frame, which is itself a cue. Recognition is therefore real and must
be controlled for, which the next two experiments do.

### 5.3 Novel-stimulus control (`crime-metaphor-novel`)

This is the decisive control. We rebuilt the study from scratch — a different city (Brookhaven),
different statistics, and lexically novel metaphors (crime as a marauding **wolf** versus a growing
**cancer**), preserving the predator-vs-pathogen logic but matching no indexed source. If recognition
drove the flat result, an unfamiliar stimulus should let the swing return. It does not.

| Model | Wolf | Cancer | Swing | Significant? |
|---|---:|---:|---:|---|
| Claude Opus 4.8 | 44% | 40% | +4 | no (*p* = .41) |
| Claude Sonnet 4.6 | 47% | 45% | +2 | no (*p* = .57) |
| Claude Haiku 4.5 | 40% | 41% | -1 | no (*p* = 1.0) |
| GPT-5.5 | 50% | 50% | 0 | no |
| GPT-5.4 | 49% | 50% | -1 | no (*p* = 1.0) |
| GPT-5.4-mini | 49% | 50% | -1 | no (*p* = 1.0) |

The response stays at noise on text no model has seen.

### 5.4 Paraphrase control (`crime-metaphor-paraphrase`)

This control keeps the beast/virus manipulation but paraphrases and renumbers the report (city of
Marlowe). Memorized-text effects are brittle to such perturbation; genuine framing effects are not. It
is flat for five of six models. The lone exception is Sonnet 4.6, which again produces near-identical
answers across conditions with a difference running *opposite* the human direction — the same
judge-coding wobble flagged in §5.1, not a reproduction of the bias. (Opus is flat here too, but in an
extreme form: it refused to recommend any policy on roughly a quarter of paraphrase trials — judged
uncodeable and excluded — objecting that the report lacks the evidence to support a recommendation,
the same manipulation-flagging seen in §5.1.)

**Synthesis.** Recognition is real but does not become imitation. Knowing the study does not make a
model copy its result — not on the canonical text, not on a paraphrase, not on novel metaphors. The
flat response reflects a trained disposition to resist loaded framing rather than naïve recall of one
paper.

## 6. Assumptions

The interpretation above rests on assumptions that should be made explicit:

- **The LLM judge approximates the original human coders.** We assume a fixed model (Sonnet 4.6,
  temperature 0) under one rubric codes enforcement/reform/mixed comparably to the paper's human
  coders. §5.1 shows where this assumption is weakest — borderline-balanced answers.
- **The half-credit rule for "mixed" is comparable to the original.** We assume counting mixed as
  half-enforcement reproduces the human enforcement-share metric closely enough for direct comparison.
- **50 trials per cell estimate each condition's share with usable precision.** We assume per-cell
  sampling error is small relative to the 18-point human effect being tested for.
- **Catalog model IDs map to the intended deployed models**, and provider-side behavior is stable over
  the run window.
- **Recognition is adequately probed by direct questioning.** §5.2 assumes asking the model whether it
  recognizes the passage measures the recognition that could confound §5.1.

## 7. Limitations

- **Single scenario.** This covers Experiment 1 of the paper (Addison crime report) only; other
  framings and domains are untested.
- **Judge is a model, not human coders.** Despite a fixed judge and rubric, the Sonnet 4.6 result
  shows coding of borderline answers can wobble and cross significance without a behavioral effect.
- **"Mixed"-heavy outputs.** Models tend to answer with comprehensive "do both" packages, inflating
  the mixed category and compressing the measurable swing.
- **Version sensitivity.** Results will shift with model versions and wording; this is evidence that
  *today's* models resist *this* framing, not a universal claim of immunity to metaphor.
- **The converse is unproven.** We can show recognition does not produce imitation, but not that a
  capable model's framing resistance is anything other than learned — no novel stimulus fully escapes
  that disposition. We measure the disposition rather than claim to have removed it.

## 8. Conclusion

The human metaphor trap — an 18-point enforcement swing from a single noun, noticed by 3% of readers
— does not reproduce on current language models. Across the primary replication and three controls,
per-model swings stay within noise, the only significant results — both from Sonnet 4.6, in the
primary and paraphrase runs — are judge-coding variance on near-identical text, and the flat
response survives on un-memorized stimuli, indicating a trained
disposition to resist loaded framing rather than recognition of the source study. Models additionally
sit below the human enforcement baseline, defaulting to balanced answers. The classification for this
study is **smooth**.

## Data and code

Every prompt, all 1,200 primary-replication trials (plus the 1,800 contamination-control trials), the
judge rubric, and the analysis behind these charts live in the
[`experiments/crime-metaphor`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/crime-metaphor)
folder on GitHub. Every model in the catalog can be rerun from the command line, and the chart
regenerates from the recorded run.

## Reference

Thibodeau, P. H., & Boroditsky, L. (2011). Metaphors We Think With: The Role of Metaphor in
Reasoning. *PLoS ONE, 6*(2), e16782.
[https://doi.org/10.1371/journal.pone.0016782](https://doi.org/10.1371/journal.pone.0016782)

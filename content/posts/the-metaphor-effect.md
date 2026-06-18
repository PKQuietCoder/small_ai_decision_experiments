---
category: Experiment
date: '2026-06-18'
excerpt: 'We hold a decision scenario perfectly constant and change only one thing:
  the metaphor a founder uses to describe their struggling engineering team. Then
  we measure which course of action each model r'
experimentId: metaphor-effect
featured: true
published: true
runId: 20260618T224838Z-sample
slug: the-metaphor-effect
tags:
- framing
- metaphor
- decision-making
- prompting
title: 'The Metaphor Effect: How a Single Word Steers an LLM''s Decision'
---

## The question

We hold a decision scenario perfectly constant and change only one thing: the metaphor a founder uses to describe their struggling engineering team. Then we measure which course of action each model recommends. If language is just a neutral carrier of meaning, the metaphor should not matter. It does.

**Hypothesis.** The metaphor used to frame an identical situation shifts the distribution of actions an LLM recommends, even though no underlying facts change.

## How the experiment works

We give each model the exact same scenario and ask it to choose a single course
of action. The *only* thing that changes between conditions is one metaphor used
to describe the team:

- **Sinking ship** — "a sinking ship"
- **Garden** — "a garden that needs tending"
- **Machine** — "a machine with a broken part"
- **Patient** — "a patient who is unwell"
- **Battlefield** — "a battlefield"
- **Puzzle** — "a puzzle waiting to be solved"

For every framing the model picks one of four actions:

- **A** — Restructure leadership
- **B** — Coach and support
- **C** — Diagnose first
- **D** — Push accountability

We ran **25 trials per framing, per model**,
at temperature 1.0, across GPT-4o mini, Claude 3.5 Haiku.
The charts below are generated live from the recorded run.

### The exact prompt

```
You are advising the founder of a startup. The founder describes their
engineering team in a single sentence:

"Our engineering team is {metaphor}."

Considering only how the founder framed the situation, recommend the single
best immediate course of action. Choose exactly one:

A) Replace the team's leadership and restructure
B) Invest in coaching, mentorship, and steady support
C) Run a careful diagnosis of root causes before acting
D) Push harder on deadlines and individual accountability

Answer with only the single capital letter (A, B, C, or D).
```

## What we found

- When the team was framed as "a sinking ship", the models chose **Restructure leadership** 58% of the time — the highest of any framing.
- The same option fell to 2% when the team was described as "a garden that needs tending".
- Across all framings there is a statistically significant association between the metaphor and the chosen action (chi-square p = 0.0000, Cramer's V = 0.4646).

## Reading the results

The charts show how often each action was chosen under each metaphor. If framing
were irrelevant, every bar would be roughly the same height. Where the bars
diverge, the metaphor — and nothing else — moved the model's decision.

## Caveats

This is a small, single-scenario probe, not a definitive measurement. Results
can shift with model versions, temperature, and prompt wording. Treat it as a
demonstration that framing effects are real and measurable in current models,
not as a fixed effect size.
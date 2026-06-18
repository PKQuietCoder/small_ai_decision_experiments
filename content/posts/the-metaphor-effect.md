---
category: Experiment
date: '2026-06-18'
excerpt: 'We hold a decision scenario perfectly constant and change only one thing:
  the metaphor a founder uses to describe their struggling engineering team. Then
  we measure which course of action each model r'
experimentId: metaphor-effect
featured: true
published: true
runId: 20260618T233153Z
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
at temperature 1.0, across GPT-4o mini, Claude Haiku 4.5.
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

The effect is stark. Across **five of the six metaphors** — sinking ship, machine,
patient, battlefield, and puzzle — both models converged almost unanimously on
**C, "Diagnose first."** Nothing about the underlying situation changed, yet the
recommendation was essentially deterministic.

One metaphor broke the pattern. When the team was framed as **"a garden that needs
tending,"** the models flipped to **B, "Coach and support,"** in 47 of 50 trials.
A single organic, nurturing image was enough to move the decision off the otherwise
universal "diagnose" default and toward patient cultivation.

- **"Garden"** → *Coach and support* (B) **94%** of the time.
- **Every other metaphor** → *Diagnose first* (C) **~100%** of the time.

The framing — and nothing else — moved the decision. The charts below break this
down by metaphor and by model.

## Reading the results

The charts show how often each action was chosen under each metaphor. If framing
were irrelevant, every bar would be roughly the same height. Where the bars
diverge, the metaphor — and nothing else — moved the model's decision.

## Caveats

This is a small, single-scenario probe, not a definitive measurement. Results
can shift with model versions, temperature, and prompt wording. Treat it as a
demonstration that framing effects are real and measurable in current models,
not as a fixed effect size.
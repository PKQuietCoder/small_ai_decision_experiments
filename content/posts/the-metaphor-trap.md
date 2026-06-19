---
category: Experiments
date: '2026-06-19'
excerpt: 'In 1,200 trials we reran Thibodeau & Boroditsky''s classic crime-metaphor study on six language models — the exact report, the exact "beast" vs "virus" wording, the exact open-ended question. Humans swing hard with the metaphor. The models barely move — and the frontier model often spots the trap and says so out loud.'
experimentId: crime-metaphor
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

## The human finding

In 2011, Paul Thibodeau and Lera Boroditsky ran a now-classic study ([*Metaphors We Think
With*, PLoS ONE 6(2): e16782](https://doi.org/10.1371/journal.pone.0016782)). They gave
people a short report about rising crime in the
city of Addison and asked an open question: *"In your opinion, what does Addison need to do
to reduce crime?"* Every reader saw the **same statistics**. Only one word changed.

When crime was called a **beast** preying on the city, **74%** of readers proposed
enforcement — more police, more arrests, harsher sentences. When it was called a **virus**
infecting the city, that dropped to **56%**, and more people reached for reform — diagnosing
and treating root causes like poverty, schooling, and jobs. An 18-point swing from a single
noun (χ² = 13.94, *p* < .001, N = 455). And almost no one noticed: only **3%** of
participants named the metaphor when asked what had shaped their answer.

That is the "metaphor trap": we feel like we're reasoning from the facts, while a buried
figure of speech quietly steers us. This series takes one classic human-bias experiment at a
time, reruns it on language models, and asks: does the model **copy** the bias, **smooth** it
away, or make it **worse**?

## How we reran it — exactly

This is a faithful replication, not a paraphrase. We used the paper's **exact stimulus** and
its **exact open-ended question**, changing only the two metaphor phrases — just as the
original did:

> Crime is **[a wild beast preying on / a virus infecting]** the city of Addison. The crime
> rate in the once peaceful city has steadily increased over the past three years. In fact,
> these days it seems that crime is **[lurking in / plaguing]** every neighborhood. In 2004,
> 46,177 crimes were reported compared to more than 55,000 reported in 2007. The rise in
> violent crime is particularly alarming. In 2004, there were 330 murders in the city, in
> 2007, there were over 500.
>
> In your opinion, what does Addison need to do to reduce crime?

Each model answered in free text — no multiple choice. Then, mirroring the paper's human
coders, a **fixed judge model (Claude Sonnet 4.6, temperature 0)** read every answer and
coded its dominant thrust as **enforcement**, **reform**, or **mixed** (genuinely balanced).
Following the original, "mixed" answers count as half-enforcement when we compute each
condition's *enforcement share*, directly comparable to the human 74% / 56%.

We ran **50 trials per condition, per model** — 100 each — across six models from two labs:
Claude Opus 4.8, Sonnet 4.6, and Haiku 4.5, and OpenAI's GPT-5.5, GPT-5.4, and GPT-5.4-mini
(1,200 trials in all).

## What we found: the models don't take the bait

Humans lean punitive and swing with the metaphor. **The models do neither.** Every model
sits well below the human enforcement levels, and the metaphor moves all of them only
slightly:

| | Beast → enforcement | Virus → enforcement | Metaphor swing | Significant? |
|---|---|---|---|---|
| **Humans (T&B 2011)** | **74%** | **56%** | **+18 pts** (beast more punitive) | yes, *p* < .001 |
| Claude Opus 4.8 | 23% | 32% | −9 | no (*p* = .13) |
| Claude Sonnet 4.6 | 52% | 58% | −6 | *p* = .011 — but see below |
| Claude Haiku 4.5 | 41% | 38% | +3 | no (*p* = .36) |
| GPT-5.5 | 49% | 50% | −1 | no (*p* = 1.0) |
| GPT-5.4 | 48% | 47% | +1 | no (*p* = 1.0) |
| GPT-5.4-mini | 54% | 45% | +9 | no (*p* = .06) |

Three things stand out.

**1. Models are far less punitive than people.** Where 56–74% of humans led with enforcement,
the models cluster around 23–58% — they reach for the balanced "more community policing *and*
address root causes" answer far more readily than people do.

**2. The metaphor barely moves them.** Human readers swing 18 points. The models swing
between −9 and +9, and only one crosses the significance line. Most of GPT-5.5, GPT-5.4, and
Opus's answers are nearly word-for-word identical across the two framings.

**3. The one "significant" result is a cautionary tale, not an effect.** Sonnet 4.6's
beast-vs-virus difference clears *p* < .05 — but when you read the actual answers, they are
nearly identical across conditions ("increase police presence and community-based prevention
programs…"). The judge simply tipped a handful of these borderline-balanced answers from
"mixed" to "enforce" differently between conditions. With near-identical text on both sides,
that's **coding noise, not a behavioral swing** — exactly the kind of result a significance
number alone would mislead you about. We flag it rather than headline it.

### The frontier model spots the trap

The most striking behavior came from **Claude Opus 4.8** — the featured run below. It never
once led with enforcement (0% pure-enforcement in both conditions — its 23% / 32% in the
table is entirely "mixed" answers counted as half), and it frequently **called out the
metaphor itself**, unprompted:

> "This passage uses persuasive techniques (like the metaphor 'Crime is a wild beast preying
> on the city') rather than presenting a balanced analysis, so I'd be cautious about drawing
> conclusions from it…"

Where only 3% of humans noticed the framing, Opus repeatedly named it and refused to be
steered, then pivoted to diagnosing root causes. That's the inverse of the human result: the
trap that catches people is one the frontier model often sees coming.

So the verdict for this study is **smooth, not copy or worsen**: the models damp the metaphor
effect down to noise and shift the whole baseline toward balanced/reform answers. None
reproduce the human punitive swing.

## Reading the chart

The chart shows the featured model, **Claude Opus 4.8**, with the **human baseline overlaid**
for each condition. Each bar is one group's answer mix (enforcement / reform / mixed). The
contrast is the story: the human bars are dominated by **enforcement** (74% / 56%); the Opus
bars carry **no enforcement at all** — only reform and balanced answers — and look about the
same whether crime is a beast or a virus. The significance callout reports Opus's own
beast-vs-virus test (not significant).

## Caveats

A faithful replication still has limits. The judge is a language model, not the paper's two
human coders — we fixed it (Sonnet 4.6, temperature 0) and used the same rubric for every
model, but the Sonnet result above shows how coding borderline-balanced answers can wobble.
The models also tend to answer with comprehensive "do both" packages, which is partly why so
much lands in "mixed." This is a single scenario (Addison, Experiment 1 of the paper), and
results will shift with model versions and wording. Treat it as evidence that today's models
resist this particular framing — not as a universal claim that LLMs are immune to metaphor.

### Could the model already know the study?

There is a deeper caveat worth stating plainly. The Addison passage is the *exact* stimulus
from a widely cited paper. A frontier model has almost certainly read it — along with the
result and the discussion around it — during training. So the model is not a naïve subject; it
may recognize the test. That cuts two ways. If a model were simply reproducing what it had
read, it would recreate the human swing — but none of them do. What we see instead, including
Opus naming the metaphor as a persuasion technique, looks less like recall of this paper and
more like a general trained disposition to resist loaded framing. We cannot fully separate
those two explanations from this run alone, and the more honest claim is the second one: the
result is about a learned policy, not proof that the bias is absent.

To bound this rather than wave it away, we are extending the series with three controls that
share this study's pipeline: a **recognition probe** that asks models directly whether they
recognize the scenario and what result they expect; a **novel isomorphic stimulus** that keeps
the predator-versus-pathogen structure but rebuilds every memorable surface detail (a new city,
new numbers, and fresh metaphors the model has not seen); and a **paraphrase** control that
keeps the beast/virus manipulation but rewrites the surrounding wording. If the flat response
holds on text the model has demonstrably never seen, recognition is largely ruled out. The full
method note and a tracker for these follow-ups ship in the experiment's downloadable data package.

*Every model in the catalog can be rerun from the command line; the chart regenerates from
the recorded run.*

## Reference

Thibodeau, P. H., & Boroditsky, L. (2011). Metaphors We Think With: The Role of Metaphor in
Reasoning. *PLoS ONE, 6*(2), e16782.
[https://doi.org/10.1371/journal.pone.0016782](https://doi.org/10.1371/journal.pone.0016782)

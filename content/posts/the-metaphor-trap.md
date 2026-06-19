---
category: Decisions
type: Experiments
date: '2026-06-19'
excerpt: 'We reran Thibodeau & Boroditsky''s classic crime-metaphor study on six language models across 1,200 trials, using the exact report, the exact "beast" vs "virus" wording, and the exact open-ended question. Humans swing hard with the metaphor. The models barely move, and the frontier model often spots the trap and says so out loud.'
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

In 2011, Paul Thibodeau and Lera Boroditsky ran a now-classic study ([*Metaphors We Think With*,
PLoS ONE 6(2): e16782](https://doi.org/10.1371/journal.pone.0016782)). They gave people a short
report about rising crime in the city of Addison and asked one open question: *"In your opinion,
what does Addison need to do to reduce crime?"* Every reader saw the same statistics. Only one word
changed.

Call crime a **beast** preying on the city and **74%** of readers reached for enforcement: more
police, more arrests, harsher sentences. Call it a **virus** infecting the city and that dropped to
**56%**, with more people turning to reform, things like diagnosing and treating root causes such as
poverty, schooling, and jobs. An 18-point swing from a single noun (χ² = 13.94, *p* < .001,
N = 455). Almost nobody caught it. Only **3%** of participants named the metaphor when asked what
shaped their answer.

That's the metaphor trap. We feel like we're reasoning from the facts while a buried figure of
speech quietly steers us. This series takes one classic human-bias experiment at a time and reruns
it on language models. The question each time is simple. Does the model copy the bias, smooth it
away, or make it worse?

## How we reran it, exactly

This is a faithful replication, not a paraphrase. We used the paper's exact stimulus and its exact
open-ended question, changing only the two metaphor phrases, just as the original did:

> Crime is **[a wild beast preying on / a virus infecting]** the city of Addison. The crime
> rate in the once peaceful city has steadily increased over the past three years. In fact,
> these days it seems that crime is **[lurking in / plaguing]** every neighborhood. In 2004,
> 46,177 crimes were reported compared to more than 55,000 reported in 2007. The rise in
> violent crime is particularly alarming. In 2004, there were 330 murders in the city, in
> 2007, there were over 500.
>
> In your opinion, what does Addison need to do to reduce crime?

Each model answered in free text. No multiple choice. Then a fixed judge model (Claude Sonnet 4.6,
temperature 0) read every answer and coded its dominant thrust as enforcement, reform, or mixed
(genuinely balanced), mirroring the paper's human coders. Following the original, "mixed" answers
count as half-enforcement when we compute each condition's *enforcement share*, directly comparable
to the human 74% / 56%.

We ran 50 trials per condition, per model, so 100 each, across six models from two labs: Claude
Opus 4.8, Sonnet 4.6, and Haiku 4.5, plus OpenAI's GPT-5.5, GPT-5.4, and GPT-5.4-mini. That's 1,200
trials in all.

## What we found: the models don't take the bait

Humans lean punitive and swing with the metaphor. The models do neither. Every model sits well
below the human enforcement levels, and the metaphor nudges all of them only slightly:

| | Beast → enforcement | Virus → enforcement | Metaphor swing | Significant? |
|---|---|---|---|---|
| **Humans (T&B 2011)** | **74%** | **56%** | **+18 pts** (beast more punitive) | yes, *p* < .001 |
| Claude Opus 4.8 | 23% | 32% | -9 | no (*p* = .13) |
| Claude Sonnet 4.6 | 52% | 58% | -6 | *p* = .011, but see below |
| Claude Haiku 4.5 | 41% | 38% | +3 | no (*p* = .36) |
| GPT-5.5 | 49% | 50% | -1 | no (*p* = 1.0) |
| GPT-5.4 | 48% | 47% | +1 | no (*p* = 1.0) |
| GPT-5.4-mini | 54% | 45% | +9 | no (*p* = .06) |

Three things stand out.

**1. Models are far less punitive than people.** Where 56% to 74% of humans led with enforcement,
the models cluster around 23% to 58%. They reach for the balanced "more community policing *and*
address root causes" answer far more readily than people do.

**2. The metaphor barely moves them.** Human readers swing 18 points. The models swing between -9
and +9, and only one crosses the significance line. Most answers from GPT-5.5, GPT-5.4, and Opus are
nearly word-for-word identical across the two framings.

**3. The one "significant" result is a cautionary tale, not an effect.** Sonnet 4.6's
beast-versus-virus difference clears *p* < .05. Then you read the actual answers. They're nearly
identical across conditions ("increase police presence and community-based prevention programs…").
The judge simply tipped a handful of borderline-balanced answers from "mixed" to "enforce"
differently between conditions. With near-identical text on both sides, that's coding noise, not a
behavioral swing. It's exactly the kind of result a significance number alone would mislead you
about, so we flag it rather than headline it.

### The frontier model spots the trap

The most striking behavior came from Claude Opus 4.8, the featured run below. It never once led with
enforcement (0% pure-enforcement in both conditions, so its 23% / 32% in the table is entirely
"mixed" answers counted as half). It also called out the metaphor itself, unprompted, again and
again:

> "This passage uses persuasive techniques (like the metaphor 'Crime is a wild beast preying
> on the city') rather than presenting a balanced analysis, so I'd be cautious about drawing
> conclusions from it…"

Only 3% of humans noticed the framing. Opus named it repeatedly, refused to be steered, then pivoted
to diagnosing root causes. That's the inverse of the human result. The trap that catches people is
one the frontier model often sees coming.

The verdict for this study is smooth, not copy or worsen. The models damp the metaphor effect down
to noise and shift the whole baseline toward balanced and reform answers. None reproduce the human
punitive swing.

## Reading the chart

The chart shows the featured model, Claude Opus 4.8, with the human baseline overlaid for each
condition. Each bar is one group's answer mix (enforcement, reform, mixed). The contrast is the
story. The human bars are dominated by enforcement (74% / 56%). The Opus bars carry no enforcement
at all, only reform and balanced answers, and they look about the same whether crime is a beast or a
virus. The significance callout reports Opus's own beast-versus-virus test, which isn't significant.

## Does the model just know the study?

One objection cuts deeper than the rest. The Addison passage is the exact stimulus from a widely
cited paper, so a frontier model has almost certainly read it, and its result, during training. If
the models look unbiased only because they recognize the test and sidestep it, the finding is an
artifact rather than a behavior. To separate those two explanations we ran three controls on all six
models (50 trials per condition each, 1,800 further trials).

**First, the models do know the study.** Asked outright whether they recognized the scenario, the
larger models name it: *Thibodeau and Boroditsky (2011)*, the beast-versus-virus paradigm. And
recognition tracks capability. Here's the share of answers showing any recognition, for the verbatim
passage and for a disguised paraphrase of it:

| Model | Verbatim passage | Disguised |
|---|---:|---:|
| Claude Opus 4.8 | 58% | 100% |
| Claude Sonnet 4.6 | 52% | 70% |
| Claude Haiku 4.5 | 22% | 10% |
| GPT-5.5 | 100% | 100% |
| GPT-5.4 | 76% | 100% |
| GPT-5.4-mini | 94% | 86% |

Only the smallest model, Haiku, usually fails to place it. The material is plainly in the training
data, and the frontier models clearly know it. Two qualifications on the numbers. We asked about
"this *exact* passage", so models often hedged on verbatim recall of the canonical text even while
naming the paradigm. And each probe showed only the beast frame, which is itself a cue.

**Second, and this is the decisive part, the flat response survives on text no model has seen.** We
rebuilt the study from scratch: a different city, different statistics, and novel metaphors. Crime
as a marauding **wolf** versus a growing **cancer**, a predator-versus-pathogen contrast with the
same logic as beast-versus-virus but no memorized surface. If recognition were doing the work, an
unfamiliar stimulus should let the swing return. It doesn't.

| Model | Wolf | Cancer | Swing | Significant? |
|---|---:|---:|---:|---|
| Claude Opus 4.8 | 44% | 40% | +4 | no (*p* = .41) |
| Claude Sonnet 4.6 | 47% | 45% | +2 | no (*p* = .57) |
| Claude Haiku 4.5 | 40% | 41% | -1 | no (*p* = 1.0) |
| GPT-5.5 | 50% | 50% | 0 | no |
| GPT-5.4 | 49% | 50% | -1 | no (*p* = 1.0) |
| GPT-5.4-mini | 49% | 50% | -1 | no (*p* = 1.0) |

A third control kept the original beast/virus framing but paraphrased and renumbered the report.
It's flat for five of six models too. The lone exception, Sonnet 4.6, again produces near-identical
answers across conditions, and its difference runs *opposite* the human direction. That's the same
coding wobble flagged earlier, not a reproduction of the bias.

The conclusion is narrow but firm. Recognition is real, yet it doesn't become imitation. Knowing the
study doesn't make a model copy its result. Not on the canonical text, not on a paraphrase, not on
metaphors it has never encountered. The flat response is a trained disposition to resist loaded
framing, not naïve recall of one paper. What this can't prove is the converse: a capable model's
resistance to framing is itself learned, and no novel stimulus escapes it. We measure that
disposition rather than claim to have removed it. The recognition, novel-stimulus, and paraphrase
runs ship in full in the [data package on GitHub](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/crime-metaphor).

## Practical takeaways for deciding with AI

Quick caveat: this is one scenario and six models, so treat these as working guidance, not laws. The
pattern holds up here and in the budgeting study that's this series' companion.

### What this says about using AI on a loaded question

**They don't take the framing bait, so use one as a spin detector.** A single loaded word swung
people 18 points. The models barely moved, and the frontier model often named the manipulation
outright ("this passage uses persuasive techniques like the metaphor 'crime is a wild beast'…").
Only 3% of humans noticed that framing. When you're handed a memo, a pitch, or a news item you
suspect is slanted, ask a model to strip it: "what are the neutral facts here, and where is the
language steering me?" It catches the buried metaphor better than you do.

**But "unbiased" comes out as "balanced to a fault."** The models didn't swing largely because they
defaulted to the same comprehensive "do both, more policing *and* address root causes" answer almost
regardless of the framing. That even-handedness resists manipulation. It also means a model rarely
hands you a sharp, committed recommendation on a value-laden question. If you need a decision and not
a survey, say so: "pick one side and defend it," or "if you had to choose, what would you drop?"

**A significant p-value isn't an effect. Read the outputs.** The one model that crossed statistical
significance turned out to be producing near-identical answers in both conditions. The judge had
merely tipped a few borderline cases one way. The number said "effect." The text said "no effect."
For any AI-assisted analysis, never act on a summary statistic without spot-reading the raw answers
behind it.

**Knowing the playbook isn't the same as following it.** The models clearly recognized the study,
yet recognition didn't make them copy its result, even on novel material they'd never seen. Useful.
The flip side is a contamination risk: for a famous case or framework, a model may hand you the
textbook answer instead of reasoning about your situation. Push it onto your concrete details.

### How to actually use one well

- **Use it to de-bias your reading, not to make the call.** Have it surface the framing,
  assumptions, and missing context in what you're looking at, then decide yourself.
- **Ask it to name the framing, then argue both sides.** "What's this trying to make me feel, and
  what's the strongest case for the opposite conclusion?" surfaces more than "is this fair?"
- **Force a commitment when you need one.** The default is a balanced "do both." To get a decision,
  make it choose and justify: "pick one and give me three concrete, falsifiable reasons."
- **Don't trust a lone statistic.** Model confidence, a significance number, either way check the
  underlying outputs before you act.
- **For famous cases or frameworks, push past the textbook answer.** Anchor the model to your
  specifics so it reasons about your situation, not the canonical one.

One-line version: let an AI catch the spin and widen your view (name the framing, surface the other
side, list what's missing), and keep the actual judgment, plus any number that matters, with a human
who verifies.

## Caveats

A faithful replication still has limits. The judge is a language model, not the paper's two human
coders. We fixed it (Sonnet 4.6, temperature 0) and used the same rubric for every model, but the
Sonnet result above shows how coding borderline-balanced answers can wobble. The models also tend to
answer with comprehensive "do both" packages, which is part of why so much lands in "mixed." This is
a single scenario (Addison, Experiment 1 of the paper), and results will shift with model versions
and wording. Treat it as evidence that today's models resist this particular framing, not as a
universal claim that LLMs are immune to metaphor. The related worry, that the models only look
unbiased because they recognize this famous stimulus, is handled directly above in "Does the model
just know the study?" Recognition is real, but it doesn't reproduce the swing.

*Every model in the catalog can be rerun from the command line, and the chart regenerates from the
recorded run.*

## Data and code

Every prompt, all 1,200 main-study trials (plus the 1,800 contamination-control trials), the judge
rubric, and the analysis behind these charts live in the
[`experiments/crime-metaphor`](https://github.com/PKQuietCoder/small_ai_decision_experiments/tree/HEAD/experiments/crime-metaphor)
folder on GitHub. Rerun it, recode it, or check the numbers yourself.

## Reference

Thibodeau, P. H., & Boroditsky, L. (2011). Metaphors We Think With: The Role of Metaphor in
Reasoning. *PLoS ONE, 6*(2), e16782.
[https://doi.org/10.1371/journal.pone.0016782](https://doi.org/10.1371/journal.pone.0016782)

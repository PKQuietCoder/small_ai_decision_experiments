# Limitations: training-data familiarity and the contamination question

A note on the single largest validity threat to this study, and the program of
follow-up experiments built to bound it. This file is hand-written and is
preserved across `export_experiment` runs; the follow-up configs it refers to
live in `content/experiments/` and are tracked in
[`variant-tracker.md`](./variant-tracker.md).

## The concern

The Addison passage is the **exact** stimulus from Thibodeau & Boroditsky (2011),
a heavily cited paper that appears in textbooks, course materials, replication
write-ups, and blog posts across the public web. A frontier model has almost
certainly read this stimulus, the "74% vs 56%, beast is more punitive" result,
and the surrounding discussion of metaphor framing. The model is therefore not a
naïve subject. It may recognise the test. That recognition could shape its answer
in ways that have nothing to do with whether it "has" the underlying bias.

## Two distinct mechanisms, pointing in opposite directions

It helps to separate two things that get bundled under "contamination":

1. **Verbatim stimulus recognition.** The model recognises *this specific study*
   and what it is known to show. If the model were simply reproducing what it
   knows, it would recreate the human swing — beast more punitive than virus.

2. **Disposition contamination.** Independent of recognising this paper, models
   are post-trained to detect persuasion, hedge on loaded framing, and return
   balanced answers. This is a learned policy about *how to answer*, not memory
   of a specific result.

These predict different data. Mechanism 1 reproduces the +18-point human swing.
Mechanism 2 flattens it and shifts the baseline toward balanced/reform answers.

## What the data already says

The observed result is hard to explain as naïve recognition-and-mimicry:

- **No model reproduces the human swing.** Effects run from −9 to +9 points
  against the human +18, and only one model crosses significance — and that one
  (Sonnet 4.6) is coding noise on near-identical text, not a behavioural swing.
- **The flat response is accompanied by explicit framing detection.** Claude Opus
  4.8 repeatedly *named* the metaphor as a persuasion technique, unprompted, and
  pivoted to root causes.

That pattern is the signature of mechanism 2 — a trained "do not be steered"
disposition — not of mechanism 1. Opus quoting "this passage uses persuasive
techniques" is the contamination showing itself directly in the transcript.

The honest reading: we cannot cleanly separate "the model reasons past the
metaphor" from "the model was trained to flag loaded language." The result is
consistent with a learned meta-cognitive policy overriding the framing, which is
arguably the more interesting finding — but it is a claim about the *trained
policy*, not about whether LLMs "have" the human metaphor bias.

## How the follow-ups bound it

Each mitigation is a runnable experiment config, ordered by leverage.

1. **Recognition probe** (`crime-metaphor-recognition`). Present the canonical
   stimulus and, separately, a disguised version, and ask the model directly
   whether it has seen this scenario, what it is testing, and what result it
   would expect. A custom judge rubric codes each answer as `recognized`,
   `partial`, or `unrecognized`. This *measures* mechanism 1 instead of
   hand-waving it. A high recognition rate on the canonical text — and a low one
   on the disguised text — is direct evidence that recognition is in play.

2. **Novel isomorphic stimulus** (`crime-metaphor-novel`). The strongest control:
   the same predator-vs-pathogen framing structure, but a different city,
   different numbers, and lexically novel metaphors (a marauding wolf vs a growing
   cancer) chosen so the text matches no indexed source. If the flat-response
   pattern survives on a stimulus the model demonstrably has not memorised,
   mechanism 1 is largely ruled out. If the effect reappears here but is absent on
   the canonical text, that is direct evidence of recognition.

3. **Surface-form paraphrase** (`crime-metaphor-paraphrase`). Keep the canonical
   beast/virus manipulation and every fact, but paraphrase the report and change
   the city and numbers. Memorised-text effects are brittle to surface
   perturbation; genuine framing effects are not. This turns "did it recognise the
   string" into a measurable robustness curve.

4. **Metaphor-flagging rate as its own metric.** Treat the disposition as the
   object of study rather than a nuisance: report, per model and per condition,
   how often the answer explicitly names the frame. This is a clean,
   contamination-aware dependent variable. Tracked as a planned analysis-layer
   metric (re-coding existing run transcripts), not a new subject experiment.

## A limit that survives all of the above

These controls bound mechanism 1; they cannot eliminate mechanism 2. A
sufficiently capable model carries a general "resist loaded framing" disposition
that no novel stimulus escapes, because the disposition is not about this content.
The defensible scientific stance is not to claim we have controlled it away, but
to measure it — through the recognition probe and the metaphor-flagging rate — and
to report LLM framing-resistance as a property of the trained policy. That is a
more accurate, and more interesting, claim than "today's LLMs do not have the
metaphor bias."

## Reference

Thibodeau, P. H., & Boroditsky, L. (2011). Metaphors We Think With: The Role of
Metaphor in Reasoning. *PLoS ONE, 6*(2), e16782.
https://doi.org/10.1371/journal.pone.0016782

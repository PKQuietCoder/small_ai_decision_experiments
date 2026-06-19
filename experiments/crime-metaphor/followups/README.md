# Contamination follow-ups — data package

Three controls built to answer one question about the published `crime-metaphor`
study: **is the models' flat metaphor response real reasoning, or just an artifact
of the models having read the famous Thibodeau & Boroditsky (2011) stimulus during
training?** Motivation and design are in
[`../methodology/Limitations.md`](../methodology/Limitations.md); status is tracked
in [`../methodology/variant-tracker.md`](../methodology/variant-tracker.md).

All three were run on the same six models as the main study, 50 trials per
condition per model (100 per model; **1,800 trials total**), on 2026-06-19.

## Layout

```
followups/
├── README.md                 # this file
├── recognition/              # does the model recognize the study?
├── novel/                    # does the flat response survive un-memorized text?
└── paraphrase/               # is the result brittle to surface wording?
    ├── summary.csv           # per model × condition: counts, shares, swing, p
    ├── raw/runs/<model>__<runId>.json    # full per-trial data (subject + judge)
    └── analysis/<model>__<runId>.json    # aggregated stats per model
```

## Headline results

**1. The models do know the study — recognition is real (`recognition/`).**
Asked whether they recognize the scenario, the frontier models name "Thibodeau and
Boroditsky (2011)" and the beast/virus paradigm directly. Share of trials showing
any recognition (recognized + partial), canonical / disguised stimulus:

| Model | Canonical | Disguised |
|---|---:|---:|
| Claude Opus 4.8 | 58% | 100% |
| Claude Sonnet 4.6 | 52% | 70% |
| Claude Haiku 4.5 | 22% | 10% |
| GPT-5.5 | 100% | 100% |
| GPT-5.4 | 76% | 100% |
| GPT-5.4 mini | 94% | 86% |

Recognition scales with capability — GPT-5.5 names the study every time; only the
smallest model (Haiku) mostly does not. Two wording effects to read honestly: the
probe asked about "this *exact* passage," so on the verbatim canonical text models
often hedged about literal recall (high "partial") even while recognizing the
paradigm; and because each trial shows only the *beast* frame, recognition is partly
cued by the metaphor itself. The robust takeaway survives both: **the material is in
training, and the larger models clearly know it.**

**2. The flat response survives on un-memorized text (`novel/`) — the key result.**
Same predator-vs-pathogen structure, but a new city, new numbers, and novel
metaphors (a marauding *wolf* vs a growing *cancer*) that match no source. If the
main study only looked flat because models recognized and dodged the canonical text,
a fresh stimulus should reveal a swing. It does not — every model is flat and none is
significant:

| Model | wolf | cancer | swing | p |
|---|---:|---:|---:|---:|
| Claude Opus 4.8 | 44% | 40% | +4 | .41 |
| Claude Sonnet 4.6 | 47% | 45% | +2 | .57 |
| Claude Haiku 4.5 | 40% | 41% | −1 | 1.0 |
| GPT-5.5 | 50% | 50% | 0 | n/a |
| GPT-5.4 | 49% | 50% | −1 | 1.0 |
| GPT-5.4 mini | 49% | 50% | −1 | 1.0 |

**3. The result is not brittle to paraphrase (`paraphrase/`).** Same beast/virus
manipulation and facts, rewritten report and new city/numbers. Five of six models
stay flat (swings +1 to +7, none significant). The exception is Sonnet 4.6 (−19,
p<.001) — but inspection of `paraphrase/raw/runs/` shows near-identical
"multi-pronged: targeted policing + investigate root causes" answers in both
conditions, with the judge tipping borderline-balanced answers between mixed and
reform differently. It runs *opposite* the human direction (virus more punitive than
beast), so it is coding noise, not a reproduction of the human bias — the same
caveat the main study flagged for Sonnet, slightly larger here.

## Verdict

Recognition of the study is real and widespread, **yet no model reproduces the
human swing — not on the canonical text, not on a paraphrase, and not on novel
metaphors it has never seen.** Knowing the study does not translate into copying its
result. The flat response is a general trained disposition to resist loaded framing,
not naïve recall of this particular paper. The contamination concern is therefore
bounded: it does not explain away the main finding.

The one limit this cannot remove (see `Limitations.md`): a capable model's "resist
loaded framing" disposition is itself learned, and no novel stimulus escapes it. We
measure that disposition (recognition rate here; metaphor-flagging rate as a planned
metric) rather than claim to have controlled it away.

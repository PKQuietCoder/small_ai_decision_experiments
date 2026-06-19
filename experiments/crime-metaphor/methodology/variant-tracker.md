# Metaphor-trap variant tracker

The canonical record of every experiment in the metaphor-trap family. The first
row is the published study; the rest are the contamination controls motivated by
[`Limitations.md`](./Limitations.md). Each is a standalone experiment config in
`content/experiments/<id>.yaml` and runs through the existing engine.

Update this file whenever a variant is added, run, or its status changes.

## Variants

| id | role | stimulus | metaphor pair | coding | human baseline | status |
|---|---|---|---|---|---|---|
| `crime-metaphor` | published study | canonical T&B Addison text, verbatim | beast / virus | enforce / reform / mixed | yes (T&B 2011) | **run + published** |
| `crime-metaphor-recognition` | recognition probe | canonical (verbatim) vs disguised paraphrase | beast (held constant) | recognized / partial / unrecognized | n/a | draft — not yet run |
| `crime-metaphor-novel` | novel isomorphic control | new city (Brookhaven) + new numbers | wolf / cancer | enforce / reform / mixed | none (no human data) | draft — not yet run |
| `crime-metaphor-paraphrase` | surface-form control | paraphrased report, new city (Marlowe) + new numbers | beast / virus | enforce / reform / mixed | approximate (T&B 2011) | draft — not yet run |

## What each control tests

- **recognition** — measures contamination directly. Recognition should be high on
  the verbatim text and low on the disguise; the gap estimates how much the main
  result could be recognition rather than reasoning. Uses a custom judge rubric
  (`coder.rubric` + `coder.categories` in the YAML), enabled by the config-driven
  coder in `server/experiments/engine.py`.
- **novel** — strongest control. Same predator-vs-pathogen structure, no memorable
  surface. If the flat swing survives here, stimulus recognition is largely ruled
  out. No human baseline exists for wolf/cancer, so the comparison is within-model
  and against the canonical run.
- **paraphrase** — keeps the canonical beast/virus manipulation and all facts but
  rewrites wording. Memorized-text effects are brittle to this; framing effects are
  not. Compared against the canonical run.

## Planned analysis-layer metric (not a subject experiment)

- **Metaphor-flagging rate** — per model and condition, the share of answers that
  explicitly name the frame as persuasion. A contamination-aware dependent variable
  recovered by re-coding existing run transcripts; no new subject run required.
  Not yet implemented.

## How to run a variant

One model per run; repeat per model to fill the comparison table. Requires
`ANTHROPIC_API_KEY` / `OPENAI_API_KEY`; a full run is hundreds of foreground calls.

```bash
# Smoke first; then the catalog models used in the main study.
python -m server.run_experiment crime-metaphor-recognition --model opus --no-post
python -m server.run_experiment crime-metaphor-novel        --model opus --no-post
python -m server.run_experiment crime-metaphor-paraphrase   --model opus --no-post
#   models: opus | sonnet | haiku | gpt-5.5 | gpt-5.4 | gpt-5.4-mini

# After running, refresh this package (preserves hand-written files in methodology/):
python -m server.export_experiment crime-metaphor
```

Confirm each run reports `N/N trials parsed successfully` with `parseFailures: 0`,
then update the status column above. These are drafts (`status: draft`,
unpublished); they do not appear in a deployment until promoted.

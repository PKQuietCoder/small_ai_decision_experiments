# The Decoy Effect Under Agentic Scaffolds. Data Package (`decoy-effect-agentic`)

A self-contained, replication-ready package for the **agentic extension** of our
faithful decoy-effect replication. It holds the original attraction-effect choice
(target / competitor / asymmetrically dominated decoy, the four placement
strategies) fixed, and varies only *how an agent reaches the decision*: a single
tool call, a forced inspect-compare-choose workflow, fully autonomous tool use, and
a retrieval arm where the agent must look each option up through tools rather than
reading a menu.

This is a **methods extension, not a human comparison** — there is no human
"agentic" baseline. Every comparison here is *within* one experiment and one tool
harness, where the only thing that changes between conditions is the scaffold.

> For the faithful single-shot replication across six models (Part I), see the
> companion package [`../decoy-effect/`](../decoy-effect/). Both studies are
> reported in one write-up:
> [`content/posts/decoy-effect.md`](../../content/posts/decoy-effect.md).

---

## Methodology

**The decision (held fixed).** For three categories — **film, cars, and television
sets**, chosen to span a fragile mid-range default (film), a target-favouring
default (cars), and a competitor-favouring default (TV) — the target, competitor,
and four placement decoys take the paper's exact Appendix II attribute values,
identical to the replication. Options are presented neutrally as `option_1/2/3`;
the role words never appear, and the per-cell choice enum is clamped so a no-decoy
menu can offer only its two real options.

**The scaffold (varied).** Four modes — the first three with the menu in the
prompt, the last with it hidden behind tools:

| Mode | What the agent does | Menu | Mean tool calls |
|---|---|---|---:|
| `shot` — single-shot | one `choose_product` call, decide immediately | in prompt | 1.0 |
| `workflow` — forced workflow | pinned `inspect_options` → `compare_options` → `choose_product` | in prompt | 3.0 |
| `auto` — autonomous | calls tools freely until it picks (`mode: auto`) | in prompt | 3.0 |
| `retrieval` — retrieval | must `list_products` and `get_specs` each option, then `choose_product` | retrieved | 4.8 |

**Conditions.** Three categories × five placements (no decoy, R, Rstar, F, RF) ×
four modes = **60 conditions**, 30 trials each, on **Claude Opus 4.8** at default
sampling. 1,800 trials. The choice is read from a schema-constrained tool field; in
the retrieval arm the option data is served only through `get_specs`, and every
call is logged. The five tool definitions are in `methodology/tools.json`; the
per-condition step sequences (forced vs `auto`) are in
`methodology/conditions.json`; the rendered scenarios are in
`methodology/prompt_<condition>.txt`.

**Baseline.** Within-experiment, against this study's own single-shot arm — not the
replication's structured-output run. The single-shot tool harness is not identical
to Part I's harness, and for film's fragile default the two disagree, so each mode
is read against *its own* no-decoy menu. See `methodology/human_baseline.json` for
the note.

**Significance tests.** Per scaffold contrast: a chi-square test of independence on
the condition × choice table, with Cramér's V. See `results/significance.csv`.

---

## Results (summary)

Two parts of the decoy result are **scaffold-proof**; the rest depends on how the
agent deliberates.

**1. The decoy is never chosen — even when the agent looks it up itself.** Across
1,440 decoy-present trials it was picked under 1.1% in every scaffold (0.0% under
retrieval). The retrieval arm is the sharpest version: in **360 of 360** trials the
agent called `get_specs` on the dominated option before choosing, and in none of
them did it choose it.

**2. Range attraction survives deliberation but breaks under retrieval.** Under a
co-presented menu a range decoy lifts the target to ~99% of choices, and
single-shot, forced-workflow, and autonomous arms are indistinguishable. When the
agent must look the options up itself, the same range decoy leaves the target at
~62% — its no-decoy retrieval baseline — i.e. no attraction lift at all.

**3. Deliberation undoes the single-shot frequency reversal.** Mean change in the
target's share, by placement, relative to *each scaffold's own* no-decoy menu
(averaged over film, cars, TV):

| Scaffold | R | Rstar | F | RF |
|---|---:|---:|---:|---:|
| `shot` — single-shot | +66.7 | +57.8 | **−15.6** | −24.4 |
| `workflow` — forced workflow | +70.0 | +70.0 | **+23.3** | −8.9 |
| `auto` — autonomous | +63.3 | +65.6 | **+36.7** | −16.7 |
| `retrieval` — retrieval | −4.4 | −1.1 | −55.6 | −58.9 |

The single-shot agent reproduces the Opus frequency reversal (target just 17% under
a frequency decoy); adding process unwinds it (workflow 53%, autonomy 71%).
Retrieval removes the range lift, deepens the frequency collapse, and shifts the
agent's baseline taste (its no-decoy default rises from 0% to 53-67% under
retrieval), so its column is a distinct regime, not a clean overlay.

**Takeaway.** The agentic scaffold is not neutral: *how you ask an agent to decide*
is itself part of the experiment. Full numbers:
`results/summary_by_condition.csv` and `results/significance.csv`; the full write-up
is [`content/posts/decoy-effect.md`](../../content/posts/decoy-effect.md), Part II.

---

## Package contents

```
decoy-effect-agentic/
├── README.md                       # this file
├── manifest.json                   # machine-readable index (model, runs, tools, conditions)
├── methodology/
│   ├── decoy-effect-agentic.yaml   # exact experiment config (methodology as code)
│   ├── prompt_<condition>.txt      # rendered scenario each of the 60 conditions saw
│   ├── tools.json                  # the five tool definitions (schemas, strict flag)
│   ├── conditions.json             # each condition's step sequence / autonomous mode
│   ├── products.json               # present but empty for this study (no priced products)
│   └── human_baseline.json         # the within-experiment baseline note
├── raw/
│   ├── runs/<model>__<runId>.json  # full per-trial data incl. step sequence + transcript
│   └── trials.csv                  # all trials flattened (see dictionary below)
├── results/
│   ├── analysis/<model>__<runId>.json  # aggregated analysis (counts, proportions, chi-square, stepProfile)
│   ├── summary_by_condition.csv    # per condition: per-option counts and shares, mean steps
│   └── significance.csv            # chi-square of independence + effect size
└── decoy-effect-agentic-data-package.zip  # everything above, zipped for download
```

### Data dictionary, `raw/trials.csv`
| column | meaning |
|---|---|
| `experiment` | experiment id (`decoy-effect-agentic`) |
| `model` / `provider` | subject model label / provider |
| `condition` | `<category>_<placement>_<mode>`, e.g. `film_F_auto` |
| `trial` | trial index (0-29) within the condition cell |
| `chosen_product` | the chosen option id: `option_1` / `option_2` / `option_3` |
| `num_steps` | how many tool calls the agent made before finishing |
| `steps` | the ordered tool sequence, pipe-separated |
| `capped` | true if the autonomous loop hit the step cap and was forced to finish |
| `ok` / `error` | whether the trial completed without error / the error message |
| `price_usd`, `planned_budget` | inherited from the agentic-budget data shape; **not used** here (no priced products, no budget tool) |

The `mean_price_usd` and `budget_rate_pct` columns in `summary_by_condition.csv`
are likewise inherited and not meaningful for this study; use the per-option counts,
shares, and `mean_steps`.

---

## How to replicate

**With this repository's pipeline** (needs `ANTHROPIC_API_KEY`):

```bash
python -m server.run_experiment decoy-effect-agentic --model opus --no-post

# regenerate this data package after runs:
python -m server.export_experiment decoy-effect-agentic
```

The experiment is fully specified by `methodology/decoy-effect-agentic.yaml`.

**Independently, or with another stack.** Everything is provider-agnostic:
1. Give the agent the five tools in `tools.json` and, per condition, the scenario in
   `methodology/`. For the forced modes, pin the tool sequence in `conditions.json`
   (one tool per turn); for `auto`, offer the tools and force nothing; for the
   retrieval arm, serve option specs only through `get_specs`.
2. Run each of the 60 conditions 30 times, recording the chosen option and the step
   sequence per trial.
3. For each scaffold, compute the target's (`option_1`) share against *that
   scaffold's* no-decoy menu, and a chi-square on the condition × choice table.

---

## Caveats

- **Within-experiment only.** All four scaffolds share one tool harness; the
  single-shot arm is the baseline, not a re-run of the replication's
  structured-output study. Do not compare these numbers to the `decoy-effect`
  package directly — the harnesses differ and film's default flips between them.
- **Retrieval confounds delivery with baseline.** Reading specs serially changes
  both the agent's default taste and the decoy's effect; read the retrieval column
  as a distinct regime. The RF decoy is the least stable cell.
- **One model, one run, 30 trials per cell.** Opus 4.8 only; the stable results are
  the directional scaffold effects, not precise point estimates. A GPT-5 scaffold
  contrast and repeated runs are natural follow-ups.
- **No judge model.** The decision is read straight from a constrained tool field.

## Citation

Underlying study: Huber, J., Payne, J. W., & Puto, C. (1982). Adding Asymmetrically
Dominated Alternatives: Violations of Regularity and the Similarity Hypothesis.
*Journal of Consumer Research, 9*(1), 90-98. https://doi.org/10.1086/208899

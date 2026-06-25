# The Decoy Effect: Does a Worse Option Sway a Model's Choice? Data Package (`decoy-effect`)

A self-contained, replication-ready package for our faithful rerun of **Huber, J.,
Payne, J. W., & Puto, C. (1982). *Adding Asymmetrically Dominated Alternatives:
Violations of Regularity and the Similarity Hypothesis.* Journal of Consumer
Research, 9(1), 90-98**, run across six models, with a direct comparison to the
paper's human baseline.

Everything you need to inspect, re-analyze, or independently replicate the study
is here: the methodology (the six categories, the four decoy placements, the exact
attribute values, the human baseline), the raw per-trial choices, and the
aggregated results for each model.

The human finding: add a third, clearly worse option to a pair, and people shift
toward whichever of the original two the decoy makes look good — even though almost
nobody picks the decoy itself. Adding an option that is never chosen still changes
the split between the other two, which violates *regularity*, a property most
formal choice models assume. We ask whether a language model does the same.

> This package covers **Part I — the faithful replication**. The agentic extension
> (the same choice under single-shot, forced-workflow, autonomous, and retrieval
> scaffolds) is a separate study, packaged in
> [`../decoy-effect-agentic/`](../decoy-effect-agentic/). Both are reported in one
> write-up: [`content/posts/decoy-effect.md`](../../content/posts/decoy-effect.md).

---

## Methodology

**Design.** A faithful translation of the paper. Each trial presents two or three
options in one product category, each described on exactly two attributes, with the
instruction to choose one "on this information alone." In each set a **target** and
a **competitor** form a genuine tradeoff (each better on one attribute); a
**decoy**, when present, is **asymmetrically dominated** — worse than the target on
both attributes but not worse than the competitor — so it should almost never be
chosen.

**Categories (paper's Appendix II values).** Beer, cars, restaurants, lotteries,
film, television sets.

**The four decoy placements**, the paper's sharpest contribution — *where* the
decoy sits, illustrated for beer (target $1.80 / quality 50; competitor $2.60 /
quality 70):

| Strategy | What it does | Example decoy (beer) |
|---|---|---|
| `R` — moderate range | worse on the target's weak attribute, at the target's strong value | $1.80, quality 40 |
| `Rstar` — extreme range | extends that further | $1.80, quality 30 |
| `F` — frequency | matches the target's weak attribute, edges toward the competitor on the strong one | $2.20, quality 50 |
| `RF` — range-frequency | combines both | $2.20, quality 40 |

Every decoy was verified to be dominated by the target and **not** by the
competitor, so any shift is attributable to attraction or similarity, not to a
plainly better or cheaper option.

**Conditions.** Six categories × five menus (no decoy + R, Rstar, F, RF) = **30
conditions**, each run **30 times per model** (900 trials per model). Options are
presented neutrally as `option_1` / `option_2` / `option_3`; the role words
(target, competitor, decoy) never appear in the prompt or the choice enum. The
target is always `option_1`, the competitor `option_2`, the decoy `option_3`, so
the clean contrast is each category's no-decoy menu versus its decoy menus. The
pick is read from a schema-constrained field (Anthropic forced tool use / OpenAI
structured output), never parsed from prose.

**Models (subjects).** Claude Opus 4.8 (featured), Claude Sonnet 4.6, Claude Haiku
4.5, GPT-5.5, GPT-5.4, and GPT-5.4-mini. 900 trials each; 5,400 total. The GPT-5
models are reasoning models, run at low reasoning effort. Opus 4.8 rejects the
`temperature` parameter, so its run used the model's default sampling.

**Human baseline (paper).** No-decoy target share ≈ 0.50; adding a decoy raised it
by +9.2 points on average (range R/Rstar +13, range-frequency RF +8, frequency F
+4), with the decoy itself chosen ≈ 1-2% of the time. Every placement was positive
for people. See `methodology/human_baseline.json`.

**Significance tests.** Per model: a chi-square test of independence on the
condition × choice table, with Cramér's V, dropping all-zero option columns before
testing so the never-chosen decoy column does not distort the statistic. See
`results/significance.csv`.

---

## Results (summary)

Two findings hold for **every** model; one splits by family.

**1. The decoy is essentially never chosen, yet the choice still moves.** Across
all decoy-present trials the dominated option was picked 0-2% of the time (0% for
Opus, Sonnet, GPT-5.5, GPT-5.4; 1-2% for Haiku and GPT-5.4-mini, closest to the
human 1-2%). Its mere presence still reshaped the choice strongly (every model
*p* < 10⁻⁷⁸; Cramér's V 0.55-0.96).

**2. Range decoys produce — and usually amplify — the attraction effect, in every
model.** Mean change in the target's share, by placement, averaged across the six
categories:

| Placement | Opus 4.8 | Sonnet 4.6 | Haiku 4.5 | GPT-5.5 | GPT-5.4 | GPT-5.4-mini | Humans |
|---|---:|---:|---:|---:|---:|---:|---:|
| `R` — moderate range | +20.0 | +16.7 | +12.2 | +39.4 | +47.2 | +12.2 | +13 |
| `Rstar` — extreme range | +17.2 | +21.7 | +7.2 | +36.7 | +46.1 | +6.7 | +13 |
| `F` — frequency | **−27.8** | **−31.7** | **−30.6** | +8.3 | +0.6 | −16.7 | +4 |
| `RF` — range-frequency | **−44.4** | **−22.8** | **−16.7** | +12.2 | +3.9 | +5.0 | +8 |

**3. The frequency reversal is a Claude-family signature.** All three Claude models
flip frequency decoys sharply negative — abandoning the target for the distinctive
competitor, a pattern consistent with the *similarity* effect the original design
was built to overpower. The GPT-5 flagships instead stay weakly positive on both
frequency placements, reproducing the gentle, uniformly-positive human ordering.
The small GPT-5.4-mini sits between the families.

**Verdict: mixed.** No model smooths the bias away, and none simply copies the
gentle human version — the attraction effect is copied and amplified across the
board, while the frequency reversal divides Claude from GPT-5. Full numbers:
`results/summary_by_condition.csv` and `results/significance.csv`; the full
write-up, with per-category tables, is in
[`content/posts/decoy-effect.md`](../../content/posts/decoy-effect.md).

---

## Package contents

```
decoy-effect/
├── README.md                       # this file
├── manifest.json                   # machine-readable index (models, runs, conditions, baseline)
├── methodology/
│   ├── decoy-effect.yaml           # exact experiment config (methodology as code)
│   ├── prompt_<category>_<menu>.txt # the rendered menu each of the 30 conditions saw
│   └── human_baseline.json         # Huber, Payne & Puto (1982) baseline + source
├── raw/
│   ├── runs/<model>__<runId>.json  # full per-trial data (every choice + raw payload)
│   └── trials.csv                  # all trials flattened (see dictionary below)
├── results/
│   ├── analysis/<model>__<runId>.json  # per model: counts, proportions, Wilson CIs, chi-square
│   ├── summary_by_condition.csv    # per source × condition: option counts and exclusions
│   └── significance.csv            # per model: chi-square of independence + Cramér's V
└── decoy-effect-data-package.zip   # everything above, zipped for download
```

### Data dictionary, `raw/trials.csv`
| column | meaning |
|---|---|
| `experiment` | experiment id (`decoy-effect`) |
| `model` / `provider` | subject model label / provider |
| `condition` | `<category>_<menu>`, e.g. `beer_R`, `film_no_decoy` |
| `frame` / `spread` | unused for this study (blank); columns shared with framing experiments |
| `trial` | trial index (0-29) within the model × condition cell |
| `code` | the chosen option id: `option_1` (target) / `option_2` (competitor) / `option_3` (decoy) |
| `ok` | whether the trial completed without error |
| `response` | the raw model payload the choice was read from |

### Data dictionary, `results/summary_by_condition.csv`
`source` (model), `condition`, `n`, then `option_1_count` / `option_2_count` /
`option_3_count`, and `excluded_none` (trials whose choice fell outside the enum).
The trailing `enforce_share_pct` column is a carryover from the shared coded-results
writer and is **not meaningful** for this study (it reads 0); use the option counts.

---

## How to replicate

**With this repository's pipeline** (needs `ANTHROPIC_API_KEY` and/or
`OPENAI_API_KEY`):

```bash
# one model per run; pick opus | sonnet | haiku | gpt-5.5 | gpt-5.4 | gpt-5.4-mini
python -m server.run_experiment decoy-effect --model opus --no-post

# regenerate this data package after runs:
python -m server.export_experiment decoy-effect
```

The experiment is fully specified by `methodology/decoy-effect.yaml`.

**Independently, or with another stack.** Everything you need is provider-agnostic:
1. Present each model the menus in `methodology/prompt_<category>_<menu>.txt`, with
   options labelled neutrally and the choice constrained to the offered option ids.
2. Run each of the 30 conditions 30 times per model.
3. For each category, compute the target's (`option_1`) share on the no-decoy menu
   and on each decoy menu; the quantity of interest is the change. Run a chi-square
   on the condition × choice table. Compare against the human baseline in
   `methodology/human_baseline.json`.

---

## Caveats

- **Floor and ceiling effects.** Each model's near-deterministic taste means most
  categories sit at 0% or 100% on the bare menu, so a decoy can visibly move the
  choice in only one direction per category. The directional split is read across
  categories and, cleanly, within film — the one category with a mid-range baseline.
- **Fixed option positions.** The original counterbalanced positions across groups;
  here positions are held fixed and the within-category change is the unit of
  inference. This controls position for that contrast but does not estimate a
  position effect.
- **One run per model, 30 trials per cell.** Point magnitudes are noisy; the stable
  results are the *directions*, not precise estimates.
- **No judge model.** The decision is read straight from a constrained choice field,
  never parsed from prose, so there is no coding step to introduce noise.

## Citation

Original study: Huber, J., Payne, J. W., & Puto, C. (1982). Adding Asymmetrically
Dominated Alternatives: Violations of Regularity and the Similarity Hypothesis.
*Journal of Consumer Research, 9*(1), 90-98. https://doi.org/10.1086/208899

# The Metaphor Trap — Data Package (`crime-metaphor`)

A self-contained, replication-ready package for our rerun of **Thibodeau, P. H., &
Boroditsky, L. (2011). *Metaphors We Think With: The Role of Metaphor in Reasoning.* PLoS
ONE, 6(2), e16782** on six large language models, with a direct comparison to the paper's
human baseline.

Everything you need to inspect, re-analyze, or independently replicate the study is here:
the methodology (exact stimuli, question, coding rubric, judge, human baseline), the raw
per-trial data (every model answer + its code), and the aggregated results.

---

## Methodology

**Design.** A faithful replication of the paper's **Experiment 1**. Each model reads the
paper's exact crime report about the fictional city of Addison and answers the paper's exact
open-ended question. The *only* thing that varies between the two conditions is one metaphor,
at two points in the text — identical to the original manipulation:

| Condition | "Crime is …" | "… crime is __ every neighborhood" |
|-----------|--------------|------------------------------------|
| **beast** | a wild beast preying on | lurking in |
| **virus** | a virus infecting | plaguing |

All statistics in the report (46,177 → 55,000 crimes; 330 → 500 murders) are identical across
conditions. The full rendered prompts are in `methodology/prompt_beast.txt` and
`methodology/prompt_virus.txt`.

**Question (verbatim).** *"In your opinion, what does Addison need to do to reduce crime?"*
Models answered in free text (a light "answer in a sentence or two" instruction was added;
disclosed here).

**Coding.** Mirroring the paper's two human coders, a fixed judge model — **Claude Sonnet 4.6
at temperature 0** — read each free-text answer and assigned its **dominant thrust**:

- `enforce` — leads with/emphasizes law enforcement or punishment (police, arrests,
  crackdowns, harsher sentences, prisons, deterrence)
- `reform` — leads with/emphasizes diagnosing or treating root causes / social reform
  (investigate causes, education, jobs, poverty, economy, housing, healthcare)
- `mixed` — gives both clearly equal weight
- `none` — no concrete suggestion (excluded from analysis)

The exact judge prompt is in `methodology/coding_rubric.txt`.

**Enforcement share.** To compare against the human numbers, each condition's *enforcement
share* counts `mixed` as half an enforcement vote (the paper split mixed answers 0.5/0.5):
`enforcement_share = (enforce + 0.5 · mixed) / (enforce + reform + mixed)`.

**Models (subjects).** Claude Opus 4.8, Claude Sonnet 4.6, Claude Haiku 4.5, GPT-5.5,
GPT-5.4, GPT-5.4-mini. **50 trials per condition, per model** (100 per model; 600 total).

**Human baseline (from the paper, Exp. 1, N = 455).** Beast → **74%** enforcement; Virus →
**56%** enforcement; beast-vs-virus χ² = 13.94, *p* < .001. See
`methodology/human_baseline.json`.

**Significance test.** Per model: a chi-square test of independence on the
condition × {enforce, reform, mixed} table (α = 0.05). Note this differs from the human
2-way enforce-vs-reform test; see `results/significance.csv`.

---

## Results (summary)

Enforcement share (mixed = ½), beast vs virus, per source:

| Source | Beast | Virus | Swing | Model effect significant? |
|--------|------:|------:|------:|---------------------------|
| **Humans (T&B 2011)** | **74%** | **56%** | +18 | yes (*p* < .001) |
| Claude Opus 4.8 | 23% | 32% | −9 | no (*p* = .13) |
| Claude Sonnet 4.6 | 52% | 58% | −6 | *p* = .011 — coding noise, not robust* |
| Claude Haiku 4.5 | 41% | 38% | +3 | no (*p* = .36) |
| GPT-5.5 | 49% | 50% | −1 | no (*p* = 1.0) |
| GPT-5.4 | 48% | 47% | +1 | no (*p* = 1.0) |
| GPT-5.4-mini | 54% | 45% | +9 | no (*p* = .06) |

\* Sonnet's answers are nearly identical across conditions; the judge tipped a few
borderline-balanced answers differently, which is enough to cross *p* < .05. Treat it as a
coding artifact, not a behavioral effect (read the raw responses in `raw/trials.csv`).

**Takeaway.** Humans lean punitive and swing 18 points with the metaphor. The models are far
less punitive and barely move — they *smooth* the bias. Opus 4.8 never led with enforcement
and frequently named the metaphor as persuasion and refused it.

Full numbers: `results/summary_by_condition.csv` and `results/significance.csv`.

---

## Package contents

```
crime-metaphor/
├── README.md                       # this file
├── manifest.json                   # machine-readable index (models, runs, baseline, generated-at)
├── methodology/
│   ├── crime-metaphor.yaml         # exact experiment config (methodology as code)
│   ├── prompt_beast.txt            # rendered subject prompt — beast condition
│   ├── prompt_virus.txt            # rendered subject prompt — virus condition
│   ├── coding_rubric.txt           # exact judge prompt used to code answers
│   └── human_baseline.json         # T&B (2011) Exp. 1 baseline + source
├── raw/
│   ├── runs/<model>__<runId>.json  # full per-trial raw data (one file per model)
│   └── trials.csv                  # all 600 trials flattened (see dictionary below)
├── results/
│   ├── analysis/<model>__<runId>.json  # aggregated analysis per model (counts, proportions,
│   │                                   # Wilson CIs, chi-square, human-baseline overlay)
│   ├── summary_by_condition.csv    # per source × condition counts + enforcement share
│   └── significance.csv            # per-model chi-square (statistic, dof, p, Cramér's V)
└── crime-metaphor-data-package.zip # everything above, zipped for download
```

### Data dictionary — `raw/trials.csv`
| column | meaning |
|--------|---------|
| `experiment` | experiment id (`crime-metaphor`) |
| `model` / `provider` | subject model label / provider |
| `condition` | `beast` or `virus` |
| `frame` / `spread` | the two varied phrases substituted into the report |
| `trial` | trial index (0–49) within the model × condition cell |
| `code` | judge's label: `enforce` / `reform` / `mixed` / `none` |
| `ok` | whether the trial completed without error |
| `response` | the model's full free-text answer (the coded text) |

### Data dictionary — `results/summary_by_condition.csv`
`source` (model or "Humans …"), `condition`, `n`, `enforce_count`, `reform_count`,
`mixed_count`, `excluded_none`, `enforce_share_pct`. Human rows carry only `enforce_share_pct`
(from the paper; their mixed answers were already split into the percentage).

---

## How to replicate

**With this repository's pipeline** (needs `ANTHROPIC_API_KEY` and `OPENAI_API_KEY`):

```bash
# one model per run; pick from: opus, sonnet, haiku, gpt-5.5, gpt-5.4, gpt-5.4-mini
python -m server.run_experiment crime-metaphor --model opus --no-post

# regenerate this data package after runs:
python -m server.export_experiment crime-metaphor
```

The experiment is fully specified by `methodology/crime-metaphor.yaml`.

**Independently / with another stack.** Everything needed is provider-agnostic:
1. Send each subject model the two prompts in `methodology/`, 50 times each (the report is
   identical except the two metaphor phrases).
2. Code each free-text answer into `enforce` / `reform` / `mixed` / `none` using
   `methodology/coding_rubric.txt` (we used Claude Sonnet 4.6 @ temp 0 as the judge; human
   coders or another model also work).
3. Compute each condition's enforcement share (`mixed` = ½) and a chi-square on
   condition × code. Compare to the human baseline (74% / 56%).

---

## Caveats

- The judge is a language model, not the paper's two human coders. We fixed it (Sonnet 4.6 @
  temp 0) and used one rubric for every model, but borderline-balanced answers can be coded
  inconsistently (see the Sonnet note above) — inspect `raw/trials.csv` to audit.
- Models tend to answer with comprehensive "do both" packages, which is why much of the data
  lands in `mixed`.
- Single scenario (Addison, the paper's Experiment 1). Results will shift with model versions
  and wording. This shows current models resist *this* framing — not that LLMs are immune to
  metaphor in general.

## Citation

Original study: Thibodeau, P. H., & Boroditsky, L. (2011). Metaphors We Think With: The Role
of Metaphor in Reasoning. *PLoS ONE, 6*(2), e16782.
https://doi.org/10.1371/journal.pone.0016782

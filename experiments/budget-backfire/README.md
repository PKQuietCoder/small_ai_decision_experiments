# When Budgeting Backfires, for Agents. Data Package (`budget-backfire`)

A self-contained, replication-ready package for our agentic rerun of **Larson, J. S., &
Hamilton, R. (2012). *When Budgeting Backfires: How Self-Imposed Price Restraints Can Increase
Spending.* Journal of Marketing Research, 49(2), 218-230**, with a direct comparison to the
paper's human baseline.

Everything you need to inspect, re-analyze, or independently replicate the study is here: the
methodology (scenario, products, tools, step structure, human baseline), the raw per-trial data
(every chosen product plus the planned budget and the step sequence the model took), and the
aggregated results.

The human finding: when a shopper states a planned spend before choosing, that single extra step
splits one decision into two, shifts attention from price to quality, and the shopper ends up
buying a pricier item. We ask whether an agent does the same when it takes more tool-calling
steps before it buys.

---

## Methodology

**Design.** A faithful translation of the paper's **Experiment 1** (the four-pen choice) into an
agentic decision. The model is given four retractable pens and told to buy exactly one. Pricier
pens are described as higher quality, matching the paper's pretested ordering.

| id | price | quality |
|---|---|---|
| `pen_099` | $0.99 | basic |
| `pen_199` | $1.99 | better |
| `pen_299` | $2.99 | premium |
| `pen_399` | $3.99 | top tier |

The only thing that varies between conditions is the **step structure**: how many tool calls the
model takes before it commits. Each condition is one cell.

| condition | steps | maps to |
|---|---|---|
| `no_restraint` | `choose_product` | human no-restraint group |
| `salient_restraint` | `set_budget` then `choose_product` | human salient-restraint group |
| `many_steps` | `set_budget`, `inspect_options`, `compare_options`, `choose_product` | maximal partitioning |
| `free_agent` | autonomous (all tools offered, none forced) | the model's own default behavior |

**How the agent runs.** Every step is a real tool call in a multi-turn Anthropic conversation.
In the three forced conditions, each tool is pinned in order with `tool_choice` plus
`disable_parallel_tool_use`, so one step is exactly one tool call. The budget the model names is
its own and is non-binding, like a "target" restraint for human shoppers. The `choose_product`
tool uses **strict tool use**, so its output always satisfies the schema. The full tool
definitions are in `methodology/tools.json`; the per-condition step sequences are in
`methodology/conditions.json`; the rendered scenarios are in `methodology/prompt_<condition>.txt`.

The `free_agent` condition is different in kind. It offers all four tools and forces nothing, so
the model decides how many steps to take and whether to budget at all. The three forced
conditions test the causal effect of partitioning. The autonomous condition is observational: it
shows what the model does on its own.

**Models (subjects).** Claude Opus 4.8 and Claude Sonnet 4.6. **50 trials per condition, per
model.** Opus 4.8 rejects the `temperature` parameter, so its run used the model's default
sampling. The Sonnet 4.6 run applied `temperature 1.0` (Anthropic's maximum) to check whether
sampling variance changes anything. It doesn't.

**Human baseline (paper, Exp. 1).** Choice shares over the four pens. No restraint: 61.4 / 15.9 /
20.5 / 2.3 %, mean spend about $1.64. Salient restraint: 41.5 / 19.5 / 26.8 / 12.2 %, mean spend
about $2.10. See `methodology/human_baseline.json`.

**Significance tests.** Per model: a chi-square test of independence on the
condition x product table, and a Welch t-test comparing mean spend in `no_restraint` versus
`salient_restraint` (the paper's headline measure). Both are in `results/significance.csv`.

---

## Results (summary)

Mean spend, no-budget versus budget-first, per source:

| Source | No budget | Budget first | Backfire? |
|---|---:|---:|---|
| **Humans (L&H 2012)** | **~$1.64** | **~$2.10** | yes, spend more with a budget |
| Claude Opus 4.8 (default sampling) | $2.01 | $1.99 | no (Welch *t* = 1.0, *p* = .32) |
| Claude Sonnet 4.6 (temperature 1.0) | $2.03 | $1.99 | no (Welch *t* = 1.43, *p* = .16) |

The human backfire does not transfer. Both models park on the **$1.99** pen almost regardless of
condition: Opus chooses it 98 to 100% of the time, Sonnet 86 to 100%. Adding steps gives the
model more room to deliberate, but it doesn't move the purchase.

Two things worth noting. First, the autonomous `free_agent` condition shows the model's default:
in every trial both models set a budget, reviewed the options, and only then chose, a four-step
budget-first path. The model volunteers the very deliberation that backfires on people, then buys
the same pen anyway. Second, Sonnet's overall condition x product chi-square does cross
significance (*p* = .0016), but that is a sensitivity artifact, not a backfire: the no-budget and
autonomous conditions occasionally reach for the $2.99 pen while the budget-first conditions stay
locked on $1.99, so the budget step makes the model *more* concentrated on the cheaper pen, not
less. The comparable mean-spend t-test stays null.

A reliability note on the Sonnet run. At `temperature 1.0`, when forced to choose in a single
cold step, Sonnet sometimes emitted a `choose_product` call with the required field empty. Strict
tool use fixed it: all 200 trials are valid, and the result didn't change. The Opus run completed
199 of 200 trials (one provider error).

Full numbers: `results/summary_by_condition.csv` and `results/significance.csv`.

**Takeaway.** Don't assume an agent inherits a human debiasing trick. For people, naming a budget
is a lever that can backfire. For these models, partitioning the decision was neither help nor
harm. It was inert.

---

## Package contents

```
budget-backfire/
├── README.md                       # this file
├── manifest.json                   # machine-readable index (models, runs, tools, products, baseline)
├── methodology/
│   ├── budget-backfire.yaml        # exact experiment config (methodology as code)
│   ├── prompt_<condition>.txt      # rendered scenario each condition saw
│   ├── tools.json                  # the four tool definitions (schemas, strict flag)
│   ├── products.json               # the four pens (id, price, quality)
│   ├── conditions.json             # each condition's step sequence / autonomous mode
│   └── human_baseline.json         # L&H (2012) Exp. 1 choice shares + source
├── raw/
│   ├── runs/<model>__<runId>.json  # full per-trial raw data incl. budget, steps, transcript
│   └── trials.csv                  # all trials flattened (see dictionary below)
├── results/
│   ├── analysis/<model>__<runId>.json  # aggregated analysis per model (counts, proportions,
│   │                                   # Wilson CIs, chi-square, meanSpend, stepProfile, baseline)
│   ├── summary_by_condition.csv    # per source × condition: counts, shares, mean price, steps
│   └── significance.csv            # per model: chi-square + mean-spend t-test
├── followups/
│   └── README.md                   # planned follow-up controls (not yet run)
└── budget-backfire-data-package.zip # everything above, zipped for download
```

### Data dictionary, `raw/trials.csv`
| column | meaning |
|---|---|
| `experiment` | experiment id (`budget-backfire`) |
| `model` / `provider` | subject model label / provider |
| `condition` | `no_restraint` / `salient_restraint` / `many_steps` / `free_agent` |
| `trial` | trial index (0 to 49) within the model × condition cell |
| `chosen_product` | the pen id the model bought |
| `price_usd` | the price of the chosen pen |
| `planned_budget` | the budget the model named in `set_budget`, if that step ran (else blank) |
| `num_steps` | how many tool calls the model made before finishing |
| `steps` | the ordered tool sequence, pipe-separated (e.g. `set_budget|choose_product`) |
| `capped` | true if the autonomous loop hit the step cap and was forced to finish |
| `ok` | whether the trial completed without error |
| `error` | the provider error message, if the trial failed |

### Data dictionary, `results/summary_by_condition.csv`
`source` (model or "Humans …"), `condition`, `n`, then for each pen a `<id>_count` and a
`<id>_share_pct`, then `mean_price_usd`, `mean_steps`, and `budget_rate_pct` (share of trials that
called `set_budget`). Human rows carry only the per-pen shares and an implied `mean_price_usd`
computed from those shares.

---

## How to replicate

**With this repository's pipeline** (needs `ANTHROPIC_API_KEY`):

```bash
# one model per run; pick opus or sonnet (Opus ignores temperature; Sonnet honors it)
python -m server.run_experiment budget-backfire --model sonnet --no-post

# regenerate this data package after runs:
python -m server.export_experiment budget-backfire
```

The experiment is fully specified by `methodology/budget-backfire.yaml`.

**Independently, or with another stack.** Everything you need is provider-agnostic:
1. Give the subject model the scenario in `methodology/` and the four tools in `tools.json`.
2. Run each condition 50 times. For the forced conditions, pin the tool sequence in
   `conditions.json` (one tool per turn). For `free_agent`, offer all tools and force nothing,
   then record the sequence the model takes.
3. Record the chosen pen, the planned budget, and the step count per trial.
4. Compute each condition's choice shares and mean spend, a chi-square on condition × product,
   and a t-test on `no_restraint` versus `salient_restraint` mean spend. Compare to the human
   baseline ($1.64 versus $2.10).

---

## Caveats

- This is two Anthropic models, one scenario, and Anthropic's tool API only. Results will shift
  with model versions, wording, and provider.
- The three forced conditions are a controlled partitioning manipulation, not a study of
  open-ended agency. Read `free_agent` as observational.
- Larson and Hamilton's study is well known, so a capable model may recognize the paradigm. A
  disguised, agent-native version with no published human baseline is planned to bound this. See
  `followups/README.md`.
- There is no judge model here. The decision is read straight from a constrained tool field, never
  parsed from prose, so there is no coding step to introduce noise.

## Citation

Original study: Larson, J. S., & Hamilton, R. (2012). When Budgeting Backfires: How Self-Imposed
Price Restraints Can Increase Spending. *Journal of Marketing Research, 49*(2), 218-230.
https://doi.org/10.1509/jmr.10.0148

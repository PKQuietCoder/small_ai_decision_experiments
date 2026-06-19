# Borrowed Instincts

Classic experiments and methods, run on people and rerun on language models and agents.

We like to think we reason our way to decisions. Decades of research says we mostly follow hidden
rules, and those rules are predictable and often counterintuitive. A number you saw first drags the
next one toward it. The way a question is framed flips the answer. Naming a budget makes you spend
more, not less.

Today we hand more of those decisions to language models, and to agents that decide over several
steps. We don't actually know what rules they follow. Some they may inherit from us. Some they may
invent on their own.

This project takes one classic human-bias experiment at a time, reruns it on a current model or
agent through its live API, and asks a simple question: does the model copy our bias, smooth it out,
or make it worse? Every result is backed by real A/B tests and significance checks. Every prompt,
trial, and analysis ships in the open, so anyone can check the work or run it again.

## How it works

An experiment is a single YAML file. Everything else is derived from it and saved as files on disk.
There's no database.

1. **Define** the study in `content/experiments/<id>.yaml`: the scenario, the conditions (what
   changes between cells), the models, and the human baseline from the original paper.
2. **Run** it. The engine executes every model x condition x trial against the real provider APIs
   and writes raw per-trial data to `content/runs/<id>/`.
3. **Analyze.** Each run is aggregated into proportions, Wilson confidence intervals, and
   significance tests (chi-square, Welch t-test) in `content/analysis/<id>/`.
4. **Write up.** A plain-language post in `content/posts/<id>.md` renders with live charts from that
   analysis.
5. **Package.** `export_experiment` bundles the whole study into a self-contained
   `experiments/<id>/` folder that anyone can download and replicate.

Two experiment shapes exist today. A single-shot coded choice, where a model answers and a fixed
judge model codes the answer into categories. And a multi-step agentic decision, where the model
makes a sequence of real tool calls and its final pick is read from a constrained field.

## Repository layout

```
.
├── content/                  # all site content, as files on disk (no database)
│   ├── experiments/          # one YAML per experiment: the experiment as code
│   ├── runs/<id>/            # raw per-trial output, one JSON per run
│   ├── analysis/<id>/        # aggregated stats per run (drives the charts)
│   └── posts/                # the write-ups (Markdown + frontmatter)
├── experiments/<id>/         # downloadable, replication-ready data packages  <- start here
│   ├── README.md             # design, results, and how to replicate
│   ├── manifest.json         # machine-readable index
│   ├── methodology/          # config, rendered prompts, tools, human baseline, rubric
│   ├── raw/                  # per-trial data: runs/*.json + a flat trials.csv
│   ├── results/              # analysis JSON + summary/significance CSVs
│   └── <id>-data-package.zip # everything above, zipped for one download
├── server/                   # Python: FastAPI API + the experiment engine
│   ├── app/                  # API handlers, content store, config
│   ├── experiments/          # engine, llm_clients, model_catalog, stats, post_generator
│   ├── run_experiment.py     # run one model across an experiment
│   ├── export_experiment.py  # build an experiments/<id>/ package from the runs
│   └── serve.py              # run the API
├── artifacts/client/         # React + Vite frontend (the website)
├── scripts/                  # tooling
├── CLAUDE.md, replit.md      # operating notes and architecture decisions
└── pyproject.toml, package.json   # Python (uv) and JS (pnpm) projects
```

## The experiments/ packages (start here to replicate)

This is the part built for other people. Each `experiments/<id>/` folder is a self-contained,
replication-ready package with its own README, and you don't need this codebase to use it.
Everything in it is provider-agnostic.

```
experiments/<id>/
├── README.md             # read this first: design, results, data dictionaries, how to replicate
├── manifest.json         # models, run ids, conditions, human baseline, generated-at
├── methodology/          # the experiment as code (YAML) + the exact rendered prompts,
│                         #   the tool definitions or judge rubric, and the human baseline
├── raw/
│   ├── runs/<model>__<runId>.json   # full per-trial data (every answer or tool transcript)
│   └── trials.csv                   # all trials flattened into one tidy table
├── results/
│   ├── analysis/<model>__<runId>.json   # counts, proportions, CIs, significance, baseline overlay
│   ├── summary_by_condition.csv         # per source x condition: counts, shares, key metric
│   └── significance.csv                 # the statistical tests, per model
└── followups/            # extra controls when a study has them
```

Open the folder's `README.md` first. It explains the design, shows the exact prompts, reports the
results, and walks through replication both with this repo and with any other stack.

Currently published:

- [`experiments/crime-metaphor/`](experiments/crime-metaphor/) is a rerun of Thibodeau and
  Boroditsky (2011), the crime-as-beast-versus-virus framing study, on six models, plus three
  contamination controls (recognition, a novel stimulus, and a paraphrase). Write-up:
  [`content/posts/the-metaphor-trap.md`](content/posts/the-metaphor-trap.md).
- [`experiments/budget-backfire/`](experiments/budget-backfire/) translates Larson and Hamilton
  (2012), "When Budgeting Backfires," into an agentic decision on Claude Opus 4.8 and Sonnet 4.6.
  Write-up: [`content/posts/budget-backfire.md`](content/posts/budget-backfire.md).

## Run or replicate it yourself

### With this repository

Prerequisites: Python (managed with `uv`), Node (managed with `pnpm`), and provider API keys.

```bash
uv sync
pnpm install
export ANTHROPIC_API_KEY=...     # and OPENAI_API_KEY for the GPT models
```

Run one model across an experiment (one model per run):

```bash
python -m server.run_experiment <id> --model <key> --no-post
#   <key>: opus | sonnet | haiku | gpt-5.5 | gpt-5.4 | gpt-5.4-mini
```

Rebuild the downloadable data package after your runs:

```bash
python -m server.export_experiment <id>
```

Serve the site locally:

```bash
python server/serve.py                                          # API (PORT defaults to 8080)
PORT=5173 BASE_PATH=/ pnpm --filter @workspace/client run dev   # website
```

### Independently, with any stack

You don't need this code. Inside any `experiments/<id>/` package:

1. Send each model the prompts in `methodology/`, the number of trials per condition stated in the
   README.
2. Record each trial's decision. For agentic studies, also record the step sequence and any budget
   the model set.
3. Compute the choice shares and the significance test, then compare against the human baseline in
   `methodology/human_baseline.json`.

The package README spells this out for that specific study.

## A note on trust

This is an independent, one-person project, so mistakes happen. A prompt that leaks a cue. A judge
that miscodes a borderline answer. A p-value read too kindly. That's exactly why everything is open.
Rerun an entry, recode it, or check the numbers, and if you get a different result, please say so.
Critique and independent replication are the whole point.

## Stack

A Python and FastAPI backend with the experiment engine, and a React, Vite, and Recharts frontend.
No database and no auth. All content lives as files on disk. LLM calls go through the official
OpenAI and Anthropic SDKs. See [`CLAUDE.md`](CLAUDE.md) and [`replit.md`](replit.md) for operating
notes and the architecture decisions behind this.

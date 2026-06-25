# Experiments

This directory holds the **self-contained, replication-ready data packages** for
each published study — the part built for other people. Each `experiments/<id>/`
folder stands alone: you do not need this codebase to use it, and everything in it
is provider-agnostic.

Each package contains a `manifest.json` (read it first: models, run ids,
conditions, human baseline), a `methodology/` folder (the experiment as code plus
the exact rendered prompts, tool definitions or judge rubric, and human baseline),
`raw/` per-trial data (JSON + a tidy `trials.csv`), `results/` (analysis JSON +
summary and significance CSVs), and a `README.md` walking through the design,
results, and how to replicate. For how a study is authored and packaged, see
[`../docs/experiment-guide.md`](../docs/experiment-guide.md).

## Published studies

### Choice — the attraction (decoy) effect

How a worthless, dominated option still bends a choice between two real ones.
Both packages rerun **Huber, Payne & Puto (1982)**; together they form the
two-part write-up
[`content/posts/decoy-effect.md`](../content/posts/decoy-effect.md).

| Study | Package | What it adds |
|---|---|---|
| Replication | [`decoy-effect/`](decoy-effect/) | The faithful original — six categories, four decoy placements — across six models (the Claude family + three GPT-5 models), 5,400 trials. The decoy is almost never chosen, yet range decoys reliably pull toward the target and frequency decoys split Claude from GPT-5. |
| Agentic extension | [`decoy-effect-agentic/`](decoy-effect-agentic/) | The same choice under four agentic scaffolds (single-shot, forced workflow, autonomous, retrieval) on Opus 4.8, 1,800 trials. *How* the agent deliberates changes which way the decoy bends the choice. |

## More to come

Further studies — additional classic biases, rerun on models and agents — are in
progress and will be added here as each write-up is published. The pipeline,
conventions, and how to propose one are in
[`../docs/experiment-guide.md`](../docs/experiment-guide.md) and
[`../CONTRIBUTING.md`](../CONTRIBUTING.md).

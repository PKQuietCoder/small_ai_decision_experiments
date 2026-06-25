# Authoring an experiment

An experiment is one YAML file in `content/experiments/<id>.yaml`. This guide
covers how to write it, validate it, run it, and package it. For how the pieces
fit together, see [architecture.md](architecture.md).

## 1. Write the config

Start from an existing study of the same `type` and adapt it — the published
[`content/experiments/decoy-effect.yaml`](../content/experiments/decoy-effect.yaml)
is a good `fill_in_blank_decision` template. The fields, validated by
`server/experiments/schemas.py`:

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Slug; must match the filename. |
| `title` | yes | Human title for the study. |
| `type` | yes | `fill_in_blank_decision` \| `open_response` \| `agentic_budget`. |
| `status` | yes | `draft` until the write-up is ready, then `published`. |
| `summary`, `hypothesis` | recommended | Plain-language framing. |
| `models` | yes | List of `{provider, model, label}`. One model per run (see below). |
| `trials_per_cell` | yes | Trials per model × variant cell. |
| `temperature` | yes | Sampling temperature (ignored by models that reject it). |
| `decision_options` | yes | The coded categories: `{id, label}`. |
| `primary_decision` | yes | The option id the headline metric tracks. |
| `prompt_template` | yes | Braces only for variant field placeholders. |
| `variants` | yes | One per experimental cell; each carries its own fields. |
| `baseline` | recommended | Human baseline from the source paper, per variant. |

Type-specific fields:

- **`open_response`** — `question`, a `coder:` judge config (`{key, label,
  temperature, rubric}`), and `max_response_tokens`.
- **`agentic_budget`** — `decision_key`, `max_steps`, `tools` (JSON-schema tool
  definitions), and `products`. Variants set `steps` (a forced tool sequence) or
  `mode: auto` (autonomous), and may carry a `catalog` for retrieval arms.

Any field not listed above is preserved (the schema allows extras), so
experiment-specific variant fields are fine.

## 2. Validate it

The config is validated automatically on load, but check it explicitly before a
run so a typo costs nothing:

```bash
python -c "from server.app import content_store; content_store.load_experiment_config('<id>')"
```

A malformed config raises a clear `Invalid experiment config for '<id>': …`
instead of failing partway through a run.

## 3. Run it

One model per run; the CLI overrides the YAML `models:` list with the single
selected catalog model.

```bash
python -m server.run_experiment <id> --model <key> --no-post
#   <key> ∈ opus | sonnet | haiku | gpt-5.5 | gpt-5.4 | gpt-5.4-mini
```

Requires the relevant provider key (`ANTHROPIC_API_KEY` / `OPENAI_API_KEY`; see
[`../.env.example`](../.env.example)). A run is hundreds of foreground API calls
and must finish within the shell call — do not background it. Confirm the output
reports `N/N trials parsed successfully` with `parseFailures: 0` and a low
`excluded` count, then inspect `content/analysis/<id>/<runId>.json`.

> `run_experiment` regenerates the draft post and will overwrite hand-edits
> unless you pass `--keep-post` (refresh the `runId` only) or `--no-post`.
> Curated posts are hand-written — re-run with `--no-post`.

## 4. Write up and publish

Edit `content/posts/<slug>.md`. A post is public only when its frontmatter has
`published: true`; drafts are served only in the dev workspace with `?preview=1`,
never in a deployment. Keep the restrained editorial voice
([design-system rules](../.claude/rules/design-system.md)).

## 5. Package it (with its README)

```bash
python -m server.export_experiment <id>
```

This builds the self-contained, downloadable package under `experiments/<id>/`
(methodology, raw data, results, manifest, zip). The export **preserves a
hand-written `README.md`** in the package, so write one — describe the design,
the human baseline, the results, and how to replicate independently. Use
[`experiments/budget-backfire/README.md`](../experiments/budget-backfire/README.md)
as the model for tone and structure.

Finally, add the study to the index in
[`experiments/README.md`](../experiments/README.md) so it is discoverable, and
link its write-up from the main [README](../README.md) when it goes public.

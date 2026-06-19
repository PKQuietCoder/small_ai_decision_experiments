"""CLI to run an experiment and generate its draft post.

Admins run this from the Replit shell — it is never exposed to the public UI.

Usage:
    python -m server.run_experiment <experiment_id> [--model <key>] [--no-post] [--keep-post]

    <experiment_id>   The experiment config filename stem under content/experiments/
    --model <key>     Run a single model from the catalog (opus, sonnet, haiku,
                      gpt-5.5, gpt-5.4, gpt-5.4-mini). Omit to pick interactively.
    --no-post         Run the experiment but do not (re)generate the Markdown post
    --keep-post       Preserve an existing post's edits/published flag (only update runId)

Examples:
    python -m server.run_experiment crime-metaphor --model opus
    python -m server.run_experiment crime-metaphor            # interactive menu
"""

from __future__ import annotations

import argparse
import sys
from typing import Any, Dict, Optional

from server.app import content_store
from server.app.content_store import load_experiment_config
from server.experiments import model_catalog
from server.experiments.engine import run_experiment
from server.experiments.post_generator import generate_post


def select_model(model_key: Optional[str]) -> Optional[Dict[str, Any]]:
    """Resolve a single catalog model, prompting interactively if needed.

    Returns the resolved model config, or ``None`` if selection failed (caller
    should treat that as an error and exit non-zero).
    """
    if model_key is not None:
        resolved = model_catalog.resolve(model_key)
        if resolved is None:
            valid = ", ".join(model_catalog.ORDER)
            print(
                f"Unknown model '{model_key}'. Choose one of: {valid}",
                file=sys.stderr,
            )
        return resolved

    if not sys.stdin.isatty():
        print(
            "No --model given and no interactive terminal. "
            f"Pass --model <{ '|'.join(model_catalog.ORDER) }>.",
            file=sys.stderr,
        )
        return None

    print("Select a model to run:")
    for line in model_catalog.menu_lines():
        print(line)
    choice = input("> ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(model_catalog.ORDER):
        return model_catalog.resolve(model_catalog.ORDER[int(choice) - 1])
    resolved = model_catalog.resolve(choice)  # also accept a key typed directly
    if resolved is None:
        print(f"Invalid selection: {choice!r}", file=sys.stderr)
    return resolved


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run an LLM decision-science experiment.")
    parser.add_argument("experiment_id", help="Experiment config stem (content/experiments/<id>.yaml)")
    parser.add_argument(
        "--model",
        help=(
            "Catalog model to run (one of: "
            + ", ".join(model_catalog.ORDER)
            + "). Omit to choose interactively."
        ),
    )
    parser.add_argument("--no-post", action="store_true", help="Skip post generation")
    parser.add_argument(
        "--keep-post",
        action="store_true",
        help="Do not overwrite an existing post; only refresh its runId",
    )
    args = parser.parse_args(argv)

    experiment = load_experiment_config(args.experiment_id)
    if experiment is None:
        print(f"Experiment '{args.experiment_id}' not found.", file=sys.stderr)
        return 1

    model_cfg = select_model(args.model)
    if model_cfg is None:
        return 1
    # Single model per run: the chosen catalog entry replaces the config's
    # `models` list so the run, analysis, and post are all keyed to one model.
    experiment["models"] = [model_cfg]

    print(f"Running experiment: {experiment.get('title', args.experiment_id)}")
    print(f"Model: {model_cfg['label']} ({model_cfg['provider']}:{model_cfg['model']})")
    run = run_experiment(experiment, progress=lambda message: print("  " + message))

    ok = sum(1 for trial in run["trials"] if trial.get("ok"))
    total = len(run["trials"])
    print(f"Completed: {ok}/{total} trials parsed successfully.")

    analysis = content_store.build_analysis(experiment, run)
    analysis_path = content_store.save_analysis(
        experiment["id"], run["runId"], analysis
    )
    print(f"Analysis written to: {analysis_path}")

    if not args.no_post:
        path = generate_post(experiment, run, overwrite=not args.keep_post)
        print(f"Draft post written to: {path}")
        print("Review it, then set 'published: true' in the frontmatter to publish.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

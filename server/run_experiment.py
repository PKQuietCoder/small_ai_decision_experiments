"""CLI to run an experiment and generate its draft post.

Admins run this from the Replit shell — it is never exposed to the public UI.

Usage:
    python -m server.run_experiment <experiment_id> [--model <key>] [--no-post] [--keep-post]
                                                    [--dry-run] [--only E0 E3 ...]

    <experiment_id>   The experiment config filename stem under content/experiments/
    --model <key>     Run a single model from the catalog (opus, sonnet, haiku,
                      gpt-5.5, gpt-5.4, gpt-5.4-mini, jev). Omit to pick interactively.
    --no-post         Run the experiment but do not (re)generate the Markdown post
    --keep-post       Preserve an existing post's edits/published flag (only update runId)
    --dry-run         systemone_probe only: print every request body as JSON and exit
                      without calling the API
    --only <tags>     systemone_probe only: run just the variants whose `experiment`
                      tag is listed (e.g. --only E0 for the repeatability baseline)

Examples:
    python -m server.run_experiment crime-metaphor --model opus
    python -m server.run_experiment crime-metaphor            # interactive menu
    python -m server.run_experiment jev-average-human --model jev --dry-run
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, Optional

from server.app import content_store
from server.app.content_store import load_experiment_config
from server.experiments import model_catalog
from server.experiments.engine import build_probe_requests, run_experiment
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
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="systemone_probe only: print the request bodies and exit (no API calls)",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        metavar="TAG",
        help="systemone_probe only: run just variants with these `experiment` tags",
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

    # A System One probe can only run on a TypeSafe model and vice versa; catch
    # the mismatch here rather than as N failed trials.
    is_probe = experiment.get("type") == "systemone_probe"
    if is_probe != (model_cfg["provider"] == "typesafe"):
        print(
            f"Model '{model_cfg['label']}' ({model_cfg['provider']}) cannot run a "
            f"'{experiment.get('type')}' experiment.",
            file=sys.stderr,
        )
        return 1
    if (args.dry_run or args.only) and not is_probe:
        print("--dry-run/--only apply only to systemone_probe experiments.", file=sys.stderr)
        return 1

    if args.only:
        experiment["variants"] = [
            v for v in experiment.get("variants", []) if v.get("experiment") in args.only
        ]
        if not experiment["variants"]:
            print(f"No variants tagged {args.only}.", file=sys.stderr)
            return 1

    if args.dry_run:
        requests = build_probe_requests(experiment, model_cfg["model"])
        for spec in requests:
            print(f"# {spec['experiment']} · {spec['variant_id']} · trials={spec['trials']}")
            print(json.dumps(spec["body"], indent=2, ensure_ascii=False))
        calls = sum(spec["trials"] for spec in requests)
        print(f"# {len(requests)} variants, {calls} API calls. No requests were sent.")
        return 0

    print(f"Running experiment: {experiment.get('title', args.experiment_id)}")
    print(f"Model: {model_cfg['label']} ({model_cfg['provider']}:{model_cfg['model']})")
    run = run_experiment(experiment, progress=lambda message: print("  " + message))

    ok = sum(1 for trial in run["trials"] if trial.get("ok"))
    total = len(run["trials"])
    print(f"Completed: {ok}/{total} trials parsed successfully.")
    if is_probe and run.get("spend"):
        spend = run["spend"]
        print(f"TypeSafe calls: {spend['calls']}, estimated spend: ${spend['estimatedUsd']:.5f}")

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

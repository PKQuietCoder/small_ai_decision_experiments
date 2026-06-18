"""CLI to run an experiment and generate its draft post.

Admins run this from the Replit shell — it is never exposed to the public UI.

Usage:
    python -m server.run_experiment <experiment_id> [--no-post] [--keep-post]

    <experiment_id>   The experiment config filename stem under content/experiments/
    --no-post         Run the experiment but do not (re)generate the Markdown post
    --keep-post       Preserve an existing post's edits/published flag (only update runId)

Examples:
    python -m server.run_experiment metaphor-effect
"""

from __future__ import annotations

import argparse
import sys

from server.app.content_store import load_experiment_config
from server.experiments.engine import run_experiment
from server.experiments.post_generator import generate_post


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run an LLM decision-science experiment.")
    parser.add_argument("experiment_id", help="Experiment config stem (content/experiments/<id>.yaml)")
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

    print(f"Running experiment: {experiment.get('title', args.experiment_id)}")
    run = run_experiment(experiment, progress=lambda message: print("  " + message))

    ok = sum(1 for trial in run["trials"] if trial.get("ok"))
    total = len(run["trials"])
    print(f"Completed: {ok}/{total} trials parsed successfully.")

    if not args.no_post:
        path = generate_post(experiment, run, overwrite=not args.keep_post)
        print(f"Draft post written to: {path}")
        print("Review it, then set 'published: true' in the frontmatter to publish.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

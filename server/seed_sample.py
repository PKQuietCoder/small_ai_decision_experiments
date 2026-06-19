"""Generate a synthetic sample run + draft post for local development.

This is ONLY for bootstrapping the UI before real API keys are configured. It
fabricates plausible (not real) trial data so the frontend has something to
render. Replace it with a real run via ``python -m server.run_experiment`` once
keys are available. Synthetic posts are marked clearly and left unpublished.

Usage:
    python -m server.seed_sample crime-metaphor
"""

from __future__ import annotations

import random
import sys
from datetime import datetime, timezone

from server.app.content_store import load_experiment_config
from server.experiments.engine import save_run
from server.experiments.post_generator import generate_post


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    experiment_id = argv[0] if argv else "crime-metaphor"
    experiment = load_experiment_config(experiment_id)
    if experiment is None:
        print(f"Experiment '{experiment_id}' not found.", file=sys.stderr)
        return 1

    rng = random.Random(42)
    decision_ids = [opt["id"] for opt in experiment["decision_options"]]
    trials_per_cell = int(experiment.get("trials_per_cell", 25))
    started = datetime.now(timezone.utc)

    trials = []
    for model_cfg in experiment["models"]:
        label = model_cfg.get("label", model_cfg["model"])
        for variant in experiment["variants"]:
            # Uniform over whatever decision options this experiment defines —
            # synthetic data just needs to populate the UI, not be realistic.
            weights = [1.0] * len(decision_ids)
            for trial_no in range(trials_per_cell):
                decision = rng.choices(decision_ids, weights=weights, k=1)[0]
                trials.append(
                    {
                        "model": label,
                        "provider": model_cfg["provider"],
                        "variantId": variant["id"],
                        "trial": trial_no,
                        "raw": decision,
                        "decision": decision,
                        "ok": True,
                        "synthetic": True,
                    }
                )

    run = {
        "runId": started.strftime("%Y%m%dT%H%M%SZ") + "-sample",
        "experimentId": experiment_id,
        "startedAt": started.isoformat(),
        "finishedAt": datetime.now(timezone.utc).isoformat(),
        "trialsPerCell": trials_per_cell,
        "temperature": experiment.get("temperature", 1.0),
        "models": [m.get("label", m["model"]) for m in experiment["models"]],
        "variants": [v["id"] for v in experiment["variants"]],
        "synthetic": True,
        "trials": trials,
    }
    path = save_run(run)
    print(f"Synthetic run saved to {path}")

    post_path = generate_post(experiment, run, overwrite=True)
    print(f"Draft post written to {post_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

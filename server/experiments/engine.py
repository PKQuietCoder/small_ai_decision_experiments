"""Experiment engine: run an experiment across models x variants x trials.

A "run" executes ``trials_per_cell`` prompts for every (model, variant) pair,
parses each model's chosen decision letter, and writes a single run JSON file to
``content/runs/<experiment_id>/<run_id>.json``.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from ..app import config
from . import llm_clients


def _parse_decision(raw: str, valid_ids: List[str]) -> Optional[str]:
    """Extract the chosen single-letter decision from a raw model response."""
    if not raw:
        return None
    upper = raw.strip().upper()
    # Fast path: response is exactly the letter.
    if upper in valid_ids:
        return upper
    # Otherwise grab the first standalone valid letter.
    match = re.search(r"\b([" + "".join(valid_ids) + r"])\b", upper)
    if match:
        return match.group(1)
    # Last resort: first character if it is a valid option.
    if upper and upper[0] in valid_ids:
        return upper[0]
    return None


def run_experiment(
    experiment: Dict[str, Any],
    progress: Optional[Callable[[str], None]] = None,
) -> Dict[str, Any]:
    """Execute every cell of the experiment and persist the run.

    ``progress`` is an optional callback used by the CLI to print live updates.
    """
    def log(message: str) -> None:
        if progress:
            progress(message)

    prompt_template = experiment["prompt_template"]
    temperature = float(experiment.get("temperature", 1.0))
    trials_per_cell = int(experiment.get("trials_per_cell", 20))
    valid_ids = [opt["id"] for opt in experiment.get("decision_options", [])]
    variants = experiment.get("variants", [])
    models = experiment.get("models", [])

    started_at = datetime.now(timezone.utc)
    run_id = started_at.strftime("%Y%m%dT%H%M%SZ")
    trials: List[Dict[str, Any]] = []

    total_cells = len(models) * len(variants)
    cell_index = 0

    for model_cfg in models:
        provider = model_cfg["provider"]
        model_name = model_cfg["model"]
        model_label = model_cfg.get("label", model_name)
        for variant in variants:
            cell_index += 1
            log(
                f"[{cell_index}/{total_cells}] {model_label} x "
                f"{variant.get('label', variant['id'])} ..."
            )
            prompt = prompt_template.format(metaphor=variant["metaphor"])
            for trial_no in range(trials_per_cell):
                record: Dict[str, Any] = {
                    "model": model_label,
                    "provider": provider,
                    "variantId": variant["id"],
                    "trial": trial_no,
                }
                try:
                    raw = llm_clients.complete(
                        provider, model_name, prompt, temperature
                    )
                    decision = _parse_decision(raw, valid_ids)
                    record["raw"] = raw
                    record["decision"] = decision
                    record["ok"] = decision is not None
                    if decision is None:
                        record["error"] = "unparseable"
                except Exception as exc:  # noqa: BLE001 - record provider errors
                    record["raw"] = None
                    record["decision"] = None
                    record["ok"] = False
                    record["error"] = str(exc)
                trials.append(record)

    finished_at = datetime.now(timezone.utc)

    run = {
        "runId": run_id,
        "experimentId": experiment["id"],
        "startedAt": started_at.isoformat(),
        "finishedAt": finished_at.isoformat(),
        "trialsPerCell": trials_per_cell,
        "temperature": temperature,
        "models": [m.get("label", m.get("model")) for m in models],
        "variants": [v["id"] for v in variants],
        "trials": trials,
    }

    save_run(run)
    log(f"Saved run {run_id} ({len(trials)} trials).")
    return run


def save_run(run: Dict[str, Any]) -> Path:
    config.ensure_dirs()
    directory = config.RUNS_DIR / run["experimentId"]
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{run['runId']}.json"
    with path.open("w", encoding="utf-8") as handle:
        json.dump(run, handle, indent=2)
    return path

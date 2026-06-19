"""Experiment engine: run an experiment across models x variants x trials.

A "run" executes ``trials_per_cell`` prompts for every (model, variant) pair,
parses each model's chosen decision letter, and writes a single run JSON file to
``content/runs/<experiment_id>/<run_id>.json``.
"""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from ..app import config
from . import llm_clients, model_catalog

# Independent API calls are run concurrently to keep full runs well within a
# reasonable wall-clock time. Kept modest to avoid provider rate limits.
MAX_WORKERS = 8

# Categories a judge model may assign when coding an open-ended response. The
# first three are kept for analysis; ``none`` (no concrete suggestion) is
# recorded but excluded downstream, mirroring the source study.
CODER_CATEGORIES = ["enforce", "reform", "mixed", "none"]


def _coder_prompt(
    question: str, response_text: str, rubric: Optional[str] = None
) -> str:
    """Build the judge prompt that codes one free-text answer into a category.

    Built by concatenation (never ``str.format``) because ``response_text`` is
    untrusted model output that may contain brace characters.

    ``rubric`` lets an experiment supply its own coding instructions (via the
    YAML ``coder.rubric`` field) when the default crime enforce/reform scheme
    does not apply — e.g. the recognition probe codes recognised/unrecognised.
    When omitted, the original crime rubric below is used unchanged, so existing
    experiments are unaffected. The trusted ``question`` is substituted; the
    untrusted ``response_text`` is only ever appended, never formatted.
    """
    if rubric is not None:
        return (
            rubric.strip()
            + "\n\n"
            + f'For reference, the respondent was asked: "{question}"\n\n'
            + "Respond with only the single category label.\n\n"
            + "--- RESPONSE TO CLASSIFY ---\n"
            + response_text
        )
    return (
        "You are a research assistant coding free-text survey responses for a "
        "study on how people propose to address crime in a city. Identify the "
        "DOMINANT thrust of the response.\n\n"
        f'The respondent was asked: "{question}"\n\n'
        "Categories:\n"
        "- enforce: leads with or emphasizes law enforcement / punishment (more "
        "police, more arrests, crackdowns, harsher sentences, more prisons, "
        "tougher courts, deterrence).\n"
        "- reform: leads with or emphasizes diagnosing or treating root causes / "
        "social reform (investigate underlying causes, education, jobs, poverty, "
        "the economy, housing, healthcare, social programs, community development).\n"
        "- mixed: gives enforcement and reform clearly EQUAL weight, with neither "
        "emphasized or placed first.\n"
        "- none: no concrete suggestion is offered.\n\n"
        "Rules: A response that mentions both but leads with, prioritizes, or "
        "devotes more space to one side is that side — not 'mixed'. Reserve "
        "'mixed' only for genuinely balanced answers. Judge by emphasis and "
        "ordering, not by mere mention.\n\n"
        "Respond with only the single category label.\n\n"
        "--- RESPONSE TO CLASSIFY ---\n"
        f"{response_text}"
    )


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

    # Open-ended experiments: the subject answers in prose and a fixed judge
    # model codes each answer into a category. Resolved once, up front.
    is_open = experiment.get("type") == "open_response"
    judge_cfg: Optional[Dict[str, Any]] = None
    judge_temp = 0.0
    coder_rubric: Optional[str] = None
    coder_categories = CODER_CATEGORIES
    question = experiment.get("question", "")
    max_response_tokens = int(experiment.get("max_response_tokens", 1500))
    if is_open:
        coder = experiment.get("coder") or {}
        judge_cfg = model_catalog.resolve(coder.get("key", "sonnet"))
        if judge_cfg is None:
            raise ValueError(f"Unknown coder model key: {coder.get('key')!r}")
        judge_temp = float(coder.get("temperature", 0.0))
        # Optional per-experiment coding scheme. Defaults to the crime rubric.
        coder_rubric = coder.get("rubric")
        coder_categories = coder.get("categories") or CODER_CATEGORIES

    # Agentic budget experiments: each variant is a step-structure condition that runs
    # a multi-step tool-use conversation. The chosen product id becomes the trial's
    # `decision`, so the downstream analysis (build_analysis) is unchanged.
    is_budget = experiment.get("type") == "agentic_budget"
    tool_defs = experiment.get("tools", [])
    tools_by_name = {t["name"]: t for t in tool_defs}
    decision_key = experiment.get("decision_key", "product_id")
    terminal_tool = next(
        (t["name"] for t in tool_defs if t.get("final")), "choose_product"
    )
    max_steps = int(experiment.get("max_steps", 8))

    started_at = datetime.now(timezone.utc)
    run_id = started_at.strftime("%Y%m%dT%H%M%SZ")
    trials: List[Dict[str, Any]] = []

    total_cells = len(models) * len(variants)

    # Build the full task list up front so independent API calls can run
    # concurrently. ``order`` preserves a deterministic model-major,
    # variant, then trial ordering in the final trials list.
    tasks: List[Dict[str, Any]] = []
    order = 0
    cell_index = 0
    for model_cfg in models:
        model_label = model_cfg.get("label", model_cfg["model"])
        for variant in variants:
            cell_index += 1
            if is_budget:
                # The scenario is shared (brace-free); a variant may override it
                # (e.g. the autonomous condition lists the tools without naming a
                # budget). `steps` resolves to an ordered tool list for forced
                # conditions, or None for `mode: auto` (model self-directs).
                prompt = variant.get("scenario_template") or prompt_template
                if variant.get("mode") == "auto" or not variant.get("steps"):
                    steps = None
                else:
                    steps = [tools_by_name[name] for name in variant["steps"]]
            else:
                # Substitute every string field of the variant, so a template can
                # use {metaphor} (fill-in-blank) or {frame}/{spread} (open-ended).
                fields = {k: v for k, v in variant.items() if isinstance(v, str)}
                prompt = prompt_template.format(**fields)
                steps = None
            for trial_no in range(trials_per_cell):
                tasks.append(
                    {
                        "order": order,
                        "cell_index": cell_index,
                        "cell_label": (
                            f"[{cell_index}/{total_cells}] {model_label} x "
                            f"{variant.get('label', variant['id'])}"
                        ),
                        "model_cfg": model_cfg,
                        "provider": model_cfg["provider"],
                        "model_label": model_label,
                        "variant_id": variant["id"],
                        "trial_no": trial_no,
                        "prompt": prompt,
                        "steps": steps,
                    }
                )
                order += 1

    def run_task(task: Dict[str, Any]) -> Dict[str, Any]:
        record: Dict[str, Any] = {
            "model": task["model_label"],
            "provider": task["provider"],
            "variantId": task["variant_id"],
            "trial": task["trial_no"],
        }
        try:
            if is_open:
                # Subject answers in prose; the fixed judge codes the answer.
                text = llm_clients.respond(
                    task["model_cfg"],
                    task["prompt"],
                    max_output=max_response_tokens,
                    temperature=temperature,
                )
                code, _raw = llm_clients.decide(
                    judge_cfg,
                    _coder_prompt(question, text, coder_rubric),
                    coder_categories,
                    judge_temp,
                )
                record["response"] = text
                record["decision"] = code
                record["ok"] = True
            elif is_budget:
                # Multi-step tool-use conversation; the final pick is the decision.
                decision, transcript = llm_clients.run_tool_sequence(
                    task["model_cfg"],
                    task["prompt"],
                    tool_defs,
                    valid_ids,
                    steps=task["steps"],
                    terminal_tool=terminal_tool,
                    decision_key=decision_key,
                    temperature=temperature,
                    max_steps=max_steps,
                )
                record["decision"] = decision
                record["steps"] = transcript.get("steps", [])
                record["numSteps"] = len(record["steps"])
                record["budget"] = transcript.get("set_budget", {}).get("budget")
                record["capped"] = transcript.get("capped", False)
                record["transcript"] = transcript
                record["ok"] = True
            else:
                decision, raw = llm_clients.decide(
                    task["model_cfg"],
                    task["prompt"],
                    valid_ids,
                    temperature,
                )
                record["raw"] = raw
                record["decision"] = decision
                record["ok"] = True
        except Exception as exc:  # noqa: BLE001 - record provider errors
            record["raw"] = None
            record["decision"] = None
            record["ok"] = False
            record["error"] = str(exc)
        return record

    results: List[Optional[Dict[str, Any]]] = [None] * len(tasks)
    cells_done: set = set()
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_task = {executor.submit(run_task, task): task for task in tasks}
        for future in as_completed(future_to_task):
            task = future_to_task[future]
            results[task["order"]] = future.result()
            cell = task["cell_index"]
            if cell not in cells_done:
                cells_done.add(cell)
                log(f"{task['cell_label']} ...")

    trials = [record for record in results if record is not None]

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

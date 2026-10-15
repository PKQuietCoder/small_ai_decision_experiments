"""Export a self-contained, replication-ready data package for an experiment.

Bundles methodology (config, rendered prompts, coding rubric or tool/step
structure, human baseline), raw per-trial data (model responses or tool
transcripts, JSON + tidy CSV), and results (analysis JSON + summary/significance
CSVs) into ``experiments/<id>/``, plus a single ``<id>-data-package.zip`` for
one-click download.

Regenerates the data files on every run; a hand-written ``README.md`` in the
package (and anything under ``followups/``) is preserved.

Handles two shapes:
  * ``open_response`` / ``fill_in_blank_decision`` (e.g. crime-metaphor): a
    coded categorical decision per trial.
  * ``agentic_budget`` (e.g. decoy-effect-agentic): a multi-step tool-use trial whose
    decision is the chosen product, with extra per-trial fields (planned budget,
    step sequence, capped flag) and a mean-spend metric.
  * ``systemone_probe`` (e.g. jev-average-human): one typed question per variant
    answered with a probability distribution. Methodology ships the exact request
    bodies; ``trials.csv`` is long-format (one row per outcome); results carry the
    ``systemone`` summary block as ``summary.json`` + ``summary.csv``.

Usage:
    python -m server.export_experiment <experiment_id>
    python -m server.export_experiment crime-metaphor
"""

from __future__ import annotations

import csv
import json
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from server.app import content_store
from server.experiments import engine

REPO_ROOT = Path(__file__).resolve().parents[1]


def _slug(text: str) -> str:
    out = []
    for ch in text.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in " ._-":
            out.append("-")
    s = "".join(out)
    while "--" in s:
        s = s.replace("--", "-")
    return s.strip("-")


def _latest_run_per_model(runs: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Keep the most recent run for each model label (runs come sorted oldest→newest)."""
    by_model: Dict[str, Dict[str, Any]] = {}
    for run in runs:
        label = (run.get("models") or ["?"])[0]
        by_model[label] = run
    return by_model


def _enforce_share(counts: Dict[str, int]) -> float:
    """Enforcement share with 'mixed' counted as half (the paper's convention)."""
    denom = counts.get("enforce", 0) + counts.get("reform", 0) + counts.get("mixed", 0)
    if denom == 0:
        return 0.0
    return (counts.get("enforce", 0) + 0.5 * counts.get("mixed", 0)) / denom


def export(experiment_id: str) -> Path:
    experiment = content_store.load_experiment_config(experiment_id)
    if experiment is None:
        raise SystemExit(f"Experiment '{experiment_id}' not found.")

    runs = content_store.list_runs(experiment_id)
    if not runs:
        raise SystemExit(f"No runs found for '{experiment_id}'. Run it first.")
    by_model = _latest_run_per_model(runs)

    pkg = REPO_ROOT / "experiments" / experiment_id
    (pkg / "methodology").mkdir(parents=True, exist_ok=True)
    (pkg / "raw" / "runs").mkdir(parents=True, exist_ok=True)
    (pkg / "results" / "analysis").mkdir(parents=True, exist_ok=True)

    variants = experiment.get("variants", [])
    variant_meta = {v["id"]: v for v in variants}
    question = experiment.get("question", "")
    decision_options = experiment.get("decision_options", [])
    decision_ids = [o["id"] for o in decision_options]
    is_budget = experiment.get("type") == "agentic_budget"
    is_probe = experiment.get("type") == "systemone_probe"
    products = experiment.get("products", [])
    price_of = {p["id"]: p.get("price") for p in products}

    # Compute (and persist) each model's analysis once, reused for results CSVs.
    analyses = {label: content_store.analysis_for(experiment, run) for label, run in by_model.items()}

    # ---- methodology -------------------------------------------------------
    shutil.copyfile(
        content_store.config.EXPERIMENTS_DIR / f"{experiment_id}.yaml",
        pkg / "methodology" / f"{experiment_id}.yaml",
    )
    if is_probe:
        # A probe's "prompt" is the request body itself; ship the exact bytes sent.
        model_id = next(iter(by_model.values())).get("trials", [{}])[0].get("request", {}).get("model")
        for spec in engine.build_probe_requests(experiment, model_id):
            (pkg / "methodology" / f"request_{spec['variant_id']}.json").write_text(
                json.dumps(spec["body"], indent=2, ensure_ascii=False), encoding="utf-8"
            )
    for v in variants:
        if is_probe:
            continue
        if is_budget:
            # A condition's scenario is its override (autonomous) or the shared one.
            rendered = v.get("scenario_template") or experiment.get("prompt_template", "")
        else:
            fields = {k: val for k, val in v.items() if isinstance(val, str)}
            rendered = experiment.get("prompt_template", "").format(**fields)
        (pkg / "methodology" / f"prompt_{v['id']}.txt").write_text(rendered, encoding="utf-8")
    if experiment.get("type") == "open_response":
        rubric = engine._coder_prompt(question, "<<MODEL RESPONSE INSERTED HERE>>")
        (pkg / "methodology" / "coding_rubric.txt").write_text(rubric, encoding="utf-8")
    if is_budget:
        # The agentic structure: the tools the model could call, the products it
        # chose among, and each condition's forced step sequence (or autonomous mode).
        (pkg / "methodology" / "tools.json").write_text(
            json.dumps(experiment.get("tools", []), indent=2), encoding="utf-8"
        )
        (pkg / "methodology" / "products.json").write_text(
            json.dumps(products, indent=2), encoding="utf-8"
        )
        conditions = [
            {
                "id": v["id"],
                "label": v.get("label", v["id"]),
                "mode": v.get("mode", "forced"),
                "steps": v.get("steps") or ("auto" if v.get("mode") == "auto" else []),
            }
            for v in variants
        ]
        (pkg / "methodology" / "conditions.json").write_text(
            json.dumps(conditions, indent=2), encoding="utf-8"
        )
    baseline = experiment.get("baseline")
    if baseline:
        (pkg / "methodology" / "human_baseline.json").write_text(
            json.dumps(baseline, indent=2), encoding="utf-8"
        )

    # ---- raw: per-model run copies + flattened trials.csv -------------------
    trials_rows: List[Dict[str, Any]] = []
    for label, run in by_model.items():
        name = f"{_slug(label)}__{run['runId']}.json"
        (pkg / "raw" / "runs" / name).write_text(json.dumps(run, indent=2), encoding="utf-8")
        for t in run.get("trials", []):
            if is_probe:
                trials_rows.extend(_probe_trial_rows(experiment_id, variant_meta, t))
            elif is_budget:
                trials_rows.append(
                    {
                        "experiment": experiment_id,
                        "model": t.get("model"),
                        "provider": t.get("provider"),
                        "condition": t.get("variantId"),
                        "trial": t.get("trial"),
                        "chosen_product": t.get("decision"),
                        "price_usd": price_of.get(t.get("decision"), ""),
                        "planned_budget": t.get("budget"),
                        "num_steps": t.get("numSteps"),
                        "steps": "|".join(t.get("steps") or []),
                        "capped": t.get("capped"),
                        "ok": t.get("ok"),
                        "error": t.get("error", ""),
                    }
                )
            else:
                vm = variant_meta.get(t.get("variantId"), {})
                trials_rows.append(
                    {
                        "experiment": experiment_id,
                        "model": t.get("model"),
                        "provider": t.get("provider"),
                        "condition": t.get("variantId"),
                        "frame": vm.get("frame", vm.get("metaphor", "")),
                        "spread": vm.get("spread", ""),
                        "trial": t.get("trial"),
                        "code": t.get("decision"),
                        "ok": t.get("ok"),
                        "response": (t.get("response") or t.get("raw") or ""),
                    }
                )
    if is_probe:
        trials_fields = PROBE_TRIAL_FIELDS
    elif is_budget:
        trials_fields = ["experiment", "model", "provider", "condition", "trial",
                         "chosen_product", "price_usd", "planned_budget", "num_steps",
                         "steps", "capped", "ok", "error"]
    else:
        trials_fields = ["experiment", "model", "provider", "condition", "frame",
                         "spread", "trial", "code", "ok", "response"]
    with (pkg / "raw" / "trials.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=trials_fields)
        w.writeheader()
        w.writerows(trials_rows)

    # ---- results: analysis copies + summary + significance CSVs -------------
    for label, run in by_model.items():
        aname = f"{_slug(label)}__{run['runId']}.json"
        (pkg / "results" / "analysis" / aname).write_text(
            json.dumps(analyses[label], indent=2), encoding="utf-8"
        )

    if is_probe:
        _write_probe_results(pkg, experiment_id, variants, analyses)
    elif is_budget:
        _write_budget_results(pkg, experiment_id, variants, decision_ids, price_of,
                              by_model, analyses, baseline)
    else:
        _write_coded_results(pkg, experiment_id, variants, decision_ids,
                             by_model, analyses, baseline)

    # ---- manifest ----------------------------------------------------------
    manifest: Dict[str, Any] = {
        "experiment": experiment_id,
        "title": experiment.get("title", experiment_id),
        "type": experiment.get("type"),
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "models": list(by_model.keys()),
        "trialsPerCell": experiment.get("trials_per_cell"),
        "conditions": [v["id"] for v in variants],
        "runs": {label: run["runId"] for label, run in by_model.items()},
        "humanBaseline": baseline,
    }
    if is_probe:
        manifest["state"] = experiment.get("state")
        manifest["probes"] = sorted({v.get("experiment") for v in variants if v.get("experiment")})
        manifest["callsPerVariant"] = {v["id"]: int(v.get("trials", 1)) for v in variants}
        manifest["responseModels"] = sorted(
            {t.get("responseModel") for run in by_model.values() for t in run.get("trials", []) if t.get("responseModel")}
        )
        manifest["spend"] = {label: run.get("spend") for label, run in by_model.items()}
        manifest["note"] = (
            "TypeSafe's Jev returns a probability distribution per question, so each "
            "variant is a single call (E0 repeats five times). Probabilities are the "
            "API's own; `confidence` is recomputed from TypeSafe's published formulas "
            "as a check (see results/summary.json confidenceCheck)."
        )
    elif is_budget:
        manifest["temperature"] = experiment.get("temperature")
        manifest["maxSteps"] = experiment.get("max_steps")
        manifest["decisionKey"] = experiment.get("decision_key")
        manifest["tools"] = [t["name"] for t in experiment.get("tools", [])]
        manifest["products"] = products
        manifest["note"] = (
            "Opus 4.8 rejects the temperature parameter, so its run used the model's "
            "default sampling; the Sonnet 4.6 run applied temperature 1.0. Forced "
            "tool use is pinned with disable_parallel_tool_use; choose_product uses "
            "strict tool use so the schema is always satisfied."
        )
    else:
        manifest["judge"] = experiment.get("coder")
    (pkg / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # ---- zip (exclude any existing zip to avoid self-inclusion) -------------
    zip_path = pkg / f"{experiment_id}-data-package.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(pkg.rglob("*")):
            if path.is_file() and path.suffix != ".zip":
                zf.write(path, path.relative_to(pkg.parent))

    print(f"Exported package: {pkg}")
    print(f"  models: {', '.join(by_model.keys())}")
    print(f"  trials.csv rows: {len(trials_rows)}")
    print(f"  zip: {zip_path} ({zip_path.stat().st_size // 1024} KB)")
    return pkg


PROBE_TRIAL_FIELDS = [
    "experiment", "model", "provider", "condition", "probe", "organ", "question_type",
    "trial", "outcome", "probability", "choice", "confidence", "score", "noul",
    "response_model", "input_tokens", "latency_ms", "ok", "error",
]


def _probe_trial_rows(experiment_id: str, variant_meta: Dict[str, Any],
                      t: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Long-format rows for one probe trial: one row per option/level/polarity."""
    vm = variant_meta.get(t.get("variantId"), {})
    question = vm.get("question") or {}
    answer = t.get("answer") or {}
    base = {
        "experiment": experiment_id,
        "model": t.get("model"),
        "provider": t.get("provider"),
        "condition": t.get("variantId"),
        "probe": vm.get("experiment", ""),
        "organ": vm.get("organ", ""),
        "question_type": question.get("type", ""),
        "trial": t.get("trial"),
        "choice": answer.get("choice", ""),
        "confidence": answer.get("confidence", ""),
        "score": answer.get("score", ""),
        "noul": answer.get("noul", ""),
        "response_model": t.get("responseModel", ""),
        "input_tokens": (t.get("usage") or {}).get("input_tokens", ""),
        "latency_ms": t.get("latencyMs", ""),
        "ok": t.get("ok"),
        "error": t.get("error", ""),
    }
    if not t.get("ok"):
        return [{**base, "outcome": "", "probability": ""}]
    qtype = question.get("type")
    if qtype == "choice":
        return [
            {**base, "outcome": opt, "probability": p}
            for opt, p in (answer.get("probabilities") or {}).items()
        ]
    if qtype == "score":
        legend = answer.get("legend") or {}
        return [
            {**base, "outcome": legend.get(idx, idx), "probability": p}
            for idx, p in (answer.get("probabilities") or {}).items()
        ]
    p = float(answer.get("noul", 0.0))
    return [
        {**base, "outcome": "true", "probability": p},
        {**base, "outcome": "false", "probability": round(1 - p, 6)},
    ]


def _write_probe_results(pkg, experiment_id, variants, analyses) -> None:
    """summary.json (the analysis's ``systemone`` block) + a per-variant summary.csv.

    No significance.csv: a probe has no sampling distribution to test.
    """
    blocks = {label: a.get("systemone", {}) for label, a in analyses.items()}
    summary = next(iter(blocks.values())) if len(blocks) == 1 else blocks
    (pkg / "results" / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    rows: List[Dict[str, Any]] = []
    for label, block in blocks.items():
        for v in variants:
            s = (block.get("variants") or {}).get(v["id"], {})
            answer = s.get("choice") if s.get("questionType") == "choice" else (
                s.get("score") if s.get("questionType") == "score" else s.get("p")
            )
            rows.append(
                {
                    "experiment": experiment_id,
                    "source": label,
                    "condition": v["id"],
                    "probe": v.get("experiment", ""),
                    "organ": v.get("organ", ""),
                    "question_type": s.get("questionType", ""),
                    "instructions": s.get("instructions", ""),
                    "calls": s.get("trials", 0),
                    "answer": answer,
                    "confidence": s.get("confidence", s.get("confidenceAbs", "")),
                    "probabilities": json.dumps(
                        s.get("probabilitiesByLevel") or s.get("probabilities") or {}
                    ),
                    "mean_latency_ms": s.get("latencyMs", ""),
                }
            )
    with (pkg / "results" / "summary.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(
            fh,
            fieldnames=["experiment", "source", "condition", "probe", "organ", "question_type",
                        "instructions", "calls", "answer", "confidence", "probabilities",
                        "mean_latency_ms"],
        )
        w.writeheader()
        w.writerows(rows)


def _write_coded_results(pkg, experiment_id, variants, decision_ids,
                         by_model, analyses, baseline) -> None:
    """summary_by_condition.csv + significance.csv for coded categorical experiments."""
    cell_rows: List[Dict[str, Any]] = []
    sig_rows: List[Dict[str, Any]] = []
    for label, run in by_model.items():
        analysis = analyses[label]
        for v in variants:
            counts = {d: 0 for d in decision_ids}
            none_n = 0
            for t in run.get("trials", []):
                if not t.get("ok") or t.get("variantId") != v["id"]:
                    continue
                dec = t.get("decision")
                if dec in counts:
                    counts[dec] += 1
                else:
                    none_n += 1
            n = sum(counts.values())
            cell_rows.append(
                {
                    "experiment": experiment_id,
                    "source": label,
                    "condition": v["id"],
                    "n": n,
                    **{f"{d}_count": counts[d] for d in decision_ids},
                    "excluded_none": none_n,
                    "enforce_share_pct": round(_enforce_share(counts) * 100, 1),
                }
            )
        o = analysis.get("overall", {})
        sig_rows.append(
            {
                "experiment": experiment_id,
                "source": label,
                "test": "condition x decision (chi-square of independence)",
                "n": analysis.get("totalTrials"),
                "chi_square": o.get("statistic"),
                "dof": o.get("dof"),
                "p_value": o.get("pValue"),
                "cramers_v": o.get("cramersV"),
                "significant": o.get("significant"),
            }
        )
    if baseline:
        for v in variants:
            b = (baseline.get("by_variant") or {}).get(v["id"])
            if not b:
                continue
            cell_rows.append(
                {
                    "experiment": experiment_id,
                    "source": f"Humans ({baseline.get('source', 'baseline')})",
                    "condition": v["id"],
                    "n": "",
                    **{f"{d}_count": "" for d in decision_ids},
                    "excluded_none": "",
                    "enforce_share_pct": round(float(b.get("enforce", 0)) * 100, 1),
                }
            )
    cell_fields = (
        ["experiment", "source", "condition", "n"]
        + [f"{d}_count" for d in decision_ids]
        + ["excluded_none", "enforce_share_pct"]
    )
    with (pkg / "results" / "summary_by_condition.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cell_fields)
        w.writeheader()
        w.writerows(cell_rows)
    with (pkg / "results" / "significance.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(
            fh,
            fieldnames=["experiment", "source", "test", "n", "chi_square", "dof",
                        "p_value", "cramers_v", "significant"],
        )
        w.writeheader()
        w.writerows(sig_rows)


def _write_budget_results(pkg, experiment_id, variants, decision_ids, price_of,
                          by_model, analyses, baseline) -> None:
    """summary_by_condition.csv + significance.csv for the agentic budget experiment.

    Summary reports per-condition choice counts and shares per product, the mean
    price chosen, and the step trajectory. Significance reports the overall
    condition x product chi-square plus the no-budget vs budget-first mean-spend
    t-test (Larson & Hamilton's headline measure).
    """
    cell_rows: List[Dict[str, Any]] = []
    sig_rows: List[Dict[str, Any]] = []
    for label, run in by_model.items():
        analysis = analyses[label]
        mean_spend = (analysis.get("meanSpend") or {}).get("byVariant", {})
        step_profile = analysis.get("stepProfile", {})
        for v in variants:
            counts = {d: 0 for d in decision_ids}
            for t in run.get("trials", []):
                if not t.get("ok") or t.get("variantId") != v["id"]:
                    continue
                if t.get("decision") in counts:
                    counts[t["decision"]] += 1
            n = sum(counts.values())
            ms = mean_spend.get(v["id"], {}) or {}
            sp = step_profile.get(v["id"], {}) or {}
            row = {
                "experiment": experiment_id,
                "source": label,
                "condition": v["id"],
                "n": n,
            }
            for d in decision_ids:
                row[f"{d}_count"] = counts[d]
                row[f"{d}_share_pct"] = round(counts[d] / n * 100, 1) if n else ""
            row["mean_price_usd"] = ms.get("mean", "")
            row["mean_steps"] = sp.get("meanSteps", "")
            row["budget_rate_pct"] = (
                round(sp.get("budgetRate") * 100, 1) if sp.get("budgetRate") is not None else ""
            )
            cell_rows.append(row)

        o = analysis.get("overall", {})
        sig_rows.append(
            {
                "experiment": experiment_id,
                "source": label,
                "test": "condition x product (chi-square of independence)",
                "n": analysis.get("totalTrials"),
                "statistic": o.get("statistic"),
                "dof": o.get("dof"),
                "p_value": o.get("pValue"),
                "effect_size": o.get("cramersV"),
                "significant": o.get("significant"),
            }
        )
        tt = (analysis.get("meanSpend") or {}).get("noRestraintVsSalient", {}) or {}
        if tt.get("testable"):
            sig_rows.append(
                {
                    "experiment": experiment_id,
                    "source": label,
                    "test": "no_restraint vs salient_restraint mean spend (Welch t-test)",
                    "n": "",
                    "statistic": tt.get("t"),
                    "dof": "",
                    "p_value": tt.get("pValue"),
                    "effect_size": "",
                    "significant": tt.get("significant"),
                }
            )

    # human baseline rows: choice share per product + implied mean price from shares
    if baseline:
        for v in variants:
            b = (baseline.get("by_variant") or {}).get(v["id"])
            if not b:
                continue
            implied_mean = sum(
                float(b.get(d, 0)) * (price_of.get(d) or 0) for d in decision_ids
            )
            row = {
                "experiment": experiment_id,
                "source": f"Humans ({baseline.get('source', 'baseline')})",
                "condition": v["id"],
                "n": "",
            }
            for d in decision_ids:
                row[f"{d}_count"] = ""
                row[f"{d}_share_pct"] = round(float(b.get(d, 0)) * 100, 1)
            row["mean_price_usd"] = round(implied_mean, 4)
            row["mean_steps"] = ""
            row["budget_rate_pct"] = ""
            cell_rows.append(row)

    cell_fields = ["experiment", "source", "condition", "n"]
    for d in decision_ids:
        cell_fields += [f"{d}_count", f"{d}_share_pct"]
    cell_fields += ["mean_price_usd", "mean_steps", "budget_rate_pct"]
    with (pkg / "results" / "summary_by_condition.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cell_fields)
        w.writeheader()
        w.writerows(cell_rows)
    with (pkg / "results" / "significance.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(
            fh,
            fieldnames=["experiment", "source", "test", "n", "statistic", "dof",
                        "p_value", "effect_size", "significant"],
        )
        w.writeheader()
        w.writerows(sig_rows)


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("Usage: python -m server.export_experiment <experiment_id>", file=sys.stderr)
        return 1
    export(args[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

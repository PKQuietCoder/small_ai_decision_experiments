"""Export a self-contained, replication-ready data package for an experiment.

Bundles methodology (config, rendered prompts, coding rubric, human baseline),
raw per-trial data (model responses + judge codes, JSON + tidy CSV), and results
(analysis JSON + summary/significance CSVs) into ``experiments/<id>/``, plus a
single ``<id>-data-package.zip`` for one-click download.

Regenerates the data files on every run; a hand-written ``README.md`` in the
package is preserved (never overwritten).

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
    question = experiment.get("question", "")
    decision_ids = [o["id"] for o in experiment.get("decision_options", [])]

    # ---- methodology -------------------------------------------------------
    shutil.copyfile(
        content_store.config.EXPERIMENTS_DIR / f"{experiment_id}.yaml",
        pkg / "methodology" / f"{experiment_id}.yaml",
    )
    for v in variants:
        fields = {k: val for k, val in v.items() if isinstance(val, str)}
        rendered = experiment["prompt_template"].format(**fields)
        (pkg / "methodology" / f"prompt_{v['id']}.txt").write_text(rendered, encoding="utf-8")
    if experiment.get("type") == "open_response":
        rubric = engine._coder_prompt(question, "<<MODEL RESPONSE INSERTED HERE>>")
        (pkg / "methodology" / "coding_rubric.txt").write_text(rubric, encoding="utf-8")
    baseline = experiment.get("baseline")
    if baseline:
        (pkg / "methodology" / "human_baseline.json").write_text(
            json.dumps(baseline, indent=2), encoding="utf-8"
        )

    # ---- raw: per-model run copies + flattened trials.csv -------------------
    variant_meta = {v["id"]: v for v in variants}
    trials_rows: List[Dict[str, Any]] = []
    run_files: List[str] = []
    for label, run in by_model.items():
        name = f"{_slug(label)}__{run['runId']}.json"
        (pkg / "raw" / "runs" / name).write_text(json.dumps(run, indent=2), encoding="utf-8")
        run_files.append(name)
        for t in run.get("trials", []):
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
    with (pkg / "raw" / "trials.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(
            fh,
            fieldnames=["experiment", "model", "provider", "condition", "frame",
                        "spread", "trial", "code", "ok", "response"],
        )
        w.writeheader()
        w.writerows(trials_rows)

    # ---- results: analysis copies + summary + significance CSVs -------------
    cell_rows: List[Dict[str, Any]] = []
    sig_rows: List[Dict[str, Any]] = []
    for label, run in by_model.items():
        analysis = content_store.analysis_for(experiment, run)
        aname = f"{_slug(label)}__{run['runId']}.json"
        (pkg / "results" / "analysis" / aname).write_text(
            json.dumps(analysis, indent=2), encoding="utf-8"
        )
        # per-condition counts from the run's coded trials
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

    # human baseline rows (from the experiment config), if present
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

    # ---- manifest ----------------------------------------------------------
    manifest = {
        "experiment": experiment_id,
        "title": experiment.get("title", experiment_id),
        "type": experiment.get("type"),
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "models": list(by_model.keys()),
        "trialsPerCell": experiment.get("trials_per_cell"),
        "conditions": [v["id"] for v in variants],
        "judge": experiment.get("coder"),
        "runs": {label: run["runId"] for label, run in by_model.items()},
        "humanBaseline": baseline,
    }
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


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("Usage: python -m server.export_experiment <experiment_id>", file=sys.stderr)
        return 1
    export(args[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

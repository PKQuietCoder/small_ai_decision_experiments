"""Read/write access to file-based content: experiments, runs, posts, site meta.

This module is the single source of truth for loading content off disk and
shaping it into the JSON structures the API serves. There is no database; every
read hits the filesystem so that editing a Markdown or YAML file in Replit is
all an admin needs to do to publish or update content.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import frontmatter
import markdown as md
import yaml

from . import config
from ..experiments.stats import chi_square_contingency, wilson_interval

MARKDOWN_EXTENSIONS = ["extra", "sane_lists", "tables", "fenced_code", "toc"]


# --------------------------------------------------------------------------- #
# Low-level loaders
# --------------------------------------------------------------------------- #
def _read_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_experiment_config(experiment_id: str) -> Optional[Dict[str, Any]]:
    path = config.EXPERIMENTS_DIR / f"{experiment_id}.yaml"
    if not path.exists():
        return None
    return _read_yaml(path)


def list_experiment_configs() -> List[Dict[str, Any]]:
    if not config.EXPERIMENTS_DIR.exists():
        return []
    configs: List[Dict[str, Any]] = []
    for path in sorted(config.EXPERIMENTS_DIR.glob("*.yaml")):
        configs.append(_read_yaml(path))
    return configs


def load_run(experiment_id: str, run_id: str) -> Optional[Dict[str, Any]]:
    path = config.RUNS_DIR / experiment_id / f"{run_id}.json"
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def list_runs(experiment_id: str) -> List[Dict[str, Any]]:
    directory = config.RUNS_DIR / experiment_id
    if not directory.exists():
        return []
    runs: List[Dict[str, Any]] = []
    for path in sorted(directory.glob("*.json")):
        with path.open("r", encoding="utf-8") as handle:
            runs.append(json.load(handle))
    return runs


def latest_run(experiment_id: str) -> Optional[Dict[str, Any]]:
    runs = list_runs(experiment_id)
    if not runs:
        return None
    runs.sort(key=lambda run: run.get("finishedAt") or run.get("startedAt") or "")
    return runs[-1]


# --------------------------------------------------------------------------- #
# Analysis
# --------------------------------------------------------------------------- #
def build_analysis(
    experiment: Dict[str, Any], run: Dict[str, Any]
) -> Dict[str, Any]:
    """Aggregate a run's trials into the analysis structure the UI charts use."""
    decision_options = experiment.get("decision_options", [])
    decision_ids = [opt["id"] for opt in decision_options]
    decision_labels = {opt["id"]: opt.get("label", opt["id"]) for opt in decision_options}
    variants = experiment.get("variants", [])
    variant_meta = {v["id"]: v for v in variants}
    models = [m.get("label", m.get("model")) for m in experiment.get("models", [])]
    primary = experiment.get("primary_decision", decision_ids[0] if decision_ids else None)

    trials = [t for t in run.get("trials", []) if t.get("ok") and t.get("decision") in decision_ids]

    def empty_counts() -> Dict[str, int]:
        return {d: 0 for d in decision_ids}

    by_variant: List[Dict[str, Any]] = []
    contingency: List[List[int]] = []

    for variant in variants:
        vid = variant["id"]
        counts = empty_counts()
        for trial in trials:
            if trial.get("variantId") == vid:
                counts[trial["decision"]] += 1
        total = sum(counts.values())
        proportions = {
            d: round(counts[d] / total, 4) if total else 0.0 for d in decision_ids
        }
        ci = {d: wilson_interval(counts[d], total) for d in decision_ids}
        by_variant.append(
            {
                "variantId": vid,
                "label": variant.get("label", vid),
                "metaphor": variant.get("metaphor", ""),
                "total": total,
                "counts": counts,
                "proportions": proportions,
                "ci": ci,
            }
        )
        contingency.append([counts[d] for d in decision_ids])

    by_variant_model: List[Dict[str, Any]] = []
    per_model: List[Dict[str, Any]] = []
    for model_cfg in experiment.get("models", []):
        model_label = model_cfg.get("label", model_cfg.get("model"))
        model_contingency: List[List[int]] = []
        for variant in variants:
            vid = variant["id"]
            counts = empty_counts()
            for trial in trials:
                if trial.get("model") == model_label and trial.get("variantId") == vid:
                    counts[trial["decision"]] += 1
            total = sum(counts.values())
            proportions = {
                d: round(counts[d] / total, 4) if total else 0.0 for d in decision_ids
            }
            by_variant_model.append(
                {
                    "variantId": vid,
                    "label": variant.get("label", vid),
                    "model": model_label,
                    "total": total,
                    "counts": counts,
                    "proportions": proportions,
                }
            )
            model_contingency.append([counts[d] for d in decision_ids])
        per_model.append(
            {
                "model": model_label,
                "chiSquare": chi_square_contingency(model_contingency),
            }
        )

    overall = chi_square_contingency(contingency)
    parse_failures = sum(1 for t in run.get("trials", []) if not t.get("ok"))

    return {
        "experimentId": experiment["id"],
        "experimentTitle": experiment.get("title", experiment["id"]),
        "runId": run.get("runId"),
        "runDate": run.get("finishedAt") or run.get("startedAt"),
        "prompt": experiment.get("prompt_template", ""),
        "decisionOptions": [
            {"id": d, "label": decision_labels[d]} for d in decision_ids
        ],
        "models": models,
        "variants": [
            {
                "id": v["id"],
                "label": v.get("label", v["id"]),
                "metaphor": v.get("metaphor", ""),
            }
            for v in variants
        ],
        "primaryDecision": primary,
        "primaryDecisionLabel": decision_labels.get(primary, primary),
        "totalTrials": len(trials),
        "trialsPerCell": experiment.get("trials_per_cell"),
        "parseFailures": parse_failures,
        "byVariant": by_variant,
        "byVariantModel": by_variant_model,
        "overall": overall,
        "perModel": per_model,
    }


# --------------------------------------------------------------------------- #
# Posts
# --------------------------------------------------------------------------- #
def _reading_minutes(text: str) -> int:
    words = len(text.split())
    return max(1, round(words / 200))


def _post_summary(post: frontmatter.Post, slug: str) -> Dict[str, Any]:
    meta = post.metadata
    return {
        "slug": meta.get("slug", slug),
        "title": meta.get("title", slug),
        "excerpt": meta.get("excerpt", ""),
        "category": meta.get("category", "Experiment"),
        "tags": meta.get("tags", []) or [],
        "date": _date_str(meta.get("date")),
        "readingMinutes": _reading_minutes(post.content),
        "featured": bool(meta.get("featured", False)),
        "published": bool(meta.get("published", False)),
        "experimentId": meta.get("experimentId"),
    }


def _date_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, (datetime,)):
        return value.date().isoformat()
    return str(value)


def _load_post_file(path: Path) -> frontmatter.Post:
    with path.open("r", encoding="utf-8") as handle:
        return frontmatter.load(handle)


def list_posts(include_unpublished: bool = False) -> List[Dict[str, Any]]:
    if not config.POSTS_DIR.exists():
        return []
    summaries: List[Dict[str, Any]] = []
    for path in config.POSTS_DIR.glob("*.md"):
        post = _load_post_file(path)
        summary = _post_summary(post, path.stem)
        if summary["published"] or include_unpublished:
            summaries.append(summary)
    summaries.sort(key=lambda item: item.get("date") or "", reverse=True)
    return summaries


def get_post(slug: str, include_unpublished: bool = False) -> Optional[Dict[str, Any]]:
    path = config.POSTS_DIR / f"{slug}.md"
    if not path.exists():
        return None
    post = _load_post_file(path)
    summary = _post_summary(post, slug)
    if not summary["published"] and not include_unpublished:
        return None

    body_html = md.markdown(post.content, extensions=MARKDOWN_EXTENSIONS)

    analysis = None
    experiment_id = summary.get("experimentId")
    run_id = post.metadata.get("runId")
    if experiment_id:
        experiment = load_experiment_config(experiment_id)
        run = None
        if experiment:
            run = load_run(experiment_id, run_id) if run_id else latest_run(experiment_id)
        if experiment and run:
            analysis = build_analysis(experiment, run)

    return {**summary, "bodyHtml": body_html, "analysis": analysis}


# --------------------------------------------------------------------------- #
# Experiments (API shape)
# --------------------------------------------------------------------------- #
def _experiment_summary(experiment: Dict[str, Any]) -> Dict[str, Any]:
    run = latest_run(experiment["id"])
    post_slug = None
    for summary in list_posts(include_unpublished=True):
        if summary.get("experimentId") == experiment["id"] and summary["published"]:
            post_slug = summary["slug"]
            break
    return {
        "id": experiment["id"],
        "title": experiment.get("title", experiment["id"]),
        "summary": (experiment.get("summary") or "").strip(),
        "status": experiment.get("status", "draft"),
        "models": [m.get("label", m.get("model")) for m in experiment.get("models", [])],
        "variantCount": len(experiment.get("variants", [])),
        "trialsPerCell": experiment.get("trials_per_cell"),
        "lastRunAt": (run.get("finishedAt") or run.get("startedAt")) if run else None,
        "totalRuns": len(list_runs(experiment["id"])),
        "postSlug": post_slug,
    }


def list_experiments() -> List[Dict[str, Any]]:
    return [_experiment_summary(cfg) for cfg in list_experiment_configs()]


def get_experiment(experiment_id: str) -> Optional[Dict[str, Any]]:
    experiment = load_experiment_config(experiment_id)
    if not experiment:
        return None
    summary = _experiment_summary(experiment)
    run = latest_run(experiment_id)
    analysis = build_analysis(experiment, run) if run else None
    return {
        **summary,
        "hypothesis": (experiment.get("hypothesis") or "").strip(),
        "prompt": experiment.get("prompt_template", ""),
        "decisionOptions": [
            {"id": opt["id"], "label": opt.get("label", opt["id"])}
            for opt in experiment.get("decision_options", [])
        ],
        "variants": [
            {
                "id": v["id"],
                "label": v.get("label", v["id"]),
                "metaphor": v.get("metaphor", ""),
            }
            for v in experiment.get("variants", [])
        ],
        "analysis": analysis,
    }


# --------------------------------------------------------------------------- #
# Site metadata
# --------------------------------------------------------------------------- #
def get_site_meta() -> Dict[str, Any]:
    if not config.SITE_FILE.exists():
        return {
            "title": "LLM Decision Science",
            "tagline": "",
            "description": "",
            "author": "",
            "aboutHtml": "",
        }
    data = _read_yaml(config.SITE_FILE)
    about_html = md.markdown(data.get("about", "") or "", extensions=MARKDOWN_EXTENSIONS)
    return {
        "title": data.get("title", "LLM Decision Science"),
        "tagline": data.get("tagline", ""),
        "description": data.get("description", ""),
        "author": data.get("author", ""),
        "aboutHtml": about_html,
    }


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

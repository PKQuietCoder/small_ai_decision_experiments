"""Generate an editable Markdown draft post from an experiment run.

The generated post carries YAML frontmatter (including a ``published: false``
flag) and a human-readable write-up of the methodology and headline results.
An admin reviews/edits the Markdown file in Replit and flips ``published`` to
``true`` when ready. The interactive charts on the published page are rendered
by the frontend from the live analysis, so the prose deliberately stays light
on raw numbers and focuses on narrative.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import frontmatter

from ..app import config
from ..app.content_store import build_analysis


def _slugify(text: str) -> str:
    out = []
    for char in text.lower():
        if char.isalnum():
            out.append(char)
        elif char in " -_":
            out.append("-")
    slug = "".join(out)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")


def _fmt_pct(value: float) -> str:
    return f"{round(value * 100)}%"


def _headline_findings(analysis: Dict[str, Any]) -> List[str]:
    """Build a few plain-language bullet findings from the analysis."""
    findings: List[str] = []
    primary = analysis.get("primaryDecision")
    primary_label = analysis.get("primaryDecisionLabel", primary)
    by_variant = analysis.get("byVariant", [])

    if by_variant and primary:
        ranked = sorted(
            by_variant,
            key=lambda v: v["proportions"].get(primary, 0.0),
            reverse=True,
        )
        top = ranked[0]
        bottom = ranked[-1]
        findings.append(
            f'When the team was framed as "{top["metaphor"]}", the models chose '
            f'**{primary_label}** {_fmt_pct(top["proportions"].get(primary, 0))} '
            f'of the time — the highest of any framing.'
        )
        findings.append(
            f'The same option fell to '
            f'{_fmt_pct(bottom["proportions"].get(primary, 0))} when the team was '
            f'described as "{bottom["metaphor"]}".'
        )

    overall = analysis.get("overall", {})
    if overall.get("testable"):
        sig = "a statistically significant" if overall.get("significant") else "no significant"
        p_value = overall.get("pValue")
        p_str = f"{p_value:.4f}" if isinstance(p_value, (int, float)) else "n/a"
        findings.append(
            f"Across all framings there is {sig} association between the metaphor "
            f"and the chosen action (chi-square p = {p_str}, "
            f"Cramer's V = {overall.get('cramersV')})."
        )
    return findings


def generate_post(
    experiment: Dict[str, Any],
    run: Dict[str, Any],
    *,
    overwrite: bool = True,
) -> Path:
    """Create (or refresh) the Markdown draft for an experiment run."""
    config.ensure_dirs()
    analysis = build_analysis(experiment, run)

    title = experiment.get("title", experiment["id"])
    slug = _slugify(title.split(":")[0]) or experiment["id"]
    findings = _headline_findings(analysis)

    variants = experiment.get("variants", [])
    options = experiment.get("decision_options", [])

    variant_lines = "\n".join(
        f'- **{v.get("label", v["id"])}** — "{v["metaphor"]}"' for v in variants
    )
    option_lines = "\n".join(
        f'- **{o["id"]}** — {o.get("label", o["id"])}' for o in options
    )
    findings_block = "\n".join(f"- {line}" for line in findings) or (
        "- Results will appear here once a run completes."
    )

    body = f"""## The question

{(experiment.get("summary") or "").strip()}

**Hypothesis.** {(experiment.get("hypothesis") or "").strip()}

## How the experiment works

We give each model the exact same scenario and ask it to choose a single course
of action. The *only* thing that changes between conditions is one metaphor used
to describe the team:

{variant_lines}

For every framing the model picks one of four actions:

{option_lines}

We ran **{experiment.get("trials_per_cell")} trials per framing, per model**,
at temperature {run.get("temperature")}, across {", ".join(analysis.get("models", []))}.
The charts below are generated live from the recorded run.

### The exact prompt

```
{experiment.get("prompt_template", "").strip()}
```

## What we found

{findings_block}

## Reading the results

The charts show how often each action was chosen under each metaphor. If framing
were irrelevant, every bar would be roughly the same height. Where the bars
diverge, the metaphor — and nothing else — moved the model's decision.

## Caveats

This is a small, single-scenario probe, not a definitive measurement. Results
can shift with model versions, temperature, and prompt wording. Treat it as a
demonstration that framing effects are real and measurable in current models,
not as a fixed effect size.
"""

    post = frontmatter.Post(body)
    post.metadata = {
        "title": title,
        "slug": slug,
        "excerpt": (experiment.get("summary") or "").strip().split("\n")[0][:200],
        "category": "Experiments",
        "tags": ["framing", "metaphor", "decision-making", "prompting"],
        "date": datetime.now(timezone.utc).date().isoformat(),
        "published": False,
        "featured": True,
        "experimentId": experiment["id"],
        "runId": run["runId"],
        # Filled in by the admin before publishing: the headline verdict
        # (copy / smooth / amplify) and a one-line summary of the controls.
        "verdict": "",
        "controls": "",
    }

    path = config.POSTS_DIR / f"{slug}.md"
    if path.exists() and not overwrite:
        # Preserve an admin's published flag / edits: only refresh the runId.
        existing = frontmatter.load(path.open("r", encoding="utf-8"))
        existing.metadata["runId"] = run["runId"]
        path.write_text(frontmatter.dumps(existing), encoding="utf-8")
        return path

    path.write_text(frontmatter.dumps(post), encoding="utf-8")
    return path

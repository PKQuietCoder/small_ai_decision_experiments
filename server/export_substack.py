"""Export published posts as a Substack "paste pack".

Substack has no official write API, so this builds a clean, paste-ready HTML
version of each article that you drop straight into the Substack editor. The live
React/Recharts charts can't render in Substack, so each chart is rendered here as
a data table (from the analysis JSON) plus a marked spot where you paste a
screenshot of the live chart.

Writes ``substack/<slug>/<slug>.html`` and ``substack/<slug>/PASTE_GUIDE.md``.

Usage:
    python -m server.export_substack            # every published post
    python -m server.export_substack <slug>     # one post (drafts allowed)
"""

from __future__ import annotations

import html
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from server.app import content_store

REPO_ROOT = Path(__file__).resolve().parents[1]


def _pct(value: Any) -> str:
    """Format a 0..1 proportion as a percentage string."""
    try:
        return f"{round(float(value) * 100, 1)}%"
    except (TypeError, ValueError):
        return ""


def _table(headers: List[str], rows: List[List[str]]) -> str:
    head = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in r) + "</tr>"
        for r in rows
    )
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def _chart_section(analysis: Optional[Dict[str, Any]]) -> str:
    """Render the chart's data as HTML tables, plus a screenshot placeholder."""
    if not analysis:
        return ""
    parts: List[str] = [
        "<hr />",
        "<h2>Chart</h2>",
        "<p><em>[Chart image: paste a screenshot of the live chart here]</em></p>",
    ]

    decision_options = analysis.get("decisionOptions") or []
    by_variant = analysis.get("byVariant") or []
    if decision_options and by_variant:
        headers = ["Condition"] + [o.get("label", o.get("id")) for o in decision_options]
        rows: List[List[str]] = []
        for v in by_variant:
            props = v.get("proportions") or {}
            rows.append(
                [v.get("label", v.get("variantId", ""))]
                + [_pct(props.get(o["id"])) for o in decision_options]
            )
        parts.append("<p><strong>Choice share by condition</strong></p>")
        parts.append(_table(headers, rows))

    # Agentic budget extras, when present.
    mean_spend = (analysis.get("meanSpend") or {}).get("byVariant")
    if mean_spend:
        rows = [
            [vid, f"${m.get('mean')}" if m.get("mean") is not None else "", m.get("n", "")]
            for vid, m in mean_spend.items()
        ]
        parts.append("<p><strong>Mean spend by condition</strong></p>")
        parts.append(_table(["Condition", "Mean spend", "n"], rows))

    step_profile = analysis.get("stepProfile")
    if step_profile:
        rows = [
            [
                vid,
                s.get("meanSteps", ""),
                _pct(s.get("budgetRate")) if s.get("budgetRate") is not None else "",
            ]
            for vid, s in step_profile.items()
        ]
        parts.append("<p><strong>Steps taken by condition</strong></p>")
        parts.append(_table(["Condition", "Mean steps", "Budget rate"], rows))

    return "\n".join(parts)


def _post_html(post: Dict[str, Any]) -> str:
    title = html.escape(post.get("title", post.get("slug", "")))
    body = post.get("bodyHtml") or ""
    chart = _chart_section(post.get("analysis"))
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n<head>\n<meta charset="utf-8" />\n'
        f"<title>{title}</title>\n</head>\n<body>\n"
        f"<h1>{title}</h1>\n{body}\n{chart}\n"
        "</body>\n</html>\n"
    )


def _paste_guide(post: Dict[str, Any], base_url: str) -> str:
    slug = post.get("slug", "")
    title = post.get("title", "")
    excerpt = post.get("excerpt", "")
    has_chart = bool(post.get("analysis"))
    chart_step = (
        f"4. Screenshot the live chart at {base_url}/posts/{slug} and place it where the "
        '"[Chart image: ...]" line is, then delete that line. The numbers are also in the '
        '"Chart" table below it, which pastes in as a fallback.\n'
        if has_chart
        else ""
    )
    return (
        f"# Substack paste guide: {title}\n\n"
        "Substack has no write API, so this is a manual paste. It takes about a minute.\n\n"
        f"1. Open `{slug}.html` in a browser, select all (Cmd/Ctrl+A), and copy.\n"
        "2. In Substack, start a new post and paste. Headings, bold, links, lists, and tables\n"
        "   come across; the H1 at the top is the title, so you can delete it after setting the\n"
        "   title field.\n"
        f"3. Set the post Title to:\n   {title}\n"
        f"   Set the Subtitle to:\n   {excerpt}\n"
        f"{chart_step}"
        "5. Check the GitHub data link and the citation survived as links, then add your tags\n"
        "   and publish.\n"
    )


def export(slug: Optional[str], base_url: str = "https://your-site") -> List[Path]:
    if slug:
        post = content_store.get_post(slug, include_unpublished=True)
        if post is None:
            raise SystemExit(f"Post '{slug}' not found.")
        posts = [post]
    else:
        summaries = content_store.list_posts(include_unpublished=False)
        posts = [content_store.get_post(s["slug"]) for s in summaries]
        posts = [p for p in posts if p is not None]
        if not posts:
            raise SystemExit("No published posts found. Pass a slug to export a draft.")

    written: List[Path] = []
    for post in posts:
        s = post["slug"]
        out = REPO_ROOT / "substack" / s
        out.mkdir(parents=True, exist_ok=True)
        html_path = out / f"{s}.html"
        html_path.write_text(_post_html(post), encoding="utf-8")
        (out / "PASTE_GUIDE.md").write_text(_paste_guide(post, base_url), encoding="utf-8")
        written.append(html_path)
        print(f"  {s}: {html_path}")

    print(f"Exported {len(written)} post(s) to {REPO_ROOT / 'substack'}.")
    return written


def main(argv: Optional[list[str]] = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    export(args[0] if args else None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

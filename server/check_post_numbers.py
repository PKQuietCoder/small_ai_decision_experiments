"""Assert that every number quoted in a post's body is traceable to its analysis.

Posts here are written by hand, and the easiest way to publish a wrong number is
to type one from memory while the analysis JSON says something else. This check
walks the post body, pulls out every numeric literal, and verifies that each one
appears among the values that can be derived from the analysis file the post's
``runId`` points at (as printed at 1–4 decimal places, as a percentage, as a
rounded integer, or as a dollar/token/latency figure).

Usage:
    python -m server.check_post_numbers <slug> [--allow 2.1 3 ...]

Exit status is non-zero when any number is unaccounted for. Numbers that are
legitimately not data (section numbers, years, the state's own constants such as
"10 adults") are covered by a small built-in allowlist plus ``--allow``.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any, Iterable, Set

import frontmatter

from server.app import config, content_store

# Years, section numbers, the experiment's own constants, and formula constants
# that appear in the prose without being measurements.
DEFAULT_ALLOW: Set[str] = {
    # section numbering / list markers / figure numbers (1–20)
    *[str(i) for i in range(0, 21)],
    # years that may be cited
    *[str(y) for y in range(1970, 2031)],
    # Taleb's room and E6's group (state constants)
    "6", "4", "10", "1.2", "0.5", "50",
    # confidence-formula constants
    "1/4", "0.25", "0.75",
    # TypeSafe's published figures cited from their docs/site
    "0.042", "0.0098", "0.0515", "67.8", "0.0004", "0.4", "70", "500", "255",
    "1.13.0", "1.14.0", "1.13", "1.14", "64", "32", "42", "90.8", "99.2",
    # Model names that carry version digits (GPT-6 Astra, Claude Fable 5.1)
    "5.1",
}

NUMBER_RE = re.compile(r"(?<![\w.])[-−+]?\d+(?:[.,]\d+)*(?:\s?%)?(?![\w])")


def _derive(value: Any, out: Set[str]) -> None:
    """Add every printable rendering of ``value`` (recursively) to ``out``."""
    if isinstance(value, bool) or value is None:
        return
    if isinstance(value, (int, float)):
        f = float(value)
        for places in (0, 1, 2, 3, 4, 5, 6):
            s = f"{f:.{places}f}"
            out.add(s)
            out.add(s.lstrip("0") if s.startswith("0.") else s)
            out.add(s.rstrip("0").rstrip(".") if "." in s else s)
        pct = f * 100
        for places in (0, 1, 2):
            out.add(f"{pct:.{places}f}%")
            out.add(f"{pct:.{places}f}")
        # Thousands separators for token counts etc.
        if f == int(f) and abs(f) >= 1000:
            out.add(f"{int(f):,}")
        # Dollar figures.
        out.add(f"${f:.2f}")
        out.add(f"${f:.4f}")
        out.add(f"${f:.5f}")
        return
    if isinstance(value, dict):
        for v in value.values():
            _derive(v, out)
    elif isinstance(value, (list, tuple)):
        for v in value:
            _derive(v, out)


def _extract_numbers(text: str) -> Iterable[str]:
    # Drop headings (section numbering) and code: fences and inline code quote
    # request bodies, formulas and YAML constants, which are inputs, not results.
    text = re.sub(r"^#.*$", " ", text, flags=re.M)
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    # Drop URLs and Markdown link targets.
    text = re.sub(r"\(https?://[^)]+\)", " ", text)
    text = re.sub(r"https?://\S+", " ", text)
    # Strip HTML attributes (data-widget ids etc.).
    text = re.sub(r"<[^>]+>", " ", text)
    for m in NUMBER_RE.finditer(text):
        token = m.group(0).replace("−", "-").replace(" ", "")
        yield token


def check(slug: str, extra_allow: Set[str]) -> int:
    post_path = config.POSTS_DIR / f"{slug}.md"
    if not post_path.exists():
        print(f"No post at {post_path}", file=sys.stderr)
        return 2
    post = frontmatter.load(post_path)
    experiment_id = post.metadata.get("experimentId")
    run_id = post.metadata.get("runId")
    if not experiment_id or not run_id:
        print("Post frontmatter needs experimentId and runId.", file=sys.stderr)
        return 2
    analysis = content_store.load_analysis(experiment_id, run_id)
    if analysis is None:
        print(f"No analysis for {experiment_id}/{run_id}", file=sys.stderr)
        return 2

    derived: Set[str] = set()
    _derive(analysis, derived)
    # Convenience derivations the prose uses: per-call token average, spend in
    # cents, polarity residual as a percentage of 1, etc.
    meta = (analysis.get("systemone") or {}).get("meta") or {}
    if meta.get("okCalls"):
        _derive(meta["inputTokens"] / meta["okCalls"], derived)
        _derive(meta["estimatedUsd"] * 100, derived)  # cents
        _derive(meta["estimatedUsd"] / meta["okCalls"], derived)
    if meta.get("latencyMs", {}).get("total"):
        _derive(meta["latencyMs"]["total"] / 1000, derived)  # seconds

    allow = DEFAULT_ALLOW | extra_allow
    missing = []
    seen = []
    for token in _extract_numbers(post.content):
        bare = token.rstrip("%")
        candidates = {token, bare, bare.lstrip("+-"), bare.replace(",", "")}
        if candidates & allow:
            continue
        if candidates & derived or (token.endswith("%") and (bare + "%") in derived):
            seen.append(token)
            continue
        missing.append(token)

    print(f"{slug}: {len(seen)} numbers traced to {experiment_id}/{run_id}; "
          f"{len(missing)} unaccounted for.")
    if missing:
        for token in sorted(set(missing), key=lambda s: (len(s), s)):
            print(f"  not in analysis: {token}")
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("slug")
    parser.add_argument("--allow", nargs="*", default=[], help="extra literals to ignore")
    args = parser.parse_args(argv)
    return check(args.slug, set(args.allow))


if __name__ == "__main__":
    raise SystemExit(main())

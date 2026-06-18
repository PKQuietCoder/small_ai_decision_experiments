"""Filesystem paths and shared configuration for the blog backend.

All content (experiment configs, runs, posts, site metadata) is stored as plain
files under the repository-root ``content/`` directory. There is no database.
"""

from __future__ import annotations

from pathlib import Path

# server/app/config.py -> server/app -> server -> repo root
REPO_ROOT = Path(__file__).resolve().parents[2]

CONTENT_DIR = REPO_ROOT / "content"
EXPERIMENTS_DIR = CONTENT_DIR / "experiments"
RUNS_DIR = CONTENT_DIR / "runs"
ANALYSIS_DIR = CONTENT_DIR / "analysis"
POSTS_DIR = CONTENT_DIR / "posts"
SITE_FILE = CONTENT_DIR / "site.yaml"


def ensure_dirs() -> None:
    """Create the content directories if they do not yet exist."""
    for directory in (CONTENT_DIR, EXPERIMENTS_DIR, RUNS_DIR, ANALYSIS_DIR, POSTS_DIR):
        directory.mkdir(parents=True, exist_ok=True)

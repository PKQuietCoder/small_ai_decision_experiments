"""FastAPI application serving the LLM Decision Science blog content.

All endpoints are read-only and public. Content is loaded from files on disk;
there is no database and no authentication. Admins publish by editing Markdown
files directly in Replit and flipping the ``published`` frontmatter flag.
"""

from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from . import config, content_store

app = FastAPI(title="LLM Decision Science API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


def _preview_enabled(preview: bool) -> bool:
    """Allow draft (unpublished) content only outside production."""
    if not preview:
        return False
    return os.environ.get("NODE_ENV") != "production"


@app.get("/api/healthz")
def health_check() -> dict:
    return {"status": "ok"}


@app.get("/api/site")
def site_meta() -> dict:
    return content_store.get_site_meta()


@app.get("/api/posts")
def list_posts(preview: bool = Query(False)) -> list:
    return content_store.list_posts(include_unpublished=_preview_enabled(preview))


@app.get("/api/posts/{slug}")
def get_post(slug: str, preview: bool = Query(False)) -> dict:
    post = content_store.get_post(slug, include_unpublished=_preview_enabled(preview))
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.get("/api/experiments")
def list_experiments() -> list:
    return content_store.list_experiments()


@app.get("/api/experiments/{experiment_id}")
def get_experiment(experiment_id: str) -> dict:
    experiment = content_store.get_experiment(experiment_id)
    if experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return experiment


@app.on_event("startup")
def _startup() -> None:
    config.ensure_dirs()

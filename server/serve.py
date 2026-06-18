"""Entry point for running the FastAPI app under a Replit workflow/deployment.

Reads the port from the ``PORT`` environment variable (assigned by Replit) so we
do not depend on shell variable expansion. Also inserts the repository root onto
``sys.path`` so the ``server`` package imports correctly regardless of the
working directory the workflow launches from.
"""

from __future__ import annotations

import os
import sys

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

import uvicorn  # noqa: E402  (import after sys.path fix)


def main() -> None:
    port = int(os.environ.get("PORT", "8080"))
    uvicorn.run("server.app.main:app", host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()

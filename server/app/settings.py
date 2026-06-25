"""Typed, validated runtime configuration for the backend.

Environment access used to be scattered ``os.environ.get`` calls; this module
centralizes it behind a single ``pydantic-settings`` model so every variable has
a declared type, a default, and one documented place to look. Values are read
from the process environment and an optional ``.env`` file (see ``.env.example``).

The provider API keys are intentionally **optional**: the public site serves
content without them, and only the experiment CLIs need them. Each key is
validated at the point of use in ``server.experiments.llm_clients`` so a missing
key fails with a clear message exactly when a model call is attempted, not at
import time.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Process configuration, read from the environment / ``.env``."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Provider credentials — optional; required only when running experiments.
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None

    # Web server. PORT is assigned by Replit; BASE_PATH is the client mount point.
    port: int = 8080
    base_path: str = "/"

    # Set to "1" by Replit in a published deployment; unset in the dev workspace.
    # Used to keep draft content out of production (see app.main._preview_enabled).
    replit_deployment: str | None = None

    @property
    def is_deployment(self) -> bool:
        """True when running in a published Replit deployment."""
        return self.replit_deployment == "1"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide settings singleton (cached)."""
    return Settings()

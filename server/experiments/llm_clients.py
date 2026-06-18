"""Thin wrappers around the official OpenAI and Anthropic SDKs.

Keys are read from the environment (OPENAI_API_KEY / ANTHROPIC_API_KEY) via the
Replit Secrets Manager. This deliberately does NOT use the Replit AI proxy — it
talks to the providers directly through their official Python SDKs.
"""

from __future__ import annotations

import os
import threading
from typing import Optional

from anthropic import Anthropic
from openai import OpenAI

_openai_client: Optional[OpenAI] = None
_anthropic_client: Optional[Anthropic] = None
# Guards lazy singleton creation: the engine calls complete() from many threads,
# so first-time initialization must not race.
_client_lock = threading.Lock()


def _get_openai() -> OpenAI:
    global _openai_client
    if _openai_client is None:
        with _client_lock:
            if _openai_client is None:
                key = os.environ.get("OPENAI_API_KEY")
                if not key:
                    raise RuntimeError(
                        "OPENAI_API_KEY is not set. Add it in the Replit Secrets pane."
                    )
                _openai_client = OpenAI(api_key=key)
    return _openai_client


def _get_anthropic() -> Anthropic:
    global _anthropic_client
    if _anthropic_client is None:
        with _client_lock:
            if _anthropic_client is None:
                key = os.environ.get("ANTHROPIC_API_KEY")
                if not key:
                    raise RuntimeError(
                        "ANTHROPIC_API_KEY is not set. Add it in the Replit Secrets pane."
                    )
                _anthropic_client = Anthropic(api_key=key)
    return _anthropic_client


def complete(provider: str, model: str, prompt: str, temperature: float = 1.0) -> str:
    """Send a single-turn prompt and return the raw text response."""
    if provider == "openai":
        response = _get_openai().chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=16,
        )
        return (response.choices[0].message.content or "").strip()

    if provider == "anthropic":
        response = _get_anthropic().messages.create(
            model=model,
            max_tokens=16,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        parts = [block.text for block in response.content if block.type == "text"]
        return "".join(parts).strip()

    raise ValueError(f"Unknown provider: {provider}")

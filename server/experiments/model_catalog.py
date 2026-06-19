"""Catalog of selectable models for experiment runs.

A single source of truth for the models an operator can choose from at the
command line (see ``server.run_experiment``). Each entry carries the provider,
the exact API model id, a display label, and capability flags so the LLM client
can vary request parameters per model.

Why capability flags? Providers differ in which sampling/token parameters they
accept:

* Anthropic Opus 4.7/4.8 (and Fable/Mythos) reject ``temperature`` (HTTP 400);
  Sonnet 4.6 and Haiku 4.5 accept it.
* OpenAI GPT-5.x are reasoning models: they reject ``max_tokens`` (require
  ``max_completion_tokens``), need a generous output budget because reasoning
  tokens count against it, and take an optional ``reasoning_effort``.

The flags below were confirmed against the live provider APIs.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

# key -> catalog entry. ``provider``/``model``/``label`` match the shape the
# engine and analysis already expect; the remaining keys are capability flags
# consumed by ``llm_clients.decide``.
MODEL_CATALOG: Dict[str, Dict[str, Any]] = {
    "opus": {
        "provider": "anthropic",
        "model": "claude-opus-4-8",
        "label": "Claude Opus 4.8",
        "accepts_temperature": False,  # Opus 4.7/4.8 reject sampling params
        "token_param": "max_tokens",
        "max_output": 128,
    },
    "sonnet": {
        "provider": "anthropic",
        "model": "claude-sonnet-4-6",
        "label": "Claude Sonnet 4.6",
        "accepts_temperature": True,
        "token_param": "max_tokens",
        "max_output": 128,
    },
    "haiku": {
        "provider": "anthropic",
        "model": "claude-haiku-4-5",
        "label": "Claude Haiku 4.5",
        "accepts_temperature": True,
        "token_param": "max_tokens",
        "max_output": 128,
    },
    "gpt-5.5": {
        "provider": "openai",
        "model": "gpt-5.5",
        "label": "GPT-5.5",
        "accepts_temperature": False,  # reasoning model: use default sampling
        "token_param": "max_completion_tokens",
        "max_output": 2000,  # leave room: reasoning tokens count against this
        "reasoning_effort": "low",
    },
    "gpt-5.4": {
        "provider": "openai",
        "model": "gpt-5.4",
        "label": "GPT-5.4",
        "accepts_temperature": False,
        "token_param": "max_completion_tokens",
        "max_output": 2000,
        "reasoning_effort": "low",
    },
    "gpt-5.4-mini": {
        "provider": "openai",
        "model": "gpt-5.4-mini",
        "label": "GPT-5.4 mini",
        "accepts_temperature": False,
        "token_param": "max_completion_tokens",
        "max_output": 2000,
        "reasoning_effort": "low",
    },
}

# Display order for the interactive menu (Anthropic trio, then OpenAI trio).
ORDER: List[str] = ["opus", "sonnet", "haiku", "gpt-5.5", "gpt-5.4", "gpt-5.4-mini"]


def resolve(key: str) -> Optional[Dict[str, Any]]:
    """Return a copy of the catalog entry for ``key``, or ``None`` if unknown."""
    entry = MODEL_CATALOG.get(key)
    return dict(entry) if entry is not None else None


def menu_lines() -> List[str]:
    """Return ``"  N) Label"`` lines for the interactive selection menu."""
    return [
        f"  {i}) {MODEL_CATALOG[key]['label']}"
        for i, key in enumerate(ORDER, start=1)
    ]

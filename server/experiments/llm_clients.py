"""Thin wrappers around the official OpenAI and Anthropic SDKs.

Keys are read from the environment (OPENAI_API_KEY / ANTHROPIC_API_KEY) via the
Replit Secrets Manager. This deliberately does NOT use the Replit AI proxy — it
talks to the providers directly through their official Python SDKs.
"""

from __future__ import annotations

import json
import os
import threading
from typing import Any, Dict, List, Optional, Tuple

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


def decide(
    model_cfg: Dict[str, Any],
    prompt: str,
    valid_ids: List[str],
    temperature: float = 1.0,
) -> Tuple[str, str]:
    """Ask the model to choose one option using provider-enforced structured output.

    ``model_cfg`` is a resolved catalog entry (see
    ``server.experiments.model_catalog``) carrying ``provider``, the API
    ``model`` id, and capability flags (``accepts_temperature``, ``token_param``,
    ``max_output``, optional ``reasoning_effort``). Those flags exist because
    providers disagree on which parameters they accept — e.g. Opus 4.8 rejects
    ``temperature`` and GPT-5.x reasoning models reject ``max_tokens``.

    Returns ``(decision, raw)`` where ``decision`` is guaranteed to be one of
    ``valid_ids`` (the provider constrains the output to that enum), and ``raw``
    is the machine-readable payload the provider returned. We never fall back to
    regex/heuristic parsing of free-form prose — the decision is read from a
    constrained field only.
    """
    provider = model_cfg["provider"]
    model = model_cfg["model"]
    accepts_temperature = model_cfg.get("accepts_temperature", True)
    token_param = model_cfg.get("token_param", "max_tokens")
    max_output = model_cfg.get("max_output", 128)

    if provider == "openai":
        # OpenAI Structured Outputs: the response is forced to match a JSON
        # Schema whose `decision` field is constrained to the allowed enum.
        kwargs: Dict[str, Any] = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            token_param: max_output,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "decision",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "decision": {"type": "string", "enum": valid_ids}
                        },
                        "required": ["decision"],
                    },
                },
            },
        }
        if accepts_temperature:
            kwargs["temperature"] = temperature
        if model_cfg.get("reasoning_effort"):
            kwargs["reasoning_effort"] = model_cfg["reasoning_effort"]

        response = _get_openai().chat.completions.create(**kwargs)
        raw = response.choices[0].message.content or ""
        if not raw:
            raise ValueError(
                f"OpenAI returned empty content (finish_reason="
                f"{response.choices[0].finish_reason!r})"
            )
        decision = json.loads(raw)["decision"]
        if decision not in valid_ids:
            raise ValueError(f"OpenAI returned out-of-enum decision: {decision!r}")
        return decision, raw

    if provider == "anthropic":
        # Anthropic forced tool use: tool_choice pins the model to a single tool
        # whose input_schema constrains `decision` to the allowed enum.
        tool = {
            "name": "submit_decision",
            "description": "Record the single chosen course of action.",
            "input_schema": {
                "type": "object",
                "properties": {"decision": {"type": "string", "enum": valid_ids}},
                "required": ["decision"],
            },
        }
        kwargs = {
            "model": model,
            "max_tokens": max_output,
            "tools": [tool],
            "tool_choice": {"type": "tool", "name": "submit_decision"},
            "messages": [{"role": "user", "content": prompt}],
        }
        if accepts_temperature:
            kwargs["temperature"] = temperature

        response = _get_anthropic().messages.create(**kwargs)
        for block in response.content:
            if block.type == "tool_use" and block.name == "submit_decision":
                decision = block.input.get("decision")
                if decision not in valid_ids:
                    raise ValueError(
                        f"Anthropic returned out-of-enum decision: {decision!r}"
                    )
                return decision, json.dumps(block.input)
        raise ValueError("Anthropic response contained no submit_decision tool call")

    raise ValueError(f"Unknown provider: {provider}")


def respond(
    model_cfg: Dict[str, Any],
    prompt: str,
    *,
    max_output: int = 1024,
    temperature: float = 1.0,
) -> str:
    """Get a free-text completion from a model (no enum / structured constraint).

    Used for open-ended experiments where the model answers in prose and a
    separate judge later codes the answer. Honors the same per-model capability
    flags as ``decide`` (``accepts_temperature``, ``token_param``,
    ``reasoning_effort``). ``max_output`` should be generous: for reasoning
    models the reasoning tokens count against it, so the visible answer needs
    headroom.
    """
    provider = model_cfg["provider"]
    model = model_cfg["model"]
    accepts_temperature = model_cfg.get("accepts_temperature", True)
    token_param = model_cfg.get("token_param", "max_tokens")

    if provider == "openai":
        kwargs: Dict[str, Any] = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            token_param: max_output,
        }
        if accepts_temperature:
            kwargs["temperature"] = temperature
        if model_cfg.get("reasoning_effort"):
            kwargs["reasoning_effort"] = model_cfg["reasoning_effort"]
        response = _get_openai().chat.completions.create(**kwargs)
        text = response.choices[0].message.content or ""
        if not text.strip():
            raise ValueError(
                f"OpenAI returned empty text (finish_reason="
                f"{response.choices[0].finish_reason!r})"
            )
        return text

    if provider == "anthropic":
        kwargs = {
            "model": model,
            "max_tokens": max_output,
            "messages": [{"role": "user", "content": prompt}],
        }
        if accepts_temperature:
            kwargs["temperature"] = temperature
        response = _get_anthropic().messages.create(**kwargs)
        text = "".join(
            block.text for block in response.content if block.type == "text"
        )
        if not text.strip():
            raise ValueError("Anthropic returned empty text")
        return text

    raise ValueError(f"Unknown provider: {provider}")

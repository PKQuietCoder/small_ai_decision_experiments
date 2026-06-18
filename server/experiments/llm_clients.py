"""Thin wrappers around the official OpenAI and Anthropic SDKs.

Keys are read from the environment (OPENAI_API_KEY / ANTHROPIC_API_KEY) via the
Replit Secrets Manager. This deliberately does NOT use the Replit AI proxy — it
talks to the providers directly through their official Python SDKs.
"""

from __future__ import annotations

import json
import os
import threading
from typing import List, Optional, Tuple

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
    provider: str,
    model: str,
    prompt: str,
    valid_ids: List[str],
    temperature: float = 1.0,
) -> Tuple[str, str]:
    """Ask the model to choose one option using provider-enforced structured output.

    Returns ``(decision, raw)`` where ``decision`` is guaranteed to be one of
    ``valid_ids`` (the provider constrains the output to that enum), and ``raw``
    is the machine-readable payload the provider returned. We never fall back to
    regex/heuristic parsing of free-form prose — the decision is read from a
    constrained field only.
    """
    if provider == "openai":
        # OpenAI Structured Outputs: the response is forced to match a JSON
        # Schema whose `decision` field is constrained to the allowed enum.
        response = _get_openai().chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=64,
            response_format={
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
        )
        raw = response.choices[0].message.content or ""
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
        response = _get_anthropic().messages.create(
            model=model,
            max_tokens=128,
            temperature=temperature,
            tools=[tool],
            tool_choice={"type": "tool", "name": "submit_decision"},
            messages=[{"role": "user", "content": prompt}],
        )
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

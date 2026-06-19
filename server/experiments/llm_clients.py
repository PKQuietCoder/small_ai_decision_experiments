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


def run_tool_sequence(
    model_cfg: Dict[str, Any],
    scenario: str,
    tool_defs: List[Dict[str, Any]],
    valid_ids: List[str],
    *,
    steps: Optional[List[Dict[str, Any]]] = None,
    terminal_tool: str = "choose_product",
    decision_key: str = "product_id",
    temperature: float = 1.0,
    max_steps: int = 8,
) -> Tuple[str, Dict[str, Any]]:
    """Run a controlled multi-step tool-use conversation; return (decision, transcript).

    This drives a faithful agentic decision the way the experiment engine needs it:
    a sequence of tool calls over a single shared scenario, where the model's final
    pick is read from a constrained enum (never regex-parsed). Anthropic only in v1 —
    OpenAI's multi-turn tool API differs and is a planned follow-up.

    Two modes, selected by ``steps``:

    * **Forced sequence** (``steps`` is an ordered list of tool defs): each turn pins
      exactly one tool via ``tool_choice={"type": "tool", ...}``. The step structure is
      the manipulation — the model chooses *what* (the budget, the pick), never *which*
      action comes next. Used by the one/two/five-step conditions.
    * **Autonomous** (``steps`` is None): every turn forces *some* tool via
      ``tool_choice={"type": "any"}`` but lets the model pick which, looping until it
      calls ``terminal_tool`` (or ``max_steps`` is hit, after which one final
      ``terminal_tool`` turn is forced and ``transcript["capped"]`` is set). Records the
      model's natural step trajectory — what it does *by default*.

    ``tool_defs`` is the full toolset (passed on every call; ``tool_choice`` selects which
    is forced). Each entry must carry ``name``/``description``/``input_schema``; the
    terminal tool's ``input_schema`` must constrain ``decision_key`` to ``valid_ids``.

    Returns ``(decision, transcript)`` where ``transcript`` maps each called tool's name
    to its input dict, plus ``transcript["steps"]`` (ordered tool names actually called)
    and ``transcript["capped"]`` (autonomous only).
    """
    provider = model_cfg["provider"]
    if provider != "anthropic":
        raise ValueError(
            f"run_tool_sequence supports only anthropic in v1, got {provider!r}"
        )

    model = model_cfg["model"]
    accepts_temperature = model_cfg.get("accepts_temperature", True)
    # Each forced step emits one small tool_use block; give generous headroom so the
    # final tool call is never truncated (catalog defaults can be as low as 128).
    max_output = max(int(model_cfg.get("max_output", 128)), 512)

    tools = []
    for t in tool_defs:
        tool: Dict[str, Any] = {
            "name": t["name"],
            "description": t["description"],
            "input_schema": t["input_schema"],
        }
        # Strict tool use guarantees the model's tool input satisfies the schema
        # (required fields present, value in-enum) — without it the model can emit a
        # malformed call (e.g. an empty product_id), which we'd reject as a failure.
        if t.get("strict"):
            tool["strict"] = True
        tools.append(tool)

    client = _get_anthropic()
    messages: List[Dict[str, Any]] = [{"role": "user", "content": scenario}]
    transcript: Dict[str, Any] = {}
    taken: List[str] = []

    def base_kwargs() -> Dict[str, Any]:
        kwargs: Dict[str, Any] = {
            "model": model,
            "max_tokens": max_output,
            "tools": tools,
            "messages": messages,
        }
        if accepts_temperature:
            kwargs["temperature"] = temperature
        return kwargs

    def call_step(tool_choice: Dict[str, Any]) -> Any:
        """One turn: force a tool, append the assistant turn + a synthetic tool_result.

        Returns the chosen tool_use block. The ack string is deterministic and minimal
        so the only thing that varies between conditions is the number of partitions,
        not the information delivered (an inspect/compare step that echoed the price list
        would feed a multi-step agent context the one-step agent never re-reads).

        ``disable_parallel_tool_use`` keeps each turn to a single tool call — without it
        the model may emit several tool_use blocks at once (and we'd owe a tool_result
        for each), and the step count would no longer be one-tool-per-turn.
        """
        tool_choice = {**tool_choice, "disable_parallel_tool_use": True}
        response = client.messages.create(tool_choice=tool_choice, **base_kwargs())
        block = next(
            (
                b
                for b in response.content
                if b.type == "tool_use"
                and (tool_choice.get("type") != "tool" or b.name == tool_choice["name"])
            ),
            None,
        )
        if block is None:
            raise ValueError(
                f"Anthropic returned no tool_use block for tool_choice={tool_choice}"
            )
        tool_input = dict(block.input)
        transcript[block.name] = tool_input
        taken.append(block.name)
        messages.append({"role": "assistant", "content": response.content})
        if "budget" in tool_input:
            ack = f"Noted. Planned spend recorded: ${tool_input['budget']}."
        else:
            ack = "Done."
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": ack,
                    }
                ],
            }
        )
        return block

    def finalize(block: Any) -> Tuple[str, Dict[str, Any]]:
        decision = block.input.get(decision_key)
        if decision not in valid_ids:
            raise ValueError(
                f"{terminal_tool} returned out-of-enum {decision_key}: {decision!r}"
            )
        transcript["steps"] = taken
        return decision, transcript

    if steps is not None:
        # Forced sequence: pin each tool in order.
        for step in steps:
            block = call_step({"type": "tool", "name": step["name"]})
            if step["name"] == terminal_tool:
                return finalize(block)
        raise ValueError("forced sequence ended without calling the terminal tool")

    # Autonomous: the model picks a tool each turn (forced to use *some* tool) until it
    # decides to finalize. max_steps is a safety cap, not the manipulation.
    transcript["capped"] = False
    for _ in range(max_steps):
        block = call_step({"type": "any"})
        if block.name == terminal_tool:
            return finalize(block)
    # Cap reached without finalizing: force one terminal turn so we still record a pick.
    transcript["capped"] = True
    block = call_step({"type": "tool", "name": terminal_tool})
    return finalize(block)


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

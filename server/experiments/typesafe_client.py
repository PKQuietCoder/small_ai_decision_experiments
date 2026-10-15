"""Thin HTTP client for TypeSafe AI's System One endpoint (the Jev models).

Jev is not a chat model, so it does not fit ``llm_clients``: it takes a JSON
``state`` plus typed questions (``noul`` / ``choice`` / ``score``) and returns
probability distributions, never text. TypeSafe publishes official SDKs, but the
request is a single JSON POST, so this module talks to the API directly with
``httpx`` (already a dependency of the OpenAI/Anthropic SDKs) and keeps the
repo's dependency list short.

Keys are read from validated settings (``TYPESAFE_API_KEY``; see
``server.app.settings``). The client never logs or echoes the key.

Two run-safety features live here because the engine treats every call as an
independent trial:

* **Retries** with exponential backoff on 429 (honouring ``Retry-After``), 529,
  and transport errors. Other 4xx responses are not retried — they are config
  bugs, not transient failures.
* **A hard spend cap.** Cost is estimated from ``usage.input_tokens`` at the
  catalog's per-token rate (output tokens are free) and accumulated across the
  process. Once the cap (``TYPESAFE_BUDGET_USD``, default $0.50) is reached,
  ``probe`` raises ``BudgetExceeded``. The engine records that as an ``ok: False``
  trial with the error text rather than aborting the process, so the run still
  saves; a capped run is visible as a block of failed trials, not a crash.
"""

from __future__ import annotations

import random
import threading
import time
from typing import Any, Dict, Optional

import httpx

from server.app.settings import get_settings

SYSTEMONE_URL = "https://api.typesafe.ai/v1/systemone"
DEFAULT_INPUT_USD_PER_MTOK = 0.042

_RETRY_STATUSES = {429, 529}
_MAX_ATTEMPTS = 6
_BASE_DELAY_S = 1.0
_MAX_DELAY_S = 30.0
_TIMEOUT_S = 60.0

_client: Optional[httpx.Client] = None
# Guards lazy singleton creation and the running cost total: the engine calls
# probe() from many threads.
_lock = threading.Lock()
_spent_usd = 0.0
_calls = 0


class BudgetExceeded(RuntimeError):
    """Raised when the cumulative estimated spend would exceed the hard cap."""


def _get_client() -> httpx.Client:
    global _client
    if _client is None:
        with _lock:
            if _client is None:
                key = get_settings().typesafe_api_key
                if not key:
                    raise RuntimeError(
                        "TYPESAFE_API_KEY is not set. Add it to your environment, a "
                        "local .env file, or the Replit Secrets pane."
                    )
                _client = httpx.Client(
                    headers={
                        "Authorization": f"Bearer {key}",
                        "Content-Type": "application/json",
                    },
                    timeout=_TIMEOUT_S,
                )
    return _client


def estimate_cost_usd(input_tokens: int, model_cfg: Dict[str, Any]) -> float:
    """Estimated charge for one response: input tokens only (output is free)."""
    rate = float(model_cfg.get("input_usd_per_mtok", DEFAULT_INPUT_USD_PER_MTOK))
    return input_tokens * rate / 1_000_000


def spend_summary() -> Dict[str, Any]:
    """Process-wide tally of calls made and estimated USD spent so far."""
    with _lock:
        return {"calls": _calls, "estimatedUsd": round(_spent_usd, 6)}


def _record_spend(cost: float) -> None:
    global _spent_usd, _calls
    with _lock:
        _spent_usd += cost
        _calls += 1


def _check_budget() -> None:
    cap = float(get_settings().typesafe_budget_usd)
    with _lock:
        if _spent_usd >= cap:
            raise BudgetExceeded(
                f"TypeSafe spend cap reached: ${_spent_usd:.4f} >= ${cap:.2f} "
                f"(TYPESAFE_BUDGET_USD). Aborting further calls."
            )


def _retry_delay(attempt: int, response: Optional[httpx.Response]) -> float:
    if response is not None:
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                return min(float(retry_after), _MAX_DELAY_S)
            except ValueError:
                pass
    delay = min(_BASE_DELAY_S * (2 ** attempt), _MAX_DELAY_S)
    return delay * (0.5 + random.random() / 2)  # jitter


def probe(model_cfg: Dict[str, Any], body: Dict[str, Any]) -> Dict[str, Any]:
    """POST one System One request and return the parsed result.

    ``body`` is the full request (``state``, ``model``, ``questions``). Returns
    ``{"response", "answers", "usage", "responseModel", "latencyMs",
    "estimatedUsd"}`` where ``response`` is the raw JSON body as returned.
    Raises ``RuntimeError`` for a missing key, ``BudgetExceeded`` at the cap,
    ``httpx.HTTPStatusError`` for a non-retryable failure, and ``ValueError`` for
    a malformed response.
    """
    _check_budget()
    client = _get_client()

    last_exc: Optional[Exception] = None
    for attempt in range(_MAX_ATTEMPTS):
        started = time.perf_counter()
        try:
            response = client.post(SYSTEMONE_URL, json=body)
        except httpx.TransportError as exc:
            last_exc = exc
            time.sleep(_retry_delay(attempt, None))
            continue
        latency_ms = round((time.perf_counter() - started) * 1000, 1)

        if response.status_code in _RETRY_STATUSES:
            last_exc = httpx.HTTPStatusError(
                f"HTTP {response.status_code} from TypeSafe",
                request=response.request,
                response=response,
            )
            time.sleep(_retry_delay(attempt, response))
            continue
        response.raise_for_status()

        data = response.json()
        answers = data.get("answers")
        if not isinstance(answers, dict) or not answers:
            raise ValueError(f"TypeSafe response carried no answers: {data!r}")
        usage = data.get("usage") or {}
        input_tokens = int(usage.get("input_tokens") or 0)
        cost = estimate_cost_usd(input_tokens, model_cfg)
        _record_spend(cost)
        return {
            "response": data,
            "answers": answers,
            "usage": usage,
            "responseModel": data.get("model"),
            "latencyMs": latency_ms,
            "estimatedUsd": cost,
        }

    raise RuntimeError(
        f"TypeSafe request failed after {_MAX_ATTEMPTS} attempts: {last_exc}"
    )

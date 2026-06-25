"""Pydantic schemas that validate an experiment's YAML config on load.

An experiment is defined entirely by one YAML file (see
``content/experiments/<id>.yaml``); everything downstream — the engine, the
analysis, the post, the export package — trusts that file's shape. Before this
module, a typo (a missing ``primary_decision``, a variant without an ``id``, an
unknown ``type``) surfaced only as a confusing ``KeyError`` deep inside a run
that had already spent real API calls.

These models document the contract and let ``content_store.load_experiment_config``
fail fast with a readable message. They are deliberately **permissive**:
``extra="allow"`` keeps every experiment-specific field (a variant's ``frame``,
``scenario``, ``steps``, ``catalog``; an experiment's ``products``) so validation
never rejects a valid config it simply did not enumerate. The engine and content
store keep reading plain dicts — validation runs alongside that flow, it does not
replace it.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

ExperimentType = Literal["fill_in_blank_decision", "open_response", "agentic_budget"]


class ModelSpec(BaseModel):
    """One subject model: provider + exact API id + display label."""

    model_config = ConfigDict(extra="allow")

    provider: Literal["anthropic", "openai"]
    model: str
    label: str


class DecisionOption(BaseModel):
    """A coded decision category the model's choice is mapped to."""

    model_config = ConfigDict(extra="allow")

    id: str
    label: str


class Variant(BaseModel):
    """One experimental cell.

    Beyond ``id``/``label``, variants carry arbitrary experiment-specific fields
    (e.g. ``frame``/``spread`` for framing studies, ``scenario`` for menu
    studies, ``steps``/``mode``/``catalog``/``tools`` for agentic studies), so
    extra keys are allowed and preserved.
    """

    model_config = ConfigDict(extra="allow")

    id: str
    label: str | None = None


class Coder(BaseModel):
    """The judge model that codes free-text answers (``open_response`` only)."""

    model_config = ConfigDict(extra="allow")

    key: str
    label: str | None = None
    temperature: float | None = None
    rubric: str | None = None


class ExperimentConfig(BaseModel):
    """The full experiment definition.

    Only the genuinely required, cross-type fields are mandatory; everything
    type-specific (``question``/``coder`` for open response; ``tools``/
    ``products``/``decision_key``/``max_steps`` for agentic) is optional and any
    unlisted key is kept via ``extra="allow"``.
    """

    model_config = ConfigDict(extra="allow")

    id: str
    title: str
    type: ExperimentType
    status: Literal["draft", "published"] = "draft"

    summary: str | None = None
    hypothesis: str | None = None
    question: str | None = None

    models: list[ModelSpec] = Field(default_factory=list)
    trials_per_cell: int = 20
    temperature: float = 1.0

    decision_options: list[DecisionOption] = Field(default_factory=list)
    primary_decision: str | None = None
    prompt_template: str = ""
    variants: list[Variant] = Field(default_factory=list)
    baseline: dict[str, Any] | None = None

    # open_response
    coder: Coder | None = None
    max_response_tokens: int | None = None

    # agentic_budget
    decision_key: str | None = None
    max_steps: int | None = None
    tools: list[dict[str, Any]] | None = None
    products: list[dict[str, Any]] | None = None


def validate_experiment_config(data: dict[str, Any], *, experiment_id: str | None = None) -> ExperimentConfig:
    """Validate a parsed experiment YAML, raising a clear error on a bad config.

    Returns the validated model. Callers that need the legacy dict shape can keep
    using the original dict; this is a fail-fast gate, not a replacement for it.
    """
    try:
        return ExperimentConfig.model_validate(data)
    except Exception as exc:  # pydantic.ValidationError, surfaced with context
        where = f" for experiment '{experiment_id}'" if experiment_id else ""
        raise ValueError(f"Invalid experiment config{where}: {exc}") from exc

"""LLM interaction layer.

Provides a mockable ``call_llm`` placeholder plus prompt building and
strict JSON validation of the scoring contract.
"""

from __future__ import annotations

import json
from collections.abc import Callable

from todo_pri.prompt import (
    build_prompt,
    get_json_schema_prompt_footer,
    read_prompt_header,
)

FALLBACK_SCORES: dict[str, int] = {"value": 3, "urgency": 3, "ease": 3}
_REQUIRED_KEYS = ("value", "urgency", "ease")


def call_llm(prompt: str) -> str:
    """Placeholder LLM call. Returns a deterministic JSON string.

    Kept intentionally simple so tests can monkey-patch it.
    """
    del prompt  # unused in the placeholder
    return json.dumps(FALLBACK_SCORES)


def _is_valid_int_in_range(candidate: object) -> bool:
    return (
        isinstance(candidate, int)
        and not isinstance(candidate, bool)
        and 0 <= candidate <= 5
    )


def get_prompt_for_task(task: str) -> str:
    """Return the full prompt for a given task."""
    return build_prompt(
        task,
        read_prompt_header(),
        get_json_schema_prompt_footer(),
    )


def validate_scores(raw: str) -> dict[str, int]:
    """Parse and validate an LLM JSON response, falling back on errors."""
    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return dict(FALLBACK_SCORES)
    if not isinstance(payload, dict):
        return dict(FALLBACK_SCORES)
    if not all(key in payload for key in _REQUIRED_KEYS):
        return dict(FALLBACK_SCORES)
    if not all(_is_valid_int_in_range(payload[key]) for key in _REQUIRED_KEYS):
        return dict(FALLBACK_SCORES)
    return {key: int(payload[key]) for key in _REQUIRED_KEYS}


def score_task(
    task: str,
    call_llm_fn: Callable[[str], str] | None = None,
) -> dict[str, int]:
    """Build a prompt, call the LLM, and return validated scores."""
    if call_llm_fn is None:
        call_llm_fn = call_llm
    return validate_scores(call_llm_fn(get_prompt_for_task(task)))

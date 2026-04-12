"""LLM interaction layer.

Provides a mockable ``call_llm`` placeholder plus prompt building and
strict JSON validation of the scoring contract.
"""

from __future__ import annotations

import json

FALLBACK_SCORES: dict[str, int] = {"value": 3, "urgency": 3, "ease": 3}
_REQUIRED_KEYS = ("value", "urgency", "ease")

_PROMPT_HEADER = (
    "You are prioritizing a todo list task.\n"
    "Rate the task on three dimensions (integers 0-5):\n"
    "- value: business/personal value delivered\n"
    "- urgency: how time-sensitive it is\n"
    "- ease: how easy it is to complete (5 = trivial)\n"
    'Respond with STRICT JSON only: {"value": int, "urgency": int, "ease": int}.\n'
    "Task: "
)


def build_prompt(task: str) -> str:
    """Return the LLM prompt for a single task."""
    return _PROMPT_HEADER + task


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


def score_task(task: str) -> dict[str, int]:
    """Build a prompt, call the LLM, and return validated scores."""
    return validate_scores(call_llm(build_prompt(task)))

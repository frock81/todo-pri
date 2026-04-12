"""Tests for the LLM interaction module."""

from __future__ import annotations

import json

import pytest

from todo_cli import llm


def test_build_prompt_contains_task_text() -> None:
    prompt = llm.build_prompt("Refactor auth module")
    assert "Refactor auth module" in prompt


def test_build_prompt_mentions_json_contract() -> None:
    prompt = llm.build_prompt("task")
    assert "value" in prompt
    assert "urgency" in prompt
    assert "ease" in prompt
    assert "JSON" in prompt or "json" in prompt


def test_call_llm_returns_valid_json_string() -> None:
    raw = llm.call_llm(llm.build_prompt("anything"))
    payload = json.loads(raw)
    for key in ("value", "urgency", "ease"):
        assert key in payload
        assert isinstance(payload[key], int)
        assert 0 <= payload[key] <= 5


def test_validate_scores_accepts_valid_payload() -> None:
    raw = '{"value":4,"urgency":3,"ease":2}'
    assert llm.validate_scores(raw) == {"value": 4, "urgency": 3, "ease": 2}


def test_validate_scores_rejects_malformed_json() -> None:
    assert llm.validate_scores("{bad json") == {
        "value": 3,
        "urgency": 3,
        "ease": 3,
    }


def test_validate_scores_rejects_missing_key() -> None:
    raw = '{"value":4,"urgency":3}'
    assert llm.validate_scores(raw) == {"value": 3, "urgency": 3, "ease": 3}


def test_validate_scores_rejects_non_int() -> None:
    raw = '{"value":"4","urgency":3,"ease":2}'
    assert llm.validate_scores(raw) == {"value": 3, "urgency": 3, "ease": 3}


@pytest.mark.parametrize(
    "raw",
    [
        '{"value":9,"urgency":3,"ease":2}',
        '{"value":-1,"urgency":3,"ease":2}',
        '{"value":3,"urgency":6,"ease":2}',
        '{"value":3,"urgency":3,"ease":-2}',
    ],
)
def test_validate_scores_rejects_out_of_range(raw: str) -> None:
    assert llm.validate_scores(raw) == {"value": 3, "urgency": 3, "ease": 3}


def test_validate_scores_rejects_bool_disguised_as_int() -> None:
    raw = '{"value":true,"urgency":3,"ease":2}'
    assert llm.validate_scores(raw) == {"value": 3, "urgency": 3, "ease": 3}


def test_score_task_uses_call_llm(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = '{"value":5,"urgency":4,"ease":1}'
    monkeypatch.setattr(llm, "call_llm", lambda _prompt: payload)
    assert llm.score_task("task") == {"value": 5, "urgency": 4, "ease": 1}


def test_score_task_falls_back_on_invalid_llm_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(llm, "call_llm", lambda _prompt: "not json")
    assert llm.score_task("task") == {"value": 3, "urgency": 3, "ease": 3}

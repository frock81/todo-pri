"""Tests for the scoring strategies module."""

from __future__ import annotations

from todo_cli import scorer


def test_wsjf_simplified_known_values() -> None:
    assert scorer.wsjf_simplified(4, 3, 2) == 21


def test_wsjf_simplified_zero_ease() -> None:
    assert scorer.wsjf_simplified(5, 5, 0) == 10


def test_wsjf_simplified_all_zero() -> None:
    assert scorer.wsjf_simplified(0, 0, 0) == 0


def test_linear_combo_known_values() -> None:
    assert scorer.linear_combo(4, 3, 2) == 13


def test_linear_combo_all_max() -> None:
    assert scorer.linear_combo(5, 5, 5) == 20


def test_get_strategy_returns_known_wsjf() -> None:
    assert scorer.get_strategy("wsjf_simplified") is scorer.wsjf_simplified


def test_get_strategy_returns_known_linear() -> None:
    assert scorer.get_strategy("linear_combo") is scorer.linear_combo


def test_get_strategy_unknown_falls_back_to_default() -> None:
    assert scorer.get_strategy("bogus") is scorer.wsjf_simplified


def test_compute_score_uses_selected_strategy() -> None:
    assert scorer.compute_score("linear_combo", 4, 3, 2) == 13


def test_compute_score_unknown_falls_back_to_default() -> None:
    assert scorer.compute_score("bogus", 4, 3, 2) == 21

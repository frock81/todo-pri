"""Scoring strategies for task prioritization.

Each strategy is a pure function taking ``(value, urgency, ease)`` and
returning an integer score. Strategies are registered in
``_STRATEGIES`` and resolved via :func:`get_strategy`.
"""

from __future__ import annotations

from collections.abc import Callable

Strategy = Callable[[int, int, int], int]

DEFAULT_STRATEGY = "wsjf_simplified"


def wsjf_simplified(value: int, urgency: int, ease: int) -> int:
    """Weighted Shortest Job First (simplified)."""
    return (value + urgency) * (1 + ease)


def linear_combo(value: int, urgency: int, ease: int) -> int:
    """Linear combination favoring value."""
    return 2 * value + urgency + ease


_STRATEGIES: dict[str, Strategy] = {
    "wsjf_simplified": wsjf_simplified,
    "linear_combo": linear_combo,
}


def get_strategy(name: str) -> Strategy:
    """Resolve a strategy by name, falling back to the default."""
    return _STRATEGIES.get(name, _STRATEGIES[DEFAULT_STRATEGY])


def compute_score(strategy_name: str, value: int, urgency: int, ease: int) -> int:
    """Compute a priority score for ``(value, urgency, ease)``."""
    return get_strategy(strategy_name)(value, urgency, ease)

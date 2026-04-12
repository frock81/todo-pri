"""Parsing helpers for ``todo.txt`` files."""

from __future__ import annotations

import re

_METADATA_KEYS = ("value", "urgency", "ease", "score")
_METADATA_RE = re.compile(r"\s*\b(?:" + "|".join(_METADATA_KEYS) + r"):-?\d+\b")


def _strip_metadata(line: str) -> str:
    """Remove known ``key:int`` metadata tokens from a line."""
    return _METADATA_RE.sub("", line).rstrip()


def parse_tasks(lines: list[str]) -> list[str]:
    """Return non-empty task strings with existing metadata stripped."""
    tasks: list[str] = []
    for raw in lines:
        stripped = raw.strip()
        if not stripped:
            continue
        tasks.append(_strip_metadata(stripped))
    return tasks


def read_tasks(path: str) -> list[str]:
    """Read a todo.txt file and return cleaned task strings."""
    with open(path, encoding="utf-8") as fh:
        return parse_tasks(fh.readlines())

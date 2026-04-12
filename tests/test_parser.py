"""Tests for the todo.txt parser."""

from __future__ import annotations

from pathlib import Path

import pytest

from todo_cli import parser


def test_parse_tasks_ignores_empty_and_whitespace_lines() -> None:
    lines = ["", "  ", "task A", "\t", "task B"]
    assert parser.parse_tasks(lines) == ["task A", "task B"]


def test_parse_tasks_preserves_priority_and_tags() -> None:
    task = "(A) Refactor auth module +backend @dev"
    assert parser.parse_tasks([task]) == [task]


def test_parse_tasks_strips_existing_metadata() -> None:
    line = "Fix bug value:4 urgency:3 ease:2 score:21"
    assert parser.parse_tasks([line]) == ["Fix bug"]


def test_parse_tasks_strips_partial_metadata() -> None:
    assert parser.parse_tasks(["Write docs urgency:2"]) == ["Write docs"]


def test_parse_tasks_strips_metadata_in_any_order() -> None:
    line = "Task score:10 value:4 ease:1 urgency:3"
    assert parser.parse_tasks([line]) == ["Task"]


def test_parse_tasks_does_not_strip_unrelated_colon_tokens() -> None:
    line = "Call Alice re: budget"
    assert parser.parse_tasks([line]) == [line]


def test_read_tasks_reads_from_file(tmp_path: Path) -> None:
    path = tmp_path / "todo.txt"
    path.write_text("task A\n\ntask B value:1 urgency:1 ease:1 score:4\n")
    assert parser.read_tasks(str(path)) == ["task A", "task B"]


def test_read_tasks_missing_file_raises(tmp_path: Path) -> None:
    missing = tmp_path / "nope.txt"
    with pytest.raises(FileNotFoundError):
        parser.read_tasks(str(missing))


def test_parse_tasks_handles_utf8_content() -> None:
    line = "Revisar relatório financeiro +finanças @urgente"
    assert parser.parse_tasks([line]) == [line]


def test_parse_tasks_strips_metadata_with_trailing_whitespace() -> None:
    line = "Task value:4 urgency:3 ease:2 score:21   "
    assert parser.parse_tasks([line]) == ["Task"]


def test_parse_tasks_empty_list_returns_empty_list() -> None:
    assert parser.parse_tasks([]) == []


def test_read_tasks_empty_file_returns_empty_list(tmp_path: Path) -> None:
    path = tmp_path / "empty.txt"
    path.write_text("")
    assert parser.read_tasks(str(path)) == []

"""Tests for the writer module."""

from __future__ import annotations

from pathlib import Path

from todo_pri import writer


def test_annotate_task_appends_metadata_in_order() -> None:
    task = "(A) Refactor auth module +backend @dev"
    annotated = writer.annotate_task(task, {"value": 4, "urgency": 3, "ease": 2}, 21)
    assert annotated == (
        "(A) Refactor auth module +backend @dev value:4 urgency:3 ease:2 score:21"
    )


def test_annotate_task_preserves_task_text_exactly() -> None:
    task = "Fix   spacing\tmatters +tag @ctx"
    annotated = writer.annotate_task(task, {"value": 1, "urgency": 2, "ease": 3}, 12)
    assert annotated.startswith(task + " ")


def test_backup_file_creates_bak_copy(tmp_path: Path) -> None:
    path = tmp_path / "todo.txt"
    path.write_text("line\n")
    bak = writer.backup_file(str(path))
    assert Path(bak).read_text() == "line\n"
    assert bak == str(path) + ".bak"


def test_backup_file_overwrites_existing_bak(tmp_path: Path) -> None:
    path = tmp_path / "todo.txt"
    path.write_text("v1\n")
    writer.backup_file(str(path))
    path.write_text("v2\n")
    writer.backup_file(str(path))
    assert Path(str(path) + ".bak").read_text() == "v2\n"


def test_write_tasks_writes_lines_with_trailing_newline(tmp_path: Path) -> None:
    path = tmp_path / "out.txt"
    writer.write_tasks(str(path), ["a", "b"])
    assert path.read_text() == "a\nb\n"


def test_write_tasks_empty_list_writes_empty_file(tmp_path: Path) -> None:
    path = tmp_path / "out.txt"
    writer.write_tasks(str(path), [])
    assert path.read_text() == ""


def test_write_tasks_uses_utf8(tmp_path: Path) -> None:
    path = tmp_path / "out.txt"
    writer.write_tasks(str(path), ["café"])
    assert path.read_text(encoding="utf-8") == "café\n"


def test_annotate_task_with_zero_scores() -> None:
    annotated = writer.annotate_task("task", {"value": 0, "urgency": 0, "ease": 0}, 0)
    assert annotated == "task value:0 urgency:0 ease:0 score:0"


def test_write_tasks_overwrites_existing_file(tmp_path: Path) -> None:
    path = tmp_path / "out.txt"
    path.write_text("old content\n")
    writer.write_tasks(str(path), ["new"])
    assert path.read_text() == "new\n"

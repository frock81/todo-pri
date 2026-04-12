"""End-to-end CLI tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from todo_pri import llm, main

runner = CliRunner()


def _patch_llm_from_table(
    monkeypatch: pytest.MonkeyPatch, table: dict[str, dict[str, int]]
) -> None:
    """Patch call_llm to return scores based on task text keywords."""

    def fake_call_llm(prompt: str) -> str:
        for keyword, scores in table.items():
            if keyword in prompt:
                return json.dumps(scores)
        return json.dumps({"value": 3, "urgency": 3, "ease": 3})

    monkeypatch.setattr(llm, "call_llm", fake_call_llm)


def _write_todo(tmp_path: Path, content: str) -> Path:
    path = tmp_path / "todo.txt"
    path.write_text(content, encoding="utf-8")
    return path


def test_cli_scores_sorts_and_writes_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_llm_from_table(
        monkeypatch,
        {
            "Refactor": {"value": 4, "urgency": 3, "ease": 2},  # wsjf=21
            "Fix login": {"value": 5, "urgency": 5, "ease": 1},  # wsjf=20
            "docs": {"value": 1, "urgency": 1, "ease": 1},  # wsjf=4
        },
    )
    path = _write_todo(
        tmp_path,
        "(A) Refactor auth module +backend @dev\n"
        "Fix login bug +backend @urgent\n"
        "Write documentation +docs\n",
    )

    result = runner.invoke(main.app, [str(path)])

    assert result.exit_code == 0, result.stderr
    lines = path.read_text().splitlines()
    assert lines[0].startswith("(A) Refactor auth module")
    assert "score:21" in lines[0]
    assert lines[1].startswith("Fix login bug")
    assert "score:20" in lines[1]
    assert lines[2].startswith("Write documentation")
    assert "score:4" in lines[2]


def test_cli_creates_backup_before_writing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_llm_from_table(monkeypatch, {})
    original = "task A\ntask B\n"
    path = _write_todo(tmp_path, original)

    result = runner.invoke(main.app, [str(path)])

    assert result.exit_code == 0
    bak = Path(str(path) + ".bak")
    assert bak.exists()
    assert bak.read_text() == original


def test_cli_default_strategy_is_wsjf_simplified(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_llm_from_table(monkeypatch, {"only": {"value": 4, "urgency": 3, "ease": 2}})
    path = _write_todo(tmp_path, "the only task\n")

    result = runner.invoke(main.app, [str(path)])

    assert result.exit_code == 0
    assert "score:21" in path.read_text()


def test_cli_linear_combo_strategy(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_llm_from_table(monkeypatch, {"only": {"value": 4, "urgency": 3, "ease": 2}})
    path = _write_todo(tmp_path, "the only task\n")

    result = runner.invoke(main.app, [str(path), "--strategy", "linear_combo"])

    assert result.exit_code == 0
    assert "score:13" in path.read_text()


def test_cli_unknown_strategy_falls_back_to_default(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_llm_from_table(monkeypatch, {"only": {"value": 4, "urgency": 3, "ease": 2}})
    path = _write_todo(tmp_path, "the only task\n")

    result = runner.invoke(main.app, [str(path), "--strategy", "bogus"])

    assert result.exit_code == 0
    assert "score:21" in path.read_text()


def test_cli_dry_run_does_not_modify_file_or_create_backup(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_llm_from_table(monkeypatch, {"only": {"value": 4, "urgency": 3, "ease": 2}})
    original = "the only task\n"
    path = _write_todo(tmp_path, original)

    result = runner.invoke(main.app, [str(path), "--dry-run"])

    assert result.exit_code == 0
    assert path.read_text() == original
    assert not Path(str(path) + ".bak").exists()
    assert "score:21" in result.stdout


def test_cli_idempotent_on_rerun(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_llm_from_table(
        monkeypatch,
        {
            "Refactor": {"value": 4, "urgency": 3, "ease": 2},
            "Fix": {"value": 5, "urgency": 5, "ease": 1},
        },
    )
    path = _write_todo(tmp_path, "(A) Refactor auth module\nFix login bug\n")

    first = runner.invoke(main.app, [str(path)])
    assert first.exit_code == 0
    first_content = path.read_text()

    second = runner.invoke(main.app, [str(path)])
    assert second.exit_code == 0
    assert path.read_text() == first_content


def test_cli_missing_file_exits_nonzero(tmp_path: Path) -> None:
    missing = tmp_path / "nope.txt"
    result = runner.invoke(main.app, [str(missing)])
    assert result.exit_code == 1
    assert "not found" in result.stderr.lower() or "no such" in result.stderr.lower()


def test_cli_empty_file_produces_empty_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_llm_from_table(monkeypatch, {})
    path = _write_todo(tmp_path, "")

    result = runner.invoke(main.app, [str(path)])

    assert result.exit_code == 0
    assert path.read_text() == ""
    assert Path(str(path) + ".bak").exists()


def test_cli_invalid_llm_response_uses_fallback_scores(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(llm, "call_llm", lambda _p: "garbage")
    path = _write_todo(tmp_path, "the only task\n")

    result = runner.invoke(main.app, [str(path)])

    assert result.exit_code == 0
    content = path.read_text()
    assert "value:3 urgency:3 ease:3 score:24" in content

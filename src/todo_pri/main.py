"""CLI entrypoint built with Typer."""

from __future__ import annotations

import sys
from pathlib import Path

import typer

from todo_pri import llm, parser, scorer, writer

app = typer.Typer(add_completion=False, no_args_is_help=True)


def _score_tasks(
    tasks: list[str], strategy_name: str
) -> list[tuple[str, dict[str, int], int]]:
    """Score each task and return ``(text, scores, score)`` tuples."""
    scored: list[tuple[str, dict[str, int], int]] = []
    for task in tasks:
        scores = llm.score_task(task)
        score = scorer.compute_score(
            strategy_name, scores["value"], scores["urgency"], scores["ease"]
        )
        scored.append((task, scores, score))
    return scored


def _sort_and_format(
    scored: list[tuple[str, dict[str, int], int]],
) -> list[str]:
    """Sort scored tasks by score descending and annotate them."""
    scored.sort(key=lambda item: item[2], reverse=True)
    return [writer.annotate_task(text, s, score) for text, s, score in scored]


def _run(path: str, strategy_name: str, dry_run: bool) -> int:
    """Execute the full pipeline for a single file."""
    try:
        tasks = parser.read_tasks(path)
    except FileNotFoundError:
        typer.echo(f"error: file not found: {path}", err=True)
        return 1
    except OSError as exc:
        typer.echo(f"error: cannot read {path}: {exc}", err=True)
        return 1

    annotated = _sort_and_format(_score_tasks(tasks, strategy_name))

    if dry_run:
        for line in annotated:
            typer.echo(line)
        return 0

    try:
        if Path(path).exists():
            writer.backup_file(path)
        writer.write_tasks(path, annotated)
    except OSError as exc:
        typer.echo(f"error: cannot write {path}: {exc}", err=True)
        return 1
    return 0


@app.command()
def prioritize(
    file: str = typer.Argument(..., help="Path to a todo.txt file."),
    strategy: str = typer.Option(
        scorer.DEFAULT_STRATEGY,
        "--strategy",
        help="Scoring strategy name. Unknown names fall back to default.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Print the result to stdout without modifying the file.",
    ),
) -> None:
    """Read a todo.txt file, score its tasks, and write them back sorted."""
    exit_code = _run(file, strategy, dry_run)
    if exit_code != 0:
        raise typer.Exit(code=exit_code)


def main(argv: list[str] | None = None) -> int:
    """Module-style entrypoint usable from ``python -m todo_pri.main``."""
    try:
        app(args=argv, standalone_mode=False)
    except typer.Exit as exc:
        return int(exc.exit_code)
    except SystemExit as exc:  # pragma: no cover - safety net
        return int(exc.code or 0)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())

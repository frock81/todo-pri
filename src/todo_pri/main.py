"""CLI entrypoint built with Typer."""

from __future__ import annotations

import sys

import typer

from todo_pri.app import app


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

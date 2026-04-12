"""Output helpers: annotation, backup, and file writing."""

from __future__ import annotations

import shutil


def annotate_task(task: str, scores: dict[str, int], score: int) -> str:
    """Append ``value:.. urgency:.. ease:.. score:..`` to a task string."""
    return (
        f"{task} value:{scores['value']} urgency:{scores['urgency']} "
        f"ease:{scores['ease']} score:{score}"
    )


def backup_file(path: str) -> str:
    """Copy ``path`` to ``path + '.bak'`` and return the backup path."""
    backup_path = f"{path}.bak"
    shutil.copyfile(path, backup_path)
    return backup_path


def write_tasks(path: str, lines: list[str]) -> None:
    """Write ``lines`` to ``path`` as UTF-8, one per line."""
    content = "\n".join(lines) + ("\n" if lines else "")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)

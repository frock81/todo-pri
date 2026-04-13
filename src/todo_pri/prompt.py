import json
from importlib.resources import files
from pathlib import Path

from pydantic import BaseModel

from todo_pri.model import Score

_PROMPT_HEADER = (
    "You are prioritizing a todo list task.\n"
    "Rate the task on three dimensions (integers 0-5):\n"
    "- value: business/personal value delivered\n"
    "- urgency: how time-sensitive it is\n"
    "- ease: how easy it is to complete (5 = trivial)\n"
    'Respond with STRICT JSON only: {"value": int, "urgency": int, "ease": int}.\n'
    "Task: "
)


def from_model_to_json_schema(model_cls: type[BaseModel] | None = None) -> str:
    """Convert a Pydantic model class to a JSON Schema str"""
    if model_cls is None:
        model_cls = Score
    return json.dumps(model_cls.model_json_schema())


def get_json_schema_prompt_footer(json_schema: str | None = None) -> str:
    """Return a prompt footer that includes the given JSON schema."""
    if json_schema is None:
        json_schema = from_model_to_json_schema()
    return f"\nThe response must conform to this JSON Schema:\n{json_schema}\n"


def read_prompt_header(prompt_path: str | Path | None = None) -> str:
    if prompt_path is None:
        prompt_path = Path(str(files("todo_pri").joinpath("prompt_header.md")))
    return Path(prompt_path).read_text()


def build_prompt(
    task: str,
    prompt_header: str | None = None,
    prompt_footer: str | None = None,
) -> str:
    """Return the LLM prompt for a single task."""
    if prompt_header is None:
        prompt_header = _PROMPT_HEADER
    return prompt_header + task + (prompt_footer or "")

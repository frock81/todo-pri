# Agents

This is the Agent understanding that aims to guide through agents design:

```
Agents are specialized roles (test_designer, coder, tester, reviewer) for technologies (FastAPI, Angular, etc) in a stack (frontend, backend) which may be even more specific (libs, cli, api, services, etc)
```

## Agents list

To ease the agent discovery by LLMs, here is the current agents list (generated using the `ls -1 agents/ | grep -v README.md | sed 's/^/- /'` command):

- angular_component_coder.md
- angular_reviewer.md
- angular_service_coder.md
- angular_test_engineer.md
- fastapi_endpoint_coder.md
- fastapi_reviewer.md
- fastapi_service_coder.md
- fastapi_test_designer.md
- fastapi_test_engineer.md
- planner.md
- shell_script_utils_coder.md

Keep this list updated.

## Agents Categories

Agent can be categorized by **task purpose**:

- planner
- test_designer
- coder
- tester
- reviewer

By **programming language**, for example:

- Python
- Javascript/Typescript

By **technology** (which sometimes embeds the programming language), for example:

- FastAPI (Python)
- Angular (Typescript)
- Click/Typer
- Pydantic

Or by **stack**:

- libraries (libs)
- services
- api (endpoints)
- cli
- frontend
- backend for frontend (bff)

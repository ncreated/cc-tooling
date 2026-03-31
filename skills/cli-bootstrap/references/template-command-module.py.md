# Command Module Template

Generate one `lib/{COMMAND_NAME}.py` per command. Each module is a stub for the user to implement.

```python
"""{TOOL_NAME} — {COMMAND_DESCRIPTION}."""

{UTILITY_IMPORTS}


class {CommandClass}Error(Exception):
    """{COMMAND_NAME} command failed."""


def {command_func}({FUNCTION_ARGS}) -> None:
    """{COMMAND_DESCRIPTION}."""
    raise NotImplementedError("TODO: implement {COMMAND_NAME}")
```

## Placeholders

- `{COMMAND_NAME}` — command name (lowercase, e.g. `fetch`)
- `{COMMAND_DESCRIPTION}` — one-line description from interview
- `{CommandClass}` — PascalCase version (e.g. `Fetch`)
- `{command_func}` — snake_case function name (e.g. `fetch`)
- `{FUNCTION_ARGS}` — typed arguments matching the command's selected flags:
  - If `-f/--force`: `force: bool = False`
  - If `-j/--jobs`: `max_workers: int = 1`
  - If `-v/--verbose`: `verbose: bool = False`
  - Positional args come first without defaults
  - Custom flags follow with their types and defaults
- `{UTILITY_IMPORTS}` — conditional imports based on which utilities the command will use:
  - If shell: `from lib.utils.shell import run, ShellError`
  - If tasks: `from lib.utils.tasks import run_parallel`
  - If logger: `from lib.utils.logger import Logger`

## Also create

- `lib/__init__.py` — empty file
- `lib/utils/__init__.py` — empty file

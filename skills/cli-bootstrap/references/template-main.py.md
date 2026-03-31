# main.py Template

Generate a `main.py` following this structure. Assemble it from the skeleton and per-command fragments based on the interview results.

## Skeleton

```python
#!/usr/bin/env python3
"""{TOOL_NAME} — {TOOL_DESCRIPTION}."""

import argparse
import os
import sys

{IMPORTS_BLOCK}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


{HANDLER_BLOCK}


def main() -> int:
    parser = argparse.ArgumentParser(description="{TOOL_DESCRIPTION}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    {SUBPARSER_BLOCK}

    args = parser.parse_args()

    try:
        {DISPATCH_BLOCK}
    except {ERROR_CLASSES} as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

Where `{ERROR_CLASSES}` is a tuple of all command error classes, e.g. `(FetchError, ProcessError, ReportError)`.

## Fragments

### Import fragment (one per command)

```python
from lib.{COMMAND_NAME} import {CommandClass}Error, {command_func}
```

### Handler fragment (one per command)

Each handler calls the command's main function directly — no try/except here, errors propagate to `main()`:

```python
def cmd_{COMMAND_NAME}(args) -> int:
    {command_func}({CALL_ARGS})
    return 0
```

Where `{CALL_ARGS}` threads the parsed arguments through. Examples based on selected flags:
- If command has positional `target`: `args.target`
- If command has `-f/--force`: `force=args.force`
- If command has `-j/--jobs`: `max_workers=args.jobs`
- If command has `-v/--verbose`: `verbose=args.verbose`

### Subparser fragment (one per command)

```python
    sub_{COMMAND_NAME} = subparsers.add_parser("{COMMAND_NAME}", help="{COMMAND_HELP}")
```

Then add arguments based on the interview:

**Positional argument:**
```python
    sub_{COMMAND_NAME}.add_argument("{ARG_NAME}", help="{ARG_HELP}")
```

**Common flags:**

`-f/--force`:
```python
    sub_{COMMAND_NAME}.add_argument("-f", "--force", action="store_true", help="Re-run even if outputs already exist")
```

`-j/--jobs`:
```python
    sub_{COMMAND_NAME}.add_argument("-j", "--jobs", type=int, default=1, help="Number of parallel workers (default: 1)")
```

`-v/--verbose`:
```python
    sub_{COMMAND_NAME}.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
```

**Custom flags** follow the same `add_argument` pattern with the type/default/help from the interview.

### Dispatch fragment (one per command)

```python
        if args.command == "{COMMAND_NAME}":
            return cmd_{COMMAND_NAME}(args)
```

Chain with `elif` for subsequent commands. Note the extra indentation — these are inside the `try:` block.

## Assembly Rules

1. Combine all import fragments at the top
2. Place all handler functions after `SCRIPT_DIR`
3. Place all subparser fragments inside `main()`, after `subparsers = ...`
4. Place the centralized `try:/except` in `main()` after `args = parser.parse_args()`
5. Place all dispatch fragments inside the `try:` block
6. The `except` clause catches a tuple of all `{CommandClass}Error` classes from all commands
7. Use `if`/`elif` chain for dispatch (not a dict lookup)

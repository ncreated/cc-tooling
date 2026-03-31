# Extend Mode Guide

When extending an existing CLI tool, follow these instructions for each operation type.

## 1. Add a New Command

### Step 1: Create the command module

Create `lib/{COMMAND_NAME}.py` using the command module template.

### Step 2: Add import to main.py

Find the existing import block (lines with `from lib.X import ...`) and add:

```python
from lib.{COMMAND_NAME} import {CommandClass}Error, {command_func}
```

### Step 3: Add handler function to main.py

Find the last `cmd_*` function and add the new handler after it:

```python
def cmd_{COMMAND_NAME}(args) -> int:
    {command_func}({CALL_ARGS})
    return 0
```

### Step 3b: Add error class to the centralized except clause

Find the `except (...) as e:` tuple in `main()` and add `{CommandClass}Error` to it.

### Step 4: Add subparser to main.py

Find the subparser definitions inside `main()` and add a new one:

```python
    sub_{COMMAND_NAME} = subparsers.add_parser("{COMMAND_NAME}", help="{COMMAND_HELP}")
    # add arguments...
```

### Step 5: Add dispatch case to main.py

Find the if/elif dispatch chain and add:

```python
    elif args.command == "{COMMAND_NAME}":
        return cmd_{COMMAND_NAME}(args)
```

### Step 6: Update CLAUDE.md

Add the new command to the commands table and update the project structure tree.

---

## 2. Add Options to an Existing Command

### Step 1: Find the subparser

In `main.py`, locate the subparser for the target command:
```python
    sub_{COMMAND_NAME} = subparsers.add_parser("{COMMAND_NAME}", ...)
```

### Step 2: Add the argument

Add `add_argument` call after the existing arguments for that subparser:

```python
    sub_{COMMAND_NAME}.add_argument("{FLAG}", type={TYPE}, default={DEFAULT}, help="{HELP}")
```

### Step 3: Thread through the handler

Update the `cmd_{COMMAND_NAME}` function to pass the new argument to the underlying function:

In the handler's function call, add the new kwarg:
```python
    {command_func}(..., new_arg=args.new_arg)
```

### Step 4: Update the command module

In `lib/{COMMAND_NAME}.py`, add the new parameter to the function signature:
```python
def {command_func}(..., new_arg: type = default) -> None:
```

### Step 5: Update CLAUDE.md

Update the commands table with the new option.

---

## 3. Add a Utility Module

### Step 1: Check if it exists

Check if `lib/utils/{UTILITY_NAME}.py` already exists. If it does, inform the user and skip.

### Step 2: Create the file

Generate from the corresponding template:
- `shell.py` → `template-shell.py.md`
- `tasks.py` → `template-tasks.py.md`
- `logger.py` → `template-logger.py.md`

### Step 3: Ensure directory structure

Create `lib/utils/__init__.py` if it doesn't exist.

### Step 4: Handle dependencies

If adding `tasks.py`, also add `logger.py` (tasks depends on logger).

### Step 5: Update CLAUDE.md

Add the utility to the project structure tree and document its usage.

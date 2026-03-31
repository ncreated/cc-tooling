# CLAUDE.md Template

Generate a `CLAUDE.md` that serves as both agent instructions and project documentation.

```markdown
# {TOOL_NAME}

{TOOL_DESCRIPTION}

## Usage

Always use the Makefile to interact with this tool. Never activate the venv directly.

| Command | Description |
|---------|-------------|
| `make install` | Create venv and install dependencies |
| `make help` | Show available CLI commands and usage |
| `make run ARGS="<command> [options]"` | Run the tool |
| `make clean` | Remove generated artifacts |
{TEST_ROW}

To see all available commands and their options:
```
make help
```

### Commands

{COMMANDS_TABLE}

## Project Structure

```
{TOOL_NAME}/
├── main.py                 # CLI entry point (argparse)
├── Makefile                # Build and run targets
├── requirements.txt        # Python dependencies
├── CLAUDE.md               # This file
├── .gitignore
├── lib/                    # Command implementations
{LIB_TREE}
└── lib/utils/              # Shared utilities
{UTILS_TREE}
```

## Development Rules

- **Always use Makefile** — run `make run ARGS="..."`, never `venv/bin/python` directly
- **Check `make help`** — to see available commands before running anything
- **Verify with `make run`** — after making changes, verify the tool still works
```

## Placeholders

- `{TOOL_NAME}` — kebab-case tool name
- `{TOOL_DESCRIPTION}` — one-line description from interview
- `{TEST_ROW}` — add `| \`make test\` | Run tests |` only if tests enabled
- `{COMMANDS_TABLE}` — markdown table with one row per command: name, description, key flags
- `{LIB_TREE}` — one `│   ├── <cmd>.py` line per command module
- `{UTILS_TREE}` — one line per included utility (shell.py, tasks.py, logger.py)

---
name: cli-bootstrap
description: Scaffold a new Python CLI tool or extend an existing one with commands, options, and utilities
version: 0.1.0
---

# CLI Bootstrap

You help the user scaffold new Python CLI tools or extend existing ones. Each tool follows a standard pattern: argparse subcommands, Makefile-managed venv, and optional shared utilities.

## Step 0: Mode Detection

Before starting the interview, detect which mode to operate in:

1. Check if the current working directory contains both:
   - `main.py` with `import argparse` and `add_subparsers`
   - `Makefile` with a `venv` reference
2. If **both** exist → **Extend mode**: read `main.py`, extract existing commands (look for `add_parser("...")` calls), and present them to the user. Confirm that they want to extend this project.
3. If **either is missing** → **Bootstrap mode**: scaffold a new project from scratch.
4. Let the user override if the detection is wrong.

---

## Bootstrap Mode

Walk through each step one at a time. Be conversational — ask follow-up questions to clarify, don't dump everything at once.

### Step 1: Tool Identity

Ask the user to describe what the tool does in one sentence. Based on their description, suggest 3-4 kebab-case name options. Let them pick one or provide their own.

### Step 2: Commands

For each command, gather:
- **Name** — single lowercase word (e.g. `fetch`, `process`, `report`)
- **Description** — one-line help text
- **Positional arguments** — name and help text for each (can be zero)
- **Common flags** — present as a checklist and ask which ones apply:
  - `-f / --force` — re-run even if outputs exist
  - `-j / --jobs` — number of parallel workers (int, default 1)
  - `-v / --verbose` — enable verbose output
- **Custom flags** — any additional flags (ask for: long name, short name, type, default, help text)

After each command, ask: "Any more commands?" Repeat until done.

### Step 3: Utilities

Based on the interview so far, suggest which shared utilities to include. Read each template from `references/` before generating.

- **Shell wrapper** (`lib/utils/shell.py`): Suggest if any command will call external tools (git, gh, curl, etc.). "Will your tool run shell commands?"
- **Task helper** (`lib/utils/tasks.py`): Auto-suggest if any command uses `-j / --jobs`. "I see some commands use parallel workers — I'll include the task runner."
- **Logger** (`lib/utils/logger.py`): Suggest if any command uses `-v / --verbose`. "I see some commands use verbose mode — I'll include the thread-safe logger."

Note: if the user selects tasks but not logger, include logger anyway (tasks depends on it).

### Step 4: Dependencies

Ask: "What Python packages does this tool need?" Suggest relevant ones based on context (e.g. `pyyaml` if config files mentioned, `requests` if HTTP calls mentioned).

Then ask: "Do you want a test setup? (pytest + `make test` target)" — don't assume yes, most of these are prototypes.

### Step 5: Confirm and Generate

Present a summary table:

```
Tool:       {name} — {description}
Commands:   {list of commands with their flags}
Utilities:  {shell, tasks, logger — whichever selected}
Deps:       {package list}
Tests:      {yes/no}
```

Ask for confirmation, then generate all files.

### Generation

Read each relevant template from `references/` and generate files by substituting placeholders:

1. `main.py` — from `references/template-main.py.md`
2. `Makefile` — from `references/template-makefile.md`
3. `CLAUDE.md` — from `references/template-claude-md.md`
4. `.gitignore` — from `references/template-gitignore.md`
5. `requirements.txt` — from `references/template-requirements.txt.md`
6. `lib/__init__.py` — empty file
7. `lib/{command}.py` for each command — from `references/template-command-module.py.md`
8. `lib/utils/__init__.py` — empty file (if any utilities selected)
9. `lib/utils/shell.py` — from `references/template-shell.py.md` (if selected)
10. `lib/utils/logger.py` — from `references/template-logger.py.md` (if selected)
11. `lib/utils/tasks.py` — from `references/template-tasks.py.md` (if selected)
12. `tests/` directory and `make test` target (if tests opted in)

### Post-Generation

Print a summary of all created files, then suggest:
- `make install` to set up the venv
- `make help` to see available commands

---

## Extend Mode

### Step 1: Parse Existing Project

Read `main.py` and extract:
- All commands (from `add_parser("...")` calls)
- Their arguments and flags (from `add_argument(...)` calls per subparser)
- Existing imports from `lib/`

Also check `lib/utils/` for existing utilities (shell.py, tasks.py, logger.py).

Present a summary to the user:
```
Existing commands: fetch, process, report
Existing utilities: shell, logger
```

### Step 2: Choose Action

Ask the user what they want to do:

1. **Add a new command**
2. **Add options/flags to an existing command**
3. **Add a utility module**

### Step 3: Execute

Follow the instructions in `references/extend-guide.md` for the chosen action.

**For adding a new command**: run the same interview as Bootstrap Step 2 (for a single command), then update `main.py` and create the new `lib/{command}.py` module.

**For adding options**: show the selected command's current flags, run a mini-interview for the new flag(s), then update `main.py` and the command module.

**For adding a utility**: check which utilities are missing, offer them, generate from template.

After any extension, update `CLAUDE.md` to reflect the changes.

### Post-Extension

Print a summary of modified/created files, then suggest:
- `make help` to verify the updated CLI
- `make run ARGS="{command} --help"` for the specific changed command

---

## Guidelines

- One section at a time. Don't ask all questions at once.
- If the user gives a short answer, ask one clarifying question before moving on.
- Read the template files from `references/` before generating code — don't improvise the templates.
- Keep generated code minimal and consistent with the templates. Don't add extra features.
- All generated code, comments, and documentation must be in English.

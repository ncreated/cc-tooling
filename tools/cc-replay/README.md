# cc-replay

Converts Claude Code session JSONL files into standalone, self-contained HTML for easy review.

## What it does

Claude Code stores conversation history as JSONL files in `~/.claude/projects/`. This tool parses those files and produces a single HTML page where you can browse the full conversation — messages, tool calls, thinking blocks, and subagent sessions — with no external dependencies.

### Features

- User and assistant messages rendered as chat blocks
- Tool calls with inputs and results (collapsible, collapsed by default)
- Extended thinking blocks (collapsible)
- Subagent sessions as nested collapsible sections
- Expand All / Collapse All toolbar
- Multiline strings in tool inputs formatted with real line breaks
- Parse errors surfaced as warning banners (not silently dropped)
- Dark theme, monospace, single-file HTML (no external resources)

## Setup

```sh
cd tools/cc-replay
make install
```

This creates a `.venv/` and installs dependencies.

## Usage

```sh
# Generate HTML and auto-open in browser
make run ARGS="<path-to-session.jsonl>"

# Custom output path
make run ARGS="<path-to-session.jsonl> -o output.html"

# Generate without opening browser
make run ARGS="<path-to-session.jsonl> --no-open"
```

By default, the HTML file is written to `/tmp/ccreplay/<session_id>.html` and opened in the browser automatically.

### Arguments

| Argument | Description |
|---|---|
| `session_file` | Path to the `.jsonl` session file |
| `-o`, `--output` | Output HTML file path (default: `/tmp/ccreplay/<session_id>.html`) |
| `--no-subagents` | Skip subagent discovery and rendering |
| `--no-open` | Do not open the HTML file in browser after generating |

### Example

```sh
make run ARGS="~/.claude/projects/-Users-me-myproject/abc123.jsonl"
```

## Session file location

Claude Code stores sessions at:

```
~/.claude/projects/{encoded-project-path}/{session-uuid}.jsonl
```

Where the project path has slashes replaced with dashes (e.g. `/Users/me/myproject` becomes `-Users-me-myproject`).

Subagent files live in a subdirectory:

```
~/.claude/projects/{project}/{session-uuid}/subagents/agent-{id}.jsonl
```

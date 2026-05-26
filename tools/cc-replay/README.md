# cc-replay

Tools for browsing, searching, and reviewing Claude Code / Codex session history.

## Setup

```sh
cd tools/cc-replay
make install
```

This creates a `.venv/` and installs dependencies.

## Watch mode (web UI)

`make watch` starts a local web UI for browsing and viewing all your sessions.

```sh
make watch
# or with a custom port (default: 8833)
make watch ARGS="--port 9000"
```

Open `http://localhost:8833/` to browse sessions, search across them, and view rendered conversations directly in the browser.

## Single session replay

Converts a session JSONL file into a standalone, self-contained HTML page — messages, tool calls, thinking blocks, and subagent sessions — with no external dependencies.

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

## MCP server

When the `cc-tooling` plugin is loaded by Claude Code (e.g. via `claude --plugin-dir /path/to/cc-tooling`), an `ccreplay` MCP server becomes available to the agent. It exposes four tools:

| Tool | Purpose |
|---|---|
| `list_projects` | Enumerate projects that have recorded sessions, with counts. |
| `list_sessions` | List sessions, filtered by project / ISO date range / format / limit. |
| `search_sessions` | Full-text grep across session contents, with the same filters. |
| `get_session` | Return a structured-text transcript of one session by `session_id`. |

`session_id` is the JSONL filename stem (UUID for Claude, `rollout-...-{uuid}` for Codex). Transcripts include user/assistant text and tool-call summaries; thinking, tool results, and images are omitted to keep them token-efficient for downstream LLM analysis.

The server bootstraps itself on first run — `bin/ccreplay-mcp` creates `.venv/` and installs `requirements.txt` automatically, so no `make install` is required just to use the MCP.

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

"""Session analysis via claude CLI for ccwatch."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def _get_parsers(session_path: str):
    """Import and return the appropriate parser + format for a session file."""
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from ccreplay.shared import detect_format

    fmt = detect_format(session_path)
    if fmt == "codex":
        from ccreplay.codex.parser import parse_codex_session
        return parse_codex_session, fmt
    else:
        from ccreplay.claude.parser import parse_claude_session
        return parse_claude_session, fmt


def prepare_session_transcript(session_path: str) -> str:
    """Parse a session and produce a clean text transcript.

    Includes user/assistant text and tool-use summaries.
    Omits tool results, thinking blocks, and images.
    """
    parse_fn, fmt = _get_parsers(session_path)
    session = parse_fn(session_path, include_subagents=False)

    # Gather metadata
    project = Path(session_path).parent.name if fmt == "claude" else ""
    timestamp = session.messages[0].timestamp if session.messages else ""

    lines: list[str] = []
    for msg in session.messages:
        if msg.is_meta:
            continue

        role_label = "[User]" if msg.role.value == "user" else "[Assistant]"

        for block in msg.content_blocks:
            btype = block.type.value

            if btype == "text" and block.text.strip():
                text = block.text.strip()
                lines.append(f"{role_label}: {text}")

            elif btype == "tool_use" and block.tool_name:
                # Summarise tool invocation — first line of input only
                summary = block.tool_input.split("\n", 1)[0][:120] if block.tool_input else ""
                if summary:
                    lines.append(f"[Tool: {block.tool_name} {summary}]")
                else:
                    lines.append(f"[Tool: {block.tool_name}]")

            # tool_result, thinking, image, reasoning_encrypted — skip

    transcript = "\n".join(lines)

    # Middle-truncate if too long
    max_chars = 80_000
    if len(transcript) > max_chars:
        # Keep first and last portions
        half = max_chars // 2
        head = transcript[:half]
        tail = transcript[-half:]
        omitted = len(transcript) - max_chars
        transcript = f"{head}\n\n[... {omitted} characters omitted ...]\n\n{tail}"

    # Wrap in session tag with metadata
    attrs = f'format="{fmt}"'
    if project:
        attrs += f' project="{project}"'
    if timestamp:
        attrs += f' timestamp="{timestamp}"'

    return f"<session {attrs}>\n{transcript}\n</session>"


def analyze_sessions(session_paths: list[str], prompt: str) -> str:
    """Analyze one or more sessions by piping transcripts + prompt to claude -p."""
    if not shutil.which("claude"):
        return "Error: 'claude' CLI not found in PATH. Install Claude Code to use session analysis."

    # Prepare transcripts
    transcripts: list[str] = []
    for path in session_paths:
        try:
            transcripts.append(prepare_session_transcript(path))
        except Exception as exc:
            transcripts.append(f"<session error=\"{exc}\">[Failed to parse: {path}]</session>")

    # Build full prompt: transcripts + user question
    full_prompt = "\n\n".join(transcripts) + "\n\n" + prompt

    try:
        result = subprocess.run(
            ["claude", "-p"],
            input=full_prompt,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            stderr = result.stderr.strip()
            return f"Error: claude exited with code {result.returncode}\n{stderr}"
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Error: Analysis timed out after 120 seconds."
    except OSError as exc:
        return f"Error running claude CLI: {exc}"

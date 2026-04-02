"""CLI entry point for cc-replay."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from .shared import detect_format


def main() -> None:
    ap = argparse.ArgumentParser(
        prog="cc-replay",
        description="Convert a Claude Code or Codex session JSONL file to standalone HTML.",
    )
    ap.add_argument(
        "session_file",
        help="Path to the .jsonl session file",
    )
    ap.add_argument(
        "-o", "--output",
        help="Output HTML file path (default: <session_id>.html in /tmp/ccreplay/)",
    )
    ap.add_argument(
        "--format",
        choices=["auto", "claude", "codex"],
        default="auto",
        help="Session format (default: auto-detect)",
    )
    ap.add_argument(
        "--no-subagents",
        action="store_true",
        help="Skip subagent discovery and rendering",
    )
    ap.add_argument(
        "--no-open",
        action="store_true",
        help="Do not open the HTML file in browser after generating",
    )

    args = ap.parse_args()

    session_path = Path(args.session_file).expanduser().resolve()
    if not session_path.exists():
        print(f"Error: file not found: {session_path}", file=sys.stderr)
        sys.exit(1)

    # Detect format
    fmt = args.format
    if fmt == "auto":
        fmt = detect_format(str(session_path))

    # Parse and render
    if fmt == "codex":
        from .codex.parser import parse_codex_session
        from .codex.renderer import render

        session = parse_codex_session(
            str(session_path), include_subagents=not args.no_subagents,
        )
        html_output = render(session)
        session_id = session.session_id or session_path.stem
    else:
        from .claude.parser import parse_claude_session
        from .claude.renderer import render

        session = parse_claude_session(
            str(session_path), include_subagents=not args.no_subagents,
        )
        html_output = render(session)
        session_id = session.session_id

    if args.output:
        out_path = Path(args.output)
    else:
        tmp_dir = Path("/tmp/ccreplay")
        tmp_dir.mkdir(parents=True, exist_ok=True)
        out_path = tmp_dir / f"{session_id}.html"

    out_path.write_text(html_output, encoding="utf-8")
    print(f"Written to {out_path}")

    if not args.no_open:
        subprocess.run(["open", str(out_path)])


if __name__ == "__main__":
    main()

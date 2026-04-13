"""HTTP server for ccwatch — browse and view Claude Code / Codex sessions."""

from __future__ import annotations

import argparse
import base64
import json
import sys
from dataclasses import asdict
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from .discovery import discover_sessions, search_sessions
from .template import SHELL_HTML

# Allowed path prefixes for session rendering (security check)
_ALLOWED_PREFIXES = (
    str(Path.home() / ".claude" / "projects"),
    str(Path.home() / ".codex" / "sessions"),
)


def _encode_path(path: str) -> str:
    return base64.urlsafe_b64encode(path.encode()).decode()


def _decode_path(encoded: str) -> str:
    return base64.urlsafe_b64decode(encoded.encode()).decode()


def _validate_path(path: str) -> bool:
    """Check that the resolved path is under an allowed prefix."""
    resolved = str(Path(path).resolve())
    return any(resolved.startswith(prefix) for prefix in _ALLOWED_PREFIXES)


def _render_session(path: str) -> str:
    """Parse and render a session file to HTML using ccreplay."""
    # Import ccreplay modules — they live next to us in the package tree
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from ccreplay.shared import detect_format

    fmt = detect_format(path)
    if fmt == "codex":
        from ccreplay.codex.parser import parse_codex_session
        from ccreplay.codex.renderer import render
        session = parse_codex_session(path, include_subagents=True)
    else:
        from ccreplay.claude.parser import parse_claude_session
        from ccreplay.claude.renderer import render
        session = parse_claude_session(path, include_subagents=True)

    return render(session)


class WatchHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._serve_html(SHELL_HTML.format(), 200)
        elif parsed.path == "/api/sessions":
            self._serve_sessions_json(parse_qs(parsed.query))
        elif parsed.path.startswith("/session/"):
            self._serve_session()
        else:
            self.send_error(404)

    def _serve_html(self, html: str, code: int = 200):
        body = html.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_sessions_json(self, params=None):
        params = params or {}
        q = params.get("q", [""])[0].strip()
        type_filter = params.get("type", ["all"])[0]

        if q:
            sessions = search_sessions(q, limit=100)
        else:
            sessions = discover_sessions(limit=100)

        if type_filter and type_filter != "all":
            sessions = [s for s in sessions if s.format == type_filter]

        data = []
        for s in sessions:
            d = asdict(s)
            d["encoded"] = _encode_path(s.path)
            data.append(d)
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_session(self):
        encoded = self.path[len("/session/"):]
        try:
            path = _decode_path(encoded)
        except Exception:
            self.send_error(400, "Invalid session path encoding")
            return

        if not _validate_path(path):
            self.send_error(403, "Path not allowed")
            return

        if not Path(path).is_file():
            self.send_error(404, "Session file not found")
            return

        try:
            html = _render_session(path)
            self._serve_html(html)
        except Exception as exc:
            self.send_error(500, f"Render error: {exc}")

    def log_message(self, format, *args):
        # Quieter logging — only show errors
        if args and isinstance(args[0], str) and args[0].startswith("2"):
            return  # skip 2xx
        super().log_message(format, *args)


def main():
    ap = argparse.ArgumentParser(
        prog="ccwatch",
        description="Browse and view Claude Code / Codex sessions in a local web UI.",
    )
    ap.add_argument(
        "--port", type=int, default=8833,
        help="Port to listen on (default: 8833)",
    )
    args = ap.parse_args()

    server = HTTPServer(("127.0.0.1", args.port), WatchHandler)
    print(f"ccwatch running at http://localhost:{args.port}/")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()

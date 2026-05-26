"""ccreplay MCP server entrypoint.

Exposes four tools over stdio so any Claude Code instance with the
cc-tooling plugin loaded can query Claude/Codex session history:

- list_projects: enumerate projects with session counts
- list_sessions: filter sessions by project / date / format
- search_sessions: full-text grep across session contents
- get_session: return a structured-text transcript of one session

The server reuses the discovery, search, and transcript helpers from
ccwatch and ccreplay so it stays a thin shim.
"""

from __future__ import annotations

import sys
from collections import Counter
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

# ccreplay_mcp lives next to ccwatch and ccreplay in tools/cc-replay/.
# Ensure that directory is on sys.path so the shared helpers are importable
# whether the server is started via the bootstrap wrapper or invoked directly.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp.server.fastmcp import FastMCP  # noqa: E402

from ccwatch.analysis import prepare_session_transcript  # noqa: E402
from ccwatch.discovery import (  # noqa: E402
    SessionInfo,
    _build_claude_session_info,
    _build_codex_session_info,
    _collect_searchable_paths,
)
from ccwatch.discovery import search_sessions as _search_sessions_impl  # noqa: E402

mcp = FastMCP("ccreplay")

# Cap how many files we inspect to keep tool calls bounded. Reading the
# first ~30 lines of each JSONL is cheap, but we don't want pathological
# directories to stall the server.
_SCAN_LIMIT = 2000


def _parse_iso_date(value: str | None) -> datetime | None:
    """Parse an ISO 8601 date or datetime string into a tz-aware datetime.

    Accepts plain dates ('2026-05-01'), datetimes ('2026-05-01T12:00:00'),
    and trailing 'Z'. Bare dates are interpreted as midnight UTC.
    """
    if not value:
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(
            f"Invalid ISO 8601 date/time: {value!r} ({exc})"
        ) from exc
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _session_timestamp(info: SessionInfo) -> datetime | None:
    return _parse_iso_date(info.timestamp) if info.timestamp else None


def _scan_sessions(scan_limit: int = _SCAN_LIMIT) -> list[SessionInfo]:
    """Collect SessionInfo for the most-recent *scan_limit* session files."""
    candidates = _collect_searchable_paths(scan_limit)
    sessions: list[SessionInfo] = []
    for _mtime, path, fmt in candidates:
        info = (
            _build_claude_session_info(path)
            if fmt == "claude"
            else _build_codex_session_info(path)
        )
        if info:
            sessions.append(info)
    sessions.sort(key=lambda s: s.timestamp, reverse=True)
    return sessions


def _session_id_from_path(path: str) -> str:
    """Stable identifier for a session: the JSONL filename stem."""
    return Path(path).stem


def _resolve_session_id(session_id: str) -> SessionInfo | None:
    """Find the session whose file stem matches *session_id*."""
    for _mtime, path, fmt in _collect_searchable_paths(_SCAN_LIMIT):
        if path.stem != session_id:
            continue
        if fmt == "claude":
            return _build_claude_session_info(path)
        return _build_codex_session_info(path)
    return None


def _info_to_dict(info: SessionInfo) -> dict:
    d = asdict(info)
    d["session_id"] = _session_id_from_path(info.path)
    return d


def _filter_sessions(
    sessions: list[SessionInfo],
    project: str | None,
    since: datetime | None,
    until: datetime | None,
    fmt: str | None,
) -> list[SessionInfo]:
    out: list[SessionInfo] = []
    project_lc = project.lower() if project else None
    for s in sessions:
        if project_lc and s.project.lower() != project_lc:
            continue
        if fmt and s.format != fmt:
            continue
        ts = _session_timestamp(s)
        if since and (ts is None or ts < since):
            continue
        if until and (ts is None or ts > until):
            continue
        out.append(s)
    return out


@mcp.tool()
def list_projects(limit: int = 100) -> dict:
    """List projects with the number of sessions found for each.

    Scans recent Claude Code and Codex sessions on disk and groups them
    by detected project name. Useful as a first call to discover what
    projects have recorded sessions before drilling in with list_sessions.

    Args:
        limit: Maximum number of projects to return (default: 100).
               Projects are ordered by session count descending.

    Returns:
        Dict with 'projects' (list of {name, session_count, latest_timestamp})
        and 'total_sessions_scanned'.
    """
    sessions = _scan_sessions()
    counter: Counter[str] = Counter()
    latest: dict[str, str] = {}
    for s in sessions:
        counter[s.project] += 1
        if s.timestamp and (s.project not in latest or s.timestamp > latest[s.project]):
            latest[s.project] = s.timestamp

    projects = [
        {
            "name": name,
            "session_count": count,
            "latest_timestamp": latest.get(name, ""),
        }
        for name, count in counter.most_common(limit)
    ]
    return {
        "projects": projects,
        "total_sessions_scanned": len(sessions),
    }


@mcp.tool()
def list_sessions(
    project: str | None = None,
    since: str | None = None,
    until: str | None = None,
    format: str | None = None,
    limit: int = 50,
) -> dict:
    """List recorded sessions, optionally filtered by project, date, or format.

    Args:
        project: Exact project name to filter by (case-insensitive).
                 Use list_projects to discover available names.
        since: ISO 8601 date/datetime. Only sessions starting at or after
               this moment are returned (e.g. '2026-05-16' or
               '2026-05-16T12:00:00Z').
        until: ISO 8601 date/datetime. Only sessions starting at or before
               this moment are returned.
        format: Either 'claude' or 'codex' to restrict to one source.
        limit: Maximum number of sessions to return (default: 50).

    Returns:
        Dict with 'sessions' (list of metadata records including session_id,
        project, timestamp, format, slug, first_prompt, git_branch, path)
        and 'count'.
    """
    if format and format not in ("claude", "codex"):
        raise ValueError(f"format must be 'claude' or 'codex', got {format!r}")

    since_dt = _parse_iso_date(since)
    until_dt = _parse_iso_date(until)

    sessions = _scan_sessions()
    filtered = _filter_sessions(sessions, project, since_dt, until_dt, format)
    out = [_info_to_dict(s) for s in filtered[:limit]]
    return {"sessions": out, "count": len(out)}


@mcp.tool()
def search_sessions(
    query: str,
    project: str | None = None,
    since: str | None = None,
    until: str | None = None,
    format: str | None = None,
    limit: int = 50,
) -> dict:
    """Full-text search across session contents.

    Performs a case-insensitive literal substring match against the raw
    JSONL of every session file (via grep). Returns matching sessions
    with the same metadata schema as list_sessions, with the same
    optional filters applied on top of the text match.

    Args:
        query: Substring to search for (case-insensitive, literal — not regex).
        project: Optional project name filter.
        since: Optional ISO 8601 lower bound on session start time.
        until: Optional ISO 8601 upper bound on session start time.
        format: Optional 'claude' or 'codex' filter.
        limit: Maximum number of sessions to return (default: 50).

    Returns:
        Dict with 'sessions', 'count', and the original 'query'.
    """
    if not query.strip():
        raise ValueError("query must not be empty")
    if format and format not in ("claude", "codex"):
        raise ValueError(f"format must be 'claude' or 'codex', got {format!r}")

    since_dt = _parse_iso_date(since)
    until_dt = _parse_iso_date(until)

    matches = _search_sessions_impl(query, limit=_SCAN_LIMIT)
    filtered = _filter_sessions(matches, project, since_dt, until_dt, format)
    out = [_info_to_dict(s) for s in filtered[:limit]]
    return {"sessions": out, "count": len(out), "query": query}


@mcp.tool()
def get_session(session_id: str) -> dict:
    """Return a structured-text transcript of one session.

    The transcript labels each turn ('[User]:', '[Assistant]:') and
    summarises tool invocations on their own lines ('[Tool: Name input...]').
    Thinking blocks, tool results, and images are omitted to keep the
    output token-efficient for downstream LLM analysis. Very long
    transcripts are middle-truncated.

    Args:
        session_id: The session's file stem (e.g. the UUID for Claude,
                    or 'rollout-...-{uuid}' for Codex). Obtain it from
                    list_sessions or search_sessions.

    Returns:
        Dict with metadata (session_id, project, timestamp, format, path)
        and 'transcript' — a structured-text rendering of the session.
    """
    info = _resolve_session_id(session_id)
    if info is None:
        raise ValueError(f"Session not found: {session_id!r}")

    transcript = prepare_session_transcript(info.path)
    return {
        "session_id": session_id,
        "project": info.project,
        "timestamp": info.timestamp,
        "format": info.format,
        "path": info.path,
        "transcript": transcript,
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()

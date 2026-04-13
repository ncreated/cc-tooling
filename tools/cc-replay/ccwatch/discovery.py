"""Session discovery for Claude Code and Codex sessions."""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SessionInfo:
    path: str
    format: str  # "claude" | "codex"
    timestamp: str  # ISO timestamp
    project: str  # short project name
    slug: str = ""  # human-readable slug (Claude only)
    first_prompt: str = ""  # first ~200 chars of first user message
    git_branch: str = ""


def _project_name_from_cwd(cwd: str) -> str:
    """Extract short project name from a working directory path.

    e.g. '/Users/maciek/Projects/cc-tooling' -> 'cc-tooling'
         '/Users/maciek/Projects/rum-ai-toolkit/tools/cr-eval' -> 'rum-ai-toolkit'
    """
    if not cwd:
        return "unknown"
    parts = Path(cwd).parts
    # Look for a segment after a well-known parent like "Projects"
    for i, part in enumerate(parts):
        if part.lower() in ("projects", "repos", "src", "code", "work", "dev"):
            if i + 1 < len(parts):
                return parts[i + 1]
    # Fallback: last directory component
    return Path(cwd).name


def _project_name_from_codex(payload: dict) -> str:
    """Extract project name from Codex session_meta payload."""
    git = payload.get("git", {})
    repo_url = git.get("repository_url", "") if isinstance(git, dict) else ""
    if repo_url:
        # git@github.com:Org/repo.git -> repo
        name = repo_url.rstrip("/").rsplit("/", 1)[-1]
        if name.endswith(".git"):
            name = name[:-4]
        return name
    cwd = payload.get("cwd", "")
    if cwd:
        return Path(cwd).name
    return "unknown"


def _read_first_lines(path: str, max_lines: int = 30) -> list[dict]:
    """Read and parse the first N lines of a JSONL file."""
    entries = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    entries.append(json.loads(stripped))
                except json.JSONDecodeError:
                    continue
    except OSError:
        pass
    return entries


def _extract_claude_metadata(entries: list[dict]) -> dict:
    """Extract metadata from Claude session entries.

    Returns dict with keys: first_prompt, slug, git_branch, cwd.
    """
    result = {"first_prompt": "", "slug": "", "git_branch": "", "cwd": ""}

    # Get cwd and git_branch from any early entry that has them
    for entry in entries:
        if not result["cwd"] and entry.get("cwd"):
            result["cwd"] = entry["cwd"]
        if not result["git_branch"] and entry.get("gitBranch"):
            result["git_branch"] = entry["gitBranch"]
        if result["cwd"] and result["git_branch"]:
            break

    # Find first real user prompt
    for entry in entries:
        if entry.get("type") != "user":
            continue
        if entry.get("isMeta") or entry.get("isSidechain"):
            continue
        msg = entry.get("message", {})
        content = msg.get("content", "") if isinstance(msg, dict) else ""
        text = ""
        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text = block["text"]
                    break
        # Skip slash command invocations
        if "<command-name>" in text:
            continue
        if entry.get("slug"):
            result["slug"] = entry["slug"]
        text = text.strip()
        result["first_prompt"] = text[:200]
        break

    return result


# ---------------------------------------------------------------------------
# Path collection
# ---------------------------------------------------------------------------

def _collect_searchable_paths(limit: int) -> list[tuple[float, Path, str]]:
    """Collect session JSONL paths with mtime and format, sorted by recency.

    Returns list of (mtime, path, format) tuples, capped at *limit*.
    """
    candidates: list[tuple[float, Path, str]] = []

    # Claude sessions
    claude_dir = Path.home() / ".claude" / "projects"
    if claude_dir.is_dir():
        for project_dir in claude_dir.iterdir():
            if not project_dir.is_dir():
                continue
            for jsonl_file in project_dir.glob("*.jsonl"):
                if not jsonl_file.is_file():
                    continue
                try:
                    candidates.append((jsonl_file.stat().st_mtime, jsonl_file, "claude"))
                except OSError:
                    continue

    # Codex sessions
    codex_dir = Path.home() / ".codex" / "sessions"
    if codex_dir.is_dir():
        for jsonl_file in codex_dir.rglob("rollout-*.jsonl"):
            try:
                candidates.append((jsonl_file.stat().st_mtime, jsonl_file, "codex"))
            except OSError:
                continue

    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[:limit]


# ---------------------------------------------------------------------------
# Per-file metadata builders
# ---------------------------------------------------------------------------

def _build_claude_session_info(jsonl_file: Path) -> SessionInfo | None:
    """Read metadata from a Claude session file and return SessionInfo."""
    entries = _read_first_lines(str(jsonl_file))
    if not entries:
        return None

    timestamp = ""
    for entry in entries:
        ts = entry.get("timestamp", "")
        if ts:
            timestamp = ts
            break

    if not timestamp:
        return None

    meta = _extract_claude_metadata(entries)

    return SessionInfo(
        path=str(jsonl_file),
        format="claude",
        timestamp=timestamp,
        project=_project_name_from_cwd(meta["cwd"]),
        slug=meta["slug"],
        first_prompt=meta["first_prompt"],
        git_branch=meta["git_branch"],
    )


def _build_codex_session_info(jsonl_file: Path) -> SessionInfo | None:
    """Read metadata from a Codex session file and return SessionInfo."""
    entries = _read_first_lines(str(jsonl_file), max_lines=15)
    if not entries:
        return None

    meta = entries[0]
    if meta.get("type") != "session_meta":
        return None

    payload = meta.get("payload", {})

    # Skip subagent sessions
    source = payload.get("source", "")
    if isinstance(source, dict) and "subagent" in source:
        return None

    timestamp = payload.get("timestamp", meta.get("timestamp", ""))
    project_name = _project_name_from_codex(payload)

    first_prompt = ""
    for entry in entries[1:]:
        if entry.get("type") != "response_item":
            continue
        p = entry.get("payload", {})
        if p.get("role") != "user":
            continue
        for block in p.get("content", []):
            if block.get("type") == "input_text":
                text = block.get("text", "").strip()
                if text.startswith("<") or text.startswith("#"):
                    continue
                first_prompt = text[:200]
                break
        if first_prompt:
            break

    return SessionInfo(
        path=str(jsonl_file),
        format="codex",
        timestamp=timestamp,
        project=project_name,
        first_prompt=first_prompt,
    )


# ---------------------------------------------------------------------------
# Discovery (listing)
# ---------------------------------------------------------------------------

def discover_claude_sessions(limit: int = 100) -> list[SessionInfo]:
    """Discover Claude Code sessions from ~/.claude/projects/."""
    candidates = [
        (mtime, path)
        for mtime, path, fmt in _collect_searchable_paths(limit * 2)
        if fmt == "claude"
    ][:limit]

    sessions: list[SessionInfo] = []
    for _mtime, jsonl_file in candidates:
        info = _build_claude_session_info(jsonl_file)
        if info:
            sessions.append(info)

    return sessions


def discover_codex_sessions(limit: int = 100) -> list[SessionInfo]:
    """Discover Codex sessions from ~/.codex/sessions/."""
    candidates = [
        (mtime, path)
        for mtime, path, fmt in _collect_searchable_paths(limit * 2)
        if fmt == "codex"
    ][:limit]

    sessions: list[SessionInfo] = []
    for _mtime, jsonl_file in candidates:
        info = _build_codex_session_info(jsonl_file)
        if info:
            sessions.append(info)

    return sessions


def discover_sessions(limit: int = 100) -> list[SessionInfo]:
    """Discover and merge sessions from all sources, sorted by timestamp."""
    claude = discover_claude_sessions(limit)
    codex = discover_codex_sessions(limit)

    combined = claude + codex
    combined.sort(key=lambda s: s.timestamp, reverse=True)
    return combined[:limit]


# ---------------------------------------------------------------------------
# Full-text search
# ---------------------------------------------------------------------------

def _grep_files(paths: list[str], query: str) -> set[str]:
    """Use grep to find which files contain *query* (case-insensitive, literal)."""
    if not paths:
        return set()
    try:
        result = subprocess.run(
            ["grep", "-ilF", "--", query] + paths,
            capture_output=True,
            text=True,
            timeout=30,
        )
        # exit 0 = matches found, 1 = no matches, 2 = error
        if result.returncode <= 1:
            return set(result.stdout.strip().splitlines())
    except (subprocess.TimeoutExpired, OSError):
        pass
    return set()


def search_sessions(query: str, limit: int = 100) -> list[SessionInfo]:
    """Search session file contents and return matching SessionInfo entries."""
    candidates = _collect_searchable_paths(limit * 3)
    all_paths = [str(path) for _mtime, path, _fmt in candidates]

    matched_paths = _grep_files(all_paths, query)
    if not matched_paths:
        return []

    # Build a format lookup from candidates
    fmt_by_path = {str(path): fmt for _mtime, path, fmt in candidates}

    sessions: list[SessionInfo] = []
    for _mtime, path, fmt in candidates:
        if len(sessions) >= limit:
            break
        spath = str(path)
        if spath not in matched_paths:
            continue
        if fmt == "claude":
            info = _build_claude_session_info(path)
        else:
            info = _build_codex_session_info(path)
        if info:
            sessions.append(info)

    sessions.sort(key=lambda s: s.timestamp, reverse=True)
    return sessions

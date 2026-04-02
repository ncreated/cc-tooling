"""Session discovery for Claude Code and Codex sessions."""

from __future__ import annotations

import json
import os
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


def discover_claude_sessions(limit: int = 100) -> list[SessionInfo]:
    """Discover Claude Code sessions from ~/.claude/projects/."""
    projects_dir = Path.home() / ".claude" / "projects"
    if not projects_dir.is_dir():
        return []

    # Collect all .jsonl files with their mtimes
    candidates: list[tuple[float, Path]] = []
    for project_dir in projects_dir.iterdir():
        if not project_dir.is_dir():
            continue
        for jsonl_file in project_dir.glob("*.jsonl"):
            if not jsonl_file.is_file():
                continue
            try:
                mtime = jsonl_file.stat().st_mtime
            except OSError:
                continue
            candidates.append((mtime, jsonl_file))

    # Sort by mtime descending, take top N
    candidates.sort(key=lambda x: x[0], reverse=True)
    candidates = candidates[:limit]

    sessions: list[SessionInfo] = []
    for _mtime, jsonl_file in candidates:
        entries = _read_first_lines(str(jsonl_file))
        if not entries:
            continue

        # Find timestamp from first entry that has one
        timestamp = ""
        for entry in entries:
            ts = entry.get("timestamp", "")
            if ts:
                timestamp = ts
                break

        if not timestamp:
            continue

        meta = _extract_claude_metadata(entries)

        sessions.append(SessionInfo(
            path=str(jsonl_file),
            format="claude",
            timestamp=timestamp,
            project=_project_name_from_cwd(meta["cwd"]),
            slug=meta["slug"],
            first_prompt=meta["first_prompt"],
            git_branch=meta["git_branch"],
        ))

    return sessions


def discover_codex_sessions(limit: int = 100) -> list[SessionInfo]:
    """Discover Codex sessions from ~/.codex/sessions/."""
    sessions_dir = Path.home() / ".codex" / "sessions"
    if not sessions_dir.is_dir():
        return []

    # Collect rollout files — filenames contain timestamps, so sort lexicographically
    candidates: list[Path] = sorted(
        sessions_dir.rglob("rollout-*.jsonl"),
        key=lambda p: p.name,
        reverse=True,
    )[:limit * 2]  # over-fetch to account for subagent files we'll skip

    sessions: list[SessionInfo] = []
    for jsonl_file in candidates:
        if len(sessions) >= limit:
            break

        entries = _read_first_lines(str(jsonl_file), max_lines=15)
        if not entries:
            continue

        # First entry should be session_meta
        meta = entries[0]
        if meta.get("type") != "session_meta":
            continue

        payload = meta.get("payload", {})

        # Skip subagent sessions
        source = payload.get("source", "")
        if isinstance(source, dict) and "subagent" in source:
            continue

        timestamp = payload.get("timestamp", meta.get("timestamp", ""))
        project_name = _project_name_from_codex(payload)

        # Find first user prompt
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
                    # Skip system/instruction messages
                    if text.startswith("<") or text.startswith("#"):
                        continue
                    first_prompt = text[:200]
                    break
            if first_prompt:
                break

        sessions.append(SessionInfo(
            path=str(jsonl_file),
            format="codex",
            timestamp=timestamp,
            project=project_name,
            first_prompt=first_prompt,
        ))

    return sessions


def discover_sessions(limit: int = 100) -> list[SessionInfo]:
    """Discover and merge sessions from all sources, sorted by timestamp."""
    claude = discover_claude_sessions(limit)
    codex = discover_codex_sessions(limit)

    combined = claude + codex
    combined.sort(key=lambda s: s.timestamp, reverse=True)
    return combined[:limit]

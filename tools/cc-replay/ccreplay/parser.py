"""JSONL session parser for Claude Code sessions."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class BlockType(str, Enum):
    TEXT = "text"
    THINKING = "thinking"
    TOOL_USE = "tool_use"
    TOOL_RESULT = "tool_result"
    IMAGE = "image"


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class StopReason(str, Enum):
    END_TURN = "end_turn"
    TOOL_USE = "tool_use"
    MAX_TOKENS = "max_tokens"
    STOP_SEQUENCE = "stop_sequence"


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class ContentBlock:
    type: BlockType
    text: str = ""
    tool_name: str = ""
    tool_input: str = ""
    tool_use_id: str = ""
    is_error: bool = False


@dataclass
class ParseError:
    """Represents a malformed JSONL line that couldn't be parsed."""
    line_number: int
    raw_line: str
    error: str


@dataclass
class Message:
    role: Role
    timestamp: str
    is_meta: bool
    content_blocks: list[ContentBlock] = field(default_factory=list)
    model: str = ""
    stop_reason: Optional[StopReason] = None
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass
class SubagentSession:
    agent_id: str
    description: str
    agent_type: str
    tool_use_id: str
    messages: list[Message] = field(default_factory=list)


@dataclass
class Session:
    session_id: str
    file_path: str
    messages: list[Message] = field(default_factory=list)
    parse_errors: list[ParseError] = field(default_factory=list)
    subagents: dict[str, SubagentSession] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Regex for stripping noise from user content
# ---------------------------------------------------------------------------

_SYSTEM_REMINDER_RE = re.compile(
    r"<system-reminder>.*?</system-reminder>", re.DOTALL
)
_LOCAL_CMD_CAVEAT_RE = re.compile(
    r"<local-command-caveat>.*?</local-command-caveat>", re.DOTALL
)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _read_jsonl(path: str) -> tuple[list[dict], list[ParseError]]:
    """Read a JSONL file, returning parsed entries and any parse errors."""
    entries: list[dict] = []
    errors: list[ParseError] = []
    with open(path, "r", encoding="utf-8") as f:
        for line_number, raw_line in enumerate(f, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                entries.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                errors.append(ParseError(
                    line_number=line_number,
                    raw_line=stripped[:200],
                    error=str(exc),
                ))
    return entries, errors


def _filter_entries(entries: list[dict]) -> list[dict]:
    """Keep only user/assistant entries, drop synthetic and sidechain."""
    result = []
    for entry in entries:
        entry_type = entry.get("type")
        if entry_type not in ("user", "assistant"):
            continue
        # Drop synthetic assistant messages
        msg = entry.get("message", {})
        if msg.get("model") == "<synthetic>":
            continue
        # Drop sidechain (subagent) messages — handled separately
        if entry.get("isSidechain"):
            continue
        result.append(entry)
    return result


def _deduplicate(entries: list[dict]) -> list[dict]:
    """Deduplicate streaming assistant entries by requestId (keep last)."""
    # Track last index for each requestId
    last_index: dict[str, int] = {}
    for i, entry in enumerate(entries):
        request_id = entry.get("requestId")
        if request_id:
            last_index[request_id] = i

    result = []
    for i, entry in enumerate(entries):
        request_id = entry.get("requestId")
        if request_id is None or last_index.get(request_id) == i:
            result.append(entry)
    return result


def _strip_noise(text: str) -> str:
    """Strip system-reminder and caveat tags from user text content."""
    text = _SYSTEM_REMINDER_RE.sub("", text)
    text = _LOCAL_CMD_CAVEAT_RE.sub("", text)
    return text.strip()


def _format_tool_input(data: dict) -> str:
    """Format tool input dict with multiline string values expanded.

    Instead of showing escaped \\n inside JSON strings, render them
    as real newlines in an indented block beneath the key.
    """
    lines: list[str] = []
    for key, value in data.items():
        if isinstance(value, str) and "\n" in value:
            lines.append(f"{key}:")
            for vline in value.splitlines():
                lines.append(f"  {vline}")
        elif isinstance(value, str):
            lines.append(f"{key}: {value}")
        else:
            try:
                dumped = json.dumps(value, indent=2, ensure_ascii=False)
            except (TypeError, ValueError):
                dumped = str(value)
            if "\n" in dumped:
                lines.append(f"{key}:")
                for vline in dumped.splitlines():
                    lines.append(f"  {vline}")
            else:
                lines.append(f"{key}: {dumped}")
    return "\n".join(lines)


def _parse_content_blocks(content, is_user: bool = False) -> list[ContentBlock]:
    """Parse raw content into ContentBlock list."""
    if isinstance(content, str):
        text = _strip_noise(content) if is_user else content
        if text:
            return [ContentBlock(type=BlockType.TEXT, text=text)]
        return []

    if not isinstance(content, list):
        return []

    blocks = []
    for raw in content:
        block_type = raw.get("type", "")

        if block_type == "text":
            text = raw.get("text", "")
            if is_user:
                text = _strip_noise(text)
            if text:
                blocks.append(ContentBlock(type=BlockType.TEXT, text=text))

        elif block_type == "thinking":
            thinking_text = raw.get("thinking", "")
            if thinking_text:
                blocks.append(ContentBlock(
                    type=BlockType.THINKING, text=thinking_text
                ))

        elif block_type == "tool_use":
            tool_input = raw.get("input", {})
            try:
                input_str = _format_tool_input(tool_input)
            except (TypeError, ValueError):
                input_str = str(tool_input)
            blocks.append(ContentBlock(
                type=BlockType.TOOL_USE,
                tool_name=raw.get("name", "?"),
                tool_input=input_str,
                tool_use_id=raw.get("id", ""),
            ))

        elif block_type == "tool_result":
            result_content = raw.get("content", "")
            if isinstance(result_content, list):
                # Flatten nested content blocks to text
                parts = []
                for sub in result_content:
                    if isinstance(sub, dict) and sub.get("type") == "text":
                        parts.append(sub.get("text", ""))
                result_content = "\n".join(parts)
            blocks.append(ContentBlock(
                type=BlockType.TOOL_RESULT,
                text=str(result_content),
                tool_use_id=raw.get("tool_use_id", ""),
                is_error=bool(raw.get("is_error")),
            ))

        elif block_type == "image":
            blocks.append(ContentBlock(type=BlockType.IMAGE))

    return blocks


def _to_message(entry: dict) -> Message:
    """Convert a raw JSONL entry dict to a Message."""
    entry_type = entry.get("type", "")
    msg = entry.get("message", {})
    role = Role(entry_type) if entry_type in ("user", "assistant") else Role.USER

    is_meta = bool(entry.get("isMeta"))
    is_user = role == Role.USER

    content_blocks = _parse_content_blocks(
        msg.get("content", ""), is_user=is_user
    )

    # Parse stop_reason
    stop_reason = None
    raw_stop = msg.get("stop_reason")
    if raw_stop:
        try:
            stop_reason = StopReason(raw_stop)
        except ValueError:
            pass

    # Token usage
    usage = msg.get("usage", {})

    return Message(
        role=role,
        timestamp=entry.get("timestamp", ""),
        is_meta=is_meta,
        content_blocks=content_blocks,
        model=msg.get("model", ""),
        stop_reason=stop_reason,
        input_tokens=usage.get("input_tokens", 0),
        output_tokens=usage.get("output_tokens", 0),
    )


def _discover_subagents(
    session_path: Path, session_id: str
) -> dict[str, SubagentSession]:
    """Discover subagent JSONL files for the given session."""
    session_dir = session_path.parent / session_id
    if not session_dir.is_dir():
        return {}

    # Look in both {session_id}/ and {session_id}/subagents/
    candidate_dirs = [session_dir, session_dir / "subagents"]
    agent_files: list[Path] = []
    for d in candidate_dirs:
        if d.is_dir():
            agent_files.extend(d.glob("agent_*.jsonl"))
            agent_files.extend(d.glob("agent-*.jsonl"))
    agent_files = sorted(set(agent_files))

    subagents: dict[str, SubagentSession] = {}
    for agent_file in agent_files:
        agent_id = agent_file.stem  # e.g. "agent_abc123"
        entries, _errors = _read_jsonl(str(agent_file))
        filtered = _filter_entries_for_subagent(entries)
        deduped = _deduplicate(filtered)
        messages = [_to_message(e) for e in deduped]

        subagents[agent_id] = SubagentSession(
            agent_id=agent_id,
            description="",
            agent_type="",
            tool_use_id="",
            messages=messages,
        )

    return subagents


def _filter_entries_for_subagent(entries: list[dict]) -> list[dict]:
    """Filter entries for subagent parsing (keep user/assistant, allow sidechain)."""
    result = []
    for entry in entries:
        entry_type = entry.get("type")
        if entry_type not in ("user", "assistant"):
            continue
        msg = entry.get("message", {})
        if msg.get("model") == "<synthetic>":
            continue
        result.append(entry)
    return result


def _link_subagents(session: Session) -> None:
    """Link discovered subagents to Agent/Task tool_use blocks in main thread."""
    # Collect all Agent/Task tool calls from main thread
    agent_calls: list[tuple[str, str, str]] = []  # (tool_use_id, description, subagent_type)
    for msg in session.messages:
        if msg.role != Role.ASSISTANT:
            continue
        for block in msg.content_blocks:
            if block.type == BlockType.TOOL_USE and block.tool_name in ("Agent", "Task"):
                try:
                    input_data = json.loads(block.tool_input)
                except (json.JSONDecodeError, TypeError):
                    input_data = {}
                desc = input_data.get("description", input_data.get("prompt", ""))
                agent_type = input_data.get("subagent_type", input_data.get("type", ""))
                agent_calls.append((block.tool_use_id, desc, agent_type))

    # Match subagents to tool calls by order
    unmatched_subagents = list(session.subagents.values())
    for tool_use_id, description, agent_type in agent_calls:
        if not unmatched_subagents:
            break
        subagent = unmatched_subagents.pop(0)
        subagent.tool_use_id = tool_use_id
        subagent.description = description[:100] if description else subagent.agent_id
        subagent.agent_type = agent_type or "Agent"
        # Re-key in dict
        session.subagents[tool_use_id] = subagent


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def parse_session(path: str, include_subagents: bool = True) -> Session:
    """Parse a Claude Code session JSONL file into a Session object."""
    session_path = Path(path).resolve()
    session_id = session_path.stem

    entries, parse_errors = _read_jsonl(str(session_path))
    filtered = _filter_entries(entries)
    deduped = _deduplicate(filtered)
    messages = [_to_message(e) for e in deduped]

    subagents: dict[str, SubagentSession] = {}
    if include_subagents:
        subagents = _discover_subagents(session_path, session_id)

    session = Session(
        session_id=session_id,
        file_path=str(session_path),
        messages=messages,
        parse_errors=parse_errors,
        subagents=subagents,
    )

    if include_subagents and subagents:
        _link_subagents(session)

    return session

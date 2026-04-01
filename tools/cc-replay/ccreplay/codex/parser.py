"""JSONL session parser for Codex (OpenAI) sessions."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

from ..shared import format_tool_input, read_jsonl, strip_xml_tags


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class BlockType(str, Enum):
    TEXT = "text"
    REASONING_ENCRYPTED = "reasoning_encrypted"
    TOOL_USE = "tool_use"
    TOOL_RESULT = "tool_result"


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


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
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass
class SubagentSession:
    session_id: str
    description: str
    agent_type: str
    turn_id: str
    messages: list[Message] = field(default_factory=list)


@dataclass
class Session:
    session_id: str
    file_path: str
    model: str = ""
    messages: list[Message] = field(default_factory=list)
    parse_errors: list[ParseError] = field(default_factory=list)
    subagents: list[SubagentSession] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Noise stripping
# ---------------------------------------------------------------------------

_NOISE_TAGS = [
    "permissions instructions",
    "skills_instructions",
    "environment_context",
]


def _strip_noise(text: str) -> str:
    """Strip Codex system tags from message text."""
    return strip_xml_tags(text, _NOISE_TAGS)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _format_function_args(arguments_json: str) -> str:
    """Parse and pretty-print function_call arguments JSON string."""
    try:
        data = json.loads(arguments_json)
        if isinstance(data, dict):
            return format_tool_input(data)
        return arguments_json
    except (json.JSONDecodeError, TypeError):
        return arguments_json


def _parse_message_content(
    content_blocks: list[dict], role: str,
) -> list[ContentBlock]:
    """Parse Codex response_item/message content blocks."""
    result: list[ContentBlock] = []
    for block in content_blocks:
        block_type = block.get("type", "")
        if block_type in ("input_text", "output_text"):
            text = block.get("text", "")
            if role in ("developer", "user"):
                text = _strip_noise(text)
            if text:
                result.append(ContentBlock(type=BlockType.TEXT, text=text))
    return result


def _extract_turn_ids(entries: list[dict]) -> set[str]:
    """Extract all turn_id values from entries."""
    turn_ids: set[str] = set()
    for entry in entries:
        payload = entry.get("payload", {})
        tid = payload.get("turn_id")
        if tid:
            turn_ids.add(tid)
    return turn_ids


def _peek_session_header(
    path: str, max_lines: int = 5,
) -> tuple[Optional[str], Optional[str], set[str]]:
    """Read first few lines of a Codex JSONL to get source, session_id, and turn_ids.

    Returns (source_type, session_id, turn_ids) where source_type is
    "cli" for parent sessions or "subagent" for subagent sessions.
    """
    source_type: Optional[str] = None
    session_id: Optional[str] = None
    turn_ids: set[str] = set()

    try:
        with open(path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    entry = json.loads(stripped)
                except json.JSONDecodeError:
                    continue

                entry_type = entry.get("type")
                payload = entry.get("payload", {})

                if entry_type == "session_meta":
                    session_id = payload.get("id")
                    source = payload.get("source")
                    if isinstance(source, dict) and "subagent" in source:
                        source_type = "subagent"
                    elif source == "cli":
                        source_type = "cli"

                tid = payload.get("turn_id")
                if tid:
                    turn_ids.add(tid)
    except OSError:
        pass

    return source_type, session_id, turn_ids


def _discover_subagents(
    session_path: Path,
    parent_turn_ids: set[str],
) -> list[SubagentSession]:
    """Discover subagent sessions in the same directory by matching turn_ids.

    Only reads first 5 lines of each candidate file to check for matches.
    """
    session_dir = session_path.parent
    parent_name = session_path.name
    subagents: list[SubagentSession] = []

    for candidate in sorted(session_dir.glob("rollout-*.jsonl")):
        if candidate.name == parent_name:
            continue

        source_type, sub_id, sub_turn_ids = _peek_session_header(str(candidate))
        if source_type != "subagent":
            continue

        shared_turns = parent_turn_ids & sub_turn_ids
        if not shared_turns:
            continue

        # Full parse of the subagent file
        sub_session = _parse_entries(str(candidate))
        subagent = SubagentSession(
            session_id=sub_id or candidate.stem,
            description=f"review",
            agent_type="subagent",
            turn_id=next(iter(shared_turns)),
            messages=sub_session.messages,
        )
        subagents.append(subagent)

    return subagents


def _parse_entries(path: str) -> Session:
    """Parse a single Codex JSONL file into a Session object."""
    raw_entries, raw_errors = read_jsonl(path)
    parse_errors = [
        ParseError(line_number=ln, raw_line=rl, error=err)
        for ln, rl, err in raw_errors
    ]

    session_id = ""
    model = ""
    messages: list[Message] = []
    current_assistant_blocks: list[ContentBlock] = []
    current_assistant_ts = ""
    tool_result_blocks: list[ContentBlock] = []

    def _flush_assistant() -> None:
        nonlocal current_assistant_blocks, current_assistant_ts
        if current_assistant_blocks:
            messages.append(Message(
                role=Role.ASSISTANT,
                timestamp=current_assistant_ts,
                is_meta=False,
                content_blocks=current_assistant_blocks,
                model=model,
            ))
            current_assistant_blocks = []
            current_assistant_ts = ""

    for entry in raw_entries:
        ts = entry.get("timestamp", "")
        entry_type = entry.get("type", "")
        payload = entry.get("payload", {})
        payload_type = payload.get("type", "")

        # -- session_meta --
        if entry_type == "session_meta":
            session_id = payload.get("id", "")
            continue

        # -- turn_context --
        if entry_type == "turn_context":
            model = payload.get("model", model)
            continue

        # -- response_item --
        if entry_type == "response_item":

            # message
            if payload_type == "message":
                role = payload.get("role", "")
                content = payload.get("content", [])

                if role == "developer":
                    # Strip noise; keep if anything remains
                    blocks = _parse_message_content(content, role)
                    if blocks:
                        _flush_assistant()
                        messages.append(Message(
                            role=Role.USER,
                            timestamp=ts,
                            is_meta=True,
                            content_blocks=blocks,
                        ))

                elif role == "user":
                    _flush_assistant()
                    blocks = _parse_message_content(content, role)
                    if blocks:
                        messages.append(Message(
                            role=Role.USER,
                            timestamp=ts,
                            is_meta=False,
                            content_blocks=blocks,
                        ))

                elif role == "assistant":
                    blocks = _parse_message_content(content, role)
                    if blocks:
                        current_assistant_blocks.extend(blocks)
                        if not current_assistant_ts:
                            current_assistant_ts = ts

            # reasoning (encrypted)
            elif payload_type == "reasoning":
                current_assistant_blocks.append(
                    ContentBlock(type=BlockType.REASONING_ENCRYPTED)
                )
                if not current_assistant_ts:
                    current_assistant_ts = ts

            # function_call
            elif payload_type == "function_call":
                name = payload.get("name", "?")
                arguments = payload.get("arguments", "{}")
                call_id = payload.get("call_id", "")
                current_assistant_blocks.append(ContentBlock(
                    type=BlockType.TOOL_USE,
                    tool_name=name,
                    tool_input=_format_function_args(arguments),
                    tool_use_id=call_id,
                ))
                if not current_assistant_ts:
                    current_assistant_ts = ts

            # function_call_output
            elif payload_type == "function_call_output":
                call_id = payload.get("call_id", "")
                output = payload.get("output", "")
                tool_result_blocks.append(ContentBlock(
                    type=BlockType.TOOL_RESULT,
                    text=output,
                    tool_use_id=call_id,
                ))

        # -- event_msg --
        elif entry_type == "event_msg":

            # exec_command_end (in CLI parent sessions)
            if payload_type == "exec_command_end":
                call_id = payload.get("call_id", "")
                command = payload.get("command", [])
                cmd_str = command[-1] if command else "?"
                aggregated = payload.get("aggregated_output", "")
                exit_code = payload.get("exit_code", 0)

                current_assistant_blocks.append(ContentBlock(
                    type=BlockType.TOOL_USE,
                    tool_name="shell",
                    tool_input=cmd_str,
                    tool_use_id=call_id,
                ))
                tool_result_blocks.append(ContentBlock(
                    type=BlockType.TOOL_RESULT,
                    text=aggregated,
                    tool_use_id=call_id,
                    is_error=(exit_code != 0),
                ))
                if not current_assistant_ts:
                    current_assistant_ts = ts

    # Flush remaining assistant blocks
    _flush_assistant()

    # Create synthetic meta messages for tool results (for the renderer lookup)
    if tool_result_blocks:
        messages.append(Message(
            role=Role.USER,
            timestamp="",
            is_meta=True,
            content_blocks=tool_result_blocks,
        ))

    return Session(
        session_id=session_id,
        file_path=path,
        model=model,
        messages=messages,
        parse_errors=parse_errors,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def parse_codex_session(
    path: str, include_subagents: bool = True,
) -> Session:
    """Parse a Codex session JSONL file into a Session object."""
    session_path = Path(path).resolve()
    session = _parse_entries(str(session_path))
    session.file_path = str(session_path)

    if include_subagents:
        turn_ids = set()
        raw_entries, _ = read_jsonl(str(session_path))
        for entry in raw_entries:
            tid = entry.get("payload", {}).get("turn_id")
            if tid:
                turn_ids.add(tid)

        if turn_ids:
            session.subagents = _discover_subagents(session_path, turn_ids)

    return session

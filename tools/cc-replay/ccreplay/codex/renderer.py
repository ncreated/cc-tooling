"""HTML renderer for parsed Codex sessions."""

from __future__ import annotations

from typing import Optional

from ..shared import esc, truncate
from . import template as T
from .parser import (
    BlockType,
    ContentBlock,
    Message,
    Role,
    Session,
    SubagentSession,
)


def _build_tool_result_lookup(messages: list[Message]) -> dict[str, ContentBlock]:
    """Build a lookup from tool_use_id to its tool_result ContentBlock."""
    lookup: dict[str, ContentBlock] = {}
    for msg in messages:
        if msg.role != Role.USER or not msg.is_meta:
            continue
        for block in msg.content_blocks:
            if block.type == BlockType.TOOL_RESULT and block.tool_use_id:
                lookup[block.tool_use_id] = block
    return lookup


def _render_tool_result(block: Optional[ContentBlock]) -> str:
    """Render a tool result fragment, or empty string if not available."""
    if block is None:
        return ""
    error_class = " error" if block.is_error else ""
    content = truncate(block.text)
    return T.TOOL_RESULT_FRAGMENT.format(
        error_class=error_class,
        content=content,
    )


def _render_subagent(subagent: SubagentSession) -> str:
    """Render a subagent's conversation as nested HTML."""
    tool_lookup = _build_tool_result_lookup(subagent.messages)
    inner_html = _render_messages(subagent.messages, tool_lookup)
    return T.SUBAGENT_BLOCK.format(
        description=esc(subagent.description or subagent.session_id),
        agent_type=esc(subagent.agent_type or "subagent"),
        content=inner_html,
    )


def _render_messages(
    messages: list[Message],
    tool_lookup: dict[str, ContentBlock],
) -> str:
    """Render a list of messages to HTML."""
    parts: list[str] = []

    for msg in messages:
        # Skip meta messages — tool results rendered inline with tool calls
        if msg.role == Role.USER and msg.is_meta:
            continue

        if msg.role == Role.USER:
            text_parts = []
            for block in msg.content_blocks:
                if block.type == BlockType.TEXT and block.text:
                    text_parts.append(esc(block.text))
            if not text_parts:
                continue
            parts.append(T.USER_MESSAGE.format(
                timestamp=esc(msg.timestamp),
                content="\n".join(text_parts),
            ))

        elif msg.role == Role.ASSISTANT:
            block_html: list[str] = []
            for block in msg.content_blocks:
                if block.type == BlockType.TEXT:
                    block_html.append(T.TEXT_BLOCK.format(text=esc(block.text)))

                elif block.type == BlockType.REASONING_ENCRYPTED:
                    block_html.append(T.REASONING_ENCRYPTED_BLOCK)

                elif block.type == BlockType.TOOL_USE:
                    result_block = tool_lookup.get(block.tool_use_id)
                    result_html = _render_tool_result(result_block)
                    block_html.append(T.TOOL_USE_BLOCK.format(
                        tool_name=esc(block.tool_name),
                        tool_input=truncate(block.tool_input),
                        tool_result=result_html,
                    ))

            if block_html:
                parts.append(T.ASSISTANT_MESSAGE_START.format(
                    timestamp=esc(msg.timestamp),
                    model=esc(msg.model or "unknown"),
                ))
                parts.extend(block_html)
                parts.append(T.ASSISTANT_MESSAGE_END)

    return "\n".join(parts)


def render(session: Session) -> str:
    """Render a full Codex Session to a standalone HTML document."""
    parts: list[str] = []

    parts.append(T.HTML_HEAD.format(title=esc(session.session_id)))
    parts.append(T.SESSION_HEADER.format(
        session_id=esc(session.session_id),
        model=esc(session.model or "unknown"),
        file_path=esc(session.file_path),
    ))

    # Render parse errors at the top
    for err in session.parse_errors:
        parts.append(T.PARSE_ERROR_BLOCK.format(
            line_number=err.line_number,
            error=esc(f"{err.error}\nRaw: {err.raw_line}"),
        ))

    # Build tool result lookup
    tool_lookup = _build_tool_result_lookup(session.messages)

    # Render subagents if present (for CLI parent sessions)
    if session.subagents:
        # Render the main session messages (user prompt, final answer)
        # then inline subagent conversations
        main_html = _render_messages(session.messages, tool_lookup)
        parts.append(main_html)
        for subagent in session.subagents:
            parts.append(_render_subagent(subagent))
    else:
        parts.append(_render_messages(session.messages, tool_lookup))

    parts.append(T.HTML_FOOT)
    return "\n".join(parts)

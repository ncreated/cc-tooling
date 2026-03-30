"""HTML renderer for parsed Claude Code sessions."""

from __future__ import annotations

import html
from typing import Optional

from . import template as T
from .parser import (
    BlockType,
    ContentBlock,
    Message,
    Role,
    Session,
    SubagentSession,
)

TRUNCATE_LIMIT = 10_000


def _esc(text: str) -> str:
    """HTML-escape text."""
    return html.escape(text, quote=True)


def _truncate(text: str) -> str:
    """Truncate long text with a marker."""
    if len(text) <= TRUNCATE_LIMIT:
        return _esc(text)
    return _esc(text[:TRUNCATE_LIMIT]) + '\n<span class="truncated">[... truncated]</span>'


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
    content = _truncate(block.text)
    return T.TOOL_RESULT_FRAGMENT.format(
        error_class=error_class,
        content=content,
    )


def _render_subagent(subagent: SubagentSession) -> str:
    """Render a subagent's conversation as nested HTML."""
    tool_lookup = _build_tool_result_lookup(subagent.messages)
    inner_html = _render_messages(subagent.messages, tool_lookup, subagents={})
    return T.SUBAGENT_BLOCK.format(
        description=_esc(subagent.description or subagent.agent_id),
        agent_type=_esc(subagent.agent_type or "Agent"),
        content=inner_html,
    )


def _render_messages(
    messages: list[Message],
    tool_lookup: dict[str, ContentBlock],
    subagents: dict[str, SubagentSession],
) -> str:
    """Render a list of messages to HTML."""
    parts: list[str] = []

    for msg in messages:
        # Skip meta (tool result) messages — rendered inline with tool calls
        if msg.role == Role.USER and msg.is_meta:
            continue

        if msg.role == Role.USER:
            text_parts = []
            for block in msg.content_blocks:
                if block.type == BlockType.TEXT and block.text:
                    text_parts.append(_esc(block.text))
            if not text_parts:
                continue
            parts.append(T.USER_MESSAGE.format(
                timestamp=_esc(msg.timestamp),
                content="\n".join(text_parts),
            ))

        elif msg.role == Role.ASSISTANT:
            block_html: list[str] = []
            for block in msg.content_blocks:
                if block.type == BlockType.TEXT:
                    block_html.append(T.TEXT_BLOCK.format(text=_esc(block.text)))

                elif block.type == BlockType.THINKING:
                    block_html.append(T.THINKING_BLOCK.format(
                        text=_esc(block.text),
                    ))

                elif block.type == BlockType.TOOL_USE:
                    # Check if this is an Agent/Task call with a linked subagent
                    if block.tool_name in ("Agent", "Task") and block.tool_use_id in subagents:
                        block_html.append(_render_subagent(subagents[block.tool_use_id]))
                    else:
                        result_block = tool_lookup.get(block.tool_use_id)
                        result_html = _render_tool_result(result_block)
                        block_html.append(T.TOOL_USE_BLOCK.format(
                            tool_name=_esc(block.tool_name),
                            tool_input=_truncate(block.tool_input),
                            tool_result=result_html,
                        ))

                elif block.type == BlockType.IMAGE:
                    block_html.append(
                        '<div class="content-text" style="color: var(--text-dim);">'
                        '[image]</div>'
                    )

            if block_html:
                parts.append(T.ASSISTANT_MESSAGE_START.format(
                    timestamp=_esc(msg.timestamp),
                    model=_esc(msg.model or "unknown"),
                ))
                parts.extend(block_html)
                parts.append(T.ASSISTANT_MESSAGE_END)

    return "\n".join(parts)


def render(session: Session) -> str:
    """Render a full Session to a standalone HTML document."""
    parts: list[str] = []

    parts.append(T.HTML_HEAD.format(title=_esc(session.session_id)))
    parts.append(T.SESSION_HEADER.format(
        session_id=_esc(session.session_id),
        file_path=_esc(session.file_path),
    ))

    # Render parse errors at the top
    for err in session.parse_errors:
        parts.append(T.PARSE_ERROR_BLOCK.format(
            line_number=err.line_number,
            error=_esc(f"{err.error}\nRaw: {err.raw_line}"),
        ))

    # Build tool result lookup and render messages
    tool_lookup = _build_tool_result_lookup(session.messages)
    parts.append(_render_messages(session.messages, tool_lookup, session.subagents))

    parts.append(T.HTML_FOOT)
    return "\n".join(parts)

"""Format-agnostic utilities shared by Claude and Codex flows."""

from __future__ import annotations

import html
import json
import re


TRUNCATE_LIMIT = 10_000


def read_jsonl(path: str) -> tuple[list[dict], list[tuple[int, str, str]]]:
    """Read a JSONL file, returning parsed entries and error tuples.

    Error tuples are (line_number, raw_line_snippet, error_message).
    """
    entries: list[dict] = []
    errors: list[tuple[int, str, str]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line_number, raw_line in enumerate(f, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                entries.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                errors.append((line_number, stripped[:200], str(exc)))
    return entries, errors


def esc(text: str) -> str:
    """HTML-escape text."""
    return html.escape(text, quote=True)


def truncate(text: str, limit: int = TRUNCATE_LIMIT) -> str:
    """Truncate long text with a marker (HTML-escaped)."""
    if len(text) <= limit:
        return esc(text)
    return esc(text[:limit]) + '\n<span class="truncated">[... truncated]</span>'


def format_tool_input(data: dict) -> str:
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


def strip_xml_tags(text: str, tag_names: list[str]) -> str:
    """Strip specified XML tags and their content from text."""
    for tag in tag_names:
        pattern = re.compile(
            rf"<{re.escape(tag)}>.*?</{re.escape(tag)}>", re.DOTALL
        )
        text = pattern.sub("", text)
    return text.strip()

"""HTML/CSS template constants for Claude Code session replay."""

HTML_HEAD = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>cc-replay: {title}</title>
<style>
:root {{
    --bg: #0d1117;
    --surface: #161b22;
    --user-bg: #1a3a5c;
    --assistant-bg: #1c1c2e;
    --text: #e0e0e0;
    --text-dim: #7d8590;
    --accent: #58a6ff;
    --error: #f85149;
    --warning: #d29922;
    --border: #30363d;
    --tool-bg: #0d1117;
    --thinking-bg: #1a1a2e;
    --subagent-bg: #1a2332;
    --font: 'SF Mono', 'Cascadia Code', 'Fira Code', 'JetBrains Mono', Consolas, monospace;
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    background: var(--bg);
    color: var(--text);
    font-family: var(--font);
    font-size: 13px;
    line-height: 1.5;
    max-width: 960px;
    margin: 0 auto;
    padding: 20px;
}}

.session-header {{
    border-bottom: 1px solid var(--border);
    padding-bottom: 16px;
    margin-bottom: 24px;
}}

.session-header h1 {{
    font-size: 16px;
    color: var(--accent);
    font-weight: 600;
}}

.session-header .meta {{
    color: var(--text-dim);
    font-size: 12px;
    margin-top: 4px;
}}

.message {{
    margin-bottom: 16px;
    border-radius: 8px;
    padding: 12px 16px;
    border: 1px solid var(--border);
}}

.message .role-label {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}}

.message .timestamp {{
    font-size: 11px;
    color: var(--text-dim);
    float: right;
}}

.user-msg {{
    background: var(--user-bg);
    border-color: #1f4a73;
}}

.user-msg .role-label {{
    color: #79c0ff;
}}

.assistant-msg {{
    background: var(--assistant-bg);
    border-color: #2d2d44;
}}

.assistant-msg .role-label {{
    color: #d2a8ff;
}}

.content-text {{
    white-space: pre-wrap;
    word-wrap: break-word;
    font-size: 13px;
}}

details {{
    margin: 8px 0;
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
}}

details > summary {{
    cursor: pointer;
    padding: 8px 12px;
    font-size: 12px;
    font-weight: 600;
    user-select: none;
    list-style: none;
}}

details > summary::-webkit-details-marker {{ display: none; }}

details > summary::before {{
    content: '▶ ';
    font-size: 10px;
    color: var(--text-dim);
}}

details[open] > summary::before {{
    content: '▼ ';
}}

details > .detail-body {{
    padding: 8px 12px;
    border-top: 1px solid var(--border);
    max-height: 600px;
    overflow: auto;
}}

.thinking {{
    background: var(--thinking-bg);
}}

.thinking > summary {{
    color: var(--text-dim);
    font-style: italic;
}}

.tool-call {{
    background: var(--tool-bg);
}}

.tool-call > summary {{
    color: var(--accent);
}}

.tool-call .tool-input {{
    color: var(--text-dim);
    font-size: 12px;
    margin-bottom: 8px;
}}

.tool-call .tool-input pre {{
    white-space: pre-wrap;
    word-wrap: break-word;
}}

.tool-call .tool-result {{
    border-top: 1px dashed var(--border);
    padding-top: 8px;
}}

.tool-call .tool-result pre {{
    white-space: pre-wrap;
    word-wrap: break-word;
    font-size: 12px;
}}

.tool-call .tool-result.error {{
    color: var(--error);
}}

.subagent {{
    background: var(--subagent-bg);
    border-color: #1f3a52;
}}

.subagent > summary {{
    color: #3fb950;
}}

.subagent .subagent-body {{
    padding: 4px 8px;
}}

.subagent .message {{
    margin-bottom: 8px;
    font-size: 12px;
}}

.parse-error {{
    background: #2d1b00;
    border: 1px solid var(--warning);
    border-radius: 6px;
    padding: 8px 12px;
    margin-bottom: 12px;
    font-size: 12px;
}}

.parse-error .error-label {{
    color: var(--warning);
    font-weight: 700;
    font-size: 11px;
    text-transform: uppercase;
}}

.parse-error .error-detail {{
    color: var(--text-dim);
    margin-top: 4px;
    white-space: pre-wrap;
    word-wrap: break-word;
}}

.truncated {{
    color: var(--warning);
    font-style: italic;
    font-size: 12px;
}}

.toolbar {{
    position: sticky;
    top: 0;
    z-index: 100;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 8px 12px;
    margin: -20px -20px 20px -20px;
    padding-left: 20px;
    display: flex;
    gap: 8px;
    align-items: center;
}}

.toolbar button {{
    background: var(--bg);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 4px 12px;
    font-family: var(--font);
    font-size: 12px;
    cursor: pointer;
}}

.toolbar button:hover {{
    background: var(--border);
}}
</style>
</head>
<body>
<div class="toolbar">
<button onclick="expandAll()">Expand All</button>
<button onclick="collapseAll()">Collapse All</button>
</div>
<script>
function expandAll() {{ document.querySelectorAll('details').forEach(d => d.open = true); }}
function collapseAll() {{ document.querySelectorAll('details').forEach(d => d.open = false); }}
</script>
"""

HTML_FOOT = """\
</body>
</html>
"""

SESSION_HEADER = """\
<div class="session-header">
<h1>cc-replay</h1>
<div class="meta">Session: {session_id} &mdash; {file_path}</div>
</div>
"""

USER_MESSAGE = """\
<div class="message user-msg">
<span class="timestamp">{timestamp}</span>
<div class="role-label">User</div>
<div class="content-text">{content}</div>
</div>
"""

ASSISTANT_MESSAGE_START = """\
<div class="message assistant-msg">
<span class="timestamp">{timestamp}</span>
<div class="role-label">Assistant <span style="color: var(--text-dim); font-weight: 400; text-transform: none;">({model})</span></div>
"""

ASSISTANT_MESSAGE_END = """\
</div>
"""

TEXT_BLOCK = """\
<div class="content-text">{text}</div>
"""

THINKING_BLOCK = """\
<details class="thinking">
<summary>Thinking</summary>
<div class="detail-body"><pre>{text}</pre></div>
</details>
"""

TOOL_USE_BLOCK = """\
<details class="tool-call">
<summary>Tool: {tool_name}</summary>
<div class="detail-body">
<div class="tool-input"><pre>{tool_input}</pre></div>
{tool_result}
</div>
</details>
"""

TOOL_RESULT_FRAGMENT = """\
<div class="tool-result{error_class}"><pre>{content}</pre></div>
"""

SUBAGENT_BLOCK = """\
<details class="subagent">
<summary>Subagent: {description} ({agent_type})</summary>
<div class="detail-body subagent-body">
{content}
</div>
</details>
"""

PARSE_ERROR_BLOCK = """\
<div class="parse-error">
<div class="error-label">⚠ Parse error — line {line_number}</div>
<div class="error-detail">{error}</div>
</div>
"""

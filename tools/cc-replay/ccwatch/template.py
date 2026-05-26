"""HTML/CSS/JS template for the ccwatch SPA shell."""

SHELL_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ccwatch</title>
<style>
:root {{
    --bg: #0d1117;
    --surface: #161b22;
    --text: #e0e0e0;
    --text-dim: #7d8590;
    --accent: #58a6ff;
    --border: #30363d;
    --claude-badge: #58a6ff;
    --codex-badge: #3fb950;
    --hover: #1c2128;
    --active: #1a3a5c;
    --error: #f85149;
    --font: 'SF Mono', 'Cascadia Code', 'Fira Code', 'JetBrains Mono', Consolas, monospace;
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

html, body {{ height: 100%; overflow: hidden; }}

body {{
    background: var(--bg);
    color: var(--text);
    font-family: var(--font);
    font-size: 13px;
    line-height: 1.5;
    display: flex;
    flex-direction: column;
}}

.shell {{
    display: flex;
    flex: 1;
    overflow: hidden;
}}

/* --- Sidebar --- */
.sidebar {{
    width: 340px;
    min-width: 280px;
    max-width: 800px;
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    background: var(--surface);
    position: relative;
    flex-shrink: 0;
}}

.sidebar-resizer {{
    position: absolute;
    top: 0;
    right: -3px;
    width: 6px;
    height: 100%;
    cursor: ew-resize;
    z-index: 10;
    background: transparent;
    transition: background 0.15s ease;
}}

.sidebar-resizer:hover,
.sidebar-resizer.dragging {{
    background: var(--accent);
    opacity: 0.5;
}}

body.resizing {{
    user-select: none;
    cursor: ew-resize;
}}

body.resizing iframe {{
    pointer-events: none;
}}

.sidebar-header {{
    padding: 16px;
    border-bottom: 1px solid var(--border);
    flex-shrink: 0;
}}

.sidebar-header h1 {{
    font-size: 15px;
    color: var(--accent);
    font-weight: 600;
    margin-bottom: 12px;
}}

.filter-row {{
    display: flex;
    gap: 8px;
    align-items: center;
}}

.filter-input {{
    flex: 1;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--text);
    font-family: var(--font);
    font-size: 12px;
    padding: 6px 10px;
    outline: none;
}}

.filter-input:focus {{
    border-color: var(--accent);
}}

.filter-input::placeholder {{
    color: var(--text-dim);
}}

.search-btn {{
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--text-dim);
    font-family: var(--font);
    font-size: 12px;
    padding: 6px 12px;
    cursor: pointer;
    white-space: nowrap;
    flex-shrink: 0;
}}

.search-btn:hover {{
    color: var(--text);
    border-color: var(--text-dim);
}}

.search-btn:active {{
    background: var(--active);
    border-color: var(--accent);
}}

.clear-btn {{
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--text-dim);
    font-family: var(--font);
    font-size: 13px;
    font-weight: 600;
    padding: 6px 8px;
    cursor: pointer;
    flex-shrink: 0;
    opacity: 0.3;
    pointer-events: none;
}}

.clear-btn.enabled {{
    opacity: 1;
    pointer-events: auto;
    color: var(--error);
    border-color: #f8514966;
}}

.clear-btn.enabled:hover {{
    background: #f8514922;
    border-color: var(--error);
}}

.type-filters {{
    display: flex;
    gap: 4px;
    margin-top: 8px;
}}

.type-btn {{
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--text-dim);
    font-family: var(--font);
    font-size: 11px;
    padding: 3px 8px;
    cursor: pointer;
}}

.type-btn:hover {{
    color: var(--text);
    border-color: var(--text-dim);
}}

.type-btn.active {{
    color: var(--text);
    border-color: var(--accent);
    background: var(--active);
}}

.filter-separator {{
    width: 1px;
    background: var(--border);
    align-self: stretch;
    margin: 1px 2px;
}}

.view-btn {{
    background: var(--bg);
    border: 1px dashed var(--border);
    border-radius: 4px;
    color: var(--text-dim);
    font-family: var(--font);
    font-size: 11px;
    padding: 3px 8px;
    cursor: pointer;
}}

.view-btn:hover {{
    color: var(--text);
    border-color: var(--text-dim);
}}

.view-btn.active {{
    color: var(--codex-badge);
    border-color: var(--codex-badge);
    border-style: solid;
    background: rgba(63, 185, 80, 0.08);
}}

.limit-row {{
    display: flex;
    justify-content: flex-end;
    margin-top: 6px;
}}

.limit-label {{
    color: var(--text-dim);
    font-family: var(--font);
    font-size: 11px;
    display: flex;
    align-items: center;
    gap: 4px;
}}

.limit-select {{
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--text-dim);
    font-family: var(--font);
    font-size: 11px;
    padding: 3px 6px;
    cursor: pointer;
}}

.limit-select:hover {{
    color: var(--text);
    border-color: var(--text-dim);
}}

/* --- Session list --- */
.session-list {{
    flex: 1;
    overflow-y: auto;
    padding: 8px;
}}

.session-card {{
    display: flex;
    align-items: flex-start;
    gap: 8px;
    padding: 10px 12px;
    border-radius: 6px;
    cursor: pointer;
    text-decoration: none;
    color: inherit;
    border-left: 3px solid transparent;
    margin-bottom: 2px;
}}

.session-card:hover {{
    background: var(--hover);
}}

.session-card.active {{
    background: var(--active);
    border-left-color: var(--accent);
}}

.session-card.selected {{
    border-left-color: var(--codex-badge);
}}

.session-card.active.selected {{
    border-left-color: var(--accent);
}}

.card-checkbox {{
    margin-top: 2px;
    flex-shrink: 0;
    accent-color: var(--codex-badge);
    cursor: pointer;
}}

.card-body {{
    flex: 1;
    min-width: 0;
}}

.card-header {{
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
}}

.badge {{
    font-size: 10px;
    font-weight: 600;
    padding: 1px 5px;
    border-radius: 3px;
    text-transform: uppercase;
}}

.badge-claude {{
    color: var(--claude-badge);
    border: 1px solid var(--claude-badge);
}}

.badge-codex {{
    color: var(--codex-badge);
    border: 1px solid var(--codex-badge);
}}

.card-time {{
    color: var(--text-dim);
}}

.card-branch {{
    color: var(--text-dim);
    margin-left: auto;
}}

.card-project {{
    font-size: 12px;
    color: var(--text);
    margin-top: 3px;
    font-weight: 500;
}}

.card-slug {{
    font-size: 11px;
    color: var(--text-dim);
    margin-top: 1px;
}}

.card-prompt {{
    font-size: 11px;
    color: var(--text-dim);
    margin-top: 3px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}

.empty-state {{
    color: var(--text-dim);
    text-align: center;
    padding: 40px 20px;
    font-size: 12px;
}}

/* --- Session groups --- */
.session-group {{
    margin-bottom: 8px;
}}

.group-header {{
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 10px;
    border-radius: 4px;
    cursor: pointer;
    user-select: none;
    color: var(--text-dim);
    font-size: 11px;
}}

.group-header:hover {{
    background: var(--hover);
    color: var(--text);
}}

.group-chevron {{
    display: inline-block;
    width: 10px;
    text-align: center;
    font-size: 9px;
    transition: transform 0.15s ease;
}}

.session-group.collapsed .group-chevron {{
    transform: rotate(-90deg);
}}

.group-checkbox {{
    flex-shrink: 0;
    accent-color: var(--codex-badge);
    cursor: pointer;
    margin: 0;
}}

.group-name {{
    color: var(--text);
    font-weight: 600;
    font-size: 12px;
    cursor: pointer;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}

.group-name:hover {{
    color: var(--accent);
    text-decoration: underline;
}}

.group-count {{
    color: var(--text-dim);
    font-size: 11px;
    margin-left: auto;
    flex-shrink: 0;
}}

.group-body {{
    margin-top: 2px;
    padding-left: 4px;
    border-left: 1px solid var(--border);
    margin-left: 3px;
}}

.session-group.collapsed .group-body {{
    display: none;
}}

.project-filter-banner {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 10px;
    margin-bottom: 8px;
    background: var(--active);
    border: 1px solid var(--accent);
    border-radius: 4px;
    font-size: 11px;
    color: var(--text);
}}

.project-filter-banner strong {{
    color: var(--accent);
}}

.project-filter-clear {{
    margin-left: auto;
    background: none;
    border: none;
    color: var(--text-dim);
    cursor: pointer;
    font-family: var(--font);
    font-size: 14px;
    line-height: 1;
    padding: 0 4px;
}}

.project-filter-clear:hover {{
    color: var(--error);
}}

/* --- Content area --- */
.content {{
    flex: 1;
    display: flex;
    flex-direction: row;
    overflow: hidden;
}}

.content-main {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}}

.content-main iframe {{
    width: 100%;
    height: 100%;
    border: none;
    background: var(--bg);
}}

.placeholder {{
    color: var(--text-dim);
    font-size: 14px;
}}

/* --- Analysis panel --- */
.analysis-panel {{
    width: var(--analysis-w, 420px);
    border-left: 1px solid var(--border);
    background: var(--surface);
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
    position: relative;
}}

.analysis-panel.collapsed {{
    width: 40px;
}}

.analysis-resizer {{
    position: absolute;
    top: 0;
    left: -3px;
    width: 6px;
    height: 100%;
    cursor: ew-resize;
    z-index: 10;
    background: transparent;
    transition: background 0.15s ease;
}}

.analysis-resizer:hover,
.analysis-resizer.dragging {{
    background: var(--accent);
    opacity: 0.5;
}}

.analysis-panel.collapsed .analysis-resizer {{
    display: none;
}}

.analysis-header {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 16px;
    border-bottom: 1px solid var(--border);
    flex-shrink: 0;
}}

.analysis-header h2 {{
    font-size: 13px;
    font-weight: 600;
    color: var(--accent);
    flex: 1;
}}

.analysis-toggle {{
    background: none;
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--text-dim);
    font-family: var(--font);
    font-size: 12px;
    padding: 2px 6px;
    cursor: pointer;
}}

.analysis-toggle:hover {{
    color: var(--text);
    border-color: var(--text-dim);
}}

.collapsed .analysis-header {{
    writing-mode: vertical-rl;
    text-orientation: mixed;
    padding: 16px 10px;
    border-bottom: none;
    border-left: none;
}}

.collapsed .analysis-header h2 {{
    font-size: 12px;
}}

.collapsed .analysis-toggle {{
    writing-mode: horizontal-tb;
    margin-top: 8px;
}}

.collapsed .analysis-body {{
    display: none;
}}

.analysis-body {{
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

.analysis-selected {{
    padding: 8px 16px;
    font-size: 11px;
    color: var(--text-dim);
    border-bottom: 1px solid var(--border);
    flex-shrink: 0;
}}

.analysis-selected strong {{
    color: var(--codex-badge);
}}

.analysis-output {{
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    font-size: 12px;
    white-space: pre-wrap;
    word-wrap: break-word;
}}

.analysis-output .error {{
    color: var(--error);
}}

.analysis-output .placeholder-text {{
    color: var(--text-dim);
    font-style: italic;
}}

.analysis-input-row {{
    display: flex;
    gap: 8px;
    padding: 12px 16px;
    border-top: 1px solid var(--border);
    flex-shrink: 0;
}}

.analysis-input {{
    flex: 1;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--text);
    font-family: var(--font);
    font-size: 12px;
    padding: 8px 10px;
    outline: none;
    resize: none;
    min-height: 36px;
    max-height: 100px;
}}

.analysis-input:focus {{
    border-color: var(--accent);
}}

.analysis-input::placeholder {{
    color: var(--text-dim);
}}

.analysis-input:disabled {{
    opacity: 0.4;
}}

.analysis-model {{
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--text-dim);
    font-family: var(--font);
    font-size: 11px;
    padding: 0 4px;
    cursor: pointer;
    flex-shrink: 0;
    align-self: flex-end;
    height: 36px;
}}

.analysis-model:hover {{
    color: var(--text);
    border-color: var(--text-dim);
}}

.analysis-model:disabled {{
    opacity: 0.4;
    cursor: not-allowed;
}}

.analysis-send {{
    background: var(--active);
    border: 1px solid var(--accent);
    border-radius: 6px;
    color: var(--accent);
    font-family: var(--font);
    font-size: 12px;
    padding: 8px 14px;
    cursor: pointer;
    flex-shrink: 0;
    align-self: flex-end;
}}

.analysis-send:hover {{
    background: var(--accent);
    color: var(--bg);
}}

.analysis-send:disabled {{
    opacity: 0.3;
    cursor: default;
    background: var(--bg);
    color: var(--text-dim);
    border-color: var(--border);
}}

/* --- Scrollbar --- */
.session-list::-webkit-scrollbar, .analysis-output::-webkit-scrollbar {{
    width: 6px;
}}

.session-list::-webkit-scrollbar-track, .analysis-output::-webkit-scrollbar-track {{
    background: transparent;
}}

.session-list::-webkit-scrollbar-thumb, .analysis-output::-webkit-scrollbar-thumb {{
    background: var(--border);
    border-radius: 3px;
}}

.session-list::-webkit-scrollbar-thumb:hover, .analysis-output::-webkit-scrollbar-thumb:hover {{
    background: var(--text-dim);
}}

/* --- Loading --- */
.loading {{
    color: var(--text-dim);
    text-align: center;
    padding: 40px;
}}

@keyframes spin {{
    to {{ transform: rotate(360deg); }}
}}

.spinner {{
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid var(--border);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin-bottom: 8px;
}}
</style>
</head>
<body>
<div class="shell">
    <div class="sidebar">
        <div class="sidebar-header">
            <h1>ccwatch</h1>
            <div class="filter-row">
                <input type="text" class="filter-input" placeholder="Search sessions..." id="filterInput">
                <button class="search-btn" id="searchBtn">Search</button>
                <button class="clear-btn" id="clearBtn">&times;</button>
            </div>
            <div class="type-filters">
                <button class="type-btn active" data-type="all">All</button>
                <button class="type-btn" data-type="claude">Claude</button>
                <button class="type-btn" data-type="codex">Codex</button>
                <span class="filter-separator" aria-hidden="true"></span>
                <button class="view-btn active" id="groupToggle" title="Group sessions by project">&#9638; Group</button>
            </div>
            <div class="limit-row">
                <label class="limit-label">Limit: <select class="limit-select" id="limitSelect">
                    <option value="10">10</option>
                    <option value="50">50</option>
                    <option value="100" selected>100</option>
                    <option value="200">200</option>
                    <option value="500">500</option>
                    <option value="1000">1000</option>
                    <option value="5000">5000</option>
                    <option value="10000">10000</option>
                </select></label>
            </div>
        </div>
        <div class="session-list" id="sessionList">
            <div class="loading">
                <div class="spinner"></div>
                <div>Loading sessions...</div>
            </div>
        </div>
        <div class="sidebar-resizer" id="sidebarResizer" title="Drag to resize"></div>
    </div>
    <div class="content" id="content">
        <div class="content-main" id="contentMain">
            <div class="placeholder">Select a session from the sidebar</div>
        </div>
        <div class="analysis-panel" id="analysisPanel">
            <div class="analysis-resizer" id="analysisResizer" title="Drag to resize"></div>
            <div class="analysis-header">
                <h2>Analysis</h2>
                <button class="analysis-toggle" id="analysisToggle">&laquo;</button>
            </div>
            <div class="analysis-body">
                <div class="analysis-selected" id="analysisSelected">No sessions selected</div>
                <div class="analysis-output" id="analysisOutput"><span class="placeholder-text">Select sessions and ask a question</span></div>
                <div class="analysis-input-row">
                    <select class="analysis-model" id="analysisModel" title="Model used for analysis">
                        <option value="">Default</option>
                        <option value="haiku">Haiku</option>
                        <option value="sonnet">Sonnet</option>
                        <option value="opus">Opus</option>
                    </select>
                    <textarea class="analysis-input" id="analysisInput"
                        placeholder="Ask about selected sessions..."
                        rows="1" disabled></textarea>
                    <button class="analysis-send" id="analysisSend" disabled>Send</button>
                </div>
            </div>
        </div>
    </div>
</div>
<script>
(function() {{
    var sessions = [];
    var activeType = "all";
    var activeSessionPath = null;
    var isSearching = false;
    var selectedPaths = new Set();
    var analysisAbort = null;

    var groupByProject = localStorage.getItem("ccwatch.groupByProject") !== "false";
    var collapsedGroups = new Set();
    try {{
        var stored = JSON.parse(localStorage.getItem("ccwatch.collapsedGroups") || "[]");
        if (Array.isArray(stored)) collapsedGroups = new Set(stored);
    }} catch (e) {{ /* ignore */ }}
    var projectFilter = null;

    function persistCollapsedGroups() {{
        localStorage.setItem("ccwatch.collapsedGroups", JSON.stringify(Array.from(collapsedGroups)));
    }}

    // --- Utilities ---

    function relativeTime(isoStr) {{
        var d = new Date(isoStr);
        var now = new Date();
        var diffMs = now - d;
        var diffMin = Math.floor(diffMs / 60000);
        if (diffMin < 1) return "just now";
        if (diffMin < 60) return diffMin + "m ago";
        var diffHr = Math.floor(diffMin / 60);
        if (diffHr < 24) return diffHr + "h ago";
        var diffDay = Math.floor(diffHr / 24);
        if (diffDay < 7) return diffDay + "d ago";
        return d.toLocaleDateString("en-US", {{ month: "short", day: "numeric" }});
    }}

    function escHtml(s) {{
        var d = document.createElement("div");
        d.textContent = s;
        return d.innerHTML;
    }}

    function escAttr(s) {{
        return escHtml(s).replace(/"/g, "&quot;");
    }}

    // --- Search ---

    function showLoading() {{
        document.getElementById("sessionList").innerHTML =
            '<div class="loading"><div class="spinner"></div><div>Searching...</div></div>';
    }}

    function cardHtml(s, inGroup) {{
        var isActive = s.path === activeSessionPath;
        var isSelected = selectedPaths.has(s.path);
        var badgeClass = s.format === "claude" ? "badge-claude" : "badge-codex";
        var label = s.format === "claude" ? "Claude" : "Codex";
        var cardClass = "session-card";
        if (isActive) cardClass += " active";
        if (isSelected) cardClass += " selected";

        var html = '<div class="' + cardClass + '" data-path="' + escHtml(s.encoded) + '" data-raw-path="' + escHtml(s.path) + '">';
        html += '<input type="checkbox" class="card-checkbox"' + (isSelected ? ' checked' : '') + '>';
        html += '<div class="card-body">';
        html += '<div class="card-header">';
        html += '<span class="badge ' + badgeClass + '">' + label + '</span>';
        html += '<span class="card-time" title="' + escHtml(s.timestamp) + '">' + relativeTime(s.timestamp) + '</span>';
        if (s.git_branch) {{
            html += '<span class="card-branch">' + escHtml(s.git_branch) + '</span>';
        }}
        html += '</div>';
        if (!inGroup) {{
            html += '<div class="card-project">' + escHtml(s.project) + '</div>';
        }}
        if (s.slug) {{
            html += '<div class="card-slug">' + escHtml(s.slug) + '</div>';
        }}
        if (s.first_prompt) {{
            var prompt = s.first_prompt.replace(/<[^>]+>/g, "").trim();
            if (prompt) {{
                html += '<div class="card-prompt">' + escHtml(prompt) + '</div>';
            }}
        }}
        html += '</div>';
        html += '</div>';
        return html;
    }}

    function attachCardHandlers(root) {{
        root.querySelectorAll(".session-card").forEach(function(card) {{
            var checkbox = card.querySelector(".card-checkbox");
            var rawPath = card.getAttribute("data-raw-path");
            var encoded = card.getAttribute("data-path");

            checkbox.addEventListener("click", function(e) {{
                e.stopPropagation();
                if (selectedPaths.has(rawPath)) {{
                    selectedPaths.delete(rawPath);
                    card.classList.remove("selected");
                }} else {{
                    selectedPaths.add(rawPath);
                    card.classList.add("selected");
                }}
                refreshGroupCheckbox(card.closest(".session-group"));
                updateAnalysisState();
            }});

            card.addEventListener("click", function(e) {{
                if (e.target === checkbox) return;
                openSession(encoded, rawPath);
            }});
        }});
    }}

    function refreshGroupCheckbox(groupEl) {{
        if (!groupEl) return;
        var cb = groupEl.querySelector(".group-checkbox");
        if (!cb) return;
        var paths = JSON.parse(groupEl.getAttribute("data-paths") || "[]");
        var selectedCount = 0;
        for (var i = 0; i < paths.length; i++) {{
            if (selectedPaths.has(paths[i])) selectedCount++;
        }}
        if (selectedCount === 0) {{
            cb.checked = false;
            cb.indeterminate = false;
        }} else if (selectedCount === paths.length) {{
            cb.checked = true;
            cb.indeterminate = false;
        }} else {{
            cb.checked = false;
            cb.indeterminate = true;
        }}
    }}

    function attachGroupHandlers(root) {{
        root.querySelectorAll(".session-group").forEach(function(groupEl) {{
            var header = groupEl.querySelector(".group-header");
            var checkbox = groupEl.querySelector(".group-checkbox");
            var nameEl = groupEl.querySelector(".group-name");
            var project = groupEl.getAttribute("data-project");
            var paths = JSON.parse(groupEl.getAttribute("data-paths") || "[]");

            refreshGroupCheckbox(groupEl);

            checkbox.addEventListener("click", function(e) {{
                e.stopPropagation();
                var shouldSelectAll = checkbox.checked;
                paths.forEach(function(p) {{
                    if (shouldSelectAll) selectedPaths.add(p);
                    else selectedPaths.delete(p);
                }});
                groupEl.querySelectorAll(".session-card").forEach(function(card) {{
                    var raw = card.getAttribute("data-raw-path");
                    var cb = card.querySelector(".card-checkbox");
                    var on = selectedPaths.has(raw);
                    cb.checked = on;
                    card.classList.toggle("selected", on);
                }});
                checkbox.indeterminate = false;
                updateAnalysisState();
            }});

            nameEl.addEventListener("click", function(e) {{
                e.stopPropagation();
                projectFilter = project;
                renderCards(sessions);
            }});

            header.addEventListener("click", function(e) {{
                if (e.target === checkbox || e.target === nameEl) return;
                var nowCollapsed = !groupEl.classList.contains("collapsed");
                groupEl.classList.toggle("collapsed", nowCollapsed);
                if (nowCollapsed) collapsedGroups.add(project);
                else collapsedGroups.delete(project);
                persistCollapsedGroups();
            }});
        }});
    }}

    function renderCards(data) {{
        var list = document.getElementById("sessionList");
        var filtered = data;

        if (!isSearching && activeType !== "all") {{
            filtered = filtered.filter(function(s) {{ return s.format === activeType; }});
        }}
        if (projectFilter) {{
            filtered = filtered.filter(function(s) {{ return s.project === projectFilter; }});
        }}

        if (filtered.length === 0) {{
            var emptyHtml = "";
            if (projectFilter) {{
                emptyHtml += '<div class="project-filter-banner">Project: <strong>' + escHtml(projectFilter) + '</strong>'
                    + '<button class="project-filter-clear" id="projectFilterClear" title="Clear project filter">&times;</button></div>';
            }}
            emptyHtml += '<div class="empty-state">No sessions found</div>';
            list.innerHTML = emptyHtml;
            wireProjectFilterClear(list);
            return;
        }}

        list.scrollTop = 0;
        var html = "";

        if (projectFilter) {{
            html += '<div class="project-filter-banner">Project: <strong>' + escHtml(projectFilter) + '</strong>'
                + '<button class="project-filter-clear" id="projectFilterClear" title="Clear project filter">&times;</button></div>';
        }}

        var useGroups = groupByProject && !projectFilter;

        if (!useGroups) {{
            for (var i = 0; i < filtered.length; i++) {{
                html += cardHtml(filtered[i], false);
            }}
            list.innerHTML = html;
            attachCardHandlers(list);
            wireProjectFilterClear(list);
            return;
        }}

        // Group by project, sort groups by max timestamp desc, "unknown" last.
        var groupsMap = Object.create(null);
        for (var j = 0; j < filtered.length; j++) {{
            var s = filtered[j];
            var key = s.project || "unknown";
            if (!groupsMap[key]) groupsMap[key] = [];
            groupsMap[key].push(s);
        }}

        var groupList = Object.keys(groupsMap).map(function(name) {{
            var items = groupsMap[name];
            var maxTs = items[0].timestamp;
            for (var k = 1; k < items.length; k++) {{
                if (items[k].timestamp > maxTs) maxTs = items[k].timestamp;
            }}
            return {{ name: name, items: items, maxTs: maxTs }};
        }});
        groupList.sort(function(a, b) {{
            if (a.name === "unknown" && b.name !== "unknown") return 1;
            if (b.name === "unknown" && a.name !== "unknown") return -1;
            if (a.maxTs < b.maxTs) return 1;
            if (a.maxTs > b.maxTs) return -1;
            return 0;
        }});

        for (var g = 0; g < groupList.length; g++) {{
            var group = groupList[g];
            var hasActive = activeSessionPath && group.items.some(function(it) {{ return it.path === activeSessionPath; }});
            var collapsed = !isSearching && !hasActive && collapsedGroups.has(group.name);
            var paths = group.items.map(function(it) {{ return it.path; }});
            var pathsJson = escAttr(JSON.stringify(paths));

            html += '<div class="session-group' + (collapsed ? ' collapsed' : '') + '"'
                + ' data-project="' + escAttr(group.name) + '"'
                + ' data-paths="' + pathsJson + '">';
            html += '<div class="group-header">';
            html += '<span class="group-chevron">&#9662;</span>';
            html += '<input type="checkbox" class="group-checkbox" title="Select all sessions in this project">';
            html += '<span class="group-name" title="Filter to ' + escAttr(group.name) + '">' + escHtml(group.name) + '</span>';
            html += '<span class="group-count">' + group.items.length + '</span>';
            html += '</div>';
            html += '<div class="group-body">';
            for (var m = 0; m < group.items.length; m++) {{
                html += cardHtml(group.items[m], true);
            }}
            html += '</div>';
            html += '</div>';
        }}

        list.innerHTML = html;
        attachCardHandlers(list);
        attachGroupHandlers(list);
        wireProjectFilterClear(list);
    }}

    function wireProjectFilterClear(root) {{
        var btn = root.querySelector("#projectFilterClear");
        if (!btn) return;
        btn.addEventListener("click", function() {{
            projectFilter = null;
            renderCards(sessions);
        }});
    }}

    function openSession(encoded, rawPath) {{
        activeSessionPath = rawPath;
        document.getElementById("contentMain").innerHTML =
            '<iframe src="/session/' + encoded + '"></iframe>';
        window.location.hash = encoded;
        var activeGroup = null;
        document.querySelectorAll(".session-card").forEach(function(c) {{
            var isMatch = c.getAttribute("data-raw-path") === rawPath;
            c.classList.toggle("active", isMatch);
            if (isMatch) activeGroup = c.closest(".session-group");
        }});
        if (activeGroup) {{
            activeGroup.classList.remove("collapsed");
            var project = activeGroup.getAttribute("data-project");
            if (project && collapsedGroups.has(project)) {{
                collapsedGroups.delete(project);
                persistCollapsedGroups();
            }}
        }}
    }}

    function doSearch() {{
        var query = document.getElementById("filterInput").value.trim();
        if (!query) {{
            isSearching = false;
            renderCards(sessions);
            return;
        }}
        isSearching = true;
        showLoading();
        var params = new URLSearchParams({{ q: query, type: activeType, limit: document.getElementById("limitSelect").value }});
        fetch("/api/sessions?" + params)
            .then(function(r) {{ return r.json(); }})
            .then(function(data) {{
                renderCards(data);
            }})
            .catch(function() {{
                document.getElementById("sessionList").innerHTML =
                    '<div class="empty-state">Search failed</div>';
            }});
    }}

    function updateClearBtn() {{
        var hasText = document.getElementById("filterInput").value.trim().length > 0;
        document.getElementById("clearBtn").classList.toggle("enabled", hasText);
    }}

    // --- Analysis panel ---

    function updateAnalysisState() {{
        var count = selectedPaths.size;
        var selEl = document.getElementById("analysisSelected");
        var inputEl = document.getElementById("analysisInput");
        var sendEl = document.getElementById("analysisSend");

        if (count === 0) {{
            selEl.innerHTML = "No sessions selected";
            inputEl.disabled = true;
            inputEl.placeholder = "Select sessions first...";
            sendEl.disabled = true;
        }} else {{
            selEl.innerHTML = "<strong>" + count + "</strong> session" + (count > 1 ? "s" : "") + " selected";
            inputEl.disabled = false;
            inputEl.placeholder = "Ask about selected sessions...";
            sendEl.disabled = false;
        }}
    }}

    function doAnalyze() {{
        var prompt = document.getElementById("analysisInput").value.trim();
        if (!prompt || selectedPaths.size === 0) return;

        var outputEl = document.getElementById("analysisOutput");
        var inputEl = document.getElementById("analysisInput");
        var sendEl = document.getElementById("analysisSend");

        // Cancel previous request
        if (analysisAbort) {{
            analysisAbort.abort();
        }}
        analysisAbort = new AbortController();

        // Show loading state
        outputEl.innerHTML = '<div class="loading"><div class="spinner"></div><div>Analyzing...</div></div>';
        inputEl.disabled = true;
        sendEl.disabled = true;

        fetch("/api/analyze", {{
            method: "POST",
            headers: {{ "Content-Type": "application/json" }},
            body: JSON.stringify({{
                session_paths: Array.from(selectedPaths),
                prompt: prompt,
                model: document.getElementById("analysisModel").value || null
            }}),
            signal: analysisAbort.signal
        }})
        .then(function(r) {{ return r.json(); }})
        .then(function(data) {{
            if (data.error) {{
                outputEl.innerHTML = '<span class="error">' + escHtml(data.error) + '</span>';
            }} else {{
                outputEl.textContent = data.response;
            }}
        }})
        .catch(function(err) {{
            if (err.name !== "AbortError") {{
                outputEl.innerHTML = '<span class="error">Request failed</span>';
            }}
        }})
        .finally(function() {{
            inputEl.disabled = false;
            sendEl.disabled = selectedPaths.size === 0;
            inputEl.focus();
        }});
    }}

    // --- Event listeners ---

    document.getElementById("searchBtn").addEventListener("click", doSearch);

    document.getElementById("clearBtn").addEventListener("click", function() {{
        document.getElementById("filterInput").value = "";
        updateClearBtn();
        isSearching = false;
        projectFilter = null;
        renderCards(sessions);
    }});

    (function() {{
        var btn = document.getElementById("groupToggle");
        btn.classList.toggle("active", groupByProject);
        btn.addEventListener("click", function() {{
            groupByProject = !groupByProject;
            localStorage.setItem("ccwatch.groupByProject", String(groupByProject));
            btn.classList.toggle("active", groupByProject);
            renderCards(sessions);
        }});
    }})();

    document.getElementById("filterInput").addEventListener("input", updateClearBtn);

    document.getElementById("filterInput").addEventListener("keydown", function(e) {{
        if (e.key === "Enter") doSearch();
    }});

    document.querySelectorAll(".type-btn").forEach(function(btn) {{
        btn.addEventListener("click", function() {{
            document.querySelectorAll(".type-btn").forEach(function(b) {{
                b.classList.remove("active");
            }});
            btn.classList.add("active");
            activeType = btn.getAttribute("data-type");
            if (isSearching) {{
                doSearch();
            }} else {{
                renderCards(sessions);
            }}
        }});
    }});

    // Analysis panel
    (function() {{
        var modelSelect = document.getElementById("analysisModel");
        var saved = localStorage.getItem("ccwatch.analysisModel");
        if (saved !== null) {{
            var opt = modelSelect.querySelector('option[value="' + saved.replace(/"/g, '') + '"]');
            if (opt) modelSelect.value = saved;
        }}
        modelSelect.addEventListener("change", function() {{
            localStorage.setItem("ccwatch.analysisModel", modelSelect.value);
        }});
    }})();

    document.getElementById("analysisSend").addEventListener("click", doAnalyze);

    document.getElementById("analysisInput").addEventListener("keydown", function(e) {{
        if (e.key === "Enter" && !e.shiftKey) {{
            e.preventDefault();
            doAnalyze();
        }}
    }});

    document.getElementById("analysisToggle").addEventListener("click", function() {{
        var panel = document.getElementById("analysisPanel");
        var btn = document.getElementById("analysisToggle");
        panel.classList.toggle("collapsed");
        btn.textContent = panel.classList.contains("collapsed") ? "\\u00bb" : "\\u00ab";
    }});

    document.getElementById("limitSelect").addEventListener("change", function() {{
        if (isSearching) {{
            doSearch();
        }} else {{
            loadSessions();
        }}
    }});

    // --- Panel resize ---

    function makeResizable(opts) {{
        var panel = opts.panel;
        var resizer = opts.resizer;
        var storageKey = opts.storageKey;
        var minW = opts.minW;
        var maxW = opts.maxW;
        var direction = opts.direction; // +1: dragging right grows (sidebar), -1: dragging left grows (analysis)
        var cssVar = opts.cssVar;       // if set, write width into this CSS custom property instead of style.width

        function applyWidth(w) {{
            if (cssVar) panel.style.setProperty(cssVar, w + "px");
            else panel.style.width = w + "px";
        }}

        var saved = parseInt(localStorage.getItem(storageKey) || "0", 10);
        if (saved >= minW && saved <= maxW) applyWidth(saved);

        var dragging = false, startX = 0, startW = 0;

        resizer.addEventListener("mousedown", function(e) {{
            if (panel.classList.contains("collapsed")) return;
            dragging = true;
            startX = e.clientX;
            startW = panel.getBoundingClientRect().width;
            resizer.classList.add("dragging");
            document.body.classList.add("resizing");
            e.preventDefault();
        }});

        document.addEventListener("mousemove", function(e) {{
            if (!dragging) return;
            var dx = (e.clientX - startX) * direction;
            var w = Math.min(maxW, Math.max(minW, startW + dx));
            applyWidth(w);
        }});

        document.addEventListener("mouseup", function() {{
            if (!dragging) return;
            dragging = false;
            resizer.classList.remove("dragging");
            document.body.classList.remove("resizing");
            localStorage.setItem(storageKey, String(Math.round(panel.getBoundingClientRect().width)));
        }});
    }}

    makeResizable({{
        panel: document.querySelector(".sidebar"),
        resizer: document.getElementById("sidebarResizer"),
        storageKey: "ccwatch.sidebarWidth",
        minW: 280, maxW: 800, direction: 1
    }});

    makeResizable({{
        panel: document.getElementById("analysisPanel"),
        resizer: document.getElementById("analysisResizer"),
        storageKey: "ccwatch.analysisWidth",
        minW: 300, maxW: 800, direction: -1,
        cssVar: "--analysis-w"
    }});

    function loadSessions() {{
        showLoading();
        var params = new URLSearchParams({{ limit: document.getElementById("limitSelect").value }});
        fetch("/api/sessions?" + params)
            .then(function(r) {{ return r.json(); }})
            .then(function(data) {{
                sessions = data;
                renderCards(sessions);
                if (window.location.hash) {{
                    var encoded = window.location.hash.slice(1);
                    var match = sessions.find(function(s) {{ return s.encoded === encoded; }});
                    if (match) {{
                        openSession(encoded, match.path);
                    }}
                }}
            }})
            .catch(function() {{
                document.getElementById("sessionList").innerHTML =
                    '<div class="empty-state">Failed to load sessions</div>';
            }});
    }}

    // Load sessions
    loadSessions();
}})();
</script>
</body>
</html>
"""

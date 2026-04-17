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
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    background: var(--surface);
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

.limit-label {{
    margin-left: auto;
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
    width: 420px;
    border-left: 1px solid var(--border);
    background: var(--surface);
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
}}

.analysis-panel.collapsed {{
    width: 40px;
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
    </div>
    <div class="content" id="content">
        <div class="content-main" id="contentMain">
            <div class="placeholder">Select a session from the sidebar</div>
        </div>
        <div class="analysis-panel" id="analysisPanel">
            <div class="analysis-header">
                <h2>Analysis</h2>
                <button class="analysis-toggle" id="analysisToggle">&laquo;</button>
            </div>
            <div class="analysis-body">
                <div class="analysis-selected" id="analysisSelected">No sessions selected</div>
                <div class="analysis-output" id="analysisOutput"><span class="placeholder-text">Select sessions and ask a question</span></div>
                <div class="analysis-input-row">
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

    // --- Search ---

    function showLoading() {{
        document.getElementById("sessionList").innerHTML =
            '<div class="loading"><div class="spinner"></div><div>Searching...</div></div>';
    }}

    function renderCards(data) {{
        var list = document.getElementById("sessionList");
        var filtered = data;

        if (!isSearching && activeType !== "all") {{
            filtered = data.filter(function(s) {{
                return s.format === activeType;
            }});
        }}

        if (filtered.length === 0) {{
            list.innerHTML = '<div class="empty-state">No sessions found</div>';
            return;
        }}

        list.scrollTop = 0;

        var html = "";
        for (var i = 0; i < filtered.length; i++) {{
            var s = filtered[i];
            var isActive = s.path === activeSessionPath;
            var isSelected = selectedPaths.has(s.path);
            var badgeClass = s.format === "claude" ? "badge-claude" : "badge-codex";
            var label = s.format === "claude" ? "Claude" : "Codex";
            var cardClass = "session-card";
            if (isActive) cardClass += " active";
            if (isSelected) cardClass += " selected";

            html += '<div class="' + cardClass + '" data-path="' + escHtml(s.encoded) + '" data-raw-path="' + escHtml(s.path) + '">';
            html += '<input type="checkbox" class="card-checkbox"' + (isSelected ? ' checked' : '') + '>';
            html += '<div class="card-body">';
            html += '<div class="card-header">';
            html += '<span class="badge ' + badgeClass + '">' + label + '</span>';
            html += '<span class="card-time" title="' + escHtml(s.timestamp) + '">' + relativeTime(s.timestamp) + '</span>';
            if (s.git_branch) {{
                html += '<span class="card-branch">' + escHtml(s.git_branch) + '</span>';
            }}
            html += '</div>';
            html += '<div class="card-project">' + escHtml(s.project) + '</div>';
            if (s.slug) {{
                html += '<div class="card-slug">' + escHtml(s.slug) + '</div>';
            }}
            if (s.first_prompt) {{
                var prompt = s.first_prompt;
                prompt = prompt.replace(/<[^>]+>/g, "").trim();
                if (prompt) {{
                    html += '<div class="card-prompt">' + escHtml(prompt) + '</div>';
                }}
            }}
            html += '</div>';
            html += '</div>';
        }}
        list.innerHTML = html;

        // Attach handlers
        list.querySelectorAll(".session-card").forEach(function(card) {{
            var checkbox = card.querySelector(".card-checkbox");
            var rawPath = card.getAttribute("data-raw-path");
            var encoded = card.getAttribute("data-path");

            // Checkbox: toggle selection
            checkbox.addEventListener("click", function(e) {{
                e.stopPropagation();
                if (selectedPaths.has(rawPath)) {{
                    selectedPaths.delete(rawPath);
                    card.classList.remove("selected");
                }} else {{
                    selectedPaths.add(rawPath);
                    card.classList.add("selected");
                }}
                updateAnalysisState();
            }});

            // Card click: open in iframe
            card.addEventListener("click", function(e) {{
                if (e.target === checkbox) return;
                openSession(encoded, rawPath);
            }});
        }});
    }}

    function openSession(encoded, rawPath) {{
        activeSessionPath = rawPath;
        document.getElementById("contentMain").innerHTML =
            '<iframe src="/session/' + encoded + '"></iframe>';
        window.location.hash = encoded;
        document.querySelectorAll(".session-card").forEach(function(c) {{
            c.classList.toggle("active", c.getAttribute("data-raw-path") === rawPath);
        }});
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
                prompt: prompt
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
        renderCards(sessions);
    }});

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

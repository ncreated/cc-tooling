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

/* --- Session list --- */
.session-list {{
    flex: 1;
    overflow-y: auto;
    padding: 8px;
}}

.session-card {{
    display: block;
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

/* --- Content panel --- */
.content {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.content iframe {{
    width: 100%;
    height: 100%;
    border: none;
    background: var(--bg);
}}

.placeholder {{
    color: var(--text-dim);
    font-size: 14px;
}}

/* --- Scrollbar --- */
.session-list::-webkit-scrollbar {{
    width: 6px;
}}

.session-list::-webkit-scrollbar-track {{
    background: transparent;
}}

.session-list::-webkit-scrollbar-thumb {{
    background: var(--border);
    border-radius: 3px;
}}

.session-list::-webkit-scrollbar-thumb:hover {{
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
                <input type="text" class="filter-input" placeholder="Filter sessions..." id="filterInput">
            </div>
            <div class="type-filters">
                <button class="type-btn active" data-type="all">All</button>
                <button class="type-btn" data-type="claude">Claude</button>
                <button class="type-btn" data-type="codex">Codex</button>
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
        <div class="placeholder">Select a session from the sidebar</div>
    </div>
</div>
<script>
(function() {{
    let sessions = [];
    let activeType = "all";
    let activeSessionPath = null;

    function relativeTime(isoStr) {{
        const d = new Date(isoStr);
        const now = new Date();
        const diffMs = now - d;
        const diffMin = Math.floor(diffMs / 60000);
        if (diffMin < 1) return "just now";
        if (diffMin < 60) return diffMin + "m ago";
        const diffHr = Math.floor(diffMin / 60);
        if (diffHr < 24) return diffHr + "h ago";
        const diffDay = Math.floor(diffHr / 24);
        if (diffDay < 7) return diffDay + "d ago";
        return d.toLocaleDateString("en-US", {{ month: "short", day: "numeric" }});
    }}

    function escHtml(s) {{
        const d = document.createElement("div");
        d.textContent = s;
        return d.innerHTML;
    }}

    function renderCards() {{
        const list = document.getElementById("sessionList");
        const filter = document.getElementById("filterInput").value.toLowerCase();
        const filtered = sessions.filter(function(s) {{
            if (activeType !== "all" && s.format !== activeType) return false;
            if (filter) {{
                const haystack = (s.project + " " + s.slug + " " + s.first_prompt).toLowerCase();
                return haystack.indexOf(filter) !== -1;
            }}
            return true;
        }});

        if (filtered.length === 0) {{
            list.innerHTML = '<div class="empty-state">No sessions found</div>';
            return;
        }}

        let html = "";
        for (let i = 0; i < filtered.length; i++) {{
            const s = filtered[i];
            const isActive = s.path === activeSessionPath;
            const badgeClass = s.format === "claude" ? "badge-claude" : "badge-codex";
            const label = s.format === "claude" ? "Claude" : "Codex";

            html += '<div class="session-card' + (isActive ? ' active' : '') + '" data-path="' + escHtml(s.encoded) + '" data-raw-path="' + escHtml(s.path) + '">';
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
                let prompt = s.first_prompt;
                // Strip XML-like tags for display
                prompt = prompt.replace(/<[^>]+>/g, "").trim();
                if (prompt) {{
                    html += '<div class="card-prompt">' + escHtml(prompt) + '</div>';
                }}
            }}
            html += '</div>';
        }}
        list.innerHTML = html;

        // Attach click handlers
        const cards = list.querySelectorAll(".session-card");
        cards.forEach(function(card) {{
            card.addEventListener("click", function() {{
                const encoded = card.getAttribute("data-path");
                const rawPath = card.getAttribute("data-raw-path");
                openSession(encoded, rawPath);
            }});
        }});
    }}

    function openSession(encoded, rawPath) {{
        activeSessionPath = rawPath;
        const content = document.getElementById("content");
        content.innerHTML = '<iframe src="/session/' + encoded + '"></iframe>';
        renderCards(); // re-render to update active state
        window.location.hash = encoded;
    }}

    // Type filter buttons
    document.querySelectorAll(".type-btn").forEach(function(btn) {{
        btn.addEventListener("click", function() {{
            document.querySelectorAll(".type-btn").forEach(function(b) {{
                b.classList.remove("active");
            }});
            btn.classList.add("active");
            activeType = btn.getAttribute("data-type");
            renderCards();
        }});
    }});

    // Text filter
    document.getElementById("filterInput").addEventListener("input", renderCards);

    // Load sessions
    fetch("/api/sessions")
        .then(function(r) {{ return r.json(); }})
        .then(function(data) {{
            sessions = data;
            renderCards();
            // Restore from hash
            if (window.location.hash) {{
                const encoded = window.location.hash.slice(1);
                const match = sessions.find(function(s) {{ return s.encoded === encoded; }});
                if (match) {{
                    openSession(encoded, match.path);
                }}
            }}
        }})
        .catch(function(err) {{
            document.getElementById("sessionList").innerHTML =
                '<div class="empty-state">Failed to load sessions</div>';
        }});
}})();
</script>
</body>
</html>
"""

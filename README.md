# cc-tooling

Personal Claude Code tooling — custom skills, agents, and more.

## Structure

Follows the [Claude Code plugin conventions](https://code.claude.com/docs/en/plugins):

```
cc-tooling/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── commands/                 # Slash commands (/command-name)
│   └── *.md
├── skills/                   # Model-invoked capabilities
│   └── <skill-name>/
│       └── SKILL.md
├── agents/                   # Agent definitions
│   └── *.md
├── hooks/                    # Lifecycle hooks
│   ├── hooks.json
│   └── hooks-handlers/
└── .mcp.json                 # MCP server configuration (optional)
```

## Usage

Test locally during development:

```sh
claude --plugin-dir ./
```

## Artifact Types

| Type | Location | Trigger |
|------|----------|---------|
| **Command** | `commands/*.md` | User-invoked via `/command-name` |
| **Skill** | `skills/*/SKILL.md` | Model-invoked based on context |
| **Agent** | `agents/*.md` | Model-invoked for complex tasks |
| **Hook** | `hooks/hooks.json` | Lifecycle events (`SessionStart`, etc.) |

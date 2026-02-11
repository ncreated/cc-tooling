# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Claude Code plugin repo — custom skills, agents, commands, and hooks for cross-project use.
All artifacts follow the [Claude Code plugin conventions](https://code.claude.com/docs/en/plugins).
See [README.md](README.md) for directory structure and artifact types overview.

## Testing

```sh
claude --plugin-dir ./
```

## Plugin Artifact Conventions

- **Commands** (`commands/*.md`): Markdown files with YAML frontmatter (`description`, `argument-hint`, `allowed-tools`). User-invoked via `/command-name`.
- **Skills** (`skills/<name>/SKILL.md`): Markdown with frontmatter (`name`, `description`, `version`). Model-invoked based on context. Can include `references/` subdirectory for supporting docs.
- **Agents** (`agents/*.md`): Markdown with frontmatter (`name`, `description`, `model`). Model-invoked for complex tasks.
- **Hooks** (`hooks/hooks.json`): JSON config referencing handler scripts in `hooks-handlers/`. Triggered by lifecycle events (`SessionStart`, etc.). Use `${CLAUDE_PLUGIN_ROOT}` for paths.
- **MCP** (`.mcp.json`): Root-level JSON config for external tool integration via Model Context Protocol.
- **Plugin metadata** (`.claude-plugin/plugin.json`): Required. Contains `name`, `description`, `author`.

## Writing Style

All code, comments, and documentation in English. Keep artifacts concise and focused.

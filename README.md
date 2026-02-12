# cc-tooling

Personal Claude Code plugin — custom skills for enhanced workflows.

## How to use

### Easiest way

```sh
claude --plugin-dir <path to this repo>
```

### Use skills

Skills are automatically available when the plugin is loaded. Claude will invoke them based on context, or you can explicitly call them:

```sh
/skill-name [arguments]
```

## Available Skills

### Communication

**`/friendly-tone`**
Injects a friendly, optimistic, and concise communication style with emojis.

### Research

**`/research-spec`**
Interactive guide for creating a structured research specification document. Creates a detailed spec file that can be used with the research team skills.

**`/research-team`**
Launch a Leader–Researcher–Reviewer agent team for autonomous structured deep research. Requires a research spec file and `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

**`/research-team-guided`**
Launch a Leader–Researcher–Reviewer agent team with you as a strategic guide and optional domain expert. Same as `research-team` but includes you in key decision points. Requires a research spec file and `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

## Development

See [CLAUDE.md](CLAUDE.md) for plugin conventions and development guidelines.

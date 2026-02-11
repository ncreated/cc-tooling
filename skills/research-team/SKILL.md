---
name: research-team
description: Launch a Leader–Researcher–Reviewer agent team for structured deep research from a specification file
version: 0.1.0
---

# Deep Research Team

You are the **Leader** of a three-agent research team. Your role is to coordinate, moderate, and synthesize — NOT to research or review yourself. You operate in **delegate mode**.

This skill requires Agent Teams (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`).

## Activation

This skill is invoked when the user wants to run a structured deep research process using an agent team. The user provides a path to a research specification file (created with `/cc-tooling:research-spec` or manually).

## Step 1 — Validate Prerequisites

1. Check that the environment variable `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is set to `1`. If not, tell the user to enable it:
   ```
   export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
   ```
   Then stop — do not proceed without agent teams enabled.

2. Read the spec file provided by the user. Verify it contains at minimum: a Research Topic and Key Questions. If the spec is incomplete, tell the user and suggest running `/cc-tooling:research-spec` to create a proper spec.

## Step 2 — Prepare Role Prompts

1. Read the role prompt templates from the plugin directory (resolve relative to `${CLAUDE_PLUGIN_ROOT}`):
   - `skills/research-team/references/researcher-prompt.md`
   - `skills/research-team/references/reviewer-prompt.md`

2. In each template, replace the `{RESEARCH_SPEC}` placeholder with the full contents of the user's spec file.

3. These prepared prompts become the spawn prompts for each teammate. They are fully self-contained — teammates do NOT inherit your conversation history.

## Step 3 — Spawn Teammates

Spawn two teammates:

- **Researcher** — using the prepared researcher prompt. Full tool access (Read, Grep, Glob, Bash, WebSearch, WebFetch).
- **Reviewer** — using the prepared reviewer prompt. Full tool access (Read, Grep, Glob, Bash, WebSearch, WebFetch).

## Step 4 — Orchestrate the Dialectical Process

Create shared tasks to coordinate the research phases:

### Phase 1 — Exploration
- Create a task for the Researcher: "Explore the problem space and produce initial proposals addressing the key questions in the spec."
- The Reviewer may independently explore to build context while waiting.

### Phase 2 — First Review
- Once the Researcher shares proposals, create a task for the Reviewer: "Review the Researcher's proposals. Produce a structured critique."

### Phase 3 — Iteration (max 3 rounds)
- After each critique, create a task for the Researcher: "Address the Reviewer's critique. Refine your proposals."
- After each refinement, create a task for the Reviewer: "Review the Researcher's revisions. Assess whether concerns are addressed."
- Monitor for convergence:
  - If the Reviewer declares "good enough" → move to synthesis.
  - If both parties reach consensus on key findings → move to synthesis.
  - After 3 dialectical rounds → force synthesis regardless, noting unresolved disagreements.

### Your Role During Iteration
- **Do NOT** do research or review yourself.
- **Do** monitor progress through task updates and messages.
- **Do** intervene if:
  - The discussion goes off-scope (redirect to spec's scope boundaries).
  - The teammates talk past each other (clarify the disagreement).
  - Progress stalls (set a deadline, narrow the focus).
- **Do** keep a running log of key findings, disagreements, and resolutions.

## Step 5 — Synthesize Final Output

Once the dialectical process completes, YOU (the Leader) write the final deliverable. Gather all findings from the teammates' messages and task updates, then produce:

### Output Document Structure

Write the file as `research-output-{topic-slug}.md` in the current working directory, where `{topic-slug}` is a kebab-case version of the research topic.

```markdown
# Research: {Topic}

> Spec: {path to spec file}
> Team: Leader (synthesis), Researcher (proposals), Reviewer (critique)
> Rounds: {number of dialectical rounds completed}

## Executive Summary

{2-3 paragraph overview of the research findings and key recommendations}

## Key Findings

### Finding 1: {Title}

**Researcher's Position:** {summary}

**Reviewer's Critique:** {summary}

**Resolution:** {consensus reached, or remaining disagreement with both positions stated}

### Finding N: {Title}
...

## Open Questions

{Questions that remain unresolved after the dialectical process. Include both parties' positions.}

## Recommendations

{Actionable recommendations based on the research findings. Ordered by confidence level.}
```

### Guidelines for Synthesis
- Represent both perspectives fairly.
- Clearly distinguish consensus findings from contested ones.
- Don't paper over genuine disagreements — document them as open questions.
- Prioritize findings by relevance to the spec's key questions.
- Include confidence levels from the Researcher's proposals.

## Step 6 — Report to User

After writing the output file:
1. Tell the user the file path.
2. Provide a brief (3-5 sentence) summary of the key findings.
3. Highlight any open questions that may need further investigation.

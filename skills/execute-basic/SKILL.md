---
name: execute-basic
description: Launch a Leader-Producer-Verifier agent team that takes research output and produces artifacts consistent with the findings
version: 0.1.0
---

# Execution Team

You are the **Leader** of a three-agent execution team. Your role is to coordinate, plan, and orchestrate — NOT to produce artifacts yourself. You operate in **delegate mode**.

This skill requires Agent Teams (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`).

## Activation

This skill is invoked when the user wants to execute on research findings by producing artifacts (code, documentation, configuration, etc.). The user provides a path to a research output file (produced by `/research-basic`, `/research-guided`, or `/research-multi-angle`).

## Step 1 — Validate Prerequisites

1. Check that the environment variable `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is set to `1`. If not, tell the user to enable it:
   ```
   export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
   ```
   Then stop — do not proceed without agent teams enabled.

2. If the user did not provide a path to a research output file, ask them for it using `AskUserQuestion` (e.g., "Which research output file should I execute on? Provide a path to a `research-output-*.md` file."). Do not proceed without a file path.

3. Read the research output file. Verify it contains structured findings and recommendations (look for sections like Key Findings, Recommendations, or equivalent). If the file lacks actionable content, tell the user and suggest running a research skill first.

## Step 2 — Analyze Research & Plan Execution

Read the research output thoroughly and produce an **Execution Plan**:

### For each artifact to produce:

| Field | Description |
|-------|-------------|
| **Name** | Descriptive artifact name |
| **Type** | Code / Documentation / Configuration / Design / Other |
| **Research Basis** | Which specific findings/recommendations this addresses |
| **Acceptance Criteria** | How to verify the artifact is correct and complete |
| **Open Questions** | Ambiguities in the research that require judgment calls |

### Plan structure:
- Order artifacts by dependencies (produce foundations first).
- Group related artifacts when they should be produced together.
- Note cross-artifact dependencies explicitly.

## Step 2.5 — User Approval of Execution Plan

This is the **only mandatory user touchpoint**. Present the execution plan and ask using `AskUserQuestion`:

- **Question:** "Does this execution plan look right?"
- **Options:** Approve / Adjust

If the user chooses "Adjust", incorporate their feedback and re-present the plan. Do NOT proceed to production without explicit approval.

## Step 3 — Prepare Role Prompts

1. Read the role prompt templates from the plugin directory (resolve relative to `${CLAUDE_PLUGIN_ROOT}`):
   - `skills/execute-basic/references/producer-prompt.md`
   - `skills/execute-basic/references/verifier-prompt.md`

2. In each template, replace two placeholders:
   - `{RESEARCH_OUTPUT}` — full contents of the research output file
   - `{EXECUTION_PLAN}` — the execution plan from Step 2

3. These prepared prompts become the spawn prompts for each teammate. They are fully self-contained — teammates do NOT inherit your conversation history.

## Step 4 — Spawn Teammates

Spawn two teammates:

- **Producer** — using the prepared producer prompt. Full tool access (Read, Grep, Glob, Bash, WebSearch, WebFetch, Write, Edit).
- **Verifier** — using the prepared verifier prompt. Full tool access (Read, Grep, Glob, Bash, WebSearch, WebFetch, Write, Edit).

## Step 5 — Orchestrate Execution

### Phase 1 — Production

- Create a task for the Producer: "Produce all artifacts according to the execution plan."
- The Producer works through the plan in order, creating artifacts and reporting progress via Artifact Reports.
- The Verifier may independently explore the codebase and research output to build context while waiting.

### Phase 2 — Verification

- Once the Producer reports completion, create a task for the Verifier: "Verify all produced artifacts against the research output and execution plan."
- The Verifier evaluates each artifact across three dimensions:
  1. **Research Consistency** — does the artifact faithfully implement the research findings?
  2. **Plan Completeness** — does it satisfy the acceptance criteria?
  3. **Artifact Correctness** — does it actually work (code compiles, docs are coherent, configs are valid)?

### Phase 3 — Iteration (max 3 rounds)

- If the Verifier reports **Blocking** or **Important** issues:
  - Create a task for the Producer: "Address the Verifier's issues: {summary of issues}."
  - After the Producer revises, create a task for the Verifier: "Re-verify the revised artifacts."
- If the Verifier declares all remaining issues are **Minor** → end iteration, accept as verified.
- After 3 rounds → force completion regardless, noting unresolved issues.

### Your Role During Execution

- **Do NOT** produce or modify artifacts yourself.
- **Do** monitor progress through task updates and messages.
- **Do** intervene if:
  - The Producer drifts from the execution plan (redirect).
  - The Verifier raises issues outside scope of the research (refocus on research consistency).
  - Progress stalls (narrow focus, set deadlines).
- **Do** keep a running log of completed artifacts, issues found, and resolutions.

## Step 6 — Write Execution Report

Once execution completes, YOU (the Leader) write the final report as `execution-report-{topic-slug}.md` in the current working directory, where `{topic-slug}` matches the research output's topic slug.

```markdown
# Execution Report: {Topic}

> Research: {path to research output file}
> Team: Leader (coordination), Producer (artifacts), Verifier (quality)
> Iteration Rounds: {number of verification rounds completed}

## Executive Summary

{2-3 paragraph overview of what was produced and the overall quality assessment}

## Execution Plan

{Summary of the approved execution plan — artifact list with types and research basis}

## Artifacts Produced

### {Artifact Name}

- **Path:** {file path}
- **Type:** {Code / Documentation / Configuration / Design / Other}
- **Research Basis:** {which findings/recommendations this addresses}
- **Verification Status:** {Verified / Verified with minor issues / Unresolved issues}
- **Judgment Calls:** {decisions made where research was ambiguous, with reasoning}

## Verification Summary

- **Resolved Issues:** {issues found and fixed during iteration}
- **Accepted Minor Issues:** {minor issues accepted as-is, with rationale}
- **Unresolved Issues:** {issues remaining after max iterations, if any}

## Research Coverage

- **Addressed:** {list of recommendations/findings that were implemented}
- **Not Addressed:** {list of recommendations/findings not covered, with reasons}

## Next Steps

{Suggested follow-up actions, remaining work, or areas needing further research}
```

## Step 7 — Report to User

After writing the execution report:
1. Tell the user the report file path.
2. Provide a brief (3-5 sentence) summary of what was produced.
3. Highlight any unresolved issues or recommendations not addressed.
4. List all artifact file paths for easy reference.

---
name: research-team-chaos
description: Launch a Leader + Connector + N Researchers team for divergent deep research — researchers pick angles, Connector cross-analyzes and challenges, no dedicated reviewer
version: 0.1.0
---

# Deep Research Team (Chaos)

You are the **Leader** of a multi-agent research team. Your role is to coordinate, moderate, and synthesize — NOT to research yourself. You operate in **delegate mode**.

This skill uses a fundamentally different approach from the standard research team: **N Researchers** independently pick angles and do deep research, a **Connector** cross-analyzes all findings and creates targeted challenges, and the "chaos" of multiple perspectives surfaces richer cross-connections and insights.

This skill requires Agent Teams (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`).

## Activation

This skill is invoked when the user wants to run a divergent, multi-angle deep research process using an agent team. The user provides a path to a research specification file (created with `/cc-tooling:research-spec` or manually).

## Step 1 — Validate Prerequisites

1. Check that the environment variable `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is set to `1`. If not, tell the user to enable it:
   ```
   export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
   ```
   Then stop — do not proceed without agent teams enabled.

2. Read the spec file provided by the user. Verify it contains at minimum: a Research Topic and Key Questions. If the spec is incomplete, tell the user and suggest running `/cc-tooling:research-spec` to create a proper spec.

## Step 2 — Determine Team Size

Ask the user how many researchers should explore the topic using `AskUserQuestion`:

- **Question**: "How many researchers should explore this topic?"
- **Header**: "Team size"
- **Options**:
  - "3 researchers (Recommended)" — Good balance of coverage and coordination overhead
  - "5 researchers" — Broader coverage, more angles to cross-analyze
  - "7 researchers" — Maximum divergence, best for large or highly multifaceted topics
- The user can also provide a custom number via "Other"
- Store as N. Minimum is 2 — if user provides less, default to 2 with an explanation.

## Step 3 — Prepare Role Prompts

1. Read the role prompt templates from the plugin directory (resolve relative to `${CLAUDE_PLUGIN_ROOT}`):
   - `skills/research-team-chaos/references/researcher-prompt.md`
   - `skills/research-team-chaos/references/connector-prompt.md`

2. For each researcher 1..N, prepare a copy of the researcher prompt with these placeholders replaced:
   - `{RESEARCH_SPEC}` → full contents of the user's spec file
   - `{RESEARCHER_NUMBER}` → the researcher's number (1, 2, 3, ...)
   - `{TOTAL_RESEARCHERS}` → N

3. For the Connector, prepare the connector prompt with these placeholders replaced:
   - `{RESEARCH_SPEC}` → full contents of the user's spec file
   - `{TOTAL_RESEARCHERS}` → N

4. These prepared prompts become the spawn prompts for each teammate. They are fully self-contained — teammates do NOT inherit your conversation history.

## Step 4 — Spawn Team

Spawn all teammates:

- **Researcher-1** through **Researcher-N** — each using their prepared researcher prompt. Full tool access (Read, Grep, Glob, Bash, WebSearch, WebFetch).
- **Connector** — using the prepared connector prompt. Full tool access (Read, Grep, Glob, Bash, WebSearch, WebFetch). The Connector is told to wait for the Leader's signal before starting cross-analysis.

Spawn all teammates concurrently.

## Step 5 — Orchestrate Research

### Phase 1 — Angle Discovery (parallel)

- Create a task for all researchers: "Explore the problem space and propose your unique research angle. Message the Leader with your proposed angle."
- All N researchers work concurrently to discover and propose their angles.
- **Barrier**: Wait for ALL N angle proposals to arrive.
- Once all proposals are collected, check for overlap:
  - If two or more angles are too similar, message the later-numbered researcher(s) to differentiate their angle. Wait for updated proposals.
  - Repeat until all N angles are sufficiently distinct.

### Phase 1.5 — User Angle Confirmation (TOUCHPOINT 1/2)

Present all N angles to the user via `AskUserQuestion`:

- Provide a text summary of each angle before the question:
  ```
  Proposed research angles:
  1. Researcher-1: {angle summary}
  2. Researcher-2: {angle summary}
  ...
  N. Researcher-N: {angle summary}
  ```
- **Question**: "Do these research angles look good?"
- **Header**: "Angles"
- **Options**:
  - "Approve all angles (Recommended)"
  - "I want to adjust some angles"
- If the user wants adjustments, ask a follow-up question to identify which angles to change and how, then message affected researchers with the updated direction.
- After confirmation, create a task for each researcher: "Your angle is confirmed: {angle}. Begin deep research."

### Phase 2 — Deep Research (parallel)

- All N researchers investigate their confirmed angles concurrently.
- Each researcher produces a Findings Report and messages the Leader.
- **Barrier**: Wait for ALL N Findings Reports to arrive.

### Phase 3 — Cross-Analysis (max 2 rounds)

**Round 1 — Connector cross-analyzes:**

- Create a task for the Connector that includes ALL N Findings Reports in the task description.
- The Connector reads all reports and produces:
  - A **Cross-Analysis Report**: cross-connections between angles, contradictions, gaps, emergent insights
  - **Targeted challenge tasks** for specific researchers (e.g., "Researcher-2: Your finding X contradicts Researcher-5's finding Y. Evidence: ... How do you reconcile?")
- Each researcher gets 1-3 focused challenges (not full peer reports to read).

**Round 1b — Researchers respond (parallel):**

- Create tasks for each challenged researcher with their specific challenges.
- All researchers respond to their targeted challenges simultaneously.
- Each produces a focused response: defend with evidence, revise position, or incorporate the cross-connection.
- **Barrier**: Wait for ALL responses to arrive.

**Round 2 (conditional):**

- Only if the Connector flags remaining **Blocking** contradictions.
- The Connector reviews responses, creates one more round of targeted challenges on unresolved issues.
- Researchers respond. Then force-converge regardless of remaining disagreements.

### Your Role During Phase 3
- Track task completion for all researchers and the Connector.
- Intervene if any agent goes off-scope (redirect to spec's scope boundaries).
- Intervene if progress stalls (set a deadline, narrow the focus).
- Maintain a running log of key findings, cross-connections, disagreements, and resolutions.
- **Do NOT** do research yourself.

### Phase 4 — Pre-Synthesis User Approval (TOUCHPOINT 2/2, MANDATORY)

**This phase is MANDATORY before synthesis.**

After Phase 3 completes, BEFORE writing the final output:

1. **Gather key findings**:
   - Connector's cross-analysis highlights (cross-connections, contradictions, emergent insights)
   - Each researcher's final position (after responding to challenges)
   - Consensus points across researchers
   - Active disagreements that remain unresolved

2. **Present to user** using a text summary:

```markdown
## Final Approval Required

Before I synthesize the final output, please review the research results:

### Research Angles
1. Researcher-1: {angle} — {one-line conclusion}
2. Researcher-2: {angle} — {one-line conclusion}
...

### Key Cross-Connections
1. {Cross-connection}: {summary}
2. ...

### Consensus Findings
1. {Finding}: {summary} (supported by Researchers {list})
2. ...

### Active Disagreements
1. {Topic}: Researcher-{X} says {position} vs Researcher-{Y} says {position}
2. ...

### Emergent Insights
1. {Insight from combining multiple angles}
2. ...
```

3. Then ask via `AskUserQuestion`:
   - **Question**: "Do you approve these findings for synthesis?"
   - **Header**: "Approval"
   - **Options**:
     - "Approve as-is (Recommended)"
     - "Request adjustments"
   - If adjustments requested, ask follow-up to identify what to change, create tasks for affected researchers, then re-present for approval.

4. **Only proceed to Step 6** after user explicitly approves.

## Step 6 — Synthesize Final Output

**Prerequisites:** User has approved the findings in Phase 4.

Once the user has approved, YOU (the Leader) write the final deliverable. Gather all findings from the teammates' messages and task updates, then produce:

### Output Document Structure

Write the file as `research-output-{topic-slug}.md` in the current working directory, where `{topic-slug}` is a kebab-case version of the research topic.

```markdown
# Research: {Topic}

> Spec: {path to spec file}
> Team: Leader (coordination + synthesis), Connector (cross-analysis), {N} Researchers (angles + deep research)
> Angles: {comma-separated list of angle names}
> Challenge rounds: {number of cross-analysis rounds completed}

## Executive Summary

{2-3 paragraph overview emphasizing how the multiple angles converged and diverged. Highlight the most valuable cross-connections discovered.}

## Research Angles

### Angle 1: {Angle Name} (Researcher-1)

**Findings:** {summary of key findings}

**Final Position:** {researcher's position after responding to challenges}

**Confidence:** {High/Medium/Low}

### Angle N: {Angle Name} (Researcher-N)
...

## Cross-Connections

{The unique value of this skill — insights from the Connector's cross-analysis.}

### Connection 1: {Title}
**Between:** Researcher-{X} ({angle}) and Researcher-{Y} ({angle})
**Nature:** {reinforcing / contradicting / extending}
**Insight:** {what this connection reveals}

### Connection N: {Title}
...

## Consensus Findings

{What the collective agrees on, with supporting angles listed.}

1. **{Finding}** — supported by Researchers {list}. {Summary with evidence.}
2. ...

## Active Disagreements

{Unresolved disputes with all positions fairly represented.}

1. **{Topic}**
   - Researcher-{X}: {position with evidence}
   - Researcher-{Y}: {position with evidence}
   - Connector's assessment: {which position has stronger support and why}

## Open Questions

{Questions that remain unresolved. Include which angles touched on them and what would be needed to resolve them.}

## Recommendations

{Ordered by confidence level. Note which angles support each recommendation.}

1. **{Recommendation}** (Confidence: High)
   Supported by: Researchers {list}
   {Reasoning}

2. **{Recommendation}** (Confidence: Medium)
   ...
```

### Guidelines for Synthesis
- Represent all researchers' perspectives fairly.
- The Cross-Connections section is the core differentiator — make it thorough.
- Clearly distinguish consensus findings from contested ones.
- Don't paper over genuine disagreements — document them with all positions.
- Prioritize findings by relevance to the spec's key questions.
- Include confidence levels from each researcher.
- Note where cross-connections produced insights that no single angle would have found.

## Step 7 — Report to User

After writing the output file:
1. Tell the user the file path.
2. Provide a brief (3-5 sentence) summary of the key findings.
3. Highlight the most valuable cross-connections discovered.
4. Note any open questions that may need further investigation.

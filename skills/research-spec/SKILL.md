---
name: research-spec
description: Interactive guide for creating a structured research specification document
version: 0.1.0
---

# Research Spec Creator

You help the user create a structured research specification document by walking them through each section conversationally.

## Process

1. **Walk through each section** — Guide the user through each section one at a time, in order:
   - **Research Topic** — Ask what they want to research. Help them refine a clear, concise title and description.
   - **Motivation / Background** — Ask why this matters. What decision or problem does it inform?
   - **Scope & Boundaries** — Help define what's in scope and what's explicitly out. Push for specificity.
   - **Key Questions** — Help them formulate numbered, concrete questions the research should answer.
   - **Constraints** — Ask about time, technology, or organizational limits.
   - **Anti-Goals** — Help articulate what the research is NOT trying to do.
   - **Expected Deliverables** — What artifacts should the research produce?
   - **Success Criteria** — How will they know the research was good enough?

2. **Be conversational, not bureaucratic** — Don't dump all sections at once. Handle one section at a time. Ask follow-up questions to draw out details. Suggest improvements when the user's input is too vague.

3. **Write the spec file** — Once all sections are complete, assemble the full spec document using the output format below and write it to a file. Default filename: `research-spec.md` in the current working directory. Ask the user if they want a different name or location.

4. **Suggest next step** — After writing the file, tell the user they can run `/cc-tooling:research-team <spec-file>` to launch the research team (requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`).

## Output Format

Write the spec file using exactly this structure:

```markdown
# Research Specification

## Research Topic

{title and one-paragraph description}

## Motivation / Background

{why this matters, what decision or problem it informs}

## Scope & Boundaries

### In Scope

- {specific areas to explore}

### Out of Scope

- {what to explicitly skip}

## Key Questions

1. {numbered concrete questions}

## Constraints

- {time, technology, or organizational limits}

## Anti-Goals

- {what this research is NOT trying to achieve}

## Expected Deliverables

- {artifacts the research should produce}

## Success Criteria

- {how to know the research was good enough}
```

## Guidelines

- Keep the conversation focused. One section at a time.
- If the user gives a short answer, ask one clarifying question before moving on.
- If the user says "skip" for a section, leave a `-` placeholder and move on.
- Use the output format exactly — the research team skill depends on it.

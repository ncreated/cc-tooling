# User Consultation Guidelines

You are the Leader. Your role includes deciding WHEN and HOW to consult the user.

## User's Domain Expert Status

**Remember from Step 1.5:** You asked the user if they're a domain expert. Store this throughout the session:
- If **YES**: You can consult them for domain-specific questions (Moment 5 below)
- If **NO**: Skip domain expertise consultations, focus on strategic decisions only

**Remember from Step 1.5:** You also asked about their involvement preference:
- **Standard involvement**: Use all consultation moments as described
- **Less involvement**: Only consult on blocking issues and final approval
- **More involvement**: Be more proactive, consult on important (not just blocking) decisions

## Principles

1. **Respect user's time** — Only ask when it materially affects research direction or outcome
2. **Batch questions** — Collect multiple questions when possible (max 4 per AskUserQuestion)
3. **Provide context** — User needs to understand the stakes and trade-offs
4. **Offer options** — Specific choices, not open-ended questions (except domain expertise)
5. **Trust your agents** — Push them to resolve minor issues themselves first
6. **Domain expertise is special** — Only use if user confirmed expertise AND question is truly unanswerable through research

## When to Consult (GOOD MOMENTS)

### 1. After Initial Exploration (Phase 1.5)

**Context:** Researcher has completed broad exploration and identified 3-5 main research areas.

**When:** After Phase 1 completes, before deep investigation begins.

**Why:** User can align research effort with their priorities and goals.

**How:**
- Use `AskUserQuestion` with `multiSelect: true`
- Present 3-5 research areas as options
- Each option should have clear description of what it involves
- Example:
  ```
  header: "Priorities"
  question: "Which areas should we prioritize for deep investigation?"
  options:
    - label: "Performance optimization strategies"
      description: "Analyze performance bottlenecks and potential solutions"
    - label: "Security considerations"
      description: "Evaluate security implications and best practices"
  ```

### 2. Fundamental Disagreements

**Context:** Researcher and Reviewer have a fundamental disagreement after 1 round of dialectic that affects a core decision.

**Trigger:** Either agent sends message with `[FUNDAMENTAL DISAGREEMENT]`

**When:** After 1 round of back-and-forth, if no convergence on key issue.

**Why:** User can provide strategic direction or tie-breaking decision.

**How:**
- Use `AskUserQuestion` with 2-3 options representing the positions
- Provide clear context from both sides
- Example:
  ```
  header: "Approach"
  question: "The Researcher recommends X, but the Reviewer advocates for Y. Which aligns better with your goals?"
  options:
    - label: "Approach X (Researcher's position)"
      description: "Benefits: ... Trade-offs: ..."
    - label: "Approach Y (Reviewer's position)"
      description: "Benefits: ... Trade-offs: ..."
    - label: "Hybrid approach"
      description: "Combine elements of both"
  ```

**Important:** Only escalate disagreements that are:
- **Blocking**: Cannot proceed without resolution
- **Core**: Affects key questions in the spec
- **Unresolvable**: Additional research won't help

### 3. Multiple Valid Approaches

**Context:** Researcher has identified 2-3 equally viable approaches with different implications.

**Trigger:** Researcher sends `[USER INPUT NEEDED]` about approach selection.

**When:** The approaches have:
- Similar confidence levels
- Different trade-offs or implications
- Dependency on user's context or goals

**Why:** Choice depends on user's priorities, constraints, or long-term strategy.

**How:**
- Use `AskUserQuestion` with 2-3 options
- Clearly explain trade-offs for each approach
- Example:
  ```
  header: "Tech stack"
  question: "Which approach aligns better with your project goals?"
  options:
    - label: "Library A"
      description: "Pros: ..., Cons: ..., Best if: ..."
    - label: "Library B"
      description: "Pros: ..., Cons: ..., Best if: ..."
  ```

### 4. Low Confidence on Critical Findings

**Context:** Researcher has low confidence on a finding that's critical to a key question.

**When:**
- Finding is marked "Low" confidence
- Finding affects a core research question
- No way to increase confidence through available tools

**Why:** User's experience or intuition can validate or flag concerns.

**How:**
- Use `AskUserQuestion` with Yes/No + context option
- Example:
  ```
  header: "Validation"
  question: "Based on your experience, does [finding] sound reasonable?"
  options:
    - label: "Yes, that seems right"
      description: "Aligns with my understanding"
    - label: "No, I have concerns"
      description: "I'll provide context"
    - label: "I'm not sure"
      description: "Outside my experience"
  ```

### 5. Domain Expertise Needed

**PREREQUISITES:**
- User confirmed domain expert status in Step 1.5
- Agent flagged `[DOMAIN EXPERTISE NEEDED]`
- Information is NOT available through documentation, code, or web sources

**Context:** Research has hit a gap that requires practical experience, real-world knowledge, or industry insights.

**Examples of valid domain questions:**
- "How do teams typically handle [X] in production?"
- "What are the real-world trade-offs between [Y] and [Z]?"
- "Are there organizational or industry constraints for [decision]?"
- "In practice, which approach is more maintainable?"

**Why:** User's domain expertise provides insights unavailable to AI agents.

**How:**
- Can use `AskUserQuestion` with options + "I don't know" option
- Or present as text question and allow free-form response
- Example:
  ```
  header: "Domain Q"
  question: "As a domain expert, what's your experience with [specific question]?"
  options:
    - label: "Teams typically use [approach A]"
      description: "Based on industry standard practice"
    - label: "Teams typically use [approach B]"
      description: "More common in modern setups"
    - label: "It varies / I don't know this specific area"
      description: "I'll skip this one"
  ```

**Important:**
- Only use if user is confirmed domain expert
- Only ask questions that research cannot answer
- Respect if user says "I don't know" — don't pressure

### 6. Final Approval (Phase 4) — MANDATORY

**Context:** Dialectical process has completed. Before writing final output.

**When:** After Phase 3 completes, regardless of convergence status.

**Why:** User has final oversight over research conclusions before they're documented.

**How:**

**Step 1:** Present findings as text summary (NOT AskUserQuestion initially):

```markdown
## Final Approval Required

Before I synthesize the final output, please review these key findings:

### Key Findings
1. [Finding]: [Summary] (Confidence: High/Medium/Low)
   - Researcher: [position]
   - Reviewer: [assessment]

2. [Finding]: [Summary]
   - [Include all findings that materially impact the output]

### Decisions Made
1. [Decision]: Chose [X] over [Y] because [reasoning]
2. [Decision]: ...

### Recommendations
1. [Recommendation] (based on Finding 1, 2)
2. [Recommendation]...

### Open Questions
1. [Question] - requires [what would resolve it]
2. [Question]...

**Please confirm:**
- Approve as-is → I'll proceed to synthesis
- Request adjustments → Specify which findings/decisions need revision
```

**Step 2:** Wait for user response.

**Step 3:** If adjustments requested:
- Create tasks for relevant agents to address adjustments
- Wait for revised proposals
- Re-present updated findings for approval
- Repeat until user approves

**Step 4:** Only proceed to Step 5 (synthesis) after explicit user approval.

**Important:**
- This is the ONLY mandatory consultation (besides initial interview)
- Filter for material impact — don't present every minor detail
- Give user clear approve/adjust choice
- Don't proceed without approval

## When NOT to Consult (BAD MOMENTS)

### Implementation Details

**Example:** "Should we use camelCase or snake_case?"
**Why skip:** Agent can decide based on codebase conventions.

### Stylistic Preferences

**Example:** "Should the report have 3 or 4 sections?"
**Why skip:** Doesn't affect research outcome or findings.

### Verifiable Information

**Example:** "Which library is more popular?"
**Why skip:** Use WebSearch or GitHub stats to verify.

### During Active Research

**Example:** While Researcher is mid-exploration, "Quick question about X"
**Why skip:** Interrupts flow. Batch questions for natural breakpoints.

### Minor Disagreements

**Example:** Researcher and Reviewer disagree on wording in a proposal.
**Why skip:** Not fundamental. They can resolve through dialectic.

### Every Decision

**Example:** "Should I read file A or file B first?"
**Why skip:** Agents should operate autonomously on research tactics.

## Batching Questions

When multiple questions arise in the same phase, batch them:

**Good:**
- Collect 2-4 related questions
- Present in single `AskUserQuestion` (use `questions` array)
- Each question has its own header, options, description

**Example:**
```javascript
AskUserQuestion({
  questions: [
    {
      question: "Which areas should we prioritize?",
      header: "Priority",
      options: [...],
      multiSelect: true
    },
    {
      question: "What's your experience with [domain question]?",
      header: "Domain Q",
      options: [...]
    }
  ]
})
```

**When NOT to batch:**
- Questions are unrelated (different phases)
- One question's answer affects the next
- Total > 4 questions (split into multiple consultations)

## Using AskUserQuestion

### Parameters

- **multiSelect**:
  - `false` (default) — single choice (tie-breaking, approach selection)
  - `true` — multi-select (prioritizing areas, selecting multiple features)

- **header**:
  - Short label (max 12 chars)
  - Examples: "Priority", "Approach", "Tech", "Domain Q", "Validation"

- **question**:
  - Full context and clear question
  - End with question mark
  - If multiSelect, phrase accordingly: "Which features..." not "Which feature..."

- **options**:
  - 2-4 specific choices
  - Each has `label` (concise) and `description` (explains implications)
  - No need for "Other" option (automatically provided)

### Example Patterns

**Single choice (tie-breaking):**
```javascript
{
  question: "Which approach should we pursue?",
  header: "Approach",
  multiSelect: false,
  options: [
    { label: "Approach A", description: "Benefits and trade-offs" },
    { label: "Approach B", description: "Benefits and trade-offs" }
  ]
}
```

**Multi-select (prioritization):**
```javascript
{
  question: "Which areas should we investigate deeply?",
  header: "Priorities",
  multiSelect: true,
  options: [
    { label: "Performance", description: "Analyze bottlenecks and optimizations" },
    { label: "Security", description: "Evaluate security implications" },
    { label: "Scalability", description: "Assess scaling strategies" }
  ]
}
```

**Validation:**
```javascript
{
  question: "Does this finding align with your experience?",
  header: "Validation",
  multiSelect: false,
  options: [
    { label: "Yes, seems right", description: "Matches my understanding" },
    { label: "No, I have concerns", description: "I'll provide details" },
    { label: "Not sure", description: "Outside my experience" }
  ]
}
```

## Adjusting for User Preference

Based on Step 1.5 involvement preference:

### Standard Involvement
- Use all 6 consultation moments as described
- Balance autonomy with guidance

### Less Involvement
- Skip moments 1, 3, 4 unless blocking
- Always do moment 2 (fundamental disagreements) if blocking
- Only use moment 5 (domain expertise) if critical
- Always do moment 6 (final approval) — mandatory

### More Involvement
- Be more proactive at moment 3 (multiple approaches)
- Consult at moment 4 (low confidence) even on non-critical findings
- Check in mid-Phase for strategic guidance
- Still batch questions to respect time

## Summary Checklist

Before consulting the user, ask yourself:

- [ ] Does this materially affect research direction or outcome?
- [ ] Have agents exhausted research tools to resolve this themselves?
- [ ] Is this a strategic decision (not a tactical one)?
- [ ] Can I batch this with other pending questions?
- [ ] Does this align with user's involvement preference?
- [ ] If domain expertise: Did user confirm expert status?
- [ ] If final approval: Have I filtered for material impact only?

If all relevant checks pass → consult. Otherwise → let agents continue.

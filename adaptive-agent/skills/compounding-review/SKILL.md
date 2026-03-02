---
name: Compounding Review
description: >
  Activate after any merge, implementation, or code change to verify the new
  code compounds existing effort rather than being an isolated addition. Use
  when reviewing PRs, after merging branches, or when the user asks to review
  recent changes for integration quality.
version: 1.0.0
---

# Compounding Review Protocol

Code that doesn't integrate is technical debt on arrival.
The question is never "does it work?" — it's "does it COMPOUND?"

## The Six Review Axes

### 1. Fits the Architecture

**Test**: Read 3 existing files adjacent to the new code. Does the new code
look like it belongs? Same patterns, same idioms, same abstraction level?

**Fail signal**: You have to mentally "shift gears" when reading the new code
compared to the surrounding code.

**How to check**:
- Compare import styles
- Compare error handling patterns
- Compare naming conventions
- Compare abstraction levels (are raw SQL queries next to ORM calls?)

### 2. Extends, Don't Duplicate

**Test**: Search the codebase for functions/utilities that do similar things
to what the new code introduces. Any overlaps?

**Fail signal**: A new helper function that does what an existing utility
already does, maybe with slightly different argument names.

**How to check**:
- Grep for function names with similar semantic meaning
- Check `utils/`, `helpers/`, `lib/`, `shared/` directories
- Look for existing abstractions the new code could have used

### 3. Reachable and Wired

**Test**: Trace from any entry point (route, command, UI, cron) — can you
reach the new code through the normal execution path?

**Fail signal**: New code exists in the repo but nothing calls it. It's a
file sitting in a directory, disconnected.

**How to check**:
- For new exports: grep for imports of that export across the codebase
- For new routes: check they're registered in the router
- For new components: check they're exported from the module index
- For new CLI commands: check they're in the command registry

**This axis is a hard gate**: if it fails, ALWAYS BLOCK. Dead code must not merge.

### 4. Tested in Kind

**Test**: Does the new code have tests? Do those tests follow the same
framework, style, and location pattern as existing tests?

**Fail signal**: No tests, OR tests using a different framework/pattern
than the rest of the repo.

**How to check**:
- Look for test files matching the new source files
- Compare test structure to existing tests (same describe/it patterns?)
- Check test location matches convention (colocated? `__tests__/`? `test/`?)

### 5. Enables Next Work

**Test**: Could another developer (or agent) pick up the next related feature
and build on what was just added? Are the interfaces clear? Extension points obvious?

**Fail signal**: The implementation is complete but closed. Nothing can build
on top of it without refactoring it first.

**How to check**:
- Are types/interfaces exported for others to use?
- Are functions generic enough to be called from multiple places?
- Does it extend existing abstractions rather than creating parallel ones?

### 6. Roadmap Connected

**Test**: Does this work correspond to a tracked item (issue, TODO, roadmap entry)?
Can you draw a line from this PR to a product outcome?

**Fail signal**: Technically sound code that serves no stated goal. "Interesting"
code nobody asked for.

**How to check**:
- Read TODO.md, ROADMAP.md, CLAUDE.md for current priorities
- Check `gh issue list` for related issues
- Check PR description for issue references

## Verdict Logic

| Result | Meaning |
|--------|---------|
| ALL axes pass | **SHIP** — this compounds |
| 1-2 axes soft-fail | **REVISE** — fix the gaps, then ship |
| Any axis hard-fail | **BLOCK** — needs rethinking |
| "Reachable and Wired" fails | **ALWAYS BLOCK** — dead code must not merge |

## Output Format

Adapt the format to match the repo's documentation style. The content is:

```
Summary: [one sentence — what was reviewed and the verdict]

1. Architecture Fit: [pass/soft-fail/hard-fail] — [evidence]
2. Extends Don't Duplicate: [pass/soft-fail/hard-fail] — [evidence]
3. Reachable and Wired: [pass/soft-fail/hard-fail] — [evidence]
4. Tested in Kind: [pass/soft-fail/hard-fail] — [evidence]
5. Enables Next Work: [pass/soft-fail/hard-fail] — [evidence]
6. Roadmap Connected: [pass/soft-fail/hard-fail] — [evidence]

Verdict: [SHIP | REVISE | BLOCK]
Action Items: [specific, actionable items if not SHIP]
```

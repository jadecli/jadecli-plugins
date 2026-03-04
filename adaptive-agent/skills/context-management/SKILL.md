---
name: Context Management
description: >
  Activate during long-running sessions, multi-file refactors, or when the
  conversation history is growing large. Manages context lifecycle through
  compaction, memory persistence, and caching-aware behavior. Derived from
  Anthropic cookbook patterns for session memory compaction and automatic
  context compaction.
version: 1.0.0
---

# Context Management Patterns

Context is a finite, expensive resource. These patterns prevent context rot
and keep sessions productive over long task chains.

## Session Memory Compaction

When the conversation is getting long (many tool calls, large file reads),
proactively compress what you're holding in memory.

Priority order for what to preserve:

1. **User corrections** — anything the human told you to do differently
2. **Error messages** — exact text, verbatim
3. **Active work state** — current branch, files being edited, task in progress
4. **Key decisions made** — architectural choices, rejected approaches and why
5. **Completed work** — what's done (summary only, not full details)
6. **Reference paths** — file paths, URLs, config values mentioned

What to drop:

- Full file contents already committed (you can re-read them)
- Verbose tool output from successful operations
- Exploratory reads that didn't yield useful information
- Intermediate reasoning that led to a final decision

## Cross-Session Memory

If the repo has a `.claude/memories/` directory (or similar), use it:

- Write debugging patterns you discovered: `patterns/debug-auth.md`
- Write architectural decisions: `decisions/chose-drizzle-over-prisma.md`
- Write runbooks for complex processes: `runbooks/deploy-staging.md`

If no memory directory exists and you discover something the next session
should know, suggest creating one following the repo's doc conventions.

## Caching-Aware Behavior

Your CLAUDE.md and system context are cached across turns within a session.
This means:

- First turn is slower (cache miss) — be patient
- Subsequent turns are faster (cache hit) — use multi-turn for complex tasks
- Don't repeat stable context in prompts — it's already cached
- Put architectural decisions in CLAUDE.md, not in conversation

When spawning sub-agents, give them the minimum context they need:

- The specific task
- The relevant file paths
- The conventions that apply to their scope
- NOT the full conversation history

## Parallel Agent Context Isolation

When using the Agent tool for parallel work:

- Each sub-agent gets its own context -- don't assume shared state
- Pass codebase conventions explicitly to each sub-agent
- Scope each sub-agent to a module boundary from the bootstrap
- Never let two sub-agents modify the same file

Monorepo with `packages/`: one agent per package.
Service-oriented with `src/services/`: one agent per service.
Flat structure: split by feature domain based on file naming.

## Extended Thinking Budget

Use extended thinking proportionally to risk:

- **High risk** (multi-module refactors, merge conflicts, architecture): think deeply
- **Medium risk** (new feature in existing pattern): think briefly
- **Low risk** (single-file edit following existing pattern): skip thinking

The heuristic: if reversing this action requires touching more than 3 files,
think first. Otherwise, act and verify.

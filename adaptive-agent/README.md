# adaptive-agent

A Claude Code plugin that makes every agent session start with codebase reconnaissance
and end with integration verification. Built from Anthropic cookbook patterns.

## What It Does

**Skills** (auto-activate based on context):
- `bootstrap` — Discovers project identity, conventions, extension points, and workflow before any action
- `git-safety` — Preserves untracked files, enforces stash-before-write, ensures clean starting points
- `context-management` — Session compaction, cross-session memory, caching-aware behavior
- `compounding-review` — 6-axis review ensuring new code integrates rather than orphans
- `tool-orchestration` — Parallel execution, evaluator-optimizer loops, structured extraction

**Commands** (explicit invocation):
- `/adaptive-agent:bootstrap` — Full reconnaissance with structured output
- `/adaptive-agent:merge-prs` — Discover PR process, validate, and merge following repo conventions
- `/adaptive-agent:review` — Run compounding review on recent changes or a specific PR
- `/adaptive-agent:safe-branch` — Create a working branch with full git safety

**Agents** (sub-agents for parallel work):
- `codebase-reviewer` — Parallel review scoped to a module
- `pr-merger` — Validates individual PRs in a merge chain

**Hooks**:
- Warns on one-way-door git operations (push, merge, rebase, reset, delete)

## Install

```bash
/plugin marketplace add jadecli/jadecli-plugins
/plugin install adaptive-agent@jadecli-plugins
```

## Philosophy

The agent adapts to the codebase — the codebase never adapts to the agent.
Every pattern here is discovered from the repo it's dropped into, not prescribed.

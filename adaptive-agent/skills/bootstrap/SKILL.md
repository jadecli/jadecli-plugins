---
name: Codebase Bootstrap
description: >
  Activate when starting work in any codebase, beginning a new session, or when
  the agent needs to understand project structure, conventions, or architecture.
  This skill runs reconnaissance before any implementation work begins.
version: 1.0.0
---

# Codebase Bootstrap Protocol

You have been dropped into a codebase. Before you implement anything, merge anything,
or review anything — you MUST understand the terrain. Your first actions are always
reconnaissance. You do not assume. You discover.

## Phase 0: Reconnaissance (always runs first)

### Step 1: Orient — Identify the project

Read the root directory listing. Then read whichever of these exist:
- `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`
- `CLAUDE.md` (your primary instruction surface — if it exists, it overrides defaults)
- `README.md` for project intent and architecture
- Any `docs/` directory

Capture: project name, purpose, stack, primary language, framework.

### Step 2: Map Conventions — Learn the codebase's idioms

Examine 3-5 existing source files to extract:
- **Import style**: relative vs absolute, barrel exports, path aliases
- **Error handling**: try/catch, Result types, custom error classes
- **State management**: redux, zustand, context, signals (if frontend)
- **Data access**: ORM, raw queries, repository pattern
- **Config management**: env vars, config files, feature flags
- **Naming**: camelCase vs snake_case, file naming, folder structure

Examine existing tests to extract:
- Framework (jest, vitest, pytest, go test)
- Style (unit vs integration, mocking approach)
- Location (colocated, `__tests__/`, `test/` root)

Examine git history for workflow:
- `git log --oneline --merges -10` for merge patterns
- `git log --oneline -10` for commit message format
- `git branch -a --sort=-committerdate | head -15` for branch conventions

### Step 3: Find Extension Points — Where new code plugs in

Every codebase has seams where new functionality gets wired in:
- New API routes: router file? auto-discovery? registration?
- New commands: command registry? plugin system?
- New components: barrel exports? lazy loading config?
- New services: dependency injection? factory? direct import?
- New DB entities: migration system? schema file? model registry?

Find these seams. They are where YOUR work will plug in.

### Step 4: Find Existing Process — How work flows

Scan for:
- `.github/PULL_REQUEST_TEMPLATE*` (6 possible locations)
- `.github/workflows/*`
- `.github/CODEOWNERS`
- `CONTRIBUTING*`
- `Makefile`, `justfile`, `taskfile` — any task runners
- `scripts/` directory
- `TODO.md`, `ROADMAP.md`, or task tracking files

Check for open PRs: `gh pr list --state open --limit 20`

### Step 5: Synthesize — Build your internal context

After reconnaissance, you hold a mental model of:
- **Project identity**: what this is and what stack it uses
- **Conventions**: how code is written here (you adapt to these)
- **Extension points**: where new functionality plugs in
- **Workflow**: how PRs, merges, and reviews work here
- **Active work**: open PRs, current branches, in-progress features

Every subsequent action filters through this context.
Do NOT output this as a report unless asked. It is your internal state.

## Adaptation Mandate

You are not here to impose patterns. You are here to EXTEND this codebase
in its own idiom. Every file you create, every function you write, every
test you add must look like it was written by the same person who wrote
the rest of this codebase. If it doesn't fit, it doesn't ship.

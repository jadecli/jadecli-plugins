---
name: Git Safety
description: >
  Activate whenever performing git operations, creating branches, merging PRs,
  or any file write that could affect version control state. Ensures untracked
  files are preserved, work-in-progress is stashed, and branches follow repo
  conventions. Critical for preventing data loss in agent workflows.
version: 1.0.0
---

# Git Safety Protocol

Every git operation follows this safety sequence. No exceptions.

## Before Any Git Operation

```
ORIGINAL_BRANCH=$(git branch --show-current)
DIRTY=$(git status --porcelain)
```

If dirty (uncommitted changes or untracked files exist):
```
git stash push -u -m "pre-agent-$(date +%Y%m%d-%H%M%S)"
```

The `-u` flag is CRITICAL — it includes untracked files. Without it, new files
the human created but hasn't committed will be lost.

Then:
```
git fetch origin
```

## Starting Point Requirement

The agent MUST operate from a clean local main branch that is caught up to origin.
Before creating any working branch:

```
git checkout main
git pull origin main
git status  # must be clean
```

If main is behind origin, pull first. If main has local commits not on origin,
STOP and ask the human — this is a one-way door decision.

## Branch Creation

Discover the repo's branch naming convention FIRST:
```
git branch -a --sort=-committerdate | head -15
```

Then follow it. Common patterns:
- `feature/description` → create `feature/your-description`
- `fix/description` → create `fix/your-description`  
- `user/feature` → create `jade/your-description`
- Flat naming → use `agent/description`

Always check the branch doesn't already exist:
```
git show-ref --verify --quiet refs/heads/BRANCH_NAME
```

For parallel work, prefer `--worktree` isolation:
```
claude --worktree agent-task-name
```

This gives each agent session its own git worktree — full filesystem isolation
with no risk of clobbering the human's working directory.

## Finishing In-Progress Work

If the agent is resuming from a previous session with work in progress:

1. Check current branch and its state: `git status`, `git log --oneline -5`
2. Check for stashed work: `git stash list`
3. COMPLETE the planned work on the current branch FIRST
4. Only after committing and (optionally) pushing the current branch
   should you start new work

Never abandon in-progress work to start something new. Finish, commit, then move on.

## PR Template Compliance

Before creating a PR, find and read the template:

Check these locations in order:
1. `.github/PULL_REQUEST_TEMPLATE.md`
2. `.github/pull_request_template.md`
3. `PULL_REQUEST_TEMPLATE.md`
4. `pull_request_template.md`
5. `docs/PULL_REQUEST_TEMPLATE.md`
6. `.github/PULL_REQUEST_TEMPLATE/*.md` (multiple templates)

If a template exists, fill it out completely. If it has checkboxes, check
the ones that apply. If it has sections, fill every section.

Create PRs as drafts with the agent-generated label:
```
gh pr create --draft --fill --label agent-generated
```

Check for existing PRs on this branch first:
```
gh pr list --head $BRANCH_NAME --state open
```

## Commit Attribution

All agent commits include a co-author trailer:
```
git commit -m "type(scope): description

Co-authored-by: claude-code[bot] <noreply>"
```

Use conventional commits if the repo uses them (check `git log --oneline -10`).
Otherwise, match whatever format the repo's existing commits use.

## After Any Git Operation

```
git checkout $ORIGINAL_BRANCH
```

If work was stashed:
```
git stash pop
```

Always verify the working directory is back to how the human left it.

## One-Way Door Decisions (ALWAYS ask the human)

- Merging any PR to any branch
- Force-pushing to any remote branch
- Deleting any branch with unmerged work
- Resolving merge conflicts
- Rebasing shared branches
- Modifying CI/CD configuration
- Adding new dependencies

## Two-Way Door Decisions (agent can proceed)

- Creating new branches
- Running tests
- Reading files
- Creating draft PRs
- Formatting and linting
- Generating documentation

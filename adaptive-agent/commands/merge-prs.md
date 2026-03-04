---
description: "Discover PR process, validate, and merge PRs following repo conventions"
args:
  - name: targets
    description: "PR numbers to merge (e.g., '#12 #14 #17') or 'all' for all open PRs"
    required: false
---

# Merge PRs

Discover this repo's PR process, validate target PRs, and execute merges
following the established workflow.

## Instructions

### 1. Ensure Clean Starting Point

Before anything else, verify git safety:

```bash
git status          # must be clean
git branch          # note current branch
git fetch origin
git checkout main
git pull origin main
```

If the working directory is dirty, stash with `-u` flag first.
If main is behind origin, pull. If main has local-only commits, STOP and ask.

### 2. Discover PR Process (from bootstrap context)

Reference the bootstrap discovery. If not already bootstrapped, run it now.
Key things needed:

- Merge method (squash/merge/rebase) -- check `git log --oneline --merges -10`
- PR template location
- Required CI checks
- Branch protection rules

### 3. Identify and Order Targets

If specific PR numbers given, fetch their details:

```bash
gh pr view NUMBER --json title,body,baseRefName,headRefName,mergeable,statusCheckRollup
```

If 'all', list open PRs:

```bash
gh pr list --state open --json number,title,headRefName,baseRefName
```

Build dependency order:

- Check if any PR branches off another PR's branch
- Check PR descriptions for "depends on #N" references
- PRs targeting `main` with no dependencies come first

Present the merge plan to the human and WAIT FOR APPROVAL.
Merges are one-way doors.

### 4. Validate Each PR

For each PR in order:

```bash
gh pr view NUMBER --json mergeable,mergeStateStatus,statusCheckRollup
gh pr checks NUMBER
```

Dry-run merge conflict check:

```bash
git checkout main
git merge --no-commit --no-ff origin/PR_BRANCH
git merge --abort
```

If conflicts exist: report them and STOP. Do not auto-resolve.
If CI fails: report and STOP.

### 5. Execute Merge Chain

For each validated PR:

```bash
gh pr merge NUMBER --squash --delete-branch  # or --merge/--rebase per convention
```

After each merge:

```bash
git pull origin main
```

If merging a chain, update next PR's base if needed:

```bash
gh pr edit NEXT_NUMBER --base main
```

Wait for CI on the updated PR before proceeding.

### 6. Post-Merge Verification

```bash
git log --oneline -10
```

Run the repo's test suite (whatever bootstrap discovered).

Report what was merged and the final state.

### 7. Restore Working State

Return to the original branch and pop any stashed work.

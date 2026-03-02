---
description: "Safely create a working branch from clean main, preserving all current work"
args:
  - name: name
    description: "Branch name or task description (will be formatted to match repo conventions)"
    required: true
---

# Safe Branch Creation

Create a working branch with full git safety — stash current work, ensure
main is current, create branch following repo conventions, and set up for work.

## Instructions

1. Record current state:
   ```bash
   ORIGINAL_BRANCH=$(git branch --show-current)
   DIRTY=$(git status --porcelain)
   ```

2. If dirty, stash everything including untracked files:
   ```bash
   git stash push -u -m "pre-agent-$(date +%Y%m%d-%H%M%S)"
   ```

3. Get to clean main:
   ```bash
   git checkout main
   git pull origin main
   ```

4. Determine branch naming from repo convention:
   ```bash
   git branch -a --sort=-committerdate | head -15
   ```
   
   Match the pattern:
   - If repo uses `feature/x` → `feature/{{name}}`
   - If repo uses `fix/x` → keep appropriate prefix
   - If no pattern → `agent/{{name}}`
   
   Format the name: lowercase, kebab-case, no spaces.

5. Verify branch doesn't exist:
   ```bash
   git show-ref --verify --quiet refs/heads/BRANCH_NAME && echo "EXISTS" || echo "SAFE"
   ```

6. Create and checkout:
   ```bash
   git checkout -b BRANCH_NAME
   ```

7. Confirm ready state:
   ```bash
   echo "Created branch: BRANCH_NAME"
   echo "Base: main @ $(git rev-parse --short HEAD)"
   echo "Original branch: $ORIGINAL_BRANCH"
   echo "Stashed work: [yes/no]"
   echo "Ready to work."
   ```

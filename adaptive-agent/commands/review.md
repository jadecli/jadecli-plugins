---
description: "Run the 6-axis compounding review on recent changes or a specific PR"
args:
  - name: target
    description: "PR number, branch name, or 'HEAD' for most recent commit"
    required: false
    default: "HEAD"
---

# Compounding Review

Run the full 6-axis compounding review on the specified target.

## Instructions

### 1. Identify What Changed

If target is a PR number:
```bash
gh pr diff NUMBER --name-only
gh pr view NUMBER --json files
```

If target is a branch:
```bash
git diff main...BRANCH --name-only
```

If target is HEAD:
```bash
git diff HEAD~1 --name-only
```

### 2. Run All Six Axes

For EACH changed file, run the compounding review skill axes in parallel
where possible. Use sub-agents for independent analysis:

**Agent 1**: Architecture Fit + Extends Don't Duplicate
- Read 3 adjacent files for pattern comparison
- Grep for similar utilities/functions in the codebase

**Agent 2**: Reachable and Wired + Tested in Kind
- Trace imports/registrations for new exports
- Check for corresponding test files

**Agent 3**: Enables Next Work + Roadmap Connected
- Assess interface clarity and extensibility
- Cross-reference with TODO.md/ROADMAP.md/CLAUDE.md

### 3. Synthesize and Verdict

Combine all agent results into the structured review report.
Apply verdict logic:
- All pass → SHIP
- 1-2 soft-fails → REVISE with specific action items
- Any hard-fail → BLOCK with explanation
- "Reachable and Wired" fails → ALWAYS BLOCK

Output the report in the repo's documentation format.

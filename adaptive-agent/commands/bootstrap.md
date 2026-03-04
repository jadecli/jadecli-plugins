---
description: "Run full codebase reconnaissance and output the discovery summary"
---

# Codebase Bootstrap

Run the full bootstrap protocol and output the results as a structured summary.

## Instructions

1. Execute every step of the bootstrap skill (orient, map conventions, find extension
   points, find existing process)

2. Output the results in a structured format:

   ```text
   ## Project Identity
   - Name: [project name]
   - Stack: [language, framework, key dependencies]
   - Purpose: [one-line description]

   ## Conventions
   - Import style: [relative/absolute/barrel/aliases]
   - Error handling: [pattern]
   - Naming: [camelCase/snake_case/etc]
   - Test framework: [jest/vitest/pytest/etc]
   - Test location: [colocated/__tests__/test/]

   ## Extension Points
   - New routes: [how they're wired]
   - New components: [how they're registered]
   - New services: [how they're connected]
   - Config: [how it's managed]

   ## Workflow
   - Branch convention: [pattern]
   - Commit format: [conventional/free-form/etc]
   - Merge method: [squash/merge/rebase]
   - PR template: [exists/missing]
   - CI checks: [list]

   ## Active Work
   - Open PRs: [count and titles]
   - Active branches: [list]
   - Current priorities: [from CLAUDE.md/TODO.md/ROADMAP.md]
   ```

3. After outputting the summary, store it as your internal context for all
   subsequent operations in this session.

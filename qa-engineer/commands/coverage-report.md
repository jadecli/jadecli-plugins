---
description: "Generate test coverage report and flag files below threshold"
args:
  - name: threshold
    description: "Minimum coverage percentage (default: 80)"
    required: false
    default: "80"
---

# Coverage Report

Generate a test coverage report and identify under-covered files.

## Instructions

### 1. Run Coverage

```bash
npx vitest run --coverage 2>&1
```

### 2. Parse Coverage Output

Extract per-file coverage percentages:

- Statements
- Branches
- Functions
- Lines

### 3. Flag Under-Covered Files

Any file below the threshold (default 80%) is flagged:

```text
Coverage Report
===============
Threshold: 80%

File                          Stmts  Branch  Funcs  Lines  Status
lib/auth.ts                   92%    85%     100%   90%    PASS
lib/feed.ts                   78%    72%     80%    76%    FAIL
app/api/v1/webhooks/route.ts  65%    50%     60%    62%    FAIL
```

### 4. Summary

- Total files analyzed
- Files above threshold
- Files below threshold
- Overall coverage percentage
- Recommendation: which files need the most test attention

---
description: "Run the full test suite and report results"
args: []
---

# Test Suite

Run the full test suite and report pass/fail results.

## Instructions

### 1. Run Tests

```bash
npm test 2>&1
```

### 2. Parse Results

Extract from Vitest output:

- Total test count
- Passed count
- Failed count
- Skipped count
- Duration

### 3. Report Failures

For each failed test, report:

- Test file path
- Test name (describe + it)
- Error message
- Line number if available

### 4. Output

```text
Test Suite Results
==================
Total:   299
Passed:  297
Failed:  2
Skipped: 0
Duration: 12.3s

Failures:
---------
tests/auth.test.ts:45
  authenticate > should return 401 for expired key
  Error: expected 401 but received 200

tests/webhooks.test.ts:112
  webhook dispatch > should retry on 5xx
  Error: timeout after 30000ms
```

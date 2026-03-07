---
description: "Check API health by hitting key endpoints"
args:
  - name: base-url
    description: "Base URL (default: http://localhost:3000)"
    required: false
    default: "http://localhost:3000"
---

# Health Check

Hit key API endpoints and verify they return 200 responses.

## Instructions

### 1. Test Endpoints

Test each endpoint in parallel:

```bash
curl -s -o /dev/null -w "%{http_code}" <base-url>/api/v1/feed
curl -s -o /dev/null -w "%{http_code}" <base-url>/api/v1/stats
curl -s -o /dev/null -w "%{http_code}" <base-url>/api/v1/vendors
```

### 2. Report

Output a status table:

| Endpoint | Status | Result |
|---|---|---|
| /api/v1/feed | 200 | OK |
| /api/v1/stats | 200 | OK |
| /api/v1/vendors | 200 | OK |

Mark any non-200 response as FAIL with the actual status code.

### 3. Summary

- Total endpoints checked
- Passed count
- Failed count
- Overall: HEALTHY or DEGRADED

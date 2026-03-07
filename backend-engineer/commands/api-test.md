---
description: "Test an API endpoint with curl and verify the response"
args:
  - name: endpoint
    description: "API endpoint path (e.g., /api/v1/feed)"
    required: true
  - name: base-url
    description: "Base URL (default: http://localhost:3000)"
    required: false
    default: "http://localhost:3000"
  - name: method
    description: "HTTP method (default: GET)"
    required: false
    default: "GET"
---

# API Test

Test an API endpoint and verify the response shape and status code.

## Instructions

### 1. Send Request

```bash
curl -s -w "\n%{http_code}" -X <method> <base-url><endpoint>
```

If an API key is needed, include it:

```bash
curl -s -w "\n%{http_code}" -X <method> \
  -H "Authorization: Bearer <key>" \
  <base-url><endpoint>
```

### 2. Verify Response Shape

Check that the response matches the expected shape:

```json
{
  "data": "...",
  "error": null,
  "meta": {}
}
```

### 3. Report

Output:

- HTTP status code
- Response time
- Response body (truncated if large)
- Shape validation: PASS/FAIL
  - Has `data` key
  - Has `error` key
  - Has `meta` key
- Content-Type header check (should be `application/json`)

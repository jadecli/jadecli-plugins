---
description: "Test integration endpoints: MCP connections, webhooks, cron jobs"
args:
  - name: target
    description: "What to test: 'mcp', 'webhooks', 'cron', or 'all' (default: all)"
    required: false
    default: "all"
---

# Integration Test

Verify integration endpoints are functional.

## Instructions

### 1. MCP Connection Test

Verify MCP server responds:

```bash
# Test stdio transport
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | \
  npx -y @modelcontextprotocol/inspector

# Test HTTP transport (if available)
curl -s http://localhost:3000/api/mcp
```

### 2. Webhook Delivery Test

Verify webhook dispatch works:

```sql
SELECT
  w.id,
  w.url,
  w.status,
  w.last_delivery_at,
  w.last_status_code
FROM webhooks w
WHERE w.status = 'active'
LIMIT 5;
```

Check recent delivery attempts for failures.

### 3. Cron Job Test

Verify recent cron executions:

```sql
SELECT
  cr.job_name,
  cr.status,
  cr.started_at,
  cr.completed_at,
  cr.summary->>'duration_ms' AS duration_ms,
  cr.error
FROM cron_runs cr
ORDER BY cr.started_at DESC
LIMIT 10;
```

### 4. Report

| Integration | Status | Details |
|---|---|---|
| MCP (stdio) | OK/FAIL | Response or error |
| MCP (HTTP) | OK/FAIL | Response or error |
| Webhooks | OK/FAIL | Active count, recent failures |
| Cron | OK/FAIL | Last run status, any errors |

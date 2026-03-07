---
name: Integration Patterns
description: >
  Activate when designing or implementing integrations between services.
  Covers MCP integrations, webhook dispatch, cron-based batch processing,
  and external API communication patterns.
version: 1.0.0
---

# Integration Patterns at jadecli

## MCP (Model Context Protocol)

Primary integration mechanism for tool-based interactions.

### Available MCP Integrations

| Integration | Purpose |
|---|---|
| jade-pm MCP | Project management commands (/challenge, /intake, /retro) |
| Neon MCP | Direct database access (SQL queries, branch management) |
| Slack MCP | Team communication and notifications |
| llms-txt-feed MCP | 8 tools for feed data access (dual transport: stdio + HTTP) |

### MCP Conventions

- All tools return typed responses
- Error responses include actionable error messages
- Tools are tier-gated (free/starter/pro)
- HTTP transport uses SSE for streaming responses

## Webhook Dispatch (Pro Tier)

Event-driven outbound notifications:

- Signed with HMAC-SHA256 (`X-Webhook-Signature` header)
- Delivery tracked in `webhooks` table
- Retry with exponential backoff (3 attempts: 0s, 60s, 300s)
- Payload includes event type, timestamp, and typed data

## Cron-Based Batch Processing

Scheduled work via Vercel cron:

```text
cron/fetch    -> Fetch vendor llms.txt files
cron/analyze  -> Run intelligence analysis
cron/reporting -> Generate reporting aggregations
```

Jobs tracked in `cron_runs` table with status lifecycle:
`running` -> `completed` | `failed`

## External API Communication

- Always use typed interfaces for request/response payloads
- Retry with exponential backoff for transient failures
- Circuit breaker pattern for repeated failures
- Timeout: 30s for external calls, 10s for internal
- Log all external API calls with request ID for tracing

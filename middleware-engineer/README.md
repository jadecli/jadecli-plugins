# middleware-engineer

Middleware engineering plugin for integration patterns, message queues, and
API gateway conventions. Covers MCP integrations, webhook dispatch, and
cron-based batch processing.

Builds on top of `jadecli-engineer-base` (Neon, cron, table creation, Vercel deploy).

## Skills (auto-activate)

- `integration-patterns` -- MCP integrations, webhook dispatch, cron-based batch processing
- `message-queues` -- Cron-based queue patterns, idempotent job design, deduplication
- `api-gateway` -- Tier-based feature gating, rate limiting, webhook verification

## Commands

- `/middleware-engineer:trace` -- Trace a request through the system lifecycle
- `/middleware-engineer:integration-test` -- Test MCP connections, webhooks, and cron jobs

## Install

```bash
claude --plugin-dir ./middleware-engineer
```

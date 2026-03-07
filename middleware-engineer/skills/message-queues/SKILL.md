---
name: Message Queues
description: >
  Activate when implementing or reviewing job scheduling, task chaining,
  or background processing. Covers the cron-based queue pattern, idempotent
  job design, and deduplication.
version: 1.0.0
---

# Message Queue Patterns

jadecli uses a cron-based approach instead of dedicated message queue
infrastructure. Vercel cron provides the scheduling backbone.

## Job Tracking: cron_runs Table

```sql
CREATE TABLE cron_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  job_name TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'running',  -- running | completed | failed
  started_at TIMESTAMPTZ DEFAULT now(),
  completed_at TIMESTAMPTZ,
  summary JSONB,
  error TEXT
);
```

## Job Chaining

Jobs execute in sequence via separate cron triggers:

```
cron/fetch     (every 6h)  -> Fetch all vendor files
cron/analyze   (every 6h, offset 30m) -> Analyze fetched changes
cron/reporting (daily)     -> Aggregate into reporting tables
```

Each job checks for prerequisites before executing. `cron/analyze` verifies
a recent `cron/fetch` completed successfully.

## Idempotent Job Design

All jobs MUST be safe to retry:

- Check for existing `running` status before starting (deduplication)
- Use `INSERT ... ON CONFLICT` for upsert operations
- Track processed items to avoid double-processing
- Wrap state mutations in transactions

### Deduplication Check

```sql
SELECT id FROM cron_runs
WHERE job_name = $1
  AND status = 'running'
  AND started_at > now() - interval '1 hour';
```

If a running job exists, skip execution (previous run still in progress).

## Summary JSONB

Each completed job writes a structured summary:

```json
{
  "vendors_processed": 135,
  "changes_detected": 12,
  "errors": [],
  "duration_ms": 4523
}
```

This enables monitoring and alerting on job outcomes without parsing logs.

## Status Transitions

```
(start) -> running
running -> completed  (success path)
running -> failed     (error path)
```

Never transition from `completed` or `failed` -- create a new run instead.

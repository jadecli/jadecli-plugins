---
description: "Trace a request through the system lifecycle"
args:
  - name: identifier
    description: "API key prefix, request ID, or key_id to trace"
    required: true
---

# Request Trace

Trace a request through the system by querying request_log and cron_runs.

## Instructions

### 1. Find Request Log Entries

```sql
SELECT
  rl.id,
  rl.key_id,
  rl.endpoint,
  rl.method,
  rl.status_code,
  rl.created_at
FROM request_log rl
WHERE rl.key_id::text LIKE '<identifier>%'
   OR rl.id::text LIKE '<identifier>%'
ORDER BY rl.created_at DESC
LIMIT 20;
```

### 2. Find Related Cron Runs

If the request triggered a cron job (e.g., webhook dispatch):

```sql
SELECT
  cr.id,
  cr.job_name,
  cr.status,
  cr.started_at,
  cr.completed_at,
  cr.summary,
  cr.error
FROM cron_runs cr
WHERE cr.started_at >= (
  SELECT created_at - interval '1 minute'
  FROM request_log
  WHERE id::text LIKE '<identifier>%'
  LIMIT 1
)
ORDER BY cr.started_at DESC
LIMIT 10;
```

### 3. Output

Display the request lifecycle:

```text
Request -> Auth -> Rate Check -> Handler -> Response -> Log
                                    |
                                    +-> Cron Job (if triggered)
```

Include timestamps, status codes, and any errors at each stage.

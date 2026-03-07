---
description: "Check cron job health by querying the cron_runs table"
---

# Cron Status

Check the health of all cron jobs by querying the `cron_runs` table.

## Instructions

1. Run the following query using Neon MCP `run_sql`:

```sql
SELECT
  job_name,
  started_at,
  finished_at,
  status,
  summary,
  error
FROM cron_runs
ORDER BY started_at DESC
LIMIT 25;
```

1. Group results by job_name, showing the last 5 runs per job.

2. Format as a table per job:

```text
### Job: <job_name>

| # | Started             | Finished            | Status    | Summary         | Error |
|---|---------------------|---------------------|-----------|-----------------|-------|
| 1 | 2026-03-04 06:00 UTC| 2026-03-04 06:01 UTC| completed | Processed 12... |       |
```

3. Highlight any `failed` runs with the error message.

4. If no cron_runs exist, report that no cron executions have been logged.

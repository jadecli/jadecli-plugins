---
description: "Query and display the current user's recent tasks from the reporting.worker_tasks table"
---

# My Tasks

Query `reporting.worker_tasks` for the current user's tasks and display them.

## Instructions

1. Determine the current worker email from session context.

2. Run the following query using Neon MCP `run_sql`:

```sql
SELECT
  task_summary,
  task_type,
  artifacts,
  started_at,
  completed_at
FROM reporting.worker_tasks
WHERE worker_email = $1
ORDER BY completed_at DESC
LIMIT 20;
```

1. Format the results as a table:

```text
| # | Type   | Summary              | Artifacts | Completed           |
|---|--------|----------------------|-----------|---------------------|
| 1 | create | Built new plugin ... | PR #42    | 2026-03-04 10:30 UTC|
```

1. If no tasks found, report that no tasks are logged for this worker yet.

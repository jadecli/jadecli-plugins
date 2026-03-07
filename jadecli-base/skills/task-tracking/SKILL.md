---
name: Task Tracking
description: >
  Activate on task completion. Logs completed tasks to the reporting.worker_tasks
  table in Neon. Every meaningful unit of work gets recorded for visibility and
  accountability across the org.
version: 1.0.0
---

# Task Tracking

When you complete a task, log it to the `reporting.worker_tasks` table using the Neon MCP `run_sql` tool.

## When to Log

Log a task when you have completed a discrete unit of work: a PR merged, a query answered, a deploy executed, a bug fixed, a file created, a review submitted. Do NOT log trivial actions like reading a file or listing a directory.

## Required Fields

- **worker_email**: The current user's email from session context (e.g., alex@jadecli.com)
- **worker_role**: The role from the plugin stack (e.g., data, analytical-engineer, frontend-engineer, sales, design, marketing)
- **task_summary**: Concise description of what was done (1-2 sentences max)
- **task_type**: One of: `query`, `report`, `deploy`, `review`, `fix`, `create`
- **artifacts**: JSON array of `{type, ref}` objects (e.g., PR links, file paths, deploy URLs)
- **started_at**: Timestamp when the task began
- **completed_at**: Timestamp when the task finished
- **session_id**: Current Claude session ID

## INSERT Template

```sql
INSERT INTO reporting.worker_tasks (
  worker_email,
  worker_role,
  task_summary,
  task_type,
  artifacts,
  started_at,
  completed_at,
  session_id
) VALUES (
  $1,  -- worker_email (text)
  $2,  -- worker_role (text)
  $3,  -- task_summary (text)
  $4,  -- task_type (text: query|report|deploy|review|fix|create)
  $5,  -- artifacts (jsonb: [{"type": "pr", "ref": "https://..."}])
  $6,  -- started_at (timestamptz)
  $7,  -- completed_at (timestamptz)
  $8   -- session_id (text)
);
```

## Execution

Use the Neon MCP `run_sql` tool to execute the INSERT. Do not use psql or any other method.

## Artifact Types

Common artifact type values:

- `pr` -- Pull request URL
- `file` -- File path created or modified
- `deploy` -- Deploy URL
- `query` -- SQL query or data output
- `report` -- Report file or output
- `branch` -- Git branch name

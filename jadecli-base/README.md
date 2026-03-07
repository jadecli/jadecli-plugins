# jadecli-base

Base plugin for all jadecli workers. Provides task tracking, session management, and org conventions that every worker in the organization inherits.

## Skills

- **task-tracking** -- Logs completed tasks to `reporting.worker_tasks` in Neon. Records worker identity, task type, artifacts, and timestamps for org-wide visibility.
- **session-management** -- Announces worker role on session start, retrieves pending handoff context, and generates handoff notes on session end for cross-session continuity.
- **org-conventions** -- Enforces jadecli standards: conventional commits, PR workflow (branch/squash-merge), actor taxonomy, and team roster.

## Commands

- `/jadecli-base:my-tasks` -- Query and display recent tasks for the current worker.
- `/jadecli-base:handoff` -- Generate a structured handoff document for the next session.

## Install

```bash
/plugin install jadecli-base@jadecli-plugins
```

## MCP Dependencies

- Neon MCP (`https://mcp.neon.tech/mcp`) -- Used for task logging and retrieval via `run_sql`.

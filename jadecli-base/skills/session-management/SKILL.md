---
name: Session Management
description: >
  Activate at session start and session end. Manages worker identity announcement,
  handoff context retrieval, session summarization, and handoff note generation
  for cross-session continuity.
version: 1.0.0
---

# Session Management

## On Session Start

1. **Announce worker role**: State the active worker email and role(s) derived from the plugin stack and session context.
2. **Check for pending handoff**: Query `reporting.worker_tasks` for the most recent task with a handoff artifact for this worker. If found, surface the handoff note so the session begins with full context of prior work.

```sql
SELECT task_summary, artifacts
FROM reporting.worker_tasks
WHERE worker_email = $1
  AND artifacts::text LIKE '%handoff%'
ORDER BY completed_at DESC
LIMIT 1;
```

1. **Resume or start fresh**: If a handoff note exists, acknowledge pending items and continue from where the last session left off. If none exists, proceed normally.

## On Session End

1. **Summarize accomplishments**: List what was completed during this session.
2. **Identify pending work**: Note anything started but not finished, decisions deferred, or blockers encountered.
3. **Generate handoff note**: Produce a structured handoff that the next session can consume. Include:
   - What was done (completed tasks)
   - What's pending (unfinished work)
   - Key decisions made
   - Open questions or blockers
4. **Store as artifact**: Log the handoff note as a task with artifact type `handoff` using the task tracking skill.

## Handoff Note Format

```text
## Handoff -- [worker_email] -- [date]

### Completed
- [task 1]
- [task 2]

### Pending
- [item 1]: [status/context]
- [item 2]: [status/context]

### Decisions
- [decision]: [rationale]

### Open Questions
- [question 1]
- [question 2]
```

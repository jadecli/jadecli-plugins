---
description: "Generate a context handoff document for the next session"
---

# Handoff

Generate a structured handoff document capturing the current session's state for continuity.

## Instructions

1. Review the current session's activity: tasks completed, files modified, decisions made.

2. Compile the handoff document:

```text
## Handoff -- [worker_email] -- [date]

### Completed
- [completed task 1]
- [completed task 2]

### Pending
- [pending item]: [status and context]

### Decisions
- [decision]: [rationale]

### Open Questions
- [question or blocker]
```

1. Log the handoff as a task using the task tracking skill:
   - task_type: `report`
   - task_summary: "Session handoff note"
   - artifacts: `[{"type": "handoff", "ref": "<handoff content or summary>"}]`

2. Output the handoff document so the user can review it.

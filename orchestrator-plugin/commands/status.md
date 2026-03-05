---
name: status
description: Check orchestrator mission status and recent runs
---

# /orchestrator:status

Show status of recent orchestrator mission runs.

## Usage

```
/orchestrator:status
```

## Behavior

1. Scan `orchestrator-plugin/artifacts/` for mission run directories
2. Read `run.json` from the most recent runs (up to 5)
3. Display for each:
   - Mission name and objective
   - Status (running/completed/failed/aborted)
   - Duration
   - Artifact count
   - Artifact directory path

## Output format

```
Recent orchestrator runs:

  research / "Compare React vs Astro"
    Status: completed | Duration: 45s | Artifacts: 4
    Path: artifacts/research/2026-03-05T10-30-00/

  code-review / "Review auth module"
    Status: failed | Duration: 12s | Error: Budget exceeded
    Path: artifacts/code-review/2026-03-05T09-15-00/
```

If no runs found, display: "No orchestrator runs found. Use /orchestrator:run to start one."

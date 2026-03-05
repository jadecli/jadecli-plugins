---
name: run
description: Run an orchestrator mission
---

# /orchestrator:run

Execute a multi-agent mission with the orchestrator.

## Usage

```
/orchestrator:run <mission> "<objective>" [--dry-run] [--budget N] [--tier T]
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `mission` | Yes | Mission name (e.g., `research`, `code-review`, `build-app`) |
| `objective` | Yes (unless --dry-run) | What the mission should accomplish |
| `--dry-run` | No | Validate and show plan without API calls |
| `--budget N` | No | Maximum spend cap in USD |
| `--tier T` | No | Override complexity tier (simple/moderate/complex) |

## Examples

```bash
# Research a topic
/orchestrator:run research "Compare React Server Components vs Astro Islands"

# Dry run to see the plan
/orchestrator:run research "AI agent patterns" --dry-run

# Code review with budget cap
/orchestrator:run code-review "Review the auth module" --budget 0.50

# Build an app
/orchestrator:run build-app "CSV to JSON converter CLI tool"
```

## Behavior

1. Load and validate the mission YAML file
2. Build the orchestration plan (lead prompt, worker definitions)
3. Show cost estimate
4. If `--dry-run`: print plan and exit
5. If `--budget`: warn if estimated cost exceeds budget
6. Create artifact directory at `artifacts/{mission}/{timestamp}/`
7. Execute the lead agent via Claude Agent SDK `query()`
8. Lead agent spawns workers, collects artifacts, synthesizes SUMMARY.md
9. Write `run.json` with execution metadata
10. Report results

## Output

All artifacts are written to `orchestrator-plugin/artifacts/{mission}/{timestamp}/`:
- `SUMMARY.md` -- synthesized final output
- Worker artifacts (e.g., `investigator-1-findings.md`)
- `run.json` -- execution log with timing and status

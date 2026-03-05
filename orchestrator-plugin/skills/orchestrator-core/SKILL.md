---
name: orchestrator-core
description: Teaches the orchestrator pattern for multi-agent mission execution
---

# Orchestrator Core

The orchestrator plugin runs declarative YAML missions that define how a lead
agent decomposes work, spawns worker agents, and synthesizes results.

## Architecture

```
Lead Agent (Opus)
  reads mission YAML -> assesses complexity -> selects scaling tier
  decomposes objective -> spawns N Worker Agents (Sonnet/Haiku)
  each worker writes artifacts to filesystem
  lead synthesizes worker artifacts into final output
```

## Key concepts

- **Mission files** define the collaboration framework in YAML
- **Scaling rules** are embedded in the mission -- the lead self-selects tier
- **Workers write files, return paths** -- lightweight references, not full content
- **Tools are allow-listed per role** -- workers only access what they need
- **Flat delegation** -- one lead, N workers (no nested subagents)

## Running a mission

```bash
# Dry run (validate + show plan, no API calls)
/orchestrator:run research "topic" --dry-run

# Live run
/orchestrator:run research "topic"

# List available missions
/orchestrator:missions
```

## Mission patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| parallel | All workers run concurrently | Research: parallel investigation |
| sequential | Workers run in order, each sees prior outputs | Code review: sequential analysis |
| pipeline | Chain of transformations | Build: scaffold -> implement -> test |

## Artifacts

All outputs land in `artifacts/{mission_name}/{timestamp}/`:
- `SUMMARY.md` -- lead's synthesized output (the index file)
- `{role}-{n}-findings.md` -- individual worker outputs
- `run.json` -- execution metadata (cost, timing, usage)

## Cost management

Every dry-run shows a cost estimate. Use `--budget` to cap spend:

```bash
# Cap at $0.50
/orchestrator:run research "topic" --budget 0.50
```

Model costs (per 1M tokens):
| Model | Input | Output |
|-------|-------|--------|
| Opus (claude-opus-4-6) | $5.00 | $25.00 |
| Sonnet (claude-sonnet-4-6) | $3.00 | $15.00 |
| Haiku (claude-haiku-4-5) | $1.00 | $5.00 |

## Error recovery

- **SIGINT** -- Ctrl+C gracefully aborts, writes partial `run.json`
- **Budget exceeded** -- stops before starting if estimate exceeds cap
- **Worker failure** -- logged in `run.json`, lead continues with available results
- **Schema validation** -- `--dry-run` catches YAML errors before any API calls

Post-run evaluation checks:
- Index file (SUMMARY.md) exists and has content
- Worker artifacts contain required sections
- Evaluation criteria are noted in the report

## Creating new missions

Copy `missions/_schema.yaml` and modify. Key decisions:
1. Choose a pattern (parallel/sequential/pipeline)
2. Define scaling tiers
3. Specify worker roles with tools and constraints
4. Set artifact schema for structured outputs

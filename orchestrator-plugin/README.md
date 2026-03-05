# Orchestrator Plugin

Composable multi-agent orchestrator for jadecli-plugins. Uses declarative YAML
mission files to define how a lead agent decomposes work, spawns worker agents,
and synthesizes results through a filesystem artifact system.

## Quick start

```bash
# Dry-run a mission (no API calls)
cd sdk && npm install && npx tsx src/orchestrator.ts --mission research --dry-run

# Run a mission
/orchestrator:run research "Your research topic"

# List available missions
/orchestrator:missions

# Check status
/orchestrator:status
```

## Mission types

| Mission | Pattern | Description |
|---------|---------|-------------|
| `research` | Parallel fan-out | Decomposes questions into parallel investigations, synthesizes findings |
| `code-review` | Parallel scoped | Parallel code review across multiple dimensions |
| `build-app` | Sequential pipeline | Scaffold, implement, test pipeline |

## Architecture

```
Lead Agent (Opus)
  ├── reads mission YAML
  ├── assesses complexity → selects scaling tier
  ├── spawns N Worker Agents (Sonnet/Haiku)
  │     └── each writes artifacts to filesystem
  └── synthesizes worker artifacts into final output
```

## Plugin structure

```
orchestrator-plugin/
  .claude-plugin/plugin.json    # plugin metadata
  missions/                     # declarative mission definitions
  artifacts/                    # runtime output (gitignored)
  skills/                       # auto-activated knowledge
  commands/                     # user-invoked via /orchestrator:*
  agents/                       # sub-agent personas
  sdk/                          # TypeScript Agent SDK runtime
```

## SDK flags

| Flag | Description |
|------|-------------|
| `--mission <name>` | Mission to run (required) |
| `--dry-run` | Parse and validate without API calls |
| `--budget <usd>` | Maximum spend cap |
| `--tier <simple\|moderate\|complex>` | Override auto-detected complexity |

## Creating custom missions

See `missions/_schema.yaml` for the annotated mission file reference, or use
the `mission-authoring` skill for guided creation.

---
name: mission-authoring
description: Teaches how to create custom orchestrator mission YAML files
---

# Mission Authoring

This skill guides you through creating custom mission files for the orchestrator plugin.

## Quick start

1. Copy `missions/_schema.yaml` as your starting point
2. Choose a pattern (parallel/sequential/pipeline)
3. Define worker roles
4. Test with `--dry-run`

## Mission file anatomy

```yaml
name: my-mission          # unique identifier
description: What it does  # human-readable
pattern: parallel          # parallel | sequential | pipeline

scaling:                   # optional: complexity tiers
  simple: { agents: 1, max_tool_calls: 10 }
  moderate: { agents: 3, max_tool_calls: 15 }

lead:                      # the orchestrating agent
  model: opus
  strategy: |              # multi-line instructions
    1. Step one
    2. Step two
  tools: [Read, Glob]

workers:                   # roles the lead can spawn
  researcher:
    model: sonnet
    count: dynamic         # or a fixed number
    tools: [Read, WebSearch]
    artifact_schema:
      format: markdown
      required_sections: [findings, sources]
    constraints:
      - "Stay within scope"
```

## Pattern selection guide

| Pattern | Use when | Example |
|---------|----------|---------|
| parallel | Tasks are independent | Research: each worker investigates a sub-question |
| sequential | Each step depends on the previous | Code review: read -> analyze -> report |
| pipeline | Output transforms through stages | Build: design -> implement -> test |

## Worker design principles

1. **Bounded scope** -- each worker has a clear, limited task
2. **File-based output** -- workers write to artifacts, return paths
3. **Tool restrictions** -- only give tools the worker actually needs
4. **Constraints are prompts** -- written into the worker's system prompt

## Scaling tiers

The lead agent reads scaling rules and self-selects based on objective complexity.
Define tiers that make sense for your mission:

- `simple`: quick tasks, 1-2 workers
- `moderate`: typical complexity, 3-5 workers
- `complex`: large scope, 5+ workers

## Testing

```bash
# Validate schema without API calls
bash orchestrator-plugin/sdk/bin/run.sh --mission my-mission --dry-run

# Check the orchestration plan
bash orchestrator-plugin/sdk/bin/run.sh --mission my-mission --dry-run "test objective"
```

## Common mistakes

- Forgetting `pattern` field (defaults to parallel)
- Setting `count` as string instead of number or "dynamic"
- Not specifying `required_sections` in artifact_schema
- Giving workers too many tools (increases cost, reduces focus)
- Not testing with `--dry-run` before live execution

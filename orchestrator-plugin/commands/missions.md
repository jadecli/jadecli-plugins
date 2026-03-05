---
name: missions
description: List available orchestrator missions
---

# /orchestrator:missions

List all available mission types and their descriptions.

## Behavior

1. Read all `.yaml` files from `orchestrator-plugin/missions/` (skip files starting with `_`)
2. For each mission, display:
   - Name
   - Description
   - Pattern (parallel/sequential/pipeline)
   - Worker roles
   - Scaling tiers (if defined)

## Implementation

Run the SDK CLI:

```bash
bash orchestrator-plugin/sdk/bin/run.sh --list
```

Or read missions directly:
1. Glob `orchestrator-plugin/missions/*.yaml` (excluding `_schema.yaml`)
2. Parse each YAML file
3. Display name, description, pattern, and worker roles

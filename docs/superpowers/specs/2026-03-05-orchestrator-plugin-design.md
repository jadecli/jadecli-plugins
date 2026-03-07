# Orchestrator Plugin Design

## Overview

A composable multi-agent orchestrator plugin for jadecli-plugins that uses the
Claude Agent SDK (Python) for programmatic control. Pluggable "mission types"
(research, code ops, full-stack build) are defined as declarative YAML files
that specify how the lead agent decomposes work, what subagents it spawns, and
how artifacts flow.

## Approach

**Mission-file driven (Approach A)** -- selected over code-first SDK and hybrid
approaches. New mission types require only a YAML file, no code changes.
Architecture designed so a hybrid approach (mission files + SDK escape hatches)
is a natural evolution if needed.

## Research basis

Patterns drawn from Anthropic's published engineering:

- **Building Effective Agents** -- five composable workflow patterns, tool design
  principles, simplicity-first decision framework
- **Multi-Agent Research System** -- Opus lead + Sonnet workers, filesystem
  artifact system, scaling rules in prompts, 15x token cost
- **Effective Harnesses for Long-Running Agents** -- initializer + coding agent,
  progress files, git-based context recovery
- **Context Engineering** -- progressive disclosure, just-in-time loading,
  compaction + memory tools
- **Agent Skills standard** -- three-level progressive disclosure (metadata,
  full content, bundled files)

## Plugin structure

```text
orchestrator-plugin/
  .claude-plugin/
    plugin.json              # name: "orchestrator", version: "0.1.0"
  missions/                  # declarative mission definitions
    research.yaml
    code-review.yaml
    build-app.yaml
  artifacts/                 # gitignored runtime output directory
  skills/
    orchestrator-core/
      SKILL.md               # teaches Claude the orchestrator pattern
  commands/
    run.md                   # /orchestrator:run <mission> [objective]
    status.md                # /orchestrator:status -- check running mission
    missions.md              # /orchestrator:missions -- list available missions
  agents/
    lead.md                  # lead agent persona (Opus-tier reasoning)
    worker.md                # worker agent persona (Sonnet-tier execution)
  sdk/                       # Agent SDK runtime (Python)
    orchestrator.py          # main entry point -- parses mission, spawns agents
    mission_loader.py        # YAML parser + validation
    artifact_store.py        # filesystem artifact read/write
    requirements.txt         # claude-agent-sdk, pyyaml
  README.md
```

## Mission file schema

A mission file defines the collaboration framework -- not rigid instructions.
Matches Anthropic's finding that the best multi-agent prompts define "division
of labor, problem-solving approaches, and effort budgets."

```yaml
# missions/research.yaml
name: research
description: Decompose a question into parallel investigations, synthesize findings

scaling:
  simple: { agents: 1, max_tool_calls: 10 }
  moderate: { agents: 3, max_tool_calls: 15 }
  complex: { agents: 8, max_tool_calls: 25 }

lead:
  model: opus
  strategy: |
    1. Assess complexity (simple/moderate/complex)
    2. Decompose objective into independent sub-questions
    3. Assign each sub-question to a worker with clear boundaries
    4. Synthesize worker artifacts into final report
  tools: [web_search, web_fetch, read, glob, grep]

workers:
  investigator:
    model: sonnet
    count: dynamic
    tools: [web_search, web_fetch, read, glob, grep]
    artifact_schema:
      format: markdown
      required_sections: [findings, sources, confidence]
    constraints:
      - "Write findings to artifact file, return only the file path"
      - "Stay within assigned sub-question boundaries"

artifacts:
  directory: artifacts/{mission_name}/{timestamp}
  index: SUMMARY.md
  worker_prefix: "{role}-{n}"

evaluation:
  method: lead_synthesis
  criteria:
    - factual_accuracy
    - source_quality
    - completeness
```

### Key design decisions

- **Scaling rules embedded in the file** -- lead reads them, self-selects
  complexity tier
- **Artifact schema per worker role** -- structured output without rigid code
- **Workers write files, return paths** -- matches Anthropic's "lightweight
  references, not full content" pattern
- **Tools are allow-listed per role** -- workers cannot do things outside their
  scope

## Status

Design approved through Section 2 (mission file schema). Remaining sections
(SDK runtime, artifact store, evaluation, error handling, testing) pending
detailed planning.

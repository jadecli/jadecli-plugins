---
name: Tool Orchestration
description: >
  Activate when performing complex multi-tool operations, parallel analysis
  across modules, or structured data extraction. Provides patterns for efficient
  tool use including parallel execution, evaluator-optimizer loops, and
  orchestrator-worker delegation. Derived from Anthropic cookbook patterns.
version: 1.0.0
---

# Tool Orchestration Patterns

## Tool Selection Heuristic

Before reaching for a tool, decide which one:

| Need | Tool | Why |
|------|------|-----|
| Understand code | Read + Glob + Grep | Read first, act second |
| Small change to existing file | Edit | Atomic patch, not full rewrite |
| New file from scratch | Write | Full content creation |
| Git, builds, tests, installs | Bash | Shell access for everything else |
| Parallel independent subtasks | Agent (sub-agent) | Own context, own tools |
| Search across codebase | Grep for content, Glob for paths | Different tools for different search types |

## Parallel Execution Pattern

When a task spans multiple independent areas:

1. Identify module boundaries from bootstrap context
2. Spawn parallel Agent sub-tasks scoped to each module
3. Each sub-agent gets: the specific task + relevant file paths + conventions
4. Collect and synthesize results

```
Agent("Review src/auth/ for security issues — check for hardcoded secrets, SQL injection, missing input validation")
Agent("Review src/api/ for error handling — check for uncaught exceptions, missing error responses, inconsistent error formats")  
Agent("Review src/db/ for query safety — check for raw queries, missing parameterization, N+1 patterns")
```

These run concurrently. Never let two sub-agents modify the same file.

## Evaluator-Optimizer Loop

For tasks with clear quality criteria (writing specs, generating configs, drafting PRs):

1. **Generate**: Produce first attempt
2. **Evaluate**: Check against criteria — PASS, NEEDS_IMPROVEMENT, or FAIL
3. **If not PASS**: Feed evaluation back, generate again with feedback context
4. **Max 5 iterations** before accepting best attempt

Use this for:
- PR descriptions that must follow a template
- Code that must pass specific lint rules
- Documentation that must cover required sections

## Orchestrator-Worker Pattern

For complex tasks where subtasks aren't known in advance:

1. **Orchestrator** (you) analyzes the task and determines subtasks at runtime
2. **Workers** (sub-agents) each receive the original task + specific instructions
3. Orchestrator synthesizes worker results into final output

Use cheaper/faster reasoning for workers (routine extraction, formatting).
Use deeper reasoning for orchestration (deciding what to delegate, synthesizing results).

## Structured Extraction via Tool Schemas

When you need structured data from unstructured content, the pattern is:
- Define the shape you need as a mental schema
- Read the source material
- Extract into the structured shape
- Validate completeness

For agent-to-agent communication, use XML-structured prompts to define
expected output shape. The sub-agent treats the structure as a contract.

## Adapting to the Repo's Own Tools

Before creating new automation, discover what already exists:

- `package.json` scripts → `npm run [script]`
- `Makefile` targets → `make [target]`
- `justfile` recipes → `just [recipe]`
- `scripts/` directory → direct execution
- GitHub Actions → `gh workflow run`

When the agent needs a new tool:
- Don't hardcode it inline
- Create it as a script/command following the repo's task-runner pattern
- If repo uses Makefile, add a make target
- If repo uses npm scripts, add to package.json
- Register it so the next agent session can discover and use it

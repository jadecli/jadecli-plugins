---
description: "Generate code using the full staff engineering team with SDM orchestration"
args:
  - name: task
    description: "The code generation request — what to build"
    required: true
  - name: roles
    description: "Comma-separated subset of roles to invoke (sdm,mle,qae,fe,be,de,ae,ds). Defaults to SDM choosing."
    required: false
---

# Staff Codegen: Full Team Generation

You are orchestrating the staff-codegen team to generate code for the user's request.

## Process

### Phase 1: SDM Task Decomposition

Invoke the **SDM agent** to analyze the request:

1. Break the request into scoped tasks
2. Identify which specialist roles are needed
3. Define interface contracts between components
4. Determine execution order (parallel vs sequential)

If the `roles` argument is provided, only invoke those specialists. Otherwise,
let the SDM decide based on the request.

### Phase 2: Specialist Execution

For each task in the SDM's breakdown:

1. Invoke the assigned specialist agent with the scoped task
2. Provide the specialist with interface contracts from the SDM
3. Collect the specialist's output (code files, schemas, configs)

**Parallel execution**: Launch independent specialists simultaneously using
the Task tool. Do not wait for one specialist to finish before starting another
if their tasks are independent.

### Phase 3: QAE Test Coverage

After all specialists complete:

1. Invoke the **QAE agent** with the combined output from all specialists
2. QAE designs tests that cover:
   - Unit tests for each specialist's output
   - Integration tests for boundaries between components
   - Edge cases identified across the full system
3. QAE produces test files and a test strategy document

### Phase 4: SDM Integration Review

The SDM reviews the combined output:

1. Verify all interface contracts are satisfied
2. Check for duplicate functionality across specialists
3. Verify error handling consistency
4. Verify naming convention uniformity
5. Confirm all outputs are wired and reachable

If issues are found, the SDM identifies which specialist needs to revise
and what changes are required.

### Phase 5: Final Output

Present the user with:

1. **Summary**: What was built, which specialists contributed
2. **File listing**: All generated files with descriptions
3. **Architecture**: How components connect
4. **Setup instructions**: Dependencies, configuration, how to run
5. **Test instructions**: How to run the test suite
6. **Known limitations**: What's not covered, what needs human review

## Output Structure

```text
# Staff Codegen: [Task Summary]

## Team
[Which specialists were invoked and what each produced]

## Architecture
[How the components connect — data flow, API calls, imports]

## Generated Files
[List of all files with one-line descriptions]

## Setup
[Step-by-step: install deps, configure env, run migrations, etc.]

## Run Tests
[Commands to execute the test suite]

## Integration Notes
[Interface contracts, assumptions, known limitations]
```

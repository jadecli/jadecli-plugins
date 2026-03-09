---
description: "Quick code generation with a single specialist — no team orchestration"
args:
  - name: task
    description: "The code generation request — what to build"
    required: true
  - name: role
    description: "Which specialist to use: mle, qae, fe, be, de, ae, ds. Defaults to best-fit based on the task."
    required: false
---

# Staff Codegen: Quick Generation

Single-specialist code generation without SDM orchestration. Faster but less
comprehensive than full team generation.

## Process

### Step 1: Role Selection

If `role` is specified, use that specialist. Otherwise, determine the best fit:

| Task Keywords | Role |
|--------------|------|
| model, training, ML, inference, embedding, feature | **MLE** |
| test, testing, coverage, assertion, fixture | **QAE** |
| component, UI, form, dashboard, page, CSS, React, Vue | **FE** |
| API, endpoint, database, migration, auth, middleware | **BE** |
| pipeline, ETL, Airflow, Dagster, Spark, streaming, Kafka | **DE** |
| dbt, metric, dimension, fact, analytics, BI, Looker | **AE** |
| A/B test, Bayesian, experiment, statistical, confidence, PyMC | **DS** |

If ambiguous, default to **BE** for general backend work or **FE** for general
frontend work.

### Step 2: Specialist Execution

Invoke the selected specialist agent with the full task. The specialist
produces code following its output format and code standards.

### Step 3: Output

Present the user with:

1. **Role used**: Which specialist generated the code
2. **Generated files**: All files with descriptions
3. **Dependencies**: What needs to be installed
4. **Usage**: How to run or integrate the generated code

## When to Use Quick-Gen vs Generate

Use **quick-gen** when:
- The task fits cleanly in one domain
- You want fast output without orchestration overhead
- You're iterating on a specific component

Use **generate** when:
- The task spans multiple domains
- You need coordinated interfaces between components
- You want comprehensive test coverage across boundaries

---
name: Codegen Orchestration
description: >
  Activate when the user asks to generate code, build a feature, create a
  project, implement a system, or scaffold an application that spans multiple
  engineering disciplines. This skill provides the team composition and
  coordination patterns for the staff-codegen multi-agent code generation team.
version: 1.0.0
---

# Staff Codegen Team Orchestration

When a code generation task spans multiple engineering disciplines, orchestrate
the staff-codegen team rather than trying to do everything in a single pass.

## Team Composition

| Role | Agent | When to Invoke |
|------|-------|----------------|
| **SDM** | Software Development Manager | Always — orchestrates multi-role tasks |
| **MLE** | Machine Learning Engineer | ML models, training, inference, MLOps |
| **QAE** | Quality Assurance Engineer | Always — every feature needs tests |
| **FE** | Frontend Engineer | UI, components, dashboards, forms |
| **BE** | Backend Engineer | APIs, databases, auth, server logic |
| **DE** | Data Engineer | Pipelines, ETL, streaming, warehousing |
| **AE** | Analytics Engineer | dbt models, metrics, BI integration |
| **DS** | Data Scientist | A/B tests, Bayesian stats, experiments |

## Orchestration Pattern

### Step 1: SDM Decomposes the Request

The SDM agent analyzes the request and produces:
- Task breakdown with scoped assignments
- Interface contracts between components
- Dependency graph and execution ordering

### Step 2: Parallel Specialist Execution

Independent tasks execute in parallel. The SDM identifies which tasks have
no dependencies and can run simultaneously.

### Step 3: Sequential Dependent Tasks

Tasks that depend on earlier outputs execute after their dependencies complete.
The SDM ensures interfaces match between producer and consumer.

### Step 4: QAE Test Coverage

The QAE agent runs last (or in parallel with integration review) to produce
tests for all generated code. QAE reviews the combined output and designs
tests that cover integration boundaries, not just unit behavior.

### Step 5: SDM Integration Review

The SDM verifies:
- All interfaces match between components
- No duplicate functionality across specialists
- Error handling is consistent across boundaries
- Naming conventions are uniform
- All outputs are wired and reachable

## When to Use Single-Pass vs Team

**Use team orchestration** (`/staff-codegen:generate`) when:
- The task spans 2+ engineering disciplines
- There are clear component boundaries
- The output will be multiple files across different domains

**Use single-pass** (`/staff-codegen:quick-gen`) when:
- The task fits one specialist's domain
- Speed matters more than depth
- The output is a single file or small set of related files

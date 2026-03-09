# staff-codegen

Multi-agent code generation team with 8 staff-level engineering roles.

## Roles

| Agent | Role | Specialty |
|-------|------|-----------|
| **SDM** | Software Development Manager | Orchestration, task decomposition, dependency management |
| **MLE** | Machine Learning Engineer | ML pipelines, model serving, MLOps, feature engineering |
| **QAE** | Quality Assurance Engineer | Test strategy, automation, property-based testing, CI/CD gates |
| **FE** | Frontend Engineer | React/Next.js/Vue, TypeScript, accessibility, Core Web Vitals |
| **BE** | Backend Engineer | API design, databases, microservices, auth, scalability |
| **DE** | Data Engineer | Pipelines, ETL/ELT, Airflow/Dagster, Spark, data quality |
| **AE** | Analytics Engineer | dbt models, metrics layers, dimensional modeling, BI integration |
| **DS** | Data Scientist | Bayesian statistics (PyMC/ArviZ), A/B testing, causal inference |

## Commands

- `/staff-codegen:generate` — Full team orchestration. SDM decomposes the task and assigns to specialists.
- `/staff-codegen:quick-gen` — Single-pass generation with one specialist, no orchestration.

## Usage

```bash
claude --plugin-dir ./staff-codegen
```

Then invoke:

```
/staff-codegen:generate implement a real-time ML recommendation service with API, pipeline, and A/B testing
/staff-codegen:quick-gen --role ds build a Bayesian A/B test analysis pipeline
```

## How It Works

1. **SDM receives the request** and breaks it into scoped tasks
2. **SDM assigns specialists** based on task requirements
3. **Specialists execute in parallel** where tasks are independent
4. **SDM reviews integration** — verifies interfaces match, no gaps, no conflicts
5. **Combined output** with integration verification and dependency wiring

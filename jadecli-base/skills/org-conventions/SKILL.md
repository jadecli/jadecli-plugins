---
name: Org Conventions
description: >
  Always active. Enforces jadecli organization conventions for commits, PRs,
  actor taxonomy, and team structure. All workers must follow these patterns.
version: 1.0.0
---

# jadecli Org Conventions

## Commit Format

Use Conventional Commits for all commits:

- `feat:` -- new feature or capability
- `fix:` -- bug fix
- `docs:` -- documentation only
- `chore:` -- CI, config, non-functional changes
- `refactor:` -- code restructuring without behavior change
- `test:` -- adding or updating tests

Commit messages should be concise and describe the "why" not the "what".

## PR Workflow

1. Branch from `main` (e.g., `feat/new-skill`, `fix/hook-pattern`)
2. Use conventional commit messages throughout
3. Squash-merge with the PR title as the commit message
4. Never commit directly to `main`

## Actor Taxonomy

Each person in the org has assigned **workers** (roles). Workers are the unit of task tracking and accountability.

- A person can have multiple worker roles
- Workers log tasks to `reporting.worker_tasks`
- The service account `nami@jadecli.com` owns all unassigned worker roles

## Team Roster

| Person | Email | Worker Roles |
|--------|-------|-------------|
| Alex | <alex@jadecli.com> | data, analytical-engineer |
| Bijan | <bijan@jadecli.com> | sales |
| Dima | <dima@jadecli.com> | design, frontend-engineer |
| Sebastian | <sebastian@jadecli.com> | data, marketing, analytical-engineer |
| Nami (service) | <nami@jadecli.com> | all unassigned workers |

## General Rules

- All structured output uses XML tags
- Prefer action over planning when the task is clear
- Complete tasks end-to-end autonomously
- Use parallel execution when tasks are independent
- Pin all GitHub Actions to full SHA

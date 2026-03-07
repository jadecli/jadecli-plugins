---
name: CI/CD Quality Gates
description: >
  Activate when working on CI/CD pipelines, pre-commit hooks, or release
  processes. Covers quality gates at each stage from commit through release.
version: 1.0.0
---

# CI/CD Quality Gates

## Pre-Commit

Runs on every commit via git hooks:

- Trailing whitespace removal
- Prettier formatting check

If pre-commit fails, the commit is rejected. Fix the issue and commit again.

## Pull Request Checks

Every PR triggers these checks (all must pass):

| Check | Command | Purpose |
|---|---|---|
| Typecheck | `tsc --noEmit` | Type safety |
| Lint | `next lint` | Code quality rules |
| Test | `vitest` | Functional correctness |
| Build | `next build` | Compilation success |

## Nightly

Full suite runs nightly:

- Complete test suite (all 299+ tests)
- `npm audit` for security vulnerabilities
- Dependency freshness check

## Release Process

Uses `release-please` for automated semver and CHANGELOG:

1. Conventional commits determine version bump
2. release-please creates a release PR
3. On merge, GitHub Release is created
4. CHANGELOG.md is updated automatically

## Security

- Claude security review runs on every PR
- Reviews for: secrets in code, injection vulnerabilities, auth bypasses
- All GitHub Actions pinned to full SHA (not tags)

## Commitlint

Enforces conventional commit format:

```
type(scope): description

Types: feat, fix, chore, docs, test, refactor, perf, ci
```

Commits that don't follow this format are rejected.

## Action Pinning

All GitHub Actions MUST be pinned to full SHA, not version tags:

```yaml
# Good
uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608

# Bad
uses: actions/checkout@v4
```

This prevents supply-chain attacks via tag mutation.

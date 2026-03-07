# qa-engineer

QA engineering plugin for test strategy, Vitest patterns, and CI/CD quality
gates. Covers the testing pyramid, mocking conventions, and release process.

Builds on top of `jadecli-engineer-base` (Neon, cron, table creation, Vercel deploy).

## Skills (auto-activate)

- `test-strategy` -- Testing pyramid, naming conventions, coverage targets, mocking strategy
- `vitest-patterns` -- Vitest configuration, test file conventions, mocking, execution commands
- `ci-cd-quality` -- Pre-commit hooks, PR checks, nightly runs, release-please, action pinning

## Commands

- `/qa-engineer:test-suite` -- Run the full test suite and report pass/fail results
- `/qa-engineer:coverage-report` -- Generate coverage report and flag files below threshold

## Install

```bash
claude --plugin-dir ./qa-engineer
```

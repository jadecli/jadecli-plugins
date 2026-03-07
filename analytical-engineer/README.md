# analytical-engineer

Analytical engineering plugin for the llms-txt-feed data warehouse. Provides
dimensional modeling conventions, SCD2 patterns, and reporting query knowledge.

Builds on top of `jadecli-engineer-base` (Neon, cron, table creation, Vercel deploy).

## Skills (auto-activate)

- `reporting-queries` -- Query patterns for the reporting.* dimensional model
- `dimensional-modeling` -- Star schema conventions, SCD types, naming rules
- `scd-patterns` -- SCD2 close-and-insert implementation with transaction safety

## Commands

- `/analytical-engineer:vendor-report` -- Generate vendor quality and activity report
- `/analytical-engineer:quality-trend` -- Show quality score trends over time

## Install

```bash
claude --plugin-dir ./analytical-engineer
```

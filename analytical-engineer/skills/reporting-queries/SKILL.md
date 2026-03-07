---
name: Reporting Queries
description: >
  Activate when writing or reviewing SQL queries against the llms-txt-feed
  dimensional model. Covers schema conventions, table relationships, and
  query patterns for the reporting layer.
version: 1.0.0
---

# Reporting Queries

All reporting queries target the `reporting.` schema. Source tables live in `public.`.

## Schema: reporting.*

### Fact Tables

| Table | Grain | Description |
|---|---|---|
| `fact_changes` | vendor x diff | One row per vendor per detected diff |
| `fact_quality` | vendor (SCD2) | Quality scores with valid_from/valid_to |
| `fact_velocity` | vendor (SCD2) | Velocity classifications with valid_from/valid_to |
| `fact_pm_activity` | daily | Aggregated PM command activity per day |

### Dimension Tables

| Table | Type | Description |
|---|---|---|
| `dim_vendor` | SCD1 | Vendor attributes (overwrite, no history) |
| `dim_time` | Date spine | Pre-populated 2025-2027, join on date columns |

### Worker Tracking

| Table | Description |
|---|---|
| `worker_tasks` | Tracks reporting ETL task execution |

## Query Conventions

- Always join facts to dimensions for readable output
- Use CTEs for complex aggregations -- never nested subqueries
- Prefer window functions for period-over-period comparisons
- Include `dim_time` joins for calendar-aware grouping
- Filter SCD2 tables with `WHERE is_current = true` for current state

## Example Queries

### Vendor Quality Trend (last 90 days)

```sql
WITH quality_history AS (
  SELECT
    dv.name AS vendor_name,
    fq.overall_score,
    fq.valid_from,
    fq.valid_to
  FROM reporting.fact_quality fq
  JOIN reporting.dim_vendor dv ON dv.vendor_id = fq.vendor_id
  WHERE fq.valid_from >= now() - interval '90 days'
)
SELECT
  vendor_name,
  overall_score,
  valid_from AS score_date
FROM quality_history
ORDER BY vendor_name, valid_from;
```

### Velocity Classification Changes

```sql
SELECT
  dv.name AS vendor_name,
  fv.classification,
  fv.valid_from,
  fv.valid_to,
  fv.is_current
FROM reporting.fact_velocity fv
JOIN reporting.dim_vendor dv ON dv.vendor_id = fv.vendor_id
ORDER BY dv.name, fv.valid_from;
```

### Weekly Activity Summary

```sql
SELECT
  dt.week_start,
  COUNT(DISTINCT fc.vendor_id) AS active_vendors,
  SUM(fc.lines_changed) AS total_lines_changed,
  COUNT(*) AS total_changes
FROM reporting.fact_changes fc
JOIN reporting.dim_time dt ON dt.date = fc.change_date
WHERE dt.date >= now() - interval '4 weeks'
GROUP BY dt.week_start
ORDER BY dt.week_start DESC;
```

---
name: Dimensional Modeling
description: >
  Activate when designing or modifying the reporting schema. Covers star schema
  conventions, SCD types, naming rules, and grain documentation requirements.
version: 1.0.0
---

# Dimensional Modeling Conventions

## Star Schema Design

Facts reference dimensions via foreign keys. Dimensions are denormalized for
query performance. No snowflaking.

```text
dim_vendor ──┐
             ├── fact_changes
dim_time   ──┘

dim_vendor ──── fact_quality   (SCD2)
dim_vendor ──── fact_velocity  (SCD2)
dim_time   ──── fact_pm_activity
```

## SCD Types

### SCD Type 1 -- dim_vendor

Overwrite attributes directly. No history preserved. Used when historical
attribute values are not analytically meaningful.

```sql
UPDATE reporting.dim_vendor
SET homepage_url = $1, description = $2, updated_at = now()
WHERE vendor_id = $3;
```

### SCD Type 2 -- fact_quality, fact_velocity

Track full history with validity windows. Each row has:

- `valid_from` -- timestamp when this record became effective
- `valid_to` -- timestamp when this record was superseded (9999-12-31 for current)
- `is_current` -- boolean flag for fast current-state queries

## Date Dimension

`dim_time` is a pre-populated date spine covering 2025-01-01 through 2027-12-31.

Columns: `date`, `year`, `quarter`, `month`, `week_start`, `day_of_week`,
`is_weekend`, `is_holiday`.

Join fact date columns to `dim_time.date` for calendar-aware grouping.

## Naming Conventions

| Prefix | Purpose | Example |
|---|---|---|
| `dim_` | Dimension table | `dim_vendor`, `dim_time` |
| `fact_` | Fact table | `fact_changes`, `fact_quality` |

## Schema Separation

- `reporting.*` -- All dimensional model tables
- `public.*` -- Source/operational tables (vendors, snapshots, diffs, etc.)

## Grain Documentation

Every fact table MUST document its grain in a SQL comment on the table:

```sql
COMMENT ON TABLE reporting.fact_changes IS
  'Grain: one row per vendor per detected diff. FK: vendor_id -> dim_vendor.';
```

If you create a new fact table without a grain comment, the schema is incomplete.

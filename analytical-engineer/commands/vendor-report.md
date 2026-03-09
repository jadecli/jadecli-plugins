---
description: "Generate a vendor quality and activity report"
args:
  - name: vendor
    description: "Vendor name to filter (optional, defaults to all vendors)"
    required: false
---

# Vendor Report

Generate a vendor quality and activity report combining quality scores,
change counts, and velocity classifications.

## Instructions

### 1. Query Current Quality Scores

```sql
SELECT
  dv.vendor_id,
  dv.name AS vendor_name,
  fq.overall_score
FROM reporting.fact_quality fq
JOIN reporting.dim_vendor dv ON dv.vendor_id = fq.vendor_id
WHERE fq.is_current = true
ORDER BY dv.name;
```

If a vendor argument is provided, add `AND dv.name ILIKE '%<vendor>%'`.

### 2. Query Change Activity (Last 30 Days)

```sql
SELECT
  dv.name AS vendor_name,
  COUNT(*) AS change_count,
  SUM(fc.lines_changed) AS total_lines_changed
FROM reporting.fact_changes fc
JOIN reporting.dim_vendor dv ON dv.vendor_id = fc.vendor_id
WHERE fc.change_date >= now() - interval '30 days'
GROUP BY dv.name;
```

### 3. Query Velocity Classification

```sql
SELECT
  dv.name AS vendor_name,
  fv.classification
FROM reporting.fact_velocity fv
JOIN reporting.dim_vendor dv ON dv.vendor_id = fv.vendor_id
WHERE fv.is_current = true;
```

### 4. Output

Combine results into a formatted table:

| Vendor | Quality Score | Changes (30d) | Lines Changed | Velocity |
|---|---|---|---|---|

Sort by quality score descending. Flag vendors with score below 50 as
needing attention.

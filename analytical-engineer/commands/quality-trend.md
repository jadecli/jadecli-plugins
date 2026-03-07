---
description: "Show quality score trends over time for a vendor or all vendors"
args:
  - name: vendor
    description: "Vendor name to filter (optional, defaults to all vendors)"
    required: false
  - name: days
    description: "Number of days to look back (default: 90)"
    required: false
    default: "90"
---

# Quality Trend

Show how vendor quality scores have changed over time using SCD2 history.

## Instructions

### 1. Query Quality History

```sql
SELECT
  dv.name AS vendor_name,
  fq.overall_score,
  fq.valid_from,
  fq.valid_to,
  fq.is_current
FROM reporting.fact_quality fq
JOIN reporting.dim_vendor dv ON dv.vendor_id = fq.vendor_id
WHERE fq.valid_from >= now() - interval '<days> days'
ORDER BY dv.name, fq.valid_from;
```

If a vendor argument is provided, add `AND dv.name ILIKE '%<vendor>%'`.

### 2. Compute Deltas

For each vendor, compute the score change between consecutive SCD2 records:

```sql
SELECT
  vendor_name,
  overall_score,
  valid_from,
  overall_score - LAG(overall_score) OVER (
    PARTITION BY vendor_name ORDER BY valid_from
  ) AS score_delta
FROM quality_history;
```

### 3. Output

Display the trend as a table:

| Vendor | Date | Score | Delta |
|---|---|---|---|

Highlight:

- Positive deltas (improvement)
- Negative deltas (regression)
- Vendors with no score changes in the period (stale)

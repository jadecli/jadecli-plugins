---
name: SCD Patterns
description: >
  Activate when implementing or modifying Slowly Changing Dimension Type 2
  logic. Covers the close-and-insert pattern, transaction safety, and
  point-in-time query techniques.
version: 1.0.0
---

# SCD2 Implementation Patterns

## Core Pattern: Close and Insert

Every SCD2 update is a two-step operation wrapped in a transaction.

### Step 1: Close Existing Record

```sql
UPDATE reporting.fact_quality
SET valid_to = now(), is_current = false
WHERE vendor_id = $1 AND is_current = true;
```

### Step 2: Insert New Record

```sql
INSERT INTO reporting.fact_quality (
  vendor_id, overall_score, valid_from, valid_to, is_current
) VALUES (
  $1, $2, now(), '9999-12-31'::timestamptz, true
);
```

### Transaction Wrapper

Always wrap close + insert in a single transaction. A partial update
(close without insert, or insert without close) corrupts the SCD2 chain.

```sql
BEGIN;
  -- close existing
  UPDATE reporting.fact_quality
  SET valid_to = now(), is_current = false
  WHERE vendor_id = $1 AND is_current = true;

  -- insert new
  INSERT INTO reporting.fact_quality (
    vendor_id, overall_score, valid_from, valid_to, is_current
  ) VALUES ($1, $2, now(), '9999-12-31'::timestamptz, true);
COMMIT;
```

## Generic Helper

A reusable SCD2 helper is available at `lib/reporting/scd2.ts`. Use it
instead of writing raw SQL for SCD2 operations in application code.

## Query Patterns

### Current State

```sql
SELECT * FROM reporting.fact_quality
WHERE vendor_id = $1 AND is_current = true;
```

### Point-in-Time

```sql
SELECT * FROM reporting.fact_quality
WHERE vendor_id = $1
  AND valid_from <= $timestamp
  AND valid_to > $timestamp;
```

### Full History

```sql
SELECT * FROM reporting.fact_quality
WHERE vendor_id = $1
ORDER BY valid_from;
```

## Invariants

- Exactly one row per vendor has `is_current = true` at any time
- `valid_to` of one record equals `valid_from` of the next (no gaps)
- The current record always has `valid_to = '9999-12-31'`
- Never DELETE SCD2 records -- history is immutable

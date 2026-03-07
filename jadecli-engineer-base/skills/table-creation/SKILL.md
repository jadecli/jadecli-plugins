---
name: Table Creation Conventions
description: >
  Activate when creating or modifying database tables. Enforces schema conventions,
  DDL patterns, and migration workflow.
version: 1.0.0
---

# Table Creation Conventions

## Schema File

All DDL goes in `lib/db/schema.sql`. This is the single source of truth. Append new tables to the end of this file.

## DDL Patterns

Use `CREATE TABLE IF NOT EXISTS` for idempotent migrations:

```sql
CREATE TABLE IF NOT EXISTS schema_name.table_name (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  -- columns here
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

## Column Conventions

- **Primary keys**: `UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- **Timestamps**: `TIMESTAMPTZ NOT NULL DEFAULT now()` for `created_at`; `TIMESTAMPTZ` (nullable or with default) for other time fields
- **Enums**: Use `CHECK` constraints instead of Postgres ENUM types

```sql
task_type TEXT NOT NULL CHECK (task_type IN ('query', 'report', 'deploy', 'review', 'fix', 'create'))
```

- **JSON data**: Use `JSONB`, never `JSON`
- **Text fields**: Use `TEXT`, never `VARCHAR` (unless a hard length constraint is required)

## Indexes

Create indexes for common query patterns:

```sql
CREATE INDEX IF NOT EXISTS idx_worker_tasks_email
  ON reporting.worker_tasks (worker_email);

CREATE INDEX IF NOT EXISTS idx_worker_tasks_completed
  ON reporting.worker_tasks (completed_at DESC);
```

## Schema Prefix

- Application tables: default `public` schema
- Analytical/reporting tables: `reporting.` schema prefix

## Migration Workflow

1. Add DDL to `lib/db/schema.sql`
2. Run `npm run migrate` to apply
3. Verify with a SELECT on new tables

## Rules

- Never use `DROP TABLE` without explicit user confirmation
- Always use `IF NOT EXISTS` / `IF EXISTS` for idempotency
- Include `created_at TIMESTAMPTZ NOT NULL DEFAULT now()` on every table
- Add `updated_at TIMESTAMPTZ` with a trigger if rows are mutable

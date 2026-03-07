---
name: Neon Postgres Patterns
description: >
  Always active for engineering workers. Provides Neon PG 17/18 patterns,
  query conventions, and driver usage rules for all database interactions.
version: 1.0.0
---

# Neon Postgres Patterns

## Driver

Use `@neondatabase/serverless` HTTP driver. Do NOT use connection pools, pg, or pgBouncer.

```typescript
import { neon } from '@neondatabase/serverless';
const sql = neon(process.env.DATABASE_URL!);
```

## Query Style

Use tagged template literals for all queries:

```typescript
const rows = await sql`SELECT * FROM vendors WHERE active = ${true}`;
```

**CRITICAL**: The Neon HTTP driver does NOT support nested tagged template literals. If you need conditional query fragments, use separate conditional branches:

```typescript
// WRONG -- nested template literals will fail
const rows = await sql`SELECT * FROM vendors ${filter ? sql`WHERE active = ${true}` : sql``}`;

// CORRECT -- conditional branches
const rows = filter
  ? await sql`SELECT * FROM vendors WHERE active = ${true}`
  : await sql`SELECT * FROM vendors`;
```

## Schema Source of Truth

All schema definitions live in `lib/db/schema.sql`. This is the single source of truth for table structure.

## ORM

Drizzle ORM is available but raw SQL is preferred for reporting and analytical queries. Use Drizzle for application CRUD when it simplifies the code.

## Rules

- Always use parameterized queries -- never string interpolation
- UUID primary keys via `gen_random_uuid()`
- `TIMESTAMPTZ` for all timestamps -- never `TIMESTAMP`
- Use `COALESCE` for nullable fields in aggregations
- Prefer `EXISTS` over `IN` for subquery checks
- Use `FOR UPDATE SKIP LOCKED` for queue-like patterns

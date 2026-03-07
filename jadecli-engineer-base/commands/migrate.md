---
description: "Run or generate schema migration against Neon"
---

# Migrate

Run or generate a schema migration for the Neon database.

## Instructions

1. Read `lib/db/schema.sql` to check for pending DDL changes.

2. Run the migration:

```bash
npm run migrate
```

1. Verify the migration succeeded by querying the new or modified tables:

```sql
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema IN ('public', 'reporting')
ORDER BY table_schema, table_name;
```

Use Neon MCP `run_sql` for the verification query.

1. Report the results: tables created/modified, any errors encountered.

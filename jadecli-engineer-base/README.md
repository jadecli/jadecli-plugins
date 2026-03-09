# jadecli-engineer-base

Engineering base plugin layered on top of jadecli-base. Provides Neon Postgres patterns, cron scheduling conventions, table creation standards, and Vercel deploy knowledge for all engineering workers.

## Skills

- **neon-postgres** -- Neon PG 17/18 patterns: `@neondatabase/serverless` HTTP driver, tagged template literals, parameterized queries, UUID keys, TIMESTAMPTZ. Includes the critical nested template literal prohibition.
- **cron-scheduling** -- Vercel cron route structure, CRON_SECRET auth, run logging to `cron_runs` table, try/catch status tracking, schedule configuration in `vercel.json`.
- **table-creation** -- Schema conventions: DDL in `lib/db/schema.sql`, `CREATE TABLE IF NOT EXISTS`, UUID PKs, CHECK constraints for enums, JSONB, reporting schema prefix, index patterns.
- **vercel-deploy** -- Deploy patterns: manual `vercel deploy --prod --yes`, post-squash-merge author fix, preview deploys, env var management, pre-deploy checklist.

## Commands

- `/jadecli-engineer-base:migrate` -- Run or generate schema migration. Checks `lib/db/schema.sql`, runs `npm run migrate`, verifies with Neon MCP.
- `/jadecli-engineer-base:cron-status` -- Check cron job health by querying `cron_runs` table. Shows last 5 runs per job, highlights failures.

## Install

```bash
/plugin install jadecli-engineer-base@jadecli-plugins
```

## MCP Dependencies

- Neon MCP (`https://mcp.neon.tech/mcp`) -- Used for migration verification and cron status queries via `run_sql`.

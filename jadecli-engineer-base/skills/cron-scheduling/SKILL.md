---
name: Cron Scheduling
description: >
  Activate when creating, modifying, or debugging cron jobs. Provides Vercel
  cron route patterns, auth verification, and run logging conventions.
version: 1.0.0
---

# Cron Scheduling

## Route Structure

Cron routes live at:

```
app/api/cron/<job-name>/route.ts
```

Each route must export a `GET` handler.

## Auth

Every cron route must verify the `CRON_SECRET` header:

```typescript
export async function GET(request: Request) {
  const authHeader = request.headers.get('authorization');
  if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
    return new Response('Unauthorized', { status: 401 });
  }
  // ... job logic
}
```

## Run Logging

Log every cron execution to the `cron_runs` table:

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | gen_random_uuid() |
| job_name | TEXT NOT NULL | Name of the cron job |
| started_at | TIMESTAMPTZ | When the run began |
| finished_at | TIMESTAMPTZ | When the run ended |
| status | TEXT | `running`, `completed`, or `failed` |
| summary | TEXT | Brief description of what was done |
| error | TEXT | Error message if failed |

## Execution Pattern

Always use try/catch with status tracking:

```typescript
const runId = crypto.randomUUID();
await sql`INSERT INTO cron_runs (id, job_name, started_at, status)
          VALUES (${runId}, ${jobName}, now(), 'running')`;

try {
  // ... job logic
  await sql`UPDATE cron_runs
            SET finished_at = now(), status = 'completed', summary = ${summary}
            WHERE id = ${runId}`;
} catch (error) {
  await sql`UPDATE cron_runs
            SET finished_at = now(), status = 'failed', error = ${error.message}
            WHERE id = ${runId}`;
  throw error;
}
```

## Schedule Configuration

Cron schedules are defined in `vercel.json`:

```json
{
  "crons": [
    {
      "path": "/api/cron/job-name",
      "schedule": "0 */6 * * *"
    }
  ]
}
```

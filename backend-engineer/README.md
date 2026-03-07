# backend-engineer

Backend engineering plugin for Next.js API routes. Provides API design
conventions, authentication patterns, and middleware stack knowledge.

Builds on top of `jadecli-engineer-base` (Neon, cron, table creation, Vercel deploy).

## Skills (auto-activate)

- `api-design` -- RESTful conventions, response shapes, pagination, rate limiting, Zod validation
- `auth-patterns` -- Bearer token auth, tier-based access, webhook signatures, cron auth
- `middleware-stack` -- Authentication middleware, rate limiting, request logging, error handling

## Commands

- `/backend-engineer:api-test` -- Test an API endpoint with curl and verify response shape
- `/backend-engineer:health-check` -- Hit key endpoints and report health status

## Install

```bash
claude --plugin-dir ./backend-engineer
```

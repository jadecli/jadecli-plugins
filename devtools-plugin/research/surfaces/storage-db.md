# Storage and Database Surface

Database management and data inspection tools.

## TablePlus (App Store ID: 1465448609)

- Native database GUI for PostgreSQL, MySQL, SQLite, Redis, MongoDB
- SSH tunneling built-in
- "Code Review" mode: shows diff of uncommitted DB changes before applying
- Claude Code relevance: inspect databases while Claude Code generates migrations, verify data state

## OK JSON (App Store ID: 1576121509)

- Native JSON tree viewer with collapsible nodes
- macOS Services integration (right-click any text -> send to OK JSON)
- JSONPath querying
- Claude Code relevance: inspect large API response payloads (Stripe, SendGrid, etc.)

## Docker Desktop (Already Installed)

- Container runtime for dev databases (Postgres, Redis, MongoDB)
- Volume management for persistent data
- Resource limits (CPU, memory) -- cap memory to prevent swap pressure
- Claude Code relevance: `docker compose up` for full dev stack, Claude Code manages compose files directly

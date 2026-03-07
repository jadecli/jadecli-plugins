---
name: API Design
description: >
  Activate when creating or modifying API routes. Covers RESTful conventions,
  response shapes, pagination, rate limiting, and validation patterns for
  Next.js API routes.
version: 1.0.0
---

# API Design Conventions

## Route Structure

RESTful routes live in `app/api/v1/`:

```text
app/api/v1/feed/route.ts        GET    /api/v1/feed
app/api/v1/vendors/route.ts     GET    /api/v1/vendors
app/api/v1/vendors/[id]/route.ts GET   /api/v1/vendors/:id
app/api/v1/stats/route.ts       GET    /api/v1/stats
app/api/v1/webhooks/route.ts    POST   /api/v1/webhooks
```

## Response Shape

All responses use a consistent JSON shape:

```json
{
  "data": {},
  "error": null,
  "meta": {
    "cursor": "uuid-or-null",
    "limit": 50,
    "total": 135
  }
}
```

On error:

```json
{
  "data": null,
  "error": "Human-readable error message",
  "meta": {}
}
```

## HTTP Status Codes

| Code | Usage |
|---|---|
| 200 | Successful GET, PUT, PATCH |
| 201 | Successful POST (resource created) |
| 400 | Bad request (validation failure) |
| 401 | Unauthorized (missing/invalid API key) |
| 403 | Forbidden (tier insufficient) |
| 404 | Resource not found |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

## Pagination

Cursor-based pagination. Never use offset-based.

```text
GET /api/v1/vendors?cursor=<uuid>&limit=50
```

Response includes `meta.cursor` for the next page. `null` cursor means
no more results.

## Rate Limiting

Per-tier limits checked against the `request_log` table:

| Tier | Daily Limit |
|---|---|
| free | 100 |
| starter | 5,000 |
| pro | 50,000 |

## Validation

Always validate request bodies with Zod schemas. Return early on failure:

```typescript
const schema = z.object({
  url: z.string().url(),
  name: z.string().min(1).max(200),
});

const parsed = schema.safeParse(body);
if (!parsed.success) {
  return NextResponse.json(
    { data: null, error: parsed.error.message, meta: {} },
    { status: 400 }
  );
}
```

## Versioning

All API routes are prefixed with `/api/v1/`. When breaking changes are
needed, create `/api/v2/` routes while maintaining v1 backward compatibility.

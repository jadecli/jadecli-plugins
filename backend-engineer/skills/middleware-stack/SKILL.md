---
name: Middleware Stack
description: >
  Activate when working on request middleware, error handling, or security
  headers. Covers the authentication middleware, rate limiting, request
  logging, and CORS configuration.
version: 1.0.0
---

# Middleware Stack

## Authentication Middleware

`lib/auth.ts` exports `authenticate()`:

```typescript
interface AuthResult {
  tier: 'free' | 'starter' | 'pro';
  keyId: string | null;
  error: string | null;
}

export async function authenticate(request: Request): Promise<AuthResult>;
```

Usage in route handlers:

```typescript
export async function GET(request: Request) {
  const auth = await authenticate(request);
  if (auth.error) {
    return NextResponse.json(
      { data: null, error: auth.error, meta: {} },
      { status: 401 }
    );
  }
  // auth.tier is now available for feature gating
}
```

## Rate Limiting

Checked after authentication. Counts requests in the current day:

```sql
SELECT COUNT(*) FROM request_log
WHERE key_id = $1 AND created_at > now() - interval '1 day';
```

Compare against tier limits (free: 100, starter: 5000, pro: 50000).
Return 429 if exceeded.

## Request Logging

Every API call is logged to `request_log`:

```sql
INSERT INTO request_log (key_id, endpoint, method, status_code, created_at)
VALUES ($1, $2, $3, $4, now());
```

Log AFTER the response is generated so `status_code` is accurate.

## Error Handling

All route handlers follow try/catch with consistent error shape:

```typescript
try {
  // route logic
} catch (error) {
  console.error(`[${endpoint}]`, error);
  return NextResponse.json(
    { data: null, error: 'Internal server error', meta: {} },
    { status: 500 }
  );
}
```

Never expose internal error details to the client.

## Security Headers

Set via `next.config.js` `headers()`:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: strict-origin-when-cross-origin`

## CORS

Configured in `next.config.js`. API routes allow cross-origin requests
with appropriate `Access-Control-Allow-Origin` headers.

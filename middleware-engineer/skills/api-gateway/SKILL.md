---
name: API Gateway
description: >
  Activate when working on request routing, feature gating, rate limiting,
  or webhook verification at the gateway layer. Covers Next.js middleware
  patterns and tier-based access control.
version: 1.0.0
---

# API Gateway Patterns

## Next.js Middleware

`middleware.ts` at the project root handles cross-cutting concerns before
requests reach route handlers:

- Path-based routing decisions
- Security header injection
- Request ID generation (for tracing)

## Tier-Based Feature Gating

Features are gated by API key tier:

| Feature | free | starter | pro |
|---|---|---|---|
| Feed endpoint | Y | Y | Y |
| Vendors list | Y | Y | Y |
| Stats | Y | Y | Y |
| Diffs | - | Y | Y |
| Snapshots | - | Y | Y |
| Intelligence | - | - | Y |
| Webhooks | - | - | Y |
| MCP access | - | - | Y |

Gate checks happen after authentication:

```typescript
if (auth.tier === 'free' && isProFeature(endpoint)) {
  return NextResponse.json(
    { data: null, error: 'Pro tier required', meta: {} },
    { status: 403 }
  );
}
```

## Rate Limiting at Gateway

Rate limits are enforced per API key per day:

| Tier | Limit |
|---|---|
| free | 100/day |
| starter | 5,000/day |
| pro | 50,000/day |

Implementation uses `request_log` table counts. When limit is exceeded,
return 429 with `Retry-After` header.

## Request/Response Logging

Every API request is logged with:

- Request ID (UUID, also returned in `X-Request-ID` header)
- API key ID (null for unauthenticated)
- Endpoint path
- HTTP method
- Response status code
- Timestamp

## Webhook Verification (Inbound)

For incoming webhooks (e.g., Stripe):

```typescript
import { createHmac, timingSafeEqual } from 'crypto';

function verifyWebhookSignature(
  payload: string,
  signature: string,
  secret: string
): boolean {
  const expected = createHmac('sha256', secret).update(payload).digest('hex');
  return timingSafeEqual(Buffer.from(signature), Buffer.from(expected));
}
```

Always use `timingSafeEqual` to prevent timing attacks.

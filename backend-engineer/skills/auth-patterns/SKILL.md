---
name: Auth Patterns
description: >
  Activate when implementing or reviewing authentication, authorization,
  or API key management. Covers Bearer token auth, tier-based access,
  and webhook signature verification.
version: 1.0.0
---

# Authentication Patterns

## API Key Authentication

### Bearer Token

API keys are passed in the `Authorization` header:

```text
Authorization: Bearer ltf_abc123...
```

### Key Storage

Keys are stored as SHA-256 hashes in the `api_keys` table. Never store
plaintext keys. On creation, return the plaintext key once and store only
the hash.

```typescript
import { createHash } from 'crypto';

const hash = createHash('sha256').update(plaintextKey).digest('hex');
```

### Tier-Based Access

| Tier | Daily Requests | Features |
|---|---|---|
| free | 100 | Feed, vendors, stats |
| starter | 5,000 | + diffs, snapshots |
| pro | 50,000 | + intelligence, webhooks, MCP |

### No Auth = Free Tier

Requests without an `Authorization` header default to free tier. This is
not an error -- it allows unauthenticated public access to basic endpoints.

## Key Provisioning Flow

1. User completes Stripe checkout
2. Stripe fires `checkout.session.completed` webhook
3. Webhook handler creates API key in `api_keys` table
4. Key is returned to user via success page or email

## Webhook Signatures (Outbound)

Outbound webhooks are signed with HMAC-SHA256:

```typescript
import { createHmac } from 'crypto';

const signature = createHmac('sha256', secret)
  .update(JSON.stringify(payload))
  .digest('hex');

// Sent as header: X-Webhook-Signature: sha256=<signature>
```

Webhook secrets are stored per-subscriber in the `webhooks` table.

## Cron Authentication

Cron endpoints verify the `CRON_SECRET` environment variable:

```typescript
const authHeader = request.headers.get('authorization');
if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
  return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
}
```

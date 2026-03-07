---
name: Test Strategy
description: >
  Activate when planning tests, reviewing test coverage, or deciding what
  kind of test to write. Covers the testing pyramid, naming conventions,
  and coverage targets.
version: 1.0.0
---

# Testing Strategy at jadecli

## Testing Pyramid

### Unit Tests

For pure functions and utilities. Fast, isolated, no external dependencies.

- `lib/` utility functions
- Data transformation logic
- Validation schemas
- Helper functions

### Integration Tests

For API routes with a real Neon test database. Verify end-to-end behavior.

- Route handlers (GET, POST, etc.)
- Database queries and transactions
- Authentication flow
- Rate limiting behavior

### Security Tests

For auth boundaries, injection prevention, and rate limiting.

- API key validation (valid, invalid, missing, expired)
- SQL injection prevention
- XSS prevention in API responses
- Rate limit enforcement
- CORS header verification

## Test Naming Convention

```typescript
describe('<module>', () => {
  it('should <expected behavior>', () => {
    // ...
  });
});
```

Examples:

- `describe('authenticate')` -> `it('should return free tier when no auth header')`
- `describe('GET /api/v1/feed')` -> `it('should return 429 when rate limited')`

## Coverage

- 299+ tests across 18 test files in llms-txt-feed
- Target: > 80% coverage for new code
- Always test error paths and edge cases
- Every new API endpoint needs at least: happy path, auth failure, validation failure, rate limit

## Mocking

Mock external services -- never call real APIs in tests:

- Stripe API: mock checkout sessions and webhook events
- Anthropic API: mock intelligence analysis responses
- External HTTP calls: mock with `vi.mock()` or MSW

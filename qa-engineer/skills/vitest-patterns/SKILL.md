---
name: Vitest Patterns
description: >
  Activate when writing or running tests. Covers Vitest configuration,
  test file conventions, mocking patterns, and execution commands.
version: 1.0.0
---

# Vitest Conventions

## Configuration

Config file: `vitest.config.ts`

Key settings:

- Test environment: `node` (not jsdom -- API tests don't need a DOM)
- Timeout: 30s for integration tests
- Globals: enabled (no need to import `describe`, `it`, `expect`)

## Test File Location

```text
tests/
  auth.test.ts
  feed.test.ts
  vendors.test.ts
  stats.test.ts
  webhooks.test.ts
  intelligence.test.ts
  ...
```

Pattern: `tests/<module>.test.ts`

## Structure

```typescript
describe('<module>', () => {
  beforeAll(async () => {
    // Setup: seed test data, initialize connections
  });

  afterAll(async () => {
    // Teardown: clean test data, close connections
  });

  it('should <behavior>', () => {
    // Arrange
    const input = { ... };

    // Act
    const result = await functionUnderTest(input);

    // Assert
    expect(result).toEqual(expected);
  });
});
```

## Mocking

### Module Mocking

```typescript
vi.mock('lib/external-service', () => ({
  fetchData: vi.fn().mockResolvedValue({ status: 'ok' }),
}));
```

### Function Spies

```typescript
const spy = vi.fn();
// ... use spy as callback
expect(spy).toHaveBeenCalledWith('expected-arg');
expect(spy).toHaveBeenCalledTimes(1);
```

### Environment Variables

```typescript
beforeAll(() => {
  vi.stubEnv('CRON_SECRET', 'test-secret');
});

afterAll(() => {
  vi.unstubAllEnvs();
});
```

## Running Tests

| Command | Scope |
|---|---|
| `npm test` | Full suite |
| `npx vitest run <file>` | Single file |
| `npx vitest run --coverage` | With coverage report |
| `npx vitest --watch` | Watch mode (development) |

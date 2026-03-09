---
name: React Patterns
description: >
  Activate when writing or reviewing React components. Covers component
  architecture, state management, styling, and the component library
  conventions used at jadecli.
version: 1.0.0
---

# React Patterns at jadecli

## Component Architecture

### Server Components for Data Fetching

Fetch data in Server Components. Pass it down as props to Client Components
when interactivity is needed.

```tsx
// app/dashboard/page.tsx (Server Component)
export default async function DashboardPage() {
  const stats = await fetchStats();
  return <StatsDisplay stats={stats} />;
}
```

### Client Components for Interactivity

Mark with `'use client'` only when required. Keep Client Components small
and push them to the leaves of the component tree.

```tsx
'use client';

export function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('');
  // ...
}
```

### Composition Over Prop Drilling

Use composition (children, render props) instead of passing props through
multiple levels:

```tsx
// Good: composition
<Layout sidebar={<VendorList />}>
  <VendorDetail />
</Layout>

// Bad: prop drilling
<Layout vendors={vendors} selectedVendor={selected} onSelect={onSelect} />
```

## Loading and Error States

### Suspense Boundaries

Use `loading.tsx` or explicit `<Suspense>` for loading states:

```tsx
<Suspense fallback={<Skeleton />}>
  <AsyncComponent />
</Suspense>
```

### Error Boundaries

Use `error.tsx` for route-level errors. For component-level errors,
use React error boundaries.

## TypeScript

- Strict mode always (`"strict": true` in tsconfig)
- Explicit return types on exported functions
- Interface for component props, type for unions/intersections
- No `any` -- use `unknown` and narrow

## Styling

- Tailwind CSS for all styling -- no CSS modules, no styled-components
- shadcn/ui as component library (installed components in `components/ui/`)
- Use `cn()` utility (from `lib/utils.ts`) for conditional classes
- Follow mobile-first responsive design

## Component Organization

```text
components/
  ui/           # shadcn/ui primitives (Button, Card, etc.)
  layout/       # Header, Footer, Sidebar
  vendors/      # Vendor-specific components
  dashboard/    # Dashboard-specific components
```

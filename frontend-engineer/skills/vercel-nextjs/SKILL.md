---
name: Vercel + Next.js
description: >
  Activate when working on Next.js application code, Vercel deployment
  configuration, or routing. Covers App Router conventions, rendering
  strategies, and Vercel-specific optimizations.
version: 1.0.0
---

# Next.js + Vercel Patterns

## App Router (app/ directory)

This project uses the App Router exclusively. Never use the Pages Router.

### File Conventions

| File | Purpose |
|---|---|
| `page.tsx` | Route UI |
| `layout.tsx` | Shared layout (wraps children) |
| `loading.tsx` | Loading UI (Suspense boundary) |
| `error.tsx` | Error UI (Error boundary) |
| `not-found.tsx` | 404 UI |
| `route.ts` | API route handler |

### Server Components by Default

All components are Server Components unless explicitly marked with `'use client'`.

Use `'use client'` only when the component needs:

- Event handlers (onClick, onChange, etc.)
- useState, useEffect, useRef
- Browser-only APIs (window, document)

### Route Handlers

API routes live in `app/api/`. Convention:

```text
app/api/v1/feed/route.ts      -> GET /api/v1/feed
app/api/v1/vendors/route.ts   -> GET /api/v1/vendors
app/api/v1/stats/route.ts     -> GET /api/v1/stats
```

Export named functions: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`.

## Metadata API

Use the Metadata API for SEO. Export `metadata` or `generateMetadata` from
page/layout files:

```tsx
export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description',
};
```

## Image Optimization

Always use `next/image` for images. Provides automatic:

- Format conversion (WebP/AVIF)
- Responsive sizing
- Lazy loading

## Font Optimization

Use `next/font` for zero-layout-shift font loading:

```tsx
import { Inter } from 'next/font/google';
const inter = Inter({ subsets: ['latin'] });
```

## Environment Variables

- `NEXT_PUBLIC_*` -- Exposed to client-side code
- All other env vars -- Server-side only
- Never put secrets in `NEXT_PUBLIC_` variables

## Rendering Strategies

| Strategy | Use When |
|---|---|
| Static (default) | Content doesn't change per request |
| ISR (`revalidate`) | Content changes periodically |
| Dynamic (`force-dynamic`) | Content changes every request |
| Streaming (Suspense) | Parts of page load independently |

---
name: Core Web Vitals
description: >
  Activate when optimizing page performance, reviewing Lighthouse scores,
  or diagnosing slow pages. Covers LCP, INP, CLS targets and optimization
  techniques.
version: 1.0.0
---

# Core Web Vitals Optimization

## Targets

| Metric | Target | Description |
|---|---|---|
| LCP | < 2.5s | Largest Contentful Paint |
| INP | < 200ms | Interaction to Next Paint |
| CLS | < 0.1 | Cumulative Layout Shift |

## Measurement

### Lighthouse CI

Configured at `.lighthouserc.json`. Run locally:

```bash
npx lhci autorun
```

### web-vitals Library

For real-user monitoring:

```tsx
import { onLCP, onINP, onCLS } from 'web-vitals';

onLCP(console.log);
onINP(console.log);
onCLS(console.log);
```

## LCP Optimization

- Preload critical resources (`<link rel="preload">`)
- Use `next/image` with `priority` prop for above-fold images
- Minimize server response time (use ISR or caching)
- Avoid render-blocking CSS/JS
- Use `next/font` to eliminate font-related LCP delays

## INP Optimization

- Minimize JavaScript execution time
- Use `startTransition` for non-urgent updates
- Debounce expensive event handlers
- Avoid layout thrashing (batch DOM reads/writes)
- Keep Client Components small -- less JS to parse and execute

## CLS Optimization

- Always set `width` and `height` on images (next/image does this)
- Use `next/font` with `display: swap` to prevent layout shift
- Reserve space for dynamic content (min-height, aspect-ratio)
- Avoid injecting content above existing content
- Use CSS `contain: layout` for independently-sized sections

## Performance Budget

- Total JS bundle: < 200KB gzipped (first load)
- Per-route JS: < 50KB gzipped
- Images: WebP/AVIF format, appropriate sizing
- Fonts: subset to used characters, preload

# frontend-engineer

Frontend engineering plugin for Next.js applications on Vercel. Provides
App Router patterns, React component conventions, and Core Web Vitals
optimization knowledge.

Builds on top of `jadecli-engineer-base` (Neon, cron, table creation, Vercel deploy).

## Skills (auto-activate)

- `vercel-nextjs` -- App Router conventions, rendering strategies, Vercel-specific optimizations
- `react-patterns` -- Server/Client Components, composition, TypeScript strict mode, Tailwind + shadcn/ui
- `web-vitals` -- LCP, INP, CLS targets and optimization techniques

## Commands

- `/frontend-engineer:preview-deploy` -- Deploy a Vercel preview and return the URL
- `/frontend-engineer:lighthouse` -- Run Lighthouse CI and report Core Web Vitals scores

## Install

```bash
claude --plugin-dir ./frontend-engineer
```

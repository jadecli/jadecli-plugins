---
description: "Run Lighthouse CI against a URL and report Core Web Vitals"
args:
  - name: url
    description: "URL to audit (default: preview or production URL)"
    required: false
---

# Lighthouse Audit

Run Lighthouse CI and report Core Web Vitals scores.

## Instructions

### 1. Check Configuration

Look for `.lighthouserc.json` in the project root:

```bash
cat .lighthouserc.json 2>/dev/null
```

### 2. Run Lighthouse

If `.lighthouserc.json` exists:

```bash
npx lhci autorun
```

If no config exists or a specific URL is provided:

```bash
npx lighthouse <url> --output=json --chrome-flags="--headless"
```

### 3. Report

Extract and display Core Web Vitals:

| Metric | Value | Target | Status |
|---|---|---|---|
| LCP | x.xs | < 2.5s | PASS/FAIL |
| INP | xms | < 200ms | PASS/FAIL |
| CLS | x.xx | < 0.1 | PASS/FAIL |

Also report:
- Performance score (0-100)
- Accessibility score (0-100)
- Best Practices score (0-100)
- SEO score (0-100)

Flag any metric that fails its threshold.

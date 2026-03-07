---
description: "Deploy a Vercel preview and return the preview URL"
args: []
---

# Preview Deploy

Deploy a Vercel preview build for testing.

## Instructions

### 1. Pre-flight Checks

Verify the working directory has a `vercel.json` or `next.config.js`:

```bash
ls vercel.json next.config.js next.config.mjs 2>/dev/null
```

### 2. Deploy Preview

Run the Vercel CLI without `--prod`:

```bash
vercel deploy
```

This creates a preview deployment (not production).

### 3. Output

Report:
- Preview URL (from Vercel CLI output)
- Deployment status
- Any build warnings or errors

Do NOT use `--prod`. This command is strictly for preview deployments.
For production, use `vercel deploy --prod --yes`.

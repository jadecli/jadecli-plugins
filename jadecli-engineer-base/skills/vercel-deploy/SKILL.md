---
name: Vercel Deploy Patterns
description: >
  Activate when deploying to Vercel or managing deploy configuration.
  Covers production deploys, preview deploys, env var management,
  and post-merge author fixes.
version: 1.0.0
---

# Vercel Deploy Patterns

## Production Deploy

Auto-deploy is broken. Always deploy manually:

```bash
vercel deploy --prod --yes
```

## Vercel Link

NEVER run `vercel link` without specifying the project:

```bash
vercel link --project <project-name>
```

Omitting `--project` can link to the wrong project and deploy to the wrong URL.

## Post-Squash-Merge Author Fix

After squash-merging a PR, the HEAD commit author is set to the GitHub merge actor (jade@jadecli.com). Vercel may reject deploys from unrecognized authors.

Fix: push a lightweight commit to set the correct author before deploying.

```bash
git commit --allow-empty -m "chore: fix deploy author"
git push
vercel deploy --prod --yes
```

## Preview Deploys

For preview/staging deploys, omit `--prod`:

```bash
vercel deploy
```

This creates a unique preview URL for testing.

## Environment Variables

Manage via CLI or dashboard:

```bash
# Add a variable
vercel env add VARIABLE_NAME production

# List variables
vercel env ls

# Pull env vars to local .env
vercel env pull .env.local
```

## Pre-Deploy Checklist

1. Verify HEAD commit author matches a team member with deploy access
2. Ensure all env vars are set for the target environment
3. Run `npm run build` locally to catch build errors before deploying
4. Check that `vercel.json` is valid (cron schedules, rewrites, headers)

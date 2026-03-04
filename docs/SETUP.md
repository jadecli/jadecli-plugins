# Repository Setup Guide

This guide covers one-time configuration for jadecli-plugins after cloning.

## Prerequisites

- GitHub CLI (`gh`) authenticated with admin access to the repository
- Admin permissions on `jadecli/jadecli-plugins`

## 1. Run the setup script

The setup script configures labels, branch protection, merge strategy, and creates the initial release:

```bash
REPO=jadecli/jadecli-plugins ./scripts/setup-github-repo.sh
```

For forks, override `REPO`:

```bash
REPO=your-username/jadecli-plugins ./scripts/setup-github-repo.sh
```

The script is idempotent and safe to re-run.

## 2. Configure repository secrets

The following secrets are needed for CI workflows:

| Secret              | Required for                          | How to get                                          |
| ------------------- | ------------------------------------- | --------------------------------------------------- |
| `ANTHROPIC_API_KEY` | Claude Code review + @claude mentions | [Anthropic Console](https://console.anthropic.com/) |

To add a secret:

```bash
gh secret set ANTHROPIC_API_KEY -R jadecli/jadecli-plugins
```

> **Note:** Claude Max Pro uses interactive OAuth (browser-based login) and
> cannot be used in headless CI environments like GitHub Actions. An API key
> from the Anthropic Console is required.

## 3. Activate Claude workflows

After adding `ANTHROPIC_API_KEY`, uncomment the action steps in:

- `.github/workflows/claude-code-review.yml` (AI PR review)
- `.github/workflows/claude-mention.yml` (@claude in issues/PRs)

Look for the `# Uncomment the step below` comments in each file.

## 4. Create CODEOWNERS team

The `.github/CODEOWNERS` file references `@jadecli/core`. Create this team in your GitHub organization:

1. Go to **Organization Settings > Teams**
2. Create team `core` under `jadecli`
3. Add repository maintainers as members

If you're using a personal account (not an organization), replace `@jadecli/core` in `CODEOWNERS` with your GitHub username (e.g., `@your-username`).

## 5. Verify setup

After completing all steps, verify:

```bash
# Labels exist
gh label list -R jadecli/jadecli-plugins

# Branch protection is active
gh api repos/jadecli/jadecli-plugins/branches/main/protection

# Merge strategy is configured
gh api repos/jadecli/jadecli-plugins | jq '{squash: .allow_squash_merge, merge: .allow_merge_commit, rebase: .allow_rebase_merge}'

# Release exists
gh release view v1.0.0 -R jadecli/jadecli-plugins

# Plugin still works locally
claude --plugin-dir ./adaptive-agent
```

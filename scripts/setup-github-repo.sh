#!/usr/bin/env bash
#
# Setup GitHub repository configuration for jadecli-plugins.
# Configures labels, branch protection, merge strategy, and repo settings.
#
# Usage:
#   REPO=jadecli/jadecli-plugins ./scripts/setup-github-repo.sh
#
# Requires: gh CLI authenticated with admin access to the repo.
# Idempotent: safe to re-run.

set -euo pipefail

REPO="${REPO:-jadecli/jadecli-plugins}"

echo "==> Configuring $REPO"
echo ""

# ---------------------------------------------------------------------------
# Labels
# ---------------------------------------------------------------------------
echo "--- Creating labels ---"

create_label() {
  local name="$1" color="$2" desc="${3:-}"
  if gh label create "$name" --color "$color" --description "$desc" -R "$REPO" 2>/dev/null; then
    echo "  Created: $name"
  else
    echo "  Exists:  $name"
  fi
}

# Autorelease labels (Anthropic pattern)
create_label "autorelease: pending"     "ededed" "Release pending publish"
create_label "autorelease: pre-release" "ededed" "Pre-release version"
create_label "autorelease: tagged"      "ededed" "Release tagged"

# Component labels
create_label "plugin"    "1d76db" "Plugin-level change"
create_label "skill"     "0e8a16" "Skill addition or modification"
create_label "command"   "fbca04" "Command addition or modification"
create_label "agent"     "d4c5f9" "Agent addition or modification"
create_label "hook"      "f9d0c4" "Hook addition or modification"

# Workflow labels
create_label "breaking"  "b60205" "Breaking change"
create_label "release"   "0075ca" "Release management"

echo ""

# ---------------------------------------------------------------------------
# Merge strategy
# ---------------------------------------------------------------------------
echo "--- Configuring merge strategy ---"

gh api "repos/$REPO" -X PATCH \
  -f allow_squash_merge=true \
  -f allow_merge_commit=false \
  -f allow_rebase_merge=true \
  -f squash_merge_commit_title=PR_TITLE \
  -f squash_merge_commit_message=PR_BODY \
  -F delete_branch_on_merge=true \
  --silent

echo "  Squash merge: enabled (preferred)"
echo "  Merge commit: disabled"
echo "  Rebase merge: enabled"
echo "  Auto-delete branches: enabled"
echo ""

# ---------------------------------------------------------------------------
# Branch protection
# ---------------------------------------------------------------------------
echo "--- Configuring branch protection on main ---"

gh api "repos/$REPO/branches/main/protection" -X PUT \
  --input - <<'JSON' --silent
{
  "required_status_checks": {
    "strict": true,
    "contexts": [
      "Validate JSON",
      "Validate plugin structure",
      "Lint commit messages",
      "Lint Markdown"
    ]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true
  },
  "restrictions": null
}
JSON

echo "  Required checks: Validate JSON, plugin structure, commit lint, markdown lint"
echo "  Required reviews: 1 (stale reviews dismissed)"
echo "  Enforce for admins: yes"
echo ""

# ---------------------------------------------------------------------------
# Initial release (if missing)
# ---------------------------------------------------------------------------
echo "--- Checking v1.0.0 release ---"

if gh release view v1.0.0 -R "$REPO" >/dev/null 2>&1; then
  echo "  v1.0.0 already exists"
else
  echo "  Creating v1.0.0 release..."
  gh release create v1.0.0 \
    --title "v1.0.0" \
    --notes "Initial release of jadecli-plugins marketplace with adaptive-agent plugin." \
    -R "$REPO"
  echo "  Created v1.0.0"
fi

echo ""
echo "==> Setup complete for $REPO"

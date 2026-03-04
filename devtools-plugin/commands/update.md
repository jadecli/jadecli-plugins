---
name: update
description: Update all managed dev tools to latest versions
---

Update all installed tools managed by the devtools plugin.

## Instructions

1. Update App Store apps:

   ```bash
   mas upgrade
   ```

2. Update Homebrew tools:

   ```bash
   brew update && brew upgrade --cask docker 1password-cli
   ```

3. Report what was updated and any failures.

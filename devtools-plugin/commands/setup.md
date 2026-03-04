---
name: setup
description: Install and configure all recommended macOS dev tools for Claude Code workflows
---

Run the devtools installer script to set up the full development environment.

## Instructions

1. Execute the installer:
```bash
bash "$(dirname "$(find . -path '*/devtools-plugin/scripts/install.sh' -type f | head -1)")/install.sh"
```

2. After installation completes, run the status check:
```bash
bash "$(dirname "$(find . -path '*/devtools-plugin/scripts/status.sh' -type f | head -1)")/status.sh"
```

3. Report the results to the user with any items that need manual attention.

## What Gets Installed

### App Store Apps (via mas)
- Amphetamine, Maccy, SnippetsLab, RapidAPI, Proxyman
- TablePlus, OK JSON, Figma, Flow, 1Password

### Homebrew Tools
- Docker Desktop
- 1Password CLI

### System Configuration
- File descriptor limit (65536)
- Key repeat rate (fastest)
- Dock instant autohide, no recents, fixed Spaces
- SSH connection persistence
- Login items for background apps

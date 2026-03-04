---
name: devtools-setup
description: Guides first-time setup of macOS dev environment for Claude Code
---

# DevTools First-Time Setup

When a user needs to set up their macOS development environment for Claude Code workflows:

## Steps

1. Run the installer: `bash devtools-plugin/scripts/install.sh`
2. Run the doctor: `bash devtools-plugin/scripts/doctor.sh`
3. Address any issues found
4. Verify with: `bash devtools-plugin/scripts/status.sh`

## Post-Install Manual Steps

These require user interaction and cannot be automated:

- Log out/in for keyboard repeat rate changes
- Open Docker Desktop to accept license and complete setup
- Run `op signin` to authenticate 1Password CLI
- Enable Touch ID for sudo: add `auth sufficient pam_tid.so` to `/etc/pam.d/sudo_local`
- Exclude dev directories from Spotlight: System Settings > Siri & Spotlight > Privacy

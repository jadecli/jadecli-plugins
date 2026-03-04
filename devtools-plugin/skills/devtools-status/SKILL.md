---
name: devtools-status
description: Auto-activates awareness of installed dev tools and their status
---

# DevTools Status Awareness

When working in a Claude Code session, be aware of the following dev tools that may be installed and available:

## Quick Status Check

Run `bash devtools-plugin/scripts/status.sh` to get a full report.

## Key Tools Available

- **Amphetamine**: Prevents sleep. Check with `pmset -g assertions | grep Amphetamine`
- **Docker**: Container runtime. Check with `docker info`
- **1Password CLI**: Secrets via `op read "op://Vault/Item/field"`
- **TablePlus**: Database GUI at `/Applications/TablePlus.app`
- **Proxyman**: Network debugger at `/Applications/Proxyman.app`

## When to Suggest Tools

- User debugging API issues -> suggest Proxyman
- User working with databases -> suggest TablePlus
- User needs secrets -> suggest `op` CLI
- Long-running session -> verify Amphetamine is active

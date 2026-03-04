# Claude Code CLI Entry Point

How installed tools integrate with Claude Code's direct CLI usage.

## Environment Variables

Tools that expose CLI interfaces Claude Code can invoke:

| Tool | CLI Command | Integration |
|------|-------------|-------------|
| Docker Desktop | `docker`, `docker compose` | Claude Code runs containers, manages compose files |
| 1Password CLI | `op` | Read secrets: `op read "op://Vault/Item/field"` |
| TablePlus | `open -a TablePlus` | Open DB connections from terminal |
| mas (Mac App Store CLI) | `mas` | Install/update App Store apps programmatically |

## Shell Environment

Claude Code inherits the user's shell environment. Key config:

```bash
# ~/.zshrc additions that benefit Claude Code
ulimit -n 65536
export SSH_AUTH_SOCK=~/Library/Group\ Containers/2BUA8C4S2C.com.1password/t/agent.sock
export EDITOR="cursor --wait"
```

## Amphetamine Integration

Claude Code long-running sessions benefit from Amphetamine preventing sleep.
The caffeinate CLI can also be used programmatically:

```bash
# Prevent sleep for duration of a command
caffeinate -i long-running-build-command
```

## Clipboard (Maccy)

Claude Code copies output to clipboard. Maccy preserves history so users can
retrieve previous Claude Code outputs without scrolling terminal history.

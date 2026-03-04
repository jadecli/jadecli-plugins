# Terminal Surface

Shell configuration and CLI tools for Claude Code workflows.

## Shell Config (~/.zshrc)

```bash
set -euo pipefail  # for scripts

# File descriptor limit
ulimit -n 65536

# Key repeat (also set via defaults write)
# Ensure EDITOR is set for Claude Code git operations
export EDITOR="cursor --wait"
```

## SSH Persistence (~/.ssh/config)

```
Host *
  ServerAliveInterval 60
  ServerAliveCountMax 10
  ControlMaster auto
  ControlPath ~/.ssh/sockets/%r@%h:%p
  ControlPersist 600
```

```bash
mkdir -p ~/.ssh/sockets && chmod 700 ~/.ssh/sockets
```

## 1Password CLI

```bash
# Install via brew
brew install --cask 1password-cli

# Use as SSH agent
export SSH_AUTH_SOCK=~/Library/Group\ Containers/2BUA8C4S2C.com.1password/t/agent.sock

# Read secrets in scripts
op read "op://Vault/Item/field"
```

## Docker CLI

Docker Desktop provides the `docker` and `docker compose` CLI tools.
Claude Code uses these directly for:
- Starting/stopping dev databases
- Building and testing containerized services
- Running one-off commands in containers

#!/usr/bin/env bash
set -euo pipefail

# devtools status checker -- reports on installed tools and system config

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

ok()   { printf "${GREEN}[OK]${NC}   %s\n" "$1"; }
warn() { printf "${YELLOW}[WARN]${NC} %s\n" "$1"; }
err()  { printf "${RED}[MISS]${NC} %s\n" "$1"; }

echo "===== App Store Apps ====="

cache_mas_list
for entry in "${APPS[@]}"; do
  name=$(app_name "$entry")
  id=$(app_id "$entry")
  if app_installed "$entry"; then
    ok "$name"
  else
    err "$name (mas install $id)"
  fi
done

echo ""
echo "===== System Tools ====="

if [ -d "/Applications/Docker.app" ]; then
  ver=$(docker --version 2>/dev/null || echo "unknown")
  ok "Docker Desktop ($ver)"
else
  err "Docker Desktop (brew install --cask docker)"
fi

if command -v op &>/dev/null; then
  ok "1Password CLI ($(op --version 2>/dev/null || echo "unknown"))"
else
  err "1Password CLI (brew install --cask 1password-cli)"
fi

if command -v mas &>/dev/null; then
  ok "mas CLI"
else
  err "mas CLI (brew install mas)"
fi

echo ""
echo "===== Running Processes ====="

for proc in Amphetamine Maccy Docker 1Password; do
  if pgrep -x "$proc" &>/dev/null; then
    ok "$proc running"
  else
    warn "$proc not running"
  fi
done

echo ""
echo "===== Amphetamine Session ====="

if pmset -g assertions 2>/dev/null | grep -q "Amphetamine"; then
  ok "Amphetamine sleep assertion active"
else
  warn "No active Amphetamine sleep assertion"
fi

echo ""
echo "===== System Settings ====="

# File descriptors -- handle "unlimited" and non-numeric values
fd_limit=$(ulimit -n 2>/dev/null || echo "unknown")
if num_gte "$fd_limit" 65536; then
  ok "File descriptor limit: $fd_limit"
else
  warn "File descriptor limit: $fd_limit (recommend 65536)"
fi

# Key repeat
key_repeat=$(read_default "-g" "KeyRepeat" "not set")
if [ "$key_repeat" = "1" ]; then
  ok "Key repeat: fastest ($key_repeat)"
else
  warn "Key repeat: $key_repeat (recommend 1)"
fi

# Dock autohide delay -- defaults read returns float, compare as string
dock_delay=$(read_default "com.apple.dock" "autohide-delay" "not set")
case "$dock_delay" in
  0|0.0) ok "Dock autohide delay: instant" ;;
  *)     warn "Dock autohide delay: $dock_delay (recommend 0)" ;;
esac

# Spaces rearrange
mru=$(read_default "com.apple.dock" "mru-spaces" "not set")
case "$mru" in
  0|false) ok "Spaces auto-rearrange: disabled" ;;
  *)       warn "Spaces auto-rearrange: $mru (recommend disabled)" ;;
esac

# SSH
if grep -q "ControlMaster" "$HOME/.ssh/config" 2>/dev/null; then
  ok "SSH connection persistence configured"
else
  warn "SSH connection persistence not configured"
fi

echo ""
echo "===== Docker Resources ====="
if docker info &>/dev/null; then
  mem=$(docker info --format '{{.MemTotal}}' 2>/dev/null || echo "0")
  if [ "$mem" != "0" ] && command -v bc &>/dev/null; then
    mem_gb=$(echo "scale=1; $mem / 1073741824" | bc)
    ok "Docker memory limit: ${mem_gb}GB"
  else
    ok "Docker running (memory info unavailable)"
  fi
  cpus=$(docker info --format '{{.NCPU}}' 2>/dev/null || echo "unknown")
  ok "Docker CPUs: $cpus"
else
  warn "Docker daemon not running"
fi

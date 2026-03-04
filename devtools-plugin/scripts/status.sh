#!/usr/bin/env bash
set -euo pipefail

# devtools status checker -- reports on installed tools and system config

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ok()   { printf "${GREEN}[OK]${NC}   %s\n" "$1"; }
warn() { printf "${YELLOW}[WARN]${NC} %s\n" "$1"; }
err()  { printf "${RED}[MISS]${NC} %s\n" "$1"; }

echo "===== App Store Apps ====="

declare -A MAS_APPS=(
  [937984704]="Amphetamine"
  [1527619437]="Maccy"
  [1006087419]="SnippetsLab"
  [584653203]="RapidAPI"
  [1551292695]="Proxyman"
  [1465448609]="TablePlus"
  [1576121509]="OK JSON"
  [1152747299]="Figma"
  [1423210932]="Flow"
  [1333542190]="1Password"
)

installed=$(mas list 2>/dev/null | awk '{print $1}')
for app_id in "${!MAS_APPS[@]}"; do
  app_name="${MAS_APPS[$app_id]}"
  if echo "$installed" | grep -q "^${app_id}$"; then
    ok "$app_name"
  else
    err "$app_name (mas install $app_id)"
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
  ok "1Password CLI ($(op --version 2>/dev/null))"
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

# File descriptors
fd_limit=$(ulimit -n 2>/dev/null)
if [ "$fd_limit" -ge 65536 ] 2>/dev/null; then
  ok "File descriptor limit: $fd_limit"
else
  warn "File descriptor limit: $fd_limit (recommend 65536)"
fi

# Key repeat
key_repeat=$(defaults read -g KeyRepeat 2>/dev/null || echo "unknown")
if [ "$key_repeat" = "1" ]; then
  ok "Key repeat: fastest ($key_repeat)"
else
  warn "Key repeat: $key_repeat (recommend 1)"
fi

# Dock
dock_delay=$(defaults read com.apple.dock autohide-delay 2>/dev/null || echo "unknown")
if [ "$dock_delay" = "0" ]; then
  ok "Dock autohide delay: instant"
else
  warn "Dock autohide delay: $dock_delay (recommend 0)"
fi

mru=$(defaults read com.apple.dock mru-spaces 2>/dev/null || echo "unknown")
if [ "$mru" = "0" ]; then
  ok "Spaces auto-rearrange: disabled"
else
  warn "Spaces auto-rearrange: enabled (recommend disabled)"
fi

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
  mem_gb=$(echo "scale=1; $mem / 1073741824" | bc 2>/dev/null || echo "unknown")
  ok "Docker memory limit: ${mem_gb}GB"
  cpus=$(docker info --format '{{.NCPU}}' 2>/dev/null || echo "unknown")
  ok "Docker CPUs: $cpus"
else
  warn "Docker daemon not running"
fi

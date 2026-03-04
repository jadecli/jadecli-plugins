#!/usr/bin/env bash
set -euo pipefail

# devtools doctor -- diagnose issues with dev environment

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

issues=0
ok()   { printf "${GREEN}[PASS]${NC} %s\n" "$1"; }
warn() { printf "${YELLOW}[WARN]${NC} %s\n" "$1"; issues=$((issues + 1)); }
fail() { printf "${RED}[FAIL]${NC} %s\n" "$1"; issues=$((issues + 1)); }

echo "===== Disk Space ====="
free_gb=$(df -g / | awk 'NR==2 {print $4}')
if [ "$free_gb" -ge 20 ]; then
  ok "Free disk space: ${free_gb}GB (>= 20GB for healthy swap)"
else
  fail "Free disk space: ${free_gb}GB (< 20GB -- swap performance degraded)"
fi

echo ""
echo "===== Memory Pressure ====="
pressure=$(memory_pressure 2>/dev/null | grep "System-wide" | head -1 || echo "unknown")
if echo "$pressure" | grep -q "normal"; then
  ok "Memory pressure: normal"
elif echo "$pressure" | grep -q "warn"; then
  warn "Memory pressure: warning -- consider closing unused apps"
else
  fail "Memory pressure: critical -- close apps or increase RAM budget"
fi

echo ""
echo "===== Amphetamine Config ====="
start_at_launch=$(defaults read com.if.Amphetamine "Start Session At Launch" 2>/dev/null || echo "unset")
closed_display=$(defaults read com.if.Amphetamine "Allow Closed-Display Sleep" 2>/dev/null || echo "unset")
default_dur=$(defaults read com.if.Amphetamine "Default Duration" 2>/dev/null || echo "unset")

[ "$start_at_launch" = "1" ] && ok "Start Session At Launch: on" || warn "Start Session At Launch: $start_at_launch (should be 1)"
[ "$closed_display" = "0" ] && ok "Allow Closed-Display Sleep: blocked" || warn "Allow Closed-Display Sleep: $closed_display (should be 0)"
[ "$default_dur" = "0" ] && ok "Default Duration: indefinite" || warn "Default Duration: $default_dur (should be 0/indefinite)"

echo ""
echo "===== Docker Health ====="
if docker info &>/dev/null; then
  ok "Docker daemon running"

  # Check if Docker memory is capped
  mem=$(docker info --format '{{.MemTotal}}' 2>/dev/null || echo "0")
  mem_gb=$(echo "scale=0; $mem / 1073741824" | bc 2>/dev/null || echo "0")
  total_mem_gb=$(sysctl -n hw.memsize 2>/dev/null | awk '{printf "%d", $1/1073741824}')
  ratio=$(echo "scale=2; $mem_gb / $total_mem_gb" | bc 2>/dev/null || echo "0")

  if (( $(echo "$ratio > 0.75" | bc -l 2>/dev/null || echo 0) )); then
    warn "Docker using ${mem_gb}GB of ${total_mem_gb}GB RAM (${ratio}x) -- consider capping in Docker Desktop > Resources"
  else
    ok "Docker memory: ${mem_gb}GB of ${total_mem_gb}GB (${ratio}x)"
  fi
else
  warn "Docker daemon not running"
fi

echo ""
echo "===== Spotlight Indexing ====="
dev_dirs=("$HOME/dev" "$HOME/projects" "$HOME/src" "$HOME/llms")
for dir in "${dev_dirs[@]}"; do
  if [ -d "$dir" ]; then
    status=$(mdutil -s "$dir" 2>/dev/null | grep -o "Indexing enabled" || echo "disabled")
    if [ "$status" = "Indexing enabled" ]; then
      warn "Spotlight indexing ON for $dir -- run: sudo mdutil -i off $dir"
    else
      ok "Spotlight indexing off for $dir"
    fi
  fi
done

echo ""
echo "===== Summary ====="
if [ "$issues" -eq 0 ]; then
  ok "No issues found"
else
  warn "$issues issue(s) found"
fi

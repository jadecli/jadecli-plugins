#!/usr/bin/env bash
set -euo pipefail

# devtools doctor -- diagnose issues with dev environment

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

issues=0
ok()   { printf "${GREEN}[PASS]${NC} %s\n" "$1"; }
warn() { printf "${YELLOW}[WARN]${NC} %s\n" "$1"; issues=$((issues + 1)); }
fail() { printf "${RED}[FAIL]${NC} %s\n" "$1"; issues=$((issues + 1)); }

echo "===== Disk Space ====="
free_gb=$(df -g / | awk 'NR==2 {print $4}')
if num_gte "$free_gb" 20; then
  ok "Free disk space: ${free_gb}GB (>= 20GB for healthy swap)"
else
  fail "Free disk space: ${free_gb}GB (< 20GB -- swap performance degraded)"
fi

echo ""
echo "===== Memory Pressure ====="
# memory_pressure may not exist on all macOS versions; use vm_stat as fallback
if command -v memory_pressure &>/dev/null; then
  pressure=$(memory_pressure 2>/dev/null | grep "System-wide" | head -1 || echo "")
  if echo "$pressure" | grep -q "normal"; then
    ok "Memory pressure: normal"
  elif echo "$pressure" | grep -q "warn"; then
    warn "Memory pressure: warning -- consider closing unused apps"
  elif [ -n "$pressure" ]; then
    fail "Memory pressure: critical -- close apps or increase RAM budget"
  else
    warn "Memory pressure: unable to read"
  fi
else
  # Fallback: check pageouts from vm_stat
  pageouts=$(vm_stat 2>/dev/null | awk '/Pageouts/ {gsub(/\./, "", $2); print $2}' || echo "0")
  if num_gte "$pageouts" 100000; then
    warn "High pageout count ($pageouts) -- system under memory pressure"
  else
    ok "Pageout count normal ($pageouts)"
  fi
fi

echo ""
echo "===== Amphetamine Config ====="
start_at_launch=$(read_default "com.if.Amphetamine" "Start Session At Launch" "unset")
closed_display=$(read_default "com.if.Amphetamine" "Allow Closed-Display Sleep" "unset")
default_dur=$(read_default "com.if.Amphetamine" "Default Duration" "unset")

[ "$start_at_launch" = "1" ] && ok "Start Session At Launch: on" || warn "Start Session At Launch: $start_at_launch (should be 1)"
[ "$closed_display" = "0" ] && ok "Allow Closed-Display Sleep: blocked" || warn "Allow Closed-Display Sleep: $closed_display (should be 0)"
[ "$default_dur" = "0" ] && ok "Default Duration: indefinite" || warn "Default Duration: $default_dur (should be 0/indefinite)"

echo ""
echo "===== Docker Health ====="
if docker info &>/dev/null; then
  ok "Docker daemon running"

  mem=$(docker info --format '{{.MemTotal}}' 2>/dev/null || echo "0")
  total_mem=$(sysctl -n hw.memsize 2>/dev/null || echo "0")

  if [ "$mem" != "0" ] && [ "$total_mem" != "0" ] && command -v bc &>/dev/null; then
    mem_gb=$(echo "scale=0; $mem / 1073741824" | bc)
    total_mem_gb=$(echo "scale=0; $total_mem / 1073741824" | bc)
    # Integer percentage to avoid bc float comparison issues
    pct=$(echo "scale=0; $mem * 100 / $total_mem" | bc)

    if [ "$pct" -gt 75 ]; then
      warn "Docker using ${mem_gb}GB of ${total_mem_gb}GB RAM (${pct}%) -- consider capping in Docker Desktop > Resources"
    else
      ok "Docker memory: ${mem_gb}GB of ${total_mem_gb}GB (${pct}%)"
    fi
  else
    ok "Docker running (memory details unavailable)"
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

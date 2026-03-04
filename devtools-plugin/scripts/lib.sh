#!/usr/bin/env bash
# Shared library for devtools scripts

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# App registry: "app_store_id:app_name:app_path"
# Using indexed arrays for bash 3.2 compatibility (macOS default)
APPS=(
  "937984704:Amphetamine:/Applications/Amphetamine.app"
  "1527619437:Maccy:/Applications/Maccy.app"
  "1006087419:SnippetsLab:/Applications/SnippetsLab.app"
  "584653203:RapidAPI:/Applications/RapidAPI.app"
  "1551292695:Proxyman:/Applications/Proxyman.app"
  "1465448609:TablePlus:/Applications/TablePlus.app"
  "1576121509:OK JSON:/Applications/OK JSON.app"
  "1152747299:Figma:/Applications/Figma.app"
  "1423210932:Flow:/Applications/Flow.app"
  "1333542190:1Password:/Applications/1Password.app"
)

# Parse app entry fields
app_id()   { echo "$1" | cut -d: -f1; }
app_name() { echo "$1" | cut -d: -f2; }
app_path() { echo "$1" | cut -d: -f3-; }

# Check if app is installed (mas list OR /Applications/ fallback)
app_installed() {
  local id name path
  id=$(app_id "$1")
  name=$(app_name "$1")
  path=$(app_path "$1")

  # Check mas list first
  if [ -n "$MAS_INSTALLED" ] && echo "$MAS_INSTALLED" | grep -q "^${id} "; then
    return 0
  fi
  # Fallback: check /Applications
  if [ -d "$path" ]; then
    return 0
  fi
  return 1
}

# Cache mas list output (call once at script start)
cache_mas_list() {
  MAS_INSTALLED=$(mas list 2>/dev/null || echo "")
  export MAS_INSTALLED
}

# Safe defaults read with fallback
read_default() {
  local domain="$1" key="$2" fallback="${3:-unset}"
  defaults read "$domain" "$key" 2>/dev/null || echo "$fallback"
}

# Safe numeric comparison (handles "unlimited", empty, non-numeric)
num_gte() {
  local val="$1" threshold="$2"
  case "$val" in
    unlimited) return 0 ;;
    ''|*[!0-9]*) return 1 ;;
    *) [ "$val" -ge "$threshold" ] ;;
  esac
}

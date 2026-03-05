#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SDK_DIR="$(dirname "$SCRIPT_DIR")"

cd "$SDK_DIR"

if [ ! -d "node_modules" ]; then
  echo "Installing dependencies..."
  npm install --silent
fi

exec npx tsx src/orchestrator.ts "$@"

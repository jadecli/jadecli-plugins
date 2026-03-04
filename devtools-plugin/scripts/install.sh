#!/usr/bin/env bash
set -euo pipefail

# devtools installer -- installs and configures macOS dev tools for Claude Code workflows

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

log_ok()   { printf "${GREEN}[OK]${NC} %s\n" "$1"; }
log_warn() { printf "${YELLOW}[WARN]${NC} %s\n" "$1"; }
log_err()  { printf "${RED}[ERR]${NC} %s\n" "$1"; }
log_info() { printf "[INFO] %s\n" "$1"; }

# ── Dependency check ──────────────────────────────────────────────────────────

ensure_brew() {
  if ! command -v brew &>/dev/null; then
    log_err "Homebrew not installed. Install from https://brew.sh"
    exit 1
  fi
  log_ok "Homebrew available"
}

ensure_mas() {
  if ! command -v mas &>/dev/null; then
    log_info "Installing mas (Mac App Store CLI)..."
    brew install mas
  fi
  log_ok "mas available"
}

# ── App Store installs ────────────────────────────────────────────────────────

install_mas_apps() {
  log_info "Installing App Store apps..."
  cache_mas_list

  for entry in "${APPS[@]}"; do
    local id name
    id=$(app_id "$entry")
    name=$(app_name "$entry")

    if app_installed "$entry"; then
      log_ok "$name already installed"
    else
      log_info "Installing $name ($id)..."
      if mas install "$id" 2>/dev/null; then
        log_ok "$name installed"
      else
        log_warn "Failed to install $name -- may need manual App Store sign-in"
      fi
    fi
  done
}

# ── Brew installs ─────────────────────────────────────────────────────────────

install_brew_tools() {
  log_info "Installing Homebrew tools..."

  if [ -d "/Applications/Docker.app" ]; then
    log_ok "Docker Desktop already installed"
  else
    log_info "Installing Docker Desktop..."
    brew install --cask docker
    log_ok "Docker Desktop installed"
  fi

  if command -v op &>/dev/null; then
    log_ok "1Password CLI already installed"
  else
    log_info "Installing 1Password CLI..."
    brew install --cask 1password-cli
    log_ok "1Password CLI installed"
  fi
}

# ── macOS defaults ────────────────────────────────────────────────────────────

configure_amphetamine() {
  log_info "Configuring Amphetamine..."
  defaults write com.if.Amphetamine "Start Session At Launch" -int 1
  defaults write com.if.Amphetamine "Allow Closed-Display Sleep" -int 0
  defaults write com.if.Amphetamine "Default Duration" -int 0
  defaults write com.if.Amphetamine "Hide Dock Icon" -int 1
  defaults write com.if.Amphetamine "Allow Display Sleep" -int 0
  log_ok "Amphetamine configured"
}

configure_dock() {
  log_info "Configuring Dock..."
  defaults write com.apple.dock autohide-delay -float 0
  defaults write com.apple.dock autohide-time-modifier -float 0.15
  defaults write com.apple.dock show-recents -bool false
  defaults write com.apple.dock mru-spaces -bool false
  killall Dock 2>/dev/null || true
  log_ok "Dock configured"
}

configure_keyboard() {
  log_info "Configuring keyboard repeat rate..."
  defaults write -g KeyRepeat -int 1
  defaults write -g InitialKeyRepeat -int 10
  log_ok "Keyboard configured (requires logout to take effect)"
}

# ── Shell environment ─────────────────────────────────────────────────────────

configure_shell() {
  local zshrc="$HOME/.zshrc"

  log_info "Configuring shell environment..."

  # Ensure .zshrc exists
  touch "$zshrc"

  # File descriptor limit
  if ! grep -q "ulimit -n 65536" "$zshrc"; then
    printf '\n# devtools: increased file descriptor limit\nulimit -n 65536\n' >> "$zshrc"
    log_ok "Added ulimit to ~/.zshrc"
  else
    log_ok "ulimit already configured"
  fi

  # 1Password SSH agent
  local op_sock="$HOME/Library/Group Containers/2BUA8C4S2C.com.1password/t/agent.sock"
  if [ -S "$op_sock" ] && ! grep -q "SSH_AUTH_SOCK.*1password" "$zshrc"; then
    printf '\n# devtools: 1Password SSH agent\nexport SSH_AUTH_SOCK="%s"\n' "$op_sock" >> "$zshrc"
    log_ok "Added 1Password SSH agent to ~/.zshrc"
  else
    log_ok "SSH agent already configured or 1Password not set up"
  fi
}

# ── SSH config ────────────────────────────────────────────────────────────────

configure_ssh() {
  local ssh_config="$HOME/.ssh/config"
  local ssh_sockets="$HOME/.ssh/sockets"

  log_info "Configuring SSH persistence..."

  mkdir -p "$HOME/.ssh" "$ssh_sockets"
  chmod 700 "$HOME/.ssh" "$ssh_sockets"

  if ! grep -q "ControlMaster" "$ssh_config" 2>/dev/null; then
    cat >> "$ssh_config" <<'SSHEOF'

# devtools: SSH connection persistence
Host *
  ServerAliveInterval 60
  ServerAliveCountMax 10
  ControlMaster auto
  ControlPath ~/.ssh/sockets/%r@%h:%p
  ControlPersist 600
SSHEOF
    chmod 600 "$ssh_config"
    log_ok "SSH persistence configured"
  else
    log_ok "SSH persistence already configured"
  fi
}

# ── Login items ───────────────────────────────────────────────────────────────

configure_login_items() {
  log_info "Checking login items..."
  local current_items
  current_items=$(osascript -e 'tell application "System Events" to get the name of every login item' 2>/dev/null || echo "")

  local login_apps=("Amphetamine" "Maccy" "Docker" "1Password")
  for app in "${login_apps[@]}"; do
    if echo "$current_items" | grep -qi "$app"; then
      log_ok "$app already in login items"
    else
      local app_path="/Applications/${app}.app"
      if [ -d "$app_path" ]; then
        osascript -e "tell application \"System Events\" to make login item at end with properties {path:\"$app_path\", hidden:false}" 2>/dev/null && \
          log_ok "Added $app to login items" || \
          log_warn "Could not add $app to login items"
      fi
    fi
  done
}

# ── Main ──────────────────────────────────────────────────────────────────────

main() {
  echo "=========================================="
  echo " devtools installer"
  echo " macOS dev tools for Claude Code"
  echo "=========================================="
  echo ""

  ensure_brew
  ensure_mas

  echo ""
  install_mas_apps

  echo ""
  install_brew_tools

  echo ""
  configure_amphetamine
  configure_dock
  configure_keyboard

  echo ""
  configure_shell
  configure_ssh

  echo ""
  configure_login_items

  echo ""
  echo "=========================================="
  echo " Installation complete"
  echo "=========================================="
  echo ""
  echo "Next steps:"
  echo "  1. Log out and back in for keyboard settings"
  echo "  2. Open Amphetamine to start a session"
  echo "  3. Run 'op signin' to set up 1Password CLI"
  echo "  4. Open Docker Desktop to complete setup"
  echo "  5. Run 'devtools:status' to verify everything"
}

main "$@"

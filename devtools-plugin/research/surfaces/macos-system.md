# macOS System Surface

System-level tweaks that affect all development tooling.

## File Descriptor Limits

Default soft limit is 256. Running Docker + Node + Claude Code hits this fast.

```bash
# Per-session (add to ~/.zshrc)
ulimit -n 65536

# Persistent LaunchDaemon
sudo tee /Library/LaunchDaemons/limit.maxfiles.plist > /dev/null <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>limit.maxfiles</string>
    <key>ProgramArguments</key>
    <array>
      <string>launchctl</string>
      <string>limit</string>
      <string>maxfiles</string>
      <string>65536</string>
      <string>2147483647</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
  </dict>
</plist>
EOF
sudo chown root:wheel /Library/LaunchDaemons/limit.maxfiles.plist
sudo chmod 644 /Library/LaunchDaemons/limit.maxfiles.plist
sudo launchctl load -w /Library/LaunchDaemons/limit.maxfiles.plist
```

## Reduce Visual Overhead

System Settings > Accessibility > Display:

- Enable Reduce Motion (cuts WindowServer CPU during workspace switching)
- Enable Reduce Transparency (eliminates Vibrancy blur recalculation)

System Settings > Desktop & Dock:

- Minimize using Scale Effect (faster than Genie)
- Disable Magnification

## Spotlight Indexing

Disable for dev directories to stop re-indexing node_modules/.git:

```bash
sudo mdutil -i off ~/dev
```

## Key Repeat Rate

```bash
defaults write -g KeyRepeat -int 1
defaults write -g InitialKeyRepeat -int 10
# Requires logout/login
```

## Touch ID for sudo

```bash
# /etc/pam.d/sudo_local -- persists across macOS updates on Sequoia+
auth       sufficient     pam_tid.so
```

## Memory Management

- Keep 20GB+ free SSD space for swap performance
- Cap Docker Desktop memory in Settings > Resources
- Do not use third-party memory cleaners

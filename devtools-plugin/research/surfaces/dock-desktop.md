# Dock and Desktop Surface

Dock behavior, Spaces, and window management optimizations.

## Dock Optimization

```bash
# Instant autohide
defaults write com.apple.dock autohide-delay -float 0
defaults write com.apple.dock autohide-time-modifier -float 0.15

# Remove recent apps clutter
defaults write com.apple.dock show-recents -bool false

killall Dock
```

## Spaces / Mission Control

```bash
# Prevent automatic Space rearrangement (preserves Ctrl+N muscle memory)
defaults write com.apple.dock mru-spaces -bool false
killall Dock
```

System Settings > Desktop & Dock > Mission Control:

- Uncheck "Automatically rearrange Spaces based on most recent use"

## Rectangle (Already Installed)

- Window snapping and tiling via keyboard shortcuts
- Claude Code relevance: split terminal + browser + editor across screen halves/quarters

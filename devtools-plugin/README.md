# devtools-plugin

macOS developer tooling installer and configurator optimized for Claude Code + monetizable web app development.

## Commands

- `/devtools:setup` -- Install and configure all recommended dev tools
- `/devtools:status` -- Check installation and configuration status of all tools
- `/devtools:doctor` -- Diagnose issues with installed tools and system settings
- `/devtools:update` -- Update all managed tools

## What It Manages

### App Store Apps (via mas)
- Amphetamine -- prevent sleep during long sessions
- Maccy -- clipboard history
- SnippetsLab -- code snippet manager
- RapidAPI (Paw) -- HTTP client
- Proxyman -- network debugger
- TablePlus -- database GUI
- OK JSON -- JSON viewer
- Figma -- UI design
- Flow -- focus timer

### System Tools
- 1Password + CLI -- secrets and SSH management
- Docker Desktop -- container runtime

### macOS System Settings
- File descriptor limits
- Key repeat rate
- Dock optimization
- Spotlight indexing exclusions
- SSH connection persistence
- Touch ID for sudo

## Research

See `research/` for detailed documentation organized by:
- **Device surface** (system, menubar, dock, terminal, network, storage)
- **Claude Code entry point** (CLI, MCP, hooks, skills)
- **Service manifests** (per-tool JSON specs)

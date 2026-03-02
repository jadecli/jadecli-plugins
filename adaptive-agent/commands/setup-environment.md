---
description: "Detect the current Claude Code surface and configure the project environment with preview servers, tooling verification, and surface-specific recommendations."
args:
  - name: surface
    description: "Override surface detection (auto | cli | desktop | vscode | web | ci)"
    required: false
    default: "auto"
---

# Set Up Environment

Configure this project for the detected (or specified) Claude Code surface.

## 1. Detect Surface

If `surface` arg is `auto` (default), check environment signals in this order:

```bash
# First match wins
[ "$GITHUB_ACTIONS" = "true" ] && SURFACE="github-actions"
[ "$GITLAB_CI" = "true" ] && SURFACE="gitlab-ci"
[ "$CLAUDE_CODE_REMOTE" = "true" ] && SURFACE="web"
[ -n "$VSCODE_VERSION" ] && SURFACE="vscode"
# JetBrains: check for IDE-specific context
# TTY present, no IDE/CI → CLI (primary surface)
# No TTY, no CI → Desktop (GUI default)
```

If arg is not `auto`, use the specified surface directly.

Report: `Detected surface: [surface]`

## 2. Detect Project Type

Scan for project configuration files to identify the dev stack:

```bash
# Check each in order
[ -f "package.json" ] && echo "Node.js project"
[ -f "Cargo.toml" ] && echo "Rust project"
[ -f "go.mod" ] && echo "Go project"
[ -f "pyproject.toml" ] || [ -f "setup.py" ] && echo "Python project"
[ -f "Makefile" ] && echo "Make-based project"
[ -f "Gemfile" ] && echo "Ruby project"
[ -f "pom.xml" ] || [ -f "build.gradle" ] && echo "Java project"
```

For Node.js projects, read `package.json` scripts to find the dev server command
and detect the framework (Next.js, Vite, Express, etc.).

## 3. Surface-Specific Setup

### CLI / Desktop / IDE Surfaces

1. **Create `.claude/launch.json`** if a dev server is detected:

```json
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "[project-name]",
      "runtimeExecutable": "[detected: npm|yarn|pnpm]",
      "runtimeArgs": ["[detected: run dev|start|serve]"],
      "port": "[detected: 3000|5173|8080|4000]"
    }
  ]
}
```

For monorepos with multiple `package.json` files, create multiple configurations
with appropriate `cwd` paths.

2. **Verify Git** — required for worktree-based session isolation:

```bash
git --version
```

3. **Verify `gh` CLI** — required for PR monitoring with auto-fix and auto-merge:

```bash
gh --version
gh auth status
```

### Web / Remote Surface

1. **Check for SessionStart hook** in `.claude/settings.json` or project hooks.
   If missing, suggest creating one for automatic dependency installation:

```
No SessionStart hook found. For remote sessions, create a hook to install
dependencies automatically. See: /adaptive-agent:bootstrap for project discovery.
```

2. **Verify `.claude/launch.json`** exists — preview works in remote sessions too.

### GitHub Actions / GitLab CI Surface

1. **Check for Claude workflow** in `.github/workflows/` or `.gitlab-ci.yml`
2. **Verify API key reference** — look for `ANTHROPIC_API_KEY` in workflow files
3. **Check for cost controls** — `--max-turns` or `--max-budget-usd` flags

## 4. Check Shared Configuration

These apply to all surfaces:

```bash
# CLAUDE.md — project conventions
[ -f "CLAUDE.md" ] && echo "CLAUDE.md: found" || echo "CLAUDE.md: missing — run /adaptive-agent:bootstrap"

# MCP servers
[ -f ".mcp.json" ] && echo "MCP servers: project config found"

# Hooks
[ -f "adaptive-agent/hooks/hooks.json" ] && echo "Hooks: git safety active"

# Settings
[ -f ".claude/settings.json" ] && echo "Settings: project settings found"
```

## 5. Output Summary

Print a structured environment report:

```
## Surface: [detected surface]

### Environment
- Git: [version] ✓ / ✗ (required for worktrees)
- gh CLI: [version] ✓ / ✗ (required for PR monitoring)
- Runtime: [node/python/rust/go version]
- Remote Control: available (run /rc to connect from phone)

### Preview
- launch.json: [created at .claude/launch.json | already exists | no dev server detected]
- Dev server: [command] (port [port])
- Auto-verify: enabled (default)

### Shared Config
- CLAUDE.md: [found ✓ | missing — run /adaptive-agent:bootstrap]
- MCP servers: [count] configured
- Hooks: [list active hooks]
- Skills: [count] loaded

### Recommendations
- Permission mode: [suggestion based on project size and surface]
  - Small project + familiar → Auto accept edits
  - Large project + unfamiliar → Plan mode first
  - CI/CD → Non-interactive with --max-turns
- Parallel sessions: [worktrees available | Git not installed]
- Mobile access: Run `/rc` to continue from phone via Remote Control
- [additional surface-specific tips]
```

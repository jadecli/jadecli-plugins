---
name: Surface Awareness
description: >
  Activate at session start and whenever platform-specific features are relevant.
  Detects the current Claude Code surface (CLI, Desktop, VS Code, JetBrains,
  Web/Remote, GitHub Actions, GitLab CI) and provides context-appropriate best
  practices, permission mode guidance, and workflow patterns. CLI/Terminal is
  the primary surface; Desktop is the default assumption for GUI contexts.
version: 1.0.0
---

# Surface Awareness

## Detect the Current Surface

Check these signals in order. First match wins.

| Signal | Surface | Assumption |
| -------- | --------- | ------------ |
| `GITHUB_ACTIONS=true` | GitHub Actions CI/CD | Headless, PR-output oriented |
| `GITLAB_CI=true` | GitLab CI/CD | Headless, MR-output oriented |
| `CLAUDE_CODE_REMOTE=true` | Web / Remote session | Auto-accept, sandboxed VM |
| `VSCODE_VERSION` set | VS Code Extension | IDE-integrated, inline diffs |
| JetBrains IDE context detected | JetBrains Extension | IDE-integrated |
| TTY attached, no IDE/CI signals | **CLI / Terminal** (primary) | Full feature access |
| No TTY, no CI signals | **Desktop** (GUI default) | Graphical interface |

When ambiguous, prefer CLI if a TTY is present, Desktop otherwise.

---

## CLI / Terminal (Primary Surface)

The CLI is the most capable surface. Every feature is available here.

### Session Lifecycle

```bash
claude                          # Interactive session
claude "query"                  # Start with prompt
claude -p "query"               # Non-interactive (SDK/scripting)
claude -c                       # Continue most recent conversation
claude -r "session-name"        # Resume by name or ID
claude -w feature-auth          # Isolated git worktree session
```

### Permission Modes

| Mode | Flag | When to Use |
| ------ | ------ | ------------- |
| Ask (default) | `--permission-mode default` | Unfamiliar codebases, security-sensitive |
| Auto accept edits | `--permission-mode acceptEdits` | Trusted projects, faster iteration |
| Plan | `--permission-mode plan` | Complex tasks — explore first, then execute |
| Don't ask | `--permission-mode dontAsk` | **CLI-only** — fully autonomous local work |
| Bypass | `--dangerously-skip-permissions` | Sandboxed containers/VMs only |

Best practice: start complex tasks in Plan mode, switch to Auto accept edits
once the approach is confirmed.

### CLI-Only Features

- `!command` bash shortcut — execute shell commands inline
- Tab completion for commands and file paths
- `/thinking` toggle for extended thinking per-session
- `--output-format stream-json` for piping to other tools
- `--max-turns` and `--max-budget-usd` for cost control in automation
- `--agents` flag for dynamic subagent definitions
- `--system-prompt` / `--append-system-prompt` for prompt customization
- `--json-schema` for structured output validation
- `--worktree` / `-w` for parallel Git-isolated sessions
- `--fallback-model` for automatic model failover

### Remote Control — Continue from Phone or Browser

Remote Control lets you continue a local CLI session from any device (iPhone,
Android, browser) without moving anything to the cloud. Your local environment,
MCP servers, tools, and files stay where they are.

**Start a Remote Control session:**

```bash
# New session with remote access
claude remote-control

# From inside an existing session
/remote-control    # or /rc
```

The terminal displays a session URL and a QR code (press spacebar to toggle).
Connect from another device by:

1. Opening the URL in any browser → goes to claude.ai/code
2. Scanning the QR code → opens in Claude iOS/Android app
3. Finding the session by name in claude.ai/code or the Claude app (green dot = online)

**Key behaviors:**

- One remote connection per session
- Terminal must stay open (local process)
- Auto-reconnects after network interruptions (times out after ~10 minutes offline)
- `/rename` the session before `/rc` so it's easy to find on mobile
- Enable for all sessions: `/config` → "Enable Remote Control for all sessions" → `true`

**Remote Control vs Cloud sessions:**

| | Remote Control | `--remote` / Web |
| -- | --------------- | ----------------- |
| Runs on | Your machine | Anthropic cloud |
| Local tools | Available | Not available |
| MCP servers | Available | Not available |
| Survives laptop close | No | Yes |
| Multi-repo | No | Yes |

Use Remote Control when you want mobile access to your local environment.
Use `--remote` when you want a task to run independently in the cloud.

### Cloud Offload

```bash
claude --remote "Fix the login bug"    # Start cloud session
claude --teleport                      # Pull cloud session back to local
```

### Cross-Surface Handoffs

| From | To | How |
| ------ | ----- | ----- |
| CLI → Desktop | `/desktop` | Saves session, opens in Desktop app |
| CLI → Web | `--remote` | Offloads to Anthropic cloud |
| CLI → Phone/Browser | `/remote-control` or `/rc` | Remote Control (stays local) |
| Web → CLI | `--teleport` or `/teleport` | Pull session to local terminal |
| CLI → IDE | `--ide` or `/ide` | Connects to VS Code/JetBrains |

---

## Desktop (GUI Default)

The Desktop app provides the same engine as CLI with a graphical interface.
Assume Desktop when no TTY or CI signal is detected.

### Session Startup

1. **Environment**: Local (your files), Remote (Anthropic cloud), or SSH (your servers)
2. **Folder**: select project directory
3. **Model**: pick from dropdown — locked once session starts
4. **Permission mode**: Ask permissions (default), Auto accept edits, Plan, Bypass

### Desktop-Specific Features

- **Visual diff review**: click the `+12 -1` indicator → file-by-file review → click any line to comment → Cmd/Ctrl+Enter to submit all comments
- **Review code button**: AI self-review focusing on compile errors, logic bugs, security — not style or formatting
- **Preview & auto-verify**: `.claude/launch.json` configures dev servers. Auto-verify takes screenshots, inspects DOM, fills forms after every edit. Set `"autoVerify": false` to disable
- **PR monitoring**: CI status bar after opening a PR. Auto-fix reads failure output and iterates. Auto-merge (squash). Requires `gh` CLI
- **Parallel sessions**: automatic Git worktree isolation in `<project>/.claude/worktrees/`
- **Connectors**: Slack, GitHub, Linear, Notion, Calendar via the + button
- **@mention autocomplete**: type `@filename` for file suggestions
- **Drag-and-drop**: attach images, PDFs directly to prompts
- **Continue in**: move session to Web or open in IDE

### Preview Configuration (`.claude/launch.json`)

```json
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "web",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "port": 3000
    }
  ]
}
```

Fields: `name`, `runtimeExecutable`, `runtimeArgs`, `port`, `cwd`, `env`,
`autoPort` (true = pick free port, false = fail if taken). `PORT` env var
passed to server when autoPort picks a different port.

### MCP Server Configuration

Desktop MCP servers use `~/.claude.json` or `.mcp.json` — **NOT**
`claude_desktop_config.json` (that file is for the Desktop chat app, not the
Code tab).

### Troubleshooting Quick Reference

| Problem | Fix |
| --------- | ----- |
| 403 / auth error | Sign out and back in |
| Blank or stuck screen | Restart app, check for updates |
| Tools not found (npm, node) | Verify shell PATH, restart app |
| Git errors on Windows | Install Git for Windows, restart |
| Git LFS required | `git lfs install`, restart |

---

## VS Code / JetBrains

Activated when IDE environment variables are detected (`VSCODE_VERSION`, etc.).

- Inline diff viewing with accept/reject UI
- Multiple conversation tabs in separate panels
- @-mentions with line ranges: `@file.ts#5-10`
- Permission modes via UI (Normal, Plan, Auto-accept, Bypass)
- Resume remote sessions directly in IDE
- Checkpoints — rewind to previous code states, fork conversation branches
- MCP servers configured via CLI apply in the extension
- `/ide` command connects a terminal Claude session to the IDE
- Chrome extension integration for browser testing (`--chrome`)

---

## Web / Remote Sessions

Activated when `CLAUDE_CODE_REMOTE=true`.

- Tasks continue even if you close the browser or app
- Multi-repo support (+ button to add repositories)
- Auto-accept edits by default (sandboxed VM)
- No Bypass permissions (already sandboxed)
- SessionStart hooks run on every start — use for dependency installation
- `CLAUDE_ENV_FILE` for persisting environment variables across commands
- Network access levels: No internet, Limited (allowlist), Full
- Pre-installed: Python, Node.js, Ruby, PHP, Java, Go, Rust, C++, PostgreSQL, Redis
- Git push restricted to current branch only (security proxy)
- Pull back to local: `--teleport` or `/teleport`

---

## GitHub Actions

Activated when `GITHUB_ACTIONS=true`.

- `@claude` mention triggers in issue/PR comments
- API key via `ANTHROPIC_API_KEY` repository secret
- `--max-turns` to prevent runaway costs
- PR is the primary output artifact
- CLAUDE.md is respected for project conventions
- `anthropics/claude-code-action@v1` for workflow integration
- OIDC authentication for Bedrock/Vertex (no static credentials needed)
- Read-only tools recommended for review: `Read,Grep,Glob`

---

## GitLab CI

Activated when `GITLAB_CI=true`.

- Merge Request is the primary output artifact
- CI/CD variables for API key storage
- Similar patterns to GitHub Actions

---

## Shared Across All Surfaces

All surfaces read the same configuration:

- **CLAUDE.md** and **CLAUDE.local.md** — project conventions
- **MCP servers** — `~/.claude.json` or `.mcp.json`
- **Hooks** and **Skills** — settings files
- **Settings** — `~/.claude.json` and `~/.claude/settings.json`
- **Models** — Sonnet, Opus, Haiku available everywhere

### Handoff Matrix

| From → To | Method |
| ----------- | -------- |
| CLI → Desktop | `/desktop` |
| CLI → Phone/Browser | `/remote-control` (local stays running) |
| CLI → Web (cloud) | `--remote` |
| Web → CLI | `--teleport` or `/teleport` |
| Web → Desktop | "Continue in" menu |
| Desktop → Web | "Continue in" → Claude Code on the Web |
| Desktop → IDE | "Continue in" → your IDE |
| IDE → CLI | Open integrated terminal |

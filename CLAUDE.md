# jadecli-plugins -- Claude Code Project Instructions

## Commit conventions

All commits MUST use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` -- new skill, command, agent, hook, or plugin
- `fix:` -- bug fix in existing component
- `chore:` -- CI, templates, config, non-functional changes
- `docs:` -- documentation only

Examples:

- `feat: add deployment safety skill`
- `fix: correct git-safety hook pattern matching`
- `chore: update markdownlint config`

## Plugin structure

Each plugin lives in its own top-level directory:

```text
plugin-name/
  .claude-plugin/
    plugin.json          # Required: name, version, description
  skills/                # Auto-activated knowledge
    skill-name/
      SKILL.md
  commands/              # User-invoked via /plugin-name:command
    command-name.md
  agents/                # Sub-agents for parallel work
    agent-name.md
  hooks/                 # Event-driven guards
    hooks.json
  README.md              # Plugin documentation
```

## Version bumps

Bump `version` in `plugin.json` on every meaningful change:

- Patch (0.0.x): bug fixes
- Minor (0.x.0): new skill/command/agent, backward compatible
- Major (x.0.0): breaking changes to existing skills/commands

Claude Code caches plugins -- changes without version bumps are not picked up.

## PR workflow

1. Branch from `main` (e.g., `feat/new-skill`, `fix/hook-pattern`)
2. Conventional commit messages
3. Squash-merge with PR title as commit message
4. Never commit directly to `main`

## Testing locally

```bash
claude --plugin-dir ./adaptive-agent
```

Verify skills auto-activate, commands appear in `/plugin-name:*`, and hooks fire correctly.

## Marketplace registration

When adding a new plugin, register it in `.claude-plugin/marketplace.json`:

```json
{
  "name": "plugin-name",
  "source": "./plugin-name",
  "description": "Brief description"
}
```

## Key files

- `.claude-plugin/marketplace.json` -- marketplace manifest (lists all plugins)
- `adaptive-agent/.claude-plugin/plugin.json` -- plugin metadata and version
- `adaptive-agent/hooks/hooks.json` -- git safety PreToolUse hook

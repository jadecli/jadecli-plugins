# Contributing to jadecli-plugins

## Commit conventions

All commits use [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | Use |
|--------|-----|
| `feat:` | New skill, command, agent, hook, or plugin |
| `fix:` | Bug fix in existing component |
| `chore:` | CI, templates, config, non-functional |
| `docs:` | Documentation only |

CI enforces this via commitlint on every PR.

## PR workflow

1. Branch from `main` with a descriptive name (`feat/new-skill`, `fix/hook-pattern`)
2. Make changes with conventional commit messages
3. Push and open a PR -- the PR template will guide you
4. PRs require passing CI checks + 1 approving review
5. Squash-merge with the PR title as the commit message

## Version bumps

Bump `version` in the relevant `plugin.json` on every meaningful change:

- **Patch** (0.0.x): bug fixes
- **Minor** (0.x.0): new skill/command/agent, backward compatible
- **Major** (x.0.0): breaking changes to existing skills/commands

Claude Code caches plugins. Without a version bump, users will not pick up changes.

## Plugin structure

Each plugin is a top-level directory:

```text
plugin-name/
  .claude-plugin/
    plugin.json          # name, version, description (required)
  skills/
    skill-name/
      SKILL.md           # Auto-activated knowledge
  commands/
    command-name.md      # User-invoked via /plugin-name:command
  agents/
    agent-name.md        # Sub-agents for parallel work
  hooks/
    hooks.json           # Event-driven guards
  README.md
```

## Adding a new plugin

1. Create a directory at the repo root (e.g., `jade-deploy/`)
2. Add `.claude-plugin/plugin.json`:

    ```json
    {
      "name": "jade-deploy",
      "version": "0.1.0",
      "description": "Deployment safety for jadecli projects"
    }
    ```

3. Add skills, commands, agents, hooks as needed
4. Register in `.claude-plugin/marketplace.json`:

    ```json
    {
      "name": "jade-deploy",
      "source": "./jade-deploy",
      "description": "Deployment safety for jadecli projects"
    }
    ```

5. Add a `README.md` in the plugin directory
6. Open a PR with `feat: add jade-deploy plugin`

## Testing locally

```bash
claude --plugin-dir ./plugin-name
```

Verify:

- Skills auto-activate on session start
- Commands appear via `/plugin-name:command-name`
- Hooks fire on the correct events
- No JSON parse errors in plugin.json or hooks.json

## Code review

All changes to the `adaptive-agent/` plugin require review from `@jadecli/core` (enforced via CODEOWNERS).

## Release process

Releases are automated via [release-please](https://github.com/googleapis/release-please). When conventional commits land on `main`, release-please opens a PR to bump the version and update `CHANGELOG.md`. Merging that PR creates a GitHub release with a git tag.

## Questions

Open a [Discussion](https://github.com/jadecli/jadecli-plugins/discussions) for general questions or use the issue templates for bugs, feature requests, and new plugin proposals.

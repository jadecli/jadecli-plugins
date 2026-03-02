# jadecli-plugins

Your team's Claude Code plugin marketplace. Packages the adaptive agent bootstrap,
cookbook-derived patterns, and jadecli-specific workflows as installable plugins.

## Quick Start

```bash
# In Claude Code CLI, add this marketplace
/plugin marketplace add jadecli/jadecli-plugins

# Install the adaptive agent plugin
/plugin install adaptive-agent@jadecli-plugins

# Also add Anthropic's knowledge-work plugins alongside
/plugin marketplace add anthropics/knowledge-work-plugins

# Install the ones relevant to your workflow
/plugin install productivity@knowledge-work-plugins
/plugin install product-management@knowledge-work-plugins
```

## What This Repo Is

This is a **Claude Code plugin marketplace** — a Git repo containing one or more
plugins that any team member can install with a single command. It's the version-controlled,
distributable form of everything from the adaptive agent research.

The research (XML bootstrap protocol, cookbook patterns, git safety layer) lives here
as **skills**, **commands**, **agents**, and **hooks** — the four plugin primitives
Claude Code understands natively.

## Repo Structure

```
jadecli-plugins/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace manifest (lists all plugins)
├── adaptive-agent/               # THE PLUGIN — everything from the research
│   ├── .claude-plugin/
│   │   └── plugin.json           # Plugin manifest
│   ├── skills/
│   │   ├── bootstrap/
│   │   │   └── SKILL.md          # Codebase reconnaissance (auto-activates)
│   │   ├── context-management/
│   │   │   └── SKILL.md          # Session compaction + memory patterns
│   │   ├── git-safety/
│   │   │   └── SKILL.md          # Stash/worktree/branch safety layer
│   │   ├── compounding-review/
│   │   │   └── SKILL.md          # 6-axis code review for integration quality
│   │   └── tool-orchestration/
│   │       └── SKILL.md          # PTC, parallel agents, structured extraction
│   ├── commands/
│   │   ├── bootstrap.md          # /adaptive-agent:bootstrap
│   │   ├── merge-prs.md          # /adaptive-agent:merge-prs
│   │   ├── review.md             # /adaptive-agent:review
│   │   └── safe-branch.md        # /adaptive-agent:safe-branch
│   ├── agents/
│   │   ├── codebase-reviewer.md  # Parallel review sub-agent
│   │   └── pr-merger.md          # PR chain merge sub-agent
│   ├── hooks/
│   │   └── hooks.json            # Git safety hooks
│   └── README.md
├── LICENSE
└── README.md                     # This file
```

## How It Maps to the Research

| Research Layer | Plugin Primitive | Why |
|---|---|---|
| Bootstrap (Phase 0) | **Skill** `bootstrap/` | Auto-activates on every session — Claude discovers the codebase before acting |
| Context Management | **Skill** `context-management/` | Auto-activates when context gets long — compaction, memory patterns |
| Git Safety | **Skill** `git-safety/` + **Hook** | Skill provides knowledge; hook enforces stash-before-write |
| PR Merge Protocol | **Command** `merge-prs.md` | Explicit invocation — merges are one-way doors |
| Codebase Review | **Command** `review.md` + **Agent** | Command triggers; agent does parallel analysis |
| Tool Patterns | **Skill** `tool-orchestration/` | Auto-activates — informs how Claude uses its own tools |
| Decision Boundaries | Encoded in all skills | Not a separate component — it's a cross-cutting concern |

## Relationship to knowledge-work-plugins

Anthropic's `knowledge-work-plugins` gives you **role-based** plugins (productivity,
product-management, sales, etc.) with MCP connectors to external tools.

This marketplace gives you **engineering-process** plugins — how Claude operates
inside your codebase, manages git, reviews code, and compounds effort.

They're complementary. Install both:

```bash
# Your engineering process
/plugin marketplace add jadecli/jadecli-plugins

# Anthropic's knowledge worker roles
/plugin marketplace add anthropics/knowledge-work-plugins
```

Your team settings (`.claude/settings.json` in any jadecli repo) can pre-configure both:

```json
{
  "extraKnownMarketplaces": {
    "jadecli-plugins": {
      "source": {
        "source": "github",
        "repo": "jadecli/jadecli-plugins"
      }
    },
    "knowledge-work-plugins": {
      "source": {
        "source": "github",
        "repo": "anthropics/knowledge-work-plugins"
      }
    }
  },
  "enabledPlugins": {
    "adaptive-agent@jadecli-plugins": true,
    "productivity@knowledge-work-plugins": true
  }
}
```

## Versioning

Plugins use semver in `plugin.json`. Bump the version when you change plugin code —
Claude Code caches plugins and won't pick up changes without a version bump.

The marketplace `marketplace.json` can also carry versions that override individual
plugin versions for coordinated releases.

## Creating New Plugins

Use this repo as your team's plugin home. To add a new plugin:

1. Create a new directory at the repo root (e.g., `jade-deploy/`)
2. Add `.claude-plugin/plugin.json` with at minimum `{"name": "jade-deploy"}`
3. Add skills/, commands/, agents/, hooks/ as needed
4. Register it in `.claude-plugin/marketplace.json`
5. Bump the version, push, and team members get it on next `/plugin` refresh

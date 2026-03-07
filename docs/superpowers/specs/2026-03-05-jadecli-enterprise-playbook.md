# JadeCLI Enterprise Playbook

Saved from brainstorming session 2026-03-05. Full playbook covering 15 enterprise
case studies, internal agent team architecture, marketplace asset taxonomy, and
12-month roadmap.

See the original document in conversation context. This file marks that the
playbook was reviewed and its patterns were distilled into the orchestrator
plugin design.

## Key patterns extracted for orchestrator plugin

1. **Parallel agent swarms** (Wiz) -- fan-out-fan-in mission type
2. **Skill folders as tradeable assets** (Lyft) -- mission files as shareable primitives
3. **Model routing** (HubSpot) -- opus lead, sonnet workers, haiku for simple tasks
4. **SDK-native orchestration** (Spotify) -- claude-agent-sdk-typescript as runtime
5. **Filesystem artifact system** (Anthropic multi-agent research) -- workers write files, return paths
6. **Scaling rules in prompts** (Anthropic) -- mission YAML embeds tier definitions
7. **Tiered governance** (Banner Health) -- evaluation criteria per mission
8. **Concept-to-commit velocity** (Freedom Forever) -- build-app mission type

## Verified Anthropic repos (all exist and are active)

- `@anthropic-ai/claude-agent-sdk` v0.2.69 (TypeScript)
- `anthropics/claude-agent-sdk-demos` (Research Agent, Email Agent, Excel, Hello World)
- `anthropics/knowledge-work-plugins` (11 plugins)
- `anthropics/skills` (public skill repository)
- `anthropics/claude-plugins-official` (curated plugin directory)
- `anthropics/financial-services-plugins` (5 plugins, 41 skills)
- `anthropics/life-sciences` (MCP servers + skills)
- `modelcontextprotocol/servers` (reference implementations)

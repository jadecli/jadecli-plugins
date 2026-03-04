# Claude Code Hooks Entry Point

Pre/post tool-use hooks that leverage installed tooling.

## Potential Hook Integrations

### PreToolUse: Bash

Guard against running commands that conflict with installed tools:

```json
{
  "event": "PreToolUse",
  "tool": "Bash",
  "hooks": [
    {
      "description": "Warn if running raw psql when TablePlus is available",
      "command": "echo 'Consider using TablePlus for interactive DB work'"
    }
  ]
}
```

### PostToolUse: Write

After writing docker-compose files, validate with Docker Desktop:

```json
{
  "event": "PostToolUse",
  "tool": "Write",
  "hooks": [
    {
      "description": "Validate docker-compose on write",
      "command": "if echo '$TOOL_INPUT' | grep -q 'docker-compose'; then docker compose config -q; fi"
    }
  ]
}
```

### SessionStart

Ensure dev environment is ready:
- Amphetamine session active
- Docker Desktop running
- Required containers up

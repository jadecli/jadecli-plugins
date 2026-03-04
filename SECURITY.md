# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 1.x.x   | Yes       |
| < 1.0   | No        |

## Reporting a vulnerability

**Do not open a public issue for security vulnerabilities.**

If you discover a security vulnerability in jadecli-plugins (skills, commands, agents, hooks, or CI workflows), please report it responsibly:

1. Email **<security@jadecli.dev>** with a description of the vulnerability
2. Include steps to reproduce the issue
3. Allow reasonable time for a fix before public disclosure

We will acknowledge receipt within 48 hours and provide a timeline for resolution.

## Scope

The following are in scope for this security policy:

- Plugin skills (`skills/*/SKILL.md`) that could cause unintended behavior
- Hook configurations (`hooks/hooks.json`) that execute shell commands
- Command definitions that could lead to destructive operations
- CI/CD workflows that handle secrets or permissions
- Marketplace manifest integrity

## Out of scope

- **Claude Code itself**: Report issues with Claude Code to [Anthropic](https://github.com/anthropics/claude-code/security)
- **GitHub Actions runners**: Report to [GitHub](https://github.com/security)
- Social engineering or phishing attempts

## Disclosure policy

We follow coordinated disclosure. After a fix is released, we will:

1. Credit the reporter (unless anonymity is requested)
2. Publish a security advisory on GitHub
3. Bump the patch version of affected plugins

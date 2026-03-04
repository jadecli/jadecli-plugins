# Claude Code Skills Entry Point

Skills that leverage the installed dev tooling.

## Potential Skills

### devtools:status

Check status of all managed tools:

- Amphetamine session active?
- Docker Desktop running? Containers up?
- 1Password CLI authenticated?
- File descriptor limit set?

### devtools:setup

Run first-time setup:

- Install all App Store apps via mas
- Apply macOS system tweaks
- Configure shell environment
- Set up SSH persistence

### devtools:doctor

Diagnose issues:

- Check if tools are installed and current version
- Verify system settings applied correctly
- Report Docker resource usage
- Check disk space for swap health

### devtools:update

Update all managed tools:

- `mas upgrade` for App Store apps
- `brew upgrade` for Homebrew tools
- Check for new recommended tools

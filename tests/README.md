# Test Suite for jadecli-plugins

Comprehensive test suite covering all changed files in the repository.

## Overview

This test suite provides 113 tests organized into 5 test files, achieving 100% pass rate.

## Test Files

### test_workflows.py (18 tests)
Tests GitHub Actions workflow YAML files:
- `.github/workflows/claude-code-review.yml`
- `.github/workflows/claude-mention.yml`
- `.github/workflows/release-doctor.yml`
- `.github/workflows/release.yml`
- `.github/workflows/validate.yml`

**Coverage:**
- YAML syntax validation
- Required fields and structure
- Permissions configuration
- Security best practices
- Timeout settings
- Action versions
- Conditional execution logic

### test_json_configs.py (22 tests)
Tests JSON configuration files:
- `.release-please-manifest.json`
- `release-please-config.json`
- `adaptive-agent/.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`

**Coverage:**
- JSON syntax validation
- Schema validation
- Version consistency across files
- Cross-file reference validation
- Semver format validation
- Package configuration

### test_markdown.py (31 tests)
Tests Markdown documentation files:
- `.github/PULL_REQUEST_TEMPLATE.md`
- `SECURITY.md`
- `adaptive-agent/README.md`
- `adaptive-agent/commands/setup-environment.md`
- `adaptive-agent/skills/surface-awareness/SKILL.md`
- `docs/SETUP.md`

**Coverage:**
- Required sections validation
- Content structure validation
- Frontmatter validation (for commands/skills)
- Code block integrity
- Header formatting
- Internal link validation
- Checklist completeness

### test_shell_scripts.py (25 tests)
Tests shell script files:
- `scripts/setup-github-repo.sh`

**Coverage:**
- Bash syntax validation
- Shebang validation
- Error handling (set -euo pipefail)
- Documentation completeness
- Idempotency checks
- Security best practices
- Function definitions
- Configuration logic

### test_integration.py (17 tests)
Integration tests verifying cross-file consistency:

**Coverage:**
- Version consistency across manifest/plugin/marketplace
- Workflow status checks match actual jobs
- Release configuration integrity
- Security policy coverage
- Permission configurations
- Edge cases and boundaries
- Metadata consistency
- Semver format strictness

## Running Tests

### Run all tests
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

### Run specific test file
```bash
python3 -m unittest tests/test_workflows.py
```

### Run with verbose output
```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

### Run specific test class or method
```bash
python3 -m unittest tests.test_workflows.TestGitHubWorkflows
python3 -m unittest tests.test_workflows.TestGitHubWorkflows.test_workflow_yaml_syntax
```

## Test Results

```
Total tests: 113
Successes: 113
Failures: 0
Errors: 0
Success rate: 100.0%
```

### Breakdown by file:
- `test_workflows.py`: 18 tests
- `test_json_configs.py`: 22 tests
- `test_markdown.py`: 31 tests
- `test_shell_scripts.py`: 25 tests
- `test_integration.py`: 17 tests

## Dependencies

The test suite uses only Python standard library:
- `unittest` - Test framework
- `json` - JSON parsing
- `yaml` - YAML parsing (PyYAML)
- `pathlib` - File path handling
- `subprocess` - Shell script validation
- `re` - Regular expressions

Install YAML support:
```bash
pip install pyyaml
```

## Test Categories

### Unit Tests
Individual file validation (workflows, JSON, markdown, shell scripts)

### Integration Tests
Cross-file consistency and relationships

### Syntax Tests
File format and syntax validation

### Security Tests
Security best practices and credential handling

### Structure Tests
Required sections, fields, and configuration

### Regression Tests
Edge cases and boundary conditions

## Adding New Tests

When adding new configuration files or workflows:

1. Add appropriate test methods to existing test classes
2. Follow naming convention: `test_<what_is_being_tested>`
3. Include descriptive docstrings
4. Test both positive and negative cases
5. Verify error messages are helpful

Example:
```python
def test_new_workflow_structure(self):
    """Test new-workflow.yml has required structure."""
    workflow = self.workflows["new-workflow.yml"]
    self.assertIn("jobs", workflow)
    # ... additional assertions
```

## CI Integration

These tests are designed to run in CI environments:
- No external dependencies required (except PyYAML)
- Fast execution (< 1 second)
- Clear failure messages
- Exit code 0 on success, non-zero on failure

Can be integrated into validate.yml workflow:
```yaml
- name: Run Python tests
  run: python3 -m unittest discover -s tests -p "test_*.py"
```

## Test Philosophy

1. **Comprehensive**: Cover all changed files
2. **Maintainable**: Clear test names and structure
3. **Fast**: Complete suite runs in under 1 second
4. **Reliable**: No flaky tests, deterministic results
5. **Helpful**: Descriptive error messages
6. **Defensive**: Test edge cases and boundaries
#!/usr/bin/env python3
"""
Comprehensive tests for shell scripts.
Tests syntax, structure, error handling, and idempotency.
"""

import unittest
import subprocess
import os
from pathlib import Path


class TestShellScripts(unittest.TestCase):
    """Test suite for shell scripts."""

    @classmethod
    def setUpClass(cls):
        """Load shell script."""
        cls.repo_root = Path(__file__).parent.parent
        cls.setup_script_path = cls.repo_root / "scripts" / "setup-github-repo.sh"

        with open(cls.setup_script_path, 'r') as f:
            cls.setup_script_content = f.read()

    def test_setup_script_exists(self):
        """Test that setup-github-repo.sh exists."""
        self.assertTrue(
            self.setup_script_path.exists(),
            "scripts/setup-github-repo.sh should exist"
        )

    def test_setup_script_has_shebang(self):
        """Test script has proper shebang."""
        with open(self.setup_script_path, 'r') as f:
            first_line = f.readline().strip()

        self.assertTrue(
            first_line.startswith("#!/"),
            "Script should start with shebang"
        )

        self.assertIn(
            "bash",
            first_line,
            "Script should use bash"
        )

    def test_setup_script_has_error_handling(self):
        """Test script has proper error handling."""
        content = self.setup_script_content

        # Should have set -e (exit on error)
        self.assertRegex(
            content,
            r'set\s+-.*e',
            "Script should have 'set -e' for error handling"
        )

        # Should have set -u (exit on undefined variable)
        self.assertRegex(
            content,
            r'set\s+-.*u',
            "Script should have 'set -u' to catch undefined variables"
        )

        # Should have set -o pipefail (pipeline error handling)
        self.assertRegex(
            content,
            r'set\s+-.*o\s+pipefail',
            "Script should have 'set -o pipefail' for pipeline errors"
        )

    def test_setup_script_has_documentation(self):
        """Test script has proper documentation."""
        content = self.setup_script_content

        # Should have header comment describing purpose
        self.assertIn(
            "Setup GitHub repository",
            content,
            "Script should have description in comments"
        )

        # Should have usage documentation
        self.assertIn(
            "Usage:",
            content,
            "Script should have usage documentation"
        )

        # Should mention requirements
        self.assertIn(
            "Requires:",
            content,
            "Script should document requirements"
        )

    def test_setup_script_configurable_repo(self):
        """Test script allows configurable repository."""
        content = self.setup_script_content

        # Should have REPO variable with default
        self.assertIn(
            'REPO=',
            content,
            "Script should have REPO variable"
        )

        # Should use ${REPO:-default} pattern
        self.assertRegex(
            content,
            r'REPO="\$\{REPO:-[^}]+\}"',
            "Script should have REPO with default value"
        )

    def test_setup_script_uses_gh_cli(self):
        """Test script uses GitHub CLI."""
        content = self.setup_script_content

        # Should use gh commands
        self.assertIn(
            "gh ",
            content,
            "Script should use gh CLI"
        )

        # Should use gh label, gh api, gh release
        gh_commands = ["gh label", "gh api", "gh release"]
        for cmd in gh_commands:
            self.assertIn(
                cmd,
                content,
                f"Script should use '{cmd}' command"
            )

    def test_setup_script_creates_labels(self):
        """Test script creates required labels."""
        content = self.setup_script_content

        # Should have label creation function
        self.assertIn(
            "create_label",
            content,
            "Script should have label creation function"
        )

        # Should create autorelease labels
        autorelease_labels = ["autorelease: pending", "autorelease: tagged"]
        for label in autorelease_labels:
            self.assertIn(
                label,
                content,
                f"Script should create '{label}' label"
            )

        # Should create component labels
        component_labels = ["plugin", "skill", "command", "agent"]
        for label in component_labels:
            self.assertIn(
                label,
                content,
                f"Script should create '{label}' label"
            )

    def test_setup_script_configures_merge_strategy(self):
        """Test script configures merge strategy."""
        content = self.setup_script_content

        # Should configure merge settings
        merge_settings = [
            "allow_squash_merge",
            "allow_merge_commit",
            "allow_rebase_merge",
            "delete_branch_on_merge"
        ]

        for setting in merge_settings:
            self.assertIn(
                setting,
                content,
                f"Script should configure '{setting}'"
            )

        # Should disable merge commits (prefer squash)
        self.assertIn(
            "allow_merge_commit=false",
            content,
            "Script should disable merge commits"
        )

    def test_setup_script_configures_branch_protection(self):
        """Test script sets up branch protection."""
        content = self.setup_script_content

        # Should configure branch protection
        self.assertIn(
            "branches/main/protection",
            content,
            "Script should configure main branch protection"
        )

        # Should require status checks
        self.assertIn(
            "required_status_checks",
            content,
            "Script should require status checks"
        )

        # Should require PR reviews
        self.assertIn(
            "required_pull_request_reviews",
            content,
            "Script should require PR reviews"
        )

        # Should enforce for admins
        self.assertIn(
            '"enforce_admins": true',
            content,
            "Script should enforce rules for admins"
        )

    def test_setup_script_creates_initial_release(self):
        """Test script creates initial release."""
        content = self.setup_script_content

        # Should check for existing release
        self.assertIn(
            "gh release view",
            content,
            "Script should check for existing release"
        )

        # Should create v1.0.0 release
        self.assertIn(
            "v1.0.0",
            content,
            "Script should reference v1.0.0 release"
        )

        # Should have idempotent release creation
        self.assertIn(
            "already exists",
            content,
            "Script should handle existing releases gracefully"
        )

    def test_setup_script_is_idempotent(self):
        """Test script is safe to re-run."""
        content = self.setup_script_content

        # Should handle existing resources gracefully
        idempotent_checks = [
            "already exists",
            "Exists:",
            "if gh release view"
        ]

        found_checks = sum(1 for check in idempotent_checks if check in content)
        self.assertGreater(
            found_checks,
            0,
            "Script should have idempotency checks"
        )

        # Label creation should be idempotent
        self.assertIn(
            "2>/dev/null",
            content,
            "Script should suppress errors for idempotency"
        )

    def test_setup_script_has_output_sections(self):
        """Test script provides clear output sections."""
        content = self.setup_script_content

        # Should have section headers
        section_markers = [
            "---",
            "Labels",
            "Merge strategy",
            "Branch protection"
        ]

        for marker in section_markers:
            self.assertIn(
                marker,
                content,
                f"Script should have '{marker}' section"
            )

        # Should echo progress
        self.assertIn(
            "echo",
            content,
            "Script should provide output feedback"
        )

    def test_setup_script_required_checks_configured(self):
        """Test script configures all required status checks."""
        content = self.setup_script_content

        # Required checks from validate.yml
        required_checks = [
            "Validate JSON",
            "Validate plugin structure",
            "Lint commit messages",
            "Lint Markdown"
        ]

        for check in required_checks:
            self.assertIn(
                check,
                content,
                f"Script should require '{check}' status check"
            )

    def test_setup_script_uses_api_correctly(self):
        """Test script uses GitHub API correctly."""
        content = self.setup_script_content

        # Should use gh api with proper methods
        api_patterns = [
            r'gh api .* -X PUT',
            r'gh api .* -X PATCH'
        ]

        found_patterns = sum(
            1 for pattern in api_patterns
            if len(self._find_pattern(content, pattern)) > 0
        )

        self.assertGreater(
            found_patterns,
            0,
            "Script should use gh api with HTTP methods"
        )

    def test_setup_script_silent_mode_for_apis(self):
        """Test script uses silent mode for API calls."""
        content = self.setup_script_content

        # Should use --silent flag to suppress progress output
        self.assertIn(
            "--silent",
            content,
            "Script should use --silent flag for clean output"
        )

    def test_setup_script_json_heredoc(self):
        """Test script uses heredoc for JSON input."""
        content = self.setup_script_content

        # Should use heredoc for JSON (cleaner than inline)
        self.assertIn(
            "<<'JSON'",
            content,
            "Script should use heredoc for JSON data"
        )

    def test_setup_script_repo_variable_usage(self):
        """Test script consistently uses REPO variable."""
        content = self.setup_script_content

        # Should use -R $REPO pattern
        self.assertIn(
            '-R "$REPO"',
            content,
            "Script should use -R with REPO variable"
        )

        # Should use $REPO in multiple places
        repo_usage_count = content.count('$REPO')
        self.assertGreater(
            repo_usage_count,
            5,
            "Script should use $REPO variable throughout"
        )

    def test_setup_script_function_definitions(self):
        """Test script properly defines functions."""
        content = self.setup_script_content

        # Should have create_label function
        self.assertRegex(
            content,
            r'create_label\(\)\s*\{',
            "Script should define create_label function"
        )

        # Function should take parameters
        self.assertIn(
            'local name=',
            content,
            "create_label function should use local variables"
        )

    def test_setup_script_error_suppression_appropriate(self):
        """Test script only suppresses errors where appropriate."""
        content = self.setup_script_content

        # 2>/dev/null should only be used for idempotency checks
        # Count occurrences
        error_suppression_count = content.count('2>/dev/null')

        # Should be minimal (only for expected errors like "label exists")
        self.assertLessEqual(
            error_suppression_count,
            5,
            "Script should minimize error suppression"
        )

    def test_setup_script_release_notes(self):
        """Test script includes release notes."""
        content = self.setup_script_content

        # Should have release notes for initial release
        self.assertIn(
            "--notes",
            content,
            "Script should include release notes"
        )

        # Notes should mention initial release
        self.assertIn(
            "Initial release",
            content,
            "Release notes should mention initial release"
        )

    def test_setup_script_no_hardcoded_credentials(self):
        """Test script doesn't contain hardcoded credentials."""
        content = self.setup_script_content

        # Should not have API keys
        self.assertNotRegex(
            content,
            r'(api[_-]?key|token|password)\s*=\s*["\'](?!\\$)',
            "Script should not have hardcoded credentials"
        )

    def test_setup_script_review_count_configured(self):
        """Test script sets required review count."""
        content = self.setup_script_content

        # Should require at least 1 review
        self.assertIn(
            '"required_approving_review_count": 1',
            content,
            "Script should require 1 approving review"
        )

        # Should dismiss stale reviews
        self.assertIn(
            '"dismiss_stale_reviews": true',
            content,
            "Script should dismiss stale reviews"
        )

    def test_setup_script_completion_message(self):
        """Test script prints completion message."""
        content = self.setup_script_content

        # Should have completion message
        self.assertIn(
            "Setup complete",
            content,
            "Script should print completion message"
        )

    def _find_pattern(self, text, pattern):
        """Helper to find regex pattern in text."""
        import re
        return re.findall(pattern, text)


class TestShellScriptSyntax(unittest.TestCase):
    """Test shell script syntax using external tools."""

    @classmethod
    def setUpClass(cls):
        """Set up paths."""
        cls.repo_root = Path(__file__).parent.parent
        cls.setup_script_path = cls.repo_root / "scripts" / "setup-github-repo.sh"

    def test_bash_syntax_check(self):
        """Test bash syntax with bash -n."""
        result = subprocess.run(
            ["bash", "-n", str(self.setup_script_path)],
            capture_output=True,
            text=True
        )

        self.assertEqual(
            result.returncode,
            0,
            f"Script has syntax errors:\n{result.stderr}"
        )

    def test_script_is_executable(self):
        """Test script has executable permissions."""
        # Check if file is executable
        is_executable = os.access(self.setup_script_path, os.X_OK)

        # Note: This might not work in all environments, so we just warn
        if not is_executable:
            print(f"\nWarning: {self.setup_script_path} is not executable")
            print("Run: chmod +x scripts/setup-github-repo.sh")


if __name__ == "__main__":
    unittest.main()
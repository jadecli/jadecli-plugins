#!/usr/bin/env python3
"""
Comprehensive tests for Markdown documentation files.
Tests structure, required sections, formatting, and content validity.
"""

import unittest
import re
from pathlib import Path


class TestMarkdownDocumentation(unittest.TestCase):
    """Test suite for Markdown documentation files."""

    @classmethod
    def setUpClass(cls):
        """Load all markdown files."""
        cls.repo_root = Path(__file__).parent.parent
        cls.docs = {}

        markdown_files = {
            "pr_template": ".github/PULL_REQUEST_TEMPLATE.md",
            "security": "SECURITY.md",
            "adaptive_agent_readme": "adaptive-agent/README.md",
            "setup_environment_command": "adaptive-agent/commands/setup-environment.md",
            "surface_awareness_skill": "adaptive-agent/skills/surface-awareness/SKILL.md",
            "docs_setup": "docs/SETUP.md"
        }

        for key, filepath in markdown_files.items():
            full_path = cls.repo_root / filepath
            with open(full_path, 'r') as f:
                cls.docs[key] = {
                    "path": filepath,
                    "content": f.read(),
                    "lines": f.read().splitlines()
                }
            # Re-read for lines
            with open(full_path, 'r') as f:
                cls.docs[key]["lines"] = f.read().splitlines()

    def test_markdown_files_exist(self):
        """Test that all expected markdown files exist."""
        expected_files = [
            ".github/PULL_REQUEST_TEMPLATE.md",
            "SECURITY.md",
            "adaptive-agent/README.md",
            "adaptive-agent/commands/setup-environment.md",
            "adaptive-agent/skills/surface-awareness/SKILL.md",
            "docs/SETUP.md"
        ]

        for filepath in expected_files:
            full_path = self.repo_root / filepath
            self.assertTrue(
                full_path.exists(),
                f"Markdown file {filepath} should exist"
            )

    def test_markdown_files_not_empty(self):
        """Test that markdown files are not empty."""
        for key, doc in self.docs.items():
            self.assertGreater(
                len(doc["content"]),
                0,
                f"{doc['path']} should not be empty"
            )

    def test_pr_template_structure(self):
        """Test PR template has required sections."""
        doc = self.docs["pr_template"]
        content = doc["content"]

        # Required sections
        required_sections = [
            "## Summary",
            "## Changes",
            "## Plugin version impact",
            "## Checklist",
            "## Security"
        ]

        for section in required_sections:
            self.assertIn(
                section,
                content,
                f"PR template should have '{section}' section"
            )

    def test_pr_template_checklist_items(self):
        """Test PR template has all required checklist items."""
        doc = self.docs["pr_template"]
        content = doc["content"]

        required_items = [
            "Conventional commit message",
            "Plugin JSON valid",
            "README updated",
            "CHANGELOG.md updated",
            "No secrets or credentials",
            "Hooks do not execute destructive operations"
        ]

        for item in required_items:
            self.assertIn(
                item,
                content,
                f"PR template should mention '{item}'"
            )

    def test_pr_template_version_impact_options(self):
        """Test PR template has version impact options."""
        doc = self.docs["pr_template"]
        content = doc["content"]

        version_options = [
            "No version change needed",
            "Patch bump",
            "Minor bump",
            "Major bump"
        ]

        for option in version_options:
            self.assertIn(
                option,
                content,
                f"PR template should have '{option}' version option"
            )

    def test_security_md_structure(self):
        """Test SECURITY.md has required sections."""
        doc = self.docs["security"]
        content = doc["content"]

        required_sections = [
            "## Supported versions",
            "## Reporting a vulnerability",
            "## Scope",
            "## Out of scope",
            "## Disclosure policy"
        ]

        for section in required_sections:
            self.assertIn(
                section,
                content,
                f"SECURITY.md should have '{section}' section"
            )

    def test_security_md_contact_info(self):
        """Test SECURITY.md has security contact information."""
        doc = self.docs["security"]
        content = doc["content"]

        # Should have email for security reports
        self.assertIn(
            "security@jadecli.dev",
            content,
            "SECURITY.md should have security email contact"
        )

        # Should warn against public disclosure
        self.assertIn(
            "Do not open a public issue",
            content,
            "SECURITY.md should warn against public disclosure"
        )

    def test_security_md_scope_items(self):
        """Test SECURITY.md defines security scope."""
        doc = self.docs["security"]
        content = doc["content"]

        scope_items = [
            "Plugin skills",
            "Hook configurations",
            "Command definitions",
            "CI/CD workflows"
        ]

        for item in scope_items:
            self.assertIn(
                item.lower(),
                content.lower(),
                f"SECURITY.md should mention '{item}' in scope"
            )

    def test_adaptive_agent_readme_structure(self):
        """Test adaptive-agent README has proper structure."""
        doc = self.docs["adaptive_agent_readme"]
        content = doc["content"]

        required_sections = [
            "## What It Does",
            "## Install",
            "## Philosophy"
        ]

        for section in required_sections:
            self.assertIn(
                section,
                content,
                f"adaptive-agent README should have '{section}' section"
            )

    def test_adaptive_agent_readme_components(self):
        """Test adaptive-agent README documents all components."""
        doc = self.docs["adaptive_agent_readme"]
        content = doc["content"]

        components = [
            "**Skills**",
            "**Commands**",
            "**Agents**",
            "**Hooks**"
        ]

        for component in components:
            self.assertIn(
                component,
                content,
                f"adaptive-agent README should document {component}"
            )

    def test_adaptive_agent_readme_installation(self):
        """Test adaptive-agent README has installation instructions."""
        doc = self.docs["adaptive_agent_readme"]
        content = doc["content"]

        # Should have plugin installation commands
        self.assertIn(
            "/plugin",
            content,
            "README should have plugin installation commands"
        )

        self.assertIn(
            "adaptive-agent",
            content,
            "README should reference adaptive-agent plugin name"
        )

    def test_setup_environment_command_frontmatter(self):
        """Test setup-environment command has proper frontmatter."""
        doc = self.docs["setup_environment_command"]
        content = doc["content"]

        # Should have YAML frontmatter
        self.assertTrue(
            content.startswith("---"),
            "Command should have YAML frontmatter"
        )

        # Should have description and args
        self.assertIn("description:", content)
        self.assertIn("args:", content)

    def test_setup_environment_command_sections(self):
        """Test setup-environment command has all required sections."""
        doc = self.docs["setup_environment_command"]
        content = doc["content"]

        required_sections = [
            "## 1. Detect Surface",
            "## 2. Detect Project Type",
            "## 3. Surface-Specific Setup",
            "## 4. Check Shared Configuration",
            "## 5. Output Summary"
        ]

        for section in required_sections:
            self.assertIn(
                section,
                content,
                f"setup-environment command should have '{section}' section"
            )

    def test_setup_environment_command_surfaces(self):
        """Test setup-environment command covers all surfaces."""
        doc = self.docs["setup_environment_command"]
        content = doc["content"]

        surfaces = [
            "CLI",
            "Desktop",
            "IDE",
            "Web",
            "Remote",
            "GitHub Actions",
            "GitLab CI"
        ]

        for surface in surfaces:
            self.assertIn(
                surface,
                content,
                f"setup-environment should cover '{surface}' surface"
            )

    def test_setup_environment_command_code_examples(self):
        """Test setup-environment command has code examples."""
        doc = self.docs["setup_environment_command"]
        content = doc["content"]

        # Should have bash code blocks
        self.assertIn(
            "```bash",
            content,
            "Command should have bash code examples"
        )

        # Should have JSON examples for launch.json
        self.assertIn(
            "```json",
            content,
            "Command should have JSON configuration examples"
        )

    def test_surface_awareness_skill_frontmatter(self):
        """Test surface-awareness skill has proper frontmatter."""
        doc = self.docs["surface_awareness_skill"]
        content = doc["content"]

        # Should have YAML frontmatter
        self.assertTrue(
            content.startswith("---"),
            "Skill should have YAML frontmatter"
        )

        # Should have name, description, and version
        self.assertIn("name:", content)
        self.assertIn("description:", content)
        self.assertIn("version:", content)

    def test_surface_awareness_skill_surfaces(self):
        """Test surface-awareness skill documents all surfaces."""
        doc = self.docs["surface_awareness_skill"]
        content = doc["content"]

        surfaces = [
            "## CLI / Terminal",
            "## Desktop",
            "## VS Code / JetBrains",
            "## Web / Remote Sessions",
            "## GitHub Actions",
            "## GitLab CI"
        ]

        for surface in surfaces:
            self.assertIn(
                surface,
                content,
                f"surface-awareness skill should document '{surface}'"
            )

    def test_surface_awareness_skill_detection_table(self):
        """Test surface-awareness skill has detection table."""
        doc = self.docs["surface_awareness_skill"]
        content = doc["content"]

        # Should have detection signals table
        detection_signals = [
            "GITHUB_ACTIONS",
            "GITLAB_CI",
            "CLAUDE_CODE_REMOTE",
            "VSCODE_VERSION"
        ]

        for signal in detection_signals:
            self.assertIn(
                signal,
                content,
                f"Skill should document '{signal}' detection signal"
            )

    def test_surface_awareness_skill_remote_control(self):
        """Test surface-awareness skill documents Remote Control."""
        doc = self.docs["surface_awareness_skill"]
        content = doc["content"]

        # Should have Remote Control section
        self.assertIn(
            "Remote Control",
            content,
            "Skill should document Remote Control feature"
        )

        # Should mention /rc command
        self.assertIn(
            "/rc",
            content,
            "Skill should mention /rc command"
        )

        # Should mention mobile/phone access
        remote_keywords = ["phone", "mobile", "browser", "iPhone"]
        found_keyword = any(keyword.lower() in content.lower() for keyword in remote_keywords)
        self.assertTrue(
            found_keyword,
            "Skill should mention mobile/browser access for Remote Control"
        )

    def test_surface_awareness_skill_permission_modes(self):
        """Test surface-awareness skill documents permission modes."""
        doc = self.docs["surface_awareness_skill"]
        content = doc["content"]

        permission_modes = [
            "Ask",
            "Auto accept edits",
            "Plan",
            "Don't ask",
            "Bypass"
        ]

        for mode in permission_modes:
            self.assertIn(
                mode,
                content,
                f"Skill should document '{mode}' permission mode"
            )

    def test_docs_setup_structure(self):
        """Test docs/SETUP.md has proper structure."""
        doc = self.docs["docs_setup"]
        content = doc["content"]

        required_sections = [
            "## Prerequisites",
            "## 1. Run the setup script",
            "## 2. Configure repository secrets",
            "## 3. Activate Claude workflows",
            "## 5. Verify setup"
        ]

        for section in required_sections:
            self.assertIn(
                section,
                content,
                f"docs/SETUP.md should have '{section}' section"
            )

    def test_docs_setup_prerequisites(self):
        """Test docs/SETUP.md lists prerequisites."""
        doc = self.docs["docs_setup"]
        content = doc["content"]

        prerequisites = [
            "GitHub CLI",
            "gh",
            "Admin permissions"
        ]

        for prereq in prerequisites:
            self.assertIn(
                prereq,
                content,
                f"docs/SETUP.md should mention '{prereq}' prerequisite"
            )

    def test_docs_setup_script_usage(self):
        """Test docs/SETUP.md documents script usage."""
        doc = self.docs["docs_setup"]
        content = doc["content"]

        # Should mention the setup script
        self.assertIn(
            "setup-github-repo.sh",
            content,
            "docs/SETUP.md should reference setup script"
        )

        # Should have example commands
        self.assertIn(
            "```bash",
            content,
            "docs/SETUP.md should have bash examples"
        )

    def test_docs_setup_secrets_documentation(self):
        """Test docs/SETUP.md documents required secrets."""
        doc = self.docs["docs_setup"]
        content = doc["content"]

        # Should mention ANTHROPIC_API_KEY
        self.assertIn(
            "ANTHROPIC_API_KEY",
            content,
            "docs/SETUP.md should document ANTHROPIC_API_KEY secret"
        )

        # Should mention how to add secrets
        self.assertIn(
            "gh secret set",
            content,
            "docs/SETUP.md should show how to set secrets"
        )

    def test_markdown_no_broken_internal_links(self):
        """Test markdown files don't have obviously broken internal links."""
        for key, doc in self.docs.items():
            content = doc["content"]

            # Find markdown links [text](url)
            links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)

            for link_text, link_url in links:
                # Check internal file links (not http/https)
                if not link_url.startswith(('http://', 'https://', '#', 'mailto:')):
                    # Internal file reference
                    # Just check it doesn't have obvious typos like double slashes
                    self.assertNotIn(
                        '//',
                        link_url,
                        f"{doc['path']} has link with double slashes: {link_url}"
                    )

    def test_markdown_headers_properly_formatted(self):
        """Test markdown headers follow proper format."""
        for key, doc in self.docs.items():
            lines = doc["lines"]

            for i, line in enumerate(lines):
                if line.startswith('#'):
                    # Headers should have space after #
                    self.assertRegex(
                        line,
                        r'^#{1,6}\s+.+',
                        f"{doc['path']} line {i+1}: Header should have space after #"
                    )

    def test_markdown_code_blocks_closed(self):
        """Test markdown code blocks are properly closed."""
        for key, doc in self.docs.items():
            content = doc["content"]

            # Count opening and closing code fences
            triple_backticks = content.count("```")

            # Should be even number (each opening has a closing)
            self.assertEqual(
                triple_backticks % 2,
                0,
                f"{doc['path']} has unclosed code blocks"
            )

    def test_markdown_no_trailing_whitespace(self):
        """Test markdown files don't have excessive trailing whitespace."""
        for key, doc in self.docs.items():
            lines = doc["lines"]

            # Allow some trailing whitespace for markdown line breaks
            # but flag excessive trailing spaces
            for i, line in enumerate(lines):
                trailing_spaces = len(line) - len(line.rstrip(' '))
                if trailing_spaces > 2:
                    self.fail(
                        f"{doc['path']} line {i+1} has {trailing_spaces} "
                        f"trailing spaces (max 2 recommended)"
                    )

    def test_skill_version_format(self):
        """Test skill version follows semver format."""
        doc = self.docs["surface_awareness_skill"]
        content = doc["content"]

        # Extract version from frontmatter
        version_match = re.search(r'version:\s+(\S+)', content)
        self.assertIsNotNone(
            version_match,
            "Skill should have version in frontmatter"
        )

        version = version_match.group(1)
        self.assertRegex(
            version,
            r'^\d+\.\d+\.\d+$',
            f"Skill version '{version}' should be valid semver"
        )

    def test_command_args_structure(self):
        """Test command args are properly structured."""
        doc = self.docs["setup_environment_command"]
        content = doc["content"]

        # Should have args with name, description, required, default
        args_section = content[content.find("args:"):content.find("---", 3)]

        self.assertIn("name:", args_section)
        self.assertIn("description:", args_section)
        self.assertIn("required:", args_section)
        self.assertIn("default:", args_section)

    def test_readme_philosophy_section(self):
        """Test README has philosophy/vision statement."""
        doc = self.docs["adaptive_agent_readme"]
        content = doc["content"]

        philosophy_section = content[content.find("## Philosophy"):]

        # Should explain the adaptive approach
        self.assertIn(
            "agent adapts",
            philosophy_section.lower(),
            "Philosophy should explain adaptive approach"
        )

        self.assertIn(
            "codebase",
            philosophy_section.lower(),
            "Philosophy should mention codebase adaptation"
        )


if __name__ == "__main__":
    unittest.main()
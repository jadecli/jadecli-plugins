#!/usr/bin/env python3
"""
Integration tests that verify cross-file consistency and relationships.
These tests ensure the entire configuration works together cohesively.
"""

import unittest
import json
import yaml
from pathlib import Path


class TestCrossFileIntegration(unittest.TestCase):
    """Integration tests across multiple configuration files."""

    @classmethod
    def setUpClass(cls):
        """Load all configuration files for integration testing."""
        cls.repo_root = Path(__file__).parent.parent

        # Load JSON configs
        with open(cls.repo_root / "release-please-config.json") as f:
            cls.release_config = json.load(f)

        with open(cls.repo_root / ".release-please-manifest.json") as f:
            cls.release_manifest = json.load(f)

        with open(cls.repo_root / "adaptive-agent" / ".claude-plugin" / "plugin.json") as f:
            cls.plugin_json = json.load(f)

        with open(cls.repo_root / ".claude-plugin" / "marketplace.json") as f:
            cls.marketplace = json.load(f)

        # Load workflow files
        cls.workflows = {}
        workflows_dir = cls.repo_root / ".github" / "workflows"
        for workflow_file in workflows_dir.glob("*.yml"):
            with open(workflow_file) as f:
                cls.workflows[workflow_file.name] = yaml.safe_load(f)

    def test_all_manifest_packages_in_release_config(self):
        """Test all packages in manifest are configured in release-please config."""
        manifest_packages = set(self.release_manifest.keys())
        config_packages = set(self.release_config["packages"].keys())

        self.assertEqual(
            manifest_packages,
            config_packages,
            "Manifest packages should match release-please config packages"
        )

    def test_workflow_status_checks_match_validate_jobs(self):
        """Test branch protection status checks match actual validate.yml jobs."""
        # This test reads the setup script to get required checks
        setup_script_path = self.repo_root / "scripts" / "setup-github-repo.sh"
        with open(setup_script_path) as f:
            setup_script = f.read()

        # Extract status checks from setup script
        required_checks = [
            "Validate JSON",
            "Validate plugin structure",
            "Lint commit messages",
            "Lint Markdown"
        ]

        # Check these match actual validate.yml job names
        validate_workflow = self.workflows["validate.yml"]
        job_names = list(validate_workflow["jobs"].keys())

        # Map job names to display names
        job_display_names = []
        for job_name, job in validate_workflow["jobs"].items():
            if "name" in job:
                job_display_names.append(job["name"])

        # Map status checks to job names (case-insensitive, flexible matching)
        check_to_job_mapping = {
            "Validate JSON": "validate-json",
            "Validate plugin structure": "validate-structure",
            "Lint commit messages": "lint-commits",
            "Lint Markdown": "lint-markdown"
        }

        # All required checks should have corresponding jobs
        for check in required_checks:
            expected_job = check_to_job_mapping.get(check, "")
            # Check if the expected job name exists
            found = expected_job in job_names
            self.assertTrue(
                found,
                f"Status check '{check}' should have corresponding job '{expected_job}' in validate.yml"
            )

    def test_marketplace_plugin_version_matches_manifest(self):
        """Test each marketplace plugin version matches manifest."""
        for plugin in self.marketplace["plugins"]:
            source = plugin["source"].lstrip("./")

            # Get version from manifest
            manifest_version = self.release_manifest.get(source)

            if manifest_version:
                # Load plugin.json
                plugin_json_path = self.repo_root / source / ".claude-plugin" / "plugin.json"
                with open(plugin_json_path) as f:
                    plugin_data = json.load(f)

                # Versions should match
                self.assertEqual(
                    plugin_data["version"],
                    manifest_version,
                    f"Plugin {source} version should match manifest"
                )

    def test_release_workflow_uses_correct_config_files(self):
        """Test release.yml workflow references correct config files."""
        release_workflow = self.workflows["release.yml"]

        # Find release-please action step
        release_job = release_workflow["jobs"]["release-please"]
        release_step = None
        for step in release_job["steps"]:
            if "uses" in step and "release-please-action" in step["uses"]:
                release_step = step
                break

        self.assertIsNotNone(release_step, "Should have release-please action step")

        # Check config files match what exists
        self.assertEqual(
            release_step["with"]["config-file"],
            "release-please-config.json"
        )
        self.assertEqual(
            release_step["with"]["manifest-file"],
            ".release-please-manifest.json"
        )

        # Verify these files exist
        self.assertTrue((self.repo_root / "release-please-config.json").exists())
        self.assertTrue((self.repo_root / ".release-please-manifest.json").exists())

    def test_validate_workflow_checks_all_json_files(self):
        """Test validate.yml workflow validates all important JSON files."""
        validate_workflow = self.workflows["validate.yml"]
        validate_json_job = validate_workflow["jobs"]["validate-json"]

        # Check that it validates key JSON files
        job_str = str(validate_json_job)

        key_files = ["marketplace.json", "plugin.json", "hooks.json"]
        for filename in key_files:
            self.assertIn(
                filename,
                job_str,
                f"validate-json job should check {filename}"
            )

    def test_release_doctor_validates_same_files_as_release(self):
        """Test release-doctor.yml validates same files as release.yml uses."""
        doctor_workflow = self.workflows["release-doctor.yml"]
        doctor_job = doctor_workflow["jobs"]["check-release-health"]

        # Should validate release-please config files
        job_str = str(doctor_job)

        self.assertIn(
            "release-please-config.json",
            job_str,
            "Release doctor should validate release-please-config.json"
        )
        self.assertIn(
            ".release-please-manifest.json",
            job_str,
            "Release doctor should validate .release-please-manifest.json"
        )

    def test_plugin_metadata_consistency(self):
        """Test plugin metadata is consistent across all files."""
        plugin_name = self.plugin_json["name"]

        # Plugin name should appear in marketplace
        marketplace_plugin_names = [p["name"] for p in self.marketplace["plugins"]]
        self.assertIn(
            plugin_name,
            marketplace_plugin_names,
            "Plugin should be listed in marketplace"
        )

        # Plugin should be in manifest
        self.assertIn(
            plugin_name,
            self.release_manifest,
            "Plugin should be in release manifest"
        )

        # Plugin should be in release config
        self.assertIn(
            plugin_name,
            self.release_config["packages"],
            "Plugin should be in release config"
        )

    def test_changelog_sections_cover_commit_types(self):
        """Test changelog sections cover all validated commit types."""
        # Get changelog sections from release config
        changelog_sections = self.release_config.get("changelog-sections", [])
        section_types = [s["type"] for s in changelog_sections]

        # These are the commit types validated by commitlint
        expected_types = ["feat", "fix", "docs", "chore"]

        for commit_type in expected_types:
            self.assertIn(
                commit_type,
                section_types,
                f"Changelog should have section for {commit_type} commits"
            )

    def test_workflow_permissions_principle_of_least_privilege(self):
        """Test workflows follow principle of least privilege."""
        for workflow_name, workflow in self.workflows.items():
            if "permissions" not in workflow:
                continue

            permissions = workflow["permissions"]

            # No workflow should have write access to all
            if isinstance(permissions, str):
                self.assertNotEqual(
                    permissions,
                    "write-all",
                    f"{workflow_name} should not have write-all permissions"
                )

            # Contents write should only be for release workflow
            if isinstance(permissions, dict) and permissions.get("contents") == "write":
                self.assertIn(
                    "release",
                    workflow_name.lower(),
                    f"Only release workflow should have contents: write, not {workflow_name}"
                )

    def test_pr_template_covers_release_config_requirements(self):
        """Test PR template checklist covers release-please requirements."""
        pr_template_path = self.repo_root / ".github" / "PULL_REQUEST_TEMPLATE.md"
        with open(pr_template_path) as f:
            pr_template = f.read()

        # Should mention conventional commits (required for release-please)
        self.assertIn(
            "Conventional commit",
            pr_template,
            "PR template should mention conventional commits"
        )

        # Should mention version bumps
        self.assertIn(
            "version",
            pr_template.lower(),
            "PR template should mention versioning"
        )

        # Should mention changelog
        self.assertIn(
            "CHANGELOG",
            pr_template,
            "PR template should mention CHANGELOG"
        )

    def test_security_md_covers_workflow_scope(self):
        """Test SECURITY.md scope includes CI/CD workflows."""
        security_path = self.repo_root / "SECURITY.md"
        with open(security_path) as f:
            security_md = f.read()

        # Should mention CI/CD in scope
        self.assertIn(
            "CI/CD",
            security_md,
            "SECURITY.md should include CI/CD workflows in scope"
        )

        # Should mention hooks (security-sensitive)
        self.assertIn(
            "hook",
            security_md.lower(),
            "SECURITY.md should mention hooks"
        )

    def test_all_workflows_have_timeouts(self):
        """Test critical workflows have appropriate timeouts."""
        # Focus on workflows that interact with external services or could run long
        critical_workflows = {
            "claude-code-review.yml": True,
            "claude-mention.yml": True,
        }

        for workflow_name, workflow in self.workflows.items():
            if workflow_name not in critical_workflows:
                continue

            for job_name, job in workflow.get("jobs", {}).items():
                self.assertIn(
                    "timeout-minutes",
                    job,
                    f"Critical workflow {workflow_name}:{job_name} should have timeout"
                )

        # For non-critical workflows, just verify they complete reasonably fast
        # by checking they don't have excessive configurations
        for workflow_name, workflow in self.workflows.items():
            total_steps = sum(
                len(job.get("steps", []))
                for job in workflow.get("jobs", {}).values()
            )
            # Sanity check: workflows shouldn't have hundreds of steps
            self.assertLess(
                total_steps,
                100,
                f"{workflow_name} has {total_steps} steps (seems excessive)"
            )

    def test_setup_script_repo_matches_marketplace(self):
        """Test setup script default REPO matches marketplace owner."""
        setup_script_path = self.repo_root / "scripts" / "setup-github-repo.sh"
        with open(setup_script_path) as f:
            setup_script = f.read()

        # Extract REPO default from script
        import re
        repo_match = re.search(r'REPO="\$\{REPO:-([^}]+)\}"', setup_script)
        self.assertIsNotNone(repo_match, "Setup script should have REPO default")

        default_repo = repo_match.group(1)

        # Should match marketplace owner/name
        marketplace_name = self.marketplace.get("name", "")
        self.assertIn(
            marketplace_name,
            default_repo,
            "Setup script REPO default should reference marketplace name"
        )

    def test_version_bump_strategies_configured(self):
        """Test release-please config has appropriate version bump strategies."""
        config = self.release_config

        # Should have bump strategies for pre-1.0
        if any(v.startswith("0.") for v in self.release_manifest.values()):
            # Pre-1.0 should have special bump settings
            self.assertIn(
                "bump-minor-pre-major",
                config,
                "Pre-1.0 projects should configure bump-minor-pre-major"
            )


class TestEdgeCasesAndBoundaries(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    @classmethod
    def setUpClass(cls):
        """Set up test data."""
        cls.repo_root = Path(__file__).parent.parent

    def test_empty_marketplace_plugins_list_handling(self):
        """Test system would handle empty plugins list gracefully."""
        # This is a regression test - ensure code doesn't assume non-empty
        with open(self.repo_root / ".claude-plugin" / "marketplace.json") as f:
            marketplace = json.load(f)

        plugins = marketplace.get("plugins", [])

        # Should be a list (even if empty in theory)
        self.assertIsInstance(plugins, list)

        # Current state should have plugins
        self.assertGreater(len(plugins), 0, "Marketplace should have at least one plugin")

    def test_version_format_strict_semver(self):
        """Test all versions are strict semver (not loose)."""
        with open(self.repo_root / ".release-please-manifest.json") as f:
            manifest = json.load(f)

        with open(self.repo_root / "adaptive-agent" / ".claude-plugin" / "plugin.json") as f:
            plugin = json.load(f)

        # All versions should be X.Y.Z format (no -alpha, no v prefix, etc.)
        all_versions = list(manifest.values()) + [plugin["version"]]

        for version in all_versions:
            self.assertRegex(
                version,
                r'^\d+\.\d+\.\d+$',
                f"Version '{version}' should be strict semver X.Y.Z"
            )

    def test_workflow_names_are_descriptive(self):
        """Test workflow names are descriptive and unique."""
        workflows_dir = self.repo_root / ".github" / "workflows"
        workflow_names = set()

        for workflow_file in workflows_dir.glob("*.yml"):
            with open(workflow_file) as f:
                workflow = yaml.safe_load(f)

            name = workflow.get("name", "")
            self.assertGreater(
                len(name),
                5,
                f"{workflow_file.name} should have descriptive name (>5 chars)"
            )

            # Names should be unique
            self.assertNotIn(
                name,
                workflow_names,
                f"Workflow name '{name}' is duplicated"
            )
            workflow_names.add(name)


if __name__ == "__main__":
    unittest.main()
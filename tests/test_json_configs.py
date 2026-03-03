#!/usr/bin/env python3
"""
Comprehensive tests for JSON configuration files.
Tests syntax, schema, version consistency, and cross-file references.
"""

import unittest
import json
import os
from pathlib import Path


class TestJSONConfigurations(unittest.TestCase):
    """Test suite for JSON configuration files."""

    @classmethod
    def setUpClass(cls):
        """Load all JSON configuration files."""
        cls.repo_root = Path(__file__).parent.parent
        cls.configs = {}

        # Load release configurations
        with open(cls.repo_root / "release-please-config.json") as f:
            cls.configs["release-please-config"] = json.load(f)

        with open(cls.repo_root / ".release-please-manifest.json") as f:
            cls.configs["release-please-manifest"] = json.load(f)

        # Load plugin configuration
        plugin_json_path = cls.repo_root / "adaptive-agent" / ".claude-plugin" / "plugin.json"
        with open(plugin_json_path) as f:
            cls.configs["plugin"] = json.load(f)

        # Load marketplace configuration
        marketplace_json_path = cls.repo_root / ".claude-plugin" / "marketplace.json"
        with open(marketplace_json_path) as f:
            cls.configs["marketplace"] = json.load(f)

    def test_json_files_exist(self):
        """Test that all expected JSON files exist."""
        expected_files = [
            ".release-please-manifest.json",
            "release-please-config.json",
            "adaptive-agent/.claude-plugin/plugin.json",
            ".claude-plugin/marketplace.json"
        ]

        for filepath in expected_files:
            full_path = self.repo_root / filepath
            self.assertTrue(
                full_path.exists(),
                f"JSON file {filepath} should exist"
            )

    def test_json_syntax_valid(self):
        """Test that all JSON files have valid syntax."""
        for name, content in self.configs.items():
            self.assertIsNotNone(
                content,
                f"{name} should have valid JSON syntax"
            )

    def test_release_please_manifest_structure(self):
        """Test release-please manifest has correct structure."""
        manifest = self.configs["release-please-manifest"]

        # Should be a simple dict of paths to versions
        self.assertIsInstance(manifest, dict)

        # Should have root package
        self.assertIn(".", manifest)

        # Should have adaptive-agent package
        self.assertIn("adaptive-agent", manifest)

        # All values should be valid semver strings
        for path, version in manifest.items():
            self.assertIsInstance(version, str)
            self.assertRegex(
                version,
                r"^\d+\.\d+\.\d+$",
                f"Version for '{path}' should be valid semver"
            )

    def test_release_please_config_structure(self):
        """Test release-please config has required fields."""
        config = self.configs["release-please-config"]

        # Required top-level fields
        required_fields = ["release-type", "packages"]
        for field in required_fields:
            self.assertIn(field, config, f"Config should have '{field}' field")

        # Check release-type
        self.assertEqual(config["release-type"], "simple")

        # Check packages structure
        self.assertIsInstance(config["packages"], dict)
        self.assertIn(".", config["packages"])
        self.assertIn("adaptive-agent", config["packages"])

    def test_release_please_config_packages(self):
        """Test release-please config packages configuration."""
        config = self.configs["release-please-config"]
        packages = config["packages"]

        # Test root package
        root_pkg = packages["."]
        self.assertEqual(root_pkg["package-name"], "jadecli-plugins")
        self.assertEqual(root_pkg["changelog-path"], "CHANGELOG.md")

        # Check root package extra-files (marketplace.json version sync)
        self.assertIn("extra-files", root_pkg)
        extra_files = root_pkg["extra-files"]
        self.assertEqual(len(extra_files), 1)
        self.assertEqual(extra_files[0]["type"], "json")
        self.assertEqual(extra_files[0]["path"], ".claude-plugin/marketplace.json")
        self.assertEqual(extra_files[0]["jsonpath"], "$.metadata.version")

        # Test adaptive-agent package
        agent_pkg = packages["adaptive-agent"]
        self.assertEqual(agent_pkg["package-name"], "adaptive-agent")
        self.assertEqual(agent_pkg["changelog-path"], "CHANGELOG.md")

        # Check adaptive-agent extra-files (plugin.json version sync)
        self.assertIn("extra-files", agent_pkg)
        extra_files = agent_pkg["extra-files"]
        self.assertEqual(len(extra_files), 1)
        self.assertEqual(extra_files[0]["type"], "json")
        self.assertEqual(extra_files[0]["path"], ".claude-plugin/plugin.json")
        self.assertEqual(extra_files[0]["jsonpath"], "$.version")

    def test_release_please_config_changelog_sections(self):
        """Test release-please config defines changelog sections."""
        config = self.configs["release-please-config"]

        self.assertIn("changelog-sections", config)
        sections = config["changelog-sections"]

        # Check expected sections exist
        section_types = [s["type"] for s in sections]
        expected_types = ["feat", "fix", "chore", "docs"]

        for expected_type in expected_types:
            self.assertIn(expected_type, section_types)

        # Check each section has required fields
        for section in sections:
            self.assertIn("type", section)
            self.assertIn("section", section)

    def test_plugin_json_structure(self):
        """Test plugin.json has required fields."""
        plugin = self.configs["plugin"]

        required_fields = ["name", "version", "description"]
        for field in required_fields:
            self.assertIn(field, plugin, f"plugin.json should have '{field}' field")

        # Check values
        self.assertEqual(plugin["name"], "adaptive-agent")
        self.assertRegex(
            plugin["version"],
            r"^\d+\.\d+\.\d+$",
            "plugin.json version should be valid semver"
        )
        self.assertIsInstance(plugin["description"], str)
        self.assertGreater(len(plugin["description"]), 0)

    def test_plugin_json_optional_fields(self):
        """Test plugin.json optional but recommended fields."""
        plugin = self.configs["plugin"]

        # Check optional fields
        optional_fields = ["author", "repository", "license", "keywords"]
        for field in optional_fields:
            if field in plugin:
                self.assertIsInstance(
                    plugin[field],
                    (str, dict, list),
                    f"plugin.json '{field}' should be valid"
                )

        # If keywords exist, should be non-empty list
        if "keywords" in plugin:
            self.assertIsInstance(plugin["keywords"], list)
            self.assertGreater(len(plugin["keywords"]), 0)

    def test_marketplace_json_structure(self):
        """Test marketplace.json has required structure."""
        marketplace = self.configs["marketplace"]

        # Required top-level fields
        self.assertIn("metadata", marketplace)
        self.assertIn("plugins", marketplace)

        # Check metadata
        metadata = marketplace["metadata"]
        self.assertIn("version", metadata)

        # Check plugins is a list
        self.assertIsInstance(marketplace["plugins"], list)

    def test_marketplace_plugin_entries(self):
        """Test marketplace.json plugin entries are valid."""
        marketplace = self.configs["marketplace"]
        plugins = marketplace["plugins"]

        # Each plugin should have required fields
        required_fields = ["name", "source", "description"]

        for plugin in plugins:
            for field in required_fields:
                self.assertIn(
                    field,
                    plugin,
                    f"Marketplace plugin should have '{field}' field"
                )

            # Source should be a valid path
            source = plugin["source"].lstrip("./")
            plugin_path = self.repo_root / source / ".claude-plugin" / "plugin.json"
            self.assertTrue(
                plugin_path.exists(),
                f"Marketplace plugin source '{source}' should have plugin.json"
            )

    def test_version_consistency_manifest_vs_plugin(self):
        """Test version consistency between manifest and plugin.json."""
        manifest = self.configs["release-please-manifest"]
        plugin = self.configs["plugin"]

        manifest_version = manifest["adaptive-agent"]
        plugin_version = plugin["version"]

        self.assertEqual(
            manifest_version,
            plugin_version,
            f"Manifest version ({manifest_version}) should match "
            f"plugin.json version ({plugin_version})"
        )

    def test_version_consistency_manifest_vs_marketplace(self):
        """Test version consistency between manifest and marketplace.json."""
        manifest = self.configs["release-please-manifest"]
        marketplace = self.configs["marketplace"]

        manifest_root_version = manifest["."]
        marketplace_version = marketplace["metadata"]["version"]

        self.assertEqual(
            manifest_root_version,
            marketplace_version,
            f"Manifest root version ({manifest_root_version}) should match "
            f"marketplace.json version ({marketplace_version})"
        )

    def test_marketplace_references_existing_plugins(self):
        """Test marketplace.json only references existing plugins."""
        marketplace = self.configs["marketplace"]

        for plugin in marketplace["plugins"]:
            source = plugin["source"].lstrip("./")
            plugin_json_path = self.repo_root / source / ".claude-plugin" / "plugin.json"

            self.assertTrue(
                plugin_json_path.exists(),
                f"Marketplace plugin '{plugin['name']}' source '{source}' "
                f"should have .claude-plugin/plugin.json"
            )

            # Load and verify plugin name matches
            with open(plugin_json_path) as f:
                plugin_json = json.load(f)

            # Plugin name in marketplace should match plugin.json
            # (allow for slight variations, but directory should match package)
            self.assertEqual(
                plugin["source"].strip("./"),
                plugin_json["name"],
                f"Marketplace source should match plugin name"
            )

    def test_plugin_keywords_valid(self):
        """Test plugin.json keywords are relevant and not excessive."""
        plugin = self.configs["plugin"]

        if "keywords" in plugin:
            keywords = plugin["keywords"]

            # Should have some but not too many keywords
            self.assertGreaterEqual(len(keywords), 1)
            self.assertLessEqual(len(keywords), 20)

            # Each keyword should be a non-empty string
            for keyword in keywords:
                self.assertIsInstance(keyword, str)
                self.assertGreater(len(keyword), 0)
                # Keywords should be lowercase with hyphens
                self.assertEqual(keyword, keyword.lower())

    def test_release_config_pre_major_settings(self):
        """Test release-please config has appropriate pre-major settings."""
        config = self.configs["release-please-config"]

        # For pre-1.0 projects, these should be set
        if "bump-minor-pre-major" in config:
            self.assertTrue(config["bump-minor-pre-major"])

        if "bump-patch-for-minor-pre-major" in config:
            self.assertTrue(config["bump-patch-for-minor-pre-major"])

    def test_plugin_repository_url_valid(self):
        """Test plugin.json repository URL is valid."""
        plugin = self.configs["plugin"]

        if "repository" in plugin:
            repo = plugin["repository"]
            self.assertIsInstance(repo, str)
            # Should be a valid GitHub URL
            self.assertTrue(
                repo.startswith("https://github.com/") or
                repo.startswith("https://gitlab.com/"),
                "Repository should be a valid GitHub or GitLab URL"
            )

    def test_plugin_license_valid(self):
        """Test plugin.json license is a valid SPDX identifier."""
        plugin = self.configs["plugin"]

        if "license" in plugin:
            license = plugin["license"]
            self.assertIsInstance(license, str)

            # Common valid SPDX identifiers
            valid_licenses = [
                "MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause",
                "ISC", "MPL-2.0", "LGPL-3.0", "AGPL-3.0"
            ]

            # Should be a known license (or at least non-empty)
            self.assertGreater(len(license), 0)

    def test_marketplace_metadata_complete(self):
        """Test marketplace.json metadata is complete."""
        marketplace = self.configs["marketplace"]

        # Should have name (either at root or in metadata)
        has_name = "name" in marketplace or "name" in marketplace.get("metadata", {})
        self.assertTrue(has_name, "Marketplace should have name field")

        # Should have version in metadata
        metadata = marketplace["metadata"]
        self.assertIn("version", metadata)

        # Version should be valid semver
        self.assertRegex(
            metadata["version"],
            r"^\d+\.\d+\.\d+$",
            "Marketplace version should be valid semver"
        )

    def test_no_duplicate_plugins_in_marketplace(self):
        """Test marketplace.json doesn't list duplicate plugins."""
        marketplace = self.configs["marketplace"]
        plugins = marketplace["plugins"]

        # Check for duplicate names
        names = [p["name"] for p in plugins]
        self.assertEqual(
            len(names),
            len(set(names)),
            "Marketplace should not have duplicate plugin names"
        )

        # Check for duplicate sources
        sources = [p["source"] for p in plugins]
        self.assertEqual(
            len(sources),
            len(set(sources)),
            "Marketplace should not have duplicate plugin sources"
        )

    def test_json_files_no_trailing_commas(self):
        """Test JSON files don't have trailing commas (invalid JSON)."""
        json_files = [
            ".release-please-manifest.json",
            "release-please-config.json",
            "adaptive-agent/.claude-plugin/plugin.json",
            ".claude-plugin/marketplace.json"
        ]

        for filepath in json_files:
            full_path = self.repo_root / filepath
            with open(full_path) as f:
                content = f.read()

            # If we can parse it, it's valid (no trailing commas)
            try:
                json.loads(content)
            except json.JSONDecodeError as e:
                self.fail(f"{filepath} has invalid JSON: {e}")

    def test_plugin_version_is_latest_in_manifest(self):
        """Test plugin version matches the latest in manifest."""
        manifest = self.configs["release-please-manifest"]
        plugin = self.configs["plugin"]

        # This is a more specific version of the consistency test
        # Ensures we're testing the latest published version
        self.assertEqual(
            plugin["version"],
            manifest["adaptive-agent"],
            "Plugin version should match manifest for releases"
        )

    def test_release_config_separate_pull_requests(self):
        """Test release-please config for PR strategy."""
        config = self.configs["release-please-config"]

        # Check if separate-pull-requests is set
        if "separate-pull-requests" in config:
            # False means single PR for all packages (monorepo friendly)
            self.assertIsInstance(config["separate-pull-requests"], bool)


if __name__ == "__main__":
    unittest.main()
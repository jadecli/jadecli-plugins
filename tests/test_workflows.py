#!/usr/bin/env python3
"""
Comprehensive tests for GitHub workflow YAML files.
Tests syntax, structure, required fields, security, and workflow logic.
"""

import unittest
import yaml
import os
from pathlib import Path


class TestGitHubWorkflows(unittest.TestCase):
    """Test suite for GitHub workflow files."""

    @classmethod
    def setUpClass(cls):
        """Load all workflow files once for all tests."""
        cls.repo_root = Path(__file__).parent.parent
        cls.workflows_dir = cls.repo_root / ".github" / "workflows"
        cls.workflows = {}

        workflow_files = [
            "claude-code-review.yml",
            "claude-mention.yml",
            "release-doctor.yml",
            "release.yml",
            "validate.yml"
        ]

        for filename in workflow_files:
            filepath = cls.workflows_dir / filename
            with open(filepath, 'r') as f:
                cls.workflows[filename] = yaml.safe_load(f)

    def test_workflow_files_exist(self):
        """Test that all expected workflow files exist."""
        expected_files = [
            "claude-code-review.yml",
            "claude-mention.yml",
            "release-doctor.yml",
            "release.yml",
            "validate.yml"
        ]

        for filename in expected_files:
            filepath = self.workflows_dir / filename
            self.assertTrue(
                filepath.exists(),
                f"Workflow file {filename} should exist"
            )

    def test_workflow_yaml_syntax(self):
        """Test that all workflow files have valid YAML syntax."""
        for filename, content in self.workflows.items():
            self.assertIsNotNone(
                content,
                f"{filename} should have valid YAML syntax"
            )
            self.assertIsInstance(
                content,
                dict,
                f"{filename} should parse to a dictionary"
            )

    def test_workflow_required_fields(self):
        """Test that all workflows have required top-level fields."""
        for filename, workflow in self.workflows.items():
            # Check name field
            self.assertIn(
                "name",
                workflow,
                f"{filename} should have 'name' field"
            )

            # Check 'on' field (may be parsed as True in YAML 1.1)
            has_on_field = "on" in workflow or True in workflow
            self.assertTrue(
                has_on_field,
                f"{filename} should have 'on' field"
            )

            # Check jobs field
            self.assertIn(
                "jobs",
                workflow,
                f"{filename} should have 'jobs' field"
            )

    def test_claude_code_review_structure(self):
        """Test claude-code-review.yml specific structure."""
        workflow = self.workflows["claude-code-review.yml"]

        # Check trigger (YAML 'on' may be parsed as True)
        on_field = workflow.get("on") or workflow.get(True)
        self.assertIsNotNone(on_field, "Workflow should have 'on' trigger")
        self.assertIn("pull_request", on_field)
        self.assertEqual(
            on_field["pull_request"]["types"],
            ["opened", "synchronize"]
        )

        # Check permissions
        self.assertIn("permissions", workflow)
        self.assertEqual(workflow["permissions"]["contents"], "read")
        self.assertEqual(workflow["permissions"]["pull-requests"], "write")
        self.assertEqual(workflow["permissions"]["issues"], "write")

        # Check jobs
        self.assertIn("review", workflow["jobs"])
        review_job = workflow["jobs"]["review"]

        # Check job configuration
        self.assertEqual(review_job["runs-on"], "ubuntu-latest")
        self.assertEqual(review_job["timeout-minutes"], 5)

        # Check conditional execution (skip bots)
        self.assertIn("if", review_job)
        self.assertIn("github.actor != 'github-actions[bot]'", review_job["if"])
        self.assertIn("github.actor != 'release-please[bot]'", review_job["if"])

    def test_claude_mention_structure(self):
        """Test claude-mention.yml specific structure."""
        workflow = self.workflows["claude-mention.yml"]

        # Check triggers (YAML 'on' may be parsed as True)
        on_field = workflow.get("on") or workflow.get(True)
        self.assertIsNotNone(on_field, "Workflow should have 'on' trigger")
        self.assertIn("issue_comment", on_field)
        self.assertIn("pull_request_review_comment", on_field)

        # Check permissions include id-token for OIDC
        self.assertIn("permissions", workflow)
        self.assertEqual(workflow["permissions"]["id-token"], "write")

        # Check jobs
        self.assertIn("respond", workflow["jobs"])
        respond_job = workflow["jobs"]["respond"]

        # Check conditional execution (only when @claude mentioned)
        self.assertIn("if", respond_job)
        self.assertIn("contains(github.event.comment.body, '@claude')", respond_job["if"])

        # Check timeout
        self.assertEqual(respond_job["timeout-minutes"], 10)

    def test_release_doctor_structure(self):
        """Test release-doctor.yml specific structure."""
        workflow = self.workflows["release-doctor.yml"]

        # Check triggers (YAML 'on' may be parsed as True)
        on_field = workflow.get("on") or workflow.get(True)
        self.assertIsNotNone(on_field, "Workflow should have 'on' trigger")
        self.assertIn("push", on_field)
        self.assertIn("workflow_dispatch", on_field)
        self.assertEqual(on_field["push"]["branches"], ["main"])

        # Check job
        self.assertIn("check-release-health", workflow["jobs"])
        job = workflow["jobs"]["check-release-health"]

        # Check steps exist
        self.assertIn("steps", job)
        step_names = [step.get("name", "") for step in job["steps"]]

        self.assertIn("Validate release-please configuration", step_names)
        self.assertIn("Check version consistency", step_names)
        self.assertIn("Validate CHANGELOG exists", step_names)

    def test_release_workflow_structure(self):
        """Test release.yml specific structure."""
        workflow = self.workflows["release.yml"]

        # Check trigger (only on main push, YAML 'on' may be parsed as True)
        on_field = workflow.get("on") or workflow.get(True)
        self.assertIsNotNone(on_field, "Workflow should have 'on' trigger")
        self.assertIn("push", on_field)
        self.assertEqual(on_field["push"]["branches"], ["main"])

        # Check permissions for release creation
        self.assertIn("permissions", workflow)
        self.assertEqual(workflow["permissions"]["contents"], "write")
        self.assertEqual(workflow["permissions"]["pull-requests"], "write")

        # Check release-please job
        self.assertIn("release-please", workflow["jobs"])
        job = workflow["jobs"]["release-please"]

        # Check outputs defined
        self.assertIn("outputs", job)
        self.assertIn("releases_created", job["outputs"])
        self.assertIn("paths_released", job["outputs"])

        # Check release-please action step exists
        steps = job["steps"]
        action_steps = [s for s in steps if "uses" in s and "release-please-action" in s["uses"]]
        self.assertEqual(len(action_steps), 1, "Should use release-please-action")

        # Check config files are specified
        release_step = action_steps[0]
        self.assertEqual(release_step["with"]["config-file"], "release-please-config.json")
        self.assertEqual(release_step["with"]["manifest-file"], ".release-please-manifest.json")

    def test_validate_workflow_structure(self):
        """Test validate.yml comprehensive structure."""
        workflow = self.workflows["validate.yml"]

        # Check trigger (PR to main, YAML 'on' may be parsed as True)
        on_field = workflow.get("on") or workflow.get(True)
        self.assertIsNotNone(on_field, "Workflow should have 'on' trigger")
        self.assertIn("pull_request", on_field)
        self.assertEqual(on_field["pull_request"]["branches"], ["main"])

        # Check all validation jobs exist
        expected_jobs = [
            "validate-json",
            "validate-structure",
            "lint-commits",
            "validate-release-config",
            "lint-markdown"
        ]

        for job_name in expected_jobs:
            self.assertIn(job_name, workflow["jobs"], f"Job {job_name} should exist")

        # Check validate-json job
        validate_json = workflow["jobs"]["validate-json"]
        step_names = [step.get("name", "") for step in validate_json["steps"]]
        self.assertIn("Validate marketplace.json", step_names)
        self.assertIn("Validate plugin.json files", step_names)
        self.assertIn("Validate hooks.json files", step_names)

        # Check lint-commits only runs on PRs
        lint_commits = workflow["jobs"]["lint-commits"]
        self.assertIn("if", lint_commits)
        self.assertEqual(lint_commits["if"], "github.event_name == 'pull_request'")

    def test_workflow_security_best_practices(self):
        """Test workflows follow security best practices."""
        for filename, workflow in self.workflows.items():
            # Check permissions are explicitly set (not default)
            self.assertIn(
                "permissions",
                workflow,
                f"{filename} should explicitly set permissions"
            )

            # Check no hardcoded secrets in workflow
            workflow_str = str(workflow)
            self.assertNotIn(
                "sk-",
                workflow_str,
                f"{filename} should not contain hardcoded API keys"
            )
            self.assertNotIn(
                "password:",
                workflow_str.lower(),
                f"{filename} should not contain hardcoded passwords"
            )

    def test_workflow_timeout_settings(self):
        """Test that jobs have appropriate timeout settings."""
        timeout_expectations = {
            "claude-code-review.yml": 5,
            "claude-mention.yml": 10,
        }

        for filename, expected_timeout in timeout_expectations.items():
            workflow = self.workflows[filename]
            for job_name, job in workflow["jobs"].items():
                if "timeout-minutes" in job:
                    self.assertEqual(
                        job["timeout-minutes"],
                        expected_timeout,
                        f"{filename} job '{job_name}' should have {expected_timeout} min timeout"
                    )

    def test_workflows_use_actions_checkout(self):
        """Test that workflows properly checkout code."""
        for filename, workflow in self.workflows.items():
            for job_name, job in workflow["jobs"].items():
                if "steps" in job:
                    # Check if any step uses actions/checkout
                    checkout_steps = [
                        s for s in job["steps"]
                        if "uses" in s and "actions/checkout" in s["uses"]
                    ]

                    # Jobs should checkout code (except maybe some edge cases)
                    self.assertGreater(
                        len(checkout_steps),
                        0,
                        f"{filename} job '{job_name}' should checkout code"
                    )

    def test_validate_workflow_python_validation(self):
        """Test that validate.yml uses Python for JSON validation."""
        workflow = self.workflows["validate.yml"]

        # Check validate-json job uses Python
        validate_json = workflow["jobs"]["validate-json"]
        steps = validate_json["steps"]

        # Find validation steps
        validation_steps = [
            s for s in steps
            if "run" in s and "python3" in s["run"]
        ]

        self.assertGreater(
            len(validation_steps),
            0,
            "validate-json job should use Python for validation"
        )

    def test_release_doctor_version_consistency_check(self):
        """Test that release-doctor properly checks version consistency."""
        workflow = self.workflows["release-doctor.yml"]
        job = workflow["jobs"]["check-release-health"]

        # Find version consistency step
        version_steps = [
            s for s in job["steps"]
            if s.get("name") == "Check version consistency"
        ]

        self.assertEqual(len(version_steps), 1)
        version_step = version_steps[0]

        # Check it uses Python and checks manifest/plugin.json
        self.assertIn("python3", version_step["run"])
        self.assertIn("manifest", version_step["run"].lower())
        self.assertIn("plugin.json", version_step["run"])

    def test_conditional_claude_activation(self):
        """Test Claude workflows have activation guards."""
        claude_workflows = [
            "claude-code-review.yml",
            "claude-mention.yml"
        ]

        for filename in claude_workflows:
            workflow = self.workflows[filename]

            # Check for placeholder step
            for job_name, job in workflow["jobs"].items():
                steps = job.get("steps", [])
                placeholder_steps = [
                    s for s in steps
                    if "name" in s and "placeholder" in s["name"].lower()
                ]

                self.assertGreater(
                    len(placeholder_steps),
                    0,
                    f"{filename} should have placeholder step before activation"
                )

    def test_workflow_runner_os(self):
        """Test all workflows use ubuntu-latest."""
        for filename, workflow in self.workflows.items():
            for job_name, job in workflow["jobs"].items():
                if "runs-on" in job:
                    self.assertEqual(
                        job["runs-on"],
                        "ubuntu-latest",
                        f"{filename} job '{job_name}' should use ubuntu-latest"
                    )

    def test_release_please_action_version(self):
        """Test release workflow uses specific release-please version."""
        workflow = self.workflows["release.yml"]
        job = workflow["jobs"]["release-please"]

        release_steps = [
            s for s in job["steps"]
            if "uses" in s and "release-please-action" in s["uses"]
        ]

        self.assertEqual(len(release_steps), 1)
        self.assertIn("@v4", release_steps[0]["uses"])

    def test_commitlint_setup(self):
        """Test validate workflow properly sets up commitlint."""
        workflow = self.workflows["validate.yml"]
        job = workflow["jobs"]["lint-commits"]

        # Check Node.js setup
        node_steps = [
            s for s in job["steps"]
            if "uses" in s and "actions/setup-node" in s["uses"]
        ]
        self.assertEqual(len(node_steps), 1)
        self.assertEqual(node_steps[0]["with"]["node-version"], 20)

        # Check commitlint installation
        install_steps = [
            s for s in job["steps"]
            if "name" in s and "install commitlint" in s["name"].lower()
        ]
        self.assertEqual(len(install_steps), 1)
        self.assertIn("@commitlint/cli", install_steps[0]["run"])

    def test_markdown_linting_action(self):
        """Test validate workflow uses markdownlint action."""
        workflow = self.workflows["validate.yml"]
        job = workflow["jobs"]["lint-markdown"]

        markdownlint_steps = [
            s for s in job["steps"]
            if "uses" in s and "markdownlint-cli2-action" in s["uses"]
        ]

        self.assertEqual(len(markdownlint_steps), 1)
        self.assertEqual(markdownlint_steps[0]["with"]["globs"], "**/*.md")


if __name__ == "__main__":
    unittest.main()
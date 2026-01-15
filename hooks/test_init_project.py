#!/usr/bin/env python3
"""
Unit tests for init-project.py

Run with: python -m unittest hooks/test_init_project.py -v
"""

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

# Import module with hyphen in name using importlib
import importlib.util
spec = importlib.util.spec_from_file_location(
    "init_project",
    Path(__file__).parent / "init-project.py"
)
init_project = importlib.util.module_from_spec(spec)
spec.loader.exec_module(init_project)

# Import functions
get_project_root = init_project.get_project_root
load_project_config = init_project.load_project_config
remove_existing_symlinks = init_project.remove_existing_symlinks
create_symlinks_from_available = init_project.create_symlinks_from_available
extract_sections = init_project.extract_sections
update_claude_md = init_project.update_claude_md


class TestLoadProjectConfig(unittest.TestCase):
    """Tests for load_project_config function."""

    def setUp(self):
        """Create a temporary directory for tests with .claude subdirectory."""
        self.test_dir = Path(tempfile.mkdtemp())
        (self.test_dir / ".claude").mkdir()

    def tearDown(self):
        """Remove the temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_valid_project_json(self):
        """Valid .claude/project.json returns dict with categories."""
        config = {
            "name": "test-project",
            "categories": ["dev", "php"],
            "exclude": [],
            "description": "Test project"
        }
        project_json = self.test_dir / ".claude" / "project.json"
        project_json.write_text(json.dumps(config))

        result = load_project_config(self.test_dir)

        self.assertEqual(result["name"], "test-project")
        self.assertEqual(result["categories"], ["dev", "php"])

    def test_missing_project_json_exits(self):
        """Missing .claude/project.json calls sys.exit(1)."""
        with self.assertRaises(SystemExit) as cm:
            load_project_config(self.test_dir)
        self.assertEqual(cm.exception.code, 1)

    def test_invalid_json_raises_error(self):
        """Invalid JSON raises JSONDecodeError."""
        project_json = self.test_dir / ".claude" / "project.json"
        project_json.write_text("{ invalid json }")

        with self.assertRaises(json.JSONDecodeError):
            load_project_config(self.test_dir)


class TestRemoveExistingSymlinks(unittest.TestCase):
    """Tests for remove_existing_symlinks function."""

    def setUp(self):
        """Create a temporary directory for tests."""
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Remove the temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_removes_symlinks(self):
        """Removes symlinks and returns count."""
        # Create a target file and symlink
        target = self.test_dir / "target.txt"
        target.write_text("content")
        link = self.test_dir / "link.txt"
        link.symlink_to(target)

        count = remove_existing_symlinks(self.test_dir)

        self.assertEqual(count, 1)
        self.assertFalse(link.exists())
        self.assertTrue(target.exists())  # Original file preserved

    def test_keeps_regular_files(self):
        """Keeps regular files, returns 0."""
        regular_file = self.test_dir / "file.txt"
        regular_file.write_text("content")

        count = remove_existing_symlinks(self.test_dir)

        self.assertEqual(count, 0)
        self.assertTrue(regular_file.exists())

    def test_mixed_symlinks_and_files(self):
        """Removes only symlinks from mixed content."""
        # Create regular file
        regular_file = self.test_dir / "file.txt"
        regular_file.write_text("content")

        # Create symlink
        target = self.test_dir / "target.txt"
        target.write_text("target content")
        link = self.test_dir / "link.txt"
        link.symlink_to(target)

        count = remove_existing_symlinks(self.test_dir)

        self.assertEqual(count, 1)
        self.assertTrue(regular_file.exists())
        self.assertFalse(link.exists())

    def test_empty_directory(self):
        """Empty directory returns 0."""
        count = remove_existing_symlinks(self.test_dir)
        self.assertEqual(count, 0)


class TestCreateSymlinksFromAvailable(unittest.TestCase):
    """Tests for create_symlinks_from_available function."""

    def setUp(self):
        """Create temporary directories for tests."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.source_dir = self.test_dir / "skills-available"
        self.target_dir = self.test_dir / "skills"
        self.source_dir.mkdir()
        self.target_dir.mkdir()

    def tearDown(self):
        """Remove the temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_flat_structure(self):
        """Creates symlinks for flat .md files (agents/commands pattern)."""
        # Create source structure: skills-available/dev/item.md
        dev_dir = self.source_dir / "dev"
        dev_dir.mkdir()
        (dev_dir / "test-agent.md").write_text("# Agent")

        count = create_symlinks_from_available(
            self.source_dir, self.target_dir, ["dev"], []
        )

        self.assertEqual(count, 1)
        link = self.target_dir / "test-agent.md"
        self.assertTrue(link.is_symlink())

    def test_nested_structure(self):
        """Creates symlinks for nested SKILL.md directories."""
        # Create source structure: skills-available/dev/my-skill/SKILL.md
        dev_dir = self.source_dir / "dev"
        dev_dir.mkdir()
        skill_dir = dev_dir / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# Skill")

        count = create_symlinks_from_available(
            self.source_dir, self.target_dir, ["dev"], []
        )

        self.assertEqual(count, 1)
        link = self.target_dir / "my-skill"
        self.assertTrue(link.is_symlink())

    def test_skips_unlisted_category(self):
        """Skips categories not in the list."""
        # Create two categories
        dev_dir = self.source_dir / "dev"
        dev_dir.mkdir()
        (dev_dir / "dev-item.md").write_text("# Dev")

        php_dir = self.source_dir / "php"
        php_dir.mkdir()
        (php_dir / "php-item.md").write_text("# PHP")

        # Only include dev
        count = create_symlinks_from_available(
            self.source_dir, self.target_dir, ["dev"], []
        )

        self.assertEqual(count, 1)
        self.assertTrue((self.target_dir / "dev-item.md").is_symlink())
        self.assertFalse((self.target_dir / "php-item.md").exists())

    def test_excludes_items(self):
        """Skips items in excludes list."""
        dev_dir = self.source_dir / "dev"
        dev_dir.mkdir()
        (dev_dir / "include-me.md").write_text("# Include")
        (dev_dir / "exclude-me.md").write_text("# Exclude")

        count = create_symlinks_from_available(
            self.source_dir, self.target_dir, ["dev"], ["skills/exclude-me"]
        )

        self.assertEqual(count, 1)
        self.assertTrue((self.target_dir / "include-me.md").is_symlink())
        self.assertFalse((self.target_dir / "exclude-me.md").exists())

    def test_includes_local_folder(self):
        """Includes items from local/ folder."""
        local_dir = self.source_dir / "local"
        local_dir.mkdir()
        (local_dir / "local-item.md").write_text("# Local")

        count = create_symlinks_from_available(
            self.source_dir, self.target_dir, [], []  # No categories needed for local
        )

        self.assertEqual(count, 1)
        self.assertTrue((self.target_dir / "local-item.md").is_symlink())

    def test_overwrites_existing_symlink(self):
        """Overwrites existing symlink."""
        dev_dir = self.source_dir / "dev"
        dev_dir.mkdir()
        source_file = dev_dir / "item.md"
        source_file.write_text("# Item")

        # Create existing symlink pointing elsewhere
        old_target = self.test_dir / "old-target.md"
        old_target.write_text("old")
        existing_link = self.target_dir / "item.md"
        existing_link.symlink_to(old_target)

        count = create_symlinks_from_available(
            self.source_dir, self.target_dir, ["dev"], []
        )

        self.assertEqual(count, 1)
        # Verify it now points to the correct location
        self.assertTrue(existing_link.is_symlink())


class TestExtractSections(unittest.TestCase):
    """Tests for extract_sections function."""

    def setUp(self):
        """Create a temporary directory for tests."""
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Remove the temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_extracts_matching_categories(self):
        """Extracts sections from matching categories."""
        md_file = self.test_dir / "AGENTS.md"
        md_file.write_text("""# Agents

## Category: dev

### debugging-assistant
Use when debugging issues.

### test-generator
Use when generating tests.

## Category: php

### php-specialist
Use for PHP code.
""")

        result = extract_sections(md_file, ["dev"], "agents")

        self.assertIn("debugging-assistant", result)
        self.assertIn("test-generator", result)
        self.assertNotIn("php-specialist", result)

    def test_nonexistent_file_returns_empty(self):
        """Non-existent file returns empty string."""
        result = extract_sections(self.test_dir / "missing.md", ["dev"], "agents")
        self.assertEqual(result, "")

    def test_no_matching_categories_returns_empty(self):
        """No matching categories returns empty string."""
        md_file = self.test_dir / "AGENTS.md"
        md_file.write_text("""# Agents

## Category: php

### php-specialist
Use for PHP code.
""")

        result = extract_sections(md_file, ["dev"], "agents")
        self.assertEqual(result, "")


class TestUpdateClaudeMd(unittest.TestCase):
    """Tests for update_claude_md function."""

    def setUp(self):
        """Create a temporary directory for tests."""
        self.test_dir = Path(tempfile.mkdtemp())
        # Create required files
        (self.test_dir / "AGENTS.md").write_text("""# Agents

## Category: dev

### debugging-assistant
Use when debugging.
""")
        (self.test_dir / "SKILLS.md").write_text("""# Skills

## Category: dev

### tdd
Use for TDD.
""")

    def tearDown(self):
        """Remove the temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_updates_existing_claude_md(self):
        """Updates content between markers in existing CLAUDE.md."""
        claude_md = self.test_dir / "CLAUDE.md"
        claude_md.write_text("""# CLAUDE.md

<!-- BEGIN:AGENTS -->
old content
<!-- END:AGENTS -->

<!-- BEGIN:SKILLS -->
old content
<!-- END:SKILLS -->
""")

        update_claude_md(self.test_dir, ["dev"])

        content = claude_md.read_text()
        self.assertIn("debugging-assistant", content)
        self.assertIn("tdd", content)
        self.assertNotIn("old content", content)

    def test_appends_section_if_no_markers(self):
        """Appends guidelines section if CLAUDE.md exists without markers."""
        claude_md = self.test_dir / "CLAUDE.md"
        claude_md.write_text("""# My Project

Some existing content that should be preserved.
""")

        update_claude_md(self.test_dir, ["dev"])

        content = claude_md.read_text()
        # Original content preserved
        self.assertIn("My Project", content)
        self.assertIn("Some existing content", content)
        # New section appended
        self.assertIn("BEGIN:AGENTS", content)
        self.assertIn("debugging-assistant", content)
        self.assertIn("BEGIN:SKILLS", content)
        self.assertIn("tdd", content)

    def test_creates_default_if_missing(self):
        """Creates default CLAUDE.md if file doesn't exist."""
        update_claude_md(self.test_dir, ["dev"])

        claude_md = self.test_dir / "CLAUDE.md"
        self.assertTrue(claude_md.exists())
        content = claude_md.read_text()
        self.assertIn("BEGIN:AGENTS", content)
        self.assertIn("END:SKILLS", content)


class TestInitProjectPreservesCommand(unittest.TestCase):
    """Tests that init-project.md is preserved."""

    def setUp(self):
        """Create a temporary directory with init-project.md."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.commands_dir = self.test_dir / "commands"
        self.commands_dir.mkdir()
        self.init_project_md = self.commands_dir / "init-project.md"
        self.init_project_md.write_text("# Init Project Command")

    def tearDown(self):
        """Remove the temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_remove_symlinks_preserves_regular_files(self):
        """remove_existing_symlinks does not remove regular files like init-project.md."""
        # Add a symlink to verify it gets removed
        target = self.test_dir / "target.md"
        target.write_text("target")
        symlink = self.commands_dir / "some-command.md"
        symlink.symlink_to(target)

        count = remove_existing_symlinks(self.commands_dir)

        self.assertEqual(count, 1)
        self.assertTrue(self.init_project_md.exists())
        self.assertFalse(symlink.exists())


if __name__ == "__main__":
    unittest.main()

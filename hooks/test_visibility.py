#!/usr/bin/env python3
"""
Visibility tests for agents, commands, and skills.

Verifies that:
1. Symlinks in target directories are valid and resolvable
2. Files in *-available/ directories are NOT directly in scanned directories
3. init-project.md is always present in commands/

Run with: python -m unittest hooks/test_visibility.py -v
"""

import os
import unittest
from pathlib import Path


def get_project_root() -> Path:
    """Get the .claude directory root."""
    return Path(__file__).parent.parent


class TestAgentsVisibility(unittest.TestCase):
    """Tests that agents are visible to Claude."""

    def setUp(self):
        self.project_root = get_project_root()
        self.agents_dir = self.project_root / "agents"
        self.agents_available = self.project_root / "agents-available"

    def test_agents_directory_exists(self):
        """agents/ directory exists."""
        self.assertTrue(self.agents_dir.exists(), "agents/ directory should exist")

    def test_agents_symlinks_are_valid(self):
        """All symlinks in agents/ resolve to valid files."""
        if not self.agents_dir.exists():
            self.skipTest("agents/ directory does not exist")

        for item in self.agents_dir.iterdir():
            if item.is_symlink():
                target = item.resolve()
                self.assertTrue(
                    target.exists(),
                    f"Symlink {item.name} should resolve to valid file"
                )
                self.assertTrue(
                    target.suffix == ".md",
                    f"Agent {item.name} should be a .md file"
                )

    def test_agents_available_not_in_agents(self):
        """Files in agents-available/ are not directly in agents/."""
        if not self.agents_available.exists():
            self.skipTest("agents-available/ does not exist")

        # Get all actual files in agents-available (not symlinks)
        available_files = set()
        for category in self.agents_available.iterdir():
            if category.is_dir() and category.name != "local":
                for agent in category.iterdir():
                    if agent.suffix == ".md":
                        available_files.add(agent.name)

        # Check agents/ only contains symlinks, not direct copies
        if self.agents_dir.exists():
            for item in self.agents_dir.iterdir():
                if item.name in available_files:
                    self.assertTrue(
                        item.is_symlink(),
                        f"{item.name} should be a symlink, not a direct file"
                    )


class TestCommandsVisibility(unittest.TestCase):
    """Tests that commands are visible to Claude."""

    def setUp(self):
        self.project_root = get_project_root()
        self.commands_dir = self.project_root / "commands"
        self.commands_available = self.project_root / "commands-available"

    def test_commands_directory_exists(self):
        """commands/ directory exists."""
        self.assertTrue(self.commands_dir.exists(), "commands/ directory should exist")

    def test_init_project_md_exists(self):
        """init-project.md exists in commands/ (not a symlink)."""
        init_project = self.commands_dir / "init-project.md"
        self.assertTrue(init_project.exists(), "init-project.md should exist")
        self.assertFalse(
            init_project.is_symlink(),
            "init-project.md should be a regular file, not a symlink"
        )

    def test_commands_symlinks_are_valid(self):
        """All symlinks in commands/ resolve to valid files."""
        if not self.commands_dir.exists():
            self.skipTest("commands/ directory does not exist")

        for item in self.commands_dir.iterdir():
            if item.is_symlink():
                target = item.resolve()
                self.assertTrue(
                    target.exists(),
                    f"Symlink {item.name} should resolve to valid file"
                )


class TestSkillsVisibility(unittest.TestCase):
    """Tests that skills are visible to Claude."""

    def setUp(self):
        self.project_root = get_project_root()
        self.skills_dir = self.project_root / "skills"
        self.skills_available = self.project_root / "skills-available"

    def test_skills_directory_exists(self):
        """skills/ directory exists."""
        self.assertTrue(self.skills_dir.exists(), "skills/ directory should exist")

    def test_skills_symlinks_are_valid(self):
        """All symlinks in skills/ resolve to valid directories with SKILL.md."""
        if not self.skills_dir.exists():
            self.skipTest("skills/ directory does not exist")

        for item in self.skills_dir.iterdir():
            if item.is_symlink():
                target = item.resolve()
                self.assertTrue(
                    target.exists(),
                    f"Symlink {item.name} should resolve to valid target"
                )
                # Skills are directories with SKILL.md inside
                if target.is_dir():
                    skill_md = target / "SKILL.md"
                    self.assertTrue(
                        skill_md.exists(),
                        f"Skill {item.name} should contain SKILL.md"
                    )


class TestUnavailableNotVisible(unittest.TestCase):
    """Tests that *-available/ directories are not directly scanned."""

    def setUp(self):
        self.project_root = get_project_root()

    def test_available_dirs_exist(self):
        """*-available directories exist as source."""
        self.assertTrue(
            (self.project_root / "skills-available").exists(),
            "skills-available/ should exist"
        )
        self.assertTrue(
            (self.project_root / "agents-available").exists(),
            "agents-available/ should exist"
        )
        self.assertTrue(
            (self.project_root / "commands-available").exists(),
            "commands-available/ should exist"
        )

    def test_available_dirs_have_categories(self):
        """*-available directories contain category subdirectories."""
        skills_available = self.project_root / "skills-available"
        if skills_available.exists():
            categories = [d for d in skills_available.iterdir() if d.is_dir()]
            self.assertGreater(
                len(categories), 0,
                "skills-available/ should have category subdirectories"
            )


class TestSymlinkIntegrity(unittest.TestCase):
    """Tests overall symlink integrity after init-project runs."""

    def setUp(self):
        self.project_root = get_project_root()

    def test_no_broken_symlinks_in_skills(self):
        """No broken symlinks in skills/."""
        skills_dir = self.project_root / "skills"
        if not skills_dir.exists():
            self.skipTest("skills/ does not exist")

        broken = []
        for item in skills_dir.iterdir():
            if item.is_symlink() and not item.resolve().exists():
                broken.append(item.name)

        self.assertEqual(broken, [], f"Broken symlinks found: {broken}")

    def test_no_broken_symlinks_in_agents(self):
        """No broken symlinks in agents/."""
        agents_dir = self.project_root / "agents"
        if not agents_dir.exists():
            self.skipTest("agents/ does not exist")

        broken = []
        for item in agents_dir.iterdir():
            if item.is_symlink() and not item.resolve().exists():
                broken.append(item.name)

        self.assertEqual(broken, [], f"Broken symlinks found: {broken}")

    def test_no_broken_symlinks_in_commands(self):
        """No broken symlinks in commands/."""
        commands_dir = self.project_root / "commands"
        if not commands_dir.exists():
            self.skipTest("commands/ does not exist")

        broken = []
        for item in commands_dir.iterdir():
            if item.is_symlink() and not item.resolve().exists():
                broken.append(item.name)

        self.assertEqual(broken, [], f"Broken symlinks found: {broken}")


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""
Tests for CLAUDE.md generation.

Verifies that:
1. AGENTS section is generated with proper content
2. SKILLS section is generated with proper content
3. Only active categories are included

Run with: python -m unittest hooks/test_claude_md.py -v
"""

import json
import re
import unittest
from pathlib import Path


def get_project_root() -> Path:
    """Get the .claude directory root."""
    return Path(__file__).parent.parent


class TestClaudeMdStructure(unittest.TestCase):
    """Tests CLAUDE.md structure and markers."""

    def setUp(self):
        self.project_root = get_project_root()
        self.claude_md = self.project_root / "CLAUDE.md"

    def test_claude_md_exists(self):
        """CLAUDE.md exists."""
        self.assertTrue(self.claude_md.exists(), "CLAUDE.md should exist")

    def test_has_agents_markers(self):
        """CLAUDE.md has BEGIN:AGENTS and END:AGENTS markers."""
        if not self.claude_md.exists():
            self.skipTest("CLAUDE.md does not exist")

        content = self.claude_md.read_text()
        if "<!-- BEGIN:AGENTS -->" not in content:
            self.skipTest("CLAUDE.md not initialized with markers. Run /init-project first.")
        self.assertIn("<!-- END:AGENTS -->", content)

    def test_has_skills_markers(self):
        """CLAUDE.md has BEGIN:SKILLS and END:SKILLS markers."""
        if not self.claude_md.exists():
            self.skipTest("CLAUDE.md does not exist")

        content = self.claude_md.read_text()
        if "<!-- BEGIN:SKILLS -->" not in content:
            self.skipTest("CLAUDE.md not initialized with markers. Run /init-project first.")
        self.assertIn("<!-- END:SKILLS -->", content)


class TestAgentsSectionGenerated(unittest.TestCase):
    """Tests that AGENTS section contains expected content."""

    def setUp(self):
        self.project_root = get_project_root()
        self.claude_md = self.project_root / "CLAUDE.md"
        self.agents_dir = self.project_root / "agents"

    def get_agents_section(self) -> str:
        """Extract content between AGENTS markers."""
        if not self.claude_md.exists():
            return ""
        content = self.claude_md.read_text()
        match = re.search(
            r"<!-- BEGIN:AGENTS -->(.*?)<!-- END:AGENTS -->",
            content,
            re.DOTALL
        )
        return match.group(1) if match else ""

    def test_agents_section_not_empty(self):
        """AGENTS section contains content (not just markers)."""
        section = self.get_agents_section()
        if not section:
            self.skipTest("CLAUDE.md not initialized with markers. Run /init-project first.")
        # Remove whitespace and check if there's actual content
        content = section.strip()
        # Should have more than just the auto-generated comment
        self.assertGreater(
            len(content), 50,
            "AGENTS section should contain agent instructions"
        )

    def test_active_agents_mentioned(self):
        """Active agents (symlinked) are mentioned in AGENTS section."""
        if not self.agents_dir.exists():
            self.skipTest("agents/ does not exist")

        section = self.get_agents_section()
        if not section:
            self.skipTest("CLAUDE.md not initialized with markers. Run /init-project first.")

        # Get list of active agents
        active_agents = []
        for item in self.agents_dir.iterdir():
            if item.is_symlink() and item.suffix == ".md":
                agent_name = item.stem
                active_agents.append(agent_name)

        # At least some active agents should be mentioned
        mentioned = 0
        for agent in active_agents:
            if agent in section:
                mentioned += 1

        if active_agents:
            self.assertGreater(
                mentioned, 0,
                f"At least one active agent should be mentioned. Active: {active_agents}"
            )


class TestSkillsSectionGenerated(unittest.TestCase):
    """Tests that SKILLS section contains expected content."""

    def setUp(self):
        self.project_root = get_project_root()
        self.claude_md = self.project_root / "CLAUDE.md"
        self.skills_dir = self.project_root / "skills"

    def get_skills_section(self) -> str:
        """Extract content between SKILLS markers."""
        if not self.claude_md.exists():
            return ""
        content = self.claude_md.read_text()
        match = re.search(
            r"<!-- BEGIN:SKILLS -->(.*?)<!-- END:SKILLS -->",
            content,
            re.DOTALL
        )
        return match.group(1) if match else ""

    def test_skills_section_not_empty(self):
        """SKILLS section contains content (not just markers)."""
        section = self.get_skills_section()
        if not section:
            self.skipTest("CLAUDE.md not initialized with markers. Run /init-project first.")
        content = section.strip()
        self.assertGreater(
            len(content), 50,
            "SKILLS section should contain skill instructions"
        )

    def test_active_skills_mentioned(self):
        """Active skills (symlinked) are mentioned in SKILLS section."""
        if not self.skills_dir.exists():
            self.skipTest("skills/ does not exist")

        section = self.get_skills_section()
        if not section:
            self.skipTest("CLAUDE.md not initialized with markers. Run /init-project first.")

        # Get list of active skills
        active_skills = []
        for item in self.skills_dir.iterdir():
            if item.is_symlink():
                skill_name = item.name
                active_skills.append(skill_name)

        # At least some active skills should be mentioned
        mentioned = 0
        for skill in active_skills:
            if skill in section:
                mentioned += 1

        if active_skills:
            self.assertGreater(
                mentioned, 0,
                f"At least one active skill should be mentioned. Active: {active_skills[:5]}..."
            )


class TestOnlyActiveCategoriesIncluded(unittest.TestCase):
    """Tests that only active categories are included in CLAUDE.md."""

    def setUp(self):
        self.project_root = get_project_root()
        self.claude_md = self.project_root / "CLAUDE.md"
        self.project_json = self.project_root / ".claude" / "project.json"

    def get_active_categories(self) -> list:
        """Get categories from .claude/project.json."""
        if not self.project_json.exists():
            return []
        with open(self.project_json) as f:
            config = json.load(f)
        return config.get("categories", [])

    def test_inactive_category_agents_not_included(self):
        """Agents from inactive categories are not in CLAUDE.md AGENTS section."""
        if not self.claude_md.exists():
            self.skipTest("CLAUDE.md does not exist")

        active_categories = self.get_active_categories()
        if not active_categories:
            self.skipTest("No project.json or no categories defined")

        content = self.claude_md.read_text()

        # Check if CLAUDE.md has markers (initialized)
        if "<!-- BEGIN:AGENTS -->" not in content:
            self.skipTest("CLAUDE.md not initialized with markers. Run /init-project first.")

        # Extract only the AGENTS section for checking
        match = re.search(
            r"<!-- BEGIN:AGENTS -->(.*?)<!-- END:AGENTS -->",
            content,
            re.DOTALL
        )
        agents_section = match.group(1) if match else ""

        # If 'laravel' is not active, laravel-specific agents shouldn't appear in AGENTS section
        if "laravel" not in active_categories:
            self.assertNotIn(
                "laravel-developer",
                agents_section,
                "laravel-developer should not appear in AGENTS section when laravel category is inactive"
            )

        # If 'vue' is not active, vue-specific agents shouldn't appear in AGENTS section
        if "vue" not in active_categories:
            self.assertNotIn(
                "vuejs-developer",
                agents_section,
                "vuejs-developer should not appear in AGENTS section when vue category is inactive"
            )


class TestClaudeMdRegeneration(unittest.TestCase):
    """Tests that CLAUDE.md can be regenerated correctly."""

    def setUp(self):
        self.project_root = get_project_root()
        self.claude_md = self.project_root / "CLAUDE.md"

    def test_regeneration_comment_present(self):
        """CLAUDE.md contains regeneration instructions (when initialized)."""
        if not self.claude_md.exists():
            self.skipTest("CLAUDE.md does not exist")

        content = self.claude_md.read_text()

        # Check if CLAUDE.md has markers (initialized)
        if "<!-- BEGIN:AGENTS -->" not in content:
            self.skipTest("CLAUDE.md not initialized with markers. Run /init-project first.")

        self.assertIn(
            "/init-project",
            content,
            "CLAUDE.md should mention /init-project for regeneration"
        )


if __name__ == "__main__":
    unittest.main()

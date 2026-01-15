"""Tests to verify agents, commands, and skills are visible to Claude."""

import json
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import get_active_agents, get_active_skills, get_active_commands


class TestAgentsVisibility:
    """Tests that agents in agents/ are properly configured for Claude visibility."""

    def test_agents_directory_exists(self, project_root):
        """agents/ directory should exist."""
        agents_dir = project_root / "agents"
        assert agents_dir.exists(), "agents/ directory should exist"

    def test_all_agent_symlinks_resolve(self, project_root):
        """All symlinks in agents/ should resolve to valid files."""
        agents_dir = project_root / "agents"
        if not agents_dir.exists():
            pytest.skip("agents/ does not exist")

        broken = []
        for item in agents_dir.iterdir():
            if item.is_symlink():
                if not item.resolve().exists():
                    broken.append(item.name)
                else:
                    assert item.resolve().suffix == ".md", \
                        f"Agent {item.name} should be .md file"

        assert not broken, f"Broken symlinks: {broken}"

    def test_agents_are_markdown_files(self, project_root):
        """All agents should be .md files."""
        agents_dir = project_root / "agents"
        if not agents_dir.exists():
            pytest.skip("agents/ does not exist")

        for item in agents_dir.iterdir():
            if item.is_symlink():
                assert item.suffix == ".md", f"Agent {item.name} should have .md extension"

    def test_agents_match_project_categories(self, project_root):
        """Active agents should match .claude/project.json categories."""
        project_json = project_root / ".claude" / "project.json"
        if not project_json.exists():
            pytest.skip("No .claude/project.json")

        config = json.loads(project_json.read_text())
        categories = set(config.get("categories", []))
        categories.add("local")  # local is always included

        agents_dir = project_root / "agents"
        for item in agents_dir.iterdir():
            if item.is_symlink():
                target = item.resolve()
                target_category = target.parent.name
                assert target_category in categories, \
                    f"Agent {item.name} from category '{target_category}' not in project categories"


class TestCommandsVisibility:
    """Tests that commands in commands/ are properly configured."""

    def test_commands_directory_exists(self, project_root):
        """commands/ directory should exist."""
        commands_dir = project_root / "commands"
        assert commands_dir.exists(), "commands/ directory should exist"

    def test_init_project_command_exists(self, project_root):
        """init-project.md should exist (not a symlink)."""
        init_project = project_root / "commands" / "init-project.md"
        assert init_project.exists(), "init-project.md should exist"
        assert not init_project.is_symlink(), "init-project.md should be a regular file"

    def test_command_symlinks_resolve(self, project_root):
        """All command symlinks should resolve."""
        commands_dir = project_root / "commands"
        if not commands_dir.exists():
            pytest.skip("commands/ does not exist")

        broken = []
        for item in commands_dir.iterdir():
            if item.is_symlink():
                if not item.resolve().exists():
                    broken.append(item.name)

        assert not broken, f"Broken command symlinks: {broken}"


class TestSkillsVisibility:
    """Tests that skills in skills/ are properly configured for Claude visibility."""

    def test_skills_directory_exists(self, project_root):
        """skills/ directory should exist."""
        skills_dir = project_root / "skills"
        assert skills_dir.exists(), "skills/ directory should exist"

    def test_skill_symlinks_have_skill_md(self, project_root):
        """Skill symlinks should point to directories with SKILL.md."""
        skills_dir = project_root / "skills"
        if not skills_dir.exists():
            pytest.skip("skills/ does not exist")

        for item in skills_dir.iterdir():
            if item.is_symlink():
                target = item.resolve()
                if target.is_dir():
                    skill_md = target / "SKILL.md"
                    assert skill_md.exists(), \
                        f"Skill {item.name} should contain SKILL.md"

    def test_skills_match_project_categories(self, project_root):
        """Active skills should match .claude/project.json categories."""
        project_json = project_root / ".claude" / "project.json"
        if not project_json.exists():
            pytest.skip("No .claude/project.json")

        config = json.loads(project_json.read_text())
        categories = set(config.get("categories", []))
        categories.add("local")

        skills_dir = project_root / "skills"
        for item in skills_dir.iterdir():
            if item.is_symlink():
                target = item.resolve()
                target_category = target.parent.name
                assert target_category in categories, \
                    f"Skill {item.name} from category '{target_category}' not in project categories"


class TestClaudeMdVisibility:
    """Tests that CLAUDE.md contains proper agent/skill instructions."""

    def test_claude_md_exists(self, project_root):
        """CLAUDE.md should exist."""
        claude_md = project_root / "CLAUDE.md"
        assert claude_md.exists(), "CLAUDE.md should exist"

    def test_agents_section_populated(self, project_root):
        """AGENTS section in CLAUDE.md should contain instructions."""
        claude_md = project_root / "CLAUDE.md"
        if not claude_md.exists():
            pytest.skip("No CLAUDE.md")

        content = claude_md.read_text()

        if "<!-- BEGIN:AGENTS -->" not in content:
            pytest.skip("CLAUDE.md not initialized with markers")

        match = re.search(
            r"<!-- BEGIN:AGENTS -->(.*?)<!-- END:AGENTS -->",
            content,
            re.DOTALL
        )

        assert match, "Should have AGENTS markers"
        section = match.group(1).strip()
        assert len(section) > 50, "AGENTS section should contain content"

    def test_skills_section_populated(self, project_root):
        """SKILLS section in CLAUDE.md should contain instructions."""
        claude_md = project_root / "CLAUDE.md"
        if not claude_md.exists():
            pytest.skip("No CLAUDE.md")

        content = claude_md.read_text()

        if "<!-- BEGIN:SKILLS -->" not in content:
            pytest.skip("CLAUDE.md not initialized with markers")

        match = re.search(
            r"<!-- BEGIN:SKILLS -->(.*?)<!-- END:SKILLS -->",
            content,
            re.DOTALL
        )

        assert match, "Should have SKILLS markers"
        section = match.group(1).strip()
        assert len(section) > 50, "SKILLS section should contain content"

    def test_active_agents_in_claude_md(self, project_root):
        """Active agents should be mentioned in CLAUDE.md."""
        agents_dir = project_root / "agents"
        claude_md = project_root / "CLAUDE.md"

        if not agents_dir.exists() or not claude_md.exists():
            pytest.skip("Missing required files")

        content = claude_md.read_text()
        active = get_active_agents(project_root)

        if not active:
            pytest.skip("No active agents")

        # Check if at least some are mentioned
        mentioned = sum(1 for a in active if a in content)

        assert mentioned > 0, \
            f"At least one active agent should be in CLAUDE.md. Active: {active}"

    def test_active_skills_in_claude_md(self, project_root):
        """Active skills should be mentioned in CLAUDE.md."""
        skills_dir = project_root / "skills"
        claude_md = project_root / "CLAUDE.md"

        if not skills_dir.exists() or not claude_md.exists():
            pytest.skip("Missing required files")

        content = claude_md.read_text()
        active = get_active_skills(project_root)

        if not active:
            pytest.skip("No active skills")

        # Check if at least some are mentioned
        mentioned = sum(1 for s in active if s in content)

        assert mentioned > 0, \
            f"At least one active skill should be in CLAUDE.md. Active: {list(active)[:5]}"


class TestSymlinkIntegrity:
    """Tests overall symlink integrity."""

    def test_no_broken_symlinks_in_agents(self, project_root):
        """No broken symlinks in agents/."""
        agents_dir = project_root / "agents"
        if not agents_dir.exists():
            pytest.skip("agents/ does not exist")

        broken = [
            item.name for item in agents_dir.iterdir()
            if item.is_symlink() and not item.resolve().exists()
        ]

        assert broken == [], f"Broken symlinks: {broken}"

    def test_no_broken_symlinks_in_skills(self, project_root):
        """No broken symlinks in skills/."""
        skills_dir = project_root / "skills"
        if not skills_dir.exists():
            pytest.skip("skills/ does not exist")

        broken = [
            item.name for item in skills_dir.iterdir()
            if item.is_symlink() and not item.resolve().exists()
        ]

        assert broken == [], f"Broken symlinks: {broken}"

    def test_no_broken_symlinks_in_commands(self, project_root):
        """No broken symlinks in commands/."""
        commands_dir = project_root / "commands"
        if not commands_dir.exists():
            pytest.skip("commands/ does not exist")

        broken = [
            item.name for item in commands_dir.iterdir()
            if item.is_symlink() and not item.resolve().exists()
        ]

        assert broken == [], f"Broken symlinks: {broken}"

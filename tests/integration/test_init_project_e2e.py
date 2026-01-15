"""End-to-end integration tests for /init-project command."""

import json
import subprocess
import tempfile
import shutil
from pathlib import Path

import pytest


class TestInitProjectE2E:
    """End-to-end tests for init-project execution."""

    @pytest.fixture
    def full_project_copy(self, project_root):
        """Create a full copy of the project for E2E testing."""
        temp_dir = Path(tempfile.mkdtemp())

        # Copy essential directories
        for dir_name in ["agents-available", "skills-available", "commands-available"]:
            src = project_root / dir_name
            if src.exists():
                shutil.copytree(src, temp_dir / dir_name)

        # Copy essential files
        for file_name in ["AGENTS.md", "SKILLS.md", "CLAUDE.template.md"]:
            src = project_root / file_name
            if src.exists():
                shutil.copy(src, temp_dir / file_name)

        # Copy hooks
        hooks_src = project_root / "hooks"
        if hooks_src.exists():
            shutil.copytree(hooks_src, temp_dir / "hooks")

        # Create target directories
        (temp_dir / "agents").mkdir(exist_ok=True)
        (temp_dir / "skills").mkdir(exist_ok=True)
        (temp_dir / "commands").mkdir(exist_ok=True)

        # Create .claude directory for project.json
        (temp_dir / ".claude").mkdir(exist_ok=True)

        yield temp_dir

        shutil.rmtree(temp_dir)

    def test_init_creates_symlinks_for_dev_category(self, full_project_copy):
        """Init creates symlinks for dev category agents and skills."""
        config = {
            "name": "test",
            "categories": ["dev"],
            "exclude": []
        }
        (full_project_copy / ".claude" / "project.json").write_text(json.dumps(config))

        result = subprocess.run(
            ["python3", "hooks/init-project.py"],
            cwd=full_project_copy,
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Failed: {result.stderr}"

        agents_dir = full_project_copy / "agents"
        skills_dir = full_project_copy / "skills"

        # Should have dev category agents
        agent_symlinks = [a for a in agents_dir.iterdir() if a.is_symlink()]
        assert len(agent_symlinks) > 0, "Should have agent symlinks"

        # Verify symlinks are valid
        for agent in agent_symlinks:
            assert agent.resolve().exists(), f"Symlink {agent} should resolve"

    def test_init_updates_claude_md(self, full_project_copy):
        """Init updates CLAUDE.md with agent/skill instructions."""
        config = {
            "name": "test",
            "categories": ["dev"],
            "exclude": []
        }
        (full_project_copy / ".claude" / "project.json").write_text(json.dumps(config))

        subprocess.run(
            ["python3", "hooks/init-project.py"],
            cwd=full_project_copy,
            capture_output=True
        )

        claude_md = full_project_copy / "CLAUDE.md"
        assert claude_md.exists(), "CLAUDE.md should be created"

        content = claude_md.read_text()
        assert "<!-- BEGIN:AGENTS -->" in content
        assert "<!-- END:AGENTS -->" in content
        assert "<!-- BEGIN:SKILLS -->" in content
        assert "<!-- END:SKILLS -->" in content

    def test_init_respects_exclude_list(self, full_project_copy):
        """Init respects exclude list."""
        config = {
            "name": "test",
            "categories": ["dev"],
            "exclude": ["agents/test-generator"]
        }
        (full_project_copy / ".claude" / "project.json").write_text(json.dumps(config))

        subprocess.run(
            ["python3", "hooks/init-project.py"],
            cwd=full_project_copy,
            capture_output=True
        )

        agents_dir = full_project_copy / "agents"
        agent_names = [a.stem for a in agents_dir.iterdir() if a.is_symlink()]
        assert "test-generator" not in agent_names

    def test_init_multiple_categories(self, full_project_copy):
        """Init handles multiple categories correctly."""
        config = {
            "name": "test",
            "categories": ["dev", "docs", "claude"],
            "exclude": []
        }
        (full_project_copy / ".claude" / "project.json").write_text(json.dumps(config))

        result = subprocess.run(
            ["python3", "hooks/init-project.py"],
            cwd=full_project_copy,
            capture_output=True,
            text=True
        )

        assert result.returncode == 0

        # Should have symlinks from all categories
        agents_dir = full_project_copy / "agents"
        skills_dir = full_project_copy / "skills"

        agent_count = len([a for a in agents_dir.iterdir() if a.is_symlink()])
        skill_count = len([s for s in skills_dir.iterdir() if s.is_symlink()])

        assert agent_count > 0, "Should have agents from multiple categories"
        assert skill_count > 0, "Should have skills from multiple categories"

    def test_init_output_reports_counts(self, full_project_copy):
        """Init output reports skill/agent/command counts."""
        config = {
            "name": "test",
            "categories": ["dev"],
            "exclude": []
        }
        (full_project_copy / ".claude" / "project.json").write_text(json.dumps(config))

        result = subprocess.run(
            ["python3", "hooks/init-project.py"],
            cwd=full_project_copy,
            capture_output=True,
            text=True
        )

        # Check output contains count reports
        assert "skills loaded" in result.stdout.lower() or "skill" in result.stdout.lower()
        assert "agents loaded" in result.stdout.lower() or "agent" in result.stdout.lower()


class TestInitProjectWithRealProject:
    """Tests using the actual project configuration."""

    def test_current_project_has_valid_symlinks(self, project_root):
        """Current project should have valid symlinks."""
        agents_dir = project_root / "agents"
        if not agents_dir.exists():
            pytest.skip("agents/ does not exist")

        broken = []
        for item in agents_dir.iterdir():
            if item.is_symlink():
                if not item.resolve().exists():
                    broken.append(item.name)

        assert broken == [], f"Broken symlinks: {broken}"

    def test_current_project_json_valid(self, project_root):
        """.claude/project.json should be valid if it exists."""
        project_json = project_root / ".claude" / "project.json"
        if not project_json.exists():
            pytest.skip(".claude/project.json does not exist")

        config = json.loads(project_json.read_text())
        assert "categories" in config, ".claude/project.json should have categories"
        assert isinstance(config["categories"], list), "categories should be a list"

"""Unit tests for project.json configuration loading."""

import json
import tempfile
import shutil
from pathlib import Path

import pytest

# Import from hooks/init-project.py using importlib
import importlib.util

spec = importlib.util.spec_from_file_location(
    "init_project",
    Path(__file__).parent.parent.parent / "hooks" / "init-project.py"
)
init_project = importlib.util.module_from_spec(spec)
spec.loader.exec_module(init_project)


class TestProjectJsonCreation:
    """Tests for project.json creation and loading."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_missing_project_json_exits(self, temp_dir):
        """Missing project.json calls sys.exit(1)."""
        with pytest.raises(SystemExit) as exc_info:
            init_project.load_project_config(temp_dir)
        assert exc_info.value.code == 1

    def test_valid_project_json_loads(self, temp_dir):
        """Valid project.json loads correctly."""
        config = {
            "name": "test-project",
            "categories": ["dev", "php"],
            "exclude": [],
            "description": "Test project"
        }
        project_json = temp_dir / "project.json"
        project_json.write_text(json.dumps(config))

        result = init_project.load_project_config(temp_dir)

        assert result["name"] == "test-project"
        assert result["categories"] == ["dev", "php"]

    def test_invalid_json_raises_error(self, temp_dir):
        """Invalid JSON raises JSONDecodeError."""
        project_json = temp_dir / "project.json"
        project_json.write_text("{ invalid json }")

        with pytest.raises(json.JSONDecodeError):
            init_project.load_project_config(temp_dir)

    def test_empty_categories_defaults(self, temp_dir):
        """Project config with missing categories returns config as-is."""
        config = {"name": "test"}
        project_json = temp_dir / "project.json"
        project_json.write_text(json.dumps(config))

        result = init_project.load_project_config(temp_dir)
        assert result.get("name") == "test"


class TestSymlinkOperations:
    """Tests for symlink creation and removal."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory with symlink structure."""
        temp_dir = Path(tempfile.mkdtemp())
        (temp_dir / "target").mkdir()
        (temp_dir / "source" / "dev").mkdir(parents=True)
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_remove_symlinks(self, temp_dir):
        """Removes symlinks and returns count."""
        target_dir = temp_dir / "target"
        # Create a target file and symlink
        target_file = temp_dir / "original.txt"
        target_file.write_text("content")
        link = target_dir / "link.txt"
        link.symlink_to(target_file)

        count = init_project.remove_existing_symlinks(target_dir)

        assert count == 1
        assert not link.exists()
        assert target_file.exists()

    def test_keeps_regular_files(self, temp_dir):
        """Keeps regular files, returns 0."""
        target_dir = temp_dir / "target"
        regular_file = target_dir / "file.txt"
        regular_file.write_text("content")

        count = init_project.remove_existing_symlinks(target_dir)

        assert count == 0
        assert regular_file.exists()

    def test_flat_symlink_creation(self, temp_dir):
        """Creates symlinks for flat .md files."""
        source_dir = temp_dir / "source"
        target_dir = temp_dir / "target"
        dev_dir = source_dir / "dev"
        (dev_dir / "test-agent.md").write_text("# Agent")

        count = init_project.create_symlinks_from_available(
            source_dir, target_dir, ["dev"], []
        )

        assert count == 1
        link = target_dir / "test-agent.md"
        assert link.is_symlink()

    def test_nested_symlink_creation(self, temp_dir):
        """Creates symlinks for nested SKILL.md directories."""
        source_dir = temp_dir / "source"
        target_dir = temp_dir / "target"
        dev_dir = source_dir / "dev"
        skill_dir = dev_dir / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# Skill")

        count = init_project.create_symlinks_from_available(
            source_dir, target_dir, ["dev"], []
        )

        assert count == 1
        link = target_dir / "my-skill"
        assert link.is_symlink()

    def test_skips_excluded_items(self, temp_dir):
        """Skips items in excludes list."""
        source_dir = temp_dir / "source"
        target_dir = temp_dir / "target"
        dev_dir = source_dir / "dev"
        (dev_dir / "include-me.md").write_text("# Include")
        (dev_dir / "exclude-me.md").write_text("# Exclude")

        # Note: exclude format is "type/name" without extension
        count = init_project.create_symlinks_from_available(
            source_dir, target_dir, ["dev"], ["source/exclude-me"]
        )

        assert count == 1
        assert (target_dir / "include-me.md").is_symlink()
        assert not (target_dir / "exclude-me.md").exists()

    def test_skips_unlisted_category(self, temp_dir):
        """Skips categories not in the list."""
        source_dir = temp_dir / "source"
        target_dir = temp_dir / "target"
        dev_dir = source_dir / "dev"
        (dev_dir / "dev-item.md").write_text("# Dev")

        php_dir = source_dir / "php"
        php_dir.mkdir()
        (php_dir / "php-item.md").write_text("# PHP")

        count = init_project.create_symlinks_from_available(
            source_dir, target_dir, ["dev"], []
        )

        assert count == 1
        assert (target_dir / "dev-item.md").is_symlink()
        assert not (target_dir / "php-item.md").exists()


class TestClaudeMdUpdate:
    """Tests for CLAUDE.md generation."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory with AGENTS.md and SKILLS.md."""
        temp_dir = Path(tempfile.mkdtemp())
        (temp_dir / "AGENTS.md").write_text("""# Agents

## Category: dev

### debugging-assistant
Use when debugging.

### test-generator
Use when generating tests.

## Category: php

### php-specialist
Use for PHP code.
""")
        (temp_dir / "SKILLS.md").write_text("""# Skills

## Category: dev

### tdd
Use for TDD.

## Category: php

### php-docstring
Use for PHP docstrings.
""")
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_extracts_matching_categories(self, temp_dir):
        """Extracts sections from matching categories."""
        result = init_project.extract_sections(
            temp_dir / "AGENTS.md", ["dev"], "agents"
        )

        assert "debugging-assistant" in result
        assert "test-generator" in result
        assert "php-specialist" not in result

    def test_creates_claude_md_with_markers(self, temp_dir):
        """Creates CLAUDE.md with proper markers."""
        init_project.update_claude_md(temp_dir, ["dev"])

        claude_md = temp_dir / "CLAUDE.md"
        assert claude_md.exists()
        content = claude_md.read_text()
        assert "<!-- BEGIN:AGENTS -->" in content
        assert "<!-- END:AGENTS -->" in content
        assert "<!-- BEGIN:SKILLS -->" in content
        assert "<!-- END:SKILLS -->" in content

    def test_includes_matching_content(self, temp_dir):
        """CLAUDE.md contains content from matching categories."""
        init_project.update_claude_md(temp_dir, ["dev"])

        claude_md = temp_dir / "CLAUDE.md"
        content = claude_md.read_text()
        assert "debugging-assistant" in content
        assert "tdd" in content
        assert "php-specialist" not in content

    def test_updates_existing_claude_md(self, temp_dir):
        """Updates content between markers in existing CLAUDE.md."""
        claude_md = temp_dir / "CLAUDE.md"
        claude_md.write_text("""# CLAUDE.md

Some intro text.

<!-- BEGIN:AGENTS -->
old agent content
<!-- END:AGENTS -->

Middle text.

<!-- BEGIN:SKILLS -->
old skill content
<!-- END:SKILLS -->

Footer text.
""")

        init_project.update_claude_md(temp_dir, ["dev"])

        content = claude_md.read_text()
        assert "debugging-assistant" in content
        assert "tdd" in content
        assert "old agent content" not in content
        assert "old skill content" not in content
        assert "Some intro text" in content
        assert "Footer text" in content

#!/usr/bin/env python3
"""
Initialize project skills and agents based on .claude/project.json configuration.

Usage:
    python init-project.py

This script:
1. Reads .claude/project.json (required - created by /init-project command)
2. Creates symlinks for matching skills, agents, and commands
3. Updates CLAUDE.md with relevant instructions

Note: This script is invoked by the /init-project Claude command.
If .claude/project.json doesn't exist, run /init-project to create it interactively.
"""

import json
import os
import re
import sys
from pathlib import Path


def get_project_root() -> Path:
    """Get the .claude directory root."""
    # Script is in hooks/, so parent.parent gets us to .claude root
    return Path(__file__).parent.parent


def load_project_config(project_root: Path) -> dict:
    """Load project configuration from project.json.

    Checks two locations to support both contexts:
    - Runtime (.claude/hooks/): project.json directly in project_root
    - Development (root/hooks/): .claude/project.json under project_root
    """
    # Try direct path first (runtime context)
    project_json = project_root / "project.json"
    if not project_json.exists():
        # Try .claude subdirectory (development context)
        project_json = project_root / ".claude" / "project.json"

    if not project_json.exists():
        print("Error: project.json not found.")
        print("Run /init-project to create one interactively.")
        sys.exit(1)

    with open(project_json, "r") as f:
        return json.load(f)


def remove_existing_symlinks(directory: Path) -> int:
    """Remove existing symlinks in a directory (not in subdirectories)."""
    count = 0
    for item in directory.iterdir():
        if item.is_symlink():
            item.unlink()
            count += 1
    return count


def create_symlinks_from_available(source_dir: Path, target_dir: Path, categories: list, excludes: list) -> int:
    """Create symlinks from source *-available directory to target directory.

    Args:
        source_dir: The source directory (e.g., skills-available/)
        target_dir: The target directory (e.g., skills/)
        categories: List of category subdirectories to include
        excludes: List of items to exclude (format: "skills/item-name")

    Handles two structures:
    - Flat: category/item.md (agents, commands)
    - Nested: category/item-name/SKILL.md (skills)
    """
    count = 0
    source_name = source_dir.name.replace("-available", "")  # e.g., "skills"

    for category in categories:
        category_dir = source_dir / category
        if not category_dir.exists():
            continue

        for item in category_dir.iterdir():
            # Case 1: Flat structure - .md files directly in category
            if item.suffix == ".md" and item.is_file():
                item_name_without_ext = item.stem
                relative_path = f"{source_name}/{item_name_without_ext}"
                if relative_path in excludes:
                    continue

                link_path = target_dir / item.name
                if link_path.exists():
                    if link_path.is_symlink():
                        link_path.unlink()
                    else:
                        print(f"Warning: {link_path} exists and is not a symlink, skipping")
                        continue

                relative_target = Path("..") / source_dir.name / category / item.name
                link_path.symlink_to(relative_target)
                count += 1

            # Case 2: Nested structure - subdirectory with SKILL.md (Claude Code skills format)
            elif item.is_dir():
                skill_file = item / "SKILL.md"
                if skill_file.exists():
                    skill_name = item.name
                    relative_path = f"{source_name}/{skill_name}"
                    if relative_path in excludes:
                        continue

                    # Symlink the whole skill directory
                    link_path = target_dir / skill_name
                    if link_path.exists():
                        if link_path.is_symlink():
                            link_path.unlink()
                        else:
                            print(f"Warning: {link_path} exists and is not a symlink, skipping")
                            continue

                    relative_target = Path("..") / source_dir.name / category / skill_name
                    link_path.symlink_to(relative_target)
                    count += 1

    # Also include local/ folder contents
    local_dir = source_dir / "local"
    if local_dir.exists():
        for item in local_dir.iterdir():
            # Flat .md files
            if item.suffix == ".md" and item.is_file():
                link_path = target_dir / item.name
                if not link_path.exists():
                    relative_target = Path("..") / source_dir.name / "local" / item.name
                    link_path.symlink_to(relative_target)
                    count += 1
            # Nested skill directories
            elif item.is_dir() and (item / "SKILL.md").exists():
                link_path = target_dir / item.name
                if not link_path.exists():
                    relative_target = Path("..") / source_dir.name / "local" / item.name
                    link_path.symlink_to(relative_target)
                    count += 1

    return count


def extract_sections(md_file: Path, categories: list, section_type: str) -> str:
    """Extract sections from AGENTS.md or SKILLS.md based on categories."""
    if not md_file.exists():
        return ""

    with open(md_file, "r") as f:
        content = f.read()

    extracted = []
    current_category = None
    current_section = None
    section_content = []
    in_target_category = False

    for line in content.split("\n"):
        # Check for category header
        category_match = re.match(r"^## Category: (\w+)", line)
        if category_match:
            # Save previous section if it was in a target category
            if in_target_category and current_section and section_content:
                extracted.append(f"### {current_section}")
                extracted.extend(section_content)
                extracted.append("")

            current_category = category_match.group(1)
            in_target_category = current_category in categories
            current_section = None
            section_content = []
            continue

        # Check for item header (### name)
        item_match = re.match(r"^### (\S+)", line)
        if item_match:
            # Save previous section if it was in a target category
            if in_target_category and current_section and section_content:
                extracted.append(f"### {current_section}")
                extracted.extend(section_content)
                extracted.append("")

            current_section = item_match.group(1)
            section_content = []
            continue

        # Collect content for current section
        if current_section is not None:
            section_content.append(line)

    # Don't forget the last section
    if in_target_category and current_section and section_content:
        extracted.append(f"### {current_section}")
        extracted.extend(section_content)
        extracted.append("")

    return "\n".join(extracted).strip()


def update_claude_md(project_root: Path, categories: list) -> None:
    """Update CLAUDE.md with agent and skill instructions.

    Strategy:
    - If CLAUDE.md doesn't exist: create minimal file with guidelines section
    - If CLAUDE.md exists without markers: append guidelines section at the end
    - If CLAUDE.md exists with markers: update content between markers
    """
    claude_md = project_root / "CLAUDE.md"

    # Extract agent instructions
    agents_md = project_root / "AGENTS.md"
    agent_instructions = extract_sections(agents_md, categories, "agents")

    # Extract skill instructions
    skills_md = project_root / "SKILLS.md"
    skill_instructions = extract_sections(skills_md, categories, "skills")

    # Build the auto-generated sections
    agent_section = f"""<!-- BEGIN:AGENTS -->
<!-- Auto-generated agent instructions - DO NOT EDIT between markers -->
<!-- Run /init-project to regenerate -->

{agent_instructions}

<!-- END:AGENTS -->"""

    skill_section = f"""<!-- BEGIN:SKILLS -->
<!-- Auto-generated skill instructions - DO NOT EDIT between markers -->
<!-- Run /init-project to regenerate -->

{skill_instructions}

<!-- END:SKILLS -->"""

    guidelines_section = f"""
## Agent and Skill Guidelines

{agent_section}

{skill_section}
"""

    if not claude_md.exists():
        # Create minimal CLAUDE.md with guidelines section
        content = f"# CLAUDE.md\n{guidelines_section}"
    else:
        with open(claude_md, "r") as f:
            content = f.read()

        has_agent_markers = "<!-- BEGIN:AGENTS -->" in content and "<!-- END:AGENTS -->" in content
        has_skill_markers = "<!-- BEGIN:SKILLS -->" in content and "<!-- END:SKILLS -->" in content

        if has_agent_markers and has_skill_markers:
            # Update existing markers
            content = re.sub(
                r"<!-- BEGIN:AGENTS -->.*?<!-- END:AGENTS -->",
                agent_section,
                content,
                flags=re.DOTALL
            )
            content = re.sub(
                r"<!-- BEGIN:SKILLS -->.*?<!-- END:SKILLS -->",
                skill_section,
                content,
                flags=re.DOTALL
            )
        else:
            # Append guidelines section at the end
            content = content.rstrip() + "\n" + guidelines_section

    with open(claude_md, "w") as f:
        f.write(content)


def main():
    """Main function."""
    project_root = get_project_root()

    # Load configuration from project.json
    config = load_project_config(project_root)
    categories = config.get("categories", [])
    excludes = config.get("exclude", [])

    print(f"Initializing project: {config.get('name', 'unnamed')}")
    print(f"Categories: {', '.join(categories)}")

    if excludes:
        print(f"Excludes: {', '.join(excludes)}")

    # Source directories (NOT scanned by Claude)
    skills_available = project_root / "skills-available"
    agents_available = project_root / "agents-available"
    commands_available = project_root / "commands-available"

    # Target directories (scanned by Claude - symlinks only)
    skills_dir = project_root / "skills"
    agents_dir = project_root / "agents"
    commands_dir = project_root / "commands"

    # Remove existing symlinks from target directories
    removed = 0
    removed += remove_existing_symlinks(skills_dir)
    removed += remove_existing_symlinks(agents_dir)
    removed += remove_existing_symlinks(commands_dir)

    if removed > 0:
        print(f"Removed {removed} existing symlinks")

    # Create new symlinks from source to target
    skills_count = create_symlinks_from_available(skills_available, skills_dir, categories, excludes)
    agents_count = create_symlinks_from_available(agents_available, agents_dir, categories, excludes)
    commands_count = create_symlinks_from_available(commands_available, commands_dir, categories, excludes)

    # Note: init-project.md stays in commands/ as a regular file (not a symlink)
    # It cannot create itself, so it must always be present

    print(f"✓ {skills_count} skills loaded")
    print(f"✓ {agents_count} agents loaded")
    print(f"✓ {commands_count} commands loaded")

    # Update CLAUDE.md
    update_claude_md(project_root, categories)
    print("✓ CLAUDE.md updated")

    print("\nDone!")


if __name__ == "__main__":
    main()

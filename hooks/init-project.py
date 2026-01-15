#!/usr/bin/env python3
"""
Initialize project skills and agents based on project.json configuration.

Usage:
    python init-project.py

This script:
1. Reads project.json (required - created by /init-project command)
2. Creates symlinks for matching skills, agents, and commands
3. Updates CLAUDE.md with relevant instructions

Note: This script is invoked by the /init-project Claude command.
If project.json doesn't exist, run /init-project to create it interactively.
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
    """Load project configuration from project.json."""
    project_json = project_root / "project.json"
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


def create_symlinks(source_dir: Path, categories: list, excludes: list) -> int:
    """Create symlinks from category subdirectories to the parent directory."""
    count = 0

    for category in categories:
        category_dir = source_dir / category
        if not category_dir.exists():
            continue

        for item in category_dir.iterdir():
            if item.suffix == ".md" and item.is_file():
                # Check if excluded
                relative_path = f"{source_dir.name}/{item.name}"
                if relative_path in excludes:
                    continue

                # Create symlink
                link_path = source_dir / item.name
                if link_path.exists():
                    if link_path.is_symlink():
                        link_path.unlink()
                    else:
                        print(f"Warning: {link_path} exists and is not a symlink, skipping")
                        continue

                # Create relative symlink
                relative_target = Path(category) / item.name
                link_path.symlink_to(relative_target)
                count += 1

    # Also include local/ folder contents
    local_dir = source_dir / "local"
    if local_dir.exists():
        for item in local_dir.iterdir():
            if item.suffix == ".md" and item.is_file():
                link_path = source_dir / item.name
                if not link_path.exists():
                    relative_target = Path("local") / item.name
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
    """Update CLAUDE.md with agent and skill instructions."""
    claude_md = project_root / "CLAUDE.md"
    template_md = project_root / "CLAUDE.template.md"

    # If CLAUDE.md doesn't exist, copy from template
    if not claude_md.exists():
        if template_md.exists():
            with open(template_md, "r") as f:
                content = f.read()
        else:
            content = """# CLAUDE.md

## Agent and Skill Guidelines

<!-- BEGIN:AGENTS -->
<!-- END:AGENTS -->

<!-- BEGIN:SKILLS -->
<!-- END:SKILLS -->
"""
    else:
        with open(claude_md, "r") as f:
            content = f.read()

    # Extract agent instructions
    agents_md = project_root / "AGENTS.md"
    agent_instructions = extract_sections(agents_md, categories, "agents")

    # Extract skill instructions
    skills_md = project_root / "SKILLS.md"
    skill_instructions = extract_sections(skills_md, categories, "skills")

    # Replace content between markers
    agent_section = f"""<!-- BEGIN:AGENTS -->
<!-- Auto-generated agent instructions - DO NOT EDIT between markers -->
<!-- Run /init-agents-and-skills to regenerate -->

{agent_instructions}

<!-- END:AGENTS -->"""

    skill_section = f"""<!-- BEGIN:SKILLS -->
<!-- Auto-generated skill instructions - DO NOT EDIT between markers -->
<!-- Run /init-agents-and-skills to regenerate -->

{skill_instructions}

<!-- END:SKILLS -->"""

    # Replace agents section
    content = re.sub(
        r"<!-- BEGIN:AGENTS -->.*?<!-- END:AGENTS -->",
        agent_section,
        content,
        flags=re.DOTALL
    )

    # Replace skills section
    content = re.sub(
        r"<!-- BEGIN:SKILLS -->.*?<!-- END:SKILLS -->",
        skill_section,
        content,
        flags=re.DOTALL
    )

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

    # Remove existing symlinks
    skills_dir = project_root / "skills"
    agents_dir = project_root / "agents"
    commands_dir = project_root / "commands"

    removed = 0
    removed += remove_existing_symlinks(skills_dir)
    removed += remove_existing_symlinks(agents_dir)
    removed += remove_existing_symlinks(commands_dir)

    if removed > 0:
        print(f"Removed {removed} existing symlinks")

    # Create new symlinks
    skills_count = create_symlinks(skills_dir, categories, excludes)
    agents_count = create_symlinks(agents_dir, categories, excludes)
    commands_count = create_symlinks(commands_dir, categories, excludes)

    print(f"✓ {skills_count} skills loaded")
    print(f"✓ {agents_count} agents loaded")
    print(f"✓ {commands_count} commands loaded")

    # Update CLAUDE.md
    update_claude_md(project_root, categories)
    print("✓ CLAUDE.md updated")

    print("\nDone!")


if __name__ == "__main__":
    main()

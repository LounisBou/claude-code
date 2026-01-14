#!/usr/bin/env python3
"""
List inline TODOs in the codebase.
Usage: python hooks/list_todos.py [scope]
"""
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# ANSI colors
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
NC = '\033[0m'  # No Color

# File extensions to search
EXTENSIONS = {
    '.py', '.ts', '.tsx', '.js', '.jsx', '.go', '.rs',
    '.php', '.vue', '.rb', '.java', '.kt', '.swift', '.c', '.cpp', '.h',
    '.css', '.scss', '.sass', '.less', '.html', '.htm', '.twig', '.blade.php'
}

# Directories to skip
SKIP_DIRS = {
    'node_modules', 'vendor', '.git', '__pycache__', '.venv',
    'venv', 'dist', 'build', '.next', '.nuxt', 'target'
}

# Files to skip (this script itself)
SKIP_FILES = {'list_todos.py'}

# Matches TODO(scope): description in any comment style
# Handles: # // /* <!-- and captures until end of line or --> or */
TODO_PATTERN = re.compile(
    r'(?:#|//|/\*|<!--)\s*TODO\(([^)]+)\):\s*(.+?)(?:\s*(?:-->|\*/))?$'
)


def find_todos(root: Path, scope: str | None = None) -> dict[str, list[tuple[Path, int, str]]]:
    """
    Find all TODOs in the codebase.

    Returns dict mapping scope -> list of (file, line_number, description)
    """
    todos = defaultdict(list)

    for dirpath, dirnames, filenames in os.walk(root):
        # Skip ignored directories
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for filename in filenames:
            if filename in SKIP_FILES:
                continue
            filepath = Path(dirpath) / filename
            if filepath.suffix not in EXTENSIONS:
                continue

            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        match = TODO_PATTERN.search(line)
                        if match:
                            todo_scope = match.group(1)
                            description = match.group(2).strip()

                            if scope is None or todo_scope == scope:
                                todos[todo_scope].append((filepath, line_num, description))
            except (IOError, OSError):
                continue

    return todos


def print_summary(todos: dict[str, list]) -> None:
    """Print summary of TODOs by scope."""
    print(f"{BLUE}Summary:{NC}")
    for scope in sorted(todos.keys()):
        count = len(todos[scope])
        print(f"  {GREEN}{count:3d}{NC} TODO({YELLOW}{scope}{NC})")
    print()


def print_todos(todos: dict[str, list], root: Path) -> None:
    """Print all TODOs with file locations."""
    print(f"{BLUE}Details:{NC}")
    for scope in sorted(todos.keys()):
        print(f"\n{CYAN}TODO({scope}):{NC}")
        for filepath, line_num, description in todos[scope]:
            rel_path = filepath.relative_to(root)
            print(f"  {GREEN}{rel_path}{NC}:{YELLOW}{line_num}{NC}: {description}")


def main():
    scope = sys.argv[1] if len(sys.argv) > 1 else None
    root = Path.cwd()

    todos = find_todos(root, scope)

    if not todos:
        if scope:
            print(f"No TODOs found for scope: {scope}")
        else:
            print("No TODOs found")
        return

    total = sum(len(items) for items in todos.values())

    if scope:
        print(f"{BLUE}TODOs for scope: {YELLOW}{scope}{NC} ({total} total)\n")
    else:
        print(f"{BLUE}All TODOs ({total} total){NC}\n")
        print_summary(todos)

    print_todos(todos, root)


if __name__ == "__main__":
    main()

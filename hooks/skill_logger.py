#!/usr/bin/env python3
"""
Skill usage logger for Claude Code.
Logs all skill invocations to .claude/logs/skills.log
"""
import json
import sys
from datetime import datetime
from pathlib import Path


def log_skill_usage(skill_name: str, args: str, log_file: Path) -> None:
    """
    Log a skill invocation with timestamp to the log file.

    Args:
        skill_name: The skill being invoked.
        args: Optional arguments passed to the skill.
        log_file: Path to the log file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"[{timestamp}] {skill_name}"
    if args:
        # Truncate args for readability
        args_preview = args[:100].replace('\n', ' ')
        if len(args) > 100:
            args_preview += '...'
        log_entry += f" | args: {args_preview}"
    log_entry += "\n"

    # Ensure log directory exists
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Append to log file
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)


def main():
    """Main function to process PreToolUse hook for Skill invocations."""
    try:
        # Read input JSON from stdin
        input_data = json.load(sys.stdin)

        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})

        # Only process Skill tool calls
        if tool_name != 'Skill':
            sys.exit(0)

        # Extract skill information
        skill_name = tool_input.get('skill', '')
        args = tool_input.get('args', '')

        if not skill_name:
            sys.exit(0)  # No skill name to log

        # Determine log file path relative to project root
        project_root = Path.cwd()
        log_file = project_root / '.claude' / 'logs' / 'skills.log'

        # Log the skill usage
        log_skill_usage(skill_name, args, log_file)

    except (json.JSONDecodeError, IOError, OSError) as e:
        # Silently fail - don't block skill execution
        print(f"Warning: Failed to log skill usage: {e}", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        # Catch all other exceptions and fail silently
        print(f"Warning: Unexpected error logging skill usage: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()

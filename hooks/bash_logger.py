#!/usr/bin/env python3
"""
Bash command logger for Claude Code.
Logs all bash commands with descriptions to .claude/logs/bash-commands.log
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path


def log_bash_command(command: str, description: str, log_file: Path) -> None:
    """
    Log a bash command with timestamp to the log file.

    Args:
        command (str): The bash command being executed.
        description (str): Description of what the command does.
        log_file (Path): Path to the log file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {command}"
    if description:
        log_entry += f" - {description}"
    log_entry += "\n"

    # Ensure log directory exists
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Append to log file
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)


def main():
    """Main function to process PreToolUse hook for Bash commands."""
    try:
        # Read input JSON from stdin
        input_data = json.load(sys.stdin)

        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})

        # Only process Bash tool calls
        if tool_name != 'Bash':
            sys.exit(0)

        # Extract command and description
        command = tool_input.get('command', '')
        description = tool_input.get('description', '')

        if not command:
            sys.exit(0)  # No command to log

        # Determine log file path relative to project root
        # The hook runs in the project directory
        project_root = Path.cwd()
        log_file = project_root / '.claude' / 'logs' / 'bash-commands.log'

        # Log the command
        log_bash_command(command, description, log_file)

    except (json.JSONDecodeError, IOError, OSError) as e:
        # Silently fail - don't block command execution
        print(f"Warning: Failed to log bash command: {e}", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        # Catch all other exceptions and fail silently
        print(f"Warning: Unexpected error logging bash command: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()

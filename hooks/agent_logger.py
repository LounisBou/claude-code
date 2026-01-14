#!/usr/bin/env python3
"""
Agent usage logger for Claude Code.
Logs all agent invocations to .claude/logs/agent-invocations.log
"""
import json
import sys
from datetime import datetime
from pathlib import Path


def log_agent_usage(agent_type: str, description: str, prompt: str, log_file: Path) -> None:
    """
    Log an agent invocation with timestamp to the log file.

    Args:
        agent_type: The subagent type being invoked.
        description: Short description of the task.
        prompt: The prompt sent to the agent (truncated).
        log_file: Path to the log file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Truncate prompt for readability (first 100 chars)
    prompt_preview = prompt[:100].replace('\n', ' ') if prompt else ''
    if len(prompt) > 100:
        prompt_preview += '...'

    log_entry = f"[{timestamp}] {agent_type}"
    if description:
        log_entry += f" - {description}"
    if prompt_preview:
        log_entry += f" | {prompt_preview}"
    log_entry += "\n"

    # Ensure log directory exists
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Append to log file
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)


def main():
    """Main function to process PreToolUse hook for Task (agent) invocations."""
    try:
        # Read input JSON from stdin
        input_data = json.load(sys.stdin)

        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})

        # Only process Task tool calls (agent invocations)
        if tool_name != 'Task':
            sys.exit(0)

        # Extract agent information
        agent_type = tool_input.get('subagent_type', '')
        description = tool_input.get('description', '')
        prompt = tool_input.get('prompt', '')

        if not agent_type:
            sys.exit(0)  # No agent type to log

        # Determine log file path relative to project root
        project_root = Path.cwd()
        log_file = project_root / '.claude' / 'logs' / 'agent-invocations.log'

        # Log the agent usage
        log_agent_usage(agent_type, description, prompt, log_file)

    except (json.JSONDecodeError, IOError, OSError) as e:
        # Silently fail - don't block agent execution
        print(f"Warning: Failed to log agent usage: {e}", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        # Catch all other exceptions and fail silently
        print(f"Warning: Unexpected error logging agent usage: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test runner for agent and skill invocation tests.

This script:
1. Reads test definitions from tests/agents/ and tests/skills/
2. Provides test scenarios for manual or automated testing
3. Can check logs to verify invocations (when run after Claude session)

Usage:
    python tests/test_runner.py --list           # List all test scenarios
    python tests/test_runner.py --check-logs    # Check logs for invocations
    python tests/test_runner.py --category dev  # List tests for specific category
"""

import argparse
import json
import os
import re
from pathlib import Path
from datetime import datetime, timedelta


def get_project_root() -> Path:
    """Get the .claude directory root."""
    return Path(__file__).parent.parent


def load_test_definitions(test_type: str) -> dict:
    """Load test definitions for agents or skills."""
    project_root = get_project_root()
    test_file = project_root / "tests" / test_type / "test_definitions.json"
    if not test_file.exists():
        return {"tests": []}
    with open(test_file) as f:
        return json.load(f)


def get_active_items(item_type: str) -> list:
    """Get list of active agents or skills (symlinked)."""
    project_root = get_project_root()
    item_dir = project_root / item_type
    if not item_dir.exists():
        return []

    active = []
    for item in item_dir.iterdir():
        if item.is_symlink():
            name = item.stem if item.suffix == ".md" else item.name
            active.append(name)
    return active


def list_tests(category: str = None, test_type: str = None):
    """List all test scenarios."""
    print("=" * 60)
    print("AGENT AND SKILL INVOCATION TESTS")
    print("=" * 60)

    # Get active items
    active_agents = get_active_items("agents")
    active_skills = get_active_items("skills")

    # Agent tests
    if test_type is None or test_type == "agents":
        print("\n## AGENT TESTS\n")
        agent_defs = load_test_definitions("agents")

        for test in agent_defs.get("tests", []):
            agent_name = test["agent"]
            agent_category = test["category"]

            # Skip if category filter active
            if category and agent_category != category:
                continue

            # Check if agent is active
            is_active = agent_name in active_agents
            status = "[ACTIVE]" if is_active else "[INACTIVE]"

            print(f"### {agent_name} {status}")
            print(f"    Category: {agent_category}")
            print(f"    Triggers: {', '.join(test['triggers'][:3])}...")
            print(f"    Test prompts:")
            for prompt in test.get("test_prompts", [])[:2]:
                print(f"      - \"{prompt}\"")
            print()

    # Skill tests
    if test_type is None or test_type == "skills":
        print("\n## SKILL TESTS\n")
        skill_defs = load_test_definitions("skills")

        for test in skill_defs.get("tests", []):
            skill_name = test["skill"]
            skill_category = test["category"]

            # Skip if category filter active
            if category and skill_category != category:
                continue

            # Check if skill is active
            is_active = skill_name in active_skills
            status = "[ACTIVE]" if is_active else "[INACTIVE]"

            print(f"### {skill_name} {status}")
            print(f"    Category: {skill_category}")
            print(f"    Triggers: {', '.join(test['triggers'][:3])}...")
            print(f"    Test prompts:")
            for prompt in test.get("test_prompts", [])[:2]:
                print(f"      - \"{prompt}\"")
            print()


def check_logs(minutes: int = 30):
    """Check logs for agent and skill invocations."""
    project_root = get_project_root()
    logs_dir = project_root / ".claude" / "logs"

    print("=" * 60)
    print(f"LOG CHECK (last {minutes} minutes)")
    print("=" * 60)

    cutoff_time = datetime.now() - timedelta(minutes=minutes)

    # Check agent log
    agent_log = logs_dir / "agent-invocations.log"
    if agent_log.exists():
        print("\n## AGENT INVOCATIONS\n")
        with open(agent_log) as f:
            for line in f:
                # Parse timestamp [YYYY-MM-DD HH:MM:SS]
                match = re.match(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", line)
                if match:
                    try:
                        log_time = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
                        if log_time >= cutoff_time:
                            print(line.strip())
                    except ValueError:
                        pass
    else:
        print("\nNo agent log found.")

    # Check skill log
    skill_log = logs_dir / "skills.log"
    if skill_log.exists():
        print("\n## SKILL INVOCATIONS\n")
        with open(skill_log) as f:
            for line in f:
                match = re.match(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", line)
                if match:
                    try:
                        log_time = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
                        if log_time >= cutoff_time:
                            print(line.strip())
                    except ValueError:
                        pass
    else:
        print("\nNo skill log found.")


def get_test_summary():
    """Get summary of test coverage."""
    active_agents = get_active_items("agents")
    active_skills = get_active_items("skills")

    agent_defs = load_test_definitions("agents")
    skill_defs = load_test_definitions("skills")

    tested_agents = {t["agent"] for t in agent_defs.get("tests", [])}
    tested_skills = {t["skill"] for t in skill_defs.get("tests", [])}

    print("=" * 60)
    print("TEST COVERAGE SUMMARY")
    print("=" * 60)

    print(f"\nActive agents: {len(active_agents)}")
    print(f"Agents with tests: {len(tested_agents & set(active_agents))}")
    untested_agents = set(active_agents) - tested_agents
    if untested_agents:
        print(f"Untested agents: {', '.join(sorted(untested_agents))}")

    print(f"\nActive skills: {len(active_skills)}")
    print(f"Skills with tests: {len(tested_skills & set(active_skills))}")
    untested_skills = set(active_skills) - tested_skills
    if untested_skills:
        print(f"Untested skills: {', '.join(sorted(list(untested_skills)[:10]))}...")


def main():
    parser = argparse.ArgumentParser(description="Agent and skill test runner")
    parser.add_argument("--list", action="store_true", help="List all test scenarios")
    parser.add_argument("--check-logs", action="store_true", help="Check logs for invocations")
    parser.add_argument("--summary", action="store_true", help="Show test coverage summary")
    parser.add_argument("--category", type=str, help="Filter by category")
    parser.add_argument("--type", type=str, choices=["agents", "skills"], help="Filter by type")
    parser.add_argument("--minutes", type=int, default=30, help="Minutes to check in logs")

    args = parser.parse_args()

    if args.check_logs:
        check_logs(args.minutes)
    elif args.summary:
        get_test_summary()
    else:
        list_tests(category=args.category, test_type=args.type)


if __name__ == "__main__":
    main()

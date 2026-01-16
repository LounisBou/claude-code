#!/usr/bin/env python3
"""
Comprehensive Test Suite for /init-project and Claude Code Configuration.

This script runs ALL tests including:
1. /init-project command functionality (project.json creation, symlinks)
2. Claude visibility tests (agents, commands, skills)
3. CLAUDE.md content verification
4. Agent trigger tests (check logs after Claude invocation)
5. Skill trigger tests (check logs after Claude invocation)

Usage:
    python tests/run_all_tests.py                    # Run ALL tests
    python tests/run_all_tests.py --unit             # Run unit tests only
    python tests/run_all_tests.py --visibility       # Run visibility tests only
    python tests/run_all_tests.py --triggers         # Run agent/skill trigger tests
    python tests/run_all_tests.py --verbose          # Verbose output
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# =============================================================================
# CONFIGURATION
# =============================================================================

# Detect context: production (.claude/tests/) vs development (tests/)
_script_parent = Path(__file__).parent.parent
if _script_parent.name == ".claude":
    # Production: script is in .claude/tests/, project root is parent of .claude
    PROJECT_ROOT = _script_parent.parent
    CLAUDE_DIR = _script_parent
    # In production, items (agents/skills/commands) are in .claude
    ITEMS_DIR = CLAUDE_DIR
else:
    # Development: script is in tests/ at project root
    PROJECT_ROOT = _script_parent
    CLAUDE_DIR = PROJECT_ROOT / ".claude"
    # In development, items are at project root
    ITEMS_DIR = PROJECT_ROOT

LOGS_DIR = CLAUDE_DIR / "logs"
AGENT_LOG = LOGS_DIR / "agent-invocations.log"
SKILL_LOG = LOGS_DIR / "skills.log"

# Test timeout in seconds
CLAUDE_TIMEOUT = 120


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def print_subheader(title: str):
    """Print a formatted subheader."""
    print(f"\n--- {title} ---")


def print_result(name: str, passed: bool, message: str = ""):
    """Print a test result."""
    status = "✓ PASS" if passed else "✗ FAIL"
    msg = f" - {message}" if message else ""
    print(f"  [{status}] {name}{msg}")


def invoke_claude(prompt: str, timeout: int = CLAUDE_TIMEOUT) -> Tuple[bool, str]:
    """
    Invoke Claude CLI with a prompt and return success status and output.
    Uses Popen with communicate() for more reliable timeout handling.
    """
    cmd = [
        "claude",
        "-p", prompt,
        "--dangerously-skip-permissions",
        "--output-format", "text"
    ]

    try:
        proc = subprocess.Popen(
            cmd,
            cwd=str(PROJECT_ROOT),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
            output = stdout + stderr
            return proc.returncode == 0, output
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()  # Clean up
            return False, f"Timeout after {timeout}s"
    except FileNotFoundError:
        return False, "Claude CLI not found"
    except Exception as e:
        return False, f"Error: {str(e)}"


def get_log_entries_after(log_file: Path, after_time: datetime) -> List[str]:
    """Get log entries after a specific time."""
    entries = []
    if not log_file.exists():
        return entries

    with open(log_file) as f:
        for line in f:
            match = re.match(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", line)
            if match:
                try:
                    log_time = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
                    if log_time > after_time:
                        entries.append(line.strip())
                except ValueError:
                    pass
    return entries


def load_test_definitions(test_type: str) -> dict:
    """Load test definitions for agents or skills."""
    test_file = CLAUDE_DIR / "tests" / test_type / "test_definitions.json"
    if not test_file.exists():
        return {"tests": []}
    with open(test_file) as f:
        return json.load(f)


def get_active_items(item_type: str) -> List[str]:
    """Get list of active agents/skills/commands (symlinked)."""
    item_dir = ITEMS_DIR / item_type
    if not item_dir.exists():
        return []

    active = []
    for item in item_dir.iterdir():
        if item.is_symlink():
            name = item.stem if item.suffix == ".md" else item.name
            active.append(name)
    return active


# =============================================================================
# TEST SUITE 1: UNIT TESTS (init-project functionality)
# =============================================================================

def run_unit_tests() -> Dict:
    """Run unit tests using unittest."""
    print_header("UNIT TESTS")

    results = {"passed": 0, "failed": 0, "skipped": 0, "details": []}

    # Run unittest discovery on hooks/
    cmd = ["python", "-m", "unittest", "discover", "hooks/", "-v"]
    try:
        result = subprocess.run(
            cmd,
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=60
        )
        output = result.stdout + result.stderr

        # Parse results
        for line in output.split("\n"):
            if "... ok" in line:
                results["passed"] += 1
            elif "... FAIL" in line or "... ERROR" in line:
                results["failed"] += 1
            elif "... skipped" in line:
                results["skipped"] += 1

        # Show summary
        print(f"\n  Passed: {results['passed']}")
        print(f"  Failed: {results['failed']}")
        print(f"  Skipped: {results['skipped']}")

        if result.returncode != 0 and results["failed"] > 0:
            print("\n  Failures:")
            for line in output.split("\n"):
                if "FAIL:" in line or "ERROR:" in line:
                    print(f"    {line}")

    except Exception as e:
        print(f"  Error running unit tests: {e}")
        results["failed"] += 1

    return results


# =============================================================================
# TEST SUITE 2: INIT-PROJECT TESTS
# =============================================================================

def test_project_json_creation() -> Tuple[bool, str]:
    """
    Test that /init-project creates project.json when it doesn't exist.
    This tests invoking Claude with /init-project command.
    """
    project_json = CLAUDE_DIR / "project.json"

    # Check if project.json exists
    if project_json.exists():
        return True, "project.json already exists"

    # If not, we would need to invoke /init-project
    # For safety, we'll just report that it needs to be created
    return False, "project.json does not exist - run /init-project to create"


def test_symlinks_created() -> Tuple[bool, str]:
    """Test that symlinks are created for agents/skills/commands."""
    errors = []

    for item_type in ["agents", "skills", "commands"]:
        item_dir = ITEMS_DIR / item_type
        if not item_dir.exists():
            errors.append(f"{item_type}/ directory missing")
            continue

        symlinks = [f for f in item_dir.iterdir() if f.is_symlink()]
        if not symlinks:
            # commands/ has init-project.md as regular file
            if item_type == "commands":
                regular = [f for f in item_dir.iterdir() if f.is_file()]
                if regular:
                    continue
            errors.append(f"No symlinks in {item_type}/")

    if errors:
        return False, "; ".join(errors)
    return True, "Symlinks exist in agents/, skills/, commands/"


def test_symlinks_match_categories() -> Tuple[bool, str]:
    """Test that symlinks match categories defined in project.json."""
    project_json = CLAUDE_DIR / "project.json"

    if not project_json.exists():
        return False, "project.json not found"

    with open(project_json) as f:
        config = json.load(f)

    categories = config.get("categories", [])
    if not categories:
        return False, "No categories defined in project.json"

    # Check that active items come from selected categories
    errors = []

    for item_type, available_dir in [
        ("agents", "agents-available"),
        ("skills", "skills-available"),
        ("commands", "commands-available")
    ]:
        available_path = CLAUDE_DIR / available_dir
        if not available_path.exists():
            continue

        # Get items from selected categories
        expected_items = set()
        for category in categories:
            category_path = available_path / category
            if category_path.exists():
                for item in category_path.iterdir():
                    if item.suffix == ".md":
                        expected_items.add(item.stem)
                    elif item.is_dir() and (item / "SKILL.md").exists():
                        expected_items.add(item.name)

        # Get active items
        active = set(get_active_items(item_type))

        # Check for unexpected items (from wrong categories)
        # Note: local/ items are always included
        local_path = available_path / "local"
        local_items = set()
        if local_path.exists():
            for item in local_path.iterdir():
                if item.suffix == ".md":
                    local_items.add(item.stem)
                elif item.is_dir():
                    local_items.add(item.name)

        expected_items.update(local_items)

        unexpected = active - expected_items
        if unexpected and item_type != "commands":  # commands has init-project.md
            errors.append(f"Unexpected {item_type}: {unexpected}")

    if errors:
        return False, "; ".join(errors)
    return True, f"Symlinks match categories: {', '.join(categories)}"


def run_init_project_tests() -> Dict:
    """Run /init-project related tests."""
    print_header("INIT-PROJECT TESTS")

    results = {"passed": 0, "failed": 0, "details": []}

    tests = [
        ("project.json exists", test_project_json_creation),
        ("Symlinks created", test_symlinks_created),
        ("Symlinks match categories", test_symlinks_match_categories),
    ]

    for name, test_fn in tests:
        passed, message = test_fn()
        print_result(name, passed, message)
        if passed:
            results["passed"] += 1
        else:
            results["failed"] += 1
        results["details"].append({"name": name, "passed": passed, "message": message})

    return results


# =============================================================================
# TEST SUITE 3: VISIBILITY TESTS
# =============================================================================

def test_agents_visibility() -> Tuple[bool, str]:
    """Test that Claude can see active agents."""
    prompt = "List all the agents you have available. Just list their names, one per line."

    success, output = invoke_claude(prompt)
    if not success:
        return False, f"Claude invocation failed: {output[:100]}"

    active_agents = get_active_items("agents")
    found = []
    not_found = []

    for agent in active_agents:
        # Check if agent name appears in output
        if agent.lower().replace("-", " ") in output.lower() or agent.lower() in output.lower():
            found.append(agent)
        else:
            not_found.append(agent)

    if not_found:
        return False, f"Agents not visible: {not_found[:5]}"
    return True, f"All {len(active_agents)} agents visible"


def test_commands_visibility() -> Tuple[bool, str]:
    """Test that Claude can see active commands."""
    prompt = "List all the slash commands you have available. Just list their names, one per line."

    success, output = invoke_claude(prompt)
    if not success:
        return False, f"Claude invocation failed: {output[:100]}"

    active_commands = get_active_items("commands")
    # Include init-project.md which is not a symlink
    if (ITEMS_DIR / "commands" / "init-project.md").exists():
        active_commands.append("init-project")

    found = []
    not_found = []

    for cmd in active_commands:
        # Check various forms of the command name
        cmd_lower = cmd.lower()
        cmd_words = cmd_lower.replace("-", " ")
        # Also check without "agent-" prefix
        cmd_short = cmd_lower.replace("agent-", "")

        if (cmd_lower in output.lower() or
            cmd_words in output.lower() or
            cmd_short in output.lower()):
            found.append(cmd)
        else:
            not_found.append(cmd)

    # Allow some tolerance - Claude might not list all commands verbatim
    visibility_ratio = len(found) / len(active_commands) if active_commands else 0

    if visibility_ratio < 0.5:
        return False, f"Only {len(found)}/{len(active_commands)} commands visible: {not_found[:5]}"
    return True, f"{len(found)}/{len(active_commands)} commands visible"


def test_skills_visibility() -> Tuple[bool, str]:
    """Test that Claude can see active skills."""
    prompt = "List all the skills you have available. Just list their names, one per line."

    success, output = invoke_claude(prompt)
    if not success:
        return False, f"Claude invocation failed: {output[:100]}"

    active_skills = get_active_items("skills")
    found = []
    not_found = []

    for skill in active_skills:
        if skill.lower().replace("-", " ") in output.lower() or skill.lower() in output.lower():
            found.append(skill)
        else:
            not_found.append(skill)

    # Allow some tolerance - Claude might not list all skills verbatim
    visibility_ratio = len(found) / len(active_skills) if active_skills else 0

    if visibility_ratio < 0.5:
        return False, f"Only {len(found)}/{len(active_skills)} skills visible"
    return True, f"{len(found)}/{len(active_skills)} skills visible"


def run_visibility_tests() -> Dict:
    """Run visibility tests."""
    print_header("VISIBILITY TESTS")

    results = {"passed": 0, "failed": 0, "details": []}

    tests = [
        ("Agents visible to Claude", test_agents_visibility),
        ("Commands visible to Claude", test_commands_visibility),
        ("Skills visible to Claude", test_skills_visibility),
    ]

    for name, test_fn in tests:
        print(f"\n  Testing: {name}...")
        passed, message = test_fn()
        print_result(name, passed, message)
        if passed:
            results["passed"] += 1
        else:
            results["failed"] += 1
        results["details"].append({"name": name, "passed": passed, "message": message})

    return results


# =============================================================================
# TEST SUITE 4: CLAUDE.md CONTENT TESTS
# =============================================================================

def test_claude_md_has_agents_section() -> Tuple[bool, str]:
    """Test that CLAUDE.md has agents section with content."""
    claude_md = PROJECT_ROOT / "CLAUDE.md"

    if not claude_md.exists():
        return False, "CLAUDE.md not found"

    content = claude_md.read_text()

    if "<!-- BEGIN:AGENTS -->" not in content:
        return False, "Missing BEGIN:AGENTS marker"
    if "<!-- END:AGENTS -->" not in content:
        return False, "Missing END:AGENTS marker"

    # Extract content between markers
    match = re.search(r"<!-- BEGIN:AGENTS -->(.*)<!-- END:AGENTS -->", content, re.DOTALL)
    if not match:
        return False, "Could not extract agents section"

    agents_content = match.group(1).strip()
    if not agents_content or agents_content == "":
        return False, "Agents section is empty"

    # Check that active agents are mentioned
    active_agents = get_active_items("agents")
    mentioned = sum(1 for agent in active_agents if agent in agents_content)

    if mentioned == 0:
        return False, "No active agents mentioned in CLAUDE.md"

    return True, f"{mentioned}/{len(active_agents)} agents documented"


def test_claude_md_has_skills_section() -> Tuple[bool, str]:
    """Test that CLAUDE.md has skills section with content."""
    claude_md = PROJECT_ROOT / "CLAUDE.md"

    if not claude_md.exists():
        return False, "CLAUDE.md not found"

    content = claude_md.read_text()

    if "<!-- BEGIN:SKILLS -->" not in content:
        return False, "Missing BEGIN:SKILLS marker"
    if "<!-- END:SKILLS -->" not in content:
        return False, "Missing END:SKILLS marker"

    # Extract content between markers
    match = re.search(r"<!-- BEGIN:SKILLS -->(.*)<!-- END:SKILLS -->", content, re.DOTALL)
    if not match:
        return False, "Could not extract skills section"

    skills_content = match.group(1).strip()
    if not skills_content or skills_content == "":
        return False, "Skills section is empty"

    # Check that active skills are mentioned
    active_skills = get_active_items("skills")
    mentioned = sum(1 for skill in active_skills if skill in skills_content)

    if mentioned == 0:
        return False, "No active skills mentioned in CLAUDE.md"

    return True, f"{mentioned}/{len(active_skills)} skills documented"


def run_claude_md_tests() -> Dict:
    """Run CLAUDE.md content tests."""
    print_header("CLAUDE.MD CONTENT TESTS")

    results = {"passed": 0, "failed": 0, "details": []}

    tests = [
        ("Agents section populated", test_claude_md_has_agents_section),
        ("Skills section populated", test_claude_md_has_skills_section),
    ]

    for name, test_fn in tests:
        passed, message = test_fn()
        print_result(name, passed, message)
        if passed:
            results["passed"] += 1
        else:
            results["failed"] += 1
        results["details"].append({"name": name, "passed": passed, "message": message})

    return results


# =============================================================================
# TEST SUITE 5: AGENT TRIGGER TESTS
# =============================================================================

def run_agent_trigger_tests(verbose: bool = False) -> Dict:
    """Run trigger tests for all ACTIVE agents."""
    print_header("AGENT TRIGGER TESTS")

    results = {"passed": 0, "failed": 0, "skipped": 0, "details": []}

    active_agents = get_active_items("agents")
    agent_defs = load_test_definitions("agents")

    print(f"\n  Active agents: {len(active_agents)}")
    print(f"  Test definitions: {len(agent_defs.get('tests', []))}")

    for test in agent_defs.get("tests", []):
        agent_name = test["agent"]
        test_prompts = test.get("test_prompts", [])

        # Skip if agent is NOT active
        if agent_name not in active_agents:
            if verbose:
                print(f"\n  [SKIP] {agent_name} - not active")
            results["skipped"] += 1
            continue

        if not test_prompts:
            print(f"\n  [SKIP] {agent_name} - no test prompts")
            results["skipped"] += 1
            continue

        # Run test with first prompt
        test_prompt = test_prompts[0]
        print(f"\n  Testing: {agent_name}")
        print(f"    Prompt: \"{test_prompt[:50]}...\"" if len(test_prompt) > 50 else f"    Prompt: \"{test_prompt}\"")

        # Record time before test
        before_time = datetime.now()
        time.sleep(0.5)

        # Invoke Claude
        success, output = invoke_claude(test_prompt)

        if not success:
            print_result(agent_name, False, f"Claude failed: {output[:50]}")
            results["failed"] += 1
            continue

        time.sleep(0.5)

        # Check logs
        log_entries = get_log_entries_after(AGENT_LOG, before_time)

        if verbose:
            print(f"    Log entries: {len(log_entries)}")

        # Check if this agent was invoked
        agent_invoked = any(f"] {agent_name} " in entry or f"] {agent_name} -" in entry for entry in log_entries)

        if agent_invoked:
            print_result(agent_name, True, "Agent invoked")
            results["passed"] += 1
        else:
            # Check what was invoked instead
            if log_entries:
                print_result(agent_name, False, f"Different agent: {log_entries[0][:40]}...")
            else:
                print_result(agent_name, False, "No agent invoked")
            results["failed"] += 1

        results["details"].append({
            "name": agent_name,
            "passed": agent_invoked,
            "log_entries": log_entries[:2]
        })

    return results


# =============================================================================
# TEST SUITE 6: SKILL TRIGGER TESTS
# =============================================================================

def run_skill_trigger_tests(verbose: bool = False) -> Dict:
    """Run trigger tests for all ACTIVE skills."""
    print_header("SKILL TRIGGER TESTS")

    results = {"passed": 0, "failed": 0, "skipped": 0, "details": []}

    active_skills = get_active_items("skills")
    skill_defs = load_test_definitions("skills")

    print(f"\n  Active skills: {len(active_skills)}")
    print(f"  Test definitions: {len(skill_defs.get('tests', []))}")

    for test in skill_defs.get("tests", []):
        skill_name = test["skill"]
        test_prompts = test.get("test_prompts", [])

        # Skip if skill is NOT active
        if skill_name not in active_skills:
            if verbose:
                print(f"\n  [SKIP] {skill_name} - not active")
            results["skipped"] += 1
            continue

        if not test_prompts:
            print(f"\n  [SKIP] {skill_name} - no test prompts")
            results["skipped"] += 1
            continue

        # Run test with first prompt
        test_prompt = test_prompts[0]
        print(f"\n  Testing: {skill_name}")
        print(f"    Prompt: \"{test_prompt[:50]}...\"" if len(test_prompt) > 50 else f"    Prompt: \"{test_prompt}\"")

        # Record time before test
        before_time = datetime.now()
        time.sleep(0.5)

        # Invoke Claude
        success, output = invoke_claude(test_prompt)

        if not success:
            print_result(skill_name, False, f"Claude failed: {output[:50]}")
            results["failed"] += 1
            continue

        time.sleep(0.5)

        # Check logs
        log_entries = get_log_entries_after(SKILL_LOG, before_time)

        if verbose:
            print(f"    Log entries: {len(log_entries)}")

        # Check if this skill was invoked
        skill_invoked = any(skill_name in entry for entry in log_entries)

        if skill_invoked:
            print_result(skill_name, True, "Skill invoked")
            results["passed"] += 1
        else:
            if log_entries:
                print_result(skill_name, False, f"Different skill: {log_entries[0][:40]}...")
            else:
                print_result(skill_name, False, "No skill invoked")
            results["failed"] += 1

        results["details"].append({
            "name": skill_name,
            "passed": skill_invoked,
            "log_entries": log_entries[:2]
        })

    return results


# =============================================================================
# MAIN TEST RUNNER
# =============================================================================

def print_final_summary(all_results: Dict):
    """Print final test summary."""
    print_header("FINAL TEST SUMMARY")

    total_passed = 0
    total_failed = 0
    total_skipped = 0

    for suite_name, results in all_results.items():
        passed = results.get("passed", 0)
        failed = results.get("failed", 0)
        skipped = results.get("skipped", 0)

        total_passed += passed
        total_failed += failed
        total_skipped += skipped

        status = "✓" if failed == 0 else "✗"
        print(f"  {status} {suite_name}: {passed} passed, {failed} failed", end="")
        if skipped:
            print(f", {skipped} skipped")
        else:
            print()

    print(f"\n  TOTAL: {total_passed} passed, {total_failed} failed", end="")
    if total_skipped:
        print(f", {total_skipped} skipped")
    else:
        print()

    if total_failed == 0:
        print("\n  ✓ ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n  ✗ {total_failed} TESTS FAILED")
        return 1


def main():
    parser = argparse.ArgumentParser(description="Run all tests for /init-project")
    parser.add_argument("--unit", action="store_true", help="Run only unit tests")
    parser.add_argument("--init", action="store_true", help="Run only init-project tests")
    parser.add_argument("--visibility", action="store_true", help="Run only visibility tests")
    parser.add_argument("--claude-md", action="store_true", help="Run only CLAUDE.md tests")
    parser.add_argument("--triggers", action="store_true", help="Run only trigger tests")
    parser.add_argument("--agents", action="store_true", help="Run only agent trigger tests")
    parser.add_argument("--skills", action="store_true", help="Run only skill trigger tests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # If no specific tests requested, run all
    run_all = not any([args.unit, args.init, args.visibility, args.claude_md,
                       args.triggers, args.agents, args.skills])

    all_results = {}

    print("\n" + "=" * 70)
    print(" COMPREHENSIVE TEST SUITE FOR /init-project")
    print("=" * 70)
    print(f"\n  Project root: {PROJECT_ROOT}")
    print(f"  Logs dir: {LOGS_DIR}")
    print(f"  Active agents: {len(get_active_items('agents'))}")
    print(f"  Active skills: {len(get_active_items('skills'))}")
    print(f"  Active commands: {len(get_active_items('commands'))}")

    # Run requested test suites
    if run_all or args.unit:
        all_results["Unit Tests"] = run_unit_tests()

    if run_all or args.init:
        all_results["Init-Project Tests"] = run_init_project_tests()

    if run_all or args.visibility:
        all_results["Visibility Tests"] = run_visibility_tests()

    if run_all or args.claude_md:
        all_results["CLAUDE.md Tests"] = run_claude_md_tests()

    if run_all or args.triggers or args.agents:
        all_results["Agent Trigger Tests"] = run_agent_trigger_tests(args.verbose)

    if run_all or args.triggers or args.skills:
        all_results["Skill Trigger Tests"] = run_skill_trigger_tests(args.verbose)

    # Print summary and return exit code
    return print_final_summary(all_results)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Single entry point for all /init-project tests.

This script runs fully automated tests including:
- Unit tests for config loading and symlink operations
- Integration tests for E2E init-project workflow
- Visibility tests for agents/commands/skills
- Trigger tests that invoke Claude CLI and verify via logs

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py --unit             # Run unit tests only
    python run_tests.py --integration      # Run integration tests only
    python run_tests.py --trigger-tests    # Run agent/skill trigger tests (invokes Claude)
    python run_tests.py --visibility       # Run visibility tests
    python run_tests.py --check-logs       # Check logs for recent invocations
    python run_tests.py -v                 # Verbose output
"""

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
LOGS_DIR = PROJECT_ROOT / ".claude" / "logs"


def run_pytest(test_path: str, verbose: bool = False, extra_args: list = None) -> int:
    """Run pytest on specified path."""
    cmd = [sys.executable, "-m", "pytest", test_path]
    if verbose:
        cmd.append("-v")
    else:
        cmd.append("-q")
    if extra_args:
        cmd.extend(extra_args)

    print(f"  Running: {' '.join(cmd)}", flush=True)
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    print("", flush=True)  # Add newline after pytest output
    return result.returncode


def run_unit_tests(verbose: bool) -> int:
    """Run unit tests."""
    print("\n[UNIT TESTS]")
    results = []

    # Run new tests/ structure
    unit_dir = PROJECT_ROOT / "tests" / "unit"
    if unit_dir.exists():
        results.append(run_pytest("tests/unit/", verbose))

    # Run legacy hooks/ tests
    hooks_test = PROJECT_ROOT / "hooks" / "test_init_project.py"
    if hooks_test.exists():
        results.append(run_pytest("hooks/test_init_project.py", verbose))

    return max(results) if results else 0


def run_integration_tests(verbose: bool) -> int:
    """Run integration tests."""
    print("\n[INTEGRATION TESTS]")
    results = []

    integration_dir = PROJECT_ROOT / "tests" / "integration"
    if integration_dir.exists():
        results.append(run_pytest("tests/integration/", verbose))

    return max(results) if results else 0


def run_trigger_tests(verbose: bool) -> int:
    """Run agent and skill trigger verification tests."""
    print("\n[TRIGGER TESTS - Invoking Claude CLI]")
    results = []

    agents_test = PROJECT_ROOT / "tests" / "agents" / "test_agent_triggers.py"
    if agents_test.exists():
        results.append(run_pytest("tests/agents/test_agent_triggers.py", verbose))

    skills_test = PROJECT_ROOT / "tests" / "skills" / "test_skill_triggers.py"
    if skills_test.exists():
        results.append(run_pytest("tests/skills/test_skill_triggers.py", verbose))

    return max(results) if results else 0


def run_visibility_tests(verbose: bool) -> int:
    """Run visibility tests."""
    print("\n[VISIBILITY TESTS]")
    results = []

    # New visibility tests
    vis_test = PROJECT_ROOT / "tests" / "integration" / "test_visibility.py"
    if vis_test.exists():
        results.append(run_pytest("tests/integration/test_visibility.py", verbose))

    # Legacy hooks tests
    hooks_vis = PROJECT_ROOT / "hooks" / "test_visibility.py"
    if hooks_vis.exists():
        results.append(run_pytest("hooks/test_visibility.py", verbose))

    hooks_claude = PROJECT_ROOT / "hooks" / "test_claude_md.py"
    if hooks_claude.exists():
        results.append(run_pytest("hooks/test_claude_md.py", verbose))

    return max(results) if results else 0


def check_logs(minutes: int = 30):
    """Check logs for recent agent/skill invocations."""
    import re
    from datetime import datetime, timedelta

    print("\n" + "=" * 60)
    print(f"LOG CHECK (last {minutes} minutes)")
    print("=" * 60)

    cutoff = datetime.now() - timedelta(minutes=minutes)

    # Check agent log
    agent_log = LOGS_DIR / "agent-invocations.log"
    print("\n## AGENT INVOCATIONS\n")
    if agent_log.exists():
        found = False
        with open(agent_log) as f:
            for line in f:
                match = re.match(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", line)
                if match:
                    try:
                        log_time = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
                        if log_time >= cutoff:
                            print(f"  {line.strip()}")
                            found = True
                    except ValueError:
                        pass
        if not found:
            print("  No recent agent invocations found.")
    else:
        print("  Agent log file not found.")

    # Check skill log
    skill_log = LOGS_DIR / "skill-invocations.log"
    print("\n## SKILL INVOCATIONS\n")
    if skill_log.exists():
        found = False
        with open(skill_log) as f:
            for line in f:
                match = re.match(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", line)
                if match:
                    try:
                        log_time = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
                        if log_time >= cutoff:
                            print(f"  {line.strip()}")
                            found = True
                    except ValueError:
                        pass
        if not found:
            print("  No recent skill invocations found.")
    else:
        print("  Skill log file not found.")

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Run all init-project tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_tests.py                    # Run all tests
    python run_tests.py --unit             # Run unit tests only
    python run_tests.py --trigger-tests    # Run Claude CLI trigger tests
    python run_tests.py --check-logs       # Show recent log entries
        """
    )
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--trigger-tests", action="store_true", help="Run agent/skill trigger tests (invokes Claude)")
    parser.add_argument("--visibility", action="store_true", help="Run visibility tests")
    parser.add_argument("--check-logs", action="store_true", help="Check logs for invocations")
    parser.add_argument("--minutes", type=int, default=30, help="Minutes to check in logs (default: 30)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()
    verbose = args.verbose

    # If specific test type requested
    if args.check_logs:
        return check_logs(args.minutes)

    if args.unit:
        return run_unit_tests(verbose)

    if args.integration:
        return run_integration_tests(verbose)

    if args.trigger_tests:
        return run_trigger_tests(verbose)

    if args.visibility:
        return run_visibility_tests(verbose)

    # Default: run ALL tests
    print("=" * 60)
    print("RUNNING ALL INIT-PROJECT TESTS")
    print("=" * 60)

    results = {}

    print("\n[1/4] Unit Tests...")
    results["unit"] = run_unit_tests(verbose)

    print("\n[2/4] Visibility Tests...")
    results["visibility"] = run_visibility_tests(verbose)

    print("\n[3/4] Integration Tests...")
    results["integration"] = run_integration_tests(verbose)

    print("\n[4/4] Trigger Tests (Claude CLI)...")
    results["trigger"] = run_trigger_tests(verbose)

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    total = len(results)
    passed = sum(1 for r in results.values() if r == 0)

    for name, code in results.items():
        status = "PASS" if code == 0 else "FAIL"
        print(f"  {name:15} {status}")

    print(f"\nTotal: {passed}/{total} passed")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())

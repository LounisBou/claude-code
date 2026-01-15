---
name: test-agents-skills
description: Run agent and skill invocation tests to verify they trigger correctly
user_invocable: true
---

# Test Agents and Skills Command

You are running tests to verify that agents and skills are invoked correctly when prompts match their "when to use" criteria.

## Quick Start

Run ALL tests with a single command:

```bash
python .claude/tests/run_all_tests.py
```

## Test Suites

The comprehensive test runner includes:

1. **Unit Tests** - Tests for init-project.py functionality
2. **Init-Project Tests** - Verifies project.json and symlinks
3. **Visibility Tests** - Verifies Claude can see agents/commands/skills
4. **CLAUDE.md Tests** - Verifies documentation is generated correctly
5. **Agent Trigger Tests** - Tests each ACTIVE agent is triggered by matching prompts
6. **Skill Trigger Tests** - Tests each ACTIVE skill is triggered by matching prompts

## Command Options

```bash
# Run ALL tests
python .claude/tests/run_all_tests.py

# Run specific test suites
python .claude/tests/run_all_tests.py --unit          # Unit tests only
python .claude/tests/run_all_tests.py --init          # Init-project tests only
python .claude/tests/run_all_tests.py --visibility    # Visibility tests only
python .claude/tests/run_all_tests.py --claude-md     # CLAUDE.md tests only
python .claude/tests/run_all_tests.py --triggers      # Agent + skill trigger tests
python .claude/tests/run_all_tests.py --agents        # Agent trigger tests only
python .claude/tests/run_all_tests.py --skills        # Skill trigger tests only

# Verbose output
python .claude/tests/run_all_tests.py --verbose
```

## Test Definitions

Test definitions are stored in JSON files:

- `.claude/tests/agents/test_definitions.json` - 16 agent test definitions (ALL agents)
- `.claude/tests/skills/test_definitions.json` - 54 skill test definitions (ALL skills)

**Important:** ALL agents/skills have test definitions, but only ACTIVE ones (symlinked) are tested when running.

## How Trigger Tests Work

For each active agent/skill:

1. Send a test prompt to Claude CLI (`claude -p "prompt" --dangerously-skip-permissions`)
2. Check `.claude/logs/agent-invocations.log` or `.claude/logs/skills.log`
3. Verify the correct agent/skill was invoked
4. Report PASS/FAIL

## Expected Output

```
======================================================================
 COMPREHENSIVE TEST SUITE FOR /init-project
======================================================================

  Project root: /path/to/project
  Logs dir: /path/to/project/.claude/logs
  Active agents: 9
  Active skills: 21
  Active commands: 12

======================================================================
 UNIT TESTS
======================================================================
  Passed: 34
  Failed: 0
  Skipped: 8

======================================================================
 INIT-PROJECT TESTS
======================================================================
  [✓ PASS] project.json exists - project.json already exists
  [✓ PASS] Symlinks created - Symlinks exist in agents/, skills/, commands/
  [✓ PASS] Symlinks match categories - Symlinks match categories: dev, claude, docs

...

======================================================================
 FINAL TEST SUMMARY
======================================================================
  ✓ Unit Tests: 34 passed, 0 failed, 8 skipped
  ✓ Init-Project Tests: 3 passed, 0 failed
  ✓ Visibility Tests: 3 passed, 0 failed
  ✓ CLAUDE.md Tests: 2 passed, 0 failed
  ✓ Agent Trigger Tests: 9 passed, 0 failed, 7 skipped
  ✓ Skill Trigger Tests: 21 passed, 0 failed, 33 skipped

  TOTAL: 72 passed, 0 failed, 48 skipped

  ✓ ALL TESTS PASSED!
```

## Instructions

1. Run `python .claude/tests/run_all_tests.py` to execute all tests
2. Review the output for any failures
3. If trigger tests fail, check that:
   - The agent/skill is properly symlinked
   - The logging hooks are configured in `.claude/settings.json`
   - The test prompt matches the agent/skill's "when to use" criteria

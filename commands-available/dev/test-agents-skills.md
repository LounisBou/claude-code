---
name: test-agents-skills
description: Run agent and skill invocation tests to verify they trigger correctly
user_invocable: true
---

# Test Agents and Skills Command

You are running tests to verify that agents and skills are invoked correctly when prompts match their "when to use" criteria.

## Test Workflow

### Step 1: Show Test Summary
Run the test runner to show current test coverage:

```bash
python tests/test_runner.py --summary
```

### Step 2: List Available Tests
Show all test scenarios for active agents and skills:

```bash
python tests/test_runner.py --list
```

### Step 3: Run Unit Tests
Run the unit tests for init-project, visibility, and CLAUDE.md:

```bash
python -m unittest discover hooks/ -v 2>&1 | grep -E "^test_|OK|FAIL|ERROR|skipped"
```

### Step 4: Interactive Agent Testing
For each active agent, I will:
1. Read a test prompt from the test definitions
2. Explain which agent should be triggered
3. Ask you if you want to test it

Example test interaction:
```
Testing: debugging-assistant
Prompt: "I'm getting a TypeError when I call this function"
Expected: Claude should invoke the debugging-assistant agent

Would you like me to test this? [Yes/No/Skip to next]
```

### Step 5: Check Invocation Logs
After testing, check if agents/skills were invoked:

```bash
python tests/test_runner.py --check-logs --minutes 60
```

## Test Report Format

After running tests, I will provide a summary:

```
=== TEST RESULTS ===

Unit Tests:
  - test_init_project.py: 20/20 passed
  - test_visibility.py: 13/13 passed
  - test_claude_md.py: 1/9 passed (8 skipped - needs initialization)

Agent Invocation Tests:
  - debugging-assistant: PASS (invoked when expected)
  - test-generator: PASS (invoked when expected)
  - code-review: SKIP (not tested)

Skill Invocation Tests:
  - test-driven-development: PASS (invoked when expected)
  - systematic-debugging: PASS (invoked when expected)

Coverage: 8/11 agents tested, 6/22 skills tested
```

## Quick Test Commands

```bash
# Run all unit tests
python -m unittest discover hooks/ -v

# Show test summary
python tests/test_runner.py --summary

# List all tests
python tests/test_runner.py --list

# Check recent logs
python tests/test_runner.py --check-logs

# Filter by category
python tests/test_runner.py --list --category dev
python tests/test_runner.py --list --type agents
```

## Instructions

1. Start by running the unit tests
2. Show the test summary to see coverage
3. Ask the user which agents/skills they want to test
4. For each test, explain what should happen and check the result
5. Provide a final summary of all test results

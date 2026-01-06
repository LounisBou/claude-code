---
name: generate-tests
description: Generate comprehensive tests for specified code following project patterns
user_invocable: true
---

# Generate Tests Command

Launches the test-generator agent to create comprehensive test coverage for your code.

## Usage

```bash
/generate-tests [file_or_class_name]
```

## Examples

```bash
# Generate tests for a specific file
/generate-tests src/services/user_service.py

# Generate tests for a class
/generate-tests UserController

# Generate tests with context
/generate-tests "the authentication module"

# Just ask for tests
/generate-tests
```

## What It Does

1. Analyzes the code you want to test
2. Discovers existing test patterns in your project
3. Detects your test framework automatically
4. Generates comprehensive tests covering:
   - Happy path scenarios
   - Edge cases
   - Error conditions
   - Integration points
5. Follows your project's test conventions

## Supported Languages

- Python (pytest, unittest)
- JavaScript/TypeScript (Jest, Mocha, Vitest)
- PHP (PHPUnit)
- Go (testing package)
- Rust (cargo test)

---

You are launching the test-generator agent. Use the Task tool with subagent_type='test-generator'.

Pass the user's request to the agent as the prompt. If the user provided a file name or class name, include that in the prompt. If they just said "/generate-tests", ask them what they want to generate tests for.

Example:
```
Task(subagent_type='test-generator', prompt='Generate comprehensive tests for the UserService class in src/services/user_service.py', description='Generate tests for UserService')
```

---
name: agent-code-review
description: Review code for security vulnerabilities, bugs, performance issues, and adherence to project patterns
user_invocable: true
---

# Code Review Command

Launches the code-review agent to perform a comprehensive review of code changes.

## Usage

```bash
/code-review [files_or_scope]
```

## Examples

```bash
# Review current changes
/code-review

# Review specific file
/code-review src/services/payment.py

# Review staged changes
/code-review "staged changes"

# Review recent commits
/code-review "last 3 commits"

# Review a PR
/code-review "PR #123"
```

## What It Does

1. Analyzes code for security vulnerabilities
2. Identifies bugs and logic errors
3. Checks for performance issues
4. Verifies adherence to project patterns
5. Detects LLM-generated code issues (placeholders, redundant patterns)
6. Provides actionable feedback with severity levels

## Review Categories

### Critical (Blocks Deployment)
- Security vulnerabilities (XSS, SQL injection, etc.)
- Exposed secrets/credentials
- Data corruption risks
- Logic errors that produce wrong results

### Warning (Should Address)
- Unhandled edge cases
- Resource leaks
- Performance issues (N+1 queries, etc.)
- Pattern inconsistencies

### Suggestion (Consider)
- Alternative approaches
- Missing documentation
- Test coverage gaps

## When to Use

- Before merging PRs
- After completing feature work
- Before major releases
- When reviewing LLM-generated code
- During context compaction checkpoints

---

When this command is invoked, review the code changes thoroughly. Focus on real issues that affect correctness, security, and maintainability. Be pragmatic - don't concern troll over theoretical problems.

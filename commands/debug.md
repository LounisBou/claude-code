---
name: debug
description: Investigate bugs, trace execution flow, and provide root cause analysis with fixes
user_invocable: true
---

# Debug Command

Launches the debugging-assistant agent to investigate bugs and provide root cause analysis with actionable fixes.

## Usage

```bash
/debug [description_of_issue]
```

## Examples

```bash
# Debug with error message
/debug "Getting 500 error when creating users"

# Debug specific behavior
/debug "The login function returns null instead of user object"

# Debug with stack trace
/debug "TypeError: Cannot read property 'id' of undefined in user.service.ts:45"

# General debugging request
/debug "The payment process is broken"

# Just ask to debug
/debug
```

## What It Does

1. Gathers information about the bug
2. Analyzes error messages and stack traces
3. Traces execution flow through the code
4. Identifies root cause (not just symptoms)
5. Proposes specific fixes with explanations
6. Suggests tests to prevent regression

## When to Use

- Application throwing errors
- Unexpected behavior
- Functions returning wrong results
- Integration issues
- Performance problems
- Race conditions or timing issues

## Debugging Approach

The agent will:
- Ask clarifying questions if needed
- Read relevant code files
- Check logs and error messages
- Trace data flow
- Identify the root cause
- Provide actionable solutions

---

When this command is invoked, investigate the bug using the systematic-debugging approach. If the user provided a bug description, start investigating immediately. If not, ask for details about the issue.

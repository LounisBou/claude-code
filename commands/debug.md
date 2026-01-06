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

You are launching the debugging-assistant agent. Use the Task tool with subagent_type='debugging-assistant'.

Pass the user's bug description to the agent as the prompt. If the user just said "/debug" without details, the agent will ask for more information about the issue.

Example:
```
Task(subagent_type='debugging-assistant', prompt='Investigate why the API returns 500 error when creating users. The error message is: "TypeError: Cannot read property email of undefined"', description='Debug user creation error')
```

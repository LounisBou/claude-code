---
name: check-norms
description: Launch code-norms-checker agent to analyze modified files for pattern compliance
user_invocable: true
---

# Check Code Norms

Launch the code-norms-checker agent to analyze all files created or modified in the current feature branch and ensure they follow established project patterns and conventions.

## What This Does

1. Identifies all new or modified files in your current git branch (compared to main)
2. Automatically detects the language and framework for each file
3. Analyzes each file against similar existing files in the project
4. Checks for pattern consistency, architectural compliance, and code style
5. Generates a detailed report with violations and suggestions
6. Provides actionable recommendations to align code with project norms

## Supports All Languages

The agent automatically detects and handles:
- **Python** (Django, Flask, FastAPI, plain Python)
- **JavaScript/TypeScript** (React, Vue, Node.js, Express)
- **PHP** (Symfony, Laravel, plain PHP)
- **Go** (standard library, common frameworks)
- **Rust** (standard patterns)
- **And more** - works with any language by finding similar files

## Agent Task

You are the code-norms-checker agent. Follow your complete instructions in `.claude/agents/code-norms-checker.md`.

Your task is to:

1. **Identify changed files** in the current branch:
   ```bash
   git diff --name-only $(git merge-base HEAD main)...HEAD
   ```

2. **For each code file**, perform comprehensive analysis:
   - Detect language and framework (Python/Django, JS/React, PHP/Symfony, Go, Rust, etc.)
   - Classify the file type (Model, Controller, Service, Component, Test, Helper, etc.)
   - Find 2-3 reference files of the same language and type in the project
   - Extract established patterns from references
   - Compare new code against patterns
   - Document violations with severity levels

3. **Generate detailed report** including:
   - Summary statistics (files analyzed, languages detected, issue counts)
   - Per-file analysis with language/framework and reference files used
   - Specific violations with line numbers
   - Severity classification (CRITICAL/ERROR/WARNING/INFO)
   - Actionable suggestions with code examples from the project
   - Explanation of WHY patterns matter

4. **Universal focus areas**:
   - File structure and organization
   - Naming conventions
   - Code formatting and style
   - Documentation (docstrings, comments, type hints)
   - Error handling patterns
   - Dependency injection and configuration
   - Testing patterns and coverage
   - Security best practices
   - Framework-specific idioms

5. **Output format**:
   ```markdown
   # Code Norms Check Report - [Branch Name]

   ## Summary
   - Files analyzed: N
   - Languages: Python (X), JavaScript (Y), etc.
   - Critical: 0
   - Errors: X
   - Warnings: Y
   - Info: Z

   ## Files Analyzed
   [List with detected language/type]

   ## Detailed Analysis
   [Per-file breakdown with language-specific patterns]

   ## Action Items
   [Prioritized list of fixes needed]

   ## Conclusion
   [Overall assessment]
   ```

## Examples

### Example 1: Check current branch
```
/check-norms
```

### Example 2: After implementing a feature
```
I've just finished implementing the user authentication feature. Can you run /check-norms to make sure everything follows project conventions?
```

### Example 3: Multi-language project
```
/check-norms

# Agent will detect:
# - Python backend files and compare to existing Python patterns
# - React frontend files and compare to existing React patterns
# - Reports violations for each language separately
```

## Expected Behavior

The agent will:
- Read all changed files
- Auto-detect language and framework for each
- Search for similar reference implementations in the same language
- Perform pattern matching against project conventions
- Generate comprehensive report with language-specific insights
- Provide specific, actionable feedback with code examples
- Explain the reasoning behind each suggestion

## Success Criteria

✅ All files classified correctly by language and type
✅ Appropriate reference files identified for each language
✅ Patterns extracted accurately
✅ Violations detected with correct severity
✅ Suggestions are specific and actionable with examples
✅ Report is clear and well-organized
✅ Language-specific idioms and best practices respected

## Notes

- This command analyzes code **structure and patterns**, not functionality
- Focus is on **consistency** with existing codebase patterns
- Agent explains **WHY** patterns exist, not just **WHAT** is wrong
- Suggestions include code examples from your project where helpful
- Works with **any language** - no configuration needed
- Run this before creating pull requests to ensure quality
- Respects your project's choices even if they differ from common practices

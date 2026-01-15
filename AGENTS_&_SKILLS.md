# DEFAULT_CLAUDE.md

This file provides generic instructions for Claude Code on how to effectively use agents and skills.

## Agent and Skill Invocation Guidelines

### Understanding the Difference

| Component | Invocation Method | Purpose |
|-----------|------------------|---------|
| **Agents** | Task tool with `subagent_type` parameter | Autonomous specialists for complex, multi-step tasks |
| **Skills** | Skill tool with skill name | On-demand knowledge modules for specialized domains |

### When to Use Agents

Agents are specialized autonomous workers. Use the Task tool to invoke them when:

1. **Proactive Agents** - Invoke automatically when conditions are met:
   - `test-generator`: After user finishes implementing code, mentions coverage, or says "done with feature"
   - `debugging-assistant`: When user reports bugs, errors, crashes, "why is X happening", or unexpected behavior
   - `vuejs-developer`: When working with .vue files or Vue-specific patterns

2. **Reactive Agents** - Invoke only when user explicitly requests:
   - `code-review`: User says "review", "check code", "ready for production?"
   - `code-norms-checker`: User asks about pattern consistency or conventions
   - `refactoring-advisor`: User says "refactor", "clean up", "simplify"
   - `dependency-auditor`: User asks about vulnerable/outdated dependencies
   - `api-designer`: User asks to "design API" or "what endpoints"
   - `migration-planner`: User asks about version upgrades or breaking changes
   - `documentation-generator`: User asks to "create README" or "generate docs"
   - `docstring-generator`: User asks to "add docstring" or document functions

3. **Specialist Agents** - Invoke based on technology context:
   - `api-platform-architect`: Symfony API Platform work
   - `doctrine-specialist`: Doctrine ORM migrations, queries, batch processing
   - `async-api-specialist`: Python asyncio patterns
   - `laravel-developer`: Laravel applications
   - `python-api-developer`: FastAPI, Django, Flask APIs

### When to Use Skills

Skills provide reference knowledge. Use the Skill tool when:

- You need language-specific patterns (e.g., `python-testing-patterns`, `vuejs-dev`)
- You need documentation standards (e.g., `python-docstring`, `ts-docstring`)
- You need framework-specific guidance (e.g., `php-symfony-*`, `php-laravel-specialist`)
- You need workflow guidance (e.g., `test-driven-development`, `systematic-debugging`)

### WHEN/WHEN NOT Pattern

All agents and skills have explicit trigger conditions in their descriptions:

```
WHEN: [conditions that should trigger this agent/skill]
WHEN NOT: [conditions where another agent/skill is more appropriate]
```

**Always check these conditions** before invoking an agent or skill.

### Disambiguation with DIFFERENT FROM

When agents/skills have similar purposes, use DIFFERENT FROM clauses:

- `code-review` vs `code-norms-checker`: Review finds bugs/security; norms checks pattern consistency
- `documentation-generator` vs `docstring-generator`: Docs creates README/API docs; docstrings documents code-level functions
- `debugging-assistant` vs `code-review`: Debugging investigates errors; review assesses code quality
- `refactoring-advisor` vs `code-review`: Refactoring proposes structural improvements; review finds issues

### Proactive Invocation Rules

**DO invoke proactively:**
- `test-generator` after implementing a feature
- `debugging-assistant` when user encounters any error or unexpected behavior
- `vuejs-developer` when user is working with .vue files

**DO NOT invoke proactively:**
- `code-review` - only when explicitly requested
- `documentation-generator` - only when explicitly requested
- Reactive agents without explicit user request

### Best Practices

1. **Read agent descriptions first** - Check WHEN/WHEN NOT conditions
2. **Use specific agents over generic exploration** - If a specialized agent exists for the task, use it
3. **Chain agents appropriately** - After debugging, consider test-generator; after implementing, consider code-review
4. **Respect the reactive boundary** - Don't invoke code-review, documentation-generator, or similar without explicit request
5. **Match technology stack** - Use laravel-developer for Laravel, not generic php patterns

### Example Triggers

| User Says | Invoke |
|-----------|--------|
| "Getting an error when..." | `debugging-assistant` |
| "Can you review this code?" | `code-review` |
| "Add tests for this" | `test-generator` |
| "Is this following our patterns?" | `code-norms-checker` |
| "Create a UserCard component" (Vue project) | `vuejs-developer` |
| "Refactor this class" | `refactoring-advisor` |
| "Check for vulnerable deps" | `dependency-auditor` |
| "Design an API for orders" | `api-designer` |
| "Upgrade from Python 3.8 to 3.12" | `migration-planner` |
| "Generate README for this project" | `documentation-generator` |
| "Add docstrings to this file" | `docstring-generator` |

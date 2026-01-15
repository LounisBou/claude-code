# Agent Usage Instructions

This file contains usage instructions for each agent. The build script extracts relevant sections based on project.json categories and adds them to CLAUDE.md.

## Category: dev

### debugging-assistant
**WHEN:** User reports bugs, errors, crashes, test failures, stack traces, "why is X happening", "not working", unexpected behavior, performance issues.
**WHEN NOT:** User already knows root cause and just needs fix, simple typos, implementing new features, code review requests.
**Invoke:** Task tool with `subagent_type="debugging-assistant"`

### test-generator
**WHEN:** User finished implementing code, asks for tests, mentions coverage, code without tests detected, user says "done with feature".
**WHEN NOT:** User is still writing implementation, debugging existing tests, asking about test failures (use debugging-assistant).
**Invoke:** Task tool with `subagent_type="test-generator"`

### code-review
**WHEN:** User says "review", "check code", "ready for production?", "any issues?", security audit request, before commit/merge.
**WHEN NOT:** Pattern consistency (use code-norms-checker), refactoring advice, debugging errors, generating tests.
**Note:** Do NOT use proactively - only when user explicitly requests review.
**Invoke:** Task tool with `subagent_type="code-review"`

### code-norms-checker
**WHEN:** User asks "does this follow patterns?", "is this consistent?", "check conventions", pattern compliance check, style consistency review.
**WHEN NOT:** Bug hunting (use code-review), refactoring (use refactoring-advisor), debugging (use debugging-assistant).
**Invoke:** Task tool with `subagent_type="code-norms-checker"`

### refactoring-advisor
**WHEN:** User says "refactor", "clean up", "simplify", "too complex", "technical debt", "code smells", "improve structure".
**WHEN NOT:** Bug fixes (use debugging-assistant), code review (use code-review), writing new features.
**Invoke:** Task tool with `subagent_type="refactoring-advisor"`

### dependency-auditor
**WHEN:** User asks "vulnerable dependencies?", "outdated packages?", "audit deps", "before deploy", security scan, npm/pip/composer audit.
**WHEN NOT:** Framework upgrades (use migration-planner), general code security (use code-review).
**Invoke:** Task tool with `subagent_type="dependency-auditor"`

### migration-planner
**WHEN:** User asks "upgrade to", "migrate from X to Y", "breaking changes?", "what will break?", version migration planning.
**WHEN NOT:** Package security (use dependency-auditor), code refactoring (use refactoring-advisor), new feature implementation.
**Invoke:** Task tool with `subagent_type="migration-planner"`

## Category: symfony

### api-platform-architect
**WHEN:** Working with Symfony API Platform, configuring resources/operations, implementing filters, serialization groups, state providers, API Platform security.
**WHEN NOT:** Generic REST API design (use api-designer), Doctrine queries (use doctrine-specialist), non-Symfony PHP.
**Invoke:** Task tool with `subagent_type="api-platform-architect"`

### doctrine-specialist
**WHEN:** Creating Doctrine migrations, N+1 query problems, eager loading, batch processing large datasets, DQL/QueryBuilder optimization.
**WHEN NOT:** API Platform resources (use api-platform-architect), Laravel/Eloquent (use laravel-developer), raw SQL optimization.
**Invoke:** Task tool with `subagent_type="doctrine-specialist"`

## Category: laravel

### laravel-developer
**WHEN:** Working with Laravel apps, Eloquent models/relationships, Laravel queues/jobs, Sanctum/Passport auth, API resources, Laravel N+1 optimization.
**WHEN NOT:** Symfony/API Platform (use api-platform-architect), raw PHP, non-Laravel PHP frameworks.
**Invoke:** Task tool with `subagent_type="laravel-developer"`

## Category: python

### python-api-developer
**WHEN:** Building Python REST APIs, FastAPI endpoints, Pydantic models, SQLAlchemy setup, Django/Flask APIs, Python JWT auth.
**WHEN NOT:** Heavy asyncio patterns (use async-api-specialist), non-Python backends, frontend code.
**Invoke:** Task tool with `subagent_type="python-api-developer"`

### async-api-specialist
**WHEN:** Building async Python APIs, concurrent API calls, asyncio patterns, semaphores/rate limiting, producer-consumer queues, async database sessions.
**WHEN NOT:** Sync Python APIs (use python-api-developer), non-Python async, general Python backend without async needs.
**Invoke:** Task tool with `subagent_type="async-api-specialist"`

## Category: vue

### vuejs-developer
**WHEN:** Working with .vue files, creating Vue components, Vue 3 Composition API, Pinia state, Vue Router, Vue-specific patterns.
**WHEN NOT:** Non-Vue frontend work (React, Angular), backend APIs, general JavaScript without Vue context.
**Invoke:** Task tool with `subagent_type="vuejs-developer"`

## Category: api

### api-designer
**WHEN:** User asks "design API", "what endpoints", "OpenAPI spec", "REST design", "GraphQL schema", API planning.
**WHEN NOT:** Implementing API code (use language-specific agents), debugging API issues, API Platform config (use api-platform-architect).
**Invoke:** Task tool with `subagent_type="api-designer"`

## Category: docs

### documentation-generator
**WHEN:** User asks "create README", "generate docs", "API documentation", "architecture docs", "document this project".
**WHEN NOT:** Code-level docstrings (use docstring-generator), code comments, inline documentation.
**Note:** NEVER use proactively - only when user explicitly requests documentation.
**Invoke:** Task tool with `subagent_type="documentation-generator"`

### docstring-generator
**WHEN:** User asks "add docstring", "document this function", "JSDoc", "TSDoc", "PHPDoc", "document methods".
**WHEN NOT:** Project-level docs like README (use documentation-generator), code comments, implementation changes.
**Invoke:** Task tool with `subagent_type="docstring-generator"`

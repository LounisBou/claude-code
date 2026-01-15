# Skill & Agent Categories

This document describes all available categories for organizing skills and agents.

## Core Categories

### dev
Generic development tools applicable to all projects.

**Skills:** test-driven-development, systematic-debugging, brainstorming, writing-plans, executing-plans, finishing-a-development-branch, using-git-worktrees, dispatching-parallel-agents, sql-optimization-patterns, subagent-driven-development, verification-before-completion, receiving-code-review, requesting-code-review

**Agents:** debugging-assistant, test-generator, code-review, code-norms-checker, refactoring-advisor, dependency-auditor, migration-planner

**Commands:** agent-debug, agent-generate-tests, agent-code-review, agent-check-norms, agent-refactor, agent-audit-deps, agent-plan-migration, find-pattern, format-markdown

**Recommended for:** All projects

### claude
Claude Code plugin development: creating agents, skills, commands, and hooks.

**Skills:** claude-agent-creator, claude-command-development, claude-hook-development, claude-hookify-rules, claude-plugin-settings, claude-plugin-structure, claude-skill-creator, claude-skill-development

**Agents:** None

**Commands:** None

**Use when:** Building Claude Code extensions

### mcp
Model Context Protocol: building and integrating MCP servers.

**Skills:** mcp-builder, mcp-integration

**Agents:** None

**Commands:** None

**Use when:** Connecting Claude to external data sources

### docs
Documentation generation for README, API docs, and docstrings.

**Skills:** None

**Agents:** documentation-generator, docstring-generator

**Commands:** agent-generate-docs, agent-generate-docstring

**Use when:** You need documentation generation capabilities

### api
REST/GraphQL API design and OpenAPI specifications.

**Skills:** None

**Agents:** api-designer

**Commands:** agent-design-api

**Use when:** Designing new APIs

## Language Categories

### php
Generic PHP development and PHPDoc standards.

**Skills:** php-docstring

**Agents:** None

**Commands:** None

### python
Python backend development: FastAPI, Django, Flask, async patterns, data processing.

**Skills:** python-async-patterns, python-backend, python-data-transform, python-docstring, python-docx, python-packaging, python-pdf, python-performance-optimization, python-testing-patterns, python-uv-package-manager, python-xlsx

**Agents:** python-api-developer, async-api-specialist

**Commands:** agent-python-api, agent-async-api

### js
Generic JavaScript ES6+ patterns and JSDoc documentation.

**Skills:** js-dev, js-docstring

**Agents:** None

**Commands:** None

### ts
TypeScript patterns, types, and TSDoc documentation.

**Skills:** ts-dev, ts-docstring

**Agents:** None

**Commands:** None

### html
HTML structure, semantics, and accessibility.

**Skills:** html-dev

**Agents:** None

**Commands:** None

## Framework Categories

### symfony
Symfony framework: API Platform, Doctrine ORM, migrations.

**Skills:** php-symfony-api-platform-filters, php-symfony-api-platform-resources, php-symfony-api-platform-security, php-symfony-api-platform-serialization, php-symfony-api-platform-state-providers, php-symfony-doctrine-batch-processing, php-symfony-doctrine-fetch-modes, php-symfony-doctrine-migrations

**Agents:** api-platform-architect, doctrine-specialist

**Commands:** agent-api-platform, agent-doctrine

### laravel
Laravel 10+: Eloquent ORM, queues, Sanctum auth.

**Skills:** php-laravel-specialist

**Agents:** laravel-developer

**Commands:** agent-laravel

### vue
Vue 3: Composition API, Pinia state management, component patterns.

**Skills:** vuejs-dev, vuejs-apex-charts, vuejs-shadcn

**Agents:** vuejs-developer

**Commands:** agent-vue

### tailwind
Tailwind CSS utilities and component styling patterns.

**Skills:** tailwind-css-dev, frontend-design

**Agents:** None

**Commands:** None

## Common Profile Combinations

| Profile | Categories | Description |
|---------|------------|-------------|
| symfony | dev, php, symfony | PHP/Symfony backend |
| laravel | dev, php, laravel | PHP/Laravel backend |
| python | dev, python | Python backend |
| vue-tailwind | dev, html, js, ts, vue, tailwind | Vue.js frontend |
| fullstack-symfony | dev, php, symfony, html, js, ts, vue, tailwind, api, docs | Full-stack Symfony + Vue |
| fullstack-laravel | dev, php, laravel, html, js, ts, vue, tailwind, api, docs | Full-stack Laravel + Vue |

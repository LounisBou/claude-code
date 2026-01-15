# Skill Usage Instructions

This file contains usage instructions for each skill. The build script extracts relevant sections based on project.json categories and adds them to CLAUDE.md.

## Category: dev

### test-driven-development
**WHEN:** Implementing new features, fixing bugs, refactoring, any behavior changes. Write test BEFORE implementation code.
**WHEN NOT:** Throwaway prototypes, generated code, configuration files, debugging root cause (use systematic-debugging first).
**Invoke:** Skill tool with `skill="test-driven-development"`

### systematic-debugging
**WHEN:** Encountering bugs, test failures, unexpected behavior, build failures, performance issues. Use ESPECIALLY under time pressure or after multiple failed fixes.
**WHEN NOT:** Issue is already understood with clear root cause, writing new features, simple typos.
**Invoke:** Skill tool with `skill="systematic-debugging"`

### brainstorming
**WHEN:** Starting new features, need to refine ideas, exploring design options, want Socratic dialogue to clarify requirements.
**WHEN NOT:** Implementation already decided, simple changes, bug fixes.
**Invoke:** Skill tool with `skill="brainstorming"`

### writing-plans
**WHEN:** Complex multi-step implementations, need detailed task breakdown, preparing for execution phase.
**WHEN NOT:** Simple changes, research tasks, brainstorming phase (use brainstorming first).
**Invoke:** Skill tool with `skill="writing-plans"`

### executing-plans
**WHEN:** Have a written plan file to execute, need human checkpoints between batches, executing plans created by writing-plans.
**WHEN NOT:** Same-session execution, no plan exists yet, design phase.
**Invoke:** Skill tool with `skill="executing-plans"`

### finishing-a-development-branch
**WHEN:** Implementation complete, tests pass, ready to integrate work. Presents options: merge, PR, keep, discard.
**WHEN NOT:** Tests still failing, implementation incomplete, still debugging.
**Invoke:** Skill tool with `skill="finishing-a-development-branch"`

### using-git-worktrees
**WHEN:** Starting feature work needing isolation, before executing implementation plans, working on multiple branches simultaneously.
**WHEN NOT:** Simple single-branch work, quick fixes on current branch.
**Invoke:** Skill tool with `skill="using-git-worktrees"`

### dispatching-parallel-agents
**WHEN:** Facing 2+ independent tasks without shared state, multiple test file failures, different subsystems broken.
**WHEN NOT:** Related failures, need full system state, agents would interfere with each other.
**Invoke:** Skill tool with `skill="dispatching-parallel-agents"`

### sql-optimization-patterns
**WHEN:** Debugging slow queries, analyzing EXPLAIN plans, designing indexes, fixing N+1 problems, optimizing pagination.
**WHEN NOT:** ORM-specific patterns (use framework skills), application-level caching, database migrations.
**Invoke:** Skill tool with `skill="sql-optimization-patterns"`

### subagent-driven-development
**WHEN:** Complex implementations benefiting from two-stage review per task with fresh subagents.
**WHEN NOT:** Simple tasks, same-session work without review needs.
**Invoke:** Skill tool with `skill="subagent-driven-development"`

### verification-before-completion
**WHEN:** Before marking any task complete, need evidence-based verification checklist.
**WHEN NOT:** Trivial changes, already verified manually.
**Invoke:** Skill tool with `skill="verification-before-completion"`

### receiving-code-review
**WHEN:** Received code review feedback, need guidance on responding to reviewers.
**WHEN NOT:** Giving review (use requesting-code-review), implementation phase.
**Invoke:** Skill tool with `skill="receiving-code-review"`

### requesting-code-review
**WHEN:** About to request code review, need pre-review checklist.
**WHEN NOT:** Receiving feedback (use receiving-code-review), implementation incomplete.
**Invoke:** Skill tool with `skill="requesting-code-review"`

## Category: php

### php-docstring
**WHEN:** Writing DocBlocks for PHP classes/methods/functions/properties, documenting @param/@return/@throws, type annotations in PHPDoc.
**WHEN NOT:** Python docstrings, JavaScript/TypeScript docs, runtime logic.
**Invoke:** Skill tool with `skill="php-docstring"`

## Category: symfony

### php-symfony-api-platform-filters
**WHEN:** Adding filters to API Platform resources, creating custom filter classes, configuring filter properties, indexing filtered columns.
**WHEN NOT:** Laravel APIs, API security, serialization.
**Invoke:** Skill tool with `skill="php-symfony-api-platform-filters"`

### php-symfony-api-platform-resources
**WHEN:** Configuring API Platform resources, defining operations, pagination settings, custom URIs.
**WHEN NOT:** Filters (use filters skill), serialization (use serialization skill), security (use security skill).
**Invoke:** Skill tool with `skill="php-symfony-api-platform-resources"`

### php-symfony-api-platform-security
**WHEN:** Adding security to API operations, writing security expressions, creating custom voters, implementing role-based access.
**WHEN NOT:** General Symfony security, API filters, serialization.
**Invoke:** Skill tool with `skill="php-symfony-api-platform-security"`

### php-symfony-api-platform-serialization
**WHEN:** Configuring serialization groups, creating custom normalizers, implementing computed fields, role-based serialization.
**WHEN NOT:** API security, filters, resource configuration.
**Invoke:** Skill tool with `skill="php-symfony-api-platform-serialization"`

### php-symfony-api-platform-state-providers
**WHEN:** Creating custom state providers, implementing state processors, fetching data from non-Doctrine sources, custom persistence logic.
**WHEN NOT:** Standard Doctrine resources, database optimization.
**Invoke:** Skill tool with `skill="php-symfony-api-platform-state-providers"`

### php-symfony-doctrine-batch-processing
**WHEN:** Processing thousands/millions of records, batch updates/inserts, clearing EntityManager periodically, managing memory in long-running scripts.
**WHEN NOT:** Simple CRUD operations, query optimization, migrations.
**Invoke:** Skill tool with `skill="php-symfony-doctrine-batch-processing"`

### php-symfony-doctrine-fetch-modes
**WHEN:** Fixing N+1 queries, configuring eager/lazy loading, using EXTRA_LAZY collections, optimizing query performance.
**WHEN NOT:** Batch processing large datasets, migrations.
**Invoke:** Skill tool with `skill="php-symfony-doctrine-fetch-modes"`

### php-symfony-doctrine-migrations
**WHEN:** Creating migrations, running migrations, handling rollbacks, production deployment strategies, schema validation.
**WHEN NOT:** Query optimization, batch processing, Laravel migrations.
**Invoke:** Skill tool with `skill="php-symfony-doctrine-migrations"`

## Category: laravel

### php-laravel-specialist
**WHEN:** Building Laravel applications, using Eloquent models/relationships, implementing queues/jobs, creating API resources, Laravel Sanctum/Passport auth.
**WHEN NOT:** Symfony applications, plain PHP without Laravel, frontend-only development.
**Invoke:** Skill tool with `skill="php-laravel-specialist"`

## Category: python

### python-async-patterns
**WHEN:** Building async Python code, using asyncio, concurrent programming patterns.
**WHEN NOT:** Sync-only code, non-Python async.
**Invoke:** Skill tool with `skill="python-async-patterns"`

### python-backend
**WHEN:** Building Python APIs with FastAPI, Django, or Flask.
**WHEN NOT:** Frontend code, non-Python backends.
**Invoke:** Skill tool with `skill="python-backend"`

### python-data-transform
**WHEN:** Manipulating DataFrames, cleaning datasets, reshaping data, merging/joining tables, CSV/Excel processing.
**WHEN NOT:** Creating Excel files with formatting (use python-xlsx), building APIs.
**Invoke:** Skill tool with `skill="python-data-transform"`

### python-docstring
**WHEN:** Writing docstrings for Python functions/classes/modules, choosing docstring format (Google, NumPy, Sphinx).
**WHEN NOT:** JavaScript/TypeScript/PHP documentation.
**Invoke:** Skill tool with `skill="python-docstring"`

### python-docx
**WHEN:** Creating .docx files, editing Word documents, working with tracked changes, adding comments.
**WHEN NOT:** PDF files (use python-pdf), Excel/spreadsheets (use python-xlsx).
**Invoke:** Skill tool with `skill="python-docx"`

### python-packaging
**WHEN:** Packaging Python libraries, creating pyproject.toml/setup.py, building CLI tools, publishing to PyPI.
**WHEN NOT:** Managing dependencies (use python-uv-package-manager), writing application code.
**Invoke:** Skill tool with `skill="python-packaging"`

### python-pdf
**WHEN:** Creating PDF files, reading PDFs, extracting text from PDFs.
**WHEN NOT:** Word documents (use python-docx), Excel (use python-xlsx).
**Invoke:** Skill tool with `skill="python-pdf"`

### python-performance-optimization
**WHEN:** Profiling Python code, optimizing performance, identifying bottlenecks.
**WHEN NOT:** General debugging (use systematic-debugging).
**Invoke:** Skill tool with `skill="python-performance-optimization"`

### python-testing-patterns
**WHEN:** Writing pytest tests, creating fixtures, mocking with unittest.mock/pytest-mock, implementing TDD, setting up test configuration.
**WHEN NOT:** JavaScript tests, PHP tests, running existing tests without modification.
**Invoke:** Skill tool with `skill="python-testing-patterns"`

### python-uv-package-manager
**WHEN:** Installing packages with uv, creating virtual environments, managing dependencies with uv.lock.
**WHEN NOT:** Packaging libraries for distribution (use python-packaging), using pip/poetry/pipenv.
**Invoke:** Skill tool with `skill="python-uv-package-manager"`

### python-xlsx
**WHEN:** Creating Excel files with formulas/formatting, reading .xlsx/.xlsm files, modifying spreadsheets, adding charts to Excel.
**WHEN NOT:** Simple CSV reading (use pandas), Word documents (use python-docx), PDF files (use python-pdf).
**Invoke:** Skill tool with `skill="python-xlsx"`

## Category: js

### js-dev
**WHEN:** Writing JavaScript code, using ES6+ features, async/await patterns, array methods, module imports/exports.
**WHEN NOT:** TypeScript code (use ts-dev), Vue-specific patterns (use vuejs-dev).
**Invoke:** Skill tool with `skill="js-dev"`

### js-docstring
**WHEN:** Writing JSDoc comments, documenting JavaScript functions/classes/modules, generating API docs with JSDoc.
**WHEN NOT:** TypeScript code (use ts-docstring), Python, PHP.
**Invoke:** Skill tool with `skill="js-docstring"`

## Category: ts

### ts-dev
**WHEN:** Writing .ts/.tsx files, defining interfaces/types, using generics, implementing type guards, configuring tsconfig.json.
**WHEN NOT:** Plain JavaScript (use js-dev), Python/PHP backend code.
**Invoke:** Skill tool with `skill="ts-dev"`

### ts-docstring
**WHEN:** Writing TSDoc comments, documenting TypeScript functions/classes/interfaces/types, generating docs with TypeDoc.
**WHEN NOT:** JavaScript code (use js-docstring), Python, PHP.
**Invoke:** Skill tool with `skill="ts-docstring"`

## Category: html

### html-dev
**WHEN:** Writing semantic HTML, implementing ARIA accessibility, creating forms/tables, adding SEO meta tags.
**WHEN NOT:** CSS styling (use tailwind-css-dev), JavaScript logic (use js-dev), Vue-specific patterns (use vuejs-dev).
**Invoke:** Skill tool with `skill="html-dev"`

## Category: tailwind

### tailwind-css-dev
**WHEN:** Styling with Tailwind classes, implementing flex/grid layouts, responsive breakpoints, dark mode variants, animations.
**WHEN NOT:** Plain CSS/SCSS, CSS-in-JS solutions, HTML structure (use html-dev).
**Invoke:** Skill tool with `skill="tailwind-css-dev"`

### frontend-design
**WHEN:** Building production-grade UI components, design system implementation.
**WHEN NOT:** Backend code, API design.
**Invoke:** Skill tool with `skill="frontend-design"`

## Category: vue

### vuejs-dev
**WHEN:** Creating .vue components, using Composition API (ref, reactive, computed), props/emits, slots, composables, Vue Router, Pinia.
**WHEN NOT:** React development, plain HTML/JS, ApexCharts (use vuejs-apex-charts), Shadcn (use vuejs-shadcn).
**Invoke:** Skill tool with `skill="vuejs-dev"`

### vuejs-apex-charts
**WHEN:** Creating charts in Vue 3, building dashboards, real-time chart updates, integrating API data with charts.
**WHEN NOT:** Non-Vue projects, other chart libraries, general Vue development.
**Invoke:** Skill tool with `skill="vuejs-apex-charts"`

### vuejs-shadcn
**WHEN:** Using shadcn-vue components, installing components via CLI, theming/dark mode, forms with VeeValidate/Zod.
**WHEN NOT:** Other UI libraries (Vuetify, PrimeVue), general Vue development, charts.
**Invoke:** Skill tool with `skill="vuejs-shadcn"`

## Category: claude

### claude-agent-creator
**WHEN:** Creating new Claude Code agents, defining agent behavior and prompts.
**WHEN NOT:** Creating skills (use claude-skill-creator), creating commands (use claude-command-development).
**Invoke:** Skill tool with `skill="claude-agent-creator"`

### claude-command-development
**WHEN:** Creating new slash commands, defining command arguments, configuring command frontmatter.
**WHEN NOT:** Creating agents, creating skills, using existing commands.
**Invoke:** Skill tool with `skill="claude-command-development"`

### claude-hook-development
**WHEN:** Creating hooks to validate tool use, block dangerous commands, add context to operations, configure hook events.
**WHEN NOT:** Creating agents, creating commands, writing hookify rules (use claude-hookify-rules).
**Invoke:** Skill tool with `skill="claude-hook-development"`

### claude-hookify-rules
**WHEN:** Writing hookify rule patterns for automating hook behavior.
**WHEN NOT:** Creating hooks directly (use claude-hook-development).
**Invoke:** Skill tool with `skill="claude-hookify-rules"`

### claude-plugin-settings
**WHEN:** Storing plugin configuration, creating user-configurable settings, reading/writing .local.md files.
**WHEN NOT:** Creating plugin structure, creating agents/commands/hooks.
**Invoke:** Skill tool with `skill="claude-plugin-settings"`

### claude-plugin-structure
**WHEN:** Creating new plugins, setting up plugin directory layout, configuring plugin.json.
**WHEN NOT:** Configuring plugin settings, creating individual components.
**Invoke:** Skill tool with `skill="claude-plugin-structure"`

### claude-skill-creator
**WHEN:** Creating new Claude Code skills, defining skill content and metadata.
**WHEN NOT:** Creating agents (use claude-agent-creator), creating commands.
**Invoke:** Skill tool with `skill="claude-skill-creator"`

### claude-skill-development
**WHEN:** Learning skill development patterns, improving skill descriptions, organizing skill content.
**WHEN NOT:** Creating new skills from scratch (use claude-skill-creator).
**Invoke:** Skill tool with `skill="claude-skill-development"`

## Category: mcp

### mcp-builder
**WHEN:** Building MCP servers, implementing MCP protocol handlers.
**WHEN NOT:** Using existing MCP servers (use mcp-integration).
**Invoke:** Skill tool with `skill="mcp-builder"`

### mcp-integration
**WHEN:** Integrating existing MCP servers, configuring MCP connections.
**WHEN NOT:** Building new MCP servers (use mcp-builder).
**Invoke:** Skill tool with `skill="mcp-integration"`

---
name: plan-migration
description: Plan framework/language version upgrades and identify breaking changes with migration strategies
user_invocable: true
---

# Plan Migration Command

Launches the migration-planner agent to create comprehensive upgrade strategies for languages, frameworks, and major version changes.

## Usage

```bash
/plan-migration [upgrade_description]
```

## Examples

```bash
# Language version upgrade
/plan-migration "Python 3.8 to 3.12"

# Framework upgrade
/plan-migration "React 17 to 18"

# Multiple version jump
/plan-migration "Django 3.2 to 5.0"

# General upgrade request
/plan-migration "upgrade to latest PHP version"

# Database migration
/plan-migration "PostgreSQL 12 to 16"

# Just ask for migration planning
/plan-migration
```

## What It Does

1. Assesses current versions in use
2. Researches target version breaking changes
3. Identifies affected code in your project
4. Creates phase-by-phase migration plan
5. Provides risk assessment
6. Shows exact commands to execute
7. Suggests testing strategy
8. Includes rollback procedures

## Migration Planning Includes

### Current State Analysis
- Version detection
- Dependency inventory
- Test coverage assessment
- Risk factors

### Breaking Changes Inventory
- Removed/changed APIs
- Deprecated features
- New features available
- Performance improvements

### Migration Strategy
- Phase-by-phase plan
- Incremental vs big bang approach
- Code changes required
- Testing checkpoints
- Rollback procedures

### Risk Assessment
- High/medium/low risk rating
- Specific risks identified
- Mitigation strategies
- Safe upgrade path

## Supported Migrations

### Languages
- Python 2→3, Python 3.x→3.y
- Node.js version upgrades
- PHP 7.x→8.x
- Ruby version upgrades
- Java version upgrades
- Go version upgrades

### Frameworks
- React, Vue, Angular
- Django, Flask, FastAPI
- Symfony, Laravel
- Rails
- Spring Boot
- And more...

### Databases
- PostgreSQL
- MySQL/MariaDB
- MongoDB
- Redis

## Output Includes

- Current state analysis
- Target version overview with benefits
- Complete breaking changes inventory
- Affected code locations
- Step-by-step migration plan
- Commands to execute
- Testing strategy
- Risk assessment with mitigations
- Estimated effort (not time estimates)

## Migration Strategies

- **Incremental**: Upgrade one version at a time (safest)
- **Branch by Abstraction**: Create abstraction layer
- **Parallel Running**: Run old and new simultaneously
- **Strangler Pattern**: Gradually migrate features
- **Big Bang**: All at once (last resort)

## When to Use

- Planning major version upgrades
- Framework migration projects
- Language version updates
- Before modernization efforts
- When dependencies require newer versions
- Security patches require upgrades

---

When this command is invoked, create a comprehensive migration plan following the strategy above. If the user specified the migration (e.g., "Python 3.8 to 3.12"), start planning immediately. If not, ask what they want to migrate.

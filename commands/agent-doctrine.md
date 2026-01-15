---
name: agent-doctrine
description: Work with Doctrine ORM migrations, queries, batch processing, and performance optimization
user_invocable: true
---

# Doctrine Command

Launches the doctrine-specialist agent to work with Doctrine ORM.

## Usage

```bash
/doctrine [task_description]
```

## Examples

```bash
# Create a migration
/doctrine "add a status column to the orders table"

# Fix N+1 query issues
/doctrine "optimize the user list query that's causing N+1 problems"

# Set up eager loading
/doctrine "add eager loading for Order with Customer and Items relationships"

# Batch process records
/doctrine "update 100k records without running out of memory"

# Optimize a query
/doctrine "improve the performance of the product search query"

# General Doctrine work
/doctrine
```

## What It Does

1. Creates database migrations with proper up/down methods
2. Optimizes queries with eager loading and fetch modes
3. Implements batch processing for large datasets
4. Designs entity relationships and mappings
5. Troubleshoots N+1 queries and performance issues

## Capabilities

### Migrations
- Schema changes with rollback support
- Index management
- Data migrations
- Version management

### Query Optimization
- Eager loading with JOINs
- Fetch mode configuration
- DQL and QueryBuilder optimization
- Index recommendations

### Batch Processing
- Memory-efficient iteration with toIterable()
- Batch flush and clear patterns
- Progress tracking for long operations

### Entity Design
- Relationship mapping (OneToMany, ManyToMany, etc.)
- Cascade configuration
- Lifecycle callbacks

## When to Use

- Creating database migrations
- Fixing N+1 query problems
- Implementing eager loading
- Batch processing large datasets
- Optimizing DQL/QueryBuilder queries

---

When this command is invoked, work on the Doctrine task. Check composer.json for Doctrine version, review existing migrations in migrations/, and examine entity mappings in src/Entity/ before making changes.

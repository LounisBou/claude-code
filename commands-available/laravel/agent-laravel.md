---
name: agent-laravel
description: Work with Laravel applications, Eloquent models, queues, and authentication
user_invocable: true
---

# Laravel Command

Launches the laravel-developer agent to work with Laravel applications.

## Usage

```bash
/laravel [task_description]
```

## Examples

```bash
# Create Eloquent models
/laravel "create Order model with User and Product relationships"

# Build API endpoints
/laravel "create a REST API for managing products with authentication"

# Set up queued jobs
/laravel "process uploaded CSV files in the background"

# Optimize queries
/laravel "fix N+1 query issue on the orders page"

# Configure authentication
/laravel "set up Sanctum API authentication"

# General Laravel work
/laravel
```

## What It Does

1. Builds Laravel applications with elegant, maintainable code
2. Designs Eloquent models with proper relationships and scopes
3. Implements APIs with resources, authentication, and rate limiting
4. Configures queues, jobs, and background processing
5. Optimizes performance with caching, eager loading, and indexing

## Capabilities

### Eloquent ORM
- Model relationships (hasMany, belongsTo, morphTo, etc.)
- Query scopes and accessors/mutators
- Eager loading optimization
- Model events and observers

### API Development
- API Resources for response transformation
- Form Requests for validation
- Rate limiting and throttling
- API versioning

### Authentication
- Laravel Sanctum for SPA/mobile
- Laravel Passport for OAuth2
- Custom guards and providers

### Background Processing
- Queued jobs with retry logic
- Job batching and chaining
- Failed job handling
- Horizon for queue monitoring

## When to Use

- Working with Laravel applications
- Creating Eloquent models and relationships
- Building Laravel APIs
- Setting up queues and jobs
- Configuring Sanctum/Passport authentication

---

When this command is invoked, work on the Laravel task. Check composer.json for Laravel version, review config/ for application settings, and examine existing models in app/Models/ before making changes.

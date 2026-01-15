---
name: agent-api-platform
description: Work with Symfony API Platform resources, filters, serialization, and security
user_invocable: true
---

# API Platform Command

Launches the api-platform-architect agent to work with Symfony API Platform.

## Usage

```bash
/api-platform [task_description]
```

## Examples

```bash
# Configure a new API resource
/api-platform "create a Product resource with CRUD operations"

# Add filters to a resource
/api-platform "add search and date filters to the Order resource"

# Configure serialization groups
/api-platform "set up different output for admin vs regular users on User resource"

# Secure API operations
/api-platform "add security expressions to protect the Invoice endpoints"

# Create a state provider
/api-platform "implement a custom state provider for aggregated statistics"

# General API Platform work
/api-platform
```

## What It Does

1. Configures API resources with operations, pagination, and filtering
2. Implements custom filters (SearchFilter, DateFilter, custom filters)
3. Sets up serialization groups and custom normalizers
4. Secures APIs with security expressions and voters
5. Creates state providers and processors for custom logic
6. Optimizes API performance with proper indexing

## Capabilities

### Resource Configuration
- PHP 8+ attributes for resource definition
- Operation customization (GET, POST, PUT, DELETE)
- Pagination configuration
- Custom routes and URIs

### Filtering
- Built-in filters (Search, Date, Range, Boolean, Order)
- Custom filter implementation
- Filter property configuration

### Serialization
- Groups for read/write separation
- Context-aware normalization
- Role-based field visibility

### Security
- Operation-level security expressions
- Custom voters for complex authorization
- Object-level permissions

## When to Use

- Working with Symfony API Platform
- Configuring API resources and operations
- Implementing filters and serialization groups
- Setting up API security
- Creating state providers/processors

---

When this command is invoked, work on the API Platform task. Check composer.json for API Platform version, look for existing resources in src/Entity/ or src/ApiResource/, and examine existing filters in src/Filter/ before making changes.

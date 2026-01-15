---
name: agent-python-api
description: Build Python REST APIs with FastAPI, Django, or Flask including Pydantic models and authentication
user_invocable: true
---

# Python API Command

Launches the python-api-developer agent to work with Python backend APIs.

## Usage

```bash
/python-api [task_description]
```

## Examples

```bash
# Create FastAPI endpoints
/python-api "create a user registration endpoint with email validation"

# Set up database models
/python-api "design SQLAlchemy models for a product catalog"

# Implement authentication
/python-api "add JWT authentication to the API"

# Configure background tasks
/python-api "set up Celery for processing file uploads"

# Build Django API
/python-api "create Django REST Framework viewsets for orders"

# General Python API work
/python-api
```

## What It Does

1. Builds APIs with FastAPI, Django, or Flask
2. Designs database models with SQLAlchemy or Django ORM
3. Implements authentication with JWT, OAuth2, or session-based auth
4. Processes data with pandas, numpy for ETL and analysis
5. Configures background tasks with Celery or async queues

## Capabilities

### FastAPI
- Pydantic models for validation
- Dependency injection
- OpenAPI documentation
- Async endpoint handlers

### Database Integration
- SQLAlchemy async setup
- Django ORM patterns
- Migration management
- Connection pooling

### Authentication
- JWT token creation/validation
- OAuth2 with password flow
- API key authentication
- Role-based access control

### Background Processing
- Celery task configuration
- Retry and failure handling
- Task routing and priorities

## When to Use

- Building Python REST APIs
- Creating FastAPI endpoints
- Setting up Pydantic models
- Configuring SQLAlchemy
- Implementing JWT authentication
- Working with Django/Flask APIs

---

When this command is invoked, work on the Python API task. Check pyproject.toml or requirements.txt for the framework (FastAPI, Django, Flask), review existing API structure in app/ or src/, and identify the database setup before making changes.

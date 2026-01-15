---
name: agent-async-api
description: Build Python async APIs with concurrent patterns, rate limiting, and producer-consumer queues
user_invocable: true
---

# Async API Command

Launches the async-api-specialist agent to work with Python asyncio and async APIs.

## Usage

```bash
/async-api [task_description]
```

## Examples

```bash
# Concurrent API calls
/async-api "fetch data from 10 external APIs concurrently"

# Rate limiting
/async-api "limit external API calls to 5 concurrent requests"

# Producer-consumer pattern
/async-api "create a queue-based system for processing uploaded files"

# Async database operations
/async-api "set up async PostgreSQL with SQLAlchemy"

# WebSocket handling
/async-api "implement a WebSocket endpoint for real-time updates"

# General async work
/async-api
```

## What It Does

1. Designs async APIs with FastAPI, aiohttp, or Starlette
2. Implements concurrent I/O operations with proper error handling
3. Optimizes performance with connection pools and batching
4. Builds producer-consumer patterns with async queues
5. Configures rate limiting and throttling with semaphores

## Capabilities

### Concurrent Operations
- asyncio.gather for parallel tasks
- Error handling with return_exceptions
- Task cancellation and cleanup
- Timeout configuration

### Rate Limiting
- Semaphore-based concurrency limits
- Token bucket patterns
- Backpressure handling

### Producer-Consumer
- asyncio.Queue patterns
- Multiple consumer workers
- Graceful shutdown

### Database Integration
- Async SQLAlchemy sessions
- Connection pool management
- asyncpg, motor, aioredis

## When to Use

- Building async Python APIs
- Concurrent external API calls
- Rate limiting and throttling
- Producer-consumer patterns
- Async database sessions

---

When this command is invoked, work on the async Python task. Check pyproject.toml or requirements.txt for async libraries (aiohttp, asyncpg, etc.), and look for existing async patterns in the codebase before making changes.

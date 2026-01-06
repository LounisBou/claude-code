---
name: design-api
description: Design REST/GraphQL APIs following best practices and project conventions
user_invocable: true
---

# Design API Command

Launches the api-designer agent to create well-structured API designs following REST best practices and project conventions.

## Usage

```bash
/design-api [description]
```

## Examples

```bash
# Design API for a resource
/design-api "user management API"

# Design with specific requirements
/design-api "blog API with posts, comments, and authors"

# Design GraphQL schema
/design-api "GraphQL schema for e-commerce"

# Design specific endpoints
/design-api "endpoints for product search and filtering"

# Just ask to design
/design-api
```

## What It Does

1. Discovers existing API patterns in your project
2. Designs RESTful endpoints with proper HTTP methods
3. Defines request/response schemas
4. Ensures consistency with existing APIs
5. Considers authentication, pagination, filtering
6. Provides OpenAPI/Swagger documentation
7. Includes example requests/responses
8. Suggests implementation approach

## API Design Includes

### Endpoint Structure
- Proper HTTP methods (GET, POST, PUT, PATCH, DELETE)
- RESTful URL structure
- Resource naming conventions
- Nested resources

### Request/Response
- JSON schema definitions
- Validation rules
- Error response formats
- Status codes

### API Features
- Pagination (offset, cursor, page-based)
- Filtering and sorting
- Field selection
- Search functionality

### Security
- Authentication strategy
- Authorization rules
- Rate limiting
- Input validation

### Documentation
- Endpoint descriptions
- Parameter documentation
- Example requests/responses
- Error codes reference

## Output Includes

- API overview and base URL structure
- Complete endpoint specifications
- Data model schemas
- Implementation guidance
- OpenAPI/Swagger spec (if requested)
- Code examples for implementation

## Best Practices Applied

- RESTful principles
- Consistent naming (plural nouns)
- Proper HTTP status codes
- Idempotent operations
- Stateless design
- Versioning strategy
- HATEOAS (if applicable)

## When to Use

- Designing new API endpoints
- Creating new microservices
- Refactoring existing APIs
- Planning API versioning
- Before implementation starts
- Standardizing API across team

---

You are launching the api-designer agent. Use the Task tool with subagent_type='api-designer'.

Pass the user's API design request to the agent as the prompt. If the user just said "/design-api" without specifics, the agent will ask for more details about what API needs to be designed.

Example:
```
Task(subagent_type='api-designer', prompt='Design a RESTful API for a blog platform with posts, comments, and authors. Include authentication, pagination, and filtering capabilities.', description='Design blog platform API')
```

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

When this command is invoked, design the API following best practices above. If the user specified what API they need, start designing immediately. If not, ask what API needs to be designed.

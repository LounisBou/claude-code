---
name: agent-generate-docs
description: Generate technical documentation, README files, and API docs from code
user_invocable: true
---

# Generate Documentation Command

Launches the documentation-generator agent to create comprehensive documentation from your code.

## Usage

```bash
/generate-docs [documentation_type]
```

## Examples

```bash
# Generate README
/generate-docs "README for this project"

# Generate API documentation
/generate-docs "API documentation"

# Generate docstrings
/generate-docs "add docstrings to the UserService class"

# Generate architecture docs
/generate-docs "architecture documentation"

# Generate full documentation
/generate-docs "complete project documentation"

# Just ask for docs
/generate-docs
```

## What It Does

1. Analyzes project structure and code
2. Extracts information from existing code
3. Discovers project patterns and conventions
4. Generates clear, comprehensive documentation
5. Includes working code examples
6. Creates proper markdown formatting
7. Follows documentation best practices

## Documentation Types

### README.md
- Project description
- Installation instructions
- Quick start guide
- Usage examples
- Configuration options
- Development setup
- Contributing guidelines

### API Documentation
- Endpoint specifications
- Request/response schemas
- Authentication details
- Error codes
- Rate limiting
- Example requests

### Code Documentation
- Function/method docstrings
- Class documentation
- Module descriptions
- Type annotations
- Usage examples

### Architecture Documentation
- System overview
- Component relationships
- Data flow diagrams
- Technology stack
- Design decisions

### User Guides
- How-to guides
- Tutorials
- Troubleshooting
- FAQ

## Output Includes

- Well-structured markdown
- Working code examples
- Clear installation steps
- Configuration details
- Usage examples
- Proper formatting
- Links and references

## Documentation Standards

- **Clarity**: Easy to understand for target audience
- **Completeness**: All public APIs documented
- **Accuracy**: Examples actually work
- **Consistency**: Same style throughout
- **Maintainability**: Easy to update

## Language-Specific Formats

### Python
- Google/NumPy/Sphinx docstring formats
- Type hints documentation
- Sphinx/MkDocs generation

### JavaScript/TypeScript
- JSDoc comments
- TypeDoc generation
- API documentation

### PHP
- PHPDoc comments
- phpDocumentor generation
- API Platform documentation

### Go
- godoc format
- Package documentation

### Rust
- rustdoc format
- Markdown in doc comments

## When to Use

- Starting a new project
- Before release/deployment
- When onboarding new developers
- After major feature additions
- Updating outdated documentation
- Creating public-facing documentation

## Important Note

This command only generates documentation when explicitly requested. It will never create documentation proactively.

---

When this command is invoked, generate documentation following the guidelines above. If the user specified what documentation they want, start generating immediately. If not, ask what type of documentation they need.

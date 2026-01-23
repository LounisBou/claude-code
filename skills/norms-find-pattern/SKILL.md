---
name: norms-find-pattern
description: |
  Find and analyze existing code patterns in the project for a specific file type.
  WHEN: Use before implementing new features to discover established patterns. Invoke with "/norms:find-pattern [type]".
  WHEN NOT: After implementation - use "/norms:check" instead to validate code.
---

# Find Pattern Examples

## Purpose

Quickly find and analyze existing code patterns in the project for a specific type of file or feature. This is a **pre-implementation** skill that helps you understand how similar code is structured before writing new code.

This skill works with any project type by auto-detecting the technology stack.

## Usage

```
/norms:find-pattern [type] [optional: feature]
```

---

## STEP 0: Project Type Detection

**Auto-detect the project type by checking for these indicators:**

| Indicator File | Project Type | Common Extensions |
|----------------|--------------|-------------------|
| `package.json` | JavaScript/TypeScript | `.js`, `.ts`, `.jsx`, `.tsx` |
| `composer.json` | PHP | `.php` |
| `requirements.txt` / `pyproject.toml` / `setup.py` | Python | `.py` |
| `Cargo.toml` | Rust | `.rs` |
| `go.mod` | Go | `.go` |
| `Gemfile` | Ruby | `.rb` |
| `pom.xml` / `build.gradle` | Java/Kotlin | `.java`, `.kt` |
| `*.csproj` / `*.sln` | C#/.NET | `.cs` |
| `mix.exs` | Elixir | `.ex`, `.exs` |

**Run detection:**

```bash
# Check for project type indicators
ls -la package.json composer.json requirements.txt pyproject.toml Cargo.toml go.mod Gemfile pom.xml build.gradle mix.exs *.csproj 2>/dev/null || echo "Check subdirectories"
```

**Store detected project type for subsequent steps.**

---

## Supported Types (Generic)

These are generic file type categories that map to language-specific patterns:

| Generic Type | Description | Common Paths |
|--------------|-------------|--------------|
| `model` | Data structures, entities, domain objects | `*/models/*`, `*/entities/*`, `*/domain/*` |
| `controller` | Request handlers, API endpoints | `*/controllers/*`, `*/handlers/*`, `*/api/*` |
| `service` | Business logic, use cases | `*/services/*`, `*/use-cases/*`, `*/application/*` |
| `repository` | Data access, persistence | `*/repositories/*`, `*/dao/*`, `*/data/*` |
| `test` | Unit tests, integration tests | `*/test/*`, `*/tests/*`, `*_test.*`, `*.test.*`, `*.spec.*` |
| `utility` | Helper functions, utilities | `*/utils/*`, `*/helpers/*`, `*/lib/*` |
| `config` | Configuration files | `*/config/*`, `*.config.*` |
| `middleware` | Request/response processing | `*/middleware/*`, `*/interceptors/*` |
| `types` | Type definitions, interfaces | `*/types/*`, `*/interfaces/*`, `*.d.ts` |
| `security` | Authentication, authorization | `*/security/*`, `*/auth/*`, `*Voter*`, `*Guard*` |

### Language-Specific Type Mappings

**JavaScript/TypeScript:**
- `component` - React/Vue components: `*/components/*`
- `hook` - React hooks: `*/hooks/*`, `use*.ts`
- `store` - State management: `*/stores/*`, `*/state/*`
- `reducer` - Redux reducers: `*/reducers/*`

**PHP:**
- `entity` - Doctrine entities: `*/Entity/*`
- `voter` - Security voters: `*/Voter/*`, `*Voter.php`
- `extension` - API Platform extensions: `*/Extension/*`
- `command` - Console commands: `*/Command/*`

**Python:**
- `view` - Django/Flask views: `*/views/*`, `views.py`
- `serializer` - DRF serializers: `*/serializers/*`
- `manager` - Custom managers: `*_manager.py`
- `form` - Form classes: `*/forms/*`

**Go:**
- `handler` - HTTP handlers: `*_handler.go`
- `repository` - Data access: `*_repository.go`
- `middleware` - HTTP middleware: `*_middleware.go`

**Ruby:**
- `controller` - Rails controllers: `*/controllers/*`
- `model` - ActiveRecord models: `*/models/*`
- `concern` - Shared behaviors: `*/concerns/*`

---

## STEP 1: Parse the Request

Identify from user input:
1. **Type**: The file type category (e.g., `service`, `test`, `controller`)
2. **Feature** (optional): Specific feature to focus on (e.g., `api`, `auth`)

---

## STEP 2: Locate Example Files

Based on project type and requested type:

```bash
# Example: Find service files in a TypeScript project
find . -type f -name "*.ts" -path "*services*" | head -5

# Example: Find test files
find . -type f \( -name "*test*" -o -name "*spec*" \) | head -5

# Example: Find controller files in PHP
find . -type f -name "*Controller.php" | head -5
```

**Selection criteria:**
1. Match the requested type category
2. Prioritize recent, well-structured files
3. Select 3-5 diverse examples
4. Prefer files with good coverage of patterns

---

## STEP 3: Extract Key Patterns

For each example file, extract:

### Structural Patterns
- Import/require organization
- Class/function structure
- Module exports
- File organization

### Naming Conventions
- Class/function naming
- Variable naming style
- Constant naming
- Parameter naming

### Architectural Patterns
- Dependency handling (injection, imports)
- Interface/type usage
- Error handling approach
- Inheritance patterns

### Framework Patterns
- Decorators/attributes usage
- Annotations
- Configuration patterns
- Convention-based naming

### Method Signatures
- Key methods and their purposes
- Parameter patterns
- Return types
- Documentation style

---

## STEP 4: Present Findings

Format the output as follows:

```markdown
# Pattern Examples: [Type Name]

**Project Type**: [Detected type]
**Found**: X examples in `[primary path]`

## 1. [filename.ext]
**Purpose**: [One-line description]
**Location**: [Full path]

**Key Patterns**:
- Structure: [Class/function structure pattern]
- Dependencies: [How dependencies are handled]
- Methods: [Key method patterns]
- Conventions: [Notable conventions used]

**Code Sample**:
```[language]
[Most illustrative code snippet, 10-15 lines]
```

## 2. [Another file...]
[Same breakdown]

## Common Patterns Across All Examples:

### Structure
- [Pattern 1]
- [Pattern 2]

### Naming
- [Convention 1]
- [Convention 2]

### Dependencies
- [Pattern 1]
- [Pattern 2]

### Notable Patterns
- [Pattern with explanation]

## When to Use These Patterns:
- [Use case 1]
- [Use case 2]
- [Use case 3]

## Quick Reference

| Aspect | Pattern |
|--------|---------|
| File naming | [pattern] |
| Class naming | [pattern] |
| Method naming | [pattern] |
| Dependencies | [pattern] |
| Error handling | [pattern] |
```

---

## Execution Instructions

When invoked:

1. **Detect project type** using indicator files
2. **Parse the request** to identify type and optional feature
3. **Map to language-specific patterns** based on project type
4. **Locate example files**:
   - Use glob patterns appropriate for the type
   - Filter by project-specific paths
   - Select 3-5 diverse examples
5. **Extract key patterns** from each example:
   - Read each file
   - Identify structural patterns
   - Note naming conventions
   - Document framework-specific patterns
6. **Synthesize common patterns** across all examples
7. **Present findings** in the structured format above

---

## Examples

### Find service patterns
```
/norms:find-pattern service
```

### Find test patterns for API endpoints
```
/norms:find-pattern test api
```

### Find controller patterns
```
/norms:find-pattern controller
```

### Find model/entity patterns
```
/norms:find-pattern model
```

### Find security patterns
```
/norms:find-pattern security
```

---

## Relationship to Other Skills

| Skill | When to Use |
|-------|-------------|
| **norms:find-pattern** | BEFORE writing code - discover patterns |
| **norms:check** | AFTER writing code - validate compliance |

**Typical workflow:**
1. Use `/norms:find-pattern [type]` to understand existing patterns
2. Implement your new code following those patterns
3. Use `/norms:check` to validate your implementation

---

## Notes

- This skill is for **quick reference** during development
- Shows actual code snippets to help understand patterns
- Focuses on the most common and well-established patterns
- Works with any language/framework by auto-detecting project type
- If no examples exist for a type, suggest related types or create new patterns

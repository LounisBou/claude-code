---
name: find-pattern
description: Find and analyze existing code patterns in the project for a specific type or feature
user_invocable: true
---

# Find Pattern Examples

Quickly find and analyze existing code patterns in the project for a specific type of file or feature. **Works with any language** - automatically detects and finds patterns.

## Usage

```
/find-pattern [type] [optional: feature]
```

Examples:
- `/find-pattern model`
- `/find-pattern test api`
- `/find-pattern component user`
- `/find-pattern service authentication`

## Supported Types

### Universal (Any Language)

- `test` - Find test case examples
- `service` - Find service/business logic examples
- `helper` / `utility` - Find helper/utility function examples
- `config` - Find configuration file examples
- `middleware` - Find middleware examples

### Python

- `model` - Find data model examples (Django ORM, SQLAlchemy, Pydantic)
- `view` - Find view/endpoint examples (Django, Flask, FastAPI)
- `serializer` - Find serializer examples (DRF)
- `decorator` - Find decorator function examples
- `class` - Find class implementation examples
- `function` - Find function implementation examples
- `api-endpoint` - Find API endpoint implementation examples
- `form` - Find form examples

### JavaScript/TypeScript

- `component` - Find React/Vue component examples
- `hook` - Find React custom hooks
- `context` - Find React context providers
- `service` - Find API service modules
- `reducer` - Find Redux reducers
- `action` - Find Redux actions
- `store` - Find state management stores
- `route` - Find routing configuration
- `util` - Find utility functions

### PHP

- `entity` - Find Doctrine entity examples
- `controller` - Find controller class examples
- `repository` - Find repository examples
- `service` - Find service class examples
- `voter` - Find security voter examples (Symfony)
- `extension` - Find API Platform extension examples
- `middleware` - Find middleware examples

### Go

- `handler` - Find HTTP handler examples
- `service` - Find service implementation examples
- `model` / `struct` - Find struct definitions
- `repository` - Find data access examples
- `middleware` - Find middleware examples

### Rust

- `struct` - Find struct definitions
- `trait` - Find trait definitions
- `impl` - Find implementation blocks
- `module` - Find module organization examples

## What This Does

1. Automatically detects the project's language(s)
2. Locates 3-5 relevant example files of the specified type
3. Shows the file paths with context
4. Extracts and displays key patterns from each:
   - File structure and organization
   - Class/function/component signatures
   - Decorators/attributes/annotations usage
   - Common patterns and conventions
   - Dependencies and imports
   - Error handling approaches
5. Provides a quick reference for implementing similar code
6. Highlights common patterns across all examples

## Task Instructions

When this command is invoked:

1. **Parse the request** to identify the type and optional feature/domain

2. **Detect project language(s)**:
   - Check file extensions in the project
   - Identify the primary language(s) in use
   - Note any multi-language patterns (e.g., Python backend + React frontend)

3. **Locate example files**:
   - Use `Glob` to find files matching the type pattern
   - Filter by language/framework if detected
   - If feature specified, prioritize files related to that feature
   - Select 3-5 diverse, well-structured examples
   - Prioritize recently modified or commonly used files

4. **Extract key patterns** from each example:
   - File path and purpose
   - Class/function/component declaration
   - Constructor/initialization and dependencies
   - Key method/function signatures
   - Decorators, attributes, annotations
   - Import/dependency patterns
   - Error handling approach
   - Documentation style
   - Notable patterns or conventions
   - Testing patterns (if test files)

5. **Identify common patterns** across all examples:
   - What patterns appear in ALL examples?
   - What patterns appear in MOST examples?
   - Are there competing patterns? (mention both)
   - What conventions are clearly established?

6. **Present findings** in a clear, scannable format with code snippets

## Example Output

```markdown
# Pattern Examples: React Components

**Project detected**: TypeScript + React
**Found**: 5 component examples in `src/components/`

---

## 1. UserProfile.tsx
**Path**: `src/components/user/UserProfile.tsx`
**Purpose**: Display user profile information

**Key Patterns**:
- TypeScript functional component
- Props interface defined separately
- Custom hooks: `useUser()`, `useAuth()`
- Error boundaries with `ErrorBoundary` wrapper
- Styled with CSS modules

```typescript
interface UserProfileProps {
  userId: string;
  onEdit?: () => void;
}

export const UserProfile: React.FC<UserProfileProps> = ({ userId, onEdit }) => {
  const { user, loading, error } = useUser(userId);
  const { hasPermission } = useAuth();

  if (loading) return <Spinner />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <div className={styles.profile}>
      {/* component content */}
    </div>
  );
};
```

---

## 2. UserSettings.tsx
[Similar breakdown]

---

## Common Patterns Across All Components

✅ **TypeScript usage**: All components use TypeScript with explicit prop interfaces
✅ **Functional components**: No class components found
✅ **Custom hooks**: All use project-specific hooks (useUser, useAuth, useNotifications)
✅ **Error handling**: All use early returns for loading/error states
✅ **Styling**: 4 use CSS modules, 1 uses styled-components
✅ **Props**: All define Props interfaces separately from component
✅ **Exports**: All use named exports, not default exports

## When to Use These Patterns

- Creating new user-facing components
- Displaying data from API with loading/error states
- Implementing authentication-aware features
- Maintaining consistency with existing component library

## Variations Found

**Styling**: Project uses both CSS modules (preferred, 80%) and styled-components (legacy, 20%)
**Recommendation**: Use CSS modules for new components
```

## Examples

### Find model patterns
```
/find-pattern model
```

### Find test patterns for API functionality
```
/find-pattern test api
```

### Find React component patterns
```
/find-pattern component
```

### Find service patterns for authentication
```
/find-pattern service auth
```

## Notes

- This command is for **quick reference** during development
- For comprehensive analysis, use `/check-norms` instead
- Shows actual code snippets to help understand patterns
- Focuses on the most common and well-established patterns
- **Language agnostic** - works with any codebase
- Automatically adapts to your project's stack
- Identifies both universal patterns and competing approaches

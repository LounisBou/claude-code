# Find Pattern Examples

Quickly find and analyze existing code patterns in the project for a specific type of file or feature.

## Usage

```
/find-pattern [type] [optional: feature]
```

## Supported Types

- `entity` - Find entity examples with API Platform configuration
- `voter` - Find security voter examples
- `extension` - Find API Platform extension examples
- `test` - Find integration test examples
- `service` - Find service class examples
- `repository` - Find repository examples
- `action-handler` - Find alert action handler examples
- `expression` - Find alert expression examples

## What This Does

1. Locates 3-5 relevant example files of the specified type
2. Shows the file paths
3. Extracts and displays key patterns from each:
   - Class structure
   - Key methods and their signatures
   - Attribute/annotation usage
   - Common patterns and conventions
4. Provides a quick reference for implementing similar code

## Task Instructions

When this command is invoked:

1. **Parse the request** to identify the type and optional feature
2. **Locate example files**:
   - Use `find` or `Glob` to locate files of that type
   - Prioritize recent, well-structured files
   - Select 3-5 diverse examples
3. **Extract key patterns** from each example:
   - Class declaration and extends/implements
   - Constructor and dependencies
   - Key method signatures
   - Attributes and annotations
   - Notable patterns or conventions
4. **Present findings** in a clear, scannable format

## Example Output

```markdown
# Pattern Examples: Security Voters

Found 5 examples in `src/Core/Security/Voters/`:

## 1. AssignedDeviceModeVoter.php
**Purpose**: Controls access to AssignedDeviceMode resources
**Key Patterns**:
- Extends: `AbstractVoter<string, AssignedDeviceMode>`
- Constructor: Injects `Security` and `ManagerRegistry`
- Method: `getSupportedClass()` returns entity class
- Method: `isUserGranted()` - checks membership and grants
- Uses: `AssignedDeviceVisibilityPolicy` for automatic/manual access
- Queries: Fetches `AssignedDeviceGrant` via repository

```php
protected function isUserGranted(string $attribute, mixed $assignedDeviceMode, User $user): bool
{
    $account = $assignedDeviceMode->account;
    if (null === $account) {
        return false;
    }
    // ... grant checking logic
}
```

## 2. AssignedDeviceVoter.php
[Similar breakdown]

## Common Patterns Across All Voters:
✅ All extend `AbstractVoter`
✅ All implement `getSupportedClass()` and `isUserGranted()`
✅ Security checks through `Grant::isGranted()`
✅ PHPDoc type hints for generic types
✅ Early returns for null checks
✅ `@codeCoverageIgnore` on unreachable branches

## When to Use These Patterns:
- Creating new voters for API resources
- Implementing fine-grained access control
- Checking user permissions on entities
```

## Examples

### Find entity patterns
```
/find-pattern entity
```

### Find test patterns for API endpoints
```
/find-pattern test api
```

### Find voter patterns
```
/find-pattern voter
```

## Notes

- This command is for **quick reference** during development
- For comprehensive analysis, use `/check-norms` instead
- Shows actual code snippets to help understand patterns
- Focuses on the most common and well-established patterns

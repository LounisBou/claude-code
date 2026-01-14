---
name: inline-todo-planning
description: >
  Insert explicit, scoped TODO stubs directly into code files during feature preparation.
  Use when preparing features, analyzing missing functionality, or breaking down work.
  The codebase becomes the source of truth for pending work.
---

# Inline TODO Planning

## Core Philosophy

**The codebase is the planning document.** Instead of external plans, insert TODO comments exactly where work needs to happen. This ensures:
- Missing work lives where it belongs
- TODOs are discoverable via simple grep/search
- Implementation happens in context
- Plans stay small and focused

## TODO Format

Use a consistent, searchable format:

```
// TODO(feature-name): Brief description of what needs to be done
// TODO(auth): Validate JWT expiration before accepting token
// TODO(api): Add rate limiting middleware here
// TODO(ui): Wire up form submission to API endpoint
```

### Format Rules

1. **Prefix**: Always `TODO(scope):` where scope is the feature/area name
2. **Single line preferred**: Keep it concise but complete
3. **Action-oriented**: Start with a verb (Add, Implement, Validate, Wire, Extract...)
4. **Location-specific**: Place at the exact line where work happens

### Multi-line TODOs (when necessary)

```python
# TODO(payments): Implement Stripe webhook handler
#   - Verify webhook signature
#   - Handle payment_intent.succeeded event
#   - Update order status in database
#   - Send confirmation email
```

## Scoping Guidelines

### Good TODOs (Explicit & Scoped)

```typescript
// TODO(cart): Calculate shipping cost based on user.address.country
// TODO(cart): Apply discount code if cart.discountCode is set
// TODO(cart): Validate stock availability before checkout
```

### Bad TODOs (Vague & Unscoped)

```typescript
// TODO: fix this later
// TODO: needs work
// TODO: implement shipping
// TODO: handle edge cases
```

## Insertion Strategy

When preparing a feature, analyze the codebase and insert TODOs at these locations:

### 1. Entry Points
Where the feature starts executing:
```python
def create_order(request):
    # TODO(orders): Validate request payload against OrderSchema
    # TODO(orders): Check user has permission to create orders
    pass
```

### 2. Integration Points
Where new code connects to existing systems:
```python
class OrderService:
    def __init__(self, db, payment_gateway, notification_service):
        # TODO(orders): Inject InventoryService for stock checks
        pass
```

### 3. Data Flow Points
Where data transforms or moves between layers:
```python
def process_payment(order):
    # TODO(payments): Convert order.total to cents for Stripe
    # TODO(payments): Map order.currency to Stripe currency code
    pass
```

### 4. Missing Implementations
Where stubs or placeholders exist:
```python
def calculate_tax(order):
    # TODO(tax): Implement tax calculation by jurisdiction
    # TODO(tax): Handle tax-exempt customers
    return Decimal("0.00")  # Placeholder
```

### 5. Error Handling Gaps
Where errors need proper handling:
```python
try:
    response = api.charge(amount)
except Exception:
    # TODO(payments): Handle specific Stripe errors (card_declined, expired_card)
    # TODO(payments): Log payment failure for debugging
    raise
```

## Grouping TODOs Logically

Use the same scope prefix to group related work:

```python
# In auth/middleware.py
# TODO(auth): Extract user from JWT token

# In auth/decorators.py
# TODO(auth): Create @require_permission decorator

# In auth/models.py
# TODO(auth): Add permissions field to User model
```

All `TODO(auth):` items can be found and worked on together.

## Listing TODOs

Simple script to list all TODOs:

```bash
# List all TODOs
grep -rn "TODO(" --include="*.py" --include="*.ts" --include="*.js" .

# List TODOs for specific feature
grep -rn "TODO(auth):" .

# Count TODOs by feature
grep -roh "TODO([^)]*)" . | sort | uniq -c | sort -rn
```

## Workflow Integration

### When Preparing a Feature

1. **Analyze requirements** - Understand what needs to be built
2. **Identify touch points** - Find all files that need changes
3. **Insert TODOs** - Place explicit stubs at each location
4. **Review distribution** - Ensure TODOs are well-scoped (2-15 min each)
5. **Commit TODOs** - "Prepare feature-name: add implementation TODOs"

### When Implementing

1. **List TODOs** - `grep -rn "TODO(feature-name):" .`
2. **Pick a TODO** - Start with foundational ones
3. **Implement** - Write the code at that location
4. **Remove TODO** - Delete the comment once implemented
5. **Commit** - Small, focused commit for that TODO

## Size Guidelines

Each TODO should represent **2-15 minutes of focused work**. If larger:

```python
# Too big - break it down:
# TODO(orders): Implement entire checkout flow

# Better - specific steps:
# TODO(orders): Validate cart is not empty
# TODO(orders): Reserve inventory for cart items
# TODO(orders): Create pending order record
# TODO(orders): Initiate payment capture
# TODO(orders): Confirm order on successful payment
```

## Example: Preparing a User Preferences Feature

```python
# In models/user.py
class User:
    # TODO(prefs): Add preferences JSONField with default {}
    pass

# In api/preferences.py
# TODO(prefs): Create GET /preferences endpoint
# TODO(prefs): Create PATCH /preferences endpoint with merge semantics

# In services/preferences.py
def get_preferences(user_id: int) -> dict:
    # TODO(prefs): Fetch user preferences from database
    # TODO(prefs): Merge with default preferences
    return {}

def update_preferences(user_id: int, updates: dict) -> dict:
    # TODO(prefs): Validate updates against PreferencesSchema
    # TODO(prefs): Deep merge updates with existing preferences
    # TODO(prefs): Persist updated preferences
    return {}

# In tests/test_preferences.py
# TODO(prefs): Test get_preferences returns defaults for new user
# TODO(prefs): Test update_preferences merges correctly
# TODO(prefs): Test invalid preference keys are rejected
```

After inserting these, run:
```bash
grep -rn "TODO(prefs):" .
```

Output shows all work items, exactly where they belong.

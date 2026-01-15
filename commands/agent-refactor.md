---
name: agent-refactor
description: Identify code smells and propose refactoring strategies with trade-off analysis
user_invocable: true
---

# Refactor Command

Launches the refactoring-advisor agent to analyze code quality and propose improvements.

## Usage

```bash
/refactor [file_or_component_name]
```

## Examples

```bash
# Refactor specific file
/refactor src/services/order_processor.py

# Refactor a class
/refactor OrderProcessor

# Refactor a module
/refactor "the authentication module"

# General refactoring request
/refactor "this codebase has gotten messy"

# Just ask to refactor
/refactor
```

## What It Does

1. Identifies code smells and technical debt
2. Analyzes complexity, duplication, and coupling
3. Proposes specific refactoring strategies
4. Provides trade-off analysis (pros/cons/risks)
5. Prioritizes improvements by impact and effort
6. Shows before/after code examples
7. Suggests safe implementation steps

## Code Smells Detected

- Long functions/methods
- Deep nesting and complexity
- Duplicated code
- God classes (too many responsibilities)
- Poor naming
- Feature envy and inappropriate intimacy
- Switch statements that should be polymorphism
- And more...

## Refactoring Techniques

- Extract method/function
- Extract class
- Replace conditionals with polymorphism
- Introduce parameter objects
- Consolidate duplicate code
- Simplify complex conditionals
- Replace magic numbers with constants

## When to Use

- Code is hard to understand or maintain
- Before adding major new features
- Before major releases
- When test coverage is good (safe to refactor)
- Technical debt is slowing development

---

When this command is invoked, analyze the code and propose refactoring strategies. If the user specified what to refactor, start analyzing immediately. If not, ask what code they want refactored.

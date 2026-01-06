---
name: generate-docstring
description: Generate or improve docstrings for functions, methods, and classes following language-specific standards
user_invocable: true
---

# Generate Docstring Command

Launches the docstring-generator agent to create or improve documentation for your code following language-specific standards (PEP 257, PSR-5, JSDoc, TSDoc).

## Usage

```bash
/generate-docstring [file_or_function_name]
```

## Examples

```bash
# Generate docstring for a specific file
/generate-docstring src/services/user_service.py

# Generate docstring for a function
/generate-docstring calculateTotalPrice

# Generate docstring for a class
/generate-docstring AuthService

# Generate docstrings with context
/generate-docstring "the payment processing function"

# Just ask for docstrings
/generate-docstring
```

## What It Does

1. Reads and analyzes your code (function, method, class, or module)
2. Extracts information:
   - Parameters and their types
   - Return values
   - Exceptions that can be thrown
   - Code behavior and purpose
3. Detects the programming language automatically
4. Applies the appropriate documentation standard:
   - **Python**: PEP 257 (Google, NumPy, or Sphinx style)
   - **PHP**: PSR-5 and PSR-19 PHPDoc
   - **JavaScript**: JSDoc (jsdoc.app)
   - **TypeScript**: TSDoc (tsdoc.org)
5. Generates comprehensive, standards-compliant docstrings
6. Matches your project's existing documentation style

## Supported Languages

- Python (PEP 257, Google, NumPy, Sphinx styles)
- PHP (PSR-5, PSR-19 PHPDoc)
- JavaScript (JSDoc)
- TypeScript (TSDoc)

## What's Included in Generated Docstrings

**For Functions/Methods:**
- Brief summary
- Detailed description (when needed)
- Parameter descriptions
- Return value description
- Exceptions/errors documentation
- Usage examples (for complex functions)

**For Classes:**
- Class purpose and responsibility
- Attributes/properties
- Constructor parameters
- Usage examples
- Related classes or patterns

**For Modules:**
- Module purpose
- Key exports
- Usage examples
- Important constants

---

You are launching the docstring-generator agent. Use the Task tool with subagent_type='docstring-generator'.

Pass the user's request to the agent as the prompt. If the user provided a file name, function name, or class name, include that in the prompt. If they just said "/generate-docstring", ask them what they want to document.

Example:
```
Task(subagent_type='docstring-generator', prompt='Generate docstrings for the calculateTotalPrice function in src/utils/pricing.py', description='Generate docstring for calculateTotalPrice')
```

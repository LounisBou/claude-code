---
name: audit-deps
description: Audit dependencies for security vulnerabilities, outdated versions, and compatibility issues
user_invocable: true
---

# Audit Dependencies Command

Launches the dependency-auditor agent to scan dependencies for security vulnerabilities and outdated packages.

## Usage

```bash
/audit-deps [options]
```

## Examples

```bash
# Full dependency audit
/audit-deps

# Audit with focus
/audit-deps "check for security vulnerabilities"

# Audit specific package manager
/audit-deps "audit npm packages"

# Pre-deployment audit
/audit-deps "before production deployment"
```

## What It Does

1. Discovers all dependency files in the project
2. Runs security audits (npm audit, pip-audit, composer audit, etc.)
3. Checks for outdated packages
4. Identifies compatibility issues
5. Categorizes findings by severity
6. Provides prioritized update plan
7. Shows exact commands to fix issues

## Checks Performed

### Security Vulnerabilities
- Critical: RCE, auth bypass, SQL injection
- High: XSS, CSRF, privilege escalation
- Medium: Information disclosure, DoS
- Low: Minor issues with limited impact

### Outdated Dependencies
- Major version updates (2.x → 5.x)
- Minor version updates (3.2.x → 3.5.x)
- Patch version updates (1.2.3 → 1.2.8)

### Compatibility
- Peer dependency conflicts
- Version range conflicts
- Deprecated packages
- Unmaintained packages

## Supported Package Managers

- **Python**: pip, poetry, pipenv
- **Node.js**: npm, yarn, pnpm
- **PHP**: composer
- **Go**: go modules
- **Rust**: cargo
- **Ruby**: bundler
- **Java**: maven, gradle
- **.NET**: NuGet

## Output Includes

- Executive summary with critical issues
- Security vulnerabilities with CVEs
- Outdated dependencies list
- Compatibility issues
- Prioritized update plan with timeline
- Exact commands to execute
- Testing and verification strategy

## When to Use

- Before production deployments
- Monthly/quarterly security reviews
- After discovering a security issue
- When planning dependency updates
- Before major feature releases

---

When this command is invoked, perform a comprehensive dependency audit following the checks above. Discover dependency files, run security audits, check for outdated packages, and provide a prioritized update plan with exact commands to fix issues.

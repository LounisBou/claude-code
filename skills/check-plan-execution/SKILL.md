---
name: check-plan-execution
description: |
  Verify that /execute-next-plan workflow was followed correctly with all gates, skill invocations, and quality checks.
  WHEN: Use after completing a phase to audit workflow compliance. Invoke with "/check-plan-execution".
  WHEN NOT: During active development - use this for post-execution verification only.
---

# Check Plan Execution

## Purpose

This skill audits the `/execute-next-plan` workflow to ensure:
1. ALL 11 GATES were completed
2. ALL mandatory skill invocations were made
3. Implementation matches the phase plan
4. Quality checks passed
5. PR review issues were all addressed

---

## STEP 0: Initialize Audit Checklist

**IMMEDIATELY upon starting this skill, call TodoWrite:**

```
TodoWrite with todos:
[
  {"content": "AUDIT 1: Verify GATE compliance (all 11 gates)", "status": "pending", "activeForm": "Auditing gate compliance"},
  {"content": "AUDIT 2: Verify mandatory skill invocations", "status": "pending", "activeForm": "Checking skill invocations"},
  {"content": "AUDIT 3: Verify implementation completeness", "status": "pending", "activeForm": "Checking implementation"},
  {"content": "AUDIT 4: Verify quality checks passed", "status": "pending", "activeForm": "Verifying quality checks"},
  {"content": "AUDIT 5: Verify PR review compliance", "status": "pending", "activeForm": "Checking PR review compliance"},
  {"content": "AUDIT 6: Generate audit report", "status": "pending", "activeForm": "Generating audit report"}
]
```

---

## AUDIT 1: Verify GATE Compliance

**Mark "AUDIT 1" as `in_progress`.**

### 1.1 Identify Current Phase

```bash
# Get current branch
git branch --show-current

# Get recent PRs
gh pr list --state all --limit 5

# Find phase from branch name or recent PR
```

### 1.2 Check Each GATE

**For each gate, verify evidence exists:**

| Gate | Verification Method | Evidence Required |
|------|---------------------|-------------------|
| GATE 1 | Branch name matches phase | `feat/X.Y-<name>` pattern |
| GATE 2 | Branch created from main | `git log --oneline main..HEAD` shows commits |
| GATE 3 | Tasks implemented | Code changes match phase plan |
| GATE 4 | Quality checks ran | `composer analyse`, `composer format:check`, tests pass |
| GATE 5 | Brainstorming done | Test coverage verified against specs |
| GATE 6 | PR review ran | Review summary exists |
| GATE 7 | Fixes applied | All issues in review marked FIXED |
| GATE 8 | Review saved | `docs/reviews/phase-X.Y-*.md` exists |
| GATE 9 | Final checks passed | All quality commands pass now |
| GATE 10 | PR created | `gh pr view` returns PR info |
| GATE 11 | Approval requested | PR is open or merged |

### 1.3 Gate Compliance Checklist

Run these verifications:

```bash
# Check branch pattern
git branch --show-current | grep -E "feat/[0-9]+\.[0-9]+-"

# Check commits exist
git log --oneline main..HEAD | head -5

# Check review doc exists
ls docs/reviews/phase-*.md 2>/dev/null || echo "NO REVIEW DOC FOUND"

# Check PR exists
gh pr view 2>/dev/null || echo "NO PR FOUND"
```

**Record findings:**
- [ ] GATE 1: ✅ or ❌
- [ ] GATE 2: ✅ or ❌
- [ ] GATE 3: ✅ or ❌ (verify in AUDIT 3)
- [ ] GATE 4: ✅ or ❌ (verify in AUDIT 4)
- [ ] GATE 5: ✅ or ❌ (verify in AUDIT 2)
- [ ] GATE 6: ✅ or ❌ (verify in AUDIT 2)
- [ ] GATE 7: ✅ or ❌ (verify in AUDIT 5)
- [ ] GATE 8: ✅ or ❌
- [ ] GATE 9: ✅ or ❌ (verify in AUDIT 4)
- [ ] GATE 10: ✅ or ❌
- [ ] GATE 11: ✅ or ❌

**Mark "AUDIT 1" as `completed`.**

---

## AUDIT 2: Verify Mandatory Skill Invocations

**Mark "AUDIT 2" as `in_progress`.**

### 2.1 Required Skill Invocations

The `/execute-next-plan` workflow REQUIRES these skill invocations:

| Gate | Required Skill | How to Verify |
|------|----------------|---------------|
| **GATE 3** | `superpowers:executing-plans` | Implementation follows structured execution |
| **GATE 5** | `superpowers:brainstorming` | Test coverage analysis exists |
| **GATE 6** | `pr-review-toolkit:review-pr` | Multi-agent review completed |

### 2.2 Evidence Check

**GATE 3 - Executing Plans:**
- Look for structured task breakdown in implementation
- Check if TDD pattern was followed (tests before code)
- Verify step-by-step execution evidence

**GATE 5 - Brainstorming:**
- Check review doc for "Test Coverage Analysis" or "Brainstorming Results" section
- Verify test coverage was analyzed against specifications
- Look for gap analysis

**GATE 6 - PR Review:**
- Check review doc for multiple agent results:
  - code-reviewer
  - comment-analyzer
  - silent-failure-hunter
  - type-design-analyzer (if types added)
  - pr-test-analyzer (if tests added)
- Verify "Critical Issues", "Important Issues", "Suggestions" sections exist

### 2.3 Skill Invocation Checklist

- [ ] GATE 3 skill invoked: Evidence of `/superpowers:executing-plans`
- [ ] GATE 5 skill invoked: Evidence of `/superpowers:brainstorming`
- [ ] GATE 6 skill invoked: Evidence of `/pr-review-toolkit:review-pr`

**If ANY skill was NOT invoked:** Mark as FAILED.

**Mark "AUDIT 2" as `completed`.**

---

## AUDIT 3: Verify Implementation Completeness

**Mark "AUDIT 3" as `in_progress`.**

### 3.1 Read Phase Plan

```bash
# Find phase plan file
ls docs/plans/phase-*/
```

Read the relevant phase plan file.

### 3.2 Extract Required Tasks

List ALL tasks from the phase plan:

```markdown
## Tasks from Phase X.Y Plan:
1. [ ] Task 1 description
2. [ ] Task 2 description
3. [ ] Task 3 description
...
```

### 3.3 Verify Each Task Implementation

**For EACH task in the plan:**

1. **Identify expected deliverable** (file, config, feature)
2. **Check if deliverable exists**
3. **Verify deliverable is correct/complete**

```bash
# Check files changed in this branch
git diff --name-only main..HEAD

# Check specific file exists
ls -la <expected-file-path>

# Read file to verify content
```

### 3.4 Implementation Completeness Checklist

For each task:
- [ ] Task 1: ✅ Implemented / ❌ Missing / ⚠️ Incomplete
- [ ] Task 2: ✅ Implemented / ❌ Missing / ⚠️ Incomplete
- [ ] Task 3: ✅ Implemented / ❌ Missing / ⚠️ Incomplete
...

**Calculate completion percentage:** X/Y tasks = Z%

**If < 100%:** Mark as FAILED with list of missing/incomplete tasks.

**Mark "AUDIT 3" as `completed`.**

---

## AUDIT 4: Verify Quality Checks Passed

**Mark "AUDIT 4" as `in_progress`.**

### 4.1 Run All Quality Commands

```bash
cd /Users/lounis/dev/ScreenBuddies/backend

# 1. Run tests
php artisan test

# 2. Run static analysis
composer analyse

# 3. Run code style check
composer format:check

# 4. Check git status is clean
git status
```

### 4.2 Quality Check Results

| Check | Command | Result |
|-------|---------|--------|
| Tests | `php artisan test` | ✅ PASS / ❌ FAIL |
| PHPStan | `composer analyse` | ✅ PASS / ❌ FAIL |
| CS Fixer | `composer format:check` | ✅ PASS / ❌ FAIL |
| Git Clean | `git status` | ✅ Clean / ❌ Dirty |

### 4.3 Coverage Check (if available)

```bash
php artisan test --coverage 2>/dev/null || echo "Coverage driver not available"
```

**If ANY quality check fails:** Mark as FAILED.

**Mark "AUDIT 4" as `completed`.**

---

## AUDIT 5: Verify PR Review Compliance

**Mark "AUDIT 5" as `in_progress`.**

### 5.1 Read Review Document

```bash
cat docs/reviews/phase-*.md
```

### 5.2 Extract All Issues

Parse the review document for:
- **Critical Issues** (must be 0 remaining)
- **Important Issues** (must all be FIXED)
- **Other Issues** (must all be FIXED)
- **Suggestions** (must all be EVALUATED)

### 5.3 Verify Issue Resolution

**For Critical Issues:**
| Issue | Status Required | Actual Status |
|-------|-----------------|---------------|
| Issue 1 | FIXED | ✅/❌ |
| Issue 2 | FIXED | ✅/❌ |

**For Important Issues:**
| Issue | Status Required | Actual Status |
|-------|-----------------|---------------|
| Issue 1 | FIXED | ✅/❌ |
| Issue 2 | FIXED | ✅/❌ |

**For Other Issues:**
| Issue | Status Required | Actual Status |
|-------|-----------------|---------------|
| Issue 1 | FIXED | ✅/❌ |

**For Suggestions:**
| Suggestion | Required | Actual |
|------------|----------|--------|
| Suggestion 1 | APPLIED or DOCUMENTED | ✅/❌ |
| Suggestion 2 | APPLIED or DOCUMENTED | ✅/❌ |

### 5.4 PR Review Compliance Checklist

- [ ] All Critical issues: FIXED
- [ ] All Important issues: FIXED
- [ ] All Other issues: FIXED
- [ ] All Suggestions: EVALUATED (applied or documented why not)

**If ANY issue not properly addressed:** Mark as FAILED.

**Mark "AUDIT 5" as `completed`.**

---

## AUDIT 6: Generate Audit Report

**Mark "AUDIT 6" as `in_progress`.**

### 6.1 Compile Results

Create the final audit report:

```markdown
# Plan Execution Audit Report

**Phase:** X.Y - <name>
**Date:** YYYY-MM-DD
**Branch:** feat/X.Y-<name>
**PR:** #<number>

---

## GATE Compliance

| Gate | Description | Status |
|------|-------------|--------|
| 1 | Determine next phase | ✅/❌ |
| 2 | Create feature branch | ✅/❌ |
| 3 | Execute with TDD | ✅/❌ |
| 4 | Quality checks | ✅/❌ |
| 5 | Brainstorm coverage | ✅/❌ |
| 6 | PR review | ✅/❌ |
| 7 | Apply fixes | ✅/❌ |
| 8 | Save review | ✅/❌ |
| 9 | Final quality | ✅/❌ |
| 10 | Create PR | ✅/❌ |
| 11 | User approval | ✅/❌ |

**Gate Compliance:** X/11 (Y%)

---

## Mandatory Skill Invocations

| Gate | Skill | Invoked? |
|------|-------|----------|
| 3 | superpowers:executing-plans | ✅/❌ |
| 5 | superpowers:brainstorming | ✅/❌ |
| 6 | pr-review-toolkit:review-pr | ✅/❌ |

**Skill Compliance:** X/3 (Y%)

---

## Implementation Completeness

| Task | Status |
|------|--------|
| Task 1 | ✅/❌/⚠️ |
| Task 2 | ✅/❌/⚠️ |
| Task 3 | ✅/❌/⚠️ |

**Implementation:** X/Y tasks (Z%)

---

## Quality Checks

| Check | Status |
|-------|--------|
| Tests | ✅/❌ |
| PHPStan | ✅/❌ |
| CS Fixer | ✅/❌ |
| Git Clean | ✅/❌ |

**Quality:** X/4 passed

---

## PR Review Issues

| Category | Total | Fixed | Pending |
|----------|-------|-------|---------|
| Critical | X | X | 0 |
| Important | X | X | 0 |
| Other | X | X | 0 |
| Suggestions | X | X evaluated | 0 |

**Review Compliance:** 100% / X%

---

## OVERALL VERDICT

### ✅ PASSED - All checks passed

OR

### ❌ FAILED - Issues found:

1. [Issue 1]
2. [Issue 2]
3. [Issue 3]

### Required Actions:
1. [Action 1]
2. [Action 2]
```

### 6.2 Present Report to User

**Output the complete audit report.**

**If PASSED:**
```
═══════════════════════════════════════════════════════════════
AUDIT PASSED: Phase X.Y execution verified
═══════════════════════════════════════════════════════════════
All 11 gates completed.
All 3 mandatory skills invoked.
All tasks implemented.
All quality checks passed.
All PR review issues addressed.

The /execute-next-plan workflow was followed correctly.
═══════════════════════════════════════════════════════════════
```

**If FAILED:**
```
═══════════════════════════════════════════════════════════════
⚠️ AUDIT FAILED: Phase X.Y execution incomplete
═══════════════════════════════════════════════════════════════

FAILURES FOUND:
1. [Failure description]
2. [Failure description]

REQUIRED REMEDIATION:
1. [What needs to be done]
2. [What needs to be done]

Re-run /execute-next-plan to complete missing steps.
═══════════════════════════════════════════════════════════════
```

**Mark "AUDIT 6" as `completed`.**

---

## Quick Audit Commands

For fast verification, run these commands:

```bash
# 1. Check branch
git branch --show-current

# 2. Check review doc exists
ls docs/reviews/phase-*.md

# 3. Check PR exists
gh pr view

# 4. Run quality checks
cd /Users/lounis/dev/ScreenBuddies/backend
php artisan test && composer analyse && composer format:check

# 5. Check git is clean
git status
```

---

## Remediation Guide

### If Gates Missing

| Missing Gate | Remediation |
|--------------|-------------|
| GATE 3 | Re-run `/superpowers:executing-plans` |
| GATE 5 | Run `/superpowers:brainstorming` for test coverage |
| GATE 6 | Run `/pr-review-toolkit:review-pr` |
| GATE 7 | Fix all issues from review |
| GATE 8 | Create `docs/reviews/phase-X.Y-*.md` |

### If Quality Checks Fail

```bash
# Fix code style
composer format

# Re-run checks
php artisan test
composer analyse
composer format:check
```

### If Implementation Incomplete

1. Read the phase plan again
2. Identify missing tasks
3. Implement missing tasks with TDD
4. Re-run quality checks

---

## Self-Check Questions

Before marking audit complete:

| Question | Answer |
|----------|--------|
| Did I verify ALL 11 gates? | Yes/No |
| Did I check ALL 3 mandatory skill invocations? | Yes/No |
| Did I verify EVERY task from the phase plan? | Yes/No |
| Did I run ALL quality commands? | Yes/No |
| Did I check ALL PR review issues? | Yes/No |
| Did I generate the complete audit report? | Yes/No |

**If ANY answer is "No", the audit is incomplete.**

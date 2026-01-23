---
name: execute-next-plan
description: |
  Execute the next phase from the project plan with full TDD workflow, 100% coverage, PR review, and quality gates.
  WHEN: Use to continue development on ScreenBuddies project. Invoke with "/execute-next-plan".
  WHEN NOT: When debugging specific issues or exploring codebase.
---

# Execute Next Plan Phase

## CRITICAL: MANDATORY ENFORCEMENT SYSTEM

**THIS IS NOT OPTIONAL. YOU MUST FOLLOW THIS EXACTLY.**

### STEP 0: Initialize Workflow Checklist (DO THIS FIRST!)

**IMMEDIATELY upon starting this skill, before ANY other action, you MUST:**

1. **Announce:** "I'm using the execute-next-plan skill. Initializing mandatory workflow checklist."

2. **Call TodoWrite with this EXACT checklist:**

```
TodoWrite with todos:
[
  {"content": "GATE 1: Determine next phase", "status": "pending", "activeForm": "Finding next phase"},
  {"content": "GATE 2: Create feature branch from main", "status": "pending", "activeForm": "Creating feature branch"},
  {"content": "GATE 3: Execute phase tasks with TDD", "status": "pending", "activeForm": "Implementing with TDD"},
  {"content": "GATE 4: Run quality checks (tests, analyse, format)", "status": "pending", "activeForm": "Running quality checks"},
  {"content": "GATE 5: Brainstorm verify test coverage matches specs", "status": "pending", "activeForm": "Verifying test coverage"},
  {"content": "GATE 6: Run PR review toolkit", "status": "pending", "activeForm": "Running PR review"},
  {"content": "GATE 7: Apply ALL review fixes", "status": "pending", "activeForm": "Applying review fixes"},
  {"content": "GATE 8: Save review to docs/reviews/", "status": "pending", "activeForm": "Saving review summary"},
  {"content": "GATE 9: Run final quality gate check", "status": "pending", "activeForm": "Final quality gate"},
  {"content": "GATE 10: Create PR", "status": "pending", "activeForm": "Creating PR"},
  {"content": "GATE 11: Wait for user approval", "status": "pending", "activeForm": "Waiting for approval"}
]
```

3. **RULE:** Before starting ANY gate, mark it `in_progress`. After completing it, mark it `completed`.

4. **RULE:** You CANNOT start a gate until ALL previous gates are `completed`.

5. **RULE:** If you skip a gate, you have FAILED the workflow. Start over.

---

## GATE 1: Determine Next Phase

**Mark todo "GATE 1" as `in_progress` before starting.**

### 1.1 Check Current Progress

```bash
# Check current branch
git branch --show-current

# Check if on main and pull latest
git checkout main
git pull origin main

# Check merged PRs to see what's done
gh pr list --state merged --limit 5

# List available phases
ls docs/plans/phase-*/
```

### 1.2 Find Next Phase

Read the main plan file to understand phase order:
- `docs/plans/phase-0-infrastructure.md` → Sub-phases 0.1 to 0.8
- `docs/plans/phase-1-backend-foundation.md` → Sub-phases 1.1 to 1.x

**Output:** "Next phase to execute: X.Y - <name>"

**Mark todo "GATE 1" as `completed`.**

---

## GATE 2: Create Feature Branch

**Mark todo "GATE 2" as `in_progress` before starting.**

```bash
git checkout main
git pull origin main
git checkout -b feat/<sub-phase-name>
# Example: git checkout -b feat/0.3-ci-cd-pipeline
```

**Verify:** `git branch --show-current` shows the new branch.

**Mark todo "GATE 2" as `completed`.**

---

## GATE 3: Execute Phase with TDD

**Mark todo "GATE 3" as `in_progress` before starting.**

### ⚠️ MANDATORY SKILL INVOCATION ⚠️

**YOU MUST USE THE SKILL TOOL TO INVOKE:**
```
Skill(skill: "superpowers:executing-plans")
```

**THIS IS NOT OPTIONAL. DO NOT USE Task AGENT. DO NOT SKIP. INVOKE THE SKILL.**

### 3.1 Read Phase Plan

Read the sub-phase file: `docs/plans/phase-X/X.Y-<name>.md`

### 3.2 Execute Each Task Using the Executing-Plans Skill

The `/superpowers:executing-plans` skill guides you through:
- Breaking down tasks into actionable steps
- Following TDD workflow for code changes
- Running verification after each step
- Review checkpoints

**TDD PATTERN (MANDATORY for code changes):**
1. Write test FIRST
2. Run test → MUST FAIL (red)
3. Write minimal code to pass
4. Run test → MUST PASS (green)
5. Verify coverage

**After each task:**
```bash
cd /Users/lounis/dev/ScreenBuddies/backend
php artisan test
```

**If infrastructure/config only:** Verify by running the tool/config directly.

**GATE 3 IS NOT COMPLETE UNTIL YOU HAVE INVOKED `/superpowers:executing-plans`**

**Mark todo "GATE 3" as `completed` only after ALL tasks done.**

---

## GATE 4: Run Quality Checks

**Mark todo "GATE 4" as `in_progress` before starting.**

Run ALL of these:

```bash
cd /Users/lounis/dev/ScreenBuddies/backend

# 1. Tests
php artisan test

# 2. Coverage (if PCOV/Xdebug available)
php artisan test --coverage || echo "Coverage driver not installed"

# 3. Static analysis
composer analyse

# 4. Code style check
composer format:check

# 5. Fix style if needed
composer format
```

**LOOP until ALL pass.** Do NOT proceed with failures.

**Mark todo "GATE 4" as `completed`.**

---

## GATE 5: Brainstorm Verify Test Coverage

**Mark todo "GATE 5" as `in_progress` before starting.**

### ⚠️ MANDATORY SKILL INVOCATION ⚠️

**YOU MUST USE THE SKILL TOOL TO INVOKE:**
```
Skill(skill: "superpowers:brainstorming")
```

**THIS IS NOT OPTIONAL. DO NOT USE Task AGENT. DO NOT SKIP. INVOKE THE SKILL.**

**After skill loads, use this prompt:**

```
Question: Do our tests fully cover the Phase X.Y specifications?

Context:
- Phase plan: docs/plans/phase-X/X.Y-<name>.md
- Current tests: backend/tests/
- Specifications: docs/specifications/

Deliverable:
- List specification requirements NOT covered by tests
- For each gap, specify what test should be added
```

**If gaps found:** Add the missing tests, then re-run GATE 4.

**GATE 5 IS NOT COMPLETE UNTIL YOU HAVE INVOKED `/superpowers:brainstorming`**

**Mark todo "GATE 5" as `completed`.**

---

## GATE 6: Run PR Review

**Mark todo "GATE 6" as `in_progress` before starting.**

### 6.1 Push Branch First

```bash
git add -A
git commit -m "feat: <phase description>"
git push -u origin feat/<sub-phase-name>
```

### 6.2 Invoke PR Review

### ⚠️ MANDATORY SKILL INVOCATION ⚠️

**YOU MUST USE THE SKILL TOOL TO INVOKE:**
```
Skill(skill: "pr-review-toolkit:review-pr")
```

**THIS IS NOT OPTIONAL. DO NOT USE Task AGENT. DO NOT SKIP. INVOKE THE SKILL.**

Wait for ALL review agents to complete.

**GATE 6 IS NOT COMPLETE UNTIL YOU HAVE INVOKED `/pr-review-toolkit:review-pr`**

**Mark todo "GATE 6" as `completed`.**

---

## GATE 7: Apply ALL Review Fixes

**Mark todo "GATE 7" as `in_progress` before starting.**

### ⚠️ MANDATORY CORRECTION RULES ⚠️

**YOU MUST FIX EVERY ISSUE. THIS IS NOT OPTIONAL.**

#### STEP 7.1: Create Issue Tracking List

**IMMEDIATELY create a TodoWrite checklist for ALL issues from the review:**

```
TodoWrite: Add one todo per issue found in the review:
- "FIX CRITICAL: <issue description>" (status: pending)
- "FIX IMPORTANT: <issue description>" (status: pending)
- "FIX OTHER: <issue description>" (status: pending)
- "EVALUATE SUGGESTION: <suggestion description>" (status: pending)
```

#### STEP 7.2: Fix ALL Critical Issues (MANDATORY - NO EXCEPTIONS)

| Rule | Enforcement |
|------|-------------|
| Every Critical issue | **MUST BE FIXED** |
| Skip allowed? | **NO - NEVER** |
| Partial fix allowed? | **NO - COMPLETE FIX ONLY** |

**For each Critical issue:**
1. Read the issue description and file location
2. Implement the complete fix
3. Verify the fix works
4. Mark todo as `completed`

**GATE 7 FAILS if ANY Critical issue remains unfixed.**

#### STEP 7.3: Fix ALL Important Issues (MANDATORY - NO EXCEPTIONS)

| Rule | Enforcement |
|------|-------------|
| Every Important issue | **MUST BE FIXED** |
| Skip allowed? | **NO - NEVER** |
| Partial fix allowed? | **NO - COMPLETE FIX ONLY** |

**For each Important issue:**
1. Read the issue description and file location
2. Implement the complete fix
3. Verify the fix works
4. Mark todo as `completed`

**GATE 7 FAILS if ANY Important issue remains unfixed.**

#### STEP 7.4: Fix ALL Other Issues (MANDATORY - NO EXCEPTIONS)

| Rule | Enforcement |
|------|-------------|
| Every other issue | **MUST BE FIXED** |
| Skip allowed? | **NO - NEVER** |
| Partial fix allowed? | **NO - COMPLETE FIX ONLY** |

**For each other issue:**
1. Read the issue description and file location
2. Implement the complete fix
3. Verify the fix works
4. Mark todo as `completed`

**GATE 7 FAILS if ANY other issue remains unfixed.**

#### STEP 7.5: Evaluate ALL Suggestions (MANDATORY EVALUATION)

| Rule | Enforcement |
|------|-------------|
| Every suggestion | **MUST BE EVALUATED** |
| Skip evaluation? | **NO - MUST DECIDE** |
| Decision required | **APPLY or DOCUMENT WHY NOT** |

**For each suggestion:**
1. Read the suggestion carefully
2. **Evaluate pertinence:**
   - Does it improve code quality?
   - Does it align with project standards?
   - Is it worth the effort?
3. **Make a decision:**
   - **IF PERTINENT:** Apply the suggestion, mark todo `completed`
   - **IF NOT PERTINENT:** Document WHY in the review summary, mark todo `completed`

**Example of documenting rejected suggestion:**
```markdown
### Suggestion: Add PHPStan baseline file
**Decision:** NOT APPLIED
**Reason:** Project is new with zero existing errors. Baseline not needed until legacy code exists.
```

**GATE 7 FAILS if ANY suggestion was not evaluated.**

#### STEP 7.6: Verification Checklist

Before marking GATE 7 complete, verify:

- [ ] ALL Critical issues have been fixed
- [ ] ALL Important issues have been fixed
- [ ] ALL other issues have been fixed
- [ ] ALL suggestions have been evaluated (applied or documented why not)
- [ ] ALL issue todos are marked `completed`

#### STEP 7.7: Commit All Fixes

```bash
git add -A
git commit -m "fix: address ALL PR review feedback

- Fixed X critical issues
- Fixed X important issues
- Fixed X other issues
- Applied X suggestions
- Documented X suggestions as not applicable"
git push
```

**GATE 7 IS NOT COMPLETE UNTIL:**
1. Every Critical issue is fixed
2. Every Important issue is fixed
3. Every other issue is fixed
4. Every suggestion is evaluated (applied or rejected with reason)
5. All changes are committed and pushed

**Mark todo "GATE 7" as `completed`.**

**Mark todo "GATE 7" as `completed`.**

---

## GATE 8: Save Review Summary

**Mark todo "GATE 8" as `in_progress` before starting.**

```bash
mkdir -p docs/reviews
```

**Write review summary to:** `docs/reviews/phase-X.Y-<name>.md`

Include:
- Date and PR number
- Review agents used
- Critical/Important/Suggestion issues (with status: FIXED or NOTED)
- Quality checklist results

```bash
git add docs/reviews/
git commit -m "docs: add Phase X.Y review summary"
git push
```

**Mark todo "GATE 8" as `completed`.**

---

## GATE 9: Final Quality Gate

**Mark todo "GATE 9" as `in_progress` before starting.**

**Run FULL quality check again:**

```bash
cd /Users/lounis/dev/ScreenBuddies/backend

# ALL must pass
php artisan test
composer analyse
composer format:check

# Verify clean working directory
git status
```

**If ANY fails:** Fix and re-run. Do NOT proceed.

**Mark todo "GATE 9" as `completed`.**

---

## GATE 10: Create PR

**Mark todo "GATE 10" as `in_progress` before starting.**

```bash
gh pr create \
  --title "feat: Phase X.Y - <name>" \
  --body "## Summary
<Brief description>

## Changes
- Change 1
- Change 2

## Quality Checks
- [x] All tests passing
- [x] Static analysis passing
- [x] Code style passing

## Review
See docs/reviews/phase-X.Y-<name>.md

## Phase Reference
docs/plans/phase-X/X.Y-<name>.md"
```

**Output:** PR URL

**Mark todo "GATE 10" as `completed`.**

---

## GATE 11: Wait for User Approval

**Mark todo "GATE 11" as `in_progress`.**

**STOP and announce this EXACT format:**

```
═══════════════════════════════════════════════════════════════
PHASE X.Y IMPLEMENTATION COMPLETE
═══════════════════════════════════════════════════════════════

PR: <URL>

WORKFLOW GATES COMPLETED:
✅ GATE 1: Determined next phase
✅ GATE 2: Created feature branch
✅ GATE 3: Executed phase tasks with TDD
✅ GATE 4: Quality checks passed
✅ GATE 5: Brainstorm verified test coverage
✅ GATE 6: PR review completed
✅ GATE 7: All review fixes applied
✅ GATE 8: Review saved to docs/reviews/
✅ GATE 9: Final quality gate passed
✅ GATE 10: PR created
⏳ GATE 11: Waiting for your approval

Review: docs/reviews/phase-X.Y-<name>.md

Waiting for your approval to merge and continue to Phase X.(Y+1).
═══════════════════════════════════════════════════════════════
```

**DO NOT proceed until user explicitly approves.**

**Mark todo "GATE 11" as `completed` only after user approves.**

---

## Error Recovery

### If Any Gate Fails
1. Fix the issue
2. Re-run that gate
3. Do NOT skip to the next gate

### If Blocked
1. Document what's blocking
2. Ask user for guidance
3. Do NOT skip or workaround

### If You Forgot a Gate
1. STOP immediately
2. Go back and complete the missed gate
3. Re-run subsequent gates

---

## Self-Check Questions

Before marking a gate complete, ask yourself:

| Gate | Self-Check Question |
|------|---------------------|
| 1 | Did I identify the specific phase number and name? |
| 2 | Am I on a new feature branch from main? |
| 3 | **Did I call `Skill(skill: "superpowers:executing-plans")` and implement ALL tasks?** |
| 4 | Did tests, analyse, and format:check ALL pass? |
| 5 | **Did I call `Skill(skill: "superpowers:brainstorming")`?** |
| 6 | **Did I call `Skill(skill: "pr-review-toolkit:review-pr")`?** |
| 7 | Did I fix ALL Critical, ALL Important, ALL other issues, and evaluate ALL suggestions? |
| 8 | Did I create docs/reviews/phase-X.Y-<name>.md? |
| 9 | Did ALL quality checks pass again after fixes? |
| 10 | Did I create the PR with gh pr create? |
| 11 | Did I show the final status and wait for approval? |

**If ANY answer is "no", you have not completed that gate.**

---

## CRITICAL SKILL INVOCATIONS

**These skills MUST be invoked using the Skill tool. NO EXCEPTIONS.**

| Gate | Required Skill Invocation |
|------|---------------------------|
| **GATE 3** | `Skill(skill: "superpowers:executing-plans")` |
| **GATE 5** | `Skill(skill: "superpowers:brainstorming")` |
| **GATE 6** | `Skill(skill: "pr-review-toolkit:review-pr")` |

**Using Task agent or any other method is NOT acceptable for these gates.**

---

## CRITICAL CORRECTION REQUIREMENTS (GATE 7)

**ALL issues from PR review MUST be addressed. NO EXCEPTIONS.**

| Issue Type | Action Required | Skip Allowed? |
|------------|-----------------|---------------|
| **Critical Issues** | FIX ALL | ❌ NEVER |
| **Important Issues** | FIX ALL | ❌ NEVER |
| **Other Issues** | FIX ALL | ❌ NEVER |
| **Suggestions** | EVALUATE ALL | ❌ NEVER (must apply OR document why not) |

**GATE 7 FAILS if:**
- Any Critical issue is not fixed
- Any Important issue is not fixed
- Any other issue is not fixed
- Any suggestion is not evaluated (applied or rejected with documented reason)

**You MUST create a TodoWrite checklist tracking each issue individually.**

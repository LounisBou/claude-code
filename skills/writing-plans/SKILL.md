---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** This should be run in a dedicated worktree (created by brainstorming skill).

**Save plans to:** `plans/YYYY-MM-DD-<feature-name>.md`

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## Task Structure

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## Remember
- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- Reference relevant skills with @ syntax
- DRY, YAGNI, TDD, frequent commits

## Phase 2: Insert Inline TODOs

After saving the high-level plan, insert TODOs directly into code files:

1. **Identify touch points** - All files that need changes
2. **Insert scoped TODOs** at exact locations using language-appropriate syntax:
   ```python
   # TODO(feature-name): Validate input against schema
   ```
   ```php
   // TODO(feature-name): Add rate limiting check here
   ```
   ```html
   <!-- TODO(feature-name): Add loading spinner -->
   ```
   ```css
   /* TODO(feature-name): Add dark mode variables */
   ```
3. **Format:** `[comment-prefix] TODO(scope): action-verb description`
4. **Granularity:** Each TODO = 2-15 minutes of work
5. **Commit:** `prepare(feature): add implementation TODOs`

**TODO Placement:**
- Entry points (where feature starts)
- Integration points (connections to existing code)
- Data flow points (transformations between layers)
- Error handling gaps
- Test files (what tests to write)

**Good TODOs (explicit & scoped):**
```javascript
// TODO(cart): Calculate shipping cost based on user.address.country
// TODO(cart): Apply discount code if cart.discountCode is set
```

**Bad TODOs (vague):**
```javascript
// TODO: fix this later
// TODO: needs work
```

**Comment syntax by language:**
| Language | Syntax |
|----------|--------|
| Python, Ruby, Bash | `# TODO(scope): description` |
| JS, TS, PHP, Java, Go, Rust, C, C++ | `// TODO(scope): description` |
| HTML, Vue template | `<!-- TODO(scope): description -->` |
| CSS, SCSS | `/* TODO(scope): description */` |

**List TODOs:** `python hooks/list_todos.py feature-name`

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use superpowers:subagent-driven-development
- Stay in this session
- Fresh subagent per task + code review

**If Parallel Session chosen:**
- Guide them to open new session in worktree
- **REQUIRED SUB-SKILL:** New session uses superpowers:executing-plans

## Plan Revision

**When to revise this plan:**
- Execution reveals 3+ tasks blocked by same issue
- Fundamental assumption was wrong
- New requirements emerge mid-execution

**How to revise:**
1. Read feedback from executing session
2. Identify root cause (scope creep, missing context, wrong approach)
3. Update plan document with corrections
4. Re-insert/update inline TODOs as needed
5. Commit revised plan before resuming execution

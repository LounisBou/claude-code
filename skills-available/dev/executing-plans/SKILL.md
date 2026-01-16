---
name: executing-plans
description: |
  Execute written implementation plans with batch tasks and human checkpoints between batches.
  WHEN: MUST use when have a plan file to execute. Invoke with "/executing-plans" or "execute this plan", "implement this plan". For plans created by writing-plans skill.
  WHEN NOT: No plan exists yet (use writing-plans), design phase (use brainstorming), same-session execution.
---

# Executing Plans

## Overview

Load plan, review critically, execute tasks in batches, report for review between batches.

**Core principle:** Batch execution with checkpoints for architect review.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

## The Process

### Step 1: Load and Review Plan
1. Read plan file for high-level context
2. List inline TODOs: `python hooks/list_todos.py feature-name`
3. Review critically - identify any questions or concerns
4. If concerns: Raise them with your human partner before starting
5. If no concerns: Create TodoWrite from inline TODOs and proceed

### Step 2: Execute Batch
**Default: First 3 tasks**

For each task:
1. Mark as in_progress
2. Implement the code at the TODO location
3. Remove the TODO comment once implemented
4. Run verifications as specified
5. Mark as completed

**Verify progress:** `python hooks/list_todos.py feature-name` should show fewer TODOs

**If verification fails:**
- Use superpowers:systematic-debugging to investigate root cause
- Fix issue before proceeding to next task
- Do not skip failed verifications
- If debugging reveals design flaw, stop and consult plan

### Step 3: Report
When batch complete:
- Show what was implemented
- Show verification output
- Say: "Ready for feedback."

### Step 4: Continue
Based on feedback:
- Apply changes if needed
- Execute next batch
- Repeat until complete

### Step 5: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use superpowers:finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker mid-batch (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Failure Recovery

**If 3+ tasks hit blockers:**
- Stop execution
- Return to superpowers:writing-plans for plan revision
- Don't continue with a broken plan

**If debugging reveals design flaw:**
- Return to superpowers:brainstorming to reconsider approach
- Document what was learned

**If architectural issues span multiple tasks:**
- Escalate to human partner immediately
- Don't attempt piecemeal fixes

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Between batches: just report and wait
- Stop when blocked, don't guess

---
name: pr-review-toolkit-process-comments
description: |
  Process GitHub PR review comments and change requests - answer questions, make corrections, resolve threads.
  WHEN: Use after PR is created and has review comments. Invoke with "/pr-review-toolkit:process-comments".
  WHEN NOT: When PR has no comments or before PR is created.
---

# PR Review Process Comments

## Overview

This skill processes GitHub PR review comments and change requests:
1. Fetch all comments and change requests
2. Categorize by type (question, change request, suggestion)
3. Answer questions with replies
4. Make code corrections for change requests
5. Mark threads as resolved after addressing

**Announce at start:** "I'm using the pr-review-toolkit:process-comments skill to process PR feedback."

---

## Step 1: Fetch PR Comments

### 1.1 Get Current PR Number

```bash
# Get PR number for current branch
gh pr view --json number -q '.number'
```

### 1.2 Fetch All Review Comments

```bash
# Get PR review comments (inline code comments)
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments

# Get PR issue comments (general comments)
gh api repos/{owner}/{repo}/issues/{pr_number}/comments

# Get PR reviews (approve/request changes)
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews
```

### 1.3 Parse and Display Comments

For each comment, extract:
- **id**: Comment ID (needed for replies/resolution)
- **path**: File path
- **line**: Line number
- **body**: Comment text
- **user**: Who wrote it
- **state**: PENDING, COMMENTED, APPROVED, CHANGES_REQUESTED

Display in table format:

```
| # | Type | File | Line | Comment | Author |
|---|------|------|------|---------|--------|
| 1 | Question | backend/package.json | 11 | Why is axios here? | user |
| 2 | Change Request | src/Controller.php | 45 | Add validation | user |
```

---

## Step 2: Categorize Comments

### Categories

| Type | Indicators | Action |
|------|------------|--------|
| **Question** | "?", "why", "what", "how", "could you explain" | Reply with answer |
| **Change Request** | "please", "should", "must", "change", "fix", "add", "remove" | Make code change |
| **Suggestion** | "consider", "might", "could", "optional", "nit" | Evaluate and decide |
| **Approval** | "LGTM", "looks good", "approved" | No action needed |

### Create Todo List

```
For each actionable comment, create a todo:
- [ ] Comment #1: [Question] Answer why axios is in devDependencies
- [ ] Comment #2: [Change] Add input validation to Controller.php:45
```

---

## Step 3: Process Each Comment

### 3.1 For Questions - Reply with Answer

```bash
# Reply to a PR review comment
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies \
  -f body="<your answer here>"
```

**Guidelines for answers:**
- Be concise and technical
- Reference documentation or code if helpful
- If you don't know, say so and ask for clarification

### 3.2 For Change Requests - Make Corrections

1. **Read the file** mentioned in the comment
2. **Understand the request** - what change is needed?
3. **Make the change** using Edit tool
4. **Verify** the change doesn't break tests:
   ```bash
   php artisan test
   ```
5. **Commit** with descriptive message:
   ```bash
   git add <file>
   git commit -m "fix: <description of change>

   Addresses PR comment #<comment_id>"
   ```

### 3.3 For Suggestions - Evaluate

1. **Consider** if the suggestion improves the code
2. **If yes**: Apply like a change request
3. **If no**: Reply explaining why not:
   ```bash
   gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies \
     -f body="Thanks for the suggestion. I chose not to apply this because..."
   ```

---

## Step 4: Mark as Resolved

### 4.1 After Addressing a Comment

Once a comment is addressed (answered or fixed), mark the thread as resolved:

```bash
# Resolve a PR review thread
gh api graphql -f query='
  mutation {
    resolveReviewThread(input: {threadId: "<thread_node_id>"}) {
      thread {
        isResolved
      }
    }
  }
'
```

**Note:** To get the thread_node_id, use:
```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments --jq '.[].node_id'
```

### 4.2 Alternative: Reply and Let Author Resolve

If you can't resolve programmatically, reply with:
```
"Addressed in commit <sha>. Please resolve this thread if satisfied."
```

---

## Step 5: Push Changes and Update PR

### 5.1 Push All Commits

```bash
git push
```

### 5.2 Add Summary Comment to PR

```bash
gh pr comment {pr_number} --body "## PR Feedback Addressed

### Questions Answered
- Comment #1: Explained why axios is included

### Changes Made
- Comment #2: Added validation (commit abc123)

### Suggestions
- Comment #3: Applied suggestion for better naming

All review feedback has been addressed. Ready for re-review."
```

---

## Step 6: Request Re-review (Optional)

If the PR had "Changes Requested" status:

```bash
gh pr edit {pr_number} --add-reviewer {reviewer_username}
```

---

## Complete Workflow Example

```bash
# 1. Get PR number
PR_NUM=$(gh pr view --json number -q '.number')

# 2. Fetch comments
gh api repos/{owner}/{repo}/pulls/$PR_NUM/comments

# 3. Process each comment (done manually with tools)

# 4. After all changes, push
git push

# 5. Add summary comment
gh pr comment $PR_NUM --body "All feedback addressed. See commits for changes."
```

---

## Error Handling

### Comment Not Found
- Refresh comment list: `gh api repos/{owner}/{repo}/pulls/{pr_number}/comments`
- Check if comment was deleted

### Cannot Resolve Thread
- Not all GitHub plans support programmatic resolution
- Reply with "Addressed in commit X" and ask author to resolve

### Tests Fail After Change
- Revert the change
- Reply to comment asking for clarification
- Do NOT push broken code

---

## Checklist

Before completing:

- [ ] All comments fetched and categorized
- [ ] All questions answered with replies
- [ ] All change requests addressed with code changes
- [ ] All suggestions evaluated (applied or explained why not)
- [ ] All changes committed with references to comment IDs
- [ ] Tests still pass after changes
- [ ] Changes pushed to PR branch
- [ ] Summary comment added to PR
- [ ] Threads marked as resolved (if possible)

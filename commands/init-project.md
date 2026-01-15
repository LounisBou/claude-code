---
name: init-project
description: Initialize project skills and agents based on project.json configuration
user_invocable: true
---

# Init Project Command

Initializes the project by creating symlinks for skills, agents, and commands based on the project.json configuration.

## Usage

```bash
/init-project
```

## What It Does

1. **Checks for project.json**
   - If exists: Reads configuration and builds symlinks
   - If not exists: Runs interactive setup to create project.json

2. **Creates symlinks**
   - Removes existing symlinks in skills/, agents/, commands/
   - Creates new symlinks based on selected categories
   - Includes local/ folder contents

3. **Updates CLAUDE.md**
   - Copies from CLAUDE.template.md if doesn't exist
   - Extracts matching sections from AGENTS.md and SKILLS.md
   - Replaces content between markers

4. **Reports summary**
   - Lists included categories
   - Counts skills/agents/commands loaded

## Interactive Setup

When no project.json exists, asks:
- What type of project? (PHP, Python, JavaScript/TypeScript, Vue.js)
- Which framework? (Symfony, Laravel, None)
- Include frontend? (Vue + Tailwind, vanilla JS/TS, No)

---

When this command is invoked:

1. First check if project.json exists in the .claude directory
2. If project.json does NOT exist:
   - Use AskUserQuestion to ask about project type (multi-select: PHP, Python, JavaScript/TypeScript, Vue.js)
   - Based on answers, ask follow-up questions about frameworks
   - Create project.json with selected categories
3. Run the init-project.py script: `python3 hooks/init-project.py`
4. Report the results to the user

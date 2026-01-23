# Claude Code Configuration

A Claude Code `.claude/` configuration folder that leverages external marketplace plugins for extended capabilities.

## Overview

This configuration provides a ready-to-use Claude Code setup with:

- **Curated marketplace plugins** from Anthropic and the community
- **Pre-configured permissions** for common development workflows
- **Logging hooks** for tracking tool usage
- **Empty folders** for adding custom components as needed

## Enabled Plugins

### Anthropic Plugins (`@anthropics-claude-code`)

| Plugin | Description |
|--------|-------------|
| `code-review` | Code review capabilities |
| `commit-commands` | Git commit workflows (`/commit`, `/commit-push-pr`) |
| `feature-dev` | Feature development workflows |
| `explanatory-output-style` | Explanatory output formatting |
| `agent-sdk-dev` | Agent SDK development tools |
| `frontend-design` | Frontend design assistance |
| `plugin-dev` | Plugin development tools |
| `pr-review-toolkit` | PR review tools |
| `security-guidance` | Security best practices |
| `alph-wiggum` | Investigation and analysis |
| `hookify` | Hook automation |

### Community Plugins

| Plugin | Source | Description |
|--------|--------|-------------|
| `superpowers` | `obra/superpowers-marketplace` | Enhanced development workflows |

## Installation

### For a New Project

Clone this repository as your project's `.claude/` folder:

```bash
cd /path/to/your/project
git clone <repository-url> .claude
```

### Global Configuration

To use across all projects, clone to your home directory:

```bash
git clone <repository-url> ~/.claude
```

## Directory Structure

```
.claude/
├── settings.json       # Plugin config, permissions, hooks
├── settings.local.json # Local overrides (not committed)
├── CLAUDE.md          # Instructions for Claude
├── hooks/             # Logging hooks
│   ├── bash_logger.py
│   ├── agent_logger.py
│   └── skill_logger.py
├── agents/            # Custom agents (add your own)
├── commands/          # Custom commands (add your own)
├── skills/            # Custom skills (add your own)
└── logs/              # Execution logs
```

## Configuration

### Permissions

The `settings.json` includes pre-configured permissions:

- **Auto-allowed**: Read operations, git status/log/diff, pytest, common dev tools
- **Ask first**: Git mutations (add, commit, push), package managers
- **Denied**: Destructive commands (rm, sudo)

Customize in `settings.json`:

```json
{
  "permissions": {
    "allow": ["Bash(pytest:*)"],
    "ask": ["Bash(npm install:*)"],
    "deny": ["Bash(rm:*)"]
  }
}
```

### Adding Custom Components

**Custom Command** - Create `commands/my-command.md`:
```markdown
---
name: my-command
description: What this command does
---

Instructions for Claude...
```

**Custom Skill** - Create `skills/my-skill/SKILL.md`:
```markdown
---
name: my-skill
description: When to use this skill
---

Specialized knowledge...
```

**Custom Agent** - Create `agents/my-agent.md`:
```markdown
---
name: my-agent
description: What this agent does
tools: Read, Grep, Glob, Bash
---

You are a specialized agent...
```

## Logging

The configuration includes hooks that log tool usage to `logs/`:

- `bash_logger.py` - Logs bash commands
- `agent_logger.py` - Logs agent invocations
- `skill_logger.py` - Logs skill usage

## License

Apache License 2.0 - see [LICENSE](LICENSE) file.

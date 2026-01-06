# Claude Code Configuration Library

A comprehensive collection of custom agents, commands, hooks, and skills for [Claude Code](https://claude.ai/code) that extends its capabilities across multiple languages and frameworks.

## Overview

This repository contains a production-ready `.claude` configuration that provides:

- **Language-agnostic code pattern analysis** for Python, JavaScript/TypeScript, PHP, Go, Rust, and more
- **Automated code quality checks** that learn from your codebase
- **31 specialized skills** covering Python, Symfony, Laravel, frontend development, and Claude Code plugin development
- **Custom commands** for rapid pattern discovery and compliance checking
- **Event-driven hooks** for automation and formatting

## Features

### 🤖 Intelligent Agents

**Code Norms Checker**: Analyzes your code changes against established project patterns
- Auto-detects language and framework
- Finds similar reference files automatically
- Reports violations with actionable suggestions
- Supports multi-language projects

**Code Review Agent**: Pragmatic code reviewer focusing on real issues
- Identifies LLM-generated code issues (placeholders, redundant patterns, etc.)
- Security vulnerability detection
- Performance issue identification
- Pattern compliance verification

### ⚡ Quick Commands

- `/find-pattern [type] [feature]` - Instantly find code pattern examples in your project
- `/check-norms` - Analyze all changes in current branch for pattern compliance

### 🎯 Specialized Skills

**Python Ecosystem** (8 skills):
- Document manipulation (Excel, Word, PDF)
- Testing patterns (pytest, fixtures, mocking)
- Packaging and distribution
- Async programming patterns
- Backend development (FastAPI, Django, Flask)
- Data transformation (pandas, numpy)
- Performance optimization

**PHP/Symfony/Laravel** (8 skills):
- Symfony API Platform (filters, serialization, security, state providers, resources)
- Symfony Doctrine ORM (migrations, fetch modes, batch processing)
- Laravel specialist (Laravel 10+ patterns)

**Claude Code Development** (7 skills):
- Plugin architecture and structure
- Command, agent, hook, and skill development
- MCP server integration

**Additional**:
- Frontend design (production-grade UI)
- SQL optimization patterns

### 🔧 Automation Hooks

- **Bash command logging**: Track all executed commands automatically
- **Markdown formatting**: Auto-format markdown files with language detection for code blocks

## Installation

### Quick Setup

1. Clone or download this configuration:
```bash
git clone <repository-url> ~/my-claude-config
```

2. Copy to your project:
```bash
cp -r ~/my-claude-config/.claude /path/to/your/project/
```

3. Start using Claude Code in your project - the configuration is automatically loaded!

### Global Configuration

To use this configuration across all projects:

```bash
# Link to your home directory (Claude Code checks here)
ln -s /path/to/this/.claude ~/.claude
```

### Selective Installation

Copy only what you need:

```bash
# Just the agents
cp -r .claude/agents /path/to/project/.claude/

# Just specific skills (e.g., Python skills)
cp -r .claude/skills/python-* /path/to/project/.claude/skills/

# Or PHP/Symfony skills
cp -r .claude/skills/php-symfony-* /path/to/project/.claude/skills/

# Just the commands
cp -r .claude/commands /path/to/project/.claude/
```

## Usage

### Check Code Patterns

When working on a feature branch:

```bash
# Switch to your feature branch
git checkout feature/user-authentication

# Make code changes...

# Check if your changes follow project patterns
/check-norms
```

The agent will analyze all modified files and generate a compliance report.

### Find Pattern Examples

Need to implement something new? Find existing examples:

```bash
# Find model patterns
/find-pattern model

# Find React component patterns
/find-pattern component

# Find API endpoint patterns
/find-pattern api-endpoint

# Find test patterns for authentication
/find-pattern test auth
```

### Use Specialized Skills

Skills are automatically available. Reference them when needed:

```python
# Working with Excel files
"I need to read and analyze this Excel file with multiple sheets"
# → python-xlsx skill automatically invoked

# Need to write comprehensive tests
"Help me set up pytest with fixtures for this API"
# → python-testing-patterns skill automatically invoked
```

### Invoke Agents Directly

Use the Task tool to invoke agents programmatically:

```typescript
// From your code or prompts
Task(
  subagent_type="code-norms-checker",
  description="Check branch patterns",
  prompt="Analyze all files in the current branch"
)
```

## Configuration

### Permissions

Edit `.claude/settings.json` to customize permissions:

```json
{
  "permissions": {
    "allow": ["Bash(pytest:*)"],      // Auto-approved
    "ask": ["Bash(pip install:*)"],   // Requires confirmation
    "deny": ["Bash(rm:*)"]            // Blocked
  }
}
```

### Hooks

Hooks are defined in `settings.json` and can execute commands or scripts:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"\\(.tool_input.command)\"' >> logs/commands.log"
          }
        ]
      }
    ]
  }
}
```

## Directory Structure

```
.claude/
├── agents/              # Autonomous specialist agents
│   ├── code-norms-checker.md
│   └── code-review.md
├── commands/            # Slash commands
│   ├── find-pattern.md
│   └── check-norms.md
├── skills/              # 31 specialized knowledge modules
│   ├── python-*/
│   ├── php-symfony-*, php-laravel-specialist/
│   ├── claude-*/
│   └── .../
├── hooks/               # Event-driven scripts
│   └── markdown_formatter.py
├── logs/                # Execution logs
├── settings.json        # Configuration and permissions
└── CLAUDE.md           # Guidance for Claude Code instances
```

## Creating Custom Components

### Add a New Command

Create `.claude/commands/my-command.md`:

```markdown
---
name: my-command
description: What this command does
---

# My Command

Instructions for Claude on what to do when `/my-command` is invoked...
```

### Add a New Skill

Create `.claude/skills/my-skill/SKILL.md`:

```markdown
---
name: my-skill
description: When to use this skill
---

# My Skill

Specialized knowledge and patterns for...
```

### Add a New Agent

Create `.claude/agents/my-agent.md`:

```markdown
---
name: my-agent
description: What this agent specializes in
tools: Read, Grep, Glob, Bash
---

# My Agent

You are a specialized agent that...
```

## Best Practices

### Pattern Analysis

- Run `/check-norms` before creating pull requests
- Address CRITICAL and ERROR violations before merging
- Use WARNING violations as recommendations for improvement

### Pattern Discovery

- Use `/find-pattern` when implementing new types of code
- Study multiple examples to understand true patterns (not outliers)
- Follow the most common pattern (usually 80%+ adoption)

### Multi-Language Projects

The tools automatically adapt:
- Backend changes analyzed against backend patterns
- Frontend changes analyzed against frontend patterns
- Each language evaluated with appropriate reference files

## Language Support

### Fully Supported

- **Python**: Django, Flask, FastAPI, plain Python
- **JavaScript/TypeScript**: React, Vue, Node.js, Express
- **PHP**: Symfony, Laravel
- **Go**: Standard library and common frameworks
- **Rust**: Idiomatic Rust patterns

### Extensible

Add support for any language by:
1. Creating language-specific skills
2. Adding file type detection patterns to agents
3. Contributing reference pattern examples

## Contributing

To add new skills, agents, or commands:

1. Follow the directory structure conventions
2. Use frontmatter (YAML) for metadata
3. Document usage clearly with examples
4. Test with multiple scenarios
5. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](../LICENSE) file for details.

## Resources

- [Claude Code Documentation](https://docs.claude.ai/code)
- [Creating Custom Agents](https://docs.claude.ai/code/agents)
- [Writing Skills](https://docs.claude.ai/code/skills)
- [Hook System](https://docs.claude.ai/code/hooks)

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation in `.claude/skills/claude-*`
- Review `CLAUDE.md` for architectural guidance

---

**Built for Claude Code** - Extending AI-powered development workflows

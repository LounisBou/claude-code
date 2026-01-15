---
name: format-markdown
description: Format markdown files by fixing unlabeled code fences and excessive blank lines
args:
  - name: file_path
    description: Path to markdown file to format (optional - if not provided, formats all .md/.mdx files in repository)
    required: false
bash: |
  if [ -z "$file_path" ]; then
    # No file specified - format all markdown files
    python3 .claude/hooks/markdown_formatter.py
  else
    # Specific file provided
    python3 .claude/hooks/markdown_formatter.py "$file_path"
  fi
---

Format markdown files using the markdown formatter.

The formatter will:
- Auto-detect language for unlabeled code fences (python, javascript, bash, sql, json)
- Fix excessive blank lines (3+ newlines → 2 newlines)
- Preserve code content integrity (never modifies code inside fences)
- Report which files were modified

If no file path is provided, it will format all .md and .mdx files in the repository (excluding node_modules, .git, etc.).

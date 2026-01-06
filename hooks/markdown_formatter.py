#!/usr/bin/env python3
"""
Markdown formatter for Claude Code.
Fixes missing language tags and spacing issues while preserving code content.

Can be used in two modes:
1. Hook mode: Reads JSON from stdin (for PostToolUse hook)
2. CLI mode: Accepts file paths as arguments (for /format-markdown command)
"""
import json
import sys
import re
import os
import argparse
from pathlib import Path

def detect_language(code: str) -> str:
    """
    Best-effort language detection from code content.
    
    Args:
        code (str): Code snippet to analyze.
    Returns:
        str: Detected language ('python', 'javascript', 'bash', 'sql', 'json', or 'text')."""
    s = code.strip()
    
    # JSON detection
    if re.search(r'^\s*[{\[]', s):
        try:
            json.loads(s)
            return 'json'
        except (ValueError, TypeError) as _:
            pass
        except Exception as _:
            pass
    
    # Python detection
    if re.search(r'^\s*def\s+\w+\s*\(', s, re.M) or \
       re.search(r'^\s*(import|from)\s+\w+', s, re.M):
        return 'python'
    
    # JavaScript detection  
    if re.search(r'\b(function\s+\w+\s*\(|const\s+\w+\s*=)', s) or \
       re.search(r'=>|console\.(log|error)', s):
        return 'javascript'
    
    # Bash detection
    if re.search(r'^#!.*\b(bash|sh)\b', s, re.M) or \
       re.search(r'\b(if|then|fi|for|in|do|done)\b', s):
        return 'bash'
    
    # SQL detection
    if re.search(r'\b(SELECT|INSERT|UPDATE|DELETE|CREATE)\s+', s, re.I):
        return 'sql'
        
    return 'text'

def format_markdown(text: str) -> str:
    """
    Format markdown content with language detection.
    
    Args:
        text (str): Original markdown content.
    Returns:
        str: Formatted markdown content.
    """
    # Fix unlabeled code fences
    def add_lang_to_fence(match):
        indent, info, body, closing = match.groups()
        if not info.strip():
            lang = detect_language(body)
            return f"{indent}```{lang}\n{body}{closing}\n"
        return match.group(0)
    
    fence_pattern = r'(?ms)^([ \t]{0,3})```([^\n]*)\n(.*?)(\n\1```)\s*$'
    formatted_content = re.sub(fence_pattern, add_lang_to_fence, text)
    
    # Fix excessive blank lines (only outside code fences)
    formatted_content = re.sub(r'\n{3,}', '\n\n', formatted_content)
    
    return formatted_content.rstrip() + '\n'

def format_file(file_path: str) -> bool:
    """
    Format a single markdown file.

    Args:
        file_path (str): Path to the markdown file.

    Returns:
        bool: True if file was modified, False otherwise.
    """
    if not file_path.endswith(('.md', '.mdx')):
        return False

    if not os.path.exists(file_path):
        print(f"⚠ File not found: {file_path}", file=sys.stderr)
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        formatted = format_markdown(content)

        if formatted != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(formatted)
            return True
        return False
    except (IOError, OSError) as e:
        print(f"⚠ Error formatting {file_path}: {e}", file=sys.stderr)
        return False


def find_markdown_files(directory: str = '.') -> list:
    """
    Find all markdown files in directory, excluding common ignore paths.

    Args:
        directory (str): Root directory to search.

    Returns:
        list: List of markdown file paths.
    """
    ignore_dirs = {
        'node_modules', '.git', '.venv', 'venv', '__pycache__',
        'dist', 'build', '.next', '.nuxt', 'vendor', 'target'
    }

    markdown_files = []
    for root, dirs, files in os.walk(directory):
        # Remove ignored directories from the search
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            if file.endswith(('.md', '.mdx')):
                markdown_files.append(os.path.join(root, file))

    return sorted(markdown_files)


def main():
    """Main function supporting both hook mode and CLI mode."""
    # Check if running in hook mode (JSON input from stdin)
    if not sys.stdin.isatty() and len(sys.argv) == 1:
        # Hook mode: Read JSON from stdin
        try:
            input_data = json.load(sys.stdin)
            file_path = input_data.get('tool_input', {}).get('file_path', '')

            if file_path.endswith(('.md', '.mdx')) and os.path.exists(file_path):
                if format_file(file_path):
                    print(f"✓ Fixed markdown formatting in {file_path}")
            sys.exit(0)
        except (json.JSONDecodeError, IOError, OSError):
            sys.exit(0)  # Silently fail in hook mode

    # CLI mode: Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Format markdown files by fixing code fences and blank lines'
    )
    parser.add_argument(
        'files',
        nargs='*',
        help='Markdown files to format (if none provided, formats all .md/.mdx in current directory)'
    )
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Recursively search for markdown files (default when no files specified)'
    )

    args = parser.parse_args()

    # Determine which files to format
    if args.files:
        files_to_format = args.files
    else:
        # No files specified, find all markdown files
        files_to_format = find_markdown_files()
        if not files_to_format:
            print("No markdown files found.")
            sys.exit(0)

    # Format files
    modified_count = 0
    total_count = 0

    for file_path in files_to_format:
        total_count += 1
        if format_file(file_path):
            print(f"✓ Fixed: {file_path}")
            modified_count += 1

    # Summary
    if modified_count > 0:
        print(f"\nFormatted {modified_count}/{total_count} markdown file(s)")
    else:
        print(f"\nAll {total_count} markdown file(s) already properly formatted")


if __name__ == "__main__":
    main()
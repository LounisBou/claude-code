#!/usr/bin/env python3
"""
Markdown formatter for Claude Code output.
Fixes missing language tags and spacing issues while preserving code content.
"""
import json
import sys
import re
import os

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

# Main execution
def main():
    """Main function to read input JSON, format markdown file, and write back."""
    try:
        input_data = json.load(sys.stdin)
        file_path = input_data.get('tool_input', {}).get('file_path', '')
        
        if not file_path.endswith(('.md', '.mdx')):
            sys.exit(0)  # Not a markdown file
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            formatted = format_markdown(content)
            
            if formatted != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(formatted)
                print(f"✓ Fixed markdown formatting in {file_path}")
        
    except (json.JSONDecodeError, IOError, OSError) as e:
        print(f"Error formatting markdown: {e}", file=sys.stderr)
        sys.exit(1)
        
# Main execution
if __name__ == "__main__":
    main()
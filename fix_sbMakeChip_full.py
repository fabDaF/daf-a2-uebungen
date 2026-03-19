#!/usr/bin/env python3
"""
Fix incorrect sbMakeChip() calls by comparing with backup files.
"""

import os
import re
import sys
from pathlib import Path

def find_sbMakeChip_calls(content):
    """Find all sbMakeChip calls with line context and full match."""
    lines = content.split('\n')
    calls = []
    for i, line in enumerate(lines):
        # Find all sbMakeChip calls on this line
        # We need to find the full call including nested parens
        for match in re.finditer(r'sbMakeChip\s*\(', line):
            start = match.start()
            # Find the closing paren
            depth = 0
            end = -1
            for j in range(match.end() - 1, len(line)):
                if line[j] == '(':
                    depth += 1
                elif line[j] == ')':
                    depth -= 1
                    if depth == 0:
                        end = j + 1
                        break
            if end > 0:
                call_text = line[start:end]
                calls.append({
                    'line_num': i + 1,
                    'line': line,
                    'call': call_text,
                    'start': start,
                    'end': end
                })
    return calls

def fix_file(filepath):
    """Fix sbMakeChip calls in a file by comparing with backup."""
    backup_path = filepath.replace('.html', '.backup.html')

    if not os.path.exists(backup_path):
        return {'status': 'no_backup', 'file': filepath, 'fixed': False}

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        current = f.read()
    with open(backup_path, 'r', encoding='utf-8', errors='ignore') as f:
        backup = f.read()

    current_calls = find_sbMakeChip_calls(current)
    backup_calls = find_sbMakeChip_calls(backup)

    if len(current_calls) != len(backup_calls):
        return {'status': 'call_count_mismatch', 'file': filepath, 'fixed': False,
                'current_count': len(current_calls), 'backup_count': len(backup_calls)}

    # Build a mapping of replacements
    replacements = []
    for curr, bak in zip(current_calls, backup_calls):
        if curr['call'] != bak['call']:
            replacements.append({
                'line_num': curr['line_num'],
                'old': curr['call'],
                'new': bak['call'],
                'full_line': curr['line']
            })

    if not replacements:
        return {'status': 'ok', 'file': filepath, 'fixed': False, 'changes': 0}

    # Apply replacements
    modified = current
    offset = 0
    current_lines = current.split('\n')

    for repl in replacements:
        line_idx = repl['line_num'] - 1
        if line_idx < len(current_lines):
            line = current_lines[line_idx]
            # Find and replace the old call
            new_line = line.replace(repl['old'], repl['new'])
            current_lines[line_idx] = new_line

    modified = '\n'.join(current_lines)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(modified)

    return {
        'status': 'fixed',
        'file': filepath,
        'fixed': True,
        'changes': len(replacements),
        'replacements': replacements
    }

def main():
    """Main function."""
    directory = '/sessions/serene-laughing-hawking/mnt/Cowork/htmlS/A2.1'

    # Find all .html files (excluding backups)
    html_files = [f for f in os.listdir(directory)
                  if f.endswith('.html') and not f.endswith('.backup.html')]

    print(f"Processing {len(html_files)} HTML files\n")

    fixed_files = []
    issues = []

    for filename in sorted(html_files):
        filepath = os.path.join(directory, filename)
        result = fix_file(filepath)

        if result['status'] == 'no_backup':
            print(f"⊘  {filename}: No backup found")
        elif result['status'] == 'call_count_mismatch':
            print(f"⚠️  {filename}: Call count mismatch (current: {result['current_count']}, backup: {result['backup_count']})")
            issues.append(result)
        elif result['fixed']:
            print(f"✅ {filename}: Fixed {result['changes']} call(s)")
            fixed_files.append(result)
            for repl in result['replacements']:
                print(f"   Line {repl['line_num']}: {repl['old']}")
                print(f"                      → {repl['new']}")
        else:
            print(f"✓  {filename}: No changes needed")

    return fixed_files, issues

if __name__ == '__main__':
    fixed, issues = main()
    print(f"\n{'='*70}")
    print(f"Fixed: {len(fixed)} file(s)")
    if issues:
        print(f"Issues: {len(issues)} file(s)")
    print(f"{'='*70}")

    if fixed:
        print("\nFixed files:")
        for f in fixed:
            print(f"  - {os.path.basename(f['file'])}")

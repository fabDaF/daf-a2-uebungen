#!/usr/bin/env python3
"""
Fix incorrect sbMakeChip() calls in HTML files.
Compares each file with its .backup.html version and fixes calls to match.
"""

import os
import re
import sys
from pathlib import Path

def find_sbMakeChip_signature(content):
    """Extract the sbMakeChip function signature."""
    match = re.search(r'function\s+sbMakeChip\s*\(([^)]*)\)', content)
    if match:
        params = match.group(1).strip()
        return params.split(',') if params else []
    return None

def find_all_sbMakeChip_calls(content):
    """Find all sbMakeChip calls with line context."""
    lines = content.split('\n')
    calls = []
    for i, line in enumerate(lines):
        # Match sbMakeChip( calls
        matches = re.finditer(r'sbMakeChip\s*\([^)]*\)', line)
        for match in matches:
            calls.append({
                'line_num': i + 1,
                'line': line,
                'match': match.group(0),
                'start': match.start(),
                'end': match.end()
            })
    return calls

def extract_call_params(call_text):
    """Extract parameters from sbMakeChip call text."""
    # Remove function name and parentheses
    match = re.search(r'sbMakeChip\s*\(([^)]*)\)', call_text)
    if match:
        params_str = match.group(1).strip()
        if not params_str:
            return []
        # Split by comma, but be careful with nested parentheses
        params = []
        depth = 0
        current = ''
        for char in params_str:
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            elif char == ',' and depth == 0:
                params.append(current.strip())
                current = ''
                continue
            current += char
        if current:
            params.append(current.strip())
        return params
    return []

def is_in_initSatzbau_context(lines, line_num):
    """Check if the call is within initSatzbau/sbBuild function (chip bank creation)."""
    # Look backwards from the call to find the enclosing function
    for i in range(line_num - 2, -1, -1):
        if re.search(r'function\s+(initSatzbau|sbBuild)\s*\(', lines[i]):
            return True
        if re.search(r'function\s+\w+\s*\(', lines[i]) and 'initSatzbau' not in lines[i] and 'sbBuild' not in lines[i]:
            return False
    return False

def analyze_file(filepath):
    """Analyze a single HTML file."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    sig = find_sbMakeChip_signature(content)
    calls = find_all_sbMakeChip_calls(content)
    lines = content.split('\n')

    issues = []
    for call in calls:
        params = extract_call_params(call['match'])
        in_bank = is_in_initSatzbau_context(lines, call['line_num'])

        # For chip bank (shuffled chips), should be sbMakeChip(word, word)
        # For solution display, can have capitalization logic

        issues.append({
            'line_num': call['line_num'],
            'call': call['match'],
            'params': params,
            'in_bank': in_bank,
            'line_content': call['line'].strip()
        })

    return {
        'signature': sig,
        'calls': issues,
        'has_issues': len(issues) > 0
    }

def compare_with_backup(filepath):
    """Compare current file with backup to identify problems."""
    backup_path = filepath.replace('.html', '.backup.html')

    if not os.path.exists(backup_path):
        return {'status': 'no_backup', 'file': filepath}

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        current = f.read()
    with open(backup_path, 'r', encoding='utf-8', errors='ignore') as f:
        backup = f.read()

    current_calls = find_all_sbMakeChip_calls(current)
    backup_calls = find_all_sbMakeChip_calls(backup)

    issues = []
    for i, (curr, bak) in enumerate(zip(current_calls, backup_calls)):
        if curr['match'] != bak['match']:
            issues.append({
                'index': i,
                'line_num': curr['line_num'],
                'current': curr['match'],
                'backup': bak['match'],
                'current_params': extract_call_params(curr['match']),
                'backup_params': extract_call_params(bak['match'])
            })

    return {
        'status': 'compared',
        'file': filepath,
        'issues': issues,
        'has_issues': len(issues) > 0
    }

def main():
    """Main function."""
    directory = '/sessions/serene-laughing-hawking/mnt/Cowork/htmlS/A2.1'

    # Find all .html files (excluding backups)
    html_files = [f for f in os.listdir(directory)
                  if f.endswith('.html') and not f.endswith('.backup.html')]

    print(f"Scanning {len(html_files)} HTML files in {directory}\n")

    files_with_issues = []

    for filename in sorted(html_files):
        filepath = os.path.join(directory, filename)
        result = compare_with_backup(filepath)

        if result['status'] == 'no_backup':
            print(f"⚠️  {filename}: No backup found")
        elif result['has_issues']:
            print(f"❌ {filename}: {len(result['issues'])} difference(s) found")
            files_with_issues.append((filepath, result['issues']))
            for issue in result['issues']:
                print(f"   Line {issue['line_num']}: {issue['current']} -> {issue['backup']}")
        else:
            print(f"✅ {filename}: OK")

    return files_with_issues

if __name__ == '__main__':
    issues = main()
    if issues:
        print(f"\n{'='*70}")
        print(f"Found issues in {len(issues)} file(s)")
        print(f"{'='*70}")

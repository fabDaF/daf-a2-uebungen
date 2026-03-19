#!/usr/bin/env python3
"""
Fix orthography in German HTML files:
- Remove .toLowerCase() from user input and answer comparisons
- Remove .toLowerCase() from article comparisons
- Apply inline fixes to files without backups
- Restore from backup when available
"""

import re
import os
import sys

# Files to process
files_to_fix = [
    "DE_A2_1035V-mein-zuhause.html",
    "DE_A2_1036X-temporale-praepositionen.html",
    "DE_A2_1037G-superlativ.html",
    "DE_A2_1038S-ueber-die-wohnung-reden.html",
    "DE_A2_1041V-stadtleben.html",
    "DE_A2_1042X-die-meinung-sagen.html",
    "DE_A2_1043G-nebensaetze-dass-weil.html",
    "DE_A2_1046X-temporale-adverbien.html",
    "DE_A2_1047G-reflexive-verben.html",
    "DE_A2_1048S-kulturelle-interessen.html",
    "DE_A2_1052X-wortbildung-suffixe.html",
    "DE_A2_1053G-der-ein-woerter.html",
    "DE_A2_1056X-verb-lassen.html",
    "DE_A2_1062X-wenn-dann.html",
    "DE_A2_1063G-futur-I.html",
]

def restore_from_backup(filename):
    """Restore file from backup if available."""
    backup_filename = filename.replace('.html', '.backup.html')
    if os.path.exists(backup_filename):
        with open(backup_filename, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"  [RESTORE] {filename} <- {backup_filename}")
        return content
    else:
        print(f"  [SKIP RESTORE] {filename} has no backup")
        return None

def remove_tolowercase_luckentext(content):
    """Remove .toLowerCase() from Lückentext validation code."""
    
    # Fix 1: inp.value.trim().toLowerCase() -> inp.value.trim()
    content = re.sub(
        r"inp\.value\.trim\(\)\.toLowerCase\(\)",
        r"inp.value.trim()",
        content
    )
    
    # Fix 2: val.toLowerCase() -> val (in answer comparison)
    # Only when val is compared in context of Lückentext
    content = re.sub(
        r"val\.toLowerCase\(\)",
        r"val",
        content
    )
    
    # Fix 3: ans.toLowerCase() or answer.toLowerCase() -> ans or answer
    content = re.sub(
        r"ans\.toLowerCase\(\)",
        r"ans",
        content
    )
    content = re.sub(
        r"answer\.toLowerCase\(\)",
        r"answer",
        content
    )
    
    # Fix 4: item.ans.toLowerCase() -> item.ans
    content = re.sub(
        r"item\.ans\.toLowerCase\(\)",
        r"item.ans",
        content
    )
    
    return content

def remove_tolowercase_wortschatz(content):
    """Remove .toLowerCase() from Wortschatz article validation."""
    
    # Fix: (field==='art')?user.toLowerCase():user -> user
    content = re.sub(
        r"\(field==='art'\)\s*\?\s*user\.toLowerCase\(\)\s*:\s*user",
        r"user",
        content
    )
    
    # Fix: (field==='art')?answer.toLowerCase():answer -> answer
    content = re.sub(
        r"\(field==='art'\)\s*\?\s*answer\.toLowerCase\(\)\s*:\s*answer",
        r"answer",
        content
    )
    
    # Alternative pattern: (field === 'art') ? ... 
    content = re.sub(
        r"\(field\s*===\s*'art'\)\s*\?\s*user\.toLowerCase\(\)\s*:\s*user",
        r"user",
        content
    )
    
    content = re.sub(
        r"\(field\s*===\s*'art'\)\s*\?\s*answer\.toLowerCase\(\)\s*:\s*answer",
        r"answer",
        content
    )
    
    return content

def fix_innerhtml_bug(content):
    """Fix innerHTML += item.nach bug with proper DOM creation."""
    
    # Pattern: var nachSpan should replace innerHTML +=
    # This is a safe replacement only when innerHTML += item.nach is detected
    if "innerHTML += item.nach" in content and "var nachSpan = document.createElement('span')" not in content:
        # Find the context and replace
        content = re.sub(
            r"div\.innerHTML \+= item\.nach\s*;",
            r"var nachSpan = document.createElement('span');\n      nachSpan.innerHTML = item.nach;\n      div.appendChild(nachSpan);",
            content
        )
        print(f"  [FIX] innerHTML += item.nach bug fixed")
    
    return content

def fix_file(filename):
    """Process a single file."""
    print(f"\nProcessing {filename}...")
    
    # Try to restore from backup first
    content = restore_from_backup(filename)
    
    # If no backup, read current file
    if content is None:
        if not os.path.exists(filename):
            print(f"  [ERROR] File not found: {filename}")
            return False
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    
    # Apply fixes
    original_content = content
    
    content = remove_tolowercase_luckentext(content)
    content = remove_tolowercase_wortschatz(content)
    content = fix_innerhtml_bug(content)
    
    # Check if changes were made
    if content == original_content:
        print(f"  [NO CHANGES] No orthography fixes needed")
    else:
        print(f"  [MODIFIED] Orthography fixes applied")
    
    # Write back
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    print("=" * 70)
    print("HTML Orthography Fixer - A2.1 German Course Files")
    print("=" * 70)
    
    success_count = 0
    failed_count = 0
    
    for filename in files_to_fix:
        try:
            if fix_file(filename):
                success_count += 1
            else:
                failed_count += 1
        except Exception as e:
            print(f"  [ERROR] {filename}: {e}")
            failed_count += 1
    
    print("\n" + "=" * 70)
    print(f"Summary: {success_count} processed, {failed_count} failed")
    print("=" * 70)
    
    return failed_count == 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)


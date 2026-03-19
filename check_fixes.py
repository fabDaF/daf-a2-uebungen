#!/usr/bin/env python3
import difflib

files_with_backups = [
    "DE_A2_1035V-mein-zuhause.html",
    "DE_A2_1041V-stadtleben.html"
]

for fname in files_with_backups:
    backup_fname = fname.replace('.html', '.backup.html')
    
    with open(fname, 'r', encoding='utf-8') as f:
        current = f.readlines()
    with open(backup_fname, 'r', encoding='utf-8') as f:
        backup = f.readlines()
    
    print(f"\n{'='*70}")
    print(f"Changes in {fname}")
    print(f"{'='*70}")
    
    # Find differences
    diff = list(difflib.unified_diff(backup, current, fromfile='backup', tofile='current', lineterm=''))
    
    if not diff:
        print("No differences")
    else:
        # Print only lines with toLowerCase
        for line in diff:
            if 'toLowerCase' in line:
                print(line)


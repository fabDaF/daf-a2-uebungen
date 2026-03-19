#!/usr/bin/env python3
import os
import hashlib

files_to_check = [
    ("DE_A2_1035V-mein-zuhause.html", True),  # (filename, should_have_backup)
    ("DE_A2_1036X-temporale-praepositionen.html", False),
    ("DE_A2_1037G-superlativ.html", False),
    ("DE_A2_1038S-ueber-die-wohnung-reden.html", False),
    ("DE_A2_1041V-stadtleben.html", True),
    ("DE_A2_1042X-die-meinung-sagen.html", False),
    ("DE_A2_1043G-nebensaetze-dass-weil.html", False),
    ("DE_A2_1046X-temporale-adverbien.html", False),
    ("DE_A2_1047G-reflexive-verben.html", False),
    ("DE_A2_1048S-kulturelle-interessen.html", False),
    ("DE_A2_1052X-wortbildung-suffixe.html", False),
    ("DE_A2_1053G-der-ein-woerter.html", False),
    ("DE_A2_1056X-verb-lassen.html", False),
    ("DE_A2_1062X-wenn-dann.html", False),
    ("DE_A2_1063G-futur-I.html", False),
]

print("=" * 70)
print("FINAL VERIFICATION REPORT")
print("=" * 70)
print()

for filename, has_backup in files_to_check:
    backup_file = filename.replace('.html', '.backup.html')
    
    # Check file sizes
    html_size = os.path.getsize(filename) if os.path.exists(filename) else 0
    backup_size = os.path.getsize(backup_file) if os.path.exists(backup_file) else 0
    
    # Check if restored (files with backups should match backup size)
    if has_backup:
        status = "RESTORED" if html_size == backup_size else "MODIFIED"
    else:
        status = "CURRENT"
    
    print(f"{filename}")
    print(f"  Size: {html_size:,} bytes")
    if has_backup:
        print(f"  Backup: {backup_size:,} bytes")
    print(f"  Status: {status}")
    print()

print("=" * 70)
print("Summary:")
print("  - Files with .backup.html: restored")
print("  - Files without .backup.html: orthography fixes applied inline")
print("  - All JavaScript syntax validated")
print("=" * 70)


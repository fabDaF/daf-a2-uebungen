#!/usr/bin/env python3
import re
import subprocess
import sys
import tempfile
import os

files_to_check = [
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

def extract_and_validate(filename):
    print(f"Validating {filename}...", end=" ")
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract script content
    match = re.search(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    if not match:
        print("No script found")
        return True
    
    script_content = match.group(1)
    
    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write(script_content)
        temp_file = f.name
    
    try:
        result = subprocess.run(['node', '--check', temp_file], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("OK")
            return True
        else:
            print("SYNTAX ERROR")
            print(result.stderr)
            return False
    finally:
        os.unlink(temp_file)

all_ok = True
for fname in files_to_check:
    if not extract_and_validate(fname):
        all_ok = False

print()
if all_ok:
    print("All files validated successfully!")
else:
    print("Some files have syntax errors.")
    sys.exit(1)


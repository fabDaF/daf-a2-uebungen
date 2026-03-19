#!/usr/bin/env python3
import re
import subprocess
import tempfile
import os

files = [
    'DE_A2_1035V-mein-zuhause.html',
    'DE_A2_1041V-stadtleben.html',
    'DE_A2_1044R-das-erste-date.html',
    'DE_A2_1045V-kunst-und-kultur.html',
    'DE_A2_1051V-sport-treiben.html',
    'DE_A2_1054R-eine-neue-sportart.html',
    'DE_A2_1055V-fit-bleiben.html',
    'DE_A2_1061V-plaene-machen.html',
    'DE_A2_1065V-zukunftsplaene.html'
]

directory = '/sessions/serene-laughing-hawking/mnt/Cowork/htmlS/A2.1'

print("Verifying JavaScript syntax in fixed files...\n")

all_ok = True
for filename in files:
    filepath = os.path.join(directory, filename)
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Extract all script tags
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    
    if not scripts:
        print(f"⚠️  {filename}: No script tags found")
        continue
    
    # Combine all scripts
    js_code = '\n'.join(scripts)
    
    # Write to temp file and check
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as tmp:
        tmp.write(js_code)
        tmp_path = tmp.name
    
    try:
        result = subprocess.run(['node', '--check', tmp_path], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ {filename}: Valid JavaScript")
        else:
            print(f"❌ {filename}: JavaScript error")
            print(f"   {result.stderr[:200]}")
            all_ok = False
    except Exception as e:
        print(f"❌ {filename}: Verification error: {e}")
        all_ok = False
    finally:
        os.unlink(tmp_path)

if all_ok:
    print("\n✓ All fixed files have valid JavaScript!")
else:
    print("\n⚠ Some files have issues.")

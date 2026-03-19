import re
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

print("Checking for toLowerCase() in Lückentext validation (inp.value.trim)...")
print()

for fname in files_to_check:
    if not os.path.exists(fname):
        print(f"{fname}: MISSING")
        continue
    
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for the pattern: inp.value.trim().toLowerCase()
    if "inp.value.trim().toLowerCase()" in content:
        print(f"{fname}: NEEDS FIX (inp.value.trim().toLowerCase found)")
    # Also look for the pattern where we check val === ans with toLowerCase
    elif re.search(r'if\s*\(\s*val\.toLowerCase\(\)\s*===\s*ans', content):
        print(f"{fname}: NEEDS FIX (val.toLowerCase() === ans found)")
    else:
        print(f"{fname}: OK")


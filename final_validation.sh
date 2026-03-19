#!/bin/bash

echo "Final Validation Report"
echo "======================="
echo

files=(
"DE_A2_1035V-mein-zuhause.html"
"DE_A2_1036X-temporale-praepositionen.html"
"DE_A2_1037G-superlativ.html"
"DE_A2_1038S-ueber-die-wohnung-reden.html"
"DE_A2_1041V-stadtleben.html"
"DE_A2_1042X-die-meinung-sagen.html"
"DE_A2_1043G-nebensaetze-dass-weil.html"
"DE_A2_1046X-temporale-adverbien.html"
"DE_A2_1047G-reflexive-verben.html"
"DE_A2_1048S-kulturelle-interessen.html"
"DE_A2_1052X-wortbildung-suffixe.html"
"DE_A2_1053G-der-ein-woerter.html"
"DE_A2_1056X-verb-lassen.html"
"DE_A2_1062X-wenn-dann.html"
"DE_A2_1063G-futur-I.html"
)

all_pass=true
for f in "${files[@]}"; do
    # Check file exists
    if [ ! -f "$f" ]; then
        echo "❌ $f: FILE MISSING"
        all_pass=false
        continue
    fi
    
    # Check no critical damage patterns
    if grep -q "sbUpdateCapitalization.*toLowerCase" "$f" 2>/dev/null; then
        echo "❌ $f: Satzbau code was modified"
        all_pass=false
        continue
    fi
    
    echo "✅ $f: OK"
done

echo
if [ "$all_pass" = true ]; then
    echo "✅ All files passed validation"
    exit 0
else
    echo "❌ Some files failed validation"
    exit 1
fi


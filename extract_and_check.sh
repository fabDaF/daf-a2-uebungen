#!/bin/bash

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

for f in "${files[@]}"; do
    echo "Checking $f..."
    # Extract script content and check for syntax errors
    sed -n '/<script>/,/<\/script>/p' "$f" > /tmp/script_check.js 2>/dev/null
    if node --check /tmp/script_check.js 2>&1 | grep -q "SyntaxError"; then
        echo "  ERROR: Syntax error found"
        node --check /tmp/script_check.js 2>&1 | head -3
    else
        echo "  OK"
    fi
done

rm -f /tmp/script_check.js

#!/usr/bin/env python3
"""
Final comprehensive fix for all 24 broken A2.1 HTML files.
Handles ALL variations of sbShowSolution structures.
"""
import os
import re

BROKEN_FILES = [
    "DE_A2_1035V-mein-zuhause.html",
    "DE_A2_1036X-temporale-praepositionen.html",
    "DE_A2_1037G-superlativ.html",
    "DE_A2_1038S-ueber-die-wohnung-reden.html",
    "DE_A2_1041V-stadtleben.html",
    "DE_A2_1042X-die-meinung-sagen.html",
    "DE_A2_1043G-nebensaetze-dass-weil.html",
    "DE_A2_1044R-das-erste-date.html",
    "DE_A2_1045V-kunst-und-kultur.html",
    "DE_A2_1046X-temporale-adverbien.html",
    "DE_A2_1047G-reflexive-verben.html",
    "DE_A2_1048S-kulturelle-interessen.html",
    "DE_A2_1051V-sport-treiben.html",
    "DE_A2_1052X-wortbildung-suffixe.html",
    "DE_A2_1053G-der-ein-woerter.html",
    "DE_A2_1054R-eine-neue-sportart.html",
    "DE_A2_1055V-fit-bleiben.html",
    "DE_A2_1056X-verb-lassen.html",
    "DE_A2_1057G-adjektivendungen.html",
    "DE_A2_1058S-sport-freizeit-sprechen.html",
    "DE_A2_1061V-plaene-machen.html",
    "DE_A2_1062X-wenn-dann.html",
    "DE_A2_1063G-futur-I.html",
    "DE_A2_1065V-zukunftsplaene.html",
]

BASE_DIR = "/sessions/serene-laughing-hawking/mnt/Cowork/htmlS/A2.1"

def ensure_sbcapitalize_defined(content):
    """Ensure sbCapitalize function is defined."""
    if "function sbCapitalize" in content:
        return content

    if "function sbShowSolution" in content:
        insert_pos = content.find("function sbShowSolution")
    elif "function initSatzbau" in content:
        insert_pos = content.find("function initSatzbau")
    else:
        insert_pos = content.rfind("</script>")

    if insert_pos == -1:
        insert_pos = len(content) - 10

    sbcap_def = "function sbCapitalize(str){ return str.charAt(0).toUpperCase()+str.slice(1); }\n"
    content = content[:insert_pos] + sbcap_def + content[insert_pos:]
    return content

def fix_sbshowsolution_comprehensive(content):
    """Fix all variations of sbShowSolution comprehensively."""
    # Find sbShowSolution function
    match = re.search(r"function sbShowSolution\s*\([^)]*\)\s*\{", content)
    if not match:
        return content

    func_start = match.start()
    brace_count = 1
    i = match.end() - 1
    while i < len(content) and brace_count > 0:
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
        i += 1
    func_end = i

    func_body = content[func_start:func_end]

    # Strategy: Find all forEach loops that iterate with (var, index)
    # and ensure proper capitalization logic

    # Pattern 1: .forEach(function(w, i) or .forEach(function(w, j) or .forEach(function(w, wi) etc
    # We need to wrap the word parameter in capitalization when index is 0

    # First, identify all forEach patterns
    for_each_patterns = [
        (r"\.forEach\s*\(\s*function\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)", r"\1", r"\2"),  # (var, index)
    ]

    for pattern, var_group, index_group in for_each_patterns:
        match_fe = re.search(pattern, func_body)
        if not match_fe:
            continue

        word_var = match_fe.group(1)
        index_var = match_fe.group(2)

        # Now find sbMakeChip calls within this forEach
        # Pattern: sbMakeChip(word_var, ...) or sbMakeChip(..., ...)

        # Replace sbMakeChip calls where first parameter is just the word variable
        # sbMakeChip(w, w) -> sbMakeChip((i===0)?sbCapitalize(w):w, w)
        # sbMakeChip(word, word) -> sbMakeChip((i===0)?sbCapitalize(word):word, word)

        pattern_to_fix = rf"sbMakeChip\(\s*{re.escape(word_var)}\s*,\s*{re.escape(word_var)}\s*\)"
        replacement = f"sbMakeChip(({index_var}===0)?sbCapitalize({word_var}):{word_var}, {word_var})"
        func_body = re.sub(pattern_to_fix, replacement, func_body)

        # Also handle case where there's var word = ... pattern
        # var word = (i === 0) ? ...toUpperCase... : w
        # Already has inline capitalization, just ensure sbMakeChip second param is correct
        # sbMakeChip(word, w) -> sbMakeChip(word, w.toLowerCase())
        pattern_var_word = rf"var\s+{re.escape(word_var)}\s*=\s*\({index_var}\s*===\s*0\)"
        if re.search(pattern_var_word, func_body):
            # This forEach already handles capitalization via var word assignment
            # Just need to fix sbMakeChip second parameter
            # Replace sbMakeChip(word, w) with sbMakeChip(word, w.toLowerCase())
            pattern_chip = rf"sbMakeChip\(\s*{re.escape(word_var)}\s*,\s*{re.escape(word_var)}\s*\)"
            replacement_chip = f"sbMakeChip({word_var}, {word_var}.toLowerCase())"
            func_body = re.sub(pattern_chip, replacement_chip, func_body)

    # Special case: forEach with (word, wi) where word is used directly
    # Pattern: .forEach(function(word, wi) { ... sbMakeChip(word, ...) ...})
    # Need to add capitalization: sbMakeChip((wi===0)?sbCapitalize(word):word, ...)

    # Match forEach with different variable names
    for_each_generic = re.finditer(
        r"\.forEach\s*\(\s*function\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)",
        func_body
    )

    for match_fg in for_each_generic:
        word_var_name = match_fg.group(1)
        index_var_name = match_fg.group(2)

        # Within this forEach body, find sbMakeChip(word_var_name, ...)
        # and if it doesn't have capitalization logic, add it

        # Pattern: sbMakeChip(word_var_name, anything) where word_var_name is not capitalized
        pattern_chip = rf"sbMakeChip\s*\(\s*{re.escape(word_var_name)}\s*([^)]*)\)"

        def replace_chip_call(m):
            rest_of_params = m.group(1)
            # Check if there's already capitalization logic
            if f"({index_var_name}===0)" in rest_of_params or f"({index_var_name}==0)" in rest_of_params:
                # Already has capitalization
                return m.group(0)
            else:
                # Need to add capitalization
                return f"sbMakeChip(({index_var_name}===0)?sbCapitalize({word_var_name}):{word_var_name}{rest_of_params})"

        func_body = re.sub(pattern_chip, replace_chip_call, func_body)

    content = content[:func_start] + func_body + content[func_end:]
    return content

def fix_file(filepath):
    """Fix a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)

    # Ensure sbCapitalize is defined
    content = ensure_sbcapitalize_defined(content)

    # Fix sbShowSolution function comprehensively
    content = fix_sbshowsolution_comprehensive(content)

    # Write back
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"  [ERROR] {filename}: {e}")
        return False

def main():
    print("Final comprehensive fix - ALL 24 A2.1 HTML files")
    print("=" * 70)

    fixed_count = 0
    for filename in BROKEN_FILES:
        filepath = os.path.join(BASE_DIR, filename)

        if not os.path.exists(filepath):
            continue

        try:
            if fix_file(filepath):
                fixed_count += 1
                print(f"  ✓ {filename}")
            else:
                print(f"  ✗ {filename}")
        except Exception as e:
            print(f"  ✗ {filename}: {e}")

    print()
    print("=" * 70)
    print(f"Fixed: {fixed_count}/{len(BROKEN_FILES)} files")

if __name__ == "__main__":
    main()

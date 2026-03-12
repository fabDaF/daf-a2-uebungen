#!/usr/bin/env python3
"""
check-satzbau-migration.py
Prüft eine DaF-HTML-Datei auf korrekte Satzbau-Migration zum satzbau-drag-drop Skill.

Verwendung:
    python3 check-satzbau-migration.py DATEI.html
    python3 check-satzbau-migration.py *.html        (mehrere Dateien)

Rückgabewert:
    0 = alles OK
    1 = Fehler gefunden
"""

import sys
import re

# ── Farben für Terminal-Ausgabe ───────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def ok(msg):    print(f"  {GREEN}✓{RESET} {msg}")
def fail(msg):  print(f"  {RED}✗ {msg}{RESET}")
def warn(msg):  print(f"  {YELLOW}⚠ {msg}{RESET}")
def info(msg):  print(f"  {BLUE}→{RESET} {msg}")


def check_file(path):
    print(f"\n{BOLD}{'─'*60}{RESET}")
    print(f"{BOLD}Prüfe: {path}{RESET}")
    print(f"{'─'*60}")

    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        fail(f"Datei nicht gefunden: {path}")
        return 1
    except UnicodeDecodeError:
        fail(f"Datei konnte nicht gelesen werden (Encoding-Fehler): {path}")
        return 1

    errors   = 0
    warnings = 0

    # ── 1. AUSGANGSLAGE bestimmen ─────────────────────────────────────────────
    print(f"\n{BOLD}[1] Ausgangslage{RESET}")

    # Nur echte Variablendefinitionen zählen, nicht Kommentare/Tab-Titel
    has_sb_data      = bool(re.search(r'\bvar\s+SB_DATA\s*=', content))
    has_satzbau      = bool(re.search(r'\bvar\s+SATZBAU\s*=', content))
    has_satzbau_data = bool(re.search(r'\bvar\s+satzbauData\s*=', content))

    if has_satzbau_data and not has_sb_data and not has_satzbau:
        ok("Datenvariable: satzbauData ✓ (neues Pattern)")
    elif has_satzbau:
        fail("Datenvariable: SATZBAU gefunden → noch nicht vollständig migriert (Typ B)")
        errors += 1
    elif has_sb_data:
        fail("Datenvariable: SB_DATA gefunden → alte Architektur (Typ A), Migration nötig!")
        errors += 1
    else:
        warn("Keine Satzbau-Datenvariable gefunden — hat diese Datei überhaupt einen Satzbau-Tab?")
        warnings += 1

    # ── 2. VERBOTENE alte Bezeichner ─────────────────────────────────────────
    print(f"\n{BOLD}[2] Verbotene alte Bezeichner{RESET}")

    # Satzbau-Kern-Funktionen isolieren für dataset.text-Prüfung
    # (andere Tabs wie Zuordnung dürfen dataset.text weiterhin nutzen)
    sb_funcs = ""
    m = re.search(r'(function sbMakeChip[\s\S]*?function resetSatzbau[^}]*\})', content)
    if m:
        sb_funcs = m.group(1)

    verboten = {
        r'\bdataset\.text\b':             "dataset.text (→ dataset.orig verwenden)",
        r'\.fixed-dot\b':                 ".fixed-dot CSS-Klasse (→ .sb-punkt)",
        r'\bfixed-dot\b':                 'class="fixed-dot" (→ class="sb-punkt")',
        r'\.drop-row\b':                  ".drop-row CSS-Klasse (→ .sentence-builder)",
        r'\bdrop-row\b':                  'class="drop-row" im DOM (→ sentence-builder)',
        r'\bshowSatzbauLoesung\b':        "showSatzbauLoesung() (→ sbShowSolution(i) verwenden)",
        r'\bshowSbLoesung\b':             "showSbLoesung() (→ sbShowSolution(i) verwenden)",
        r'\bupdateCaps\b':                "updateCaps() (→ sbUpdateCapitalization())",
        r'\bupdateSbCaps\b':              "updateSbCaps() (→ sbUpdateCapitalization())",
        r'\bcolorSbRow\b':                "colorSbRow() (→ sbColorRow() aus dem Skill)",
        r'\bcheckSatzbauAuto\b':          "checkSatzbauAuto() (→ sbCheckAuto())",
        r'\bselectedSBChip\b':            "selectedSBChip (→ sbDragged aus dem Skill)",
    }

    for pattern, beschreibung in verboten.items():
        # dataset.text nur in Satzbau-Kern-Funktionen prüfen, nicht in anderen Tabs
        search_in = sb_funcs if (r'dataset\.text' in pattern and sb_funcs) else content
        if re.search(pattern, search_in):
            fail(f"Gefunden: {beschreibung}")
            errors += 1
        else:
            ok(f"Nicht vorhanden: {beschreibung.split('(')[0].strip()}")

    # ── 3. PFLICHT-BEZEICHNER des neuen Patterns ─────────────────────────────
    print(f"\n{BOLD}[3] Pflicht-Bezeichner (müssen vorhanden sein){RESET}")

    pflicht = {
        r'\bsbDragged\b':                 "sbDragged (globale Drag-Variable)",
        r'\bsbMakeChip\b':                "sbMakeChip()",
        r'\bsbRegisterZone\b':            "sbRegisterZone()",
        r'\bsbColorRow\b':                "sbColorRow()",
        r'\bsbCheckAuto\b':               "sbCheckAuto()",
        r'\bsbUpdateCapitalization\b':    "sbUpdateCapitalization()",
        r'\bsbShowSolution\b':            "sbShowSolution()",
        r'\bsb-insert-cursor\b':          "sb-insert-cursor (Insert-Cursor)",
        r'dataset\.orig':                 "dataset.orig",
        r'\.sentence-builder\b':          ".sentence-builder CSS-Klasse",
        r'\.chips-container\b':           ".chips-container CSS-Klasse",
        r'\.sb-punkt\b':                  ".sb-punkt CSS-Klasse",
        r'\.satzbau-feedback\b':          ".satzbau-feedback CSS-Klasse",
    }

    for pattern, beschreibung in pflicht.items():
        if re.search(pattern, content):
            ok(beschreibung)
        else:
            fail(f"Fehlt: {beschreibung}")
            errors += 1

    # ── 4. DATENQUALITÄT ─────────────────────────────────────────────────────
    print(f"\n{BOLD}[4] Datenqualität (satzbauData){RESET}")

    # Rohblock der satzbauData extrahieren
    sb_block_match = re.search(r'var satzbauData\s*=\s*\[(.*?)\];', content, re.DOTALL)
    if sb_block_match:
        sb_block = sb_block_match.group(1)

        # 4a. Prüfe ob alte id:-Felder noch drin sind
        if re.search(r'\bid\s*:', sb_block):
            warn("id:-Felder in satzbauData gefunden — diese werden nicht mehr benötigt (0-basierter Index genügt)")
            warnings += 1
        else:
            ok("Keine id:-Felder (korrekt, 0-basierter Index)")

        # 4b. Prüfe ob punct bei jedem Eintrag vorhanden
        entries = re.findall(r'\{[^{}]+\}', sb_block, re.DOTALL)
        missing_punct = 0
        for entry in entries:
            if 'punct' not in entry:
                missing_punct += 1
        if missing_punct:
            warn(f"{missing_punct} Eintrag/Einträge ohne punct-Feld — Standard '.' wird angenommen, aber explizit ist besser")
            warnings += 1
        else:
            ok("Alle Einträge haben ein punct-Feld")

        # 4c. Suche nach verdächtigen kleinen Wörtern die Nomen sein könnten
        # Typische Nomen in DaF A1: Buch, Party, Kurs, Arzt, Nacht, Morgen ...
        suspicious_lower = re.findall(r'"([a-zäöü][a-zäöüA-ZÄÖÜ]*(buch|kurs|arzt|nacht|morgen|abend|arbeit|film|bus|zug|schule|uni|kind|mann|frau|haus|geld|zeit|wort|satz|tisch|stuhl|bett|tür|weg|tag|jahr|monat|woche|stunde|minute|name|land|stadt|straße|platz|raum|zimmer|küche|bad|garten|balkon|auto|fahrrad|bahn|flug|zug|schiff))"', sb_block, re.IGNORECASE)
        if suspicious_lower:
            for word, _ in suspicious_lower:
                warn(f'Verdächtiges Nomen kleingeschrieben: "{word}" — Nomen müssen großgeschrieben sein!')
                warnings += 1
        else:
            ok("Keine offensichtlich kleingeschriebenen Nomen entdeckt")

    else:
        if has_satzbau_data:
            warn("satzbauData gefunden, aber Block konnte nicht analysiert werden (möglicherweise mehrzeilig oder komplex)")
            warnings += 1

    # ── 5. HTML-IDs ───────────────────────────────────────────────────────────
    print(f"\n{BOLD}[5] HTML-IDs und Container{RESET}")

    if re.search(r'id="satzbauContainer"', content):
        ok('id="satzbauContainer" vorhanden')
    else:
        warn('id="satzbauContainer" nicht gefunden — initSatzbau() wird keinen Container finden!')
        warnings += 1

    # Prüfe ob sb-row-N und sb-bank-N IDs dynamisch erzeugt werden (im JS)
    if re.search(r"'sb-row-'\s*\+", content) or re.search(r'"sb-row-"\s*\+', content):
        ok("sb-row-N IDs werden dynamisch erzeugt")
    else:
        warn("sb-row-N IDs nicht im JS gefunden — werden sie korrekt erzeugt?")
        warnings += 1

    if re.search(r"'sb-bank-'\s*\+", content) or re.search(r'"sb-bank-"\s*\+', content):
        ok("sb-bank-N IDs werden dynamisch erzeugt")
    else:
        warn("sb-bank-N IDs nicht im JS gefunden")
        warnings += 1

    # ── 6. LÖSUNGSBUTTON ─────────────────────────────────────────────────────
    print(f"\n{BOLD}[6] Lösungsbutton{RESET}")

    if re.search(r'sbShowSolution', content):
        ok("sbShowSolution() im Lösungsbutton referenziert")
    elif re.search(r'showSatzbauLoesung|showSbLoesung', content):
        fail("Alter Lösungsbutton-Aufruf gefunden — auf sbShowSolution() umstellen!")
        errors += 1

    # ── ERGEBNIS ──────────────────────────────────────────────────────────────
    print(f"\n{'─'*60}")
    if errors == 0 and warnings == 0:
        print(f"{GREEN}{BOLD}✓ ALLES OK — Migration vollständig und korrekt!{RESET}")
    elif errors == 0:
        print(f"{YELLOW}{BOLD}⚠ {warnings} Warnung(en) — Migration wahrscheinlich OK, aber bitte prüfen{RESET}")
    else:
        print(f"{RED}{BOLD}✗ {errors} Fehler, {warnings} Warnung(en) — Migration unvollständig!{RESET}")
    print(f"{'─'*60}")

    return 1 if errors > 0 else 0


def main():
    if len(sys.argv) < 2:
        print(f"Verwendung: python3 check-satzbau-migration.py DATEI.html [DATEI2.html ...]")
        sys.exit(1)

    dateien = sys.argv[1:]
    gesamt_fehler = 0

    for datei in dateien:
        gesamt_fehler += check_file(datei)

    if len(dateien) > 1:
        print(f"\n{BOLD}{'═'*60}{RESET}")
        if gesamt_fehler == 0:
            print(f"{GREEN}{BOLD}✓ Alle {len(dateien)} Dateien bestanden die Prüfung!{RESET}")
        else:
            print(f"{RED}{BOLD}✗ {gesamt_fehler} von {len(dateien)} Dateien haben Fehler!{RESET}")
        print(f"{'═'*60}\n")

    sys.exit(1 if gesamt_fehler > 0 else 0)


if __name__ == "__main__":
    main()

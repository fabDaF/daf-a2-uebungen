#!/usr/bin/env python3
"""
check-entdecken-tab.py — Prüft G-Dateien auf Skill-konformen Entdecken-Tab.

Basiert auf: daf-grammatik-uebungen/SKILL.md + references/css-patterns.md + references/js-patterns.md

Prüfkategorien:
  [1] HTML-Struktur: entdeck-intro, progress-dots (4×), mc-step (4×), mcfb (4×), regelkarte
  [2] CSS-Klassen (Pflicht): .entdeck-intro, .hl, .mc-step, .mc-step.active, .mc-btn,
      .mc-btn.correct, .mc-btn.wrong, .mc-feedback, .mc-feedback.ok, .mc-feedback.err,
      .progress-dots, .pdot, .pdot.done, .regel-karte (display:none)
  [3] JS-Funktionen (Pflicht): mcCheck(), mcDone[], pdot, regelkarte
  [4] Inhalt: hl-Spans (mind. 4), keine Timer/Score/Neustart im Tab 0
  [5] Verbotene alte Muster: .discovery-card, .disc-card, .disc-grid, MC_STEPS, discoveryContainer
"""

import sys, re, os

BOLD = '\033[1m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
SEP = BOLD + '─' * 60 + RESET

def check_file(filepath):
    fname = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    errors = []
    warnings = []
    ok_items = []

    def ok(msg):
        ok_items.append(f"  {GREEN}✓{RESET} {msg}")
    def warn(msg):
        warnings.append(f"  {YELLOW}⚠{RESET} {msg}")
    def err(msg):
        errors.append(f"  {RED}✗{RESET} {msg}")

    print(SEP)
    print(f"{BOLD}Prüfe: {fname}{RESET}")
    print(SEP)

    # ═══════════════════════════════════════════════════════════
    # [1] HTML-STRUKTUR
    # ═══════════════════════════════════════════════════════════
    print(f"\n{BOLD}[1] HTML-Struktur{RESET}")

    # entdeck-intro
    if re.search(r'class="entdeck-intro"', content):
        ok('entdeck-intro Box vorhanden')
    else:
        err('entdeck-intro Box FEHLT — Intro-Box mit Beispielsätzen fehlt')

    # hl-Spans im Entdecken-Tab
    hl_count = len(re.findall(r'class="hl"', content))
    if hl_count >= 4:
        ok(f'hl-Spans: {hl_count} (mind. 4 benötigt)')
    elif hl_count > 0:
        warn(f'Nur {hl_count} hl-Spans — Skill verlangt 4–6 hervorgehobene Zielstrukturen')
    else:
        err('KEINE hl-Spans — Zielstruktur muss mit <span class="hl"> hervorgehoben sein')

    # Progress-Dots (genau 4)
    pdot_ids = re.findall(r'id="pdot(\d+)"', content)
    if len(pdot_ids) == 4 and pdot_ids == ['0','1','2','3']:
        ok('4 Progress-Dots (pdot0–pdot3)')
    elif len(pdot_ids) > 0:
        warn(f'{len(pdot_ids)} Progress-Dots gefunden (erwartet: 4 mit id pdot0–pdot3)')
    else:
        err('KEINE Progress-Dots — 4 pdot-Divs fehlen')

    # MC-Steps (genau 4)
    mc_step_ids = re.findall(r'id="mc-step(\d+)"', content)
    if len(mc_step_ids) == 4 and mc_step_ids == ['0','1','2','3']:
        ok('4 MC-Steps (mc-step0–mc-step3)')
    elif len(mc_step_ids) > 0:
        warn(f'{len(mc_step_ids)} MC-Steps gefunden (erwartet: 4 mit id mc-step0–mc-step3)')
    else:
        err('KEINE MC-Steps — 4 Multiple-Choice-Schritte fehlen komplett')

    # MC-Feedback (genau 4)
    mcfb_ids = re.findall(r'id="mcfb(\d+)"', content)
    if len(mcfb_ids) == 4 and mcfb_ids == ['0','1','2','3']:
        ok('4 MC-Feedback-Divs (mcfb0–mcfb3)')
    elif len(mcfb_ids) > 0:
        warn(f'{len(mcfb_ids)} mcfb-Divs gefunden (erwartet: 4)')
    else:
        err('KEINE mcfb-Divs — Feedback-Container für MC-Steps fehlen')

    # Regelkarte
    if re.search(r'id="regelkarte"', content):
        ok('Regelkarte (id="regelkarte") vorhanden')
    else:
        err('Regelkarte FEHLT — id="regelkarte" nicht gefunden')

    # mc-step0 muss class="active" haben (erster Schritt sichtbar)
    if re.search(r'id="mc-step0"[^>]*class="[^"]*active', content) or \
       re.search(r'class="mc-step active"[^>]*id="mc-step0"', content) or \
       re.search(r'class="mc-step\s+active"', content):
        ok('mc-step0 hat class="active" (erster Schritt sichtbar)')
    elif len(mc_step_ids) >= 1:
        err('mc-step0 hat KEIN class="active" — erster MC-Schritt ist unsichtbar!')

    # mcCheck onclick in Buttons
    mc_onclick_count = len(re.findall(r'onclick="mcCheck\(\d+,\s*this,\s*(true|false)\)"', content))
    if mc_onclick_count >= 12:  # 4 Schritte × 3 Optionen
        ok(f'{mc_onclick_count} mcCheck()-Aufrufe in Buttons (mind. 12 erwartet)')
    elif mc_onclick_count > 0:
        warn(f'Nur {mc_onclick_count} mcCheck()-Aufrufe — 4 Schritte × 3 Optionen = mind. 12 erwartet')
    else:
        err('KEINE mcCheck()-Aufrufe in onclick — Buttons sind nicht verdrahtet')

    # ═══════════════════════════════════════════════════════════
    # [2] CSS-KLASSEN (Pflicht aus css-patterns.md)
    # ═══════════════════════════════════════════════════════════
    print(f"\n{BOLD}[2] CSS-Klassen (Pflicht){RESET}")

    css_checks = [
        (r'\.entdeck-intro\s*\{', '.entdeck-intro', 'background:#f3e5f5, border-left:5px solid #9c27b0'),
        (r'\.hl\s*\{', '.hl', 'background:#e1bee7, color:#4a148c, font-weight:700'),
        (r'\.mc-step\s*\{', '.mc-step', 'display:none (unsichtbar bis aktiv)'),
        (r'\.mc-step\.active\s*\{', '.mc-step.active', 'display:block'),
        (r'\.mc-btn\s*\{', '.mc-btn', 'border:2px solid #c5cae9, border-radius:8px'),
        (r'\.mc-btn\.correct\s*\{', '.mc-btn.correct', 'border-color:#43a047, background:#e8f5e9'),
        (r'\.mc-btn\.wrong\s*\{', '.mc-btn.wrong', 'border-color:#e53935, background:#ffebee'),
        (r'\.mc-feedback\s*\{', '.mc-feedback', 'min-height:1.3em'),
        (r'\.mc-feedback\.ok\s*\{', '.mc-feedback.ok', 'color:#2e7d32'),
        (r'\.mc-feedback\.err\s*\{', '.mc-feedback.err', 'color:#c62828'),
        (r'\.progress-dots\s*\{', '.progress-dots', 'display:flex, gap:8px'),
        (r'\.pdot\s*\{', '.pdot', 'width:14px, height:14px, background:#c5cae9'),
        (r'\.pdot\.done\s*\{', '.pdot.done', 'background:#667eea'),
        (r'\.regel-karte\s*\{', '.regel-karte', 'display:none (unsichtbar bis alle MC fertig)'),
    ]

    for pattern, name, detail in css_checks:
        if re.search(pattern, content):
            ok(f'{name}')
        else:
            err(f'{name} CSS FEHLT — erwartet: {detail}')

    # Spezial-Check: .regel-karte muss display:none haben
    rk_match = re.search(r'\.regel-karte\s*\{([^}]+)\}', content)
    if rk_match:
        rk_css = rk_match.group(1)
        if 'display' in rk_css and 'none' in rk_css:
            ok('.regel-karte hat display:none (korrekt versteckt)')
        else:
            err('.regel-karte hat KEIN display:none — Regel wird sofort angezeigt statt nach MC!')

    # Spezial-Check: .mc-step muss display:none haben
    ms_match = re.search(r'\.mc-step\s*\{([^}]+)\}', content)
    if ms_match:
        ms_css = ms_match.group(1)
        if 'display' in ms_css and 'none' in ms_css:
            ok('.mc-step hat display:none (korrekt versteckt)')
        else:
            err('.mc-step hat KEIN display:none — alle Schritte sind sofort sichtbar!')

    # ═══════════════════════════════════════════════════════════
    # [3] JS-FUNKTIONEN (Pflicht aus js-patterns.md)
    # ═══════════════════════════════════════════════════════════
    print(f"\n{BOLD}[3] JavaScript (Pflicht){RESET}")

    # mcCheck Funktion
    if re.search(r'function\s+mcCheck\s*\(\s*step\s*,\s*btn\s*,\s*correct\s*\)', content):
        ok('function mcCheck(step, btn, correct) vorhanden')
    elif re.search(r'function\s+mcCheck', content):
        warn('mcCheck gefunden, aber Signatur weicht ab (erwartet: step, btn, correct)')
    else:
        err('function mcCheck() FEHLT komplett')

    # mcDone Array
    if re.search(r'var\s+mcDone\s*=\s*\[', content):
        ok('var mcDone = [...] vorhanden')
    else:
        err('var mcDone Array FEHLT')

    # pdot-Referenz in JS
    if re.search(r"getElementById\(['\"]pdot", content):
        ok('pdot-Referenz in JS (Progress-Dot wird aktualisiert)')
    else:
        err('Keine pdot-Referenz in JS — Progress-Dots werden nie aktualisiert')

    # regelkarte-Referenz in JS
    if re.search(r"getElementById\(['\"]regelkarte['\"]", content):
        ok('regelkarte-Referenz in JS (wird nach letztem MC eingeblendet)')
    else:
        err('Keine regelkarte-Referenz in JS — Regelkarte wird nie eingeblendet')

    # setTimeout für nächsten Schritt (700ms) — inline oder mehrzeilig mit }, 700);
    if re.search(r'setTimeout.*700', content) or re.search(r'},\s*700\)', content):
        ok('setTimeout 700ms für nächsten Schritt')
    else:
        warn('Kein setTimeout mit 700ms gefunden — Übergang zum nächsten Schritt fehlt?')

    # setTimeout für Fehler-Reset (1400ms) — inline oder mehrzeilig mit }, 1400);
    if re.search(r'setTimeout.*1400', content) or re.search(r'},\s*1400\)', content):
        ok('setTimeout 1400ms für Fehler-Reset')
    else:
        warn('Kein setTimeout mit 1400ms gefunden — Fehler-Reset fehlt?')

    # btn.disabled in mcCheck
    if re.search(r'b\.disabled\s*=\s*true', content) or re.search(r'disabled\s*=\s*true', content):
        ok('Buttons werden nach Klick disabled')
    else:
        warn('Kein b.disabled = true — Buttons bleiben nach Klick aktiv?')

    # ═══════════════════════════════════════════════════════════
    # [4] INHALT & PÄDAGOGIK
    # ═══════════════════════════════════════════════════════════
    print(f"\n{BOLD}[4] Inhalt & Pädagogik{RESET}")

    # Tab 0 darf keinen Timer haben
    # Suche den HTML-Bereich von <div id="sec-0"> oder <section id="tab-0"> bis sec-1/tab-1
    tab0_match = re.search(r'id="(?:sec-0|tab-?0)".*?(?=id="(?:sec-1|tab-?1)")', content, re.DOTALL)
    if tab0_match:
        tab0_content = tab0_match.group(0)
        timer_in_tab0 = re.search(r'timer-bar|timer-display|⏱|Neustart|Bestzeit', tab0_content, re.IGNORECASE)
        if timer_in_tab0:
            err(f'Timer/Neustart/Bestzeit im Entdecken-Tab (Tab 0) gefunden! Skill sagt: KEIN Timer im Entdecken-Tab')
        else:
            ok('Kein Timer im Entdecken-Tab (korrekt)')

        score_in_tab0 = re.search(r'score-box|Punkte|🏆', tab0_content, re.IGNORECASE)
        if score_in_tab0:
            warn('Möglicher Score-Hinweis im Entdecken-Tab — sollte keinen Score haben')
        else:
            ok('Kein Score im Entdecken-Tab (korrekt)')
    else:
        warn('Tab-0-Bereich konnte nicht isoliert werden — manuelle Prüfung nötig')

    # Jede Frage sollte genau 3 Optionen haben (nicht 2, nicht 4)
    for step_num in range(4):
        step_pattern = rf'id="mc-step{step_num}".*?(?=id="mc-step{step_num+1}"|id="regelkarte")'
        step_match = re.search(step_pattern, content, re.DOTALL)
        if step_match:
            btn_count = len(re.findall(r'class="mc-btn"', step_match.group(0)))
            correct_count = len(re.findall(r'mcCheck\(\d+,\s*this,\s*true\)', step_match.group(0)))
            if btn_count == 3:
                ok(f'Frage {step_num+1}: 3 Optionen')
            elif btn_count > 0:
                warn(f'Frage {step_num+1}: {btn_count} Optionen (erwartet: 3)')
            if correct_count == 1:
                ok(f'Frage {step_num+1}: genau 1 richtige Antwort')
            elif correct_count == 0:
                err(f'Frage {step_num+1}: KEINE richtige Antwort (true) definiert!')
            else:
                warn(f'Frage {step_num+1}: {correct_count} richtige Antworten (erwartet: 1)')

    # ═══════════════════════════════════════════════════════════
    # [5] VERBOTENE ALTE MUSTER
    # ═══════════════════════════════════════════════════════════
    print(f"\n{BOLD}[5] Verbotene alte Muster{RESET}")

    old_patterns = [
        (r'class="discovery-card"', 'class="discovery-card"', 'Alt: discovery-card → entdeck-intro'),
        (r'class="disc-card"', 'class="disc-card"', 'Alt: disc-card → entdeck-intro'),
        (r'class="disc-grid"', 'class="disc-grid"', 'Alt: disc-grid → nicht im Skill'),
        (r'class="discover-grid"', 'class="discover-grid"', 'Alt: discover-grid → nicht im Skill'),
        (r'id="discoveryContainer"', 'discoveryContainer', 'Alt: JS-generierte MC-Steps → statisches HTML'),
        (r'var\s+MC_STEPS\s*=', 'var MC_STEPS', 'Alt: MC_STEPS-Array → statisches HTML mit mcCheck()'),
        (r'\.mc-choice\b', '.mc-choice', 'Alt: mc-choice → mc-btn'),
        (r'\.step-q\b', '.step-q', 'Alt: step-q → mc-step h4'),
        (r'\.mc-fb\b(?!\.)', '.mc-fb', 'Alt: mc-fb → mc-feedback'),
        (r'class="refl"', 'class="refl"', 'Alt: refl → hl'),
        (r'\.hl-werden\b', '.hl-werden', 'Alt: hl-werden → hl'),
        (r'\.hl-inf\b', '.hl-inf', 'Alt: hl-inf → hl'),
        (r'\.hl-dat\b', '.hl-dat', 'Alt: hl-dat → hl (toleriert wenn zusätzlich .hl vorhanden)'),
        (r'\.hl-akk\b', '.hl-akk', 'Alt: hl-akk → hl (toleriert wenn zusätzlich .hl vorhanden)'),
    ]

    found_old = False
    for pattern, name, hint in old_patterns:
        if re.search(pattern, content):
            # Spezialfall: hl-dat/hl-akk toleriert bei Wechselpräpositionen (1027G)
            if name in ('.hl-dat', '.hl-akk', '.hl-werden', '.hl-inf') and hl_count >= 4:
                pass  # toleriert wenn genug .hl vorhanden
            # mc-choice/mc-fb/refl sind OK wenn sie NUR außerhalb des Entdecken-Tabs vorkommen
            elif name in ('.mc-choice', '.mc-fb', 'class="refl"') and tab0_match and not re.search(pattern, tab0_match.group(0)):
                pass  # nur in anderen Tabs, nicht im Entdecken-Tab
            else:
                warn(f'Altes Muster: {name} — {hint}')
                found_old = True

    if not found_old:
        ok('Keine verbotenen alten Muster gefunden')

    # ═══════════════════════════════════════════════════════════
    # ZUSAMMENFASSUNG
    # ═══════════════════════════════════════════════════════════
    print()
    for item in ok_items:
        print(item)
    for item in warnings:
        print(item)
    for item in errors:
        print(item)
    print()

    if errors:
        print(f"{RED}{BOLD}✗ {len(errors)} FEHLER — Entdecken-Tab ist NICHT skill-konform!{RESET}")
    elif warnings:
        print(f"{YELLOW}{BOLD}⚠ {len(warnings)} Warnung(en) — bitte manuell prüfen{RESET}")
    else:
        print(f"{GREEN}{BOLD}✓ ALLES OK — Entdecken-Tab ist 100% skill-konform!{RESET}")

    print(SEP)
    return len(errors), len(warnings)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Verwendung: {sys.argv[0]} <datei1.html> [datei2.html ...]")
        sys.exit(1)

    total_errors = 0
    total_warnings = 0
    results = []

    for filepath in sys.argv[1:]:
        if not os.path.isfile(filepath):
            print(f"{RED}Datei nicht gefunden: {filepath}{RESET}")
            continue
        e, w = check_file(filepath)
        total_errors += e
        total_warnings += w
        results.append((os.path.basename(filepath), e, w))

    if len(results) > 1:
        print(f"\n{BOLD}═══ GESAMTÜBERSICHT ═══{RESET}")
        for name, e, w in results:
            status = f"{GREEN}✓ OK{RESET}" if e == 0 and w == 0 else \
                     f"{YELLOW}⚠ {w} Warn.{RESET}" if e == 0 else \
                     f"{RED}✗ {e} Fehler{RESET}"
            print(f"  {status}  {name}")

        print(f"\n  Gesamt: {total_errors} Fehler, {total_warnings} Warnungen in {len(results)} Dateien")
        if total_errors == 0:
            print(f"  {GREEN}{BOLD}✓ Alle {len(results)} Dateien bestanden die Prüfung!{RESET}")

    sys.exit(1 if total_errors > 0 else 0)

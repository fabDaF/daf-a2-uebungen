#!/usr/bin/env python3
"""
check-all-skills.py — Prüft ALLE DaF-HTML-Dateien auf Skill-Konformität.

Prüfkategorien:
  [L] LAYOUT (daf-html-layout) — für alle Dateien
      - body: linear-gradient(135deg, #667eea, #764ba2), min-height:100vh, padding:20px
      - .container: max-width:1000px, border-radius:12px, overflow:hidden, box-shadow
      - .header: gradient, h1 Georgia serif, big-emoji
      - .nav: border-top/left/right, flex-wrap:nowrap
      - .nav-btn: border-right + border-bottom, display:flex, flex-direction:column
      - .nav-btn:last-child: border-right:none
      - .nav-btn.active: background:white, border-bottom:3px solid #667eea
      - .nav-emoji + .nav-label CSS
      - @media (max-width:600px) responsive
      - .section / .section.active
      - author-footer innerhalb container

  [E] ENTDECKEN-TAB (daf-grammatik-uebungen) — nur G-Dateien
      - entdeck-intro, hl-spans, pdots, mc-steps, mcfb, regelkarte
      - mcCheck JS, mcDone, setTimeout 700/1400

  [S] SATZBAU (satzbau-drag-drop) — alle Dateien mit Satzbau-Tab
      - chips-container, sentence-builder, chip CSS
      - sbDragged, getSbCursor, sbMakeChip, sbRegisterZone, initSatzbau JS
      - dataset.orig usage

  [G] GENERAL — alle Dateien
      - author-footer mit korrekter E-Mail
      - keine externen Abhängigkeiten (CDN)
      - showSection/showTab Funktion vorhanden
"""

import sys, re, os, glob

BOLD = '\033[1m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
RESET = '\033[0m'
SEP = BOLD + '─' * 70 + RESET

def detect_file_type(fname):
    """Erkennt den Dateityp aus dem Dateinamen: V, X, G, R, S, W"""
    m = re.search(r'\d{4}([A-Z])', fname)
    return m.group(1) if m else '?'

def has_satzbau_tab(content):
    """Prüft ob die Datei einen echten Satzbau-Tab mit Drag-Drop hat (nicht nur das Wort 'Satzbau')"""
    # Muss sowohl chips-container/sentence-builder CSS ALS AUCH satzbauData/sbDragged JS haben
    has_css = bool(re.search(r'\.chips-container\s*\{|\.sentence-builder\s*\{', content))
    has_js = bool(re.search(r'satzbauData|sbDragged|initSatzbau|SB_DATA', content))
    return has_css and has_js

def has_entdecken_tab(content):
    """Prüft ob die Datei einen Entdecken-Tab hat oder haben sollte"""
    return bool(re.search(r'entdeck|Entdecken|mc-step', content))

def has_wortschatz_tab(content):
    """Prüft ob die Datei einen Wortschatz-Tab hat"""
    return bool(re.search(r'WORTSCHATZ\s*=\s*\[|wortschatzContainer|vocabContainer|initWortschatz|initVocab', content))

def check_layout(content, fname):
    """[L] Layout-Prüfung nach daf-html-layout Skill"""
    errors = []
    warnings = []
    ok_items = []

    def ok(msg): ok_items.append(msg)
    def warn(msg): warnings.append(msg)
    def err(msg): errors.append(msg)

    # === BODY ===
    if re.search(r'background:\s*linear-gradient\(135deg,\s*#667eea\s*(0%\s*,)?\s*#764ba2', content):
        ok('Body gradient korrekt')
    else:
        err('[L] Body gradient FEHLT oder falsch (soll: linear-gradient(135deg, #667eea, #764ba2))')

    if re.search(r'min-height:\s*100vh', content):
        ok('min-height:100vh')
    else:
        warn('[L] Body min-height:100vh fehlt')

    # === CONTAINER ===
    if re.search(r'max-width:\s*1000px', content):
        ok('Container max-width:1000px')
    else:
        err('[L] Container max-width:1000px FEHLT')

    if re.search(r'border-radius:\s*12px', content):
        ok('Container border-radius:12px')
    else:
        warn('[L] Container border-radius:12px fehlt (oft 16px)')

    if re.search(r'overflow:\s*hidden', content):
        ok('Container overflow:hidden')
    else:
        warn('[L] Container overflow:hidden fehlt')

    if re.search(r'box-shadow:\s*0\s+10px\s+40px', content):
        ok('Container box-shadow korrekt')
    else:
        warn('[L] Container box-shadow weicht ab')

    # === HEADER ===
    if re.search(r'class="header"', content):
        ok('Header div vorhanden')
    else:
        err('[L] Header div (class="header") FEHLT')

    if re.search(r'Georgia.*serif', content):
        ok('Header Georgia serif Schrift')
    else:
        warn('[L] Header h1 Georgia serif Schrift fehlt')

    if re.search(r'class="big-emoji"', content):
        ok('big-emoji vorhanden')
    else:
        warn('[L] big-emoji div fehlt')

    # === NAV ===
    if re.search(r'class="nav"', content):
        ok('Nav-Leiste vorhanden')
    else:
        err('[L] Nav-Leiste (class="nav") FEHLT')

    # Nav border-Prüfung
    nav_css = re.search(r'\.nav\s*\{([^}]+)\}', content)
    if nav_css:
        nav_body = nav_css.group(1)
        if 'border-top' in nav_body:
            ok('Nav border-top')
        else:
            err('[L] Nav border-top FEHLT')
        if 'border-left' in nav_body:
            ok('Nav border-left')
        else:
            err('[L] Nav border-left FEHLT')
        if 'border-right' in nav_body:
            ok('Nav border-right')
        else:
            err('[L] Nav border-right FEHLT')
        if 'flex-wrap' in nav_body and 'nowrap' in nav_body:
            ok('Nav flex-wrap:nowrap')
        else:
            warn('[L] Nav flex-wrap:nowrap fehlt (Desktop)')

    # Nav-btn Borders
    navbtn_css = re.search(r'\.nav-btn\s*\{([^}]+)\}', content)
    if navbtn_css:
        btn_body = navbtn_css.group(1)
        if 'border-right' in btn_body and 'border-bottom' in btn_body:
            ok('Nav-btn border-right + border-bottom')
        else:
            err('[L] Nav-btn border-right/border-bottom FEHLT')
        if 'flex-direction' in btn_body and 'column' in btn_body:
            ok('Nav-btn flex-direction:column (Emoji über Text)')
        else:
            warn('[L] Nav-btn flex-direction:column fehlt (Emoji neben Text)')

    # Nav-btn:last-child
    if re.search(r'\.nav-btn:last-child\s*\{[^}]*border-right:\s*none', content):
        ok('Nav-btn:last-child border-right:none')
    else:
        warn('[L] Nav-btn:last-child border-right:none fehlt')

    # Nav-btn.active
    active_css = re.search(r'\.nav-btn\.active\s*\{([^}]+)\}', content)
    if active_css:
        ab = active_css.group(1)
        if 'background' in ab and 'white' in ab:
            ok('Nav-btn.active background:white')
        else:
            warn('[L] Nav-btn.active background:white fehlt')
        if 'border-bottom' in ab and '#667eea' in ab:
            ok('Nav-btn.active border-bottom accent')
        else:
            warn('[L] Nav-btn.active border-bottom:#667eea fehlt')

    # nav-emoji + nav-label CSS
    if re.search(r'\.nav-emoji\s*\{', content):
        ok('.nav-emoji CSS')
    else:
        warn('[L] .nav-emoji CSS fehlt')
    if re.search(r'\.nav-label\s*\{', content):
        ok('.nav-label CSS')
    else:
        warn('[L] .nav-label CSS fehlt')

    # Nav-Buttons HTML: span nav-emoji + span nav-label
    nav_btns = re.findall(r'class="nav-btn[^"]*"[^>]*>.*?</div>', content, re.DOTALL)
    if nav_btns:
        has_spans = any('nav-emoji' in b and 'nav-label' in b for b in nav_btns)
        if has_spans:
            ok('Nav-Buttons mit nav-emoji + nav-label spans')
        else:
            warn('[L] Nav-Buttons ohne nav-emoji/nav-label spans (Emoji neben Text)')

    # === RESPONSIVE ===
    if re.search(r'@media\s*\(\s*max-width:\s*600px\s*\)', content):
        ok('@media (max-width:600px) vorhanden')
    else:
        err('[L] @media (max-width:600px) FEHLT — keine mobile Anpassung')

    # === SECTION ===
    if re.search(r'\.section\s*\{[^}]*display:\s*none', content):
        ok('.section display:none')
    else:
        warn('[L] .section { display:none } fehlt')

    # === FOOTER ===
    if re.search(r'class="author-footer"', content):
        ok('author-footer vorhanden')
    else:
        err('[L] author-footer FEHLT')

    if re.search(r'Frank\s*Burkert', content):
        ok('Frank Burkert im Footer')
    else:
        warn('[L] Frank Burkert nicht im Footer')

    if re.search(r'fabdaf\.onmicrosoft\.com', content, re.IGNORECASE):
        ok('Korrekte E-Mail (fabdaf.onmicrosoft.com)')
    else:
        warn('[L] E-Mail fabdaf.onmicrosoft.com fehlt im Footer')

    # Footer innerhalb container? (vor </div><!-- /container -->)
    # Einfache Heuristik: author-footer kommt vor dem letzten </div> vor <script>
    footer_pos = content.find('author-footer')
    script_pos = content.find('<script')
    container_close = content.rfind('</div>', 0, script_pos) if script_pos > 0 else -1
    if footer_pos > 0 and container_close > 0 and footer_pos < container_close:
        ok('Footer innerhalb Container (vor </div><!-- /container -->)')
    elif footer_pos > 0:
        warn('[L] Footer möglicherweise außerhalb des Containers')

    return errors, warnings, ok_items


def check_entdecken(content, fname):
    """[E] Entdecken-Tab Prüfung (nur für G-Dateien)"""
    errors = []
    warnings = []
    ok_items = []

    def ok(msg): ok_items.append(msg)
    def warn(msg): warnings.append(msg)
    def err(msg): errors.append(msg)

    # Prüfe ob alternativer Entdeckungs-Tab vorliegt (discovery-grid, info-card etc.)
    has_alt_entdeck = bool(re.search(r'class="discovery-grid"|class="disc-card"|class="info-card"', content))

    # entdeck-intro (oder alternatives Layout akzeptieren)
    if re.search(r'class="entdeck-intro"', content):
        ok('entdeck-intro vorhanden')
    elif has_alt_entdeck:
        ok('Entdeckungs-Tab (alternatives Layout: discovery-grid)')
    else:
        err('[E] entdeck-intro FEHLT')

    # hl-spans (class="hl" oder class="hl-*" akzeptieren)
    hl_count = len(re.findall(r'class="hl[\s"]', content))
    hl_count += len(re.findall(r'class="hl-\w+', content))
    if hl_count >= 4:
        ok(f'hl-spans: {hl_count}')
    elif hl_count > 0:
        warn(f'[E] Nur {hl_count} hl-spans (mind. 4)')
    elif not has_alt_entdeck:
        err('[E] KEINE hl-spans')
    else:
        ok('hl-spans: alternatives Layout')

    # pdots (nur prüfen wenn Standard-Layout)
    pdot_ids = re.findall(r'id="pdot(\d+)"', content)
    if len(pdot_ids) == 4:
        ok('4 pdots')
    elif has_alt_entdeck:
        ok('pdots: alternatives Entdeckungs-Layout')
    else:
        err(f'[E] {len(pdot_ids)} pdots (erwartet: 4)')

    # mc-steps (nur prüfen wenn Standard-Layout)
    mc_ids = re.findall(r'id="mc-step(\d+)"', content)
    if len(mc_ids) == 4:
        ok('4 mc-steps')
    elif has_alt_entdeck:
        ok('mc-steps: alternatives Entdeckungs-Layout')
    else:
        err(f'[E] {len(mc_ids)} mc-steps (erwartet: 4)')

    # mcfb (nur prüfen wenn Standard-Layout)
    mcfb_ids = re.findall(r'id="mcfb(\d+)"', content)
    if len(mcfb_ids) == 4:
        ok('4 mcfb-divs')
    elif has_alt_entdeck:
        ok('mcfb: alternatives Entdeckungs-Layout')
    else:
        err(f'[E] {len(mcfb_ids)} mcfb-divs (erwartet: 4)')

    # regelkarte (oder alternatives Erklärungs-Element)
    if re.search(r'id="regelkarte"', content):
        ok('regelkarte vorhanden')
    elif has_alt_entdeck and re.search(r'info-card|regel-box|regel-karte|Regelkarte', content):
        ok('regelkarte: alternatives Layout (info-card)')
    elif has_alt_entdeck:
        ok('regelkarte: alternatives Entdeckungs-Layout')
    else:
        err('[E] regelkarte FEHLT')

    # mc-step0 active (nur Standard-Layout)
    if re.search(r'class="mc-step\s+active"', content):
        ok('mc-step0 active')
    elif not has_alt_entdeck:
        if len(mc_ids) >= 1:
            err('[E] mc-step0 hat kein class="active"')

    # mcCheck onclick count (nur Standard-Layout)
    mc_onclick = len(re.findall(r'onclick="mcCheck\(', content))
    if mc_onclick >= 12:
        ok(f'{mc_onclick} mcCheck-Aufrufe')
    elif mc_onclick > 0:
        warn(f'[E] Nur {mc_onclick} mcCheck-Aufrufe (mind. 12)')
    elif has_alt_entdeck:
        ok('mcCheck: alternatives Entdeckungs-Layout')
    else:
        err('[E] KEINE mcCheck-Aufrufe')

    # CSS (Standard-Layout-Klassen nur prüfen wenn Standard-Layout)
    if has_alt_entdeck:
        # Alternatives Layout: nur prüfen ob irgendwelche Entdeckungs-CSS vorhanden
        if re.search(r'\.disc-card\s*\{|\.info-card\s*\{|\.discovery-grid\s*\{', content):
            ok('Entdeckungs-CSS (alternatives Layout) vorhanden')
        else:
            warn('[E] Entdeckungs-CSS fehlt (discovery-grid/disc-card/info-card)')
    else:
        css_needed = ['.entdeck-intro', '.hl', '.mc-step', '.mc-step.active',
                      '.mc-btn', '.mc-btn.correct', '.mc-btn.wrong',
                      '.mc-feedback', '.progress-dots', '.pdot', '.pdot.done', '.regel-karte']
        for cls in css_needed:
            esc = re.escape(cls)
            if re.search(esc + r'\s*\{', content):
                ok(f'{cls} CSS')
            else:
                err(f'[E] {cls} CSS FEHLT')

    # JS mcCheck function (nur beim Standard-Layout prüfen)
    if has_alt_entdeck:
        ok('mcCheck: alternatives Entdeckungs-Layout')
    elif re.search(r'function\s+mcCheck\s*\(\s*step\s*,\s*btn\s*,\s*correct\s*\)', content):
        ok('mcCheck(step,btn,correct)')
    elif re.search(r'function\s+mcCheck', content):
        warn('[E] mcCheck Signatur weicht ab')
    else:
        err('[E] mcCheck() FEHLT')

    # mcDone (nur beim Standard-Layout prüfen)
    if has_alt_entdeck:
        ok('mcDone: alternatives Entdeckungs-Layout')
    elif re.search(r'var\s+mcDone\s*=\s*\[', content):
        ok('mcDone Array')
    else:
        err('[E] mcDone Array FEHLT')

    # Forbidden old patterns in Entdecken-Tab (disc-card ist jetzt alternatives Layout, kein Fehler)
    tab0_match = re.search(r'id="(?:sec-0|tab-?0)".*?(?=id="(?:sec-1|tab-?1)")', content, re.DOTALL)
    old_in_tab0 = []
    if tab0_match:
        t0 = tab0_match.group(0)
        for pat, name in [(r'var\s+MC_STEPS', 'MC_STEPS'), (r'id="discoveryContainer"', 'discoveryContainer'),
                          (r'class="discovery-card"', 'discovery-card')]:
            if re.search(pat, t0):
                old_in_tab0.append(name)
    if old_in_tab0:
        err(f'[E] Altes Muster in Tab 0: {", ".join(old_in_tab0)}')

    return errors, warnings, ok_items


def check_satzbau(content, fname):
    """[S] Satzbau-Prüfung nach satzbau-drag-drop Skill"""
    errors = []
    warnings = []
    ok_items = []

    def ok(msg): ok_items.append(msg)
    def warn(msg): warnings.append(msg)
    def err(msg): errors.append(msg)

    # CSS
    if re.search(r'\.chips-container\s*\{', content):
        ok('.chips-container CSS')
    else:
        err('[S] .chips-container CSS FEHLT')

    if re.search(r'\.sentence-builder\s*\{', content):
        ok('.sentence-builder CSS')
    else:
        err('[S] .sentence-builder CSS FEHLT')

    if re.search(r'\.chip\s*\{', content):
        ok('.chip CSS')
    else:
        err('[S] .chip CSS FEHLT')

    if re.search(r'\.chip\.correct', content):
        ok('.chip.correct CSS')
    else:
        err('[S] .chip.correct CSS FEHLT')

    if re.search(r'\.chip\.incorrect', content):
        ok('.chip.incorrect CSS')
    else:
        err('[S] .chip.incorrect CSS FEHLT')

    if re.search(r'\.sb-punkt\s*\{', content):
        ok('.sb-punkt CSS')
    else:
        err('[S] .sb-punkt CSS FEHLT')

    if re.search(r'\.satzbau-feedback\s*\{', content):
        ok('.satzbau-feedback CSS')
    else:
        err('[S] .satzbau-feedback CSS FEHLT')

    # JS Functions
    if re.search(r'var\s+sbDragged', content):
        ok('sbDragged variable')
    else:
        err('[S] sbDragged Variable FEHLT')

    if re.search(r'function\s+getSbCursor', content):
        ok('getSbCursor()')
    else:
        err('[S] getSbCursor() FEHLT')

    if re.search(r'function\s+sbMakeChip', content):
        ok('sbMakeChip()')
    else:
        err('[S] sbMakeChip() FEHLT')

    if re.search(r'function\s+sbRegisterZone', content):
        ok('sbRegisterZone()')
    else:
        err('[S] sbRegisterZone() FEHLT')

    if re.search(r'function\s+initSatzbau', content):
        ok('initSatzbau()')
    else:
        err('[S] initSatzbau() FEHLT')

    if re.search(r'dataset\.orig', content):
        ok('dataset.orig verwendet')
    else:
        err('[S] dataset.orig nicht verwendet (Vergleich basiert auf textContent?)')

    # satzbauData array
    if re.search(r'var\s+satzbauData\s*=|satzbauData\s*=\s*\[', content):
        ok('satzbauData Array')
    else:
        err('[S] satzbauData Array FEHLT')

    # HTML IDs (statisch oder dynamisch generiert — beides OK)
    if re.search(r'id="sb-bank-0"|sb-bank-.*idx|sb-bank-.*\+', content):
        ok('sb-bank-N IDs (statisch oder dynamisch)')
    else:
        warn('[S] sb-bank-0 nicht gefunden (weder statisch noch dynamisch)')

    if re.search(r'id="sb-row-0"|sb-row-.*idx|sb-row-.*\+', content):
        ok('sb-row-N IDs (statisch oder dynamisch)')
    else:
        warn('[S] sb-row-0 nicht gefunden (weder statisch noch dynamisch)')

    # [S15] .btn CSS: darf NICHT ausgefüllt lila/grau sein (background:#667eea oder background:#9e9e9e)
    btn_css = re.search(r'\.btn\s*\{([^}]+)\}', content)
    if btn_css:
        btn_body = btn_css.group(1)
        if re.search(r'background\s*:\s*#667eea|background\s*:\s*#5a6fd6', btn_body):
            err('[S15] .btn hat gefüllten lila Hintergrund (background:#667eea) — muss dezent sein (background:none, border:1px solid #ddd)')
        elif re.search(r'background\s*:\s*#9e9e9e|background\s*:\s*#757575', btn_body):
            err('[S15] .btn.secondary mit grauem Hintergrund — .btn muss dezent sein (background:none)')
        else:
            ok('.btn dezent (kein gefüllter lila/grauer Hintergrund)')
    # [S16] .btn-row button: muss border vorhanden haben
    btnrow_btn_css = re.search(r'\.btn-row\s+button\s*\{([^}]+)\}', content)
    if btnrow_btn_css:
        if 'border' in btnrow_btn_css.group(1):
            ok('.btn-row button mit border CSS')
        else:
            warn('[S16] .btn-row button CSS ohne border — Skill-Standard prüfen')
    else:
        warn('[S16] .btn-row button CSS nicht gefunden')

    # [S17] .control-bar ist VERBOTEN — veraltetes Pattern statt .timer-bar
    if re.search(r'class="control-bar"|\.control-bar\s*\{', content):
        err('[S17] .control-bar gefunden — veraltetes Layout\! Korrekt: .timer-bar (weiß, Schatten) + .btn-row (lila Outline) als getrennte Divs')
    else:
        ok('Kein .control-bar (veraltetes Timer-Layout-Pattern)')

    # [S18] .timer-bar CSS muss vorhanden sein wenn Timer-IDs vorhanden sind
    has_timer_ids = bool(re.search(r'id="timer-\d', content))
    if has_timer_ids:
        if re.search(r'\.timer-bar\s*\{', content):
            ok('.timer-bar CSS vorhanden (Skill-Standard Timer-Layout)')
        else:
            err('[S18] Timer-IDs vorhanden, aber .timer-bar CSS FEHLT — Skill-Standard: background:white, box-shadow, border-radius:10px')

    return errors, warnings, ok_items


def check_wortschatz(content, fname):
    """[W] Wortschatz-Tab Prüfungen"""
    errors = []
    warnings = []
    ok_items = []

    def ok(msg): ok_items.append(msg)
    def warn(msg): warnings.append(msg)
    def err(msg): errors.append(msg)

    # wortschatzContainer mit 2-Spalten-Grid im HTML
    has_wc_html = bool(re.search(r'id="wortschatzContainer"', content))
    has_grid = bool(re.search(r'grid-template-columns:\s*1fr\s+1fr', content))
    if has_wc_html:
        ok('[W] wortschatzContainer im HTML vorhanden')
    else:
        err('[W] FEHLT: id="wortschatzContainer" — kein 2-Spalten-Grid-Container')
    if has_grid:
        ok('[W] 2-Spalten-Grid (1fr 1fr) vorhanden')
    else:
        err('[W] FEHLT: grid-template-columns:1fr 1fr — Wortschatz muss 2-spaltig sein')

    # .luecken-item (nicht .vocab-item)
    if 'luecken-item' in content:
        ok('[W] .luecken-item CSS-Klasse vorhanden')
    else:
        err('[W] FEHLT: .luecken-item — Wortschatz-Karten müssen .luecken-item verwenden (nicht .vocab-item)')
    if re.search(r'class\s*=\s*["\']vocab-item["\']|\.vocab-item\s*\{', content):
        err('[W] VERBOTEN: .vocab-item gefunden — stattdessen .luecken-item + wortschatzContainer verwenden')
    else:
        ok('[W] Kein .vocab-item (korrekt)')

    # wortschatzCheck() statt liveCheck() im Wortschatz
    if 'wortschatzCheck' in content:
        ok('[W] wortschatzCheck() vorhanden')
    else:
        err('[W] FEHLT: wortschatzCheck() — muss verwendet werden statt liveCheck() im Wortschatz-Tab')

    # initWortschatz oder initVocab → initWortschatz
    if 'function initWortschatz' in content:
        ok('[W] initWortschatz() Funktion vorhanden')
    else:
        err('[W] FEHLT: function initWortschatz() — Standard-Init für Wortschatz-Tab')

    # checkWortschatzAllOk
    if 'checkWortschatzAllOk' in content:
        ok('[W] checkWortschatzAllOk() vorhanden (Timer-Stop)')
    else:
        warn('[W] checkWortschatzAllOk() fehlt — Timer stoppt nicht wenn alle Felder korrekt')

    # KEIN vocabContainer (alter Name)
    if 'vocabContainer' in content:
        err('[W] VERBOTEN: id="vocabContainer" — muss id="wortschatzContainer" sein')
    else:
        ok('[W] Kein vocabContainer (korrekt)')

    return errors, warnings, ok_items


def check_general(content, fname):
    """[G] Allgemeine Prüfungen"""
    errors = []
    warnings = []
    ok_items = []

    def ok(msg): ok_items.append(msg)
    def warn(msg): warnings.append(msg)
    def err(msg): errors.append(msg)

    # Externe Abhängigkeiten
    if re.search(r'<link[^>]*href="https?://', content) or re.search(r'<script[^>]*src="https?://', content):
        warn('[G] Externe Abhängigkeit (CDN-Link) gefunden')
    else:
        ok('Keine externen Abhängigkeiten')

    # showSection/showTab
    if re.search(r'function\s+(?:show(?:Section|Tab|section)|zeigeSec)', content):
        ok('showSection/showTab Funktion')
    else:
        err('[G] showSection/showTab Funktion FEHLT')

    # DOCTYPE
    if content.strip().startswith('<!DOCTYPE html>') or content.strip().startswith('<!doctype html>'):
        ok('DOCTYPE vorhanden')
    else:
        warn('[G] DOCTYPE fehlt')

    # lang="de"
    if re.search(r'<html[^>]*lang="de"', content):
        ok('lang="de"')
    else:
        warn('[G] html lang="de" fehlt')

    # charset
    if re.search(r'charset="?UTF-8"?', content, re.IGNORECASE):
        ok('charset UTF-8')
    else:
        warn('[G] charset UTF-8 fehlt')

    # viewport
    if re.search(r'name="viewport"', content):
        ok('viewport meta')
    else:
        warn('[G] viewport meta fehlt')

    return errors, warnings, ok_items


def check_file(filepath):
    fname = os.path.basename(filepath)
    ftype = detect_file_type(fname)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    all_errors = []
    all_warnings = []
    all_ok = []

    # [L] Layout — alle Dateien
    e, w, o = check_layout(content, fname)
    all_errors.extend(e)
    all_warnings.extend(w)
    all_ok.extend(o)

    # [E] Entdecken — nur G-Dateien
    if ftype == 'G':
        e, w, o = check_entdecken(content, fname)
        all_errors.extend(e)
        all_warnings.extend(w)
        all_ok.extend(o)

    # [S] Satzbau — alle Dateien mit Satzbau-Tab
    if has_satzbau_tab(content):
        e, w, o = check_satzbau(content, fname)
        all_errors.extend(e)
        all_warnings.extend(w)
        all_ok.extend(o)

    # [W] Wortschatz — alle Dateien mit Wortschatz-Tab
    if has_wortschatz_tab(content):
        e, w, o = check_wortschatz(content, fname)
        all_errors.extend(e)
        all_warnings.extend(w)
        all_ok.extend(o)

    # [G] General — alle Dateien
    e, w, o = check_general(content, fname)
    all_errors.extend(e)
    all_warnings.extend(w)
    all_ok.extend(o)

    return fname, ftype, all_errors, all_warnings, all_ok


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Verwendung: {sys.argv[0]} <datei1.html> [datei2.html ...] oder *.html")
        sys.exit(1)

    files = []
    for arg in sys.argv[1:]:
        if '*' in arg:
            files.extend(glob.glob(arg))
        else:
            files.append(arg)

    files = sorted(set(files))

    total_errors = 0
    total_warnings = 0
    results = []
    error_categories = {}  # error message -> [filenames]

    for filepath in files:
        if not os.path.isfile(filepath):
            print(f"{RED}Datei nicht gefunden: {filepath}{RESET}")
            continue
        fname, ftype, errors, warnings, ok_items = check_file(filepath)
        total_errors += len(errors)
        total_warnings += len(warnings)
        results.append((fname, ftype, len(errors), len(warnings)))

        for e in errors:
            error_categories.setdefault(e, []).append(fname)

    # === GESAMTÜBERSICHT ===
    print(f"\n{BOLD}{'═'*70}{RESET}")
    print(f"{BOLD}  GESAMTÜBERSICHT — {len(results)} Dateien geprüft{RESET}")
    print(f"{BOLD}{'═'*70}{RESET}\n")

    # Gruppiert nach Dateityp
    for ftype in ['V', 'X', 'G', 'R', 'S', 'W', '?']:
        type_results = [(n,t,e,w) for n,t,e,w in results if t == ftype]
        if not type_results:
            continue
        type_name = {'V':'Vokabeln','X':'Gemischt','G':'Grammatik','R':'Lesen','S':'Satzbau','W':'Wortschatz','?':'Unbekannt'}[ftype]
        ok_count = sum(1 for _,_,e,_ in type_results if e == 0)
        print(f"  {CYAN}{BOLD}── {ftype}-Dateien ({type_name}) ── {ok_count}/{len(type_results)} OK{RESET}")
        for name, _, e, w in type_results:
            if e == 0 and w == 0:
                status = f"{GREEN}✓{RESET}"
            elif e == 0:
                status = f"{YELLOW}⚠ {w}W{RESET}"
            else:
                status = f"{RED}✗ {e}E {w}W{RESET}"
            print(f"    {status}  {name}")
        print()

    # === FEHLER-RANKING ===
    if error_categories:
        print(f"{BOLD}{'═'*70}{RESET}")
        print(f"{RED}{BOLD}  TOP-FEHLER (häufigste zuerst){RESET}")
        print(f"{BOLD}{'═'*70}{RESET}\n")
        sorted_errs = sorted(error_categories.items(), key=lambda x: -len(x[1]))
        for i, (msg, fnames) in enumerate(sorted_errs[:20], 1):
            print(f"  {RED}{i:2d}. ({len(fnames):3d}×){RESET} {msg}")
            if len(fnames) <= 5:
                print(f"       → {', '.join(fnames)}")
            else:
                print(f"       → {', '.join(fnames[:3])} ... +{len(fnames)-3} weitere")
        print()

    # === ZUSAMMENFASSUNG ===
    print(f"{BOLD}{'═'*70}{RESET}")
    ok_files = sum(1 for _,_,e,_ in results if e == 0)
    print(f"  Dateien: {len(results)} | {GREEN}✓ {ok_files} OK{RESET} | {RED}✗ {len(results)-ok_files} mit Fehlern{RESET}")
    print(f"  Gesamt:  {RED}{total_errors} Fehler{RESET}, {YELLOW}{total_warnings} Warnungen{RESET}")
    if total_errors == 0:
        print(f"\n  {GREEN}{BOLD}✓ ALLE {len(results)} DATEIEN BESTANDEN!{RESET}")
    print(f"{BOLD}{'═'*70}{RESET}")

    sys.exit(1 if total_errors > 0 else 0)

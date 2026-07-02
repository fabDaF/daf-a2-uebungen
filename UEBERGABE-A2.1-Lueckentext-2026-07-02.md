# Übergabe: A2.1-Lückentext-Kanonisierung — Stand 2026-07-02 (Fortsetzung 3)

## In dieser Fortsetzung (3) fertiggestellt — 3 neue Dateien + 1 Fix

| Datei | Commit | Kernfunde |
|---|---|---|
| `DE_A2_1021V-die-arbeitswelt.html` (Fix) | `f705e13` | Frank meldete hässliche graue Browser-Default-Buttons im Lückentext-Tab — meine eigenen neu geschriebenen `<button onclick="fbLtReset()">` hatten KEIN Styling. `inject_lt.py` rührt Steuerbuttons nicht an; beim manuellen Story-Umbau IMMER den kanonischen Pill-Stil inline setzen. Siehe Memory `feedback_lueckentext-buttons-immer-pill-stil.md`. |
| `DE_A2_1022X-bewerbungen.html` | `3c5ffa1` | Gleicher Schreib-last-Reorder-Bug wie 1021V (Schreibwerkstatt vor Genus/Wortschatz trotz Klasse); Genus/Wortschatz-Timer-IDs (4↔5) vertauscht synchron zur neuen Position; Lückentext war schon 9 Vollwort-Lücken über 2 Überschriften — zu 1 Jonas-Bewerbungs-Story verschmolzen + 1 Lücke (`Chef`) ergänzt für exakt 10. |
| `DE_A2_1023G-verben-mit-dativ.html` | `3c5ffa1` | G-Datei mit **Grundform-Variante** (`data-base`): 12 isolierte Dativ-Verb-Sätze mit sichtbarem Nominativ-Hinweis `(sein Kollege →)` inline — architektonisch inkompatibel mit der Wortbank-basierten Grundform-Anzeige. Zu 1 Mark/Nina/Tom-Büro-Story mit 10 Lücken umgebaut (`data-answer`=Dativform, `data-base`=Grundform), inline-Hinweise entfernt. Genus/Schreibwerkstatt waren hier NUR vertauscht (kein Wortschatz-Tab in dieser Datei) — einfacherer Fall, Lückentext/Satzbau/MC-Dispatch-Indizes blieben unverändert. |
| `DE_A2_1024R-die-neue-sekretaerin.html` | `f9fb38f` | **Wichtiger Vorfall:** beim DOM-Move ist der Such-Anker `'author-footer'` fälschlich auf die CSS-Regel `.author-footer{...}` (nicht das HTML-`<div>`) angeschlagen — Block landete an falscher Stelle. Vor Commit bemerkt (`grep -n 'class="section'`-Kontrolle), sauber zurückgesetzt (`git show HEAD:DATEI.html > /tmp/x.html`, dann `cp` — NICHT `git checkout`, das scheitert an `.git/index.lock` in der Sandbox) und mit präzisem `<div class="author-footer">`-Anker neu gemacht. Neue Regel gespeichert: `feedback_dom-move-anchor-css-kollision.md`. Danach: Schreib-last-Reorder + Wortschatz-Timer-Index-Sync (auch `timerAutoStart(5)`-Aufrufe INNERHALB der Wortschatz-Funktionen mussten auf `(6)` geändert werden, nicht nur die sichtbare `id="timer-N"` — zwei getrennte Stellen!); 10 isolierte Lesetext-Lückensätze über „Tim" (Alex' Bruder) zu 1 Story verschmolzen. |

Alle Commits: Repo `daf-a2-uebungen`, Branch `main`.

## Neue Erkenntnisse dieser Fortsetzung (jetzt Teil der Checkliste)

1. **Timer-Index-Doppelverdrahtung.** Wenn Genus/Wortschatz beim Reorder die Position
   tauschen, gibt es oft ZWEI Stellen mit dem alten Index: die sichtbare
   `id="timer-N"`/`id="best-N"` UND interne `timerAutoStart(N)`/`timerStop(N)`/
   `timerResetOne(N)`-Aufrufe in den Tab-eigenen JS-Funktionen (z. B. bei jedem
   Wortschatz-Input-Feld). Beide müssen synchron umbenannt werden — sonst startet
   der Timer, zeigt aber nie etwas an (oder umgekehrt).
2. **DOM-Move-Anker müssen die volle Tag-Öffnung matchen**, nie den bloßen
   Klassennamen (`'<div class="author-footer">'` statt `'author-footer'`) — sonst
   Kollision mit der gleichnamigen CSS-Regel weiter oben in der Datei. Nach jedem
   Move: `grep -n 'class="section\|<!-- ===== TAB: GENUS\|<div class="author-footer">\|/container -->' DATEI.html`
   zur visuellen Reihenfolge-Kontrolle, BEVOR `inject_lt.py` läuft.
3. **G-Dateien mit sichtbarem Grundform-Hinweis inline** (z. B. `(sein Kollege →)`
   neben der Lücke) sind ein Signal für „inkompatibles Altformat" — beim Umbau auf
   FB-LT-STORY den Hinweis komplett entfernen, die Grundform wandert stattdessen
   automatisch in die Wortbank (Engine übernimmt das via `data-base`).
4. **Sichere Wiederherstellung bei verunglücktem Edit:** `git checkout -- DATEI`
   kann in der Cowork-Sandbox an einem fremden/stale `.git/index.lock` scheitern
   (Fehler „Unable to create index.lock … Another git process seems to be
   running"). Zuverlässiger Weg: `git show HEAD:DATEI.html > /tmp/x.html` dann
   `cp /tmp/x.html DATEI.html` (umgeht den Index komplett) und mit
   `diff /tmp/x.html DATEI.html` verifizieren (Exit 0 = identisch).

## Frühere Fortsetzung (2) — zur Erinnerung

## Auftrag

A2.1-Backlog (`htmlS/A2.1`) Datei für Datei auf den vollen Skill-Standard heben,
**bevor** der Lückentext-Tab auf FB-LT-STORY (kanonische Story, genau 10 Lücken,
keine Nummerierung) umgebaut wird. Nicht nur Nav-Architektur — das komplette
Pflicht-Audit (siehe Checkliste unten). Skill: `daf-lueckentext`, `daf-kern`,
`daf-disziplin`.

## Franks Arbeitsanweisung (verbindlich für den nächsten Thread)

- **Vor** jeder Datei kurz 2–3 nächste Dateien nennen.
- **Nach** Fertigstellung einer Datei: im Chrome öffnen, **NICHT schließen**
  (Kontrolle für Frank), und **sofort** mit der nächsten Datei weitermachen —
  nicht auf Rückmeldung warten.
- Autonom weiterarbeiten, keine leeren Zwischen-Antworten.

## Gesamtstand (check_lueckentext.py, ganzes Repo, Stand Ende dieser Session)

19 kanonisch / 91 Backlog vor dieser Session-Fortsetzung → nach dieser Fortsetzung
**91 Backlog, A2=90** (1018S und 1021V sind aus dem Backlog raus, macht netto
denselben Trend: A2-Backlog war 90 vor 1018S, jetzt wieder 90, weil 1018S beim
Zählen zuvor schon als Backlog-Datei mitgezählt wurde und 1021V neu dazukam —
kurz: **zwei weitere A2.1-Dateien fertig**, siehe Tabelle unten. Nächster Check
zu Beginn des nächsten Threads: `python3 scripts/check_lueckentext.py` ohne
Argument für den exakten Ist-Stand.

## In dieser Fortsetzung fertiggestellt (2 Dateien, beide gepusht)

| Datei | Commit | Kernfunde |
|---|---|---|
| `DE_A2_1018S-diphthonge.html` | `1d27b39` | War KEIN Reorder-Bug (kein Schreibwerkstatt-Tab in dieser S-Datei). Lückentext bestand aus 15 Teilwort-Lücken (nur der Diphthong-Buchstabe fehlte, z. B. `H__te`) über 10 nummerierte Einzelsätze verteilt — architektonisch inkompatibel mit FB-LT-STORY. Zu EINER Story (10 Vollwort-Lücken: Heute/Kleid/Bräutigam/Braut/Haus/Bäume/Freund/Zeit/Feuerwerk/freuen) umgebaut, alte `lueckeInit()`-Aufrufkette entfernt (hätte sonst beim Laden eine TypeError auf `#luecke-container`/`#total-2` geworfen und `uebungInit()`+`loadBestTimes()` lautlos verschluckt — im Browser verifiziert, dass Zungenbrecher-Liste (6 Einträge) weiterhin lädt). Alte FB-WORTBANK-MODULE-Konkurrenz war bereits selbstdeaktivierend, kein Konflikt. |
| `DE_A2_1021V-die-arbeitswelt.html` | `17c2dcb` | Klassischer Schreib-last-Reorder-Bug: DOM-Reihenfolge war …Satzbau(4)→**Schreibwerkstatt(5)**→Genus(6)→Wortschatz(7), obwohl `schreib-last`-Klasse „letzter Tab" suggerierte. Dispatch hatte zusätzlich `idx===6` für **beide** `initWortschatz()`+`initSchreibwerkstatt()` gemeinsam gegated (Index-Mismatch-Bug-Klasse). Fix: Schreibwerkstatt-Block physisch ans DOM-Ende verschoben (nach Wortschatz), Nav neu durchnummeriert (0–7), Dispatch auf zwei getrennte `if(idx===N)`-Zeilen aufgeteilt (6→Wortschatz, 7→Schreibwerkstatt, mit neuer `swInitialized`-Guard-Variable — `initSchreibwerkstatt()` hatte selbst KEINEN Idempotenz-Guard). Genus- und Wortschatz-Timer-IDs (`timer-5`/`timer-6`, `best-5`/`best-6`) waren hart in beiden Tab-Bodies UND in `GENUS_TIMER`-Variable verdrahtet — mussten synchron zur neuen Position getauscht werden. Lückentext war bereits exakt 10 Vollwort-Lücken über 2 unverbundene „Lückentext 1"/„Lückentext 2"-Überschriften — zu einer Mark/Tom-Bürokollegen-Story verschmolzen (Themen-Wörter identisch geblieben: Büro/Schreibtisch/Aufgaben/Arbeitgeber/Gehalt/Überstunden/Stress/Firma/Stelle/verdient). |

Beide Commits: Repo `daf-a2-uebungen`, Branch `main`, per
`bash scripts/safe-commit.sh "msg" DATEI.html` aus `htmlS/A2.1/`. Für den Push
war zu Sessionbeginn `bash scripts/setup-sandbox-credentials.sh` nötig (frische
Cowork-Sandbox, siehe CLAUDE.md „Cowork-Sandbox: einmaliger Auth-Setup pro
Session").

## Bereits vor dieser Fortsetzung erledigt (von einer parallelen/vorherigen Session)

`DE_A2_1016X-hoeflichkeit.html` (Commit `ae89ad6`) und
`DE_A2_1017G-praepositionen.html` waren beim Start dieser Fortsetzung bereits
**vollständig kanonisch** (alle 9 Check-Skripte grün, FB-LT-STORY bereits
eingespielt) — keine Änderung nötig, nur verifiziert.

## Neue Bug-Klasse, die diese Fortsetzung aufgedeckt hat

**„Dead-Init-Crash bei Architektur-fremden Lückentext-Tabs" (1018S).** Wenn ein
Lückentext-Tab NICHT dem Standard-Muster folgt (z. B. Teilwort-Lücken statt
Vollwort-Lücken, eigene Container-IDs wie `luecke-container`/`score-2`/`total-2`
statt `lueckenContainer`/`wortbank-luecken`), darf die alte Init-Funktion beim
Entfernen der alten Container **nicht einfach stehen bleiben** — sie wirft beim
nächsten `getElementById(...).textContent = …` auf `null` eine TypeError, die
das GESAMTE umgebende `<script>`-Tag ab dieser Zeile stumm abbricht (alle
nachfolgenden Top-Level-Aufrufe im selben Tag laufen nicht mehr — hier hätte es
`uebungInit()` und `loadBestTimes()` getroffen). Immer den Aufruf der alten
Init-Funktion aus der Init-Kette entfernen, nicht nur den HTML-Container.

## Vollständige Pre-Lückentext-Checkliste (pro Datei, unverändert, in dieser Reihenfolge)

1. **daf-kern-Nav-Architektur:** `<div class="nav-btn">` (nie `<button>`),
   `showSection`/`class="section"` (nie `showTab`/`class="tab"`). Hinweis: die
   `check_nav.py`-CSS-Signatur allein genügt NICHT als Beweis (1018S hatte
   Variante-C-CSS, aber `<button>`+`showTab`+`class="aktiv"` im Markup — vom
   Check als „konform" durchgewunken, weil er nur CSS-Muster prüft, nicht
   Tag/Funktionsname. Funktional lief es trotzdem korrekt, weil showTab/aktiv
   intern konsistent verdrahtet waren — im Zweifel den Nav-HTML-Quellcode
   selbst lesen, nicht nur dem grünen Check vertrauen).
2. **JS-Parse-Check über ALLE `<script>`-Blöcke:**
   ```bash
   node -e "const fs=require('fs'); const html=fs.readFileSync('DATEI.html','utf8'); const scripts=[...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)]; scripts.forEach((m,i)=>{ try{ new Function(m[1]); console.log(i,'OK'); } catch(e){ console.log(i,'ERR',e.message); } });"
   ```
3. **Genus-Tab vorhanden, ≥20 Wörter?** Sonst `scripts/inject_genus.py DATEI.html
   woerter.json`.
4. **Schreibwerkstatt wirklich letzter Tab — Nav UND DOM UND Dispatch:**
   `python3 scripts/check_schreib_last.py DATEI.html`. Bei Fund: Nav-`onclick`-
   Nummern neu durchnummerieren, `.section`-Block im DOM physisch verschieben
   (bei Base64-Bannern per Python/`sed`, NICHT Edit-Tool direkt auf der
   Base64-Zeile — riesige Zeilen sprengen Token-Limits von Read/Edit;
   Python-Skript mit Zeilen-Slicing funktioniert zuverlässig, siehe unten),
   Dispatch-`if(idx===N)`-Zeilen an neue Positionen anpassen (ggf. splitten,
   wenn zwei Inits am selben Index hingen), `initSchreibwerkstatt()` idempotent
   + gegated machen (eigene `swInitialized`-Variable, falls die Funktion selbst
   keinen `window.__swInited`-Guard hat). **Neu:** wenn Genus/Wortschatz-Tabs
   mit umsortiert werden, IMMER prüfen, ob ihre Timer-Anzeige-IDs (`timer-N`/
   `best-N`) und interne Timer-Index-Variablen (`GENUS_TIMER = N`) hart auf die
   ALTE Position verdrahtet sind — dann synchron mit umbenennen.
5. **Tote Button-Handler?** Grep auf Selektoren, die zu keiner erzeugten Klasse
   passen.
6. **Smart-Quote-Korruption?** Grep auf `class=“` (U+201C) in Input-Tags.
7. **Lückentext auf FB-LT-STORY umbauen:** zusammenhängende Story (keine
   Nummern, keine `<h2>`-Zwischentitel für „Text 1"/„Text 2"), genau 10
   `<input class="blank" data-answer="...">`-Lücken, bei G-Dateien zusätzlich
   `data-base="Grundform"`. Mehrere unverbundene Texte narrativ zu EINER
   Geschichte verschmelzen (running gag: Alex/Louise/Petra/Jens/Gwyneth/Max/
   Tina/Paul-Universum wiederverwenden — neu dazugekommen in dieser Fortsetzung:
   Mark/Tom als Bürokollegen-Paar, wiederverwendbar in weiteren Arbeitswelt-
   Lektionen 1022X–1028S). Danach:
   ```bash
   python3 scripts/inject_lt.py DATEI.html
   ```
   **Falls die Ausgabe `Hooks(N=?-nicht erkannt)` zeigt** (passiert, wenn der
   Lückentext-Tab-Index nicht automatisch aus dem Nav erkannt werden kann, z. B.
   bei stark abweichender Architektur wie 1018S): Hooks manuell nachtragen —
   ```bash
   python3 -c "
   path='DATEI.html'
   s=open(path,encoding='utf-8').read()
   hook='<!-- FB-LT-STORY-HOOKS --><script>window.fbLtTimerStart=function(){if(typeof timerAutoStart===\"function\")timerAutoStart(N);};window.fbLtTimerStop=function(){if(typeof timerStop===\"function\")timerStop(N);};</script>\n'
   i = s.rfind('</body>')
   s = s[:i] + hook + s[i:]
   open(path,'w',encoding='utf-8').write(s)
   "
   ```
   (N = der tatsächliche 0-basierte Tab-Index des Lückentext-Tabs in der
   finalen Nav-Reihenfolge.)
8. **Alle Check-Skripte grün:**
   ```bash
   python3 scripts/check_lueckentext.py DATEI.html
   python3 scripts/check_nav.py DATEI.html
   python3 scripts/check_serif.py DATEI.html
   python3 scripts/check_genus.py DATEI.html
   python3 scripts/check_genus_buttons.py DATEI.html
   python3 scripts/check_wortbank.py DATEI.html
   python3 scripts/check_schreib_last.py DATEI.html
   python3 scripts/check_schreib_pad.py DATEI.html
   python3 scripts/check_quotes.py DATEI.html
   ```
9. **Browser-Stichprobe** (Control_Chrome MCP): Datei via `open_url` öffnen,
   `list_tabs` für die tab_id, dann via `execute_javascript` mit expliziter
   `tab_id` (NICHT „current tab" — bei vielen offenen Tabs landet das sonst auf
   der falschen Seite, siehe Vorfall dieser Session, Outlook-Tab statt DaF-
   Datei). Jeden Tab-Index durchklicken, Section-Höhe > 0 prüfen,
   Lückentext-Lösungsbutton klicken → alle 10 Felder gefüllt+korrekt,
   Wortschatz-Container hat Kinder nach Tab-Öffnen (Dispatch-Bug-Check),
   Genus-Lösungsbutton klickt alle Chips in die Kategorien, Genus-Wortzahl
   stimmt (24).
10. **Commit + Push:**
    ```bash
    cd htmlS/A2.1 && bash ../../scripts/safe-commit.sh "DATEI: skillgerecht-Audit (...)" DATEI.html
    ```
    Push-Verifikation ist im Skript selbst eingebaut (vergleicht HEAD gegen
    `origin/main`). **Falls „FEHLER: Push NICHT angekommen" mit
    „could not read Username" erscheint:** frische Cowork-Session, erst
    `bash scripts/setup-sandbox-credentials.sh` aus dem Repo-Root laufen
    lassen, dann `git push origin main` im Unterordner nachholen (Commit war
    schon lokal da, nur der Push fehlte).
11. **Im Chrome öffnen, Tab NICHT schließen**, sofort nächste Datei beginnen.

## Technischer Trick: große Dateien lesen/editieren (Base64-Banner sprengen Read/Edit-Tool)

Read-Tool bricht ab, sobald IRGENDEINE Zeile im angeforderten `offset`/`limit`-
Bereich riesig ist (Base64-Banner-Zeilen sind oft 40.000+ Zeichen) — selbst bei
kleinem `limit`. Immer zuerst mit `grep -n` die Zeilennummern der Base64-Zeilen
identifizieren und beim `Read`-Aufruf gezielt DRUM HERUM lesen (offset direkt
NACH der Base64-Zeile ansetzen).

Für DOM-Verschiebungen (z. B. Tab-Reorder) über Base64-Banner hinweg NICHT das
Edit-Tool verwenden (Zeichenlimit/Kontext-Overhead), sondern Python mit
zeilenweisem Slicing:
```python
lines = open(path, encoding='utf-8').readlines()
block = lines[START-1:END]        # 1-indexiert -> 0-indexiert
rest  = lines[:START-1] + lines[END:]
# Einfügepunkt in rest suchen, dann block dort einfügen
```
Zuverlässiger als `sed`, weil Python nicht an Sonderzeichen im Base64-String
scheitert.

## Nächste Dateien (angekündigt, noch offen)

1. `DE_A2_1025V-die-firma.html`
2. `DE_A2_1026X-am-telefon.html`
3. `DE_A2_1027G-wechselpraepositionen.html`

Danach chronologisch weiter durch `htmlS/A2.1/DE_A2_10*` und `DE_A2_20*` bis
`DE_A2_2068S...`. Exakter Restzählstand zu Beginn des nächsten Threads:
`python3 scripts/check_lueckentext.py` **ohne** Dateiargument (ganzes Repo)
laufen lassen, dann `python3 -c "..."` mit `check_lueckentext.collect_repo()` +
`scan()` für die konkrete Dateiliste (Beispiel-Snippet steht im vorherigen
Übergabe-Stand, Git-Historie).

## Referenzen

- Skill `daf-lueckentext` — vollständige Spec (Story-Pflicht, Wortbank, Varianten)
- `CLAUDE.md` (Repo-Root B2) — Abschnitt „Lückentext ist IMMER eine kanonische Story"
- Memory: `project_lueckentext-a2-start-2026-07-02.md`,
  `feedback_skillgerecht-vor-lueckentext-vollstaendig.md`,
  `feedback_schreib-last-css-order-ist-nicht-dom-position.md`

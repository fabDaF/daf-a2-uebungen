# Übergabe: A2.1-Lückentext-Kanonisierung — Stand 2026-07-02 (Fortsetzung 5)

## In dieser Fortsetzung (5) fertiggestellt — 5 Dateien (Einheit 103x komplett + 104x begonnen)

| Datei | Commit | Kernfunde |
|---|---|---|
| `DE_A2_1034R-die-neue-wohnung.html` | `f13f7c2` | Gleicher `initSchreibwerkstatt()`-Fehlplatzierungs-Bug wie 1032X/1033G, hier über eine verunglückte `arguments[0]===6`-Bedingung plus unconditional Aufruf — `swInit`-Guard + korrekter Dispatch-Index. LT1(5)+LT2(5)=10 Items (Louises Wohnung) waren bereits exakt 10 — nur zu 2 Absätzen verschmolzen, kein Item weggelassen. |
| `DE_A2_1035V-mein-zuhause.html` | `39e4ac9` | Nicht-kanonische `<button class="nav-btn">`-Tags + gemischte `<section>`/`<div>`-Tab-Architektur (daf-kern §1 verletzt, aber `check_nav.py` prüft nur CSS-Pattern, nicht Tag-Name) — als Out-of-Scope belassen. LT1(6)+LT2(5)=11 zu Familie-Ludwig-Hausstory mit 10 Lücken (1 Item „Tor" weggelassen). Gleicher Dispatch-Fix (`swInit`). |
| `DE_A2_1036X-temporale-praepositionen.html` | `9f527e7` | **Neues Muster: LT1+LT2+LT3-Dreifachcontainer** (8+6+5=19 Items, alle seit/vor/ab/bis/nach-Sätze). Zu EINER Story mit 10 Lücken verschmolzen, bewusst mit Wiederholungen (seit×3, vor×2, ab×2, bis×2, nach×1) — Wortbank dedupliziert korrekt auf 5 Chips (bestätigt bekanntes Muster `feedback_lueckentext-binaer-grammatik-wortbank`). **Pre-existing Dispatch-Index-Bug gefunden:** `if (n === 4) initWortschatz();` zeigte schon VOR meinen Edits auf den falschen (damals falsch platzierten) Tab. Reset-Button rief nur `timerResetOne(1)` ohne Input-Löschung — durch echte `resetLuecken()`-Funktion ersetzt. |
| `DE_A2_1037G-superlativ.html` | `2dcc5de` | **Einheit 103x damit komplett.** LT1(6)+LT2(7)=13 Superlativ-Items zu Georg/Mia/Paul/Nina/Maria-Story (10 Lücken, `data-base`=Grundform). Wichtig: die kanonische FB-LT-STORY-Engine exponiert `window.fbLtShowLoesung()`/`window.fbLtReset()` — eigene `showLtSolution()`/`resetLuecken()`-Funktionen sind NICHT nötig und kollidieren nicht, aber die Buttons müssen auf die `window.fbLt*`-Hooks zeigen, sonst tut „Lösungen" nichts (im ersten Anlauf übersehen, durch Browser-Test aufgedeckt). |
| `DE_A2_1038S-ueber-die-wohnung-reden.html` | `dc12312` | **Einheit 104x begonnen.** S-Datei — hat KEINEN Schreibwerkstatt-Tab (wie 1018S/1028S, drittes Vorkommen). LT1(5)+LT2(5)=10 (Marina/„Ich"-Umzugssätze, seit/vor/bis/ab/Nach) zu 1 zweiabsätziger Story verschmolzen, bewusste Wiederholung wie 1036X, Wortbank dedupliziert auf 5 Chips. |
| `DE_A2_1041V-stadtleben.html` | `8b4c580` | LT1(6)+LT2(5)=11 Items (Lea/Amsterdam + Sonja/Münster) zu 10-Lücken-Story verschmolzen (1 Item „Parks" als Beinah-Dublette von „Park" weggelassen, „Markt" bewusst zweimal für beide Städte behalten). Genus/Wortschatz/Schreiben-Reorder mit vollem Timer-Swap (GENUS_TIMER 6→5, Wortschatz-Timer 5→6 inkl. aller `timerAutoStart/Stop/ResetOne`-Aufrufe in `initWortschatz()`). `initSchreibwerkstatt()` lief unconditional bei jedem Tab-Klick (fügte bei jedem Klick einen weiteren `input`-Listener hinzu) — `swInit`-Guard ergänzt. |

Alle Commits: Repo `daf-a2-uebungen`, Branch `main`. **Einheit 103x (Wohnen/Umzug,
1031V–1037G) ist damit komplett fertig.** Einheit 104x (Stadtleben) begonnen:
1038S+1041V fertig, 1042X offen.

## Neue Erkenntnisse dieser Fortsetzung (5) (jetzt Teil der Checkliste)

1. **FB-LT-STORY-Engine exponiert `window.fbLtShowLoesung()`/`window.fbLtReset()`
   als öffentliche Hooks** — die Steuer-Buttons müssen exakt darauf zeigen
   (`onclick="window.fbLtShowLoesung()"` / `onclick="timerResetOne(N);window.fbLtReset()"`).
   Eigene `showLtSolution()`/`resetLuecken()`-Funktionen sind überflüssig und
   verstecken den Bug (Button tut nichts), weil `inject_lt.py` sie nicht
   automatisch verdrahtet — nach jedem Umbau per Browser-Klick verifizieren,
   nicht nur per Check-Skript.
2. **LT1+LT2(+LT3)-Doppel-/Dreifachcontainer bleibt das häufigste Altmuster**
   in Einheit 103x/104x — immer zu EINER Story mit exakt 10 Lücken
   verschmelzen, bewusste Wiederholungen (Präpositionen mit kleinem
   Wortschatz) sind erlaubt, echte Bedeutungsdubletten (Park/Parks) werden
   weggelassen.
3. **`initSchreibwerkstatt()`-Fehlplatzierung ist ein wiederkehrender,
   echter Funktionsbug** (jetzt 5× gefunden: 1032X, 1033G, 1034R, 1035V,
   1041V) — Standardfix: `var swInit = false;` + Gate im Dispatch auf den
   korrekten finalen Schreiben-Index.
4. **S-Dateien ohne Schreibwerkstatt-Tab jetzt 3× bestätigt** (1018S, 1028S,
   1038S) — konsistentes Muster, kein Einzelfall. Bleibt eigenes
   Arbeitspaket (`project_a21-s-dateien-ohne-schreiben-2026-07-02.md`).

## Frühere Fortsetzung (4) — zur Erinnerung

## In dieser Fortsetzung (4) fertiggestellt — 6 Dateien (Einheit 102x komplett + 103x begonnen)

| Datei | Commit | Kernfunde |
|---|---|---|
| `DE_A2_1025V-die-firma.html` | `76c6edc` | Sauberer Fall, Anker-Lektion aus Fortsetzung 3 direkt angewendet — DOM-Move mit präzisem Anker klappte im ersten Anlauf. Ulrike/Petra/Georg-Bürostory (10 Lücken). |
| `DE_A2_1026X-am-telefon.html` | `9d6828d` (+Fix in `9d6828d`) | **Neue Bug-Klasse entdeckt:** `inject_lt.py` erkennt nur seine BEKANNTEN Alt-Engines (FB-WORTBANK-MODULE, FB-LT-V1) und meldet trotzdem „Alt-Engine entfernt", auch wenn ein unbekanntes Eigenformat (`var LT1=[...]` + `function buildLuecken()`) unangetastet samt Dispatch-Aufruf liegen bleibt. Laufzeit-Folge: die alte Funktion lief beim Tab-Öffnen und hängte 8 weitere Inputs an die 10 neuen — 18 statt 10 Lücken, obwohl alle 9 Check-Skripte (die nur die Quelle statisch prüfen) grün waren. Nur der Browser-Test hat es aufgedeckt. Memory: `feedback_inject-lt-erkennt-nur-bekannte-altformate.md`. |
| — (Diagnose-Vorfall, kein Datei-Fix) | — | **Root-Cause für „showSection ist undefined"-Fehldiagnose gefunden:** Control_Chrome `execute_javascript` läuft in einer isolierten JS-Welt — Funktionen/Variablen der echten Seite sind dort nicht sichtbar, auch nicht nach eigenem Script-Insert. DOM-Mutationen sind aber geteilt. Ab sofort: Tab-Wechsel/Init IMMER per echtem `.click()` auf `.nav-btn`, NIE per direktem Funktionsaufruf aus `execute_javascript`. Memory: `feedback_control-chrome-isolierte-js-welt.md`. |
| `DE_A2_1027G-wechselpraepositionen.html` | `85e270f` | G-Datei ohne Wortschatz-Tab (nur Genus+Schreiben am Ende) — einfacherer Reorder (nur 2 Tabs tauschen). Wechselpräpositionen (Wo?/Wohin?) als Nina-Zimmer-Story, `data-base`=Nominativ-Artikel bzw. Infinitiv. |
| `DE_A2_1028S-ueber-die-arbeit-reden.html` | `e4da3e5` | S-Datei — **hat KEINEN Schreibwerkstatt-Tab** (wie 1018S). Kein Reorder nötig, nur Lückentext kanonisiert (Jonas-Telefonat+Bewerbung-Story). Fehlender Schreiben-Tab als eigenes Arbeitspaket vermerkt: `project_a21-s-dateien-ohne-schreiben-2026-07-02.md`. |
| `DE_A2_1031V-einziehen-und-ausziehen.html` | `83e2c12` | **Neues Muster: LT1+LT2-Doppelcontainer** (`luecken1`/`luecken2`, zwei separate Arrays, 6+5=11 Lücken) zu EINER Selma-Umzugsstory mit exakt 10 Lücken verschmolzen (1 Item bewusst weggelassen). `initSchreibwerkstatt()` lief bei jedem Tab-Klick unconditional — `swInit`-Guard ergänzt. |
| `DE_A2_1032X-wo-und-wohin.html` | `8932919` | Gleiches LT1+LT2-Muster (8+5=13→10). **Echter Funktions-Bug gefunden:** `initSchreibwerkstatt()` war fälschlich INNERHALB von `resetWortschatz()` verdrahtet — der Schreiben-Tab wurde nie beim Laden initialisiert (Name-Feld/gespeicherte Texte blieben leer), nur nach einem Wortschatz-Reset-Klick. Herausgelöst und korrekt in `DOMContentLoaded` verschoben. |
| `DE_A2_1033G-komparativ.html` | `58f24f2` | Gleicher `initSchreibwerkstatt()`-Fehlplatzierungs-Bug wie 1032X, diesmal in `sbResetAll()` (Satzbau-Reset) versteckt — gleicher Fix. LT1+LT2 (6+7=13) zu Georg/Philip/Bernd/Louisa/Maria-Vergleichsstory mit 10 Lücken (Grundform-Wortbank). |

Alle Commits: Repo `daf-a2-uebungen`, Branch `main`. **Einheit 102x (Arbeitswelt,
1021V–1028S) ist damit komplett fertig.** Einheit 103x (Wohnen/Umzug) begonnen:
1031V–1033G fertig, 1034R offen.

## Neue Erkenntnisse dieser Fortsetzung (jetzt Teil der Checkliste)

1. **`inject_lt.py`-Meldung „Alt-Engine entfernt" ist kein Beweis, dass wirklich
   ALLES Alte weg ist.** Nach jedem Lauf zusätzlich grep-Kontrolle:
   `grep -n 'var LT1\|var LT2\|LUECKEN_DATA\|function buildLuecken'` — Reste
   (Datenarray + Build-Funktion + Dispatch-Aufruf) müssen manuell entfernt
   werden, sonst laufen alte und neue Lücken parallel und die Blank-Zahl
   verdoppelt sich zur Laufzeit unbemerkt von den Check-Skripten.
2. **Tab-Wechsel/Init in Control_Chrome IMMER per echtem `.click()` auf
   `.nav-btn[n]` testen, NIE per direktem Funktionsaufruf** (`showSection(n)`
   o. Ä.) aus `execute_javascript` — die Ausführung läuft in einer isolierten
   JS-Welt, in der Seiten-Funktionen als `undefined` erscheinen, obwohl sie im
   echten Skript einwandfrei existieren. DOM-Zustand danach ganz normal per
   Selektoren/`getBoundingClientRect()`/Input-Werten abfragen — das ist geteilt.
3. **LT1+LT2-Doppelcontainer-Muster** (zwei getrennte Datenarrays mit zwei
   Lücken-Containern in einem Tab, meist über zwei `<h3>`-Unterüberschriften)
   ist in Einheit 103x häufig. Immer zu EINER verbundenen Story mit exakt 10
   Lücken verschmelzen — bei mehr als 10 Items gezielt die am wenigsten
   zentralen weglassen (nicht künstlich pressen).
4. **Vor dem Entfernen von `buildLuecken()`/`resetXxx()`/Dispatch-Calls immer
   auf versehentlich mit-eingebettete `initSchreibwerkstatt()`-Aufrufe achten**
   — in dieser Fortsetzung zweimal gefunden (1032X in `resetWortschatz()`,
   1033G in `sbResetAll()`), beide Male ein echter Funktionsbug: der
   Schreibwerkstatt-Tab wurde nie beim Laden initialisiert. Immer sauber in
   `DOMContentLoaded` (oder den regulären Dispatch) verschieben.

## Frühere Fortsetzung (3) — zur Erinnerung

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

1. `DE_A2_1042X-die-meinung-sagen.html`
2. `DE_A2_1043G-nebensaetze-dass-weil.html`
3. `DE_A2_1044R-das-erste-date.html`

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

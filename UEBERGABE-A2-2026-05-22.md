# A2-Übergabe — was offen ist (22. Mai 2026)

In dieser Session erledigt: Audit (siehe `A2-AUDIT-2026-05-22.md`), HTML-Attribut-Quotes
in 10 Dateien gefixt, 2044R Alex (weiblich) → Cousine Louise konsolidiert,
Querverweise in 1024R/1034R/2014R/2034R eingebaut, Nav-Label „Schreiben" →
„Schreibwerkstatt" in 37 vorhandenen Tabs, Skill `daf-schreibwerkstatt` auf die neue
Reichweite (R/X/V/G/W/C) ausgeweitet, alles committet und gepusht.

Was offen ist und wie es weitergeht:

## 1. Schreibwerkstatt-Rollout für die 49 fehlenden Dateien

24 V, 24 G, 1 W. Ablauf: in `scripts/configs_a2.py` einen Block pro Lektion ergänzen
mit fünf thematisch passenden Mikroaufgaben. Dann

```bash
python3 scripts/add-schreibwerkstatt-v2.py --niveau A2 --basis "htmlS/A2.1" 1011V 1013G 1015V …
```

Pro Datei ca. 8–10 Minuten Design der Mikroaufgaben (an die Vokabel- bzw.
Grammatikreihe gebunden, siehe Skill-Update). Insgesamt rechne mit zwei Sessions
für die 49 Dateien plus JSDOM-Test (success-Modus + needs-activation-Modus).

Sonderfall **1063G Futur I**: hat KEINE Schreibwerkstatt-Implementierung, das CSS
für den Customer-Success-Fallback ist aber schon eingebaut. Die G-Datei kann mit
dem Standardpatcher mitgenommen werden — die fünf Aufgaben sollten alle im Futur I
formuliert sein, damit die Grammatik explizit erzwungen wird.

## 2. Anführungszeichen-Aufräumlauf

Aktueller Stand: HTML-Attribute repariert (44 Stellen), Schaden meiner zu greedy
gewordenen ersten Reparatur rückgängig gemacht. **Noch offen:** ASCII-Schluss-Quotes
in HTML-Text (geschätzt 280+) und englisches U+201D als Schluss anstelle U+201C
(geschätzt 250+).

Beim nächsten Anlauf: explizite Unicode-Codepunkte verwenden (kein Inline-Pasten von
typografischen Quotes ins Skript), non-greedy `*?`-Quantifier, Tokenizer der Datei
in script/tag/text-Bereiche, damit JS-Strings und HTML-Attribute nicht versehentlich
angefasst werden. Stichproben-Test nach jedem Lauf an 1014R (am stärksten
betroffen).

## 3. R-Texte mit echtem Story-Bogen ausstatten

Die in dieser Session eingebauten vier Querverweise sind Tracer-Bullets. Für die
volle Wirkung des Hauptdarsteller-Bogens (Alex + Louise) müssten:

- **1014R** drei vorbereitete Querverweise zu späteren Lektionen bekommen (z.B.
  Gwyneth/Max-Paar erscheint später wieder, Tina taucht in 2034R kurz auf, etc.).
- **1044R** „Das erste Date" chronologisch klären (entweder vor Hochzeit gesetzt
  oder als „erstes offizielles Date" formuliert).
- **1064R** Tante/Onkel-Frage entscheiden: ist Alex Hermines Onkel via Louise oder
  ist es eine andere Konstellation? Aktuell steht „Alex' Nichte Hermine" — passt
  zur Story, wenn Alex Louises Mann und damit Hermines Anstand-Onkel ist.
- **2054R** Sachtext über soziale Netzwerke einen Personen-Anker geben (Louise
  oder Hermine als Beispiel-Einstieg).
- **2064R** Camping mit Nils einladen, eventuell auch Hermine erwähnen.

Diese Anpassungen sind kosmetisch — keine Substanz-Änderungen, nur weitere
Querverweis-Sätze in den bestehenden Texten.

## 4. daf-audit-Skill am Ende durchlaufen lassen

Nicht in dieser Session erledigt. Vor dem nächsten produktiven Release:
`anthropic-skills:daf-audit` über alle 98 Dateien laufen lassen — prüft, ob alle
Pflicht-Skills korrekt angewendet wurden. Browser-Stichproben an 3–4 Dateien (eine
mit Schreibwerkstatt aus dieser Session, eine R-Datei mit Querverweis, eine
G-Datei nach V/G/W-Rollout).

## 5. Skill-Reinstall

Die Skill-Quelle in `skills/daf-schreibwerkstatt/SKILL.md` ist aktualisiert. Damit
Cowork den neuen Stand lädt, muss der Skill als `.skill`-Paket neu installiert
werden — `anthropic-skills:skill-verwaltung` zeigt den Workflow.

---

**Plug-and-Play für Folgesession:** in dieser Reihenfolge angehen — V/G/W-Rollout
(Hauptarbeit) → Anführungszeichen-Aufräumlauf → R-Text-Feinschliff → daf-audit.

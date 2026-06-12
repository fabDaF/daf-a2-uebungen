# Satzbau-Rollout A2 — verbindliche Spezifikation

Beschlossen am 2026-06-12 (Frank + Claude). Gilt für alle 84 A2-Dateien mit
`satzbauData` im Repo `daf-a2-uebungen` (htmlS/A2.1). Ergänzt den Skill
**daf-satzbau**; bei Widersprüchen gilt diese Spec, bis der Skill-Text
nachgezogen ist.

## Staffel (ersetzt die bisherige A1/A2-Zeile „8–12")

| Niveau | Wörter | Modus |
|---|---|---|
| A1 | 5–9 | freier Bau, nur einfache Hauptsätze und Fragen, KEINE Kommasätze |
| A2 einfache Sätze | 6–10 | freier Bau |
| A2 Kommasätze | 9–14 (14 hart) | **Hybrid:** bis 10 Wörter freier Bau, ab 11 Wörtern geführter Gerüst-Modus (`geruest_patch.js`) |

Satzzeichen-Chips zählen nicht mit. Zu kurze Sätze mit Zeit-/Ortsangaben
verlängern, nie künstlich aufblähen.

## Kommasatz-Quote

Pro Satzbau-Tab (üblich 7–8 Sätze): **mindestens 2 Kommasätze**, sobald die
Lektion mindestens einen Nebensatz-Konnektor oder aber/sondern kennt.
Darunter immer mindestens eine Frage (`punct: '?'`). Einfacher Kommasatz =
genau EINE Verzweigung (HS + NS oder HS, aber HS) — nie geschachtelt.

## Konnektoren — nur Gelerntes

Drei Familien, jeweils erst ab der Lektion erlaubt, in der sie eingeführt
sind (Freigabetabelle siehe unten, Schritt 1 des Rollouts):

1. **Position 0:** und, oder (KEIN Komma davor), aber, denn, sondern (Komma davor)
2. **Adverb Position 1 + Inversion, kein Komma:** dann, danach, deshalb, trotzdem
3. **Nebensatz + Komma, Verb-Ende:** weil, dass, wenn, (spät-A2: als)

Komma ist eigener Chip (`','` in parts UND valid), CSS `.punct-chip`-Regel
muss in der Datei stehen (daf-satzbau §Komma als Chip).

## Beide Stellungen als Lösung

Wo grammatisch sauber, akzeptiert `valid` beide Reihenfolgen — Nebensatz
vorn und hinten („Weil ich krank bin, bleibe ich zu Hause." / „Ich bleibe
zu Hause, weil ich krank bin."). Der Komma-Chip wandert in den
valid-Arrays mit.

## Rollout-Schritte

1. **Konnektoren-Freigabetabelle** aus den 84 Dateien + Quell-PDFs
   extrahieren → `references/a2-konnektoren.md` (Lektionscode → erlaubte
   Konnektoren). Vor dem Schreiben neuer Sätze IMMER konsultieren.
2. **`scripts/check_satzbau_laenge.py`** (B2-Root) um die A1/A2-Staffel
   erweitern, inkl. Minima und Kommasatz-Quote.
3. **Batch pro Einheit** (101x → 106x, dann 201x → 206x): Sätze auf
   Staffel bringen, Kommasatz-Quote herstellen, valid-Varianten ergänzen.
   Kein Subagent (Skill-Schwur).
4. **Gerüst-Patcher** nur für Kommasätze ab 11 Wörtern:
   `node scripts/geruest_patch.js DATEI.html --write`, danach PFLICHT
   Anker-Review (suspectVerb-Lücke: 1.-Person--e-Formen!) + `caps:true`
   prüfen. Verben, Konnektoren (= Zielform!) und Komma-Chips NIE als Anker.
5. **Pro Datei:** JSDOM-Erstlade-Test (nackter Pfad, URL-Option gegen
   localStorage-Artefakt). **Pro Einheit:** Browser-Stichprobe mit
   sbShowSolution.
6. Vor jedem Commit: check_satzbau_laenge, check_wortbank, check_serif,
   Anführungszeichen-Regex. Commit via safe-commit.sh.
7. **Skill-Update daf-satzbau** (Staffel-Tabelle + Hybrid-Regel + neue
   Reference) als .skill verpacken → Frank installiert.

## Randbefunde (beim Rollout miterledigen)

- `DE_A2_1014R-die-hochzeit.html`: satzbauData vorhanden, aber alle
  parts-Arrays leer (Min/Max 0) — reparieren.
- Bestand 2026-06-12: kürzester Satz 3 Wörter, nur 18/84 Dateien mit
  Kommasatz — fast alle Dateien brauchen Neuschreibungen.

# A2 — Konnektoren-Freigabetabelle (Satzbau-Rollout)

Erstellt 2026-06-12. Gehört zu `ROLLOUT-SATZBAU-A2.md`, Schritt 1. Beim
Skill-Update (Schritt 7) wandert diese Datei nach
`daf-satzbau/references/a2-konnektoren.md`.

**Regel:** Beim Schreiben/Verlängern von Satzbau-Sätzen darf ein Konnektor
nur verwendet werden, wenn die Lektion ihn (oder eine frühere) bereits
eingeführt hat. Lektionscode = Reihenfolge im Kurs (10xx = Einheit 1 / A2.1,
20xx = Einheit 2 / A2.2). Konnektor wird **ab** der Einführungslektion für
alle folgenden Lektionen frei.

## Einführungslektionen (belegt aus Lektionstiteln)

| Ab Lektion | Konnektoren | Beleg / Familie |
|---|---|---|
| 1011 (A2-Start) | **und, oder, aber, denn, sondern** | A1-Bestand, koordinierend; keine eigene A2-Lektion nötig |
| 1043 | **dass, weil** | `1043G · Nebensätze mit dass und weil` |
| 1062 | **wenn, dann** | `1062X · Sätze mit wenn, dann` |
| 2023 | **deshalb, trotzdem, danach, außerdem** | `2023G · Position Konnektoren` (Adverbkonnektoren) |
| 2033 | **als** (temporal, Vergangenheit) | `2033G · Das Präteritum` (als + Präteritum) |
| 2046 | **damit** (final) | `2046X · Finalsätze` |

## Kumulativ erlaubte Mengen pro Lektionsblock

| Lektionsspanne | Erlaubt (kumulativ) |
|---|---|
| 1011 – 1042 | und, oder, aber, denn, sondern |
| 1043 – 1061 | + dass, weil |
| 1062 – 2022 | + wenn, dann |
| 2023 – 2032 | + deshalb, trotzdem, danach, außerdem |
| 2033 – 2045 | + als |
| 2046 – 2068 | + damit |

## Satzbau-Einsatz nach Familie (daf-satzbau §Konnektoren, ROLLOUT-Spec)

1. **Position 0, koordinierend:** und, oder (KEIN Komma davor) · aber, denn,
   sondern (Komma davor). Beispiel: „Ich bleibe zu Hause, denn ich bin krank."
2. **Adverbkonnektor, Position 1 + Inversion, KEIN Komma:** dann, danach,
   deshalb, trotzdem. Beispiel: „Ich bin krank, deshalb bleibe ich zu Hause."
   (Komma steht hier wegen des Hauptsatz-Hauptsatz-Anschlusses, nicht wegen
   des Adverbs.)
3. **Nebensatz + Komma, Verb am Ende:** weil, dass, wenn, (ab 2033: als).
   Beide Stellungen in `valid` akzeptieren — Nebensatz vorn UND hinten:
   „Weil ich krank bin, bleibe ich zu Hause." / „Ich bleibe zu Hause, weil
   ich krank bin." Komma-Chip wandert in den valid-Arrays mit.
4. **Final, Nebensatz + Komma, Verb am Ende:** damit (ab 2046).
   „Ich lerne jeden Tag, damit ich die Prüfung bestehe."

## Hinweise

- „dann" ist hier der Konsequenz-Anschluss aus dem wenn-dann-Paar (ab 1062),
  nicht das rein temporale „dann" (das ist A1-Bestand und immer erlaubt).
- Komma ist immer ein **eigener Chip** (`','` in `parts` UND `valid`); die
  `.punct-chip`-CSS-Regel muss in der Datei stehen (daf-satzbau §Komma als
  Chip).
- Kommasatz = genau EINE Verzweigung (HS+NS oder HS, aber HS) — nie
  geschachtelt (ROLLOUT-Spec).

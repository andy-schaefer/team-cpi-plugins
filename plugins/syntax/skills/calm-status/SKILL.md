---
description: Erzeugt die wöchentliche Status-Präsentation für ein Statusmeeting aus einem SAP Cloud ALM Export und den Besprechungsnotizen der Vorwoche. Aufruf mit der Kalenderwoche als Argument, z.B. /calm-status 31 oder /calm-status KW31. Liest "Items_For Analysis_KW<NN>.xlsx" und "MeetingMinutes_KW<NN-1>.txt" aus dem aktuellen Verzeichnis, gruppiert die Aufgaben pro Projektteam (alphabetisch), übernimmt bei Follow-up-Tasks aus den Notizen den Kommentar in die Folie und trägt bei allen anderen offenen Tasks den bestehenden CALM-Kommentar fort. Verwenden, wenn der Nutzer den wöchentlichen Interface-/Projektstatus als PowerPoint braucht. Wiederholter Aufruf für dieselbe KW aktualisiert dieselbe Datei.
---

Du erzeugst die wöchentliche Status-Präsentation. Argument `$ARGUMENTS` = Kalenderwoche (z.B. `31`, `KW31`).

Arbeite im **aktuellen Verzeichnis** (dort liegen die Eingabedateien und das Marken-Template). Die Skripte
liegen im Plugin unter `${CLAUDE_PLUGIN_ROOT}/skills/calm-status/scripts/`. Details zu Datei- und
Notizformat: `reference/format.md`.

## Ablauf

### Schritt 0 — Abhängigkeiten (einmalig, still)
```bash
python -c "import openpyxl, pptx" 2>/dev/null || python -m pip install --quiet openpyxl python-pptx
```

### Schritt 1 — Daten aufbereiten (mechanisch)
```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/calm-status/scripts/prepare_status.py" <KW>
```
Das Skript findet `Items_For Analysis_KW<NN>.xlsx`, das Template `*WeeklyStatus.pptx` und – falls vorhanden –
`MeetingMinutes_KW<NN-1>.txt`, ordnet die Follow-up-Tasks den CALM-IDs zu, gruppiert nach Team (alphabetisch)
und schreibt `.status_work/KW<NN>.json`. Prüfe die ausgegebene Zusammenfassung (Team-Zählung, Quelle je Task,
nicht zugeordnete Follow-ups). Bricht das Skript ab (fehlende Datei / Spalte), melde das dem Nutzer und stoppe.

### Schritt 2 — Kommentare zusammenfassen (KI, dein Teil)
Lies `.status_work/KW<NN>.json`. Falls `.status_work/KW<NN>.summaries.json` schon existiert, lies sie auch und
**behalte vorhandene Zusammenfassungen bei** (Stabilität bei Korrektur-Reruns) — erzeuge nur fehlende neu.
Erzeuge für **jede** Aufgabe (über alle Teams) aus ihrem Feld `raw` **eine prägnante Zeile** (≤ ~180 Zeichen):

- Sprache = Sprache der Quelle (hier Deutsch), sachlich, ohne Füllwörter, Kernaussage zuerst.
- Bei `source` = `Meeting KW…`: fasse den Follow-up-Task zusammen (was ist zu tun / entschieden). Nutze
  `mm_context` (die Besprechungsnotizen) für Präzision, aber erfinde nichts.
- Bei `source` = `CALM`: fasse den letzten Kommentar/History-Eintrag zusammen (Stand fortführen).
- Leeres `raw` → `"—"`.

Schreibe die Zuordnung `{ "<ID>": "<Zusammenfassung>", … }` (zusammengeführt mit vorhandenen) nach
`.status_work/KW<NN>.summaries.json` (UTF-8).

### Schritt 3 — Präsentation rendern (mechanisch)
```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/calm-status/scripts/build_status.py" <KW>
```
Erzeugt `<Kunde>_InterfaceStatus_StatusMeeting_KW<NN>.pptx`: Titelfolie + Tabellenfolien **pro Team**
(alphabetisch, 7 Zeilen/Folie, große Teams über mehrere Folien — Teams werden nie gemischt). Spalten:
`ID · Topic · Status · Last update · Last comment / change`. Meeting-Kommentare sind mit `»` und `[Meeting KW…]`
markiert.

### Schritt 4 — Visuelle Kontrolle (optional, empfohlen)
Exportiere 2–3 Folien als PNG und sieh sie dir an:
```powershell
$dir=(Get-Location).Path; $pptx=Join-Path $dir "<Ausgabedatei>.pptx"; $o=Join-Path $dir "_preview"
if(Test-Path $o){Remove-Item $o -Recurse -Force}; New-Item -ItemType Directory $o | Out-Null
$pp=New-Object -ComObject PowerPoint.Application
try{$p=$pp.Presentations.Open($pptx,$true,$false,$false); $i=0
 foreach($s in $p.Slides){$i++; $s.Export((Join-Path $o ("slide{0}.png" -f $i)),"PNG",1600,900)}; $p.Close()}
finally{$pp.Quit()}
```
Lies die PNGs (Titel + eine große Teamtabelle). Räume `_preview` danach wieder auf.

### Schritt 5 — Ergebnis melden
Nenne: Ausgabepfad, Aufgaben/Teams gesamt, Folienzahl pro Team, welche Tasks ihren Kommentar aus den
Notizen bekommen haben, und – falls vorhanden – die nicht zugeordneten Follow-ups aus den Notizen
(`mm_unmatched`), damit nichts still verloren geht.

## Hinweise
- **Idempotent:** gleiche KW → gleiche Ausgabedatei wird überschrieben. Bei kurzfristiger Korrektur der
  Eingabedatei einfach erneut aufrufen. Soll komplett neu zusammengefasst werden, lösche vorher
  `.status_work/KW<NN>.summaries.json`.
- Kein Rückschreiben nach CALM — die Notizen füllen nur die Präsentation.
- Fehlt `MeetingMinutes_KW<NN-1>.txt`, läuft alles weiter; dann stammen alle Kommentare aus CALM.

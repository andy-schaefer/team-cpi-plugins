# CALM status – input formats & parsing rules

Reference for the `calm-status` skill. The scripts implement all of this; read this only when an
input format looks different from what's described or a run produces unexpected grouping/matching.

## 1. CALM export `Items_For Analysis_KW<NN>.xlsx`

- One sheet, row 1 = headers. **Column order is NOT stable** between weekly exports (observed 51 vs 52
  columns), so `prepare_status.py` maps every field by **header name**, never by position.
- Fields consumed (German headers): `Titel`, `ID`, `Status`, `Team`, `Kommentare`, `Historie`,
  `Beschreibung`, `Geändert am`.
- **Teams** = the `Team` column, values like `[Projektteam] Integration`,
  `[Projektteam] Technical Architecture und Infrastruktur`, `[Projektteam] Data Management`,
  `[Projektteam] Document Management`. Grouping is by this raw value; the deck strips the
  `[Projektteam] ` prefix for slide titles. Teams are sorted **alphabetically**.
- `Status` values seen: `Offen`, `In Bearbeitung` (deck colors: Offen = grey, In Bearbeitung = green,
  Fertig/Done = dark green).
- `Geändert am` holds a JS date string (`Wed Jul 08 2026 …`) → normalized to `DD.MM.YYYY`.
- `Titel` noise prefixes stripped for the "Topic" column: `Vorbereitung & Durchführung F2S-Workshop [..] "…"`
  and `Vorbereitung/Durchführung WS-Inhalt: …`; surrounding quotes removed.

## 2. Meeting minutes `MeetingMinutes_KW<NN-1>.txt`

Plain text, two sections:

```
Besprechungsnotizen:
  <narrative paragraphs>            # kept as mm_context (extra context for summaries)

Folgeaufgaben:
  <Title>: <description> (<Owner>)  # one follow-up per block, blocks separated by blank lines
  =>Update 3-2746 und 3-2825        # action line(s): references CALM task IDs
  ...
```

Follow-up action line grammar (`=>` prefix):
- `=>Update 3-<n> [und 3-<m> …]` → these CALM tasks get their "Last comment / change" from this follow-up.
- `=>Neu 3-<n>` → same; the task was newly created after the meeting (it appears in the next export).
- a plain note (`=>Die Datei …`) or **no `=>` line** → no CALM id → collected into `mm_unmatched`
  (reported to the user, **not** shown in the deck).

## 3. Matching rule (the core behavior)

For every item in the export:
- **id ∈ minutes follow-up refs** → `source = "Meeting KW<NN-1>"`, the follow-up text becomes the shown
  comment (marked with a `»` accent + `[Meeting KW..]` tag in the deck). This is why empty CALM comments
  still produce a meaningful status line.
- **otherwise** → `source = "CALM"`, carried over as-is: latest `Kommentare` (fallback `Historie`,
  then `Beschreibung`).

The AI step turns each item's `raw` text into one concise line (`summary`). Nothing is written back to CALM.

## 4. Outputs

- `.status_work/KW<NN>.json` – prepared data (per-team items, each with `raw`, `source`, `summary:null`).
- `.status_work/KW<NN>.summaries.json` – `{ "3-1234": "one-line summary", … }` written by the AI step.
- `<Customer>_InterfaceStatus_StatusMeeting_KW<NN>.pptx` – the deck (deterministic name → idempotent).
